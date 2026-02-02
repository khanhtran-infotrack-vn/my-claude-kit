# .NET Core / ASP.NET Core Development

Comprehensive guide for building production-ready backend systems with .NET 8/9, ASP.NET Core, Entity Framework Core, and modern C# patterns (2025).

## When to Use .NET

| Need | .NET Excels |
|------|-------------|
| Enterprise applications | Strong typing, mature tooling |
| High performance APIs | Kestrel server benchmarks top |
| Windows ecosystem | Native integration |
| Cross-platform services | .NET Core runs everywhere |
| Microservices | gRPC, minimal APIs |
| Real-time apps | SignalR built-in |

## Project Structure (Clean Architecture)

```
src/
├── Domain/                    # Enterprise business rules
│   ├── Entities/
│   ├── ValueObjects/
│   ├── Events/
│   └── Interfaces/
├── Application/               # Application business rules
│   ├── Common/
│   │   ├── Behaviors/        # MediatR pipeline behaviors
│   │   ├── Interfaces/
│   │   └── Mappings/
│   ├── Features/
│   │   └── Users/
│   │       ├── Commands/
│   │       └── Queries/
│   └── DependencyInjection.cs
├── Infrastructure/            # External concerns
│   ├── Persistence/
│   │   ├── Configurations/   # EF Core configs
│   │   └── Repositories/
│   ├── Services/
│   └── DependencyInjection.cs
└── WebApi/                    # Presentation layer
    ├── Controllers/
    ├── Middleware/
    └── Program.cs
```

## SOLID Principles in C#/.NET

### Single Responsibility Principle (SRP)

```csharp
// BAD - Class does too much
public class UserService
{
    public void CreateUser(User user) { /* ... */ }
    public void SendWelcomeEmail(User user) { /* ... */ }
    public void LogUserCreation(User user) { /* ... */ }
}

// GOOD - Separate concerns
public class UserService
{
    private readonly IUserRepository _userRepository;
    private readonly IEmailService _emailService;
    private readonly ILogger<UserService> _logger;

    public UserService(
        IUserRepository userRepository,
        IEmailService emailService,
        ILogger<UserService> logger)
    {
        _userRepository = userRepository;
        _emailService = emailService;
        _logger = logger;
    }

    public async Task<User> CreateUserAsync(CreateUserRequest request)
    {
        var user = new User(request.Email, request.Name);
        await _userRepository.AddAsync(user);

        _logger.LogInformation("User {UserId} created", user.Id);
        await _emailService.SendWelcomeEmailAsync(user);

        return user;
    }
}
```

### Open/Closed Principle (OCP)

```csharp
// Define abstraction
public interface IPaymentProcessor
{
    Task<PaymentResult> ProcessAsync(decimal amount, CancellationToken ct = default);
}

// Implementations are open for extension
public class StripePaymentProcessor : IPaymentProcessor
{
    public async Task<PaymentResult> ProcessAsync(decimal amount, CancellationToken ct = default)
    {
        // Stripe-specific implementation
        return new PaymentResult { Success = true };
    }
}

public class PayPalPaymentProcessor : IPaymentProcessor
{
    public async Task<PaymentResult> ProcessAsync(decimal amount, CancellationToken ct = default)
    {
        // PayPal-specific implementation
        return new PaymentResult { Success = true };
    }
}

// Usage - closed for modification
public class OrderService
{
    private readonly IPaymentProcessor _paymentProcessor;

    public OrderService(IPaymentProcessor paymentProcessor)
    {
        _paymentProcessor = paymentProcessor;
    }

    public async Task<Order> ProcessOrderAsync(Order order)
    {
        var result = await _paymentProcessor.ProcessAsync(order.Total);
        order.MarkAsPaid(result.TransactionId);
        return order;
    }
}
```

### Liskov Substitution Principle (LSP)

