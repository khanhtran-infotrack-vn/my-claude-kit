# Controller-Based APIs

## Basic Controller Pattern

```csharp
using MediatR;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Authorization;
using CSharpFunctionalExtensions;

namespace MyApp.Web.Controllers;

[ApiController]
[Route("api/[controller]")]
[Authorize]
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
    [ProducesResponseType(typeof(List<ProductDto>), StatusCodes.Status200OK)]
    public async Task<ActionResult<List<ProductDto>>> GetAll(CancellationToken ct)
    {
        var result = await _mediator.Send(new GetProductsQuery(), ct);
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

## Result Pattern Integration

```csharp
using CSharpFunctionalExtensions;
using Microsoft.AspNetCore.Mvc;

[ApiController]
[Route("api/[controller]")]
public sealed class OrdersController : ControllerBase
{
    private readonly IMediator _mediator;

    public OrdersController(IMediator mediator) => _mediator = mediator;

    // Pattern 1: Simple Result<T> to ActionResult<T>
    [HttpGet("{id:int}")]
    public async Task<ActionResult<OrderDto>> GetOrder(int id, CancellationToken ct)
    {
        var result = await _mediator.Send(new GetOrderQuery(id), ct);
        return result.IsSuccess ? Ok(result.Value) : NotFound(result.Error);
    }

    // Pattern 2: Result with Match pattern
    [HttpPost]
    public async Task<ActionResult<OrderDto>> CreateOrder(
        CreateOrderCommand command,
        CancellationToken ct)
    {
        var result = await _mediator.Send(command, ct);
        
        return result.Match<ActionResult<OrderDto>>(
            onSuccess: order => CreatedAtAction(nameof(GetOrder), new { id = order.Id }, order),
            onFailure: error => BadRequest(error)
        );
    }

    // Pattern 3: Result<Unit> for void operations
    [HttpPost("{id:int}/approve")]
    [ProducesResponseType(StatusCodes.Status204NoContent)]
    [ProducesResponseType(StatusCodes.Status400BadRequest)]
    public async Task<IActionResult> ApproveOrder(int id, CancellationToken ct)
    {
        var result = await _mediator.Send(new ApproveOrderCommand(id), ct);
        return result.IsSuccess ? NoContent() : BadRequest(result.Error);
    }

    // Pattern 4: Multiple error types with custom mapping
    [HttpPost("{id:int}/process")]
    public async Task<IActionResult> ProcessOrder(int id, CancellationToken ct)
    {
        var result = await _mediator.Send(new ProcessOrderCommand(id), ct);
        
        if (result.IsSuccess)
            return Ok(result.Value);

        // Custom error mapping based on error type
        return result.Error switch
        {
            "Order not found" => NotFound(result.Error),
            "Order already processed" => Conflict(result.Error),
            "Insufficient inventory" => UnprocessableEntity(result.Error),
            _ => BadRequest(result.Error)
        };
    }
}
```

## API Versioning

```csharp
using Asp.Versioning;
using Microsoft.AspNetCore.Mvc;

// Version 1.0
[ApiVersion("1.0")]
[ApiController]
[Route("api/v{version:apiVersion}/[controller]")]
public sealed class ContractsController : ControllerBase
{
    private readonly IMediator _mediator;

    public ContractsController(IMediator mediator) => _mediator = mediator;

    [HttpGet("{id:int}")]
    [MapToApiVersion("1.0")]
    public async Task<ActionResult<ContractDto>> GetContract(int id, CancellationToken ct)
    {
        var result = await _mediator.Send(new GetContractQuery(id), ct);
        return result.IsSuccess ? Ok(result.Value) : NotFound(result.Error);
    }
}

// Version 2.0 with breaking changes
[ApiVersion("2.0")]
[ApiController]
[Route("api/v{version:apiVersion}/[controller]")]
public sealed class ContractsV2Controller : ControllerBase
{
    private readonly IMediator _mediator;

    public ContractsV2Controller(IMediator mediator) => _mediator = mediator;

    [HttpGet("{id:int}")]
    [MapToApiVersion("2.0")]
    public async Task<ActionResult<ContractV2Dto>> GetContract(int id, CancellationToken ct)
    {
        var result = await _mediator.Send(new GetContractV2Query(id), ct);
        return result.IsSuccess ? Ok(result.Value) : NotFound(result.Error);
    }
}

// Program.cs setup
builder.Services.AddApiVersioning(options =>
{
    options.DefaultApiVersion = new ApiVersion(1, 0);
    options.AssumeDefaultVersionWhenUnspecified = true;
    options.ReportApiVersions = true;
    options.ApiVersionReader = new UrlSegmentApiVersionReader();
});
```

## Request Validation with FluentValidation

```csharp
using FluentValidation;

