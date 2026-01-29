# Pydantic V2 Patterns

---

## Immutable Models (Frozen)

```python
from pydantic import BaseModel, Field, field_validator

class Subscriber(BaseModel):
    model_config = {"frozen": True}  # Enables immutability

    id: str
    name: str = Field(min_length=1, max_length=100)
    email: str

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()
```

**Benefits**:
- Thread-safe
- Testable
- Enables evolutionary design

---

## Creating Modified Copies

```python
# Don't mutate, create new instance
original = Subscriber(id="1", name="John", email="j@ex.com")
updated = original.model_copy(update={"name": "Jane"})
```

---

## Field Validation

```python
from pydantic import Field

class Order(BaseModel):
    quantity: int = Field(gt=0, le=100)
    price: Decimal = Field(ge=0)
    notes: Optional[str] = Field(default=None, max_length=500)
```

---

## Custom Validators

```python
@field_validator('email')
@classmethod
def validate_email(cls, v: str) -> str:
    if '@' not in v:
        raise ValueError('Invalid email format')
    return v.lower()
```

---

## Model Configuration

```python
class Settings(BaseModel):
    model_config = {
        "frozen": True,           # Immutable
        "extra": "forbid",        # Reject unknown fields
        "str_strip_whitespace": True,
    }
```
