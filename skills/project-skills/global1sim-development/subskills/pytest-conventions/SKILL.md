---
name: pytest-conventions
description: Project-specific pytest patterns - naming, fixtures, parametrize; supports feedback-driven-design (fast tests)
parent: global1sim-development
---

# Pytest Conventions (Project Patterns)

**AGENTIC**: Fast, focused, descriptive tests.

## Naming Convention (LLM: Follow This Pattern)

```python
# Pattern: test_{function}_with_{condition}_returns_{expected}

def test_create_subscriber_with_valid_data_returns_subscriber():
    # Arrange
    data = {"id": "sub_123", "name": "John", "email": "j@ex.com"}
    
    # Act
    result = create_subscriber(data)
    
    # Assert
    assert isinstance(result, Subscriber)
    assert result.name == "John"
```

## Fixtures (LLM: Use for Test Data)

```python
@pytest.fixture
def valid_subscriber_data() -> dict:
    """Reusable test data"""
    return {
        "id": "sub_123",
        "name": "John Doe",
        "email": "john@example.com"
    }

def test_subscriber_creation(valid_subscriber_data):
    subscriber = Subscriber(**valid_subscriber_data)
    assert subscriber.name == "John Doe"
```

## Parametrize (LLM: Test Multiple Cases)

```python
@pytest.mark.parametrize("email,valid", [
    ("valid@example.com", True),
    ("invalid-email", False),
    ("", False),
])
def test_email_validation(email, valid):
    if valid:
        subscriber = Subscriber(id="1", email=email)
        assert subscriber.email == email
    else:
        with pytest.raises(ValueError):
            Subscriber(id="1", email=email)
```

## Speed Targets

```yaml
unit_test: < 100ms each
full_suite: < 10 seconds
ci_pipeline: < 10 minutes

if_slower:
  problem: Architecture issue
  skill: feedback-driven-design
  fix: Refactor for testability
```

## Quick Reference

```bash
# Run specific test
uv run pytest tests/test_file.py::test_function -v

# Run with coverage
uv run pytest --cov=src --cov-report=html

# Run fast (unit tests only)
uv run pytest tests/unit/ -v
```