```csharp
// Correct interface segregation ensures LSP
public interface IReadableRepository<T> where T : class
{
    Task<T?> GetByIdAsync(Guid id);
    Task<IEnumerable<T>> GetAllAsync();
}

public interface IWritableRepository<T> where T : class
{
    Task AddAsync(T entity);
    Task UpdateAsync(T entity);
    Task DeleteAsync(T entity);
}

public interface IRepository<T> : IReadableRepository<T>, IWritableRepository<T>
    where T : class { }

// Read-only repository (e.g., for reports)
public class ReportRepository : IReadableRepository<Report>
{
    public Task<Report?> GetByIdAsync(Guid id) { /* ... */ }
    public Task<IEnumerable<Report>> GetAllAsync() { /* ... */ }
}

// Full CRUD repository
public class UserRepository : IRepository<User>
{
    public Task<User?> GetByIdAsync(Guid id) { /* ... */ }
    public Task<IEnumerable<User>> GetAllAsync() { /* ... */ }
    public Task AddAsync(User entity) { /* ... */ }
    public Task UpdateAsync(User entity) { /* ... */ }
    public Task DeleteAsync(User entity) { /* ... */ }
}
```

### Interface Segregation Principle (ISP)

```csharp
// BAD - Fat interface
public interface IWorker
{
    void Work();
    void Eat();
    void Sleep();
}

// GOOD - Segregated interfaces
public interface IWorkable { void Work(); }
public interface IFeedable { void Eat(); }
public interface ISleepable { void Sleep(); }

public class Human : IWorkable, IFeedable, ISleepable
{
    public void Work() { /* ... */ }
    public void Eat() { /* ... */ }
    public void Sleep() { /* ... */ }
}

public class Robot : IWorkable
{
    public void Work() { /* ... */ }
}
```

### Dependency Inversion Principle (DIP)

```csharp
// High-level modules depend on abstractions
public interface IEmailSender
{
    Task SendAsync(string to, string subject, string body);
}

public interface IUserRepository
{
    Task<User?> GetByIdAsync(Guid id);
    Task AddAsync(User user);
}

// Low-level modules implement abstractions
public class SmtpEmailSender : IEmailSender
{
    public async Task SendAsync(string to, string subject, string body)
    {
        // SMTP implementation
    }
}

// DI registration in Program.cs
builder.Services.AddScoped<IEmailSender, SmtpEmailSender>();
builder.Services.AddScoped<IUserRepository, SqlUserRepository>();
```

## ASP.NET Core API Architecture

### Controller-Based vs Minimal APIs

**Use Controller-Based Architecture (Recommended)** for:
- Enterprise applications with complex business logic
- Projects requiring strong separation of concerns
- Teams familiar with MVC/Web API patterns
- Applications needing advanced features: action filters, model binding, comprehensive validation
- When you need extensive OpenAPI/Swagger documentation
- Better testability with dependency injection
- Large teams requiring consistent code organization

**Use Minimal APIs** only for:
- Microservices with simple CRUD operations
- Prototypes and proof-of-concepts
- Lightweight APIs with few endpoints
- Performance-critical scenarios where routing overhead matters

## ASP.NET Core Controller-Based APIs

**Prefer Controller-based architecture over Minimal APIs** for enterprise applications requiring:
- Separation of concerns and testability
- Complex routing and parameter binding
- Action filters and middleware
- OpenAPI/Swagger with detailed documentation

