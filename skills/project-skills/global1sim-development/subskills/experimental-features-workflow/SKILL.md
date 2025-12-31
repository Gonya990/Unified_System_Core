---
name: experimental-features-workflow
description: Minimum code, fast iterations workflow for experimental features - combines spike exploration, feature flags, and hypothesis-driven development; use when building features with high uncertainty or trying new approaches.
---

# Experimental Features Workflow

**For**: Building experimental features with minimum code, no overengineering, and fast iterations.

**Goal**: Learn fast, fail fast, ship incrementally.

## 🎯 Quick Start Decision Tree

```yaml
starting_experimental_feature:
  question: "What do I know about this feature?"

  nothing_yet:
    answer: "I don't know if this approach will work"
    action: Phase 1 - SPIKE (30-60 min exploration)

  basic_idea:
    answer: "I have a hypothesis but need to validate"
    action: Phase 2 - HYPOTHESIS (define success criteria)

  ready_to_code:
    answer: "I know what to build, just need to iterate"
    action: Phase 3 - BUILD (TDD with feature flag)

  needs_measurement:
    answer: "Feature is built, does it work?"
    action: Phase 4 - MEASURE (validate hypothesis)

  decision_time:
    answer: "Results are in"
    action: Phase 5 - DECIDE (keep, iterate, or kill)
```

## 🔄 The 5-Phase Workflow

### Phase 1: SPIKE (Exploration)

**When**: You don't know enough to write a good hypothesis
**Time Box**: 30-60 minutes MAX
**Goal**: Learn enough to form hypothesis

```bash
# Create spike branch (will be deleted!)
git checkout -b spike/feature-name

# Hack freely - NO tests, NO quality, just LEARN
# Try the simplest possible approach
# Print things, hardcode values, skip error handling

# Document what you learned
```

**Example Spike Session**:
```python
# spike_payment_gateway.py - DELETE AFTER LEARNING
def quick_test():
    """Just exploring the payment API"""
    api = PaymentGateway(key="test_key")

    # Can we charge a card?
    result = api.charge(amount=1000, currency="USD")
    print(f"Result: {result}")  # What does response look like?

    # How long does it take?
    import time
    start = time.time()
    api.charge(amount=100, currency="USD")
    print(f"Time: {time.time() - start}s")

    # What errors happen?
    try:
        api.charge(amount=-100, currency="INVALID")
    except Exception as e:
        print(f"Error type: {type(e)}, message: {e}")

# Run it
quick_test()
```

**Document Learnings**:
```markdown
## Spike Results: Payment Gateway Integration

**Duration**: 45 minutes

**Learned**:
- API uses async webhooks (not synchronous responses)
- Average response time: 150ms
- Errors return 400 with JSON: {"error": "message"}
- Test mode requires different endpoint URL
- Has official Python SDK (simpler than raw HTTP)

**Recommendation**:
- Use official SDK (handles auth, retries)
- Implement webhook handler for async responses
- Mock SDK in tests (not HTTP calls)
- Store payment intent ID, not final status

**Next Step**: Write hypothesis for Phase 2
```

**Delete Spike Code**:
```bash
git checkout main  # Back to trunk
# DO NOT MERGE spike branch - just use learnings
```

### Phase 2: HYPOTHESIS (Define Success)

**When**: After spike or when you have basic understanding
**Time Box**: 15-30 minutes
**Goal**: Write down what success looks like BEFORE coding

```markdown
## Experiment: [Feature Name]

**Problem**:
Current order processing doesn't support payment retry logic.
Result: 5% of valid payments fail permanently.

**Hypothesis**:
Adding retry logic with exponential backoff will reduce permanent
failures from 5% to <1%.

**Prediction**:
- Success rate will increase from 95% to 99%+
- P95 latency will stay under 300ms (retries are async)
- No new errors introduced in happy path

**Success Criteria** (measurable):
- [ ] Payment success rate >= 99% in load test
- [ ] P95 latency <= 300ms
- [ ] Zero errors in happy path test suite
- [ ] Retry logic activates on 4xx errors only

**Time Box**: 4 hours total (2 hours build, 2 hours test)

**Rollback Plan**:
Feature flag ENABLE_PAYMENT_RETRY=false (default off)

**How to Measure**:
```bash
# Baseline (before)
uv run pytest tests/load/test_payment_success_rate.py -v

