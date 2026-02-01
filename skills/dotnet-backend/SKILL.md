---
name: dotnet-backend
description: ".NET/C# backend developer for ASP.NET Core APIs with Entity Framework Core. Builds REST APIs with Controller-based architecture, gRPC services, authentication with Identity/JWT, authorization, database operations, background services, SignalR real-time features. Follows Clean Architecture with separated projects (Domain/Application/Infrastructure/Web), MediatR, Result pattern, and sealed classes. Triggers when: (1) Creating/modifying C# backend code, (2) Building ASP.NET Core APIs or services, (3) Working with Entity Framework Core/EF Core, (4) Implementing MediatR handlers or CQRS patterns, (5) Writing xUnit tests for .NET, (6) Configuring dependency injection or middleware, (7) Building background services with IHostedService, (8) Implementing SignalR real-time features, (9) Working with MassTransit messaging, (10) Any .NET 8/9/10 backend development. Activates for keywords: .NET, C#, ASP.NET Core, Entity Framework Core, EF Core, .NET Core, Web API, Controller, gRPC, authentication .NET, Identity, JWT .NET, authorization, LINQ, async/await C#, background service, IHostedService, SignalR, SQL Server, PostgreSQL .NET, dependency injection, middleware .NET, MediatR, CQRS, Result pattern, xUnit, FluentValidation, Serilog."
---

# .NET Backend Agent - ASP.NET Core & Enterprise API Expert

Expert .NET/C# backend developer building enterprise-grade APIs with Clean Architecture principles.

## Technical Stack

- **Runtime**: C# 13, .NET 8+ (minimum .NET 8, target .NET 10)
- **Frameworks**: ASP.NET Core 8+, Controller-based Web API, gRPC
- **ORM**: Entity Framework Core 8+, Dapper
- **Databases**: SQL Server, PostgreSQL
- **Messaging**: MassTransit (RabbitMQ/AWS SQS)
- **Patterns**: MediatR, CSharpFunctionalExtensions, FluentValidation, Mapster
- **Testing**: xUnit, NSubstitute/Moq, Shouldly/FluentAssertions
- **Logging**: Serilog (structured)

## NON-NEGOTIABLE Principles

### 1. Sealed Classes
All new classes MUST be `sealed` unless designed for inheritance.

```csharp
// CORRECT
public sealed class CreateOrderCommandHandler : IRequestHandler<CreateOrderCommand, Result<Order>> { }

// WRONG
public class OrderValidator { }
```

**Exceptions**: Domain entities with hierarchy, abstract base classes.

### 2. Result Pattern Over Exceptions
Return `Result<T>` for business logic, NOT exceptions.

```csharp
// CORRECT
if (!validation.IsValid) return Result.Failure<Order>("Validation failed");
return Result.Success(order);

// WRONG
throw new ValidationException("Invalid");
```

### 3. Async/Await with CancellationToken
All I/O MUST use `async/await` with `CancellationToken`.

```csharp
// CORRECT
public async Task<Result<OrderDto>> GetOrderAsync(int orderId, CancellationToken ct)
{
    var order = await _db.Orders.FirstOrDefaultAsync(o => o.Id == orderId, ct);
    return order is not null ? Result.Success(order.ToDto()) : Result.Failure<OrderDto>("Not found");
}

// WRONG - Missing CancellationToken, using .Result
public OrderDto GetOrder(int id) => _db.Orders.FirstOrDefaultAsync(o => o.Id == id).Result.ToDto();
```

**Prohibited**: `.Result`, `.Wait()`, `async void`

### 4. Structured Logging
Use Serilog with structured parameters, NOT string interpolation.

```csharp
// CORRECT
_logger.LogInformation("Processing order {OrderId} for client {ClientId}", orderId, clientId);

// WRONG
_logger.LogInformation($"Processing order {orderId} for client {clientId}");
```

### 5. Theory Pattern Testing
Use `[Theory]` with `[InlineData]` to eliminate test duplication.

```csharp
// CORRECT
[Theory]
[InlineData(0)]
[InlineData(-1)]
public void Validate_InvalidId_ShouldFail(int id)
{
    var result = _validator.Validate(new OrderQuery(id));
    result.IsValid.ShouldBeFalse();
}

// WRONG - Separate [Fact] per value, "Arrange/Act/Assert" comments
```

**Prohibited**: "Arrange/Act/Assert" comments, magic numbers without explanation.

### 6. Message Contract Immutability
**NEVER** change namespace/class name, rename/remove properties, change types on message contracts.

```csharp
// Breaking changes require versioning
public record SignItEmailMessageV2 { } // New version, emit both for 3-month sunset
```

**Protected namespaces**: `SignIt.Domain.Messaging.Publish.*`, `InfotrackSignIt.Domain.Messages.*`

## Clean Architecture Layers

**Separated Projects Structure:**
- **Domain** (`MyApp.Domain`) - Entities, value objects, domain events (no dependencies)
- **Application** (`MyApp.Application`) - MediatR handlers, DTOs, validators (references Domain)
- **Infrastructure** (`MyApp.Infrastructure`) - EF Core, repositories, external services (references Domain + Application)
- **Web/API** (`MyApp.Web`) - Controllers, composition root (references Application + Infrastructure)

### Project Structure
New code ONLY in:
- `InfotrackSignIt.Domain` - Entities, value objects, domain events
- `InfotrackSignIt.Application` - MediatR handlers, DTOs, validators
- `InfotrackSignIt.Infrastructure` - EF Core, repositories, external services

**Legacy Deprecated** (`Infotrack.SignIt.*`, `SignIt.*`): P0/P1 bugfixes only. NO new classes/methods.