```csharp
[ApiController]
[Route("api/[controller]")]
public sealed class UsersController : ControllerBase
{
    private readonly IMediator _mediator;
    private readonly ILogger<UsersController> _logger;

    public UsersController(IMediator mediator, ILogger<UsersController> logger)
    {
        _mediator = mediator;
        _logger = logger;
    }

    /// <summary>
    /// Retrieves all users
    /// </summary>
    /// <returns>List of users</returns>
    [HttpGet]
    [ProducesResponseType(typeof(IEnumerable<UserDto>), StatusCodes.Status200OK)]
    public async Task<ActionResult<IEnumerable<UserDto>>> GetUsers(CancellationToken ct)
    {
        var query = new GetAllUsersQuery();
        var result = await _mediator.Send(query, ct);
        return Ok(result);
    }

    /// <summary>
    /// Retrieves a user by ID
    /// </summary>
    /// <param name="id">User ID</param>
    /// <param name="ct">Cancellation token</param>
    /// <returns>User details</returns>
    [HttpGet("{id:guid}")]
    [ProducesResponseType(typeof(UserDto), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<ActionResult<UserDto>> GetUser(Guid id, CancellationToken ct)
    {
        var query = new GetUserByIdQuery(id);
        var result = await _mediator.Send(query, ct);
        return result is not null ? Ok(result) : NotFound();
    }

    /// <summary>
    /// Creates a new user
    /// </summary>
    /// <param name="command">User creation details</param>
    /// <param name="ct">Cancellation token</param>
    /// <returns>Created user</returns>
    [HttpPost]
    [ProducesResponseType(typeof(UserDto), StatusCodes.Status201Created)]
    [ProducesResponseType(StatusCodes.Status400BadRequest)]
    public async Task<ActionResult<UserDto>> CreateUser(
        CreateUserCommand command,
        CancellationToken ct)
    {
        var result = await _mediator.Send(command, ct);
        return CreatedAtAction(
            nameof(GetUser),
            new { id = result.Id },
            result);
    }

    /// <summary>
    /// Updates an existing user
    /// </summary>
    [HttpPut("{id:guid}")]
    [ProducesResponseType(StatusCodes.Status204NoContent)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<IActionResult> UpdateUser(
        Guid id,
        UpdateUserCommand command,
        CancellationToken ct)
    {
        if (id != command.Id)
            return BadRequest("ID mismatch");

        var result = await _mediator.Send(command, ct);
        return result.IsSuccess ? NoContent() : NotFound(result.Error);
    }

    /// <summary>
    /// Deletes a user
    /// </summary>
    [HttpDelete("{id:guid}")]
    [ProducesResponseType(StatusCodes.Status204NoContent)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<IActionResult> DeleteUser(Guid id, CancellationToken ct)
    {
        var command = new DeleteUserCommand(id);
        var result = await _mediator.Send(command, ct);
        return result.IsSuccess ? NoContent() : NotFound(result.Error);
    }
}
```

### Program.cs Setup for Controllers

```csharp
var builder = WebApplication.CreateBuilder(args);

// Add services
builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(options =>
{
    options.SwaggerDoc("v1", new OpenApiInfo
    {
        Title = "My API",
        Version = "v1"
    });
    // Enable XML comments for Swagger
    var xmlFile = $"{Assembly.GetExecutingAssembly().GetName().Name}.xml";
    var xmlPath = Path.Combine(AppContext.BaseDirectory, xmlFile);
    options.IncludeXmlComments(xmlPath);
});

builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseNpgsql(builder.Configuration.GetConnectionString("Default")));

var app = builder.Build();

// Configure middleware
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();
app.UseAuthentication();
app.UseAuthorization();
app.MapControllers(); // Map controller routes

app.Run();
```

## Entity Framework Core

### DbContext Configuration

```csharp
public class AppDbContext : DbContext
{
    public AppDbContext(DbContextOptions<AppDbContext> options) : base(options) { }

    public DbSet<User> Users => Set<User>();
    public DbSet<Order> Orders => Set<Order>();
    public DbSet<Product> Products => Set<Product>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.ApplyConfigurationsFromAssembly(typeof(AppDbContext).Assembly);
    }

    public override async Task<int> SaveChangesAsync(CancellationToken cancellationToken = default)
    {
        // Audit trail
        foreach (var entry in ChangeTracker.Entries<BaseEntity>())
        {
            switch (entry.State)
            {
                case EntityState.Added:
                    entry.Entity.CreatedAt = DateTime.UtcNow;
                    break;
                case EntityState.Modified:
                    entry.Entity.UpdatedAt = DateTime.UtcNow;
                    break;
            }
        }
        return await base.SaveChangesAsync(cancellationToken);
    }
}
```

### Entity Configuration (Fluent API)

