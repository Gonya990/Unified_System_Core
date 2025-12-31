# Programming Patterns

This directory contains extracted programming patterns from the Global1SIM project.

---

## Workflows

| Pattern | Description |
|---------|-------------|
| [tdd-workflow](workflows/tdd-workflow.md) | RED-GREEN-REFACTOR cycle |
| [trunk-based-development](workflows/trunk-based-development.md) | Commit 3-5+ times/day to main |

---

## Architecture

| Pattern | Description |
|---------|-------------|
| [hexagonal-architecture](architecture/hexagonal-architecture.md) | Ports & adapters, separation of concerns |

---

## Tooling

| Pattern | Description |
|---------|-------------|
| [uv-package-manager](tooling/uv-package-manager.md) | Fast Python package management |
| [pydantic-patterns](tooling/pydantic-patterns.md) | Immutable models, validation |
| [pytest-patterns](tooling/pytest-patterns.md) | Test fixtures, parametrization |

---

## Quick Start

1. **TDD**: Use RED-GREEN-REFACTOR for all changes
2. **Commits**: 3-5+ atomic commits per day
3. **Models**: Frozen Pydantic models
4. **Tests**: Fast feedback (< 10s for unit suite)
