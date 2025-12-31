# Hexagonal Architecture (Ports & Adapters)

**Based on**: Python Hexagonal Development skill

---

## Core Principle

Separate business logic (essential complexity) from infrastructure (accidental complexity).

---

## Layer Structure

```
src/
├── domain/          # Pure business logic (no imports from outside)
│   ├── models/      # Pydantic models (frozen=True)
│   └── services/    # Business operations (pure functions)
│
├── ports/           # Interfaces (abstract contracts)
│   └── repositories.py
│
├── adapters/        # Infrastructure implementations
│   ├── persistence/ # Database adapters
│   └── api/         # HTTP adapters
│
└── api/routes/      # FastAPI endpoints
```

---

## Domain Models (Pure)

```python
from pydantic import BaseModel, Field

class Subscriber(BaseModel):
    model_config = {"frozen": True}  # Immutable

    id: str
    name: str = Field(min_length=1, max_length=100)
    email: str
```

**Rules**:
- No database imports
- No HTTP imports
- Pure business logic only

---

## Ports (Interfaces)

```python
from abc import ABC, abstractmethod

class SubscriberRepository(ABC):
    @abstractmethod
    def save(self, subscriber: Subscriber) -> Subscriber:
        pass

    @abstractmethod
    def find_by_id(self, id: str) -> Optional[Subscriber]:
        pass
```

---

## Adapters (Implementations)

```python
class PostgresSubscriberRepository(SubscriberRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, subscriber: Subscriber) -> Subscriber:
        # Database-specific code here
        ...
```

---

## Services (Pure Business Logic)

```python
def activate_subscriber(
    subscriber: Subscriber,
    repository: SubscriberRepository
) -> Subscriber:
    if subscriber.active:
        raise AlreadyActiveError(subscriber.id)

    activated = subscriber.model_copy(update={"active": True})
    return repository.save(activated)
```

**Rules**:
- Accept dependencies as parameters
- Return new objects (immutable)
- No side effects except through ports

---

## Benefits

- **Testable**: Mock ports for unit tests
- **Flexible**: Swap adapters without changing business logic
- **Clear**: Essential complexity separated from accidental
