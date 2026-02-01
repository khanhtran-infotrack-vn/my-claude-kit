# .NET Authentication & Authorization

JWT authentication with ASP.NET Core following Clean Architecture.

## Domain Layer

```csharp
public class User
{
    public int Id { get; private set; }
    public string Email { get; private set; } = string.Empty;
    public string PasswordHash { get; private set; } = string.Empty;
    public List<string> Roles { get; private set; } = new();
    public bool IsActive { get; private set; } = true;

    private User() { } // EF Core

    public static User Create(string email, string passwordHash, string firstName, string lastName)
    {
        return new User
        {
            Email = email,
            PasswordHash = passwordHash,
            Roles = new List<string> { "User" },
            CreatedAt = DateTime.UtcNow
        };
    }

    public void AddRole(string role)
    {
        if (!Roles.Contains(role)) Roles.Add(role);
    }
}
```

## Application Layer - Interfaces

```csharp
public interface IJwtService
{
    string GenerateToken(int userId, string email, List<string> roles);
    int? ValidateToken(string token);
}

public interface IPasswordHasher
{
    string HashPassword(string password);
    bool VerifyPassword(string password, string hash);
}

public interface ICurrentUserService
{
    int? UserId { get; }
    string? Email { get; }
    bool IsAuthenticated { get; }
    bool IsInRole(string role);
}
```

## Application Layer - Commands

```csharp
public sealed record RegisterCommand(
    string Email, string Password, string FirstName, string LastName
) : IRequest<Result<AuthResponse>>;

public sealed class RegisterCommandHandler : IRequestHandler<RegisterCommand, Result<AuthResponse>>
{
    private readonly IApplicationDbContext _context;
    private readonly IPasswordHasher _passwordHasher;
    private readonly IJwtService _jwtService;

    public async Task<Result<AuthResponse>> Handle(RegisterCommand request, CancellationToken ct)
    {
        if (await _context.Users.AnyAsync(u => u.Email == request.Email, ct))
            return Result.Failure<AuthResponse>("Email already registered");

        var hash = _passwordHasher.HashPassword(request.Password);
        var user = User.Create(request.Email, hash, request.FirstName, request.LastName);

        _context.Users.Add(user);
        await _context.SaveChangesAsync(ct);

        var token = _jwtService.GenerateToken(user.Id, user.Email, user.Roles);
        return Result.Success(new AuthResponse(token, user.Email, user.FirstName, user.LastName));
    }
}

public sealed record LoginCommand(string Email, string Password) : IRequest<Result<AuthResponse>>;

public sealed class LoginCommandHandler : IRequestHandler<LoginCommand, Result<AuthResponse>>
{
    public async Task<Result<AuthResponse>> Handle(LoginCommand request, CancellationToken ct)
    {
        var user = await _context.Users.FirstOrDefaultAsync(u => u.Email == request.Email, ct);

        if (user is null || !_passwordHasher.VerifyPassword(request.Password, user.PasswordHash))
            return Result.Failure<AuthResponse>("Invalid credentials");

        if (!user.IsActive)
            return Result.Failure<AuthResponse>("Account is inactive");

        var token = _jwtService.GenerateToken(user.Id, user.Email, user.Roles);
        return Result.Success(new AuthResponse(token, user.Email, user.FirstName, user.LastName));
    }
}

public sealed record AuthResponse(string Token, string Email, string FirstName, string LastName);
```

## Infrastructure Layer - JWT Service

```csharp
public sealed class JwtSettings
{
    public string Secret { get; init; } = string.Empty;
    public string Issuer { get; init; } = string.Empty;
    public string Audience { get; init; } = string.Empty;
    public int ExpirationMinutes { get; init; } = 60;
}

public sealed class JwtService : IJwtService
{
    private readonly JwtSettings _settings;

    public string GenerateToken(int userId, string email, List<string> roles)
    {
        var claims = new List<Claim>
        {
            new(JwtRegisteredClaimNames.Sub, userId.ToString()),
            new(JwtRegisteredClaimNames.Email, email),
            new(JwtRegisteredClaimNames.Jti, Guid.NewGuid().ToString()),
        };
        claims.AddRange(roles.Select(role => new Claim(ClaimTypes.Role, role)));

        var key = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(_settings.Secret));
        var token = new JwtSecurityToken(
            issuer: _settings.Issuer,
            audience: _settings.Audience,
            claims: claims,
            expires: DateTime.UtcNow.AddMinutes(_settings.ExpirationMinutes),
            signingCredentials: new SigningCredentials(key, SecurityAlgorithms.HmacSha256));

        return new JwtSecurityTokenHandler().WriteToken(token);
    }
}
```