```csharp
public class UserConfiguration : IEntityTypeConfiguration<User>
{
    public void Configure(EntityTypeBuilder<User> builder)
    {
        builder.ToTable("Users");

        builder.HasKey(u => u.Id);

        builder.Property(u => u.Email)
            .IsRequired()
            .HasMaxLength(256);

        builder.HasIndex(u => u.Email)
            .IsUnique();

        builder.Property(u => u.Name)
            .IsRequired()
            .HasMaxLength(100);

        // Value object mapping
        builder.OwnsOne(u => u.Address, address =>
        {
            address.Property(a => a.Street).HasMaxLength(200);
            address.Property(a => a.City).HasMaxLength(100);
            address.Property(a => a.PostalCode).HasMaxLength(20);
        });

        // Relationships
        builder.HasMany(u => u.Orders)
            .WithOne(o => o.User)
            .HasForeignKey(o => o.UserId)
            .OnDelete(DeleteBehavior.Cascade);
    }
}
```

### Repository Pattern with EF Core

```csharp
public interface IRepository<T> where T : class
{
    Task<T?> GetByIdAsync(Guid id, CancellationToken ct = default);
    Task<IReadOnlyList<T>> GetAllAsync(CancellationToken ct = default);
    Task<T> AddAsync(T entity, CancellationToken ct = default);
    Task UpdateAsync(T entity, CancellationToken ct = default);
    Task DeleteAsync(T entity, CancellationToken ct = default);
}

public class Repository<T> : IRepository<T> where T : class
{
    protected readonly AppDbContext _context;
    protected readonly DbSet<T> _dbSet;

    public Repository(AppDbContext context)
    {
        _context = context;
        _dbSet = context.Set<T>();
    }

    public virtual async Task<T?> GetByIdAsync(Guid id, CancellationToken ct = default)
        => await _dbSet.FindAsync([id], ct);

    public virtual async Task<IReadOnlyList<T>> GetAllAsync(CancellationToken ct = default)
        => await _dbSet.ToListAsync(ct);

    public virtual async Task<T> AddAsync(T entity, CancellationToken ct = default)
    {
        await _dbSet.AddAsync(entity, ct);
        await _context.SaveChangesAsync(ct);
        return entity;
    }

    public virtual async Task UpdateAsync(T entity, CancellationToken ct = default)
    {
        _dbSet.Update(entity);
        await _context.SaveChangesAsync(ct);
    }

    public virtual async Task DeleteAsync(T entity, CancellationToken ct = default)
    {
        _dbSet.Remove(entity);
        await _context.SaveChangesAsync(ct);
    }
}
```

## MediatR / CQRS Pattern

### Command Example

```csharp
// Command
public record CreateUserCommand(string Email, string Name) : IRequest<UserDto>;

// Handler
public class CreateUserCommandHandler : IRequestHandler<CreateUserCommand, UserDto>
{
    private readonly IUserRepository _userRepository;
    private readonly IMapper _mapper;

    public CreateUserCommandHandler(IUserRepository userRepository, IMapper mapper)
    {
        _userRepository = userRepository;
        _mapper = mapper;
    }

    public async Task<UserDto> Handle(CreateUserCommand request, CancellationToken ct)
    {
        var user = new User(request.Email, request.Name);
        await _userRepository.AddAsync(user, ct);
        return _mapper.Map<UserDto>(user);
    }
}
```

### Query Example

```csharp
// Query
public record GetUserByIdQuery(Guid Id) : IRequest<UserDto?>;

// Handler
public class GetUserByIdQueryHandler : IRequestHandler<GetUserByIdQuery, UserDto?>
{
    private readonly IUserRepository _userRepository;
    private readonly IMapper _mapper;

    public GetUserByIdQueryHandler(IUserRepository userRepository, IMapper mapper)
    {
        _userRepository = userRepository;
        _mapper = mapper;
    }

    public async Task<UserDto?> Handle(GetUserByIdQuery request, CancellationToken ct)
    {
        var user = await _userRepository.GetByIdAsync(request.Id, ct);
        return user is null ? null : _mapper.Map<UserDto>(user);
    }
}
```