# With feature (after)
ENABLE_PAYMENT_RETRY=true uv run pytest tests/load/test_payment_success_rate.py -v

# Compare: success_rate, p95_latency, error_count
```
```

**Key Points**:
- ✅ Specific numbers (not "better performance")
- ✅ Time boxed (prevents overengineering)
- ✅ Measurable before/after
- ✅ Rollback plan (safe to ship)

### Phase 3: BUILD (Minimum Viable Implementation)

**When**: Hypothesis is written
**Approach**: TDD + Feature Flag + Smallest Possible Code
**Target**: Commit 3+ times during this phase

#### Step 1: Add Feature Flag

```python
# src/config/settings.py
class Settings(BaseSettings):
    # ... existing settings ...

    # Experimental: Payment retry logic (2024-11-16)
    ENABLE_PAYMENT_RETRY: bool = Field(
        default=False,
        description="Enable exponential backoff retry for payment failures"
    )

settings = Settings()
```

```bash
# .env.development
ENABLE_PAYMENT_RETRY=true  # On for development

# .env.production (default)
# ENABLE_PAYMENT_RETRY=false  # Off for production until validated
```

**Commit 1**:
```bash
git add src/config/settings.py
git commit -m "feat: add ENABLE_PAYMENT_RETRY feature flag

Experimental feature for payment retry logic.
Default: false (disabled in production)

Part of experiment: reduce payment failures 5% -> 1%"
git push origin main
```

#### Step 2: TDD the Happy Path (Minimum Code)

```python
# tests/test_payment_retry.py
import pytest
from src.services.payment_service import process_payment
from src.config.settings import settings

def test_payment_succeeds_without_retry_when_gateway_responds():
    """Baseline: Normal payment works"""
    result = process_payment(amount=100, customer_id="cust_123")

    assert result.success is True
    assert result.retry_count == 0

def test_payment_retries_on_transient_error_when_flag_enabled(
    monkeypatch, mock_payment_gateway
):
    """Experimental: Retry on 429 rate limit error"""
    monkeypatch.setattr(settings, "ENABLE_PAYMENT_RETRY", True)

    # Fail first attempt, succeed second
    mock_payment_gateway.set_responses([
        {"status": 429, "error": "Rate limited"},
        {"status": 200, "success": True}
    ])

    result = process_payment(amount=100, customer_id="cust_123")

    assert result.success is True
    assert result.retry_count == 1
```

**RED**: Run test, watch it fail
```bash
uv run pytest tests/test_payment_retry.py::test_payment_retries_on_transient_error_when_flag_enabled -v
# FAILS: AttributeError (retry logic doesn't exist)
```

**GREEN**: Minimum code to pass
```python
# src/services/payment_service.py
from src.config.settings import settings
from dataclasses import dataclass

@dataclass
class PaymentResult:
    success: bool
    retry_count: int = 0

def process_payment(amount: int, customer_id: str) -> PaymentResult:
    gateway = PaymentGateway()

    # Feature flag check
    if settings.ENABLE_PAYMENT_RETRY:
        # Experimental retry logic
        for attempt in range(2):  # Try twice max (MINIMUM viable)
            result = gateway.charge(amount, customer_id)
            if result.success:
                return PaymentResult(success=True, retry_count=attempt)
        return PaymentResult(success=False, retry_count=2)
    else:
        # Original behavior (no retry)
        result = gateway.charge(amount, customer_id)
        return PaymentResult(success=result.success, retry_count=0)
```

