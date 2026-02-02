# Test-First Development (TFD) - Mandatory for Backend

**All backend code MUST follow Test-First Development.**

## Core Principle

> "Write the test that forces you to write the code you already know you need to write."
> - Kent Beck, Creator of Test-Driven Development

## The TFD Cycle (RED-GREEN-REFACTOR)

```
┌─────────────────────────────────────┐
│  1. RED: Write a failing test      │
│     - Test describes what code     │
│       should do, not how          │
│     - Test fails (no impl yet)     │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│  2. GREEN: Make it pass            │
│     - Write MINIMAL code           │
│     - Just enough to pass test     │
│     - Don't optimize yet           │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│  3. REFACTOR: Clean up             │
│     - Improve code quality         │
│     - Extract functions/classes    │
│     - Tests MUST stay green        │
└──────────────┬──────────────────────┘
               ↓
         REPEAT for next feature
```

## Why Test-First is Non-Negotiable

### Quantified Benefits

- **40-80% fewer production bugs** (Microsoft Research, 2008)
- **50% faster debugging** - Bugs caught immediately, not in production
- **90% regression prevention** - Tests catch breaking changes
- **Zero dead code** - Every line exists to pass a test

### Design Benefits

1. **Forces clear interfaces** - Can't test unclear APIs
2. **Prevents over-engineering** - Write only what's needed
3. **Living documentation** - Tests show how to use code
4. **Refactor fearlessly** - Green tests = safe to optimize

## TFD in Practice

### Example 1: User Registration Handler

#### ❌ WRONG: Implementation-First (Don't Do This)

```typescript
// Writing implementation first, then adding tests as afterthought
export async function registerUser(req: Request, res: Response) {
  const { email, password, name } = req.body;
  
  // Implementation written without tests guiding design
  const user = await db.users.insert({ email, password, name });
  res.json(user);
}

// Tests added later (if at all) just verify what code does,
// not what it SHOULD do
```

**Problems:**
- No validation design upfront
- Stores plaintext password (security flaw)
- No duplicate email check
- No error handling
- Tests become afterthought

#### ✅ RIGHT: Test-First (Always Do This)

**Step 1: RED - Write failing tests**

```typescript
// tests/registerUser.test.ts
import { describe, it, expect, beforeEach } from 'vitest';
import { registerUser } from '../handlers/registerUser';
import { db } from '../database';

describe('registerUser', () => {
  beforeEach(async () => {
    await db.users.deleteMany({}); // Clean state
  });

  it('should register user with valid data', async () => {
    const userData = {
      email: 'test@example.com',
      password: 'SecurePass123!',
      name: 'Test User'
    };
    
    const user = await registerUser(userData);
    
    expect(user.id).toBeDefined();
    expect(user.email).toBe('test@example.com');
    expect(user.name).toBe('Test User');
    expect(user.password).toBeUndefined(); // Don't expose password
  });

  it('should hash password before storing', async () => {
    const userData = {
      email: 'test@example.com',
      password: 'PlainPassword123'
    };
    
    await registerUser(userData);
    
    const dbUser = await db.users.findOne({ email: 'test@example.com' });
    expect(dbUser.password).not.toBe('PlainPassword123');
    expect(dbUser.password).toMatch(/^\$argon2id\$/);
  });

  it('should reject duplicate email', async () => {
    await registerUser({ email: 'existing@example.com', password: 'Pass123!' });
    
    await expect(
      registerUser({ email: 'existing@example.com', password: 'Pass456!' })
    ).rejects.toThrow('Email already exists');
  });

  it('should validate email format', async () => {
    await expect(
      registerUser({ email: 'invalid-email', password: 'Pass123!' })
    ).rejects.toThrow('Invalid email format');
  });

  it('should enforce password strength', async () => {
    await expect(
      registerUser({ email: 'test@example.com', password: 'weak' })
    ).rejects.toThrow('Password must be at least 8 characters');
  });
});
```

**Tests run: ALL FAIL (RED) ✓ - No implementation exists yet**

**Step 2: GREEN - Write minimal implementation**

