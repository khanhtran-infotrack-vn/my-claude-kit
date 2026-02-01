# Clean Architecture with CQRS

## Project Structure (Separated Layers)

```
Solution.sln
├── src/
│   ├── MyApp.Domain/                      # Domain Layer (separate project)
│   │   ├── Entities/
│   │   │   ├── Product.cs
│   │   │   ├── Category.cs
│   │   │   └── Order.cs
│   │   ├── ValueObjects/
│   │   │   ├── Email.cs
│   │   │   └── Money.cs
│   │   ├── Exceptions/
│   │   │   └── DomainException.cs
│   │   ├── Events/
│   │   │   └── OrderCreatedEvent.cs
│   │   └── MyApp.Domain.csproj
│   │
│   ├── MyApp.Application/                 # Application Layer (separate project)
│   │   ├── Common/
│   │   │   ├── Interfaces/
│   │   │   │   └── IApplicationDbContext.cs
│   │   │   ├── Behaviors/
│   │   │   │   ├── ValidationBehavior.cs
│   │   │   │   └── LoggingBehavior.cs
│   │   │   └── Models/
│   │   │       └── PagedResult.cs
│   │   ├── Products/
│   │   │   ├── Commands/
│   │   │   │   ├── CreateProduct/
│   │   │   │   │   ├── CreateProductCommand.cs
│   │   │   │   │   ├── CreateProductCommandHandler.cs
│   │   │   │   │   └── CreateProductCommandValidator.cs
│   │   │   │   └── UpdateProduct/
│   │   │   ├── Queries/
│   │   │   │   ├── GetProducts/
│   │   │   │   │   ├── GetProductsQuery.cs
│   │   │   │   │   └── GetProductsQueryHandler.cs
│   │   │   │   └── GetProductById/
│   │   │   └── ProductDto.cs
│   │   ├── DependencyInjection.cs
│   │   └── MyApp.Application.csproj       # References: Domain
│   │
│   ├── MyApp.Infrastructure/              # Infrastructure Layer (separate project)
│   │   ├── Persistence/
│   │   │   ├── ApplicationDbContext.cs
│   │   │   ├── Configurations/
│   │   │   │   ├── ProductConfiguration.cs
│   │   │   │   └── CategoryConfiguration.cs
│   │   │   └── Migrations/
│   │   ├── Repositories/
│   │   │   └── ProductRepository.cs
│   │   ├── Services/
│   │   │   ├── EmailService.cs
│   │   │   └── FileStorageService.cs
│   │   ├── Identity/
│   │   │   └── UserContext.cs
│   │   ├── DependencyInjection.cs
│   │   └── MyApp.Infrastructure.csproj    # References: Domain, Application
│   │
│   └── MyApp.Web/                         # Presentation Layer (separate project)
│       ├── Controllers/
│       │   ├── ProductsController.cs
│       │   ├── OrdersController.cs
│       │   └── BaseController.cs
│       ├── Filters/
│       │   ├── ValidationFilter.cs
│       │   └── GlobalExceptionFilter.cs
│       ├── Middleware/
│       │   └── RequestLoggingMiddleware.cs
│       ├── Extensions/
│       │   └── ResultExtensions.cs
│       ├── Program.cs
│       ├── appsettings.json
│       └── MyApp.Web.csproj               # References: Application, Infrastructure
│
└── tests/
    ├── MyApp.Domain.Tests/
    ├── MyApp.Application.Tests/
    ├── MyApp.Infrastructure.Tests/
    └── MyApp.Web.Tests/
```

**Project Dependencies (Critical):**
- `Domain` → No dependencies (core business logic)
- `Application` → References `Domain` only
- `Infrastructure` → References `Domain` + `Application`
- `Web` → References `Application` + `Infrastructure` (composition root)

## 1. Domain Layer (MyApp.Domain Project)

### Entities with Encapsulation

```csharp
// MyApp.Domain/Entities/Product.cs
namespace MyApp.Domain.Entities;

public class Product
{
    public int Id { get; private set; }
    public string Name { get; private set; } = string.Empty;
    public string Description { get; private set; } = string.Empty;
    public decimal Price { get; private set; }
    public int CategoryId { get; private set; }
    public Category Category { get; private set; } = null!;
    public DateTime CreatedAt { get; private set; }
    public DateTime? UpdatedAt { get; private set; }

    private Product() { } // EF Core

    public static Product Create(string name, string description, decimal price, int categoryId)
    {
        if (string.IsNullOrWhiteSpace(name))
            throw new DomainException("Product name is required");

        if (price <= 0)
            throw new DomainException("Product price must be greater than zero");

        return new Product
        {
            Name = name,
            Description = description,
            Price = price,
            CategoryId = categoryId,
            CreatedAt = DateTime.UtcNow
        };
    }

    public void Update(string name, string description, decimal price)
    {
        if (string.IsNullOrWhiteSpace(name))
            throw new DomainException("Product name is required");

        if (price <= 0)
            throw new DomainException("Product price must be greater than zero");

        Name = name;
        Description = description;
        Price = price;
        UpdatedAt = DateTime.UtcNow;
    }
}

// MyApp.Domain/Exceptions/DomainException.cs
namespace MyApp.Domain.Exceptions;

public class DomainException : Exception
{
    public DomainException(string message) : base(message) { }
}
```