### Pipeline Behaviors (Cross-Cutting Concerns)

```csharp
// Validation behavior
public class ValidationBehavior<TRequest, TResponse> : IPipelineBehavior<TRequest, TResponse>
    where TRequest : IRequest<TResponse>
{
    private readonly IEnumerable<IValidator<TRequest>> _validators;

    public ValidationBehavior(IEnumerable<IValidator<TRequest>> validators)
    {
        _validators = validators;
    }

    public async Task<TResponse> Handle(
        TRequest request,
        RequestHandlerDelegate<TResponse> next,
        CancellationToken ct)
    {
        if (_validators.Any())
        {
            var context = new ValidationContext<TRequest>(request);
            var results = await Task.WhenAll(
                _validators.Select(v => v.ValidateAsync(context, ct)));

            var failures = results
                .SelectMany(r => r.Errors)
                .Where(f => f is not null)
                .ToList();

            if (failures.Count > 0)
                throw new ValidationException(failures);
        }
        return await next();
    }
}

// Logging behavior
public class LoggingBehavior<TRequest, TResponse> : IPipelineBehavior<TRequest, TResponse>
    where TRequest : IRequest<TResponse>
{
    private readonly ILogger<LoggingBehavior<TRequest, TResponse>> _logger;

    public LoggingBehavior(ILogger<LoggingBehavior<TRequest, TResponse>> logger)
    {
        _logger = logger;
    }

    public async Task<TResponse> Handle(
        TRequest request,
        RequestHandlerDelegate<TResponse> next,
        CancellationToken ct)
    {
        _logger.LogInformation("Handling {RequestName}", typeof(TRequest).Name);
        var response = await next();
        _logger.LogInformation("Handled {RequestName}", typeof(TRequest).Name);
        return response;
    }
}
```

## Dependency Injection Setup

```csharp
// Program.cs
var builder = WebApplication.CreateBuilder(args);

// Infrastructure
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseNpgsql(builder.Configuration.GetConnectionString("Default")));

// Repositories
builder.Services.AddScoped(typeof(IRepository<>), typeof(Repository<>));
builder.Services.AddScoped<IUserRepository, UserRepository>();

// MediatR
builder.Services.AddMediatR(cfg => {
    cfg.RegisterServicesFromAssembly(typeof(CreateUserCommand).Assembly);
    cfg.AddBehavior(typeof(IPipelineBehavior<,>), typeof(ValidationBehavior<,>));
    cfg.AddBehavior(typeof(IPipelineBehavior<,>), typeof(LoggingBehavior<,>));
});

// AutoMapper
builder.Services.AddAutoMapper(typeof(MappingProfile).Assembly);

// FluentValidation
builder.Services.AddValidatorsFromAssembly(typeof(CreateUserCommandValidator).Assembly);

// Authentication
builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options =>
    {
        options.TokenValidationParameters = new TokenValidationParameters
        {
            ValidateIssuer = true,
            ValidateAudience = true,
            ValidateLifetime = true,
            ValidateIssuerSigningKey = true,
            ValidIssuer = builder.Configuration["Jwt:Issuer"],
            ValidAudience = builder.Configuration["Jwt:Audience"],
            IssuerSigningKey = new SymmetricSecurityKey(
                Encoding.UTF8.GetBytes(builder.Configuration["Jwt:Key"]!))
        };
    });

builder.Services.AddAuthorization();
```

## Testing with xUnit

### Unit Test Example

