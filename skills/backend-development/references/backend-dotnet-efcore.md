# Entity Framework Core

EF Core patterns, configurations, queries, and performance optimization for .NET 8+.

## DbContext Configuration

```csharp
public sealed class ApplicationDbContext : DbContext, IApplicationDbContext
{
    public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options) : base(options) { }

    public DbSet<Product> Products => Set<Product>();
    public DbSet<Category> Categories => Set<Category>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.ApplyConfigurationsFromAssembly(typeof(ApplicationDbContext).Assembly);
        base.OnModelCreating(modelBuilder);
    }
}
```

## Entity Configuration

```csharp
public sealed class ProductConfiguration : IEntityTypeConfiguration<Product>
{
    public void Configure(EntityTypeBuilder<Product> builder)
    {
        builder.ToTable("Products");
        builder.HasKey(p => p.Id);
        builder.Property(p => p.Name).IsRequired().HasMaxLength(100);
        builder.Property(p => p.Price).HasPrecision(18, 2);

        builder.HasOne(p => p.Category)
            .WithMany(c => c.Products)
            .HasForeignKey(p => p.CategoryId)
            .OnDelete(DeleteBehavior.Restrict);

        builder.HasIndex(p => p.Name);
        builder.HasIndex(p => p.CategoryId);
    }
}
```

## Complex Relationships

```csharp
// Many-to-Many with payload
public sealed class OrderItemConfiguration : IEntityTypeConfiguration<OrderItem>
{
    public void Configure(EntityTypeBuilder<OrderItem> builder)
    {
        builder.HasKey(oi => new { oi.OrderId, oi.ProductId }); // Composite key
        builder.Property(oi => oi.UnitPrice).HasPrecision(18, 2);

        builder.HasOne(oi => oi.Order).WithMany(o => o.OrderItems).HasForeignKey(oi => oi.OrderId);
        builder.HasOne(oi => oi.Product).WithMany().HasForeignKey(oi => oi.ProductId);
    }
}

// Owned types (value objects)
builder.OwnsOne(up => up.Address, address =>
{
    address.Property(a => a.Street).HasMaxLength(200);
    address.Property(a => a.City).HasMaxLength(100);
});
```

## Query Patterns

```csharp
// Read-only queries (best practice)
public async Task<List<ProductDto>> GetProductDtosAsync(CancellationToken ct)
{
    return await _context.Products
        .AsNoTracking()  // Important for read-only
        .Select(p => new ProductDto(p.Id, p.Name, p.Price, p.Category.Name))
        .ToListAsync(ct);
}

// Pagination
public async Task<PagedResult<Product>> GetPagedAsync(int page, int pageSize, CancellationToken ct)
{
    var query = _context.Products.AsNoTracking().Include(p => p.Category);
    var totalCount = await query.CountAsync(ct);
    var items = await query.Skip((page - 1) * pageSize).Take(pageSize).ToListAsync(ct);
    return new PagedResult<Product>(items, totalCount, page, pageSize);
}

// Complex filtering
public async Task<List<Product>> GetBySpecificationAsync(
    Expression<Func<Product, bool>> predicate, CancellationToken ct)
{
    return await _context.Products.AsNoTracking().Where(predicate).ToListAsync(ct);
}
```

## CRUD Repository

```csharp
public sealed class ProductRepository : IProductRepository
{
    private readonly ApplicationDbContext _context;

    public async Task<Product?> GetByIdAsync(int id, CancellationToken ct) =>
        await _context.Products.Include(p => p.Category).FirstOrDefaultAsync(p => p.Id == id, ct);

    public async Task<Product> AddAsync(Product product, CancellationToken ct)
    {
        _context.Products.Add(product);
        await _context.SaveChangesAsync(ct);
        return product;
    }

    public async Task UpdateAsync(Product product, CancellationToken ct)
    {
        _context.Products.Update(product);
        await _context.SaveChangesAsync(ct);
    }

    public async Task DeleteAsync(int id, CancellationToken ct)
    {
        var product = await _context.Products.FindAsync(new object[] { id }, ct);
        if (product is not null)
        {
            _context.Products.Remove(product);
            await _context.SaveChangesAsync(ct);
        }
    }
}
```

## Migrations

```bash
# Add migration
dotnet ef migrations add InitialCreate --project Infrastructure --startup-project WebApi

# Update database
dotnet ef database update --project Infrastructure --startup-project WebApi

# Generate SQL script
dotnet ef migrations script --project Infrastructure --startup-project WebApi -o migration.sql
```

## Performance Optimization

```csharp
// Compiled queries (for hot paths)
private static readonly Func<ApplicationDbContext, int, Task<Product?>> _getById =
    EF.CompileAsyncQuery((ApplicationDbContext ctx, int id) =>
        ctx.Products.Include(p => p.Category).FirstOrDefault(p => p.Id == id));

// Split queries (prevent cartesian explosion)
var orders = await _context.Orders
    .Include(o => o.OrderItems).ThenInclude(oi => oi.Product)
    .AsSplitQuery()
    .ToListAsync(ct);

// Raw SQL for complex queries
var report = await _context.Database
    .SqlQuery<ProductSalesReport>($@"
        SELECT p.Id, p.Name, SUM(oi.Quantity) as TotalSold
        FROM Products p INNER JOIN OrderItems oi ON p.Id = oi.ProductId
        WHERE YEAR(o.CreatedAt) = {year}
        GROUP BY p.Id, p.Name")
    .ToListAsync(ct);
```

## Quick Reference

| Pattern | Usage |
|---------|-------|
| `AsNoTracking()` | Read-only queries |
| `Include()` | Eager loading |
| `ThenInclude()` | Nested relationships |
| `AsSplitQuery()` | Prevent cartesian explosion |
| `FirstOrDefaultAsync()` | Single or null |
| `ToListAsync()` | Execute and get list |
| `EF.CompileAsyncQuery` | Compiled queries |
| `AddAsync()` | Add entity |
| `Update()` | Mark modified |
| `Remove()` | Mark for deletion |
| `SaveChangesAsync()` | Persist changes |