## 2. Application Layer (MyApp.Application Project)

### Commands (Write Operations)

```csharp
// MyApp.Application/Products/Commands/CreateProduct/CreateProductCommand.cs
using MediatR;
using CSharpFunctionalExtensions;

namespace MyApp.Application.Products.Commands.CreateProduct;

public sealed record CreateProductCommand(
    string Name,
    string Description,
    decimal Price,
    int CategoryId
) : IRequest<Result<ProductDto>>;

// MyApp.Application/Products/Commands/CreateProduct/CreateProductCommandHandler.cs
using MyApp.Domain.Entities;
using MyApp.Application.Common.Interfaces;
using MediatR;
using CSharpFunctionalExtensions;

namespace MyApp.Application.Products.Commands.CreateProduct;

public sealed class CreateProductCommandHandler
    : IRequestHandler<CreateProductCommand, Result<ProductDto>>
{
    private readonly IApplicationDbContext _context;
    private readonly ILogger<CreateProductCommandHandler> _logger;

    public CreateProductCommandHandler(
        IApplicationDbContext context,
        ILogger<CreateProductCommandHandler> logger)
    {
        _context = context;
        _logger = logger;
    }

    public async Task<Result<ProductDto>> Handle(
        CreateProductCommand request,
        CancellationToken cancellationToken)
    {
        var product = Product.Create(
            request.Name,
            request.Description,
            request.Price,
            request.CategoryId
        );

        _context.Products.Add(product);
        await _context.SaveChangesAsync(cancellationToken);

        _logger.LogInformation(
            "Created product {ProductId} with name {ProductName}",
            product.Id,
            product.Name);

        return Result.Success(new ProductDto(
            product.Id,
            product.Name,
            product.Description,
            product.Price,
            product.Category.Name
        ));
    }
}

// MyApp.Application/Products/Commands/CreateProduct/CreateProductCommandValidator.cs
using FluentValidation;

namespace MyApp.Application.Products.Commands.CreateProduct;

public sealed class CreateProductCommandValidator : AbstractValidator<CreateProductCommand>
{
    public CreateProductCommandValidator()
    {
        RuleFor(x => x.Name)
            .NotEmpty()
            .MaximumLength(100);

        RuleFor(x => x.Description)
            .MaximumLength(500);

        RuleFor(x => x.Price)
            .GreaterThan(0)
            .LessThan(1000000);

        RuleFor(x => x.CategoryId)
            .GreaterThan(0);
    }
}
```

### Queries (Read Operations)

```csharp
// MyApp.Application/Products/Queries/GetProducts/GetProductsQuery.cs
using MediatR;
using CSharpFunctionalExtensions;

namespace MyApp.Application.Products.Queries.GetProducts;

public sealed record GetProductsQuery(
    int Page = 1,
    int PageSize = 10,
    string? SearchTerm = null
) : IRequest<Result<PagedResult<ProductDto>>>;

// MyApp.Application/Products/Queries/GetProducts/GetProductsQueryHandler.cs
using MyApp.Application.Common.Models;
using MyApp.Application.Common.Interfaces;
using MediatR;
using Microsoft.EntityFrameworkCore;
using CSharpFunctionalExtensions;

namespace MyApp.Application.Products.Queries.GetProducts;

public sealed class GetProductsQueryHandler
    : IRequestHandler<GetProductsQuery, Result<PagedResult<ProductDto>>>
{
    private readonly IApplicationDbContext _context;

    public GetProductsQueryHandler(IApplicationDbContext context)
    {
        _context = context;
    }

    public async Task<Result<PagedResult<ProductDto>>> Handle(
        GetProductsQuery request,
        CancellationToken cancellationToken)
    {
        var query = _context.Products
            .Include(p => p.Category)
            .AsQueryable();

        if (!string.IsNullOrWhiteSpace(request.SearchTerm))
        {
            query = query.Where(p =>
                p.Name.Contains(request.SearchTerm) ||
                p.Description.Contains(request.SearchTerm));
        }

        var totalCount = await query.CountAsync(cancellationToken);

        var products = await query
            .OrderBy(p => p.Name)
            .Skip((request.Page - 1) * request.PageSize)
            .Take(request.PageSize)
            .Select(p => new ProductDto(
                p.Id,
                p.Name,
                p.Description,
                p.Price,
                p.Category.Name
            ))
            .ToListAsync(cancellationToken);

        return Result.Success(new PagedResult<ProductDto>(
            products,
            totalCount,
            request.Page,
            request.PageSize
        ));
    }
}
```