## Infrastructure Layer - Password Hasher

```csharp
public sealed class PasswordHasher : IPasswordHasher
{
    private const int SaltSize = 16;
    private const int HashSize = 32;
    private const int Iterations = 100000;

    public string HashPassword(string password)
    {
        using var rng = RandomNumberGenerator.Create();
        var salt = new byte[SaltSize];
        rng.GetBytes(salt);

        using var pbkdf2 = new Rfc2898DeriveBytes(password, salt, Iterations, HashAlgorithmName.SHA256);
        var hash = pbkdf2.GetBytes(HashSize);

        var hashBytes = new byte[SaltSize + HashSize];
        Array.Copy(salt, 0, hashBytes, 0, SaltSize);
        Array.Copy(hash, 0, hashBytes, SaltSize, HashSize);
        return Convert.ToBase64String(hashBytes);
    }

    public bool VerifyPassword(string password, string hash)
    {
        var hashBytes = Convert.FromBase64String(hash);
        var salt = new byte[SaltSize];
        Array.Copy(hashBytes, 0, salt, 0, SaltSize);

        using var pbkdf2 = new Rfc2898DeriveBytes(password, salt, Iterations, HashAlgorithmName.SHA256);
        var testHash = pbkdf2.GetBytes(HashSize);

        for (int i = 0; i < HashSize; i++)
            if (hashBytes[i + SaltSize] != testHash[i]) return false;
        return true;
    }
}
```

## Web Layer - Auth Controller

```csharp
[ApiController]
[Route("api/[controller]")]
public sealed class AuthController : ControllerBase
{
    private readonly IMediator _mediator;
    private readonly ICurrentUserService _currentUser;

    [HttpPost("register")]
    [AllowAnonymous]
    public async Task<IActionResult> Register(RegisterCommand command, CancellationToken ct)
    {
        var result = await _mediator.Send(command, ct);
        return result.IsSuccess ? Ok(result.Value) : BadRequest(result.Error);
    }

    [HttpPost("login")]
    [AllowAnonymous]
    public async Task<IActionResult> Login(LoginCommand command, CancellationToken ct)
    {
        var result = await _mediator.Send(command, ct);
        return result.IsSuccess ? Ok(result.Value) : BadRequest(result.Error);
    }

    [HttpGet("me")]
    [Authorize]
    public IActionResult GetCurrentUser()
    {
        return Ok(new { UserId = _currentUser.UserId, Email = _currentUser.Email });
    }
}
```

## Program.cs Configuration

```csharp
builder.Services.Configure<JwtSettings>(builder.Configuration.GetSection("JwtSettings"));
var jwtSettings = builder.Configuration.GetSection("JwtSettings").Get<JwtSettings>()!;

builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options =>
    {
        options.TokenValidationParameters = new TokenValidationParameters
        {
            ValidateIssuerSigningKey = true,
            IssuerSigningKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(jwtSettings.Secret)),
            ValidateIssuer = true,
            ValidIssuer = jwtSettings.Issuer,
            ValidateAudience = true,
            ValidAudience = jwtSettings.Audience,
            ValidateLifetime = true,
            ClockSkew = TimeSpan.Zero
        };
    });

builder.Services.AddAuthorization(options =>
{
    options.AddPolicy("AdminOnly", policy => policy.RequireRole("Admin"));
    options.AddPolicy("UserOrAdmin", policy => policy.RequireRole("User", "Admin"));
});

// Middleware order matters
app.UseAuthentication();
app.UseAuthorization();
```

## appsettings.json

```json
{
  "JwtSettings": {
    "Secret": "your-super-secret-key-minimum-32-characters-long",
    "Issuer": "MyApp",
    "Audience": "MyAppUsers",
    "ExpirationMinutes": 60
  }
}
```

## Quick Reference

| Pattern | Usage |
|---------|-------|
| `[Authorize]` | Requires authentication |
| `[Authorize(Roles = "Admin")]` | Requires role |
| `[Authorize(Policy = "PolicyName")]` | Custom policy |
| `[AllowAnonymous]` | Skip authentication |
| `ICurrentUserService` | Access current user |
| `Result<T>` | Explicit success/failure |
| PBKDF2/SHA256 | Password hashing |
| JWT Bearer | Token authentication |
