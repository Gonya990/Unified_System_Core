# UV Package Manager

**UV** is a fast Python package manager. Prefer UV over pip.

---

## Setup

```bash
uv sync                           # Install all dependencies
```

---

## Adding Dependencies

```bash
uv add package-name               # Add production dependency
uv add --dev pytest ruff mypy     # Add dev dependencies
```

---

## Running Commands

```bash
uv run pytest tests/              # Run tests
uv run ruff check src/            # Linting
uv run ruff format src/           # Formatting
uv run mypy src/                  # Type checking
```

---

## TDD Commands

```bash
# Run specific test (TDD cycle)
uv run pytest tests/test_feature.py::test_name -v

# Run with coverage
uv run pytest --cov=src --cov-report=html

# Run failed tests first
uv run pytest --ff
```

---

## Common Workflows

### Before Commit
```bash
uv run pytest tests/ && \
uv run ruff check src/ tests/ && \
uv run mypy src/
```

### CI Pipeline
```bash
uv sync
uv run pytest tests/ -v
uv run ruff check src/
uv run mypy src/
```
