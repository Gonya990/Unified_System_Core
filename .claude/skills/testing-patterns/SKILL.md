# Testing Patterns Skill

Test-Driven Development workflow and testing best practices.

## TDD Workflow

### The Cycle

```
RED → GREEN → REFACTOR → REPEAT
```

1. **RED**: Write a failing test first
2. **GREEN**: Write minimum code to pass
3. **REFACTOR**: Improve code without changing behavior
4. **REPEAT**: Next requirement

### Why TDD?

- Forces you to think about requirements first
- Guarantees test coverage
- Produces smaller, focused functions
- Documents expected behavior

## Test Structure

### AAA Pattern

```javascript
describe('calculateTotal', () => {
  it('should apply discount when quantity exceeds 10', () => {
    // Arrange
    const items = createMockItems(15);
    const discountRate = 0.1;
    
    // Act
    const result = calculateTotal(items, discountRate);
    
    // Assert
    expect(result).toBe(135); // 150 - 10% discount
  });
});
```

### Behavior-Driven Naming

```javascript
describe('UserService', () => {
  describe('when user is authenticated', () => {
    it('should return user profile', () => {});
    it('should update last login timestamp', () => {});
  });
  
  describe('when user is not authenticated', () => {
    it('should throw UnauthorizedError', () => {});
    it('should not expose user data', () => {});
  });
});
```

## Factory Pattern for Test Data

### Create Reusable Factories

```javascript
function createMockUser(overrides = {}) {
  return {
    id: 'user-123',
    email: 'test@example.com',
    name: 'Test User',
    role: 'user',
    createdAt: new Date('2024-01-01'),
    ...overrides
  };
}

function createMockOrder(overrides = {}) {
  return {
    id: 'order-456',
    userId: 'user-123',
    items: [],
    total: 0,
    status: 'pending',
    ...overrides
  };
}
```

### Using Factories

```javascript
it('should calculate admin discount', () => {
  const adminUser = createMockUser({ role: 'admin' });
  const order = createMockOrder({ total: 100 });
  
  const result = applyUserDiscount(order, adminUser);
  
  expect(result.total).toBe(80); // 20% admin discount
});
```

## Mocking Patterns

### Module Mocking

```javascript
jest.mock('./api', () => ({
  fetchUser: jest.fn(),
  updateUser: jest.fn()
}));

import { fetchUser } from './api';

beforeEach(() => {
  jest.clearAllMocks();
});

it('should fetch user on mount', async () => {
  fetchUser.mockResolvedValue(createMockUser());
  
  render(<UserProfile userId="123" />);
  
  expect(fetchUser).toHaveBeenCalledWith('123');
});
```

### Spy on Implementation

```javascript
it('should log errors', () => {
  const consoleSpy = jest.spyOn(console, 'error').mockImplementation();
  
  processData(invalidInput);
  
  expect(consoleSpy).toHaveBeenCalledWith(
    expect.stringContaining('Invalid input')
  );
  
  consoleSpy.mockRestore();
});
```

## Async Testing

### Promises

```javascript
it('should resolve with user data', async () => {
  const result = await fetchUser('123');
  expect(result.id).toBe('123');
});
```

### Error Cases

```javascript
it('should reject when user not found', async () => {
  await expect(fetchUser('invalid')).rejects.toThrow('User not found');
});
```

### Timers

```javascript
jest.useFakeTimers();

it('should debounce input', () => {
  const callback = jest.fn();
  const debouncedFn = debounce(callback, 300);
  
  debouncedFn();
  debouncedFn();
  debouncedFn();
  
  expect(callback).not.toHaveBeenCalled();
  
  jest.advanceTimersByTime(300);
  
  expect(callback).toHaveBeenCalledTimes(1);
});
```

## What to Test

### DO Test

- Business logic and calculations
- Error handling paths
- Edge cases (empty, null, boundary values)
- State transitions
- Integration between components

### DON'T Test

- Framework/library internals
- Simple getters/setters
- Third-party code
- Implementation details (test behavior, not how)

## Test Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Testing mock behavior | Tests pass but code is broken | Test real behavior through public API |
| Hard-coded test data | Brittle, hard to maintain | Use factory functions |
| No error case tests | Bugs in error handling | Test both happy and error paths |
| Testing implementation | Tests break on refactor | Test observable behavior |
| One huge test | Hard to debug failures | Small, focused tests |

## Coverage Guidelines

- Aim for meaningful coverage, not 100%
- Critical paths: 100% coverage
- Business logic: 90%+ coverage
- UI components: Focus on behavior, not snapshots
- Don't write tests just to boost numbers

## Test Checklist

Before considering a feature complete:

- [ ] All requirements have corresponding tests
- [ ] Happy path is tested
- [ ] Error cases are tested
- [ ] Edge cases are tested (null, empty, boundaries)
- [ ] Tests are readable and maintainable
- [ ] Tests run quickly (<100ms each guideline)
- [ ] No flaky tests
