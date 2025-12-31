# Feature Delivery Workflow

Copy this checklist before starting work:

```
Feature Progress:
- [ ] Step 1: DeepContext search for existing ports/services
- [ ] Step 2: RED — add/adjust pytest failing test
- [ ] Step 3: GREEN — implement minimal change in service/adapter
- [ ] Step 4: REFACTOR — align names, remove duplication
- [ ] Step 5: Quality gate — `uv run pytest`, `uv run ruff check`, `uv run mypy src`
- [ ] Step 6: Update acceptance notes/tests if behavior shifted
```

## Step 1: DeepContext
- Run `mcp__deepcontext__get_indexing_status`; re-index if stale.
- Search for similar services/ports before adding new files.

## Step 2: RED
- Place new unit tests under `tests/unit` mirroring module paths.
- For service logic, prefer table-driven parametrized tests.

## Step 3: GREEN
- Touch only the layer under test (service or adapter) until it passes.
- Keep implementation minimal; duplication is acceptable until refactor.

## Step 4: REFACTOR
- Remove duplication, rename ports, and ensure dependency direction.
- Confirm immutability of models (Pydantic `model_config = ConfigDict(frozen=True)`).

## Step 5: Quality gate
- Run `uv run pytest` (full suite) and ensure coverage delta is non-negative.
- Lint: `uv run ruff check`.
- Types: `uv run mypy src`.

## Step 6: Acceptance sync
- If public behavior changed, update acceptance specs (see `python-test-strategy/reference/acceptance-tests.md`).
- Note any new fakes or fixtures needed for developers.
