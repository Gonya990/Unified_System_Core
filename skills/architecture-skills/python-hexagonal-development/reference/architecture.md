# Architecture Reference

## Contents
- Layers and allowed dependencies
- Port naming rules
- Adapter checklist
- Anti-patterns to block

## Layers and allowed dependencies
- **Models (`src/models`)**: immutable Pydantic DTOs, may depend on stdlib typing only.
- **Services (`src/services`)**: pure domain logic, talk only to ports (protocols/ABCs) provided via constructor arguments.
- **Ports (`src/repositories`, `src/api/dependencies`)**: define interfaces for persistence, messaging, and integrations.
- **Adapters (`src/repositories/impl`, `src/api/routes`)**: implement ports, may import SQLAlchemy, HTTP clients, or FastAPI.
- **API (`src/api`)**: composes services + adapters, owns exception mapping.

Dependency arrows always point inward: API → adapters → ports → services → models. If you need to import from an outer layer, introduce a new port instead.

## Port naming rules
- Use nouns plus capability, e.g., `SubscriberRepository`, `UsageLedgerPort`.
- Ports live beside their adapters; export ABC/Protocol only.
- Keep method names intention revealing (`fetch_by_iccid`, `record_top_up`).

## Adapter checklist
1. Implement the port in a separate module suffixed with `_adapter.py`.
2. Inject resources (DB session, HTTP client) via constructor.
3. Cover the adapter with the appropriate tests (see `python-test-strategy`).
4. Log integration boundaries only—services stay silent.

## Anti-patterns to block
- Services importing ORM models or HTTP clients.
- Direct `uvicorn` or FastAPI dependencies in domain code.
- Tests that reach across multiple microservices; prefer fakes or contract tests.
