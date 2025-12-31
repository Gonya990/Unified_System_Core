# Acceptance Test Guide

## Purpose
Prove that a single deployable unit (FastAPI app, background worker) delivers business capabilities while faking all external services.

## Workflow
```
Acceptance Suite:
- [ ] Boot service in-process (FastAPI TestClient or CLI entrypoint)
- [ ] Override external dependencies with fakes/mocks (WireMock, in-memory ports)
- [ ] Use realistic payloads and cover success + failure paths
- [ ] Assert both HTTP response and state change (DB, events)
- [ ] Keep suite runtime under 20 min; fail build if exceeded
```

## FastAPI example
```python
from fastapi.testclient import TestClient
from src.api.main import app
from tests.fakes.subscriber_repo import FakeSubscriberRepo


fake_repo = FakeSubscriberRepo()
app.dependency_overrides[get_subscriber_repo] = lambda: fake_repo
client = TestClient(app)


def test_activate_subscriber_flow() -> None:
    response = client.post("/subscribers/activate", json={"iccid": "123", "plan": "data-5gb"})
    assert response.status_code == 202
    assert fake_repo.fetch_by_iccid("123").plan == "data-5gb"
```

## Best practices
- Scope tests per bounded context; never call downstream microservices.
- Record fixtures close to real payloads; store them under `tests/fixtures/acceptance`.
- Parallelize via pytest-xdist if runtime creeps up (but fix slow tests first).
- If a scenario requires another service, replace it with a consumer-driven contract.
