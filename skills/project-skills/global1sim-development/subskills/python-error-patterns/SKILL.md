---
name: python-error-patterns  
description: Modern Python error handling - Exceptions for errors, Optional for "might not exist"; supports separation-of-concerns
parent: global1sim-development
---

# Python Error Patterns (Exceptions vs Optional)

**AGENTIC RULE**: Exceptions for errors, Optional for "no value".

## Decision Tree (LLM: Follow This)

```python
def when_to_use_what(scenario):
    """
    Decision tree for error handling
    """
    if scenario == "might_not_exist":
        # Expected absence (not an error)
        return "Optional[T]"
        # Example: find_by_id() might not find anything
        
    elif scenario == "unexpected_failure":
        # Error condition (exceptional)
        return "raise Exception"
        # Example: database connection failed
        
    elif scenario == "validation_failure":
        # Invalid input (error)
        return "raise ValueError"
        # Example: email format invalid
        
    elif scenario == "not_found_after_check":
        # Checked but missing (error)
        return "raise NotFoundError"
        # Example: get_by_id() expects it exists
```

## Patterns (LLM: Use These)

### Pattern 1: Optional for "Might Not Exist"

```python
from typing import Optional

def find_subscriber(id: str) -> Optional[Subscriber]:
    """
    Might not find subscriber - that's OK (not an error)
    Returns None if not found.
    """
    result = db.query(Subscriber).filter_by(id=id).first()
    return result  # None or Subscriber
```

### Pattern 2: Exception for Actual Errors

```python
class SubscriberNotFoundError(Exception):
    """Custom exception for domain errors"""
    pass

def activate_subscriber(id: str) -> Subscriber:
    """
    Expects subscriber to exist - if not, that's an ERROR
    Raises exception if not found.
    """
    subscriber = find_subscriber(id)
    if subscriber is None:
        raise SubscriberNotFoundError(f"Subscriber {id} not found")
    
    # Return updated copy (immutable!)
    return subscriber.model_copy(update={"active": True})
```

### Pattern 3: Let Exceptions Bubble to API

```python
# Service layer: Raise exceptions
def process_order(order_id: str) -> Order:
    order = find_order(order_id)
    if order is None:
        raise OrderNotFoundError(order_id)
    return order


# API layer: Catch and translate to HTTP
@app.post("/orders/{order_id}/process")
def process_order_endpoint(order_id: str):
    try:
        order = service.process_order(order_id)
        return {"id": order.id}
    except OrderNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
```

## Book Alignment

**separation-of-concerns-enforcer**:
- Business logic (services) raises domain exceptions
- API layer catches and translates to HTTP
- Repository layer returns Optional or raises

## Quick Reference

```yaml
use_optional:
  - find_by_id (might not exist)
  - search (might be empty)
  - lookup (might be None)
  
use_exception:
  - get_by_id (expects to exist)
  - validation failure
  - business rule violation
  - infrastructure failure
```
