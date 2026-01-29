# Common Experimental Feature Patterns

Quick reference for typical experimental feature scenarios in Global1SIM.

## Pattern 1: New Integration (External API/Service)

**Use Case**: Integrating with new payment gateway, SMS provider, data enrichment API

### Workflow

```yaml
Phase 1 - SPIKE (30-45 min):
  explore:
    - API authentication method
    - Request/response format
    - Rate limits and quotas
    - Error responses
    - SDK availability
  document:
    - Average latency
    - Cost per request
    - Required credentials
    - Limitations discovered

Phase 2 - HYPOTHESIS:
  problem: "Current provider has X% failure rate"
  hypothesis: "New provider will reduce failures to Y%"
  metrics:
    - Success rate
    - Response time (P95, P99)
    - Cost per transaction
  time_box: 4-6 hours

Phase 3 - BUILD:
  commit_1: "Add ENABLE_NEW_PROVIDER feature flag"
  commit_2: "Add provider adapter with mock in tests"
  commit_3: "Implement happy path integration"
  commit_4: "Add error handling for API failures"
  commit_5: "Add circuit breaker for outages"

Phase 4 - MEASURE:
  baseline: "Current provider metrics"
  experiment: "New provider metrics (canary 10% traffic)"
  duration: "1 week monitoring"

Phase 5 - DECIDE:
  success: "Full rollout, deprecate old provider"
  iterate: "Adjust error handling, continue canary"
  kill: "Revert to current provider, document why"
```

### Example Code

```python
# settings.py
class Settings(BaseSettings):
    ENABLE_TWILIO_SMS: bool = Field(
        default=False,
        description="Use Twilio for SMS (experiment: reduce failures)"
    )

# services/sms_service.py
from src.config.settings import settings
from src.adapters.sms import CurrentProvider, TwilioProvider

def send_sms(phone: str, message: str) -> SMSResult:
    if settings.ENABLE_TWILIO_SMS:
        provider = TwilioProvider()  # Experimental
    else:
        provider = CurrentProvider()  # Production

    return provider.send(phone, message)

# tests/test_sms_service.py
def test_sms_sending_with_twilio_when_flag_enabled(monkeypatch):
    monkeypatch.setattr(settings, "ENABLE_TWILIO_SMS", True)

    result = send_sms("+1234567890", "Test message")

    assert result.success is True
    assert result.provider == "twilio"
```

## Pattern 2: Performance Optimization

**Use Case**: Adding caching, database indexing, query optimization

### Workflow

```yaml
Phase 1 - SPIKE:
  profile:
    - Identify bottleneck (use profiler, logs)
    - Measure current performance
    - Try quick fix in spike branch
  time_box: 30 min

Phase 2 - HYPOTHESIS:
  current: "API response time P95 = 850ms"
  hypothesis: "Redis cache will reduce DB queries"
  prediction: "P95 will drop to <200ms"
  success_criteria:
    - P95 <= 200ms
    - Cache hit rate >= 80%
    - No increase in error rate

Phase 3 - BUILD:
  commit_1: "Add ENABLE_REDIS_CACHE flag"
  commit_2: "Add Redis adapter with cache-aside pattern"
  commit_3: "Add cache invalidation on updates"
  commit_4: "Add monitoring for hit rate"

Phase 4 - MEASURE:
  baseline: "Load test without cache"
  experiment: "Load test with cache enabled"
  metrics:
    - Response time (P50, P95, P99)
    - Cache hit rate
    - Error rate
    - Database connection pool usage

Phase 5 - DECIDE:
  success: "Enable in prod, monitor for 1 week, remove flag"
  iterate: "Adjust TTL, cache warming strategy"
  kill: "Bottleneck is elsewhere, try different approach"
```

### Example Code

```python
# settings.py
class Settings(BaseSettings):
    ENABLE_REDIS_CACHE: bool = Field(
        default=False,
        description="Use Redis for product catalog caching"
    )
    CACHE_TTL_SECONDS: int = 300  # 5 minutes

# services/product_service.py
from src.config.settings import settings
from src.adapters.cache import RedisCache

cache = RedisCache() if settings.ENABLE_REDIS_CACHE else None

def get_product(product_id: str) -> Product:
    # Experimental: Cache-aside pattern
    if settings.ENABLE_REDIS_CACHE:
        cached = cache.get(f"product:{product_id}")
        if cached:
            return Product.model_validate_json(cached)

    # Cache miss or flag disabled - query database
    product = db.query(Product).filter_by(id=product_id).first()

    if settings.ENABLE_REDIS_CACHE and product:
        cache.set(
            f"product:{product_id}",
            product.model_dump_json(),
            ttl=settings.CACHE_TTL_SECONDS
        )

    return product

# tests/load/test_product_api_performance.py
import pytest
import time

def test_product_api_response_time_p95(benchmark):
    """Load test for P95 latency measurement"""
    results = []

    for _ in range(1000):
        start = time.time()
        response = client.get("/api/products/prod_123")
        results.append(time.time() - start)

    results.sort()
    p95 = results[int(len(results) * 0.95)]

    print(f"P95 latency: {p95*1000:.0f}ms")
    assert p95 < 0.2  # 200ms target
```