// Command with validation
public sealed record CreateProductCommand(
    string Name,
    string Description,
    decimal Price,
    int CategoryId
) : IRequest<Result<ProductDto>>;

// Validator
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

// Controller - validation handled by MediatR pipeline
[HttpPost]
public async Task<ActionResult<ProductDto>> Create(
    CreateProductCommand command,
    CancellationToken ct)
{
    // Validation happens in MediatR pipeline via ValidationBehavior
    var result = await _mediator.Send(command, ct);
    return result.IsSuccess 
        ? CreatedAtAction(nameof(GetById), new { id = result.Value.Id }, result.Value)
        : BadRequest(result.Error);
}
```

## Authorization and Security

```csharp
using Microsoft.AspNetCore.Authorization;
using SignIt.Infrastructure.Security;

[ApiController]
[Route("api/[controller]")]
[Authorize] // Requires authentication
public sealed class SecureController : ControllerBase
{
    private readonly IMediator _mediator;
    private readonly IUserContext _userContext;

    public SecureController(IMediator mediator, IUserContext userContext)
    {
        _mediator = mediator;
        _userContext = userContext;
    }

    // Role-based authorization
    [HttpGet("admin")]
    [Authorize(Roles = "Admin")]
    public async Task<ActionResult<AdminDataDto>> GetAdminData(CancellationToken ct)
    {
        var result = await _mediator.Send(new GetAdminDataQuery(), ct);
        return result.IsSuccess ? Ok(result.Value) : BadRequest(result.Error);
    }

    // Policy-based authorization
    [HttpPost("sensitive")]
    [Authorize(Policy = "RequireElevatedRights")]
    public async Task<IActionResult> PerformSensitiveAction(
        SensitiveCommand command,
        CancellationToken ct)
    {
        var result = await _mediator.Send(command, ct);
        return result.IsSuccess ? NoContent() : BadRequest(result.Error);
    }

    // Extract user context
    [HttpPost("orders")]
    public async Task<ActionResult<OrderDto>> CreateOrder(
        CreateOrderCommand command,
        CancellationToken ct)
    {
        // Inject user context from authentication
        command.LoginId = _userContext.RequireLoginId();
        command.ClientId = _userContext.RequireClientId();

        var result = await _mediator.Send(command, ct);
        return result.IsSuccess 
            ? CreatedAtAction(nameof(GetOrder), new { id = result.Value.Id }, result.Value)
            : BadRequest(result.Error);
    }

    // Allow anonymous access to specific endpoint
    [HttpGet("public")]
    [AllowAnonymous]
    public async Task<ActionResult<PublicDataDto>> GetPublicData(CancellationToken ct)
    {
        var result = await _mediator.Send(new GetPublicDataQuery(), ct);
        return Ok(result.Value);
    }
}
```

## Error Handling and Problem Details

```csharp
using Microsoft.AspNetCore.Mvc;
using InfotrackSignIt.Application.Common.Errors;

[ApiController]
[Route("api/[controller]")]
public sealed class RobustController : ControllerBase
{
    private readonly IMediator _mediator;
    private readonly ILogger<RobustController> _logger;

    public RobustController(IMediator mediator, ILogger<RobustController> logger)
    {
        _mediator = mediator;
        _logger = logger;
    }

    // Using TypedResults for consistent responses
    [HttpPost("process")]
    [ProducesResponseType(StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status400BadRequest)]
    [ProducesResponseType(typeof(ErrorProblemDetails), StatusCodes.Status500InternalServerError)]
    public async Task<IResult> ProcessData(ProcessDataCommand command, CancellationToken ct)
    {
        var result = await _mediator.Send(command, ct);

        return result.Match(
            onSuccess: TypedResults.Ok,
            onFailure: error => error.ToProblemDetail()
        );
    }

    // Custom error mapping
    [HttpPost("complex")]
    public async Task<ActionResult<ComplexDto>> ComplexOperation(
        ComplexCommand command,
        CancellationToken ct)
    {
        try
        {
            var result = await _mediator.Send(command, ct);

            if (result.IsSuccess)
                return Ok(result.Value);

            _logger.LogWarning("Complex operation failed: {Error}", result.Error);
            
            return Problem(
                statusCode: StatusCodes.Status400BadRequest,
                title: "Operation Failed",
                detail: result.Error
            );
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Unhandled exception in complex operation");
            return Problem(
                statusCode: StatusCodes.Status500InternalServerError,
                title: "Internal Server Error",
                detail: "An unexpected error occurred"
            );
        }
    }
}
```

## Pagination and Filtering

```csharp
using Microsoft.AspNetCore.Mvc;

[ApiController]
[Route("api/[controller]")]
public sealed class ProductsController : ControllerBase
{
    private readonly IMediator _mediator;

    public ProductsController(IMediator mediator) => _mediator = mediator;

