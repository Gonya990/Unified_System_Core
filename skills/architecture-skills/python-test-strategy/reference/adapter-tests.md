# Adapter Test Playbook

## Checklist
1. Choose scope: one adapter + real dependency you own (DB, queue, filesystem).
2. Spin up ephemeral dependency (Testcontainers Postgres, temporary directory, WireMock).
3. Seed data via idempotent fixtures; never rely on shared state.
4. Run assertions on the adapter surface only (port methods).
5. Tear down automatically to avoid residue.

## Example (Postgres)
```python
from testcontainers.postgres import PostgresContainer
from src.repositories.subscriber_adapter import SqlSubscriberAdapter


def test_sql_adapter_persists_subscriber() -> None:
    with PostgresContainer("postgres:15-alpine") as pg:
        session = build_session(pg.get_connection_url())
        adapter = SqlSubscriberAdapter(session)

        adapter.save(sample_subscriber)

        fetched = adapter.fetch_by_iccid(sample_subscriber.iccid)
        assert fetched == sample_subscriber
```

## Flake prevention tips
- Wait for container health (e.g., `pg.get_connection_url()` inside context ensures readiness).
- Keep tests hermetic; never connect to shared dev resources.
- Fail fast with descriptive error messages when setup data is missing.

## When NOT to write adapter tests
- When logic duplicates existing service tests—keep business rules in unit/acceptance suites.
- When dependency is outside your control (3rd-party SaaS); prefer contract tests or mocks at acceptance level.