## Code Patterns

### MediatR Command Handler with Result Pattern
```csharp
public sealed class CreateOrderCommand : IRequest<Result<OrderDto>>
{
    public required string CustomerEmail { get; init; }
    public required List<OrderItemDto> Items { get; init; }
}

public sealed class CreateOrderCommandHandler : IRequestHandler<CreateOrderCommand, Result<OrderDto>>
{
    private readonly AppDbContext _db;
    private readonly ILogger<CreateOrderCommandHandler> _logger;

    public CreateOrderCommandHandler(AppDbContext db, ILogger<CreateOrderCommandHandler> logger)
    {
        _db = db;
        _logger = logger;
    }

    public async Task<Result<OrderDto>> Handle(CreateOrderCommand request, CancellationToken ct)
    {
        if (string.IsNullOrWhiteSpace(request.CustomerEmail))
            return Result.Failure<OrderDto>("Customer email is required");

        var order = new Order
        {
            CustomerEmail = request.CustomerEmail,
            Items = request.Items.Select(i => i.ToEntity()).ToList(),
            CreatedAt = DateTime.UtcNow
        };

        _db.Orders.Add(order);
        await _db.SaveChangesAsync(ct);

        _logger.LogInformation("Created order {OrderId} for {CustomerEmail}", order.Id, order.CustomerEmail);

        return Result.Success(order.ToDto());
    }
}
```

### FluentValidation
```csharp
public sealed class CreateOrderCommandValidator : AbstractValidator<CreateOrderCommand>
{
    public CreateOrderCommandValidator()
    {
        RuleFor(x => x.CustomerEmail)
            .NotEmpty().WithMessage("Customer email is required")
            .EmailAddress().WithMessage("Invalid email format");

        RuleFor(x => x.Items)
            .NotEmpty().WithMessage("At least one item is required");

        RuleForEach(x => x.Items).ChildRules(item =>
        {
            item.RuleFor(i => i.Quantity).GreaterThan(0);
            item.RuleFor(i => i.ProductId).NotEmpty();
        });
    }
}
```

### Controller with Result Mapping
```csharp
[ApiController]
[Route("api/[controller]")]
public sealed class OrdersController : ControllerBase
{
    private readonly IMediator _mediator;

    public OrdersController(IMediator mediator) => _mediator = mediator;

    [HttpPost]
    public async Task<ActionResult<OrderDto>> CreateOrder(
        CreateOrderCommand command,
        CancellationToken ct)
    {
        var result = await _mediator.Send(command, ct);
        return result.IsSuccess ? Ok(result.Value) : BadRequest(result.Error);
    }

    [HttpGet("{id:int}")]
    public async Task<ActionResult<OrderDto>> GetOrder(int id, CancellationToken ct)
    {
        var result = await _mediator.Send(new GetOrderQuery(id), ct);
        return result.IsSuccess ? Ok(result.Value) : NotFound(result.Error);
    }
}
```

### Background Service with Scoped Services
```csharp
public sealed class EmailProcessorService : BackgroundService
{
    private readonly ILogger<EmailProcessorService> _logger;
    private readonly IServiceProvider _services;

    public EmailProcessorService(ILogger<EmailProcessorService> logger, IServiceProvider services)
    {
        _logger = logger;
        _services = services;
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        while (!stoppingToken.IsCancellationRequested)
        {
            using var scope = _services.CreateScope();
            var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();

            var pendingEmails = await db.PendingEmails
                .Where(e => !e.Sent)
                .Take(10)
                .ToListAsync(stoppingToken);

            foreach (var email in pendingEmails)
            {
                await ProcessEmailAsync(email, stoppingToken);
                email.Sent = true;
            }

            await db.SaveChangesAsync(stoppingToken);
            await Task.Delay(TimeSpan.FromMinutes(1), stoppingToken);
        }
    }

    private async Task ProcessEmailAsync(PendingEmail email, CancellationToken ct)
    {
        _logger.LogInformation("Sending email to {Recipient}", email.To);
        // Email sending logic
    }
}
```

### xUnit Test with Theory Pattern
```csharp
public sealed class CreateOrderCommandValidatorTests
{
    private readonly CreateOrderCommandValidator _validator = new();

    [Theory]
    [InlineData(null)]
    [InlineData("")]
    [InlineData("   ")]
    public void Validate_EmptyEmail_ShouldFail(string? email)
    {
        var command = new CreateOrderCommand
        {
            CustomerEmail = email!,
            Items = new List<OrderItemDto> { new("prod-1", 1) }
        };

        var result = _validator.Validate(command);

        result.IsValid.ShouldBeFalse();
        result.Errors.ShouldContain(e => e.PropertyName == nameof(CreateOrderCommand.CustomerEmail));
    }

    [Fact]
    public void Validate_ValidCommand_ShouldPass()
    {
        var command = new CreateOrderCommand
        {
            CustomerEmail = "test@example.com",
            Items = new List<OrderItemDto> { new("prod-1", 1) }
        };

        var result = _validator.Validate(command);

        result.IsValid.ShouldBeTrue();
    }
}
```

## Checklist

Before completing any .NET backend task, verify:

- [ ] All classes are `sealed` (unless inheritance required)
- [ ] Business logic uses `Result<T>`, not exceptions
- [ ] All async methods include `CancellationToken`
- [ ] Logging uses structured parameters `{PropertyName}`
- [ ] Tests use `[Theory]` for multiple inputs
- [ ] No code added to legacy `Infotrack.SignIt.*` or `SignIt.*` projects
- [ ] Message contracts unchanged (namespace, class name, properties)
- [ ] No `.Result`, `.Wait()`, or `async void`
