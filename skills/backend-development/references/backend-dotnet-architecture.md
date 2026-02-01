# .NET Clean Architecture with CQRS

Clean Architecture with separated projects, MediatR, and CQRS patterns for .NET 8+.

## Project Structure

```
Solution.sln
├── src/
│   ├── MyApp.Domain/           # Entities, value objects, domain events (no dependencies)
│   ├── MyApp.Application/      # MediatR handlers, DTOs, validators (refs Domain)
│   ├── MyApp.Infrastructure/   # EF Core, repositories, services (refs Domain + Application)
│   └── MyApp.Web/              # Controllers, composition root (refs Application + Infrastructure)
└── tests/
    ├── MyApp.Domain.Tests/
    ├── MyApp.Application.Tests/
    └── MyApp.Integration.Tests/
```

**Dependency Direction:** Domain → Application → Infrastructure → Web

## Core Principles

Follow **YAGNI**, **KISS**, **DRY**, and **SOLID**:
- All classes `sealed` unless designed for inheritance
- Result<T> pattern over exceptions for business logic
- All async with `CancellationToken`
- Structured logging with `{PropertyName}` syntax

## Domain Layer

```csharp
// Entities with encapsulation
public class Product
{
    public int Id { get; private set; }
    public string Name { get; private set; } = string.Empty;
    public decimal Price { get; private set; }

    private Product() { } // EF Core

    public static Product Create(string name, decimal price)
    {
        if (price <= 0) throw new DomainException("Price must be positive");
        return new Product { Name = name, Price = price, CreatedAt = DateTime.UtcNow };
    }
}
```

## Application Layer - Commands

```csharp
// Command
public sealed record CreateProductCommand(
    string Name, string Description, decimal Price, int CategoryId
) : IRequest<Result<ProductDto>>;

// Handler
public sealed class CreateProductCommandHandler
    : IRequestHandler<CreateProductCommand, Result<ProductDto>>
{
    private readonly IApplicationDbContext _context;
    private readonly ILogger<CreateProductCommandHandler> _logger;

    public async Task<Result<ProductDto>> Handle(
        CreateProductCommand request, CancellationToken ct)
    {
        var product = Product.Create(request.Name, request.Description,
            request.Price, request.CategoryId);

        _context.Products.Add(product);
        await _context.SaveChangesAsync(ct);

        _logger.LogInformation("Created product {ProductId}", product.Id);
        return Result.Success(product.ToDto());
    }
}

// Validator
public sealed class CreateProductCommandValidator : AbstractValidator<CreateProductCommand>
{
    public CreateProductCommandValidator()
    {
        RuleFor(x => x.Name).NotEmpty().MaximumLength(100);
        RuleFor(x => x.Price).GreaterThan(0).LessThan(1000000);
    }
}
```

## Application Layer - Queries

```csharp
public sealed record GetProductsQuery(
    int Page = 1, int PageSize = 10, string? SearchTerm = null
) : IRequest<Result<PagedResult<ProductDto>>>;

public sealed class GetProductsQueryHandler
    : IRequestHandler<GetProductsQuery, Result<PagedResult<ProductDto>>>
{
    private readonly IApplicationDbContext _context;

    public async Task<Result<PagedResult<ProductDto>>> Handle(
        GetProductsQuery request, CancellationToken ct)
    {
        var query = _context.Products.AsNoTracking().Include(p => p.Category);

        if (!string.IsNullOrWhiteSpace(request.SearchTerm))
            query = query.Where(p => p.Name.Contains(request.SearchTerm));

        var totalCount = await query.CountAsync(ct);
        var items = await query
            .Skip((request.Page - 1) * request.PageSize)
            .Take(request.PageSize)
            .Select(p => new ProductDto(p.Id, p.Name, p.Price, p.Category.Name))
            .ToListAsync(ct);

        return Result.Success(new PagedResult<ProductDto>(items, totalCount, request.Page, request.PageSize));
    }
}
```

## Pipeline Behaviors

```csharp
// Validation behavior
public sealed class ValidationBehavior<TRequest, TResponse>
    : IPipelineBehavior<TRequest, TResponse>
{
    private readonly IEnumerable<IValidator<TRequest>> _validators;

    public async Task<TResponse> Handle(TRequest request,
        RequestHandlerDelegate<TResponse> next, CancellationToken ct)
    {
        if (!_validators.Any()) return await next();

        var context = new ValidationContext<TRequest>(request);
        var failures = (await Task.WhenAll(_validators.Select(v => v.ValidateAsync(context, ct))))
            .SelectMany(r => r.Errors).Where(f => f != null).ToList();

        if (failures.Count != 0) throw new ValidationException(failures);
        return await next();
    }
}
```

## Dependency Injection Setup

```csharp
// Application/DependencyInjection.cs
public static IServiceCollection AddApplication(this IServiceCollection services)
{
    services.AddMediatR(cfg => cfg.RegisterServicesFromAssembly(Assembly.GetExecutingAssembly()));
    services.AddValidatorsFromAssembly(Assembly.GetExecutingAssembly());
    services.AddTransient(typeof(IPipelineBehavior<,>), typeof(ValidationBehavior<,>));
    return services;
}

// Infrastructure/DependencyInjection.cs
public static IServiceCollection AddInfrastructure(this IServiceCollection services, IConfiguration config)
{
    services.AddDbContext<ApplicationDbContext>(options =>
        options.UseSqlServer(config.GetConnectionString("DefaultConnection")));
    services.AddScoped<IApplicationDbContext>(p => p.GetRequiredService<ApplicationDbContext>());
    return services;
}
```

## Quick Reference

| Pattern | Purpose |
|---------|---------|
| Separated Projects | Each layer is separate .csproj |
| `IRequest<T>` | MediatR command/query interface |
| `IRequestHandler<TReq, TRes>` | Handler implementation |
| `IPipelineBehavior<,>` | Cross-cutting concerns |
| `Result<T>` | Explicit success/failure |
| `sealed` classes | Default for all new classes |
| `CancellationToken` | All async methods |
