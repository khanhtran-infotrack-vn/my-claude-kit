# .NET Controller-Based APIs

ASP.NET Core Web API patterns with MediatR and Result pattern.

## Basic Controller Pattern

```csharp
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
    public async Task<ActionResult<ProductDto>> Create(CreateProductCommand command, CancellationToken ct)
    {
        var result = await _mediator.Send(command, ct);
        if (!result.IsSuccess) return BadRequest(result.Error);
        return CreatedAtAction(nameof(GetById), new { id = result.Value.Id }, result.Value);
    }

    [HttpPut("{id:int}")]
    [ProducesResponseType(StatusCodes.Status204NoContent)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<IActionResult> Update(int id, UpdateProductCommand command, CancellationToken ct)
    {
        if (id != command.Id) return BadRequest("ID mismatch");
        var result = await _mediator.Send(command, ct);
        return result.IsSuccess ? NoContent() : NotFound(result.Error);
    }

    [HttpDelete("{id:int}")]
    [ProducesResponseType(StatusCodes.Status204NoContent)]
    public async Task<IActionResult> Delete(int id, CancellationToken ct)
    {
        var result = await _mediator.Send(new DeleteProductCommand(id), ct);
        return result.IsSuccess ? NoContent() : NotFound(result.Error);
    }
}
```

## Result Pattern Integration

```csharp
// Custom error mapping
[HttpPost("{id:int}/process")]
public async Task<IActionResult> ProcessOrder(int id, CancellationToken ct)
{
    var result = await _mediator.Send(new ProcessOrderCommand(id), ct);

    if (result.IsSuccess) return Ok(result.Value);

    return result.Error switch
    {
        "Order not found" => NotFound(result.Error),
        "Order already processed" => Conflict(result.Error),
        "Insufficient inventory" => UnprocessableEntity(result.Error),
        _ => BadRequest(result.Error)
    };
}

// Match pattern
[HttpPost]
public async Task<ActionResult<OrderDto>> CreateOrder(CreateOrderCommand command, CancellationToken ct)
{
    var result = await _mediator.Send(command, ct);
    return result.Match<ActionResult<OrderDto>>(
        onSuccess: order => CreatedAtAction(nameof(GetOrder), new { id = order.Id }, order),
        onFailure: error => BadRequest(error)
    );
}
```

## API Versioning

```csharp
[ApiVersion("1.0")]
[ApiController]
[Route("api/v{version:apiVersion}/[controller]")]
public sealed class ContractsController : ControllerBase
{
    [HttpGet("{id:int}")]
    [MapToApiVersion("1.0")]
    public async Task<ActionResult<ContractDto>> GetContract(int id, CancellationToken ct) { ... }
}

// Program.cs
builder.Services.AddApiVersioning(options =>
{
    options.DefaultApiVersion = new ApiVersion(1, 0);
    options.AssumeDefaultVersionWhenUnspecified = true;
    options.ReportApiVersions = true;
    options.ApiVersionReader = new UrlSegmentApiVersionReader();
});
```

## Pagination and Filtering

```csharp
[HttpGet("search")]
public async Task<ActionResult<PagedResult<ProductDto>>> SearchProducts(
    [FromQuery] ProductSearchQuery query, CancellationToken ct)
{
    var result = await _mediator.Send(query, ct);
    return result.IsSuccess ? Ok(result.Value) : BadRequest(result.Error);
}

public sealed record ProductSearchQuery(
    int Page = 1,
    int PageSize = 10,
    string? SearchTerm = null,
    decimal? MinPrice = null,
    decimal? MaxPrice = null,
    string? SortBy = "Name",
    bool SortDescending = false
) : IRequest<Result<PagedResult<ProductDto>>>;

public sealed record PagedResult<T>(List<T> Items, int TotalCount, int Page, int PageSize)
{
    public int TotalPages => (int)Math.Ceiling(TotalCount / (double)PageSize);
    public bool HasPreviousPage => Page > 1;
    public bool HasNextPage => Page < TotalPages;
}
```

## Authorization

```csharp
[ApiController]
[Route("api/[controller]")]
[Authorize]
public sealed class SecureController : ControllerBase
{
    private readonly ICurrentUserService _currentUser;

    [HttpGet("admin")]
    [Authorize(Roles = "Admin")]
    public async Task<ActionResult<AdminDataDto>> GetAdminData(CancellationToken ct) { ... }

    [HttpPost("sensitive")]
    [Authorize(Policy = "RequireElevatedRights")]
    public async Task<IActionResult> PerformSensitiveAction(SensitiveCommand command, CancellationToken ct) { ... }

    [HttpGet("public")]
    [AllowAnonymous]
    public async Task<ActionResult<PublicDataDto>> GetPublicData(CancellationToken ct) { ... }
}
```

## File Upload/Download

```csharp
[HttpPost("upload")]
public async Task<ActionResult<FileUploadDto>> Upload(IFormFile file, CancellationToken ct)
{
    if (file.Length == 0) return BadRequest("File is empty");
    using var stream = file.OpenReadStream();
    var result = await _mediator.Send(new UploadFileCommand(file.FileName, file.ContentType, stream), ct);
    return result.IsSuccess ? Ok(result.Value) : BadRequest(result.Error);
}

[HttpGet("{id:int}/download")]
public async Task<IActionResult> Download(int id, CancellationToken ct)
{
    var result = await _mediator.Send(new GetFileQuery(id), ct);
    if (!result.IsSuccess) return NotFound(result.Error);
    return File(result.Value.Content, result.Value.ContentType, result.Value.FileName);
}
```

## Program.cs Setup

```csharp
var builder = WebApplication.CreateBuilder(args);

builder.Services.AddApplication();
builder.Services.AddInfrastructure(builder.Configuration);
builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options => { /* JWT config */ });

builder.Services.AddAuthorization(options =>
{
    options.AddPolicy("RequireElevatedRights", policy => policy.RequireRole("Admin", "SuperUser"));
});

var app = builder.Build();
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
| `[ApiController]` | Enables API behaviors |
| `ActionResult<T>` | Typed response with status |
| `[FromQuery]`, `[FromBody]` | Binding sources |
| `[ProducesResponseType]` | OpenAPI documentation |
| `CreatedAtAction()` | 201 with location header |
| `CancellationToken` | Request cancellation |