### DTOs and Common Models

```csharp
// MyApp.Application/Products/ProductDto.cs
namespace MyApp.Application.Products;

public record ProductDto(
    int Id,
    string Name,
    string Description,
    decimal Price,
    string CategoryName
);

// MyApp.Application/Common/Models/PagedResult.cs
namespace MyApp.Application.Common.Models;

public record PagedResult<T>(
    List<T> Items,
    int TotalCount,
    int Page,
    int PageSize
)
{
    public int TotalPages => (int)Math.Ceiling(TotalCount / (double)PageSize);
    public bool HasPreviousPage => Page > 1;
    public bool HasNextPage => Page < TotalPages;
}
```

### Interfaces

```csharp
// MyApp.Application/Common/Interfaces/IApplicationDbContext.cs
using MyApp.Domain.Entities;
using Microsoft.EntityFrameworkCore;

namespace MyApp.Application.Common.Interfaces;

public interface IApplicationDbContext
{
    DbSet<Product> Products { get; }
    DbSet<Category> Categories { get; }

    Task<int> SaveChangesAsync(CancellationToken cancellationToken = default);
}
```

### Dependency Injection (Application Layer)

```csharp
// MyApp.Application/DependencyInjection.cs
using System.Reflection;
using FluentValidation;
using MediatR;
using Microsoft.Extensions.DependencyInjection;

namespace MyApp.Application;

public static class DependencyInjection
{
    public static IServiceCollection AddApplication(this IServiceCollection services)
    {
        services.AddMediatR(cfg =>
            cfg.RegisterServicesFromAssembly(Assembly.GetExecutingAssembly()));

        services.AddValidatorsFromAssembly(Assembly.GetExecutingAssembly());

        services.AddTransient(typeof(IPipelineBehavior<,>), typeof(ValidationBehavior<,>));
        services.AddTransient(typeof(IPipelineBehavior<,>), typeof(LoggingBehavior<,>));

        return services;
    }
}
```

### Pipeline Behaviors

```csharp
// MyApp.Application/Common/Behaviors/ValidationBehavior.cs
using FluentValidation;
using MediatR;

namespace MyApp.Application.Common.Behaviors;

public sealed class ValidationBehavior<TRequest, TResponse>
    : IPipelineBehavior<TRequest, TResponse>
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
        CancellationToken cancellationToken)
    {
        if (!_validators.Any())
        {
            return await next();
        }

        var context = new ValidationContext<TRequest>(request);

        var validationResults = await Task.WhenAll(
            _validators.Select(v => v.ValidateAsync(context, cancellationToken)));

        var failures = validationResults
            .SelectMany(r => r.Errors)
            .Where(f => f != null)
            .ToList();

        if (failures.Count != 0)
        {
            throw new ValidationException(failures);
        }

        return await next();
    }
}

// MyApp.Application/Common/Behaviors/LoggingBehavior.cs
using MediatR;
using Microsoft.Extensions.Logging;

namespace MyApp.Application.Common.Behaviors;

public sealed class LoggingBehavior<TRequest, TResponse>
    : IPipelineBehavior<TRequest, TResponse>
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
        CancellationToken cancellationToken)
    {
        var requestName = typeof(TRequest).Name;

        _logger.LogInformation("Handling {RequestName}", requestName);

        var response = await next();

        _logger.LogInformation("Handled {RequestName}", requestName);

        return response;
    }
}
```

## 3. Infrastructure Layer (MyApp.Infrastructure Project)

### DbContext Implementation

```csharp
// MyApp.Infrastructure/Persistence/ApplicationDbContext.cs
using MyApp.Domain.Entities;
using MyApp.Application.Common.Interfaces;
using Microsoft.EntityFrameworkCore;

namespace MyApp.Infrastructure.Persistence;

public sealed class ApplicationDbContext : DbContext, IApplicationDbContext
{
    public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
        : base(options)
    {
    }

    public DbSet<Product> Products => Set<Product>();
    public DbSet<Category> Categories => Set<Category>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.ApplyConfigurationsFromAssembly(typeof(ApplicationDbContext).Assembly);
        base.OnModelCreating(modelBuilder);
    }
}
```

