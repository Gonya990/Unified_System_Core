# Pytest Patterns

---

## Test Structure

```python
def test_<action>_<condition>_<expected_result>():
    # Arrange
    data = create_test_data()

    # Act
    result = function_under_test(data)

    # Assert
    assert result == expected
```

---

## Fixtures

```python
import pytest

@pytest.fixture
def valid_subscriber() -> Subscriber:
    return Subscriber(
        id="sub_123",
        name="John Doe",
        email="john@example.com"
    )

def test_can_activate_subscriber(valid_subscriber):
    result = activate(valid_subscriber)
    assert result.active is True
```

---

## Parametrized Tests

```python
@pytest.mark.parametrize("email,valid", [
    ("valid@example.com", True),
    ("invalid", False),
    ("", False),
])
def test_email_validation(email: str, valid: bool):
    if valid:
        subscriber = Subscriber(id="1", name="Test", email=email)
        assert subscriber.email == email
    else:
        with pytest.raises(ValueError):
            Subscriber(id="1", name="Test", email=email)
```

---

## Test Organization

```
tests/
├── unit/           # Fast, isolated tests
│   └── test_services.py
├── integration/    # Tests with real dependencies
│   └── test_repositories.py
└── conftest.py     # Shared fixtures
```

---

## Running Tests

```bash
# Run all tests
uv run pytest tests/ -v

# Run specific test
uv run pytest tests/test_feature.py::test_name -v

# Run with coverage
uv run pytest --cov=src --cov-report=html

# Run failed first
uv run pytest --ff
```

---

## Speed Requirements

- Single unit test: < 100ms
- Full unit suite: < 10 seconds
- Full test suite: < 10 minutes
