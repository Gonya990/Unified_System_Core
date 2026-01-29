---
name: guard-clause-enforcer
description: Eliminate nested conditionals via early returns and inverted checks; flatten the happy path to reduce cognitive load and improve code readability.
---

# Guard Clause Enforcer

## Core Principle

**"Arrow Code" (deeply nested `if/else` statements) dramatically increases cognitive load. Guard Clauses invert conditions, return early, and flatten the happy path to the bottom of the function.**

This is the **Prime Directive for Code Readability**: every function should have its success case at the lowest indentation level.

---

## The Guard Clause Algorithm

1. **Scan** the logic for nested prerequisites (e.g., `if (user && user.isAdmin)`)
2. **Invert** the condition to check for the negative/failure state first
3. **Return Early** (or `throw`, or `continue`) immediately inside the inverted check
4. **Flatten** the "Happy Path" so it resides at the very bottom, indented by zero levels

---

## Anti-Pattern: Arrow Code

```python
# BAD: Arrow Code (4+ levels of nesting)
def process_order(user, order):
    if user:
        if user.is_active:
            if order:
                if order.items:
                    if order.total > 0:
                        # Finally, the actual logic buried deep
                        return execute_payment(order)
                    else:
                        return Error("Empty total")
                else:
                    return Error("No items")
            else:
                return Error("No order")
        else:
            return Error("Inactive user")
    else:
        return Error("No user")
```

## Correct Pattern: Guard Clauses

```python
# GOOD: Guard Clauses (flat happy path)
def process_order(user, order):
    if not user:
        return Error("No user")
    if not user.is_active:
        return Error("Inactive user")
    if not order:
        return Error("No order")
    if not order.items:
        return Error("No items")
    if order.total <= 0:
        return Error("Empty total")
    
    # Happy path at bottom, zero nesting
    return execute_payment(order)
```

---

## Language-Specific Implementations

### TypeScript / JavaScript (React, Vue, Svelte)

**Pattern:** Invert boolean checks and return `null` (for UI) or `void` early.

```typescript
// BAD
function UserDashboard({ user }: Props) {
  if (isLoading) {
    return <Spinner />;
  } else {
    if (user) {
      if (user.isAdmin) {
        return <AdminDashboard user={user} />;
      } else {
        return <UserPanel user={user} />;
      }
    } else {
      return <LoginPrompt />;
    }
  }
}

// GOOD
function UserDashboard({ user }: Props) {
  if (isLoading) return <Spinner />;
  if (!user) return <LoginPrompt />;
  if (!user.isAdmin) return <UserPanel user={user} />;
  
  return <AdminDashboard user={user} />;  // Happy path
}
```

### Rust

**Pattern:** Use `let-else` statements to unwrap `Option`/`Result` without nesting.

```rust
// BAD
fn process(opt: Option<User>) -> Result<(), Error> {
    if let Some(user) = opt {
        if user.is_valid() {
            // logic
            Ok(())
        } else {
            Err(Error::InvalidUser)
        }
    } else {
        Err(Error::NotFound)
    }
}

// GOOD
fn process(opt: Option<User>) -> Result<(), Error> {
    let Some(user) = opt else {
        return Err(Error::NotFound);
    };
    if !user.is_valid() {
        return Err(Error::InvalidUser);
    }
    
    // Happy path
    Ok(())
}
```

### Go

**Pattern:** Handle errors immediately after the function call.

```go
// BAD
func processUser(id string) (*User, error) {
    user, err := fetchUser(id)
    if err == nil {
        if user.IsActive {
            // nested logic
            return user, nil
        } else {
            return nil, ErrInactiveUser
        }
    } else {
        return nil, err
    }
}

// GOOD
func processUser(id string) (*User, error) {
    user, err := fetchUser(id)
    if err != nil {
        return nil, err
    }
    if !user.IsActive {
        return nil, ErrInactiveUser
    }
    
    // Happy path
    return user, nil
}
```

### Python

**Pattern:** Check for "falsy" values or invalid states at the top.

```python
# BAD
def validate_and_process(data):
    if data:
        if data.get("valid"):
            if len(data.get("items", [])) > 0:
                return process(data)
    return None

# GOOD
def validate_and_process(data):
    if not data:
        return None
    if not data.get("valid"):
        return None
    if len(data.get("items", [])) == 0:
        return None
    
    return process(data)  # Happy path
```