```typescript
// handlers/registerUser.ts
import { argon2id } from 'argon2';
import { z } from 'zod';
import { db } from '../database';

const RegisterSchema = z.object({
  email: z.string().email('Invalid email format'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
  name: z.string().optional()
});

export async function registerUser(data: unknown) {
  // Validate input
  const validated = RegisterSchema.parse(data);
  
  // Check duplicate email
  const existing = await db.users.findOne({ email: validated.email });
  if (existing) {
    throw new Error('Email already exists');
  }
  
  // Hash password
  const hashedPassword = await argon2id.hash(validated.password);
  
  // Create user
  const user = await db.users.insert({
    email: validated.email,
    password: hashedPassword,
    name: validated.name
  });
  
  // Don't expose password in response
  const { password, ...safeUser } = user;
  return safeUser;
}
```

**Tests run: ALL PASS (GREEN) ✓**

**Step 3: REFACTOR - Clean up while keeping tests green**

```typescript
// Extract validation to service
class UserValidator {
  private schema = z.object({
    email: z.string().email('Invalid email format'),
    password: z.string()
      .min(8, 'Password must be at least 8 characters')
      .regex(/[A-Z]/, 'Password must contain uppercase letter')
      .regex(/[0-9]/, 'Password must contain number'),
    name: z.string().optional()
  });

  validate(data: unknown) {
    return this.schema.parse(data);
  }
}

// Extract password hashing to service
class PasswordService {
  async hash(password: string): Promise<string> {
    return argon2id.hash(password);
  }

  async verify(hash: string, password: string): Promise<boolean> {
    return argon2id.verify(hash, password);
  }
}

// Clean handler
export async function registerUser(data: unknown) {
  const validator = new UserValidator();
  const passwordService = new PasswordService();
  
  const validated = validator.validate(data);
  
  const existing = await db.users.findOne({ email: validated.email });
  if (existing) throw new Error('Email already exists');
  
  const hashedPassword = await passwordService.hash(validated.password);
  
  const user = await db.users.insert({
    ...validated,
    password: hashedPassword
  });
  
  const { password, ...safeUser } = user;
  return safeUser;
}
```

**Tests run: STILL ALL PASS (GREEN) ✓ - Refactor successful**

### Example 2: Database Query Optimization

#### ❌ WRONG: Optimize without tests

```typescript
// Optimizing without test coverage
export async function getUserOrders(userId: string) {
  // Changed to join query without tests proving it works
  return db.query(`
    SELECT o.*, u.name 
    FROM orders o 
    JOIN users u ON o.user_id = u.id 
    WHERE o.user_id = $1
  `, [userId]);
}
```

#### ✅ RIGHT: Test-first optimization

**Step 1: RED - Write performance test**

```typescript
import { describe, it, expect, beforeAll } from 'vitest';
import { getUserOrders } from '../queries/getUserOrders';

describe('getUserOrders performance', () => {
  beforeAll(async () => {
    // Seed test data
    const user = await db.users.insert({ name: 'Test User' });
    await db.orders.insertMany(
      Array(100).fill(null).map((_, i) => ({
        user_id: user.id,
        total: 100 + i,
        status: 'completed'
      }))
    );
  });

  it('should fetch user orders in under 50ms', async () => {
    const start = Date.now();
    const orders = await getUserOrders('test-user-id');
    const duration = Date.now() - start;
    
    expect(duration).toBeLessThan(50);
    expect(orders).toHaveLength(100);
  });

  it('should include user name in response', async () => {
    const orders = await getUserOrders('test-user-id');
    expect(orders[0].userName).toBe('Test User');
  });
});
```

**Step 2: GREEN - Implement optimized query**

```typescript
export async function getUserOrders(userId: string) {
  return db.query(`
    SELECT 
      o.id,
      o.total,
      o.status,
      o.created_at,
      u.name as user_name
    FROM orders o
    JOIN users u ON o.user_id = u.id
    WHERE o.user_id = $1
    ORDER BY o.created_at DESC
  `, [userId]);
}
```

**Step 3: REFACTOR - Add index if needed**

```sql
-- migration: add_orders_user_id_index.sql
CREATE INDEX idx_orders_user_id ON orders(user_id);
```

**Tests verify performance improvement ✓**

## Clean Test Guidelines

### NO "Arrange/Act/Assert" Comments

**❌ Bad: Redundant comments**

