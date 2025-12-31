---
name: experimental-workflow
description: Applies scientific method to software development - treating all work as experiments with hypotheses, measurements, and controlled variables; use when exploring unknowns or validating design decisions.
---

# Experimental Workflow

Activate this skill when facing uncertainty, exploring new approaches, or validating assumptions. Treat software development as applied science.

## Core Principle

**"When we organize our thinking this way and start to make progress on the basis of many small informal experiments, we begin to limit our risk of jumping to inappropriate conclusions and so end up doing a better job."**

## The Scientific Method for Code

### Standard Scientific Method (from book):
1. **Characterize**: Make an observation of the current state
2. **Hypothesize**: Create a description, a theory that may explain your observation
3. **Predict**: Make a prediction based on your hypothesis
4. **Experiment**: Test your prediction

### Applied to Software Development:

```
1. CHARACTERIZE: "Order creation takes 2 seconds"
2. HYPOTHESIZE: "Database queries are slow because we're missing an index"
3. PREDICT: "Adding index on customer_id will reduce time to <500ms"
4. EXPERIMENT: Add index, measure actual time

Result: Either prediction confirmed (keep index) or rejected (try different hypothesis)
```

## Toyota Kata Applied to Code

**From Mike Rother's work, referenced in the book:**

### The Improvement Kata

1. **Understand the current condition**
   - Measure it objectively
   - No assumptions, only data

2. **Define the target condition**
   - Where do we want to be?
   - Must be measurable

3. **Experiment toward the target**
   - Take ONE small step
   - Define success criteria BEFORE step

4. **Check and adjust**
   - Did it move us toward target?
   - What did we learn?

5. **Repeat**

**Quote**: "This is a simple, light-weight application of the scientific method. This should be obvious. This should be 'motherhood and apple pie,' but it is not what most people in most organizations do."

## Practical Experimental Workflow

### Before Writing Any Code

```markdown
## Experiment: [Name]

**Current State**: 
- What: Order processing system
- Metric: 100 orders/hour max throughput
- Problem: Cannot scale to meet demand

**Hypothesis**:
Synchronous payment processing is the bottleneck

**Prediction**:
If we move payment processing to async queue, throughput will increase to 500+ orders/hour

**Success Criteria**:
- [ ] Orders/hour >= 500 in load test
- [ ] Payment success rate remains >= 99.9%
- [ ] P95 latency <= 200ms

**How to Measure**:
```bash
# Before
uv run pytest tests/load/test_order_throughput.py --workers=10

# After  
uv run pytest tests/load/test_order_throughput.py --workers=10

# Compare metrics from test output
```

**Time Box**: 4 hours (2 hours implementation, 2 hours measurement)

**Rollback Plan**: Feature flag ENABLE_ASYNC_PAYMENTS=false
```

### During the Experiment

- [ ] **Control the variables** - Change ONE thing only
- [ ] **Run baseline measurement** - Know current state objectively
- [ ] **Make the change** - As small as possible
- [ ] **Run measurement again** - Same conditions as baseline
- [ ] **Compare results** - Better, worse, or no change?

### After the Experiment

- [ ] **Record results** - Even if experiment "failed"
  ```markdown
  ## Results:
  - Throughput: 450 orders/hour (90% improvement but below target)
  - Success rate: 99.95% (within spec)
  - P95 latency: 180ms (better than target)
  
  ## Learning:
  - Async processing helps but not enough alone
  - Next hypothesis: Connection pool size is now bottleneck
  ```

- [ ] **Keep or revert** based on data, not feelings

- [ ] **Document in code** if keeping
  ```python
  # Experiment 2024-11-08: Async payment processing
  # Result: 90% throughput improvement (100->450 orders/hour)
  # Trade-off: Eventual consistency for payment status
  # Monitoring: payment_queue_depth, payment_processing_lag
  ```

## TDD as Experimental Process

**Key Insight**: Automated testing IS experimenting

### Test as Experiment

```python
def test_order_total_includes_tax():  # <- HYPOTHESIS
    """
    EXPERIMENT: Does order total calculation include tax?
    
    PREDICTION: 
    Order with $100 subtotal + 10% tax = $110 total
    """
    # SETUP CONTROLLED CONDITIONS
    order = Order(items=[Item(price=Decimal("100"))])
    tax_rate = Decimal("0.10")
    
    # RUN EXPERIMENT
    total = calculate_order_total(order, tax_rate)
    
    # MEASURE RESULT
    assert total == Decimal("110")  # <- MEASUREMENT
```

### Test Failure = Experiment Result

When test fails, you learned something:
- Maybe implementation is wrong (fix code)
- Maybe hypothesis is wrong (fix test)
- Maybe both are wrong (rethink approach)

**This is science, not failure!**

## Controlling the Variables

**From the book**: "If we start to think in terms of controlling the variables in our experiments so that we can achieve more consistency and reliability in our results, this leads us in the direction of more deterministic systems and code."

### In Tests

```python
# ❌ UNCONTROLLED VARIABLES - Unpredictable
def test_order_creation():
    order = create_order()  # Uses current timestamp
    time.sleep(1)  # Timing-dependent!
    assert order.status == "confirmed"  # Depends on external API

# ✅ CONTROLLED VARIABLES - Deterministic
def test_order_creation(fake_clock, fake_payment_gateway):
    fake_clock.set("2024-11-08T10:00:00Z")  # Control time
    fake_payment_gateway.will_succeed()  # Control API
    
    order = create_order()
    
    assert order.created_at == "2024-11-08T10:00:00Z"
    assert order.status == "confirmed"
```

### In Code

