# Examples

## Port definition
```python
from abc import ABC, abstractmethod
from src.models.subscriber import Subscriber


class SubscriberRepository(ABC):
    @abstractmethod
    def fetch_by_iccid(self, iccid: str) -> Subscriber | None: ...

    @abstractmethod
    def save(self, subscriber: Subscriber) -> None: ...
```

## Service using the port (pure logic)
```python
class SubscriberService:
    def __init__(self, repo: SubscriberRepository) -> None:
        self._repo = repo

    def activate(self, iccid: str, plan_code: str) -> Subscriber:
        subscriber = self._repo.fetch_by_iccid(iccid)
        if subscriber is None:
            raise ValueError("Unknown ICCID")
        updated = subscriber.activate(plan_code)
        self._repo.save(updated)
        return updated
```

## SQL adapter skeleton
```python
class SqlSubscriberAdapter(SubscriberRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def fetch_by_iccid(self, iccid: str) -> Subscriber | None:
        row = self._session.execute(
            select(DbSubscriber).where(DbSubscriber.iccid == iccid)
        ).scalar_one_or_none()
        return Subscriber.from_db(row) if row else None

    def save(self, subscriber: Subscriber) -> None:
        self._session.merge(subscriber.to_db())
```

## FastAPI dependency override
```python
def get_subscriber_service(session: Session = Depends(get_session)) -> SubscriberService:
    repo = SqlSubscriberAdapter(session)
    return SubscriberService(repo)
```

## Fast unit test with fake port
```python
class FakeRepo(SubscriberRepository):
    def __init__(self) -> None:
        self.items: dict[str, Subscriber] = {}

    def fetch_by_iccid(self, iccid: str) -> Subscriber | None:
        return self.items.get(iccid)

    def save(self, subscriber: Subscriber) -> None:
        self.items[subscriber.iccid] = subscriber


def test_activate_sets_plan():
    repo = FakeRepo()
    repo.items["123"] = Subscriber(iccid="123", plan=None)
    service = SubscriberService(repo)

    updated = service.activate("123", "data-5gb")

    assert updated.plan == "data-5gb"
```