### Java

**Pattern:** Fail fast. Throw exceptions or return early before complex logic.

```java
// BAD
public Result process(Request request) {
    if (request != null) {
        if (request.isValid()) {
            if (request.hasPermission()) {
                return doProcess(request);
            }
        }
    }
    return Result.failure();
}

// GOOD
public Result process(Request request) {
    if (request == null) {
        throw new IllegalArgumentException("Request cannot be null");
    }
    if (!request.isValid()) {
        return Result.failure("Invalid request");
    }
    if (!request.hasPermission()) {
        return Result.failure("Permission denied");
    }
    
    return doProcess(request);  // Happy path
}
```

### Ruby

**Pattern:** Use early returns with `unless` or negative conditions.

```ruby
# BAD
def process_order(order)
  if order
    if order.valid?
      if order.items.any?
        execute(order)
      end
    end
  end
end

# GOOD
def process_order(order)
  return unless order
  return unless order.valid?
  return if order.items.empty?
  
  execute(order)  # Happy path
end
```

---

## Quick Decision Tree

```
Is there nested if/else logic?
    ├── No → No action needed
    └── Yes → Can the inner condition be inverted?
              ├── No → Consider restructuring logic
              └── Yes → Apply Guard Clause:
                        1. Invert condition
                        2. Return/throw early
                        3. Remove else block
                        4. Repeat until happy path is flat
```

---

## Benefits

| Metric | Impact |
|--------|--------|
| **Cognitive Load** | Reduced - reader processes one condition at a time |
| **Indentation Levels** | Typically reduced from 4-6 to 0-1 |
| **Cyclomatic Complexity** | Lower - fewer branching paths to track |
| **Testability** | Higher - each guard clause is independently testable |
| **Debugging** | Easier - failures happen at specific guard points |

---

## Anti-Patterns to Avoid

### 1. Guard Clause with Side Effects
```python
# BAD - side effect in guard
if not validate_and_log(user):  # logging is side effect
    return Error()
```

### 2. Excessive Guards (Shotgun Guards)
```python
# BAD - too granular, consider combining
if not user:
    return Error()
if not user.name:
    return Error()
if not user.email:
    return Error()
if not user.id:
    return Error()

# BETTER - combine related checks
if not user or not all([user.name, user.email, user.id]):
    return Error("Invalid user")
```

### 3. Hidden Happy Path
```python
# BAD - happy path not obvious
def process(x):
    if condition_a:
        return handle_a()
    if condition_b:
        return handle_b()
    if condition_c:
        return handle_c()
    return default()  # Is this the happy path or error case?

# GOOD - make intent clear with comments or structure
def process(x):
    # Error cases
    if error_condition_a:
        return handle_error_a()
    if error_condition_b:
        return handle_error_b()
    
    # Success path
    return process_success()
```

---

## Integration with Other Skills

- **separation-of-concerns-enforcer**: Guard clauses at function boundaries maintain clean separation
- **refactoring-mastery**: Use "Replace Nested Conditional with Guard Clauses" refactoring pattern
- **cohesion-coach**: Guards keep validation logic cohesive at function entry
- **feedback-driven-design**: Flat code is easier to test (each guard = one test case)

---

## The Refactor Process

When you encounter arrow code:

1. **Identify** the deepest nested success case (this is your happy path)
2. **Work outward** - for each condition wrapping the happy path:
   - Invert it
   - Add early return/throw
   - Remove the `else` block
3. **Verify** tests still pass after each step
4. **Result**: Happy path at bottom, zero nesting

---

## Success Metrics

| Metric | Target |
|--------|--------|
| Maximum nesting depth | ≤2 levels in any function |
| Functions with arrow code | 0 (refactor on sight) |
| Happy path indentation | 0-1 levels |
| Guard clause coverage | 100% of preconditions |

---

## Key Insight

> "Refactored to eliminate nesting using Guard Clauses."

This is the default response when applying this skill. Guard clauses are not optional style - they are a **mandatory readability pattern** that reduces cognitive load for every reader of the code.