```typescript
it('should create order', async () => {
  // Arrange
  const userId = 'user-123';
  const items = [{ productId: 'prod-1', quantity: 2 }];
  
  // Act
  const order = await createOrder(userId, items);
  
  // Assert
  expect(order.total).toBe(100);
});
```

**✅ Good: Self-documenting structure**

```typescript
it('should create order with correct total', async () => {
  const userId = 'user-123';
  const items = [
    { productId: 'prod-1', quantity: 2, price: 25 },
    { productId: 'prod-2', quantity: 1, price: 50 }
  ];
  
  const order = await createOrder(userId, items);
  
  expect(order.total).toBe(100);
  expect(order.items).toHaveLength(2);
  expect(order.status).toBe('pending');
});
```

### Test Names Should Be Specifications

**❌ Bad: Vague names**
```typescript
it('tests the user function', async () => { ... });
it('works correctly', async () => { ... });
```

**✅ Good: Clear specifications**
```typescript
it('should return 404 when user does not exist', async () => { ... });
it('should hash password using argon2id before storage', async () => { ... });
it('should reject duplicate email addresses', async () => { ... });
```

## Coverage Requirements

**Test-First Development ensures proper coverage by design:**

| Component | Coverage | Why |
|-----------|----------|-----|
| Handlers | 100% | Entry points must be tested |
| Validators | 100% | Input validation is critical |
| Domain logic | 100% | Business rules must be verified |
| Database queries | 100% | Data integrity is essential |
| Utils/helpers | 80%+ | Reusable code needs tests |

**Overall target: 70% unit, 20% integration, 10% E2E**

## Common Anti-Patterns to Avoid

### 1. Writing Tests After Implementation

**Problem:** Tests become validation of what code does, not what it should do

```typescript
// ❌ Code written first
export function calculateDiscount(price: number, couponCode: string) {
  if (couponCode === 'SAVE10') return price * 0.9;
  return price;
}

// Test just validates existing behavior
it('should work with SAVE10 code', () => {
  expect(calculateDiscount(100, 'SAVE10')).toBe(90);
});
// Missing: expired coupons, invalid codes, negative prices, etc.
```

### 2. Mocking Everything

**Problem:** Tests don't verify real behavior

```typescript
// ❌ Over-mocking
jest.mock('./database');
jest.mock('./emailService');
jest.mock('./paymentGateway');

// Test verifies mocks, not actual integration
```

**✅ Better: Test real integrations with test database**

```typescript
// Use real test database (with TestContainers)
import { GenericContainer } from 'testcontainers';

beforeAll(async () => {
  const container = await new GenericContainer('postgres:15')
    .withExposedPorts(5432)
    .start();
  
  db = createConnection({
    host: 'localhost',
    port: container.getMappedPort(5432)
  });
});
```

### 3. Testing Implementation Details

**Problem:** Tests break when refactoring

```typescript
// ❌ Testing internal implementation
it('should call helper function', () => {
  const spy = jest.spyOn(service, 'internalHelper');
  service.doSomething();
  expect(spy).toHaveBeenCalled();
});

// ✅ Test public behavior
it('should return correct result', () => {
  const result = service.doSomething();
  expect(result).toBe(expectedValue);
});
```

## Test-First Checklist

Before writing any backend code:

- [ ] **Write failing test first** (RED)
- [ ] Test describes **what code should do**, not how
- [ ] Test covers **happy path** and **error cases**
- [ ] Test covers **edge cases** (null, empty, boundaries)
- [ ] Test names are **clear specifications**
- [ ] **NO "Arrange/Act/Assert" comments**
- [ ] Run test - verify it **FAILS** (no implementation yet)
- [ ] Write **minimal code** to pass test (GREEN)
- [ ] Run test - verify it **PASSES**
- [ ] **Refactor** code while keeping tests green
- [ ] Run tests again - verify **STILL PASSING**

## Resources

- **Test-Driven Development by Example** - Kent Beck
- **Growing Object-Oriented Software, Guided by Tests** - Steve Freeman
- **Vitest Documentation:** https://vitest.dev/
- **Testing Best Practices:** https://testingjavascript.com/
- **Backend Testing Strategies:** See `backend-testing.md`

## Summary

> **Test-First Development is not optional for backend code.**
>
> Write the test. Watch it fail. Make it pass. Clean it up. Repeat.
>
> Every bug caught in a test is a bug that never reaches production.