```csharp
public class CreateUserCommandHandlerTests
{
    private readonly Mock<IUserRepository> _userRepositoryMock;
    private readonly Mock<IMapper> _mapperMock;
    private readonly CreateUserCommandHandler _handler;

    public CreateUserCommandHandlerTests()
    {
        _userRepositoryMock = new Mock<IUserRepository>();
        _mapperMock = new Mock<IMapper>();
        _handler = new CreateUserCommandHandler(
            _userRepositoryMock.Object,
            _mapperMock.Object);
    }

    [Fact]
    public async Task Handle_ValidCommand_ReturnsUserDto()
    {
        // Arrange
        var command = new CreateUserCommand("test@example.com", "Test User");
        var expectedDto = new UserDto { Email = command.Email, Name = command.Name };

        _mapperMock.Setup(m => m.Map<UserDto>(It.IsAny<User>()))
            .Returns(expectedDto);

        // Act
        var result = await _handler.Handle(command, CancellationToken.None);

        // Assert
        Assert.NotNull(result);
        Assert.Equal(command.Email, result.Email);
        _userRepositoryMock.Verify(r => r.AddAsync(
            It.Is<User>(u => u.Email == command.Email),
            It.IsAny<CancellationToken>()), Times.Once);
    }
}
```

### Integration Test with WebApplicationFactory

```csharp
public class UsersApiTests : IClassFixture<WebApplicationFactory<Program>>
{
    private readonly HttpClient _client;
    private readonly WebApplicationFactory<Program> _factory;

    public UsersApiTests(WebApplicationFactory<Program> factory)
    {
        _factory = factory.WithWebHostBuilder(builder =>
        {
            builder.ConfigureServices(services =>
            {
                // Replace real DB with in-memory
                var descriptor = services.SingleOrDefault(
                    d => d.ServiceType == typeof(DbContextOptions<AppDbContext>));
                if (descriptor != null)
                    services.Remove(descriptor);

                services.AddDbContext<AppDbContext>(options =>
                    options.UseInMemoryDatabase("TestDb"));
            });
        });
        _client = _factory.CreateClient();
    }

    [Fact]
    public async Task GetUsers_ReturnsSuccessStatusCode()
    {
        // Act
        var response = await _client.GetAsync("/api/users");

        // Assert
        response.EnsureSuccessStatusCode();
    }

    [Fact]
    public async Task CreateUser_ValidRequest_ReturnsCreated()
    {
        // Arrange
        var request = new { Email = "test@example.com", Name = "Test User" };
        var content = new StringContent(
            JsonSerializer.Serialize(request),
            Encoding.UTF8,
            "application/json");

        // Act
        var response = await _client.PostAsync("/api/users", content);

        // Assert
        Assert.Equal(HttpStatusCode.Created, response.StatusCode);
    }
}
```

## Performance Best Practices

### Async/Await Patterns

```csharp
// Good - Async all the way
public async Task<IActionResult> GetUsersAsync()
{
    var users = await _userService.GetAllAsync();
    return Ok(users);
}

// Avoid - Blocking calls
public IActionResult GetUsers()
{
    var users = _userService.GetAllAsync().Result; // DEADLOCK RISK
    return Ok(users);
}

// Use CancellationToken
public async Task<User?> GetUserAsync(Guid id, CancellationToken ct)
{
    return await _dbContext.Users
        .AsNoTracking() // Read-only query optimization
        .FirstOrDefaultAsync(u => u.Id == id, ct);
}
```

### Query Optimization

```csharp
// Project only needed columns
var userDtos = await _dbContext.Users
    .Where(u => u.IsActive)
    .Select(u => new UserDto { Id = u.Id, Name = u.Name })
    .ToListAsync();

// Use compiled queries for hot paths
private static readonly Func<AppDbContext, Guid, Task<User?>> GetUserById =
    EF.CompileAsyncQuery((AppDbContext db, Guid id) =>
        db.Users.FirstOrDefault(u => u.Id == id));

// Pagination
var pagedUsers = await _dbContext.Users
    .OrderBy(u => u.CreatedAt)
    .Skip((pageNumber - 1) * pageSize)
    .Take(pageSize)
    .ToListAsync();
```

## Resources

- **ASP.NET Core Docs:** https://learn.microsoft.com/aspnet/core
- **EF Core Docs:** https://learn.microsoft.com/ef/core
- **Clean Architecture:** https://github.com/jasontaylordev/CleanArchitecture
- **MediatR:** https://github.com/jbogard/MediatR
- **FluentValidation:** https://docs.fluentvalidation.net
