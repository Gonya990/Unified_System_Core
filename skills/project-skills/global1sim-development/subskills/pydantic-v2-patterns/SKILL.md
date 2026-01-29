---
name: pydantic-v2-patterns
description: Pydantic V2 immutable models with validation - frozen=True enables evolutionary design; supports separation-of-concerns (pure domain models)
parent: global1sim-development
activation_triggers:
  - "creating domain model"
  - "data validation needed"
  - "API request/response models"
mandatory_config:
  frozen: true
  validation: field_validator
---

# Pydantic V2 Patterns (Immutable Models)

**AGENTIC**: Always use frozen=True for immutability. Why? Enables evolutionary design.

## Template (LLM: Use This Pattern)

```python
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from decimal import Decimal

class Subscriber(BaseModel):
    """
    Domain model - immutable, validated, pure
    
    WHY frozen=True?
    1. Thread-safe (no concurrent modification)
    2. Evolutionary design (can't mutate shared state)
    3. Testable (deterministic, no side effects)
    4. Refactoring confidence (pure functions)
    
    Book: separation-of-concerns-enforcer (essential complexity only)
    """
    model_config = {"frozen": True}  # MANDATORY
    
    # Required fields
    id: str = Field(min_length=1, description="Unique subscriber ID")
    email: str
    
    # Optional fields
    name: Optional[str] = None
    credit_limit: Decimal = Field(default=Decimal("0"), ge=0)
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, v: str) -> str:
        # Validation logic here
        if '@' not in v:
            raise ValueError('Invalid email')
        return v.lower().strip()
```

## Why Immutability? (LLM: Explain This)

**From Modern SE book**:
- Immutable data enables refactoring in tiny steps
- No side effects = easier to reason about
- Pure functions compose well

**Pattern for changes**:
```python
# DON'T mutate
subscriber.name = "New Name"  # ERROR: frozen!

# DO create new instance
updated = subscriber.model_copy(update={"name": "New Name"})
```

## Decision Tree

```yaml
creating_model:
  domain_model: → frozen=True (always)
  api_request: → frozen=True (validate input)
  api_response: → frozen=True (serialize output)
  database_orm: → separate model (don't mix concerns)
```

## Integration

- Parent: `global1sim-development`
- Skills: `separation-of-concerns-enforcer` (domain models are essential complexity)
- Pattern: Ports & Adapters (`python-hexagonal-development`)

**Always**: frozen=True, field_validator, complete type hints