**GREEN**: Test passes
```bash
uv run pytest tests/test_payment_retry.py -v
# PASSES
```

**Commit 2**:
```bash
git add tests/test_payment_retry.py src/services/payment_service.py
git commit -m "feat: add basic payment retry logic (experimental)

- Retry once on failure when ENABLE_PAYMENT_RETRY=true
- Track retry_count in result
- Original behavior unchanged when flag=false

Next: Add exponential backoff, better error handling"
git push origin main
```

#### Step 3: Iterate in Tiny Steps

**REFACTOR**: Add exponential backoff (one small improvement at a time)

```python
# Test first
def test_payment_retry_uses_exponential_backoff(monkeypatch):
    monkeypatch.setattr(settings, "ENABLE_PAYMENT_RETRY", True)

    delays = []
    original_sleep = time.sleep
    def mock_sleep(seconds):
        delays.append(seconds)

    monkeypatch.setattr(time, "sleep", mock_sleep)

    # Make it fail twice, succeed third time
    # ...

    assert delays == [1, 2]  # 1s, then 2s (exponential)
```

**Commit 3** (after implementing backoff), **Commit 4** (after adding error handling), etc.

**Key Point**: Each commit is atomic and tested. Feature is behind flag, safe to deploy even incomplete.

### Phase 4: MEASURE (Validate Hypothesis)

**When**: Minimum viable implementation is complete
**Goal**: Get real data on whether hypothesis is correct

```bash
# Run the measurement defined in Phase 2

# Baseline (flag off)
ENABLE_PAYMENT_RETRY=false uv run pytest tests/load/test_payment_success_rate.py -v
# Output: success_rate=95.2%, p95_latency=120ms, errors=0

# Experimental (flag on)
ENABLE_PAYMENT_RETRY=true uv run pytest tests/load/test_payment_success_rate.py -v
# Output: success_rate=98.8%, p95_latency=280ms, errors=0
```

**Document Results**:
```markdown
## Experiment Results: Payment Retry Logic

**Date**: 2024-11-16
**Duration**: 3.5 hours (under 4-hour time box ✓)

**Hypothesis**: Retry logic will reduce failures from 5% to <1%

**Results**:
| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Success rate | >= 99% | 98.8% | ⚠️ Close but not quite |
| P95 latency | <= 300ms | 280ms | ✅ Pass |
| Happy path errors | 0 | 0 | ✅ Pass |
| Retry activation | 4xx only | 4xx only | ✅ Pass |

**Learning**:
- Retry logic helps (95% -> 98.8%) but doesn't hit target
- Most failures are 5xx (not retryable), not 4xx
- Latency impact acceptable
- No regressions in happy path

**Next Hypothesis**:
Need to add circuit breaker for 5xx errors (partner outage),
not just retry logic.
```

### Phase 5: DECIDE (Keep, Iterate, or Kill)

**Based on data** (not feelings), choose one:

#### Option A: SUCCESS - Ship It

**When**: Hypothesis validated, targets met

```bash
# Enable in production
# .env.production
ENABLE_PAYMENT_RETRY=true

# Deploy
git tag -a v1.2.0 -m "Enable payment retry logic (reduces failures to 0.8%)"
git push origin v1.2.0

# After 1 week of production monitoring with no issues:
# Remove feature flag (it's now the default behavior)
```

**Remove flag after stability**:
```python
# Clean up after 1-2 weeks
def process_payment(amount: int, customer_id: str) -> PaymentResult:
    # Feature flag removed - retry is now standard behavior
    # (Previously: ENABLE_PAYMENT_RETRY experiment from 2024-11-16)
    for attempt in range(3):
        result = gateway.charge(amount, customer_id)
        if result.success:
            return PaymentResult(success=True, retry_count=attempt)
        time.sleep(2 ** attempt)  # Exponential backoff
    return PaymentResult(success=False, retry_count=3)
```