### Entity Configurations

```csharp
// MyApp.Infrastructure/Persistence/Configurations/ProductConfiguration.cs
using MyApp.Domain.Entities;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace MyApp.Infrastructure.Persistence.Configurations;

public sealed class ProductConfiguration : IEntityTypeConfiguration<Product>
{
    public void Configure(EntityTypeBuilder<Product> builder)
    {
        builder.ToTable("Products");
        
        builder.HasKey(p => p.Id);
        
        builder.Property(p => p.Name)
            .IsRequired()
            .HasMaxLength(100);
            
        builder.Property(p => p.Price)
            .HasPrecision(18, 2);
            
        builder.HasOne(p => p.Category)
            .WithMany()
            .HasForeignKey(p => p.CategoryId)
            .OnDelete(DeleteBehavior.Restrict);
    }
}
```

### Dependency Injection (Infrastructure Layer)

```csharp
// MyApp.Infrastructure/DependencyInjection.cs
using MyApp.Application.Common.Interfaces;
using MyApp.Infrastructure.Persistence;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;

namespace MyApp.Infrastructure;

public static class DependencyInjection
{
    public static IServiceCollection AddInfrastructure(
        this IServiceCollection services,
        IConfiguration configuration)
    {
        services.AddDbContext<ApplicationDbContext>(options =>
            options.UseSqlServer(
                configuration.GetConnectionString("DefaultConnection"),
                b => b.MigrationsAssembly(typeof(ApplicationDbContext).Assembly.FullName)));

        services.AddScoped<IApplicationDbContext>(provider =>
            provider.GetRequiredService<ApplicationDbContext>());

        return services;
    }
}
```

## 4. Web/API Layer (MyApp.Web Project)

### Controller with MediatR

```csharp
// MyApp.Web/Controllers/ProductsController.cs
using MyApp.Application.Products.Commands.CreateProduct;
using MyApp.Application.Products.Queries.GetProducts;
using MediatR;
using Microsoft.AspNetCore.Mvc;

namespace MyApp.Web.Controllers;

[ApiController]
[Route("api/[controller]")]
public sealed class ProductsController : ControllerBase
{
    private readonly IMediator _mediator;
    private readonly ILogger<ProductsController> _logger;

    public ProductsController(IMediator mediator, ILogger<ProductsController> logger)
    {
        _mediator = mediator;
        _logger = logger;
    }

    [HttpGet]
    [ProducesResponseType(typeof(PagedResult<ProductDto>), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status400BadRequest)]
    public async Task<ActionResult<PagedResult<ProductDto>>> GetProducts(
        [FromQuery] int page = 1,
        [FromQuery] int pageSize = 10,
        [FromQuery] string? searchTerm = null,
        CancellationToken ct = default)
    {
        var query = new GetProductsQuery(page, pageSize, searchTerm);
        var result = await _mediator.Send(query, ct);
        return result.IsSuccess ? Ok(result.Value) : BadRequest(result.Error);
    }

    [HttpGet("{id:int}")]
    [ProducesResponseType(typeof(ProductDto), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<ActionResult<ProductDto>> GetById(int id, CancellationToken ct)
    {
        var result = await _mediator.Send(new GetProductByIdQuery(id), ct);
        return result.IsSuccess ? Ok(result.Value) : NotFound(result.Error);
    }

    [HttpPost]
    [ProducesResponseType(typeof(ProductDto), StatusCodes.Status201Created)]
    [ProducesResponseType(StatusCodes.Status400BadRequest)]
    public async Task<ActionResult<ProductDto>> Create(
        CreateProductCommand command,
        CancellationToken ct)
    {
        var result = await _mediator.Send(command, ct);
        
        if (!result.IsSuccess)
            return BadRequest(result.Error);

        return CreatedAtAction(
            nameof(GetById),
            new { id = result.Value.Id },
            result.Value);
    }

    [HttpPut("{id:int}")]
    [ProducesResponseType(StatusCodes.Status204NoContent)]
    [ProducesResponseType(StatusCodes.Status400BadRequest)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<IActionResult> Update(
        int id,
        UpdateProductCommand command,
        CancellationToken ct)
    {
        if (id != command.Id)
            return BadRequest("ID mismatch");

        var result = await _mediator.Send(command, ct);
        return result.IsSuccess ? NoContent() : NotFound(result.Error);
    }

    [HttpDelete("{id:int}")]
    [ProducesResponseType(StatusCodes.Status204NoContent)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<IActionResult> Delete(int id, CancellationToken ct)
    {
        var result = await _mediator.Send(new DeleteProductCommand(id), ct);
        return result.IsSuccess ? NoContent() : NotFound(result.Error);
    }
}
```

