# Trunk-Based Development

**Based on**: Modern Software Engineering by Dave Farley

---

## Core Principle

> "Continuous integration and feature branching are not compatible. One exposes change early; the other defers it."

---

## The Rule

- **Minimum**: At least once per day
- **Target**: 3-5+ commits per day
- **Branch**: Always commit directly to `main`

---

## Daily Workflow

### Morning
```bash
git pull --rebase origin main
```

### During Day (3-5+ times)
```bash
uv run pytest tests/              # All tests pass
uv run ruff check src/ tests/     # Linting
git add .
git commit -m "atomic change"
git push origin main              # Expose immediately
```

---

## Feature Flags for Incomplete Work

```python
# src/config/settings.py
class Settings(BaseSettings):
    ENABLE_NEW_FEATURE: bool = Field(default=False)

# Usage
if settings.ENABLE_NEW_FEATURE:
    return handle_v2(data)
else:
    return handle_v1(data)
```

Benefits:
- Commit to main daily
- Deploy safely (flag off)
- Test in development (flag on)

---

## CI Requirements

```yaml
stages:
  unit_tests: "< 10 seconds"
  integration_tests: "< 5 minutes"
  linting: "< 1 minute"
  total: "< 10 minutes"
```

---

## When CI Fails

**Priority**: HIGHEST

```yaml
quick_fix: "< 5 min → fix and push"
complex_fix: "> 5 min → revert, fix locally, recommit"
time_limit: "Never leave CI red > 30 minutes"
```

---

## Anti-Patterns

- **Feature branches**: Defer integration, cause merge hell
- **Large commits**: Changes not exposed continuously
- **PR delays**: Waiting days breaks CI

---

## Summary

- Commit to `main` 3-5+ times per day
- Use feature flags for incomplete work
- CI must complete in <10 minutes
- Fix red CI within 30 minutes
