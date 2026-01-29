# Test-Driven Development (TDD) Workflow

**Based on**: Modern Software Engineering by Dave Farley

---

## The RED-GREEN-REFACTOR Cycle

TDD operates in three phases that repeat continuously:

### Phase 1: RED - Write Failing Test

```bash
# Write test that defines desired behavior
uv run pytest tests/test_feature.py::test_new_behavior -v
# Expected: Test FAILS (verifying test is correct)
```

**Purpose**: Define expected behavior before implementation

---

### Phase 2: GREEN - Minimal Implementation

```bash
# Write simplest possible code to make test pass
uv run pytest tests/test_feature.py::test_new_behavior -v
# Expected: Test PASSES
```

**Key Rule**: Write the MINIMUM code needed to pass.

---

### Phase 3: REFACTOR - Improve Design

```bash
# Make tiny refactoring steps, run test after EACH step
uv run pytest tests/test_feature.py::test_new_behavior -v
# After each tiny change: Test still PASSES
```

**Key Rule**: Make ONE small improvement at a time. Run tests after each change.

---

## Feedback Speed Requirements

```yaml
feedback_levels:
  level_1_ide_errors: "< 100ms"
  level_2_unit_tests: "< 10 seconds"
  level_3_full_suite: "< 10 minutes"
  level_4_ci_pipeline: "< 10 minutes"
```

---

## Batch Size Limits

### Code Level
- Function: One concern per function
- Refactoring: One transformation at a time
- Test cycle: <5 seconds per RED-GREEN-REFACTOR cycle

### Commit Level
- Frequency: 3-5 commits per day minimum
- Size: <200 lines changed
- Quality: Each commit passes all tests

---

## Quick Reference Commands

```bash
# TDD Cycle (run after EVERY change)
uv run pytest tests/test_feature.py::test_name -v

# Run all tests (before commit)
uv run pytest tests/ -v

# Run with coverage
uv run pytest --cov=src --cov-report=html
```

---

## Summary

1. **RED**: Define what you want (specification)
2. **GREEN**: Make it work (implementation)
3. **REFACTOR**: Make it right (design)

Repeat in seconds, not hours. Commit 3-5+ times per day.