## Pattern 3: New Feature with Uncertain Value

**Use Case**: AI-powered suggestions, recommendation engine, new UI workflow

### Workflow

```yaml
Phase 1 - SPIKE:
  build_prototype:
    - Simplest possible version
    - Hardcoded data OK
    - No database persistence
    - No error handling
  goal: "Does this even make sense?"
  time_box: 60 min

Phase 2 - HYPOTHESIS:
  problem: "Cart abandonment rate is 35%"
  hypothesis: "Product recommendations will increase conversion"
  prediction: "Abandonment will drop to <25%"
  metrics:
    - Cart abandonment rate
    - Recommendation click-through rate
    - Revenue per session
  time_box: 8 hours (bigger feature)

Phase 3 - BUILD:
  strategy: "Progressive enhancement"
  commit_1: "Add ENABLE_RECOMMENDATIONS flag"
  commit_2: "Simple algorithm (most popular items)"
  commit_3: "Track click events"
  commit_4: "Improve algorithm based on data"
  commit_5: "Add A/B testing infrastructure"

Phase 4 - MEASURE:
  approach: "A/B test with 10% traffic"
  duration: "2 weeks"
  metrics:
    - Variant A (control): No recommendations
    - Variant B (experiment): Recommendations enabled
  track:
    - Conversion rate
    - Cart abandonment rate
    - Click-through on recommendations
    - Revenue impact

Phase 5 - DECIDE:
  success: "Statistically significant improvement → full rollout"
  iterate: "Weak signal → try different algorithm"
  kill: "No improvement or negative impact → remove feature"
```

### Example Code

```python
# settings.py
class Settings(BaseSettings):
    ENABLE_PRODUCT_RECOMMENDATIONS: bool = Field(
        default=False,
        description="Show AI-powered product recommendations"
    )
    RECOMMENDATION_AB_TEST_PERCENTAGE: int = Field(
        default=10,
        description="Percentage of users in experiment group"
    )

# api/routes/cart.py
from src.services.recommendation_service import get_recommendations
from src.config.settings import settings
import random

@router.get("/cart")
def get_cart(cart_id: str):
    cart = cart_service.get_cart(cart_id)

    # Experimental feature: recommendations
    recommendations = None
    if settings.ENABLE_PRODUCT_RECOMMENDATIONS:
        # A/B test: only show to X% of users
        if random.random() * 100 < settings.RECOMMENDATION_AB_TEST_PERCENTAGE:
            recommendations = get_recommendations(cart)
            # Track that user is in experiment group
            analytics.track("recommendation_shown", {"cart_id": cart_id})

    return {
        "cart": cart,
        "recommendations": recommendations  # null for control group
    }

# services/recommendation_service.py
def get_recommendations(cart: Cart) -> list[Product]:
    """
    Experimental recommendation algorithm.

    V1: Simple most-popular items (baseline)
    Future: Collaborative filtering, ML model
    """
    # Start with simplest algorithm that could work
    popular_products = db.query(Product)\
        .order_by(Product.purchase_count.desc())\
        .limit(3)\
        .all()

    return popular_products

# tests/test_recommendations.py
def test_recommendations_shown_when_flag_enabled_and_user_in_test_group(
    monkeypatch
):
    monkeypatch.setattr(settings, "ENABLE_PRODUCT_RECOMMENDATIONS", True)
    monkeypatch.setattr(settings, "RECOMMENDATION_AB_TEST_PERCENTAGE", 100)

    response = client.get("/cart?cart_id=cart_123")

    assert response.json()["recommendations"] is not None
    assert len(response.json()["recommendations"]) == 3

def test_recommendations_not_shown_when_flag_disabled(monkeypatch):
    monkeypatch.setattr(settings, "ENABLE_PRODUCT_RECOMMENDATIONS", False)

    response = client.get("/cart?cart_id=cart_123")

    assert response.json()["recommendations"] is None
```

## Pattern 4: Architecture Refactoring

**Use Case**: Moving from sync to async, monolith to microservices, changing data model

### Workflow