#### Option B: ITERATE - Another Experiment

**When**: Partial success, learned something valuable

```markdown
## Experiment #2: Circuit Breaker for 5xx Errors

**Previous Learning**: Retry helped 4xx (95% -> 98.8%) but most
failures are 5xx (partner outages)

**New Hypothesis**: Circuit breaker will prevent cascade failures
during partner outages, reducing customer-facing errors from 1.2% to <0.5%

**Time Box**: 3 hours
**Rollback**: ENABLE_CIRCUIT_BREAKER=false
```

**Keep existing retry logic** (flag on), add new circuit breaker experiment.

#### Option C: KILL - Delete the Code

**When**: Hypothesis disproven, no value gained

```markdown
## Experiment Failed: Payment Retry Logic

**Results**:
- Success rate: 95.1% (no improvement from baseline 95%)
- P95 latency: 450ms (WORSE than target 300ms)
- Added complexity with no benefit

**Decision**: Revert all changes

**Learning**:
- Problem is not transient failures (4xx)
- Problem is partner gateway uptime (5xx)
- Better solution: Switch to more reliable payment partner
```

```bash
# Remove feature flag
git rm src/config/settings.py  # Remove ENABLE_PAYMENT_RETRY

# Remove implementation
# (Revert all commits or delete code)

git commit -m "revert: remove payment retry experiment

Experiment results showed no improvement in success rate
and increased latency. Root cause is partner reliability,
not transient errors.

Next: Evaluate alternative payment partners"
git push origin main
```

## 📋 Complete Checklist

Use this for every experimental feature:

### Phase 1: SPIKE (if needed)
- [ ] Create spike branch
- [ ] Set 30-60 min timer
- [ ] Hack freely (no quality requirements)
- [ ] Document learnings in markdown
- [ ] Delete spike code (back to main, don't merge)

### Phase 2: HYPOTHESIS
- [ ] Define current problem with metrics
- [ ] Write hypothesis (what you believe)
- [ ] Write prediction (specific measurable outcome)
- [ ] Define success criteria (numbers, not feelings)
- [ ] Set time box (2-8 hours typical)
- [ ] Write rollback plan (feature flag)
- [ ] Define measurement method (before/after commands)

### Phase 3: BUILD
- [ ] Add feature flag to settings (default=false)
- [ ] Commit flag (Commit 1)
- [ ] Write failing test for minimum viable behavior
- [ ] Write minimum code to pass (no edge cases yet)
- [ ] Commit working test + code (Commit 2)
- [ ] Iterate in tiny steps (1 improvement per commit)
- [ ] Each commit: run tests, all pass, push to main
- [ ] Target: 3-5 commits for this phase

### Phase 4: MEASURE
- [ ] Run baseline measurement (flag off)
- [ ] Run experimental measurement (flag on)
- [ ] Record actual results in table
- [ ] Compare to success criteria
- [ ] Document learnings (even if "failed")

### Phase 5: DECIDE
- [ ] Based on data, choose: SUCCESS / ITERATE / KILL
- [ ] If SUCCESS: Enable in prod, monitor, remove flag after stability
- [ ] If ITERATE: Keep code, write new hypothesis, repeat
- [ ] If KILL: Delete code, document learning, try different approach

## 🚫 Anti-Patterns

### ❌ "Let me build the whole thing perfectly first"
**Problem**: Overengineering, no feedback
**Fix**: Build MINIMUM viable, measure, then decide

**Example**:
```python
# ❌ DON'T: Build entire retry system upfront
class RetryStrategy(ABC):
    @abstractmethod
    def should_retry(self, error): pass

class ExponentialBackoff(RetryStrategy):
    def __init__(self, max_retries, base_delay, max_delay, jitter):
        # 200 lines of configurable retry logic

# ✅ DO: Simplest thing that could work
if settings.ENABLE_PAYMENT_RETRY:
    for attempt in range(2):
        result = gateway.charge(amount, customer_id)
        if result.success:
            return result
        time.sleep(1)  # Fixed 1s delay - SIMPLEST
```

### ❌ "No time box, I'll finish when it's done"
**Problem**: Scope creep, sunk cost fallacy
**Fix**: Set time box in Phase 2, stick to it

### ❌ "Spike code is pretty good, let me just clean it up"
**Problem**: Technical debt from exploratory code
**Fix**: Always delete spike code, reimplement with TDD

### ❌ "Feature flag is annoying, I'll remove it immediately"
**Problem**: No rollback capability
**Fix**: Keep flag for 1-2 weeks in production, then remove

### ❌ "Tests are slow, I'll skip them for this experiment"
**Problem**: Can't measure reliably, can't refactor safely
**Fix**: Fast tests are requirement (see `feedback-driven-design`)

### ❌ "Results are close enough to target"
**Problem**: Confirmation bias, no rigorous standards
**Fix**: Hit targets or mark as ITERATE/KILL

## 🎯 Integration with Other Skills

### Required Skills
- `iterative-development`: Small batches, RED-GREEN-REFACTOR
- `experimental-workflow`: Scientific method, hypothesis formation
- `continuous-integration-practice`: Feature flags, trunk-based dev

### Complementary Skills
- `feedback-driven-design`: Fast tests for measurement
- `separation-of-concerns-enforcer`: Keep feature flag logic isolated
- `empirical-measurement`: Track DORA metrics for experiments

## 📊 Success Metrics

Track these for experimental feature workflow:

- **Spike efficiency**: Learning per minute (insights / time spent)
- **Hypothesis quality**: Clear success criteria (yes/no)
- **Time box adherence**: Actual time / planned time (<= 1.2x)
- **Commit frequency**: 3+ commits during BUILD phase
- **Decision speed**: Time from MEASURE to DECIDE (< 1 day)
- **Rollback capability**: Can disable in < 5 minutes (feature flag)

## 💡 Real Example Template

```markdown
## Experiment: AI-Powered Order Suggestions

### Phase 1: SPIKE (45 min)
**Learned**: OpenAI API averages 800ms response time, costs $0.002/request

### Phase 2: HYPOTHESIS
**Problem**: Cart abandonment rate is 35%
**Hypothesis**: AI suggestions will reduce abandonment to <25%
**Time Box**: 6 hours
**Success**: Abandonment rate <= 25%, P95 latency <= 1s
**Rollback**: ENABLE_AI_SUGGESTIONS=false

### Phase 3: BUILD (4 hours)
- Commit 1: Add feature flag
- Commit 2: Basic AI integration (hardcoded prompt)
- Commit 3: Add caching layer
- Commit 4: Error handling for API failures

### Phase 4: MEASURE (1 hour)
**Results**:
- Abandonment: 32% (not at target)
- P95 latency: 950ms (within target)
- Cost: $0.15/day (acceptable)

### Phase 5: DECIDE
**Decision**: ITERATE
**Next**: Experiment #2 - A/B test different prompt templates
(Current prompt too generic, need personalization)
```

## 🔧 Tools and Commands

```bash
# Create spike (exploration phase)
git checkout -b spike/feature-name

# Back to trunk (delete spike)
git checkout main

# Enable experimental feature locally
echo "ENABLE_FEATURE_NAME=true" >> .env

# Measure baseline
ENABLE_FEATURE_NAME=false uv run pytest tests/load/test_metric.py -v

# Measure experiment
ENABLE_FEATURE_NAME=true uv run pytest tests/load/test_metric.py -v

# Fast feedback during BUILD phase
uv run pytest tests/test_feature.py -v  # After each tiny change
```

---

**Remember**: The goal is learning, not perfection. Ship experiments behind flags, measure results, make data-driven decisions.

**Core principle**: Minimum code + fast iterations + real measurements = better decisions than upfront design.