    // Simple pagination
    [HttpGet]
    public async Task<ActionResult<PagedResult<ProductDto>>> GetProducts(
        [FromQuery] int page = 1,
        [FromQuery] int pageSize = 10,
        CancellationToken ct = default)
    {
        var query = new GetProductsQuery(page, pageSize);
        var result = await _mediator.Send(query, ct);
        return result.IsSuccess ? Ok(result.Value) : BadRequest(result.Error);
    }

    // Advanced filtering with query object
    [HttpGet("search")]
    public async Task<ActionResult<PagedResult<ProductDto>>> SearchProducts(
        [FromQuery] ProductSearchQuery query,
        CancellationToken ct)
    {
        var result = await _mediator.Send(query, ct);
        return result.IsSuccess ? Ok(result.Value) : BadRequest(result.Error);
    }
}

// Query DTO
public sealed record ProductSearchQuery(
    int Page = 1,
    int PageSize = 10,
    string? SearchTerm = null,
    decimal? MinPrice = null,
    decimal? MaxPrice = null,
    int? CategoryId = null,
    string? SortBy = "Name",
    bool SortDescending = false
) : IRequest<Result<PagedResult<ProductDto>>>;

// Paged result model
public sealed record PagedResult<T>(
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

## File Upload and Download

```csharp
using Microsoft.AspNetCore.Mvc;

[ApiController]
[Route("api/[controller]")]
public sealed class FilesController : ControllerBase
{
    private readonly IMediator _mediator;

    public FilesController(IMediator mediator) => _mediator = mediator;

    // File upload
    [HttpPost("upload")]
    [ProducesResponseType(typeof(FileUploadDto), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status400BadRequest)]
    public async Task<ActionResult<FileUploadDto>> Upload(
        IFormFile file,
        CancellationToken ct)
    {
        if (file.Length == 0)
            return BadRequest("File is empty");

        using var stream = file.OpenReadStream();
        
        var command = new UploadFileCommand(
            file.FileName,
            file.ContentType,
            stream
        );

        var result = await _mediator.Send(command, ct);
        return result.IsSuccess ? Ok(result.Value) : BadRequest(result.Error);
    }

    // File download
    [HttpGet("{id:int}/download")]
    [ProducesResponseType(typeof(FileContentResult), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<IActionResult> Download(int id, CancellationToken ct)
    {
        var result = await _mediator.Send(new GetFileQuery(id), ct);

        if (!result.IsSuccess)
            return NotFound(result.Error);

        return File(
            result.Value.Content,
            result.Value.ContentType,
            result.Value.FileName
        );
    }
}
```

## Dependency Injection Setup

```csharp
// Program.cs
var builder = WebApplication.CreateBuilder(args);

// Add controllers
builder.Services.AddControllers(options =>
{
    options.Filters.Add<ValidationFilter>();
    options.Filters.Add<GlobalExceptionFilter>();
});

// API versioning
builder.Services.AddApiVersioning(options =>
{
    options.DefaultApiVersion = new ApiVersion(1, 0);
    options.AssumeDefaultVersionWhenUnspecified = true;
    options.ReportApiVersions = true;
});

// Swagger/OpenAPI
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(options =>
{
    options.SwaggerDoc("v1", new OpenApiInfo { Title = "API v1", Version = "v1" });
    options.SwaggerDoc("v2", new OpenApiInfo { Title = "API v2", Version = "v2" });
});

// Authentication & Authorization
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

builder.Services.AddAuthorization(options =>
{
    options.AddPolicy("RequireElevatedRights", policy =>
        policy.RequireRole("Admin", "SuperUser"));
});

var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI(options =>
    {
        options.SwaggerEndpoint("/swagger/v1/swagger.json", "API v1");
        options.SwaggerEndpoint("/swagger/v2/swagger.json", "API v2");
    });
}

app.UseHttpsRedirection();
app.UseAuthentication();
app.UseAuthorization();
app.MapControllers();

app.Run();
```

## Quick Reference

| Pattern | Usage |
|---------|-------|
| `ControllerBase` | Base class for API controllers |
| `[ApiController]` | Enables API-specific behaviors (auto validation, binding) |
| `[Route("api/[controller]")]` | Conventional routing |
| `[HttpGet]`, `[HttpPost]` | HTTP verb attributes |
| `ActionResult<T>` | Typed response with status codes |
| `IResult` | TypedResults for minimal API-style responses |
| `[FromQuery]`, `[FromBody]` | Explicit binding sources |
| `[ProducesResponseType]` | Document response types for OpenAPI |
| `CreatedAtAction()` | 201 with location header |
| `Ok()`, `NoContent()` | 200, 204 responses |
| `BadRequest()`, `NotFound()` | 400, 404 error responses |
| `Problem()` | RFC 7807 problem details |
| `CancellationToken` | Request cancellation support |
