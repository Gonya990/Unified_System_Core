---
name: feedback-driven-design
description: Optimizes feedback speed and quality at all development levels based on Dave Farley's Modern Software Engineering; use when designing systems, choosing architectures, or diagnosing slow development cycles.
---

# Feedback-Driven Design

Activate this skill when you need to optimize for fast, high-quality feedback loops. Without feedback, there is no learning. Without fast feedback, learning is too slow to be useful.

## Core Principle

**"Without feedback, there is no opportunity to learn. We can only guess, rather than make decisions based on reality."**

The speed AND quality of feedback both matter. Late feedback is useless. Wrong feedback leads to wrong decisions.

## The Broom Balancing Mental Model

**From the book** - Two approaches to balancing a broom:

### Approach 1: Predictive (Waterfall)
"Carefully analyze the structure of the broom, work out its center of gravity, closely examine the structure of the handle, and calculate exactly the point at which the broom will be perfectly balanced."

**Result**: "Incredibly unlikely that it will [work]. The result is extremely unstable. It relies on our predictions being perfect."

### Approach 2: Feedback-Driven (Agile)
"Put the broom on our hand and move our hand in response to how it tipped!"

**Result**: "This is how space rockets 'balance' on the thrust of their engines...profoundly more effective and more stable in terms of outcome."

**Key Quote**: "The second approach, although it may seem more ad hoc, more like 'winging it,' is actually profoundly more effective."

## The Feedback Hierarchy (Prefer Early Feedback)

Organize your work to fail at the EARLIEST possible stage:

### Level 1: IDE (Instant - Milliseconds)
- **Type errors** detected as you type
- **Syntax errors** highlighted immediately
- **Import errors** shown in real-time
- **Action**: Configure IDE for maximum error detection

```python
# Type hints give instant feedback:
def calculate_total(items: list[Item]) -> Decimal:  # IDE shows errors immediately
    return sum(item.price for item in items)
```

### Level 2: Unit Tests (Seconds)
- **Business logic** validated in isolation
- **Edge cases** caught before integration
- **Design feedback** - hard to test = poor design
- **Target**: <100ms per test, <1 second for full unit suite

```bash
# Fast feedback loop during development:
uv run pytest tests/unit/test_order_service.py -v
# Should complete in <1 second
```

### Level 3: Commit Tests / CI (Minutes)
- **Integration** with others' code validated
- **All unit tests** run together
- **Code quality** checks (ruff, mypy)
- **Target**: <10 minutes from commit to green

```bash
# Triggered automatically on commit:
git push origin feature/branch
# CI runs full suite, gives feedback in <10 min
```

### Level 4: Acceptance Tests (Minutes)
- **Feature behavior** validated end-to-end
- **API contracts** verified
- **User journeys** tested
- **Target**: <30 minutes for full acceptance suite

### Level 5: Production Monitoring (Hours/Days)
- **Real user behavior** measured
- **Business metrics** tracked
- **System health** monitored
- **Target**: Telemetry streaming, dashboards updated hourly

**Critical Principle**: "Prefer to identify defects first in compile-ability (IDE) then in unit tests and, only after those validations have succeeded, in other forms of higher-level tests so we can fail soonest."

## TDD as Design Feedback Tool

**Key Insight**: "If my tests are hard to write, that tells me something important about the quality of my code."

### The Properties TDD Reveals

When tests are hard to write, your code lacks:
- Modularity
- Separation of concerns
- High cohesion
- Information hiding (abstraction)
- Appropriate coupling

**Quote**: "TDD applies a pressure to create code that is objectively 'higher quality.' This is irrespective of the talent or experience of the software developer."

### Listening to Test Pain

```python
# ❌ Hard to test = poor design signal
class OrderService:
    def __init__(self):
        self.db = psycopg2.connect("postgresql://...")  # Hardcoded!
        self.payment_api = PaymentGateway(api_key="...")  # Hardcoded!
    
    def create_order(self, data):
        # To test this, you need real database + real payment API
        # Test is slow, brittle, requires network
        # FEEDBACK: Design is poor
        pass

# ✅ Easy to test = good design
class OrderService:
    def __init__(
        self,
        repository: OrderRepository,  # Injected
        payment_gateway: PaymentGateway  # Injected
    ):
        self.repository = repository
        self.payment_gateway = payment_gateway
    
    def create_order(self, data: OrderData) -> Order:
        # Test with fakes - fast, deterministic, no network
        # FEEDBACK: Design is good
        pass
```

**Critical Point**: "It doesn't make bad software developers great, but it does make 'bad software developers' better and 'great software developers' greater."

## Architecture-Level Feedback

### The Deployment Pipeline as Feedback

**Definition**: "A deployment pipeline is not simply a little workflow of build or test steps; it is a mechanized route from commit to production."

**Critical Requirement**: "If the pipeline says everything is good, there should be no more work to do to make you comfortable to release—nothing…no more integration checks, sign-offs, or staging tests."

### The One-Hour Rule

**From the book**: "I advise the companies that I work with to aim for creating 'releasable software' at least once per hour."

**Implication**: "If any single test takes longer than an hour to run or if your software takes longer than an hour to deploy, it won't be possible to run your tests this quickly, however much money you spend on hardware."

