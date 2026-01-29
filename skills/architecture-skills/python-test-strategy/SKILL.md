---
name: python-test-strategy
description: Enforces Dave Farley–style fast feedback by defining Python unit, adapter, contract, and acceptance testing playbooks; use when planning or diagnosing tests.
---

# Python Test Strategy

Activate this Skill for any testing question: choosing coverage, fixing flaky suites, or designing new checks.

## Core principles
- Prefer thousands of fast unit tests; treat slow tests as defects.
- Adapter tests exist only to prove an integration boundary works.
- Acceptance tests run a single deployable unit in-process with faked externals.
- Delete or quarantine brittle end-to-end suites spanning multiple services.

## Quick routing
- Need the pyramid overview? See [reference/test-pyramid.md](reference/test-pyramid.md).
- Writing adapter tests (DB, HTTP, filesystem)? Use [reference/adapter-tests.md](reference/adapter-tests.md).
- Designing developer-owned acceptance suites? Follow [reference/acceptance-tests.md](reference/acceptance-tests.md).
- Tracking health (runtime, flake rate, coverage)? Check [reference/metrics.md](reference/metrics.md).

## Workflow
1. Categorize the behavior (logic, boundary, or feature) with the decision tree in `test-pyramid.md`.
2. Draft the failing test using pytest; keep runtime targets from `metrics.md` in mind.
3. Run `uv run pytest path/to/test.py -k scenario` until green.
4. Promote tests into CI only when they meet runtime + determinism criteria.

## Tooling reminders
- Use pytest fixtures + fakes for unit tests; never spin up real services there.
- Use Testcontainers only in adapter tests and tear them down automatically.
- Acceptance tests should boot the FastAPI app via `TestClient` and override dependencies with fakes or WireMock equivalents.

## Related Skills
- Pair with `python-hexagonal-development` when new features require both design and coverage decisions.
