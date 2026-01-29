---
name: python-hexagonal-development
description: Guides Python feature work with Dave Farley–style TDD, ports-and-adapters design, and uv-based workflows; use when implementing or refactoring business logic or APIs.
---

# Python Hexagonal Development

Use this Skill whenever you need to ship or refactor Python features in Global1SIM while preserving fast feedback loops.

## Quick start
1. Run `uv sync` if dependencies changed, then open the failing test you are about to drive.
2. Before any edit, query DeepContext for existing patterns (repositories, services, fixtures).
3. Work in RED→GREEN→REFACTOR cycles; never skip the test stage.

## Guardrails
- Business logic lives in `src/services` and only depends on ports defined in `src/repositories` or `src/api/dependencies`.
- Keep models immutable (Pydantic v2, `frozen=True`).
- No direct framework or database calls inside services—add adapters instead.
- Use uv tooling exclusively (`uv run pytest`, `uv run ruff check`, `uv run mypy src`).

## Architecture map
- Follow the ports-and-adapters diagram in [reference/architecture.md](reference/architecture.md).
- Add new ports before adapters; confirm naming via the table in that reference.
- When unsure about layering, consult the “Dependency Rules” section in the same file.

## Feature workflow
Use the checklist in [reference/workflows.md](reference/workflows.md) and copy it into your working notes. It covers:
- DeepContext searches required before edits.
- TDD loops with explicit commands to run.
- Quality gates (ruff, mypy, pytest coverage).

## Examples
- Ports, services, adapters, and FastAPI dependency overrides live in [reference/examples.md](reference/examples.md).
- Each snippet includes “fast feedback” notes showing which tests guard the change.

## Related Skills
- Pair this skill with `python-test-strategy` when planning adapter or acceptance coverage.