**Result**: This constraint FORCES better architecture:
- Tests must be parallelizable
- Deployment must be automated
- System must be modular enough to test parts independently
- **This is a feature, not a bug** - Feedback constraints improve design

### Two Architectural Strategies

**From the book - No middle ground exists**:

**Option 1: Monolith**
- Build, test, and deploy EVERYTHING together
- Simpler architecture, fewer distributed system problems
- MUST optimize for speed (fast tests, fast builds, fast deploys)
- **Challenge**: Keeping feedback fast as system grows

**Option 2: Microservices**  
- Build, test, deploy each service INDEPENDENTLY
- More complex architecture, distributed system challenges
- Each piece is smaller, feedback naturally faster
- **Critical**: If testing services together, they're not microservices!

**Quote**: "Nearly everyone would like some ideal middle ground between these two extremes, but in reality, it doesn't exist. The middle ground is a fudge and is often slower and more complex than the monolithic approach."

## Feedback in Product Design

### Telemetry and Measurement

**Quote**: "Adding telemetry to our systems that allows us to gather data about which features of our systems are used, and how they are used, is now the norm."

**Application**: Instrument code to measure:
- Feature usage rates
- User journey completion
- Error frequencies
- Performance bottlenecks

```python
# Add observability for feedback:
from src.monitoring import track_event

def create_order(order_data: OrderData) -> Order:
    track_event("order.creation.started", {"customer_id": order_data.customer_id})
    
    order = self.repository.save(order_data)
    
    track_event("order.creation.completed", {
        "order_id": order.id,
        "duration_ms": timer.elapsed()
    })
    
    return order
```

## Continuous Integration as Feedback

### True CI Definition

**From the book**: "Merging all developers' working copies to a shared mainline several times a day."

**Why CI Matters**: 
- Frequent drips of feedback throughout the day
- Powerful insight into code state and system behavior
- Catches integration problems EARLY (when cheap to fix)

### CI vs Feature Branching

**Critical Insight**: "Continuous integration and feature branching are not really compatible with each other. One aims to expose change as early as possible; the other works to defer that exposure."

**The Merge Tool Trap**: 
> "It is always possible to write code that merge tools will miss; merging code is not necessarily the same as merging behavior."

**Example**: Two developers independently add "increment by one" to different parts of same function. Merge succeeds, but value is now incremented by TWO instead of one.

**Cost**: "For CI to work, we have to commit our changes frequently enough to gain that feedback...This means working very differently."

## Measuring Feedback Quality

### Speed Targets

| Feedback Level | Target Speed | Action if Slower |
|---------------|--------------|------------------|
| IDE errors | <100ms | Configure better IDE/linters |
| Single unit test | <100ms | Refactor for testability |
| Unit test suite | <10s | Parallelize or reduce I/O |
| Commit tests (CI) | <10min | Parallelize, optimize builds |
| Acceptance suite | <30min | Run in parallel, reduce scope |
| Deployment | <10min | Automate, containerize |

### Quality Checks

- [ ] **Deterministic** - Same input → same output, every time
- [ ] **Isolated** - Test doesn't affect other tests
- [ ] **Fast** - Meets speed targets above
- [ ] **Clear** - Failure message points to exact problem
- [ ] **Relevant** - Actually catches real problems

## Anti-Patterns

❌ **"We have CI because we use Jenkins/GitHub Actions"**
- Having a CI tool ≠ practicing continuous integration
- **Real CI** = merging to main multiple times per day

❌ **"Tests are too slow, skip them during development"**
- Slow tests = architectural problem, not process problem
- **Fix**: Refactor for testability, don't skip tests

❌ **"We'll test it when it's done"**
- Extended feedback loop makes feedback useless
- **Fix**: TDD - test BEFORE code exists

❌ **"100% test coverage means good tests"**
- Coverage without quality is meaningless
- **Fix**: Measure mutation test score, not just coverage

❌ **"We test in staging before production"**
- Staging testing should be automated in pipeline
- **Fix**: If pipeline green, ship to production directly

## Integration with Other Skills

- **Requires**: `iterative-development` (small batches enable fast feedback)
- **Enables**: `experimental-workflow` (experiments need measurement)
- **Pairs with**: `continuous-integration-practice` (CI is feedback mechanism)
- **Drives**: `separation-of-concerns-enforcer` (testability reveals poor separation)

## Guardrails

1. **Never slow down to "think more"** - Think by writing tests and experimenting
2. **If feedback is slow** - Architecture problem, not lack of planning
3. **IDE should catch 80% of errors** - Configure aggressive linting/typing
4. **Pipeline failure is higher priority** than new features - Fix immediately

## Success Metrics

Track these to measure feedback quality:

- **Mean time to feedback**: Average time from code change to test result
- **Feedback frequency**: How many times per day you get test results
- **False positive rate**: How often tests fail for wrong reasons
- **Time to fix failures**: How long to diagnose and fix from test failure

**Targets**:
- MTF: <1 minute for unit tests, <10 minutes for integration
- Frequency: 10+ times per day (every small change)
- False positives: <5% (deterministic tests)
- Time to fix: <15 minutes (clear failure messages)

## Related References

See [reference/principles.md](reference/principles.md) for book quotes on feedback philosophy.
See [reference/workflow.md](reference/workflow.md) for practical feedback optimization checklists.
See [examples/](examples/) for code showing fast vs slow feedback patterns.