```yaml
Phase 1 - SPIKE:
  explore:
    - New architecture pattern
    - Migration path
    - Compatibility concerns
  output: "Architecture decision record (ADR)"
  time_box: 60-90 min

Phase 2 - HYPOTHESIS:
  problem: "Sync processing blocks API responses (P95 = 2s)"
  hypothesis: "Async queue will reduce API latency"
  prediction: "P95 will drop to <300ms"
  risks:
    - Eventual consistency
    - Increased complexity
    - New failure modes (queue outage)
  time_box: 12 hours (architecture changes are bigger)

Phase 3 - BUILD:
  strategy: "Strangler fig pattern"
  commit_1: "Add ENABLE_ASYNC_PROCESSING flag"
  commit_2: "Add message queue adapter"
  commit_3: "Implement async worker for ONE operation"
  commit_4: "Add monitoring for queue depth/lag"
  commit_5: "Migrate second operation"
  note: "Keep sync code until async proven stable"

Phase 4 - MEASURE:
  baseline: "Sync version metrics"
  experiment: "Async version with 20% traffic"
  duration: "2 weeks"
  metrics:
    - API response time
    - Processing completion time
    - Error rate
    - Queue metrics (depth, lag, DLQ)

Phase 5 - DECIDE:
  success: "Migrate remaining operations, remove sync code after 1 month"
  iterate: "Fix discovered issues, continue canary"
  kill: "Revert to sync, async complexity not worth latency gain"
```

### Example Code

```python
# settings.py
class Settings(BaseSettings):
    ENABLE_ASYNC_ORDER_PROCESSING: bool = Field(
        default=False,
        description="Process orders asynchronously via message queue"
    )

# api/routes/orders.py
from src.services.order_service import create_order_sync, create_order_async
from src.config.settings import settings

@router.post("/orders")
async def create_order(order_data: OrderCreate):
    if settings.ENABLE_ASYNC_ORDER_PROCESSING:
        # Experimental: Async processing
        order = await create_order_async(order_data)
        return {
            "order_id": order.id,
            "status": "processing",  # Eventual consistency
            "message": "Order is being processed"
        }
    else:
        # Current: Sync processing
        order = create_order_sync(order_data)
        return {
            "order_id": order.id,
            "status": "completed",  # Immediate consistency
            "message": "Order completed"
        }

# services/order_service.py
from src.adapters.queue import MessageQueue

queue = MessageQueue()

async def create_order_async(order_data: OrderCreate) -> Order:
    """
    Experimental async order processing.

    Trade-off: Faster API response but eventual consistency.
    """
    # Create order record immediately (fast)
    order = Order(
        id=generate_id(),
        status="pending",
        data=order_data.model_dump()
    )
    db.add(order)
    db.commit()

    # Queue processing steps (done asynchronously)
    await queue.publish("order.created", {
        "order_id": order.id,
        "steps": ["validate_payment", "reserve_inventory", "send_confirmation"]
    })

    return order

def create_order_sync(order_data: OrderCreate) -> Order:
    """Current sync order processing (simple but slow)"""
    order = Order(id=generate_id(), status="pending", data=order_data.model_dump())
    db.add(order)

    # All steps happen synchronously (slow but consistent)
    validate_payment(order)
    reserve_inventory(order)
    send_confirmation(order)

    order.status = "completed"
    db.commit()
    return order

# workers/order_processor.py
# Async worker that processes queued orders
async def process_order_message(message):
    order_id = message["order_id"]

    for step in message["steps"]:
        if step == "validate_payment":
            validate_payment(order_id)
        elif step == "reserve_inventory":
            reserve_inventory(order_id)
        elif step == "send_confirmation":
            send_confirmation(order_id)

    # Update order status when all steps complete
    order = db.query(Order).get(order_id)
    order.status = "completed"
    db.commit()
```

## Quick Decision Matrix

| Scenario | Spike? | Time Box | Measurement |
|----------|--------|----------|-------------|
| New external API | Yes (30-45 min) | 4-6 hours | Success rate, latency, cost |
| Performance optimization | Yes (profile first) | 2-4 hours | P95 latency, resource usage |
| New UI feature | Yes (prototype) | 6-8 hours | Conversion rate, click-through |
| Architecture change | Yes (ADR) | 8-12 hours | Latency, error rate, complexity |
| Algorithm change | No (small) | 2-3 hours | Accuracy, performance |
| Database schema | No (migration) | 4-6 hours | Query performance, migration time |

## Common Hypothesis Templates

### Performance
```markdown
**Current**: Operation X takes Y ms at P95
**Hypothesis**: Optimization Z will reduce time
**Prediction**: P95 will drop to <N ms
**Success**: P95 <= N ms AND no regression in error rate
```

### Reliability
```markdown
**Current**: Feature has Y% failure rate
**Hypothesis**: Change Z will reduce failures
**Prediction**: Failure rate will drop to <X%
**Success**: Failure rate <= X% for 1 week
```

### User Behavior
```markdown
**Current**: Conversion rate is Y%
**Hypothesis**: Feature Z will increase conversion
**Prediction**: Conversion will increase to >X%
**Success**: Statistically significant increase (p < 0.05) over 2 weeks
```

### Cost Optimization
```markdown
**Current**: Service costs $Y/month
**Hypothesis**: Optimization Z will reduce cost
**Prediction**: Cost will drop to <$X/month
**Success**: Cost <= $X/month with no quality degradation
```

---

**Key Principle**: Every pattern follows the same 5-phase workflow. Only the time boxes and metrics differ.