### Program.cs (Composition Root)

```csharp
// MyApp.Web/Program.cs
using MyApp.Application;
using MyApp.Infrastructure;

var builder = WebApplication.CreateBuilder(args);

// Add layer dependencies
builder.Services.AddApplication();           // From Application project
builder.Services.AddInfrastructure(builder.Configuration);  // From Infrastructure project

builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();
app.UseAuthorization();
app.MapControllers();

app.Run();
```

## Project File Examples

### Domain Project (.csproj)

```xml
<!-- MyApp.Domain/MyApp.Domain.csproj -->
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <Nullable>enable</Nullable>
  </PropertyGroup>

  <!-- No external dependencies - Pure domain logic -->
</Project>
```

### Application Project (.csproj)

```xml
<!-- MyApp.Application/MyApp.Application.csproj -->
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <Nullable>enable</Nullable>
  </PropertyGroup>

  <ItemGroup>
    <!-- Reference Domain project only -->
    <ProjectReference Include="..\MyApp.Domain\MyApp.Domain.csproj" />
  </ItemGroup>

  <ItemGroup>
    <PackageReference Include="MediatR" Version="12.2.0" />
    <PackageReference Include="FluentValidation" Version="11.9.0" />
    <PackageReference Include="CSharpFunctionalExtensions" Version="2.40.0" />
    <PackageReference Include="Microsoft.EntityFrameworkCore" Version="8.0.0" />
  </ItemGroup>
</Project>
```

### Infrastructure Project (.csproj)

```xml
<!-- MyApp.Infrastructure/MyApp.Infrastructure.csproj -->
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <Nullable>enable</Nullable>
  </PropertyGroup>

  <ItemGroup>
    <!-- Reference Domain and Application -->
    <ProjectReference Include="..\MyApp.Domain\MyApp.Domain.csproj" />
    <ProjectReference Include="..\MyApp.Application\MyApp.Application.csproj" />
  </ItemGroup>

  <ItemGroup>
    <PackageReference Include="Microsoft.EntityFrameworkCore.SqlServer" Version="8.0.0" />
    <PackageReference Include="Microsoft.EntityFrameworkCore.Tools" Version="8.0.0" />
  </ItemGroup>
</Project>
```

### Web/API Project (.csproj)

```xml
<!-- MyApp.Web/MyApp.Web.csproj -->
<Project Sdk="Microsoft.NET.Sdk.Web">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <Nullable>enable</Nullable>
  </PropertyGroup>

  <ItemGroup>
    <!-- Reference Application and Infrastructure (composition root) -->
    <ProjectReference Include="..\MyApp.Application\MyApp.Application.csproj" />
    <ProjectReference Include="..\MyApp.Infrastructure\MyApp.Infrastructure.csproj" />
  </ItemGroup>

  <ItemGroup>
    <PackageReference Include="Swashbuckle.AspNetCore" Version="6.5.0" />
    <PackageReference Include="Serilog.AspNetCore" Version="8.0.0" />
    <PackageReference Include="Asp.Versioning.Mvc" Version="8.0.0" />
  </ItemGroup>
</Project>
```

## Quick Reference

| Pattern | Purpose |
|---------| --------|
| **Separated Projects** | Each layer is a separate .csproj for clear boundaries |
| **Domain Layer** | Pure business logic, no dependencies |
| **Application Layer** | MediatR handlers, DTOs, validators (refs Domain) |
| **Infrastructure Layer** | EF Core, external services (refs Domain + Application) |
| **Web/API Layer** | Controllers, composition root (refs Application + Infrastructure) |
| `IRequest<T>` | MediatR command/query interface |
| `IRequestHandler<TReq, TRes>` | Handler implementation |
| `IPipelineBehavior<,>` | Cross-cutting concerns |
| `IValidator<T>` | FluentValidation interface |
| `ISender` | MediatR sender for controllers |
| Domain entities | Business logic and invariants |
| Application layer | Use cases and orchestration |
| Infrastructure | External dependencies |

## Key Benefits of Separated Projects

1. **Clear Dependency Direction**: Domain → Application → Infrastructure → Web
2. **Testability**: Each layer can be tested independently
3. **Maintainability**: Changes in one layer don't affect unrelated layers
4. **Reusability**: Domain and Application can be reused in different hosts (Web API, Console, Azure Functions)
5. **Team Scalability**: Different teams can work on different layers with minimal conflicts