```python
# ❌ HARD TO CONTROL
def calculate_shipping():
    rate = requests.get("https://shipping-api.com/rates")  # External!
    return rate.json()["amount"]

# ✅ EASY TO CONTROL  
def calculate_shipping(rate_provider: ShippingRateProvider):
    rate = rate_provider.get_rate()  # Injected dependency
    return rate.amount
```

## Spike: Time-Boxed Exploration

When you don't know enough to write a good hypothesis:

### Spike Protocol

1. **Create spike branch**
   ```bash
   git checkout -b spike/payment-gateway-integration
   ```

2. **Set strict time box** (30-60 minutes max)

3. **Hack freely** - No tests, no quality, just learn
   ```python
   # spike code - DELETE AFTER
   def quick_test():
       api = PaymentAPI(key="test")
       result = api.charge(amount=100)
       print(result)  # Just exploring the API
   ```

4. **Document learnings**
   ```markdown
   ## Spike Results: Payment Gateway Integration
   
   **Learned**:
   - API uses OAuth2 (not API keys)
   - Charges are async (webhook for completion)
   - Test mode requires different endpoint
   
   **Recommendation**:
   - Use official Python SDK (handles OAuth)
   - Implement webhook handler
   - Mock SDK in tests (not HTTP)
   ```

5. **Delete spike code** - Do NOT merge!
   ```bash
   git checkout feature/payment-integration
   # Now implement properly with TDD based on learnings
   ```

## SpaceX Principle: Test Real Things

**From the book - SpaceX Starship example**:

Even when switching from 4mm to 3mm steel:
- Had all mathematical models
- Had tensile strength data
- Had computer simulations

**Still** built physical prototypes and tested to destruction.

**Why?** "These models will certainly be wrong in some maybe esoteric, difficult-to-predict way."

### Our Application

```python
# ❌ MATH SAYS IT WORKS
# "Database can handle 10,000 queries/sec theoretical max"
# (Don't ship based on math alone)

# ✅ EXPERIMENT PROVES IT WORKS
def test_database_handles_peak_load():
    """
    Load test with 10,000 actual queries/sec for 5 minutes
    Measure: query latency, error rate, connection pool exhaustion
    """
    pass
```

## Falsification Over Confirmation

**From Karl Popper (referenced in book)**: Try to DISPROVE your hypothesis, not confirm it.

### Confirmation Bias Example

```python
# ❌ ONLY TESTING HAPPY PATH
def test_order_creation_succeeds():
    order = create_order(valid_data)
    assert order.id is not None

# ✅ TRYING TO BREAK IT
def test_order_creation_with_missing_customer():
    with pytest.raises(ValidationError):
        create_order(data_without_customer)

def test_order_creation_with_negative_amount():
    with pytest.raises(ValueError):
        create_order(data_with_negative_amount)

def test_order_creation_with_duplicate_id():
    create_order(data)
    with pytest.raises(DuplicateError):
        create_order(same_data)
```

**Margaret Hamilton's Approach** (first software engineer, Apollo program):

**Quote**: "There was a fascination on my part with errors, a never ending pass-time of mine was what made a particular error, or class of errors, happen and how to prevent it in the future."

## Experiment Templates

### Performance Experiment

```markdown
## Experiment: Cache Product Catalog

**Current**: 150ms average API response time
**Hypothesis**: Database queries for product data are slow
**Prediction**: Adding Redis cache will reduce to <50ms
**Variables to Control**:
- Same test data
- Same hardware
- Same concurrent users (100)

**Measurement**:
```bash
# Baseline
uv run pytest tests/performance/test_api_latency.py
# Record P50, P95, P99

# With cache
ENABLE_REDIS_CACHE=true uv run pytest tests/performance/test_api_latency.py
# Record P50, P95, P99

# Compare
```

**Success**: P95 < 50ms AND P99 < 100ms
**Failure Threshold**: No improvement OR P95 > 200ms (worse)
```

### Architecture Experiment

```markdown
## Experiment: Event-Driven Order Processing

**Current**: Monolithic order service (2000 LOC, hard to test)
**Hypothesis**: Event-driven architecture will improve testability
**Prediction**: Cycle time for features will decrease from 3 days to 1 day

**How to Measure**:
- Track feature cycle time (JIRA closed - created) for next 4 features
- Compare to last 4 features before change

**Rollout**: Canary with 10% of orders for 1 week
**Rollback**: Feature flag within 5 minutes if error rate >1%
```

## Anti-Patterns

❌ **"I think this will work" (no measurement)**
- Implement based on intuition
- **Fix**: Define measurement before implementing

❌ **"It works on my machine" (uncontrolled variables)**
- Can't reproduce in CI
- **Fix**: Control environment variables, use containers

❌ **"We'll test it later" (no experimental mindset)**
- Build entire feature before validating
- **Fix**: Smallest possible experiment first

❌ **"Coverage is 100%" (confirmation bias)**
- Only tested happy paths
- **Fix**: Write tests that try to BREAK code

## Integration with Other Skills

- **Requires**: `feedback-driven-design` (experiments need measurement)
- **Enables**: `empirical-measurement` (experiments generate data)
- **Pairs with**: `iterative-development` (each iteration is experiment)
- **Validates**: `separation-of-concerns-enforcer` (experiments test modularity)

## Success Metrics

- **Hypothesis → Result time**: <4 hours for typical experiment
- **Experiment success rate**: 30-50% (if higher, not taking enough risks)
- **Documented learnings**: 100% (even "failures" teach us)
- **Rollback capability**: <5 minutes for any experiment

## Related References

See [reference/principles.md](reference/principles.md) for scientific method details.
See [reference/workflow.md](reference/workflow.md) for experiment templates and checklists.
See [examples/](examples/) for real experiments with results.
