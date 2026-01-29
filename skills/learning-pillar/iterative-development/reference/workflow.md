# Iterative Development - Practical Workflows

## Master Workflow: Feature Development

Copy this checklist for every new feature or significant change:

### Before Writing Any Code

- [ ] **Check DeepContext status** - Ensure codebase index is current
  ```bash
  # Use: mcp__deepcontext__get_indexing_status
  ```

- [ ] **Search for existing patterns**
  ```bash
  # Use: mcp__deepcontext__search_codebase
  # Query: Similar features, related models, test fixtures
  ```

- [ ] **Define observable outcome** (not implementation)
  - ❌ Bad: "Add database table with columns X, Y, Z"
  - ✅ Good: "User can view their order history"

- [ ] **Break into vertical slices** - Each slice delivers end-to-end value
  - Example: "View single order" before "View all orders with pagination"

### First Iteration (Getting to GREEN fast)

- [ ] **Write smallest possible test** for first slice
  ```python
  def test_user_can_view_single_order():
      # Arrange: minimal setup
      # Act: one action
      # Assert: one observable outcome
      pass
  ```

- [ ] **Run test, watch it fail** (RED)
  ```bash
  uv run pytest tests/test_feature.py::test_user_can_view_single_order -v
  # Expected output: FAILED - confirms test is valid
  ```

- [ ] **Write minimum code to pass** (GREEN)
  - Hardcode if necessary
  - Skip edge cases
  - Ignore performance
  - Goal: Make test pass in <15 minutes

- [ ] **Run test, watch it pass**
  ```bash
  uv run pytest tests/test_feature.py::test_user_can_view_single_order -v
  # Expected output: PASSED
  ```

- [ ] **Commit immediately** - You have something working
  ```bash
  git add .
  git commit -m "feat: add basic order view (hardcoded)
  
  - Returns single order for user
  - Test coverage: basic happy path
  - TODO: Edge cases, real data, error handling
  
  Co-authored-by: factory-droid[bot] <138933559+factory-droid[bot]@users.noreply.github.com>"
  ```

### Refactoring Iterations (Improving while GREEN)

- [ ] **Make one small improvement** (extract hardcoding, add validation, etc.)

- [ ] **Run test after EVERY tiny change**
  ```bash
  # After each refactoring (extract method, rename, etc.):
  uv run pytest tests/test_feature.py::test_user_can_view_single_order -v
  # Must stay PASSED
  ```

- [ ] **If test fails** - Undo last change immediately
  ```bash
  git diff  # See what you just changed
  git checkout -- <file>  # Undo the breaking change
  ```

- [ ] **When improvement is complete** - Commit
  ```bash
  git commit -am "refactor: replace hardcoded order with repository call"
  ```

- [ ] **Repeat** until code is clean, expressive, properly abstracted

### Next Iteration (Adding Functionality)

- [ ] **Add test for next small behavior**
  ```python
  def test_user_cannot_view_other_users_order():
      # New test, new behavior
      pass
  ```

- [ ] **Follow RED → GREEN → REFACTOR cycle**

- [ ] **Commit atomic change**

- [ ] **Push to trigger CI** (at least once per day)
  ```bash
  git push origin feature/esim-inventory-system
  # CI runs all tests in integration
  ```

## The "Stuck" Workflow

When you're stuck and don't know next step:

### 1. Acknowledge Current State

- [ ] **Run all tests** - What's currently working?
  ```bash
  uv run pytest tests/ -v --tb=short
  ```

- [ ] **Review recent commits** - How did we get here?
  ```bash
  git log --oneline -10
  git diff HEAD~3..HEAD  # Last 3 commits
  ```

### 2. Define Minimal Next Step

- [ ] **What's the SMALLEST testable behavior** we could add?
  - Not: "Implement entire order lifecycle"
  - Yes: "Order can transition from pending to confirmed"

- [ ] **Write that one test** - Even if you're not sure how to implement

### 3. Experiment

- [ ] **Try simplest possible implementation** (even if you know it's wrong)
  ```python
  # It's OK to start with:
  def confirm_order(order_id: str) -> Order:
      return Order(id=order_id, status="confirmed")  # Hardcoded!
  ```

- [ ] **Run test** - Does it teach you anything?

- [ ] **Spike if necessary** - Time-boxed exploration
  ```bash
  git checkout -b spike/order-confirmation-approach
  # Experiment for 30 minutes max
  # Learn what works
  # Return to main branch
  git checkout feature/esim-inventory-system
  # Apply learnings properly with tests
  ```

### 4. Re-evaluate

- [ ] **Are we closer to outcome?** 
  - Yes → Commit and continue
  - No → Revert and try different approach

- [ ] **Is batch size too large?**
  - Can we break this into smaller steps?
  - Can we simplify the test?

## The "Too Slow" Workflow

When feedback cycles are taking too long:

### Symptoms
- Tests take >10 seconds to run
- Can't commit multiple times per day
- Waiting on CI to know if change works

### Diagnosis

- [ ] **Measure test runtime**
  ```bash
  uv run pytest tests/ -v --durations=10
  # Shows slowest 10 tests
  ```

- [ ] **Identify slow tests** - Usually integration/acceptance tests

### Treatment

- [ ] **Run only relevant unit tests during development**
  ```bash
  # Fast feedback loop:
  uv run pytest tests/unit/test_order_service.py -v
  
  # Full suite before commit:
  uv run pytest tests/
  ```

- [ ] **If unit tests are slow** → Architectural problem
  - Are you hitting database in unit tests? (Should use fakes)
  - Are you calling external APIs? (Should be mocked)
  - Are you loading entire framework? (Should test pure functions)
  - **Action**: Refactor for testability (see `separation-of-concerns-enforcer`)

- [ ] **If CI is slow** → Deployment pipeline problem
  - **Target**: <10 minutes commit to green
  - **Action**: Parallelize tests, optimize Docker builds
  - **Last resort**: See `deployment-pipeline-designer` for architectural changes

## The "Continuous Integration" Workflow

Ensuring your iterations integrate with team's work:

### Daily Minimum

- [ ] **Pull latest changes** before starting work
  ```bash
  git pull --rebase origin feature/esim-inventory-system
  ```

- [ ] **Commit at least once per day**
  - Even if feature incomplete
  - Atomic, tested, passes CI

- [ ] **Push at least once per day**
  - Exposes your changes to CI
  - Validates integration with others' work

### When CI Fails

- [ ] **Stop everything** - Your code broke integration
  
- [ ] **Check CI output immediately**
  
- [ ] **Two options**:
  1. **Quick fix** (<5 min) → Fix and push
  2. **Complex fix** → Revert commit, fix locally, recommit
  
- [ ] **Never leave broken CI >30 minutes** - Blocks entire team

### Feature Flags for Incomplete Work

When feature spans multiple days but you need to commit:

```python
# In code:
from src.config.settings import settings

if settings.ENABLE_ORDER_HISTORY:
    # New incomplete feature
    return get_order_history(user_id)
else:
    # Old working code
    return get_latest_order(user_id)
```

```bash
# In .env (disabled in production):
ENABLE_ORDER_HISTORY=false
```

- [ ] **Deploy to production** even with incomplete code (flag disabled)
- [ ] **Test in development** with flag enabled
- [ ] **Remove flag** once feature complete

## Time-Boxing

When iteration takes too long:

- **Unit test RED → GREEN**: <15 minutes
  - Longer → Batch size too large, break into smaller test

- **Refactoring**: <30 minutes before commit
  - Longer → Commit intermediate state, continue refactoring

- **Feature slice**: <4 hours (half day)
  - Longer → Slice too thick, break into thinner slices

- **Spike/Exploration**: <1 hour
  - Longer → Schedule pairing session or seek help

## Quality Gates Before Each Commit

Run these before EVERY commit:

```bash
# 1. Run affected tests (seconds)
uv run pytest tests/test_order_service.py -v

# 2. Run full unit test suite (should be <1 minute)
uv run pytest tests/unit/ -v

# 3. Check code quality (seconds)
uv run ruff check src/ tests/
uv run ruff format src/ tests/

# 4. Type check (seconds to minutes)
uv run mypy src/

# 5. If all pass → Commit
git add .
git commit -m "..."

# 6. Full suite before push (minutes)
uv run pytest tests/
git push
```

**If any gate takes >5 minutes** → Architectural issue, needs fixing

## The "End of Day" Checklist

Before finishing for the day:

- [ ] **All tests passing locally**
- [ ] **At least one commit pushed** (even if work-in-progress)
- [ ] **CI is green** (or broken build has been fixed)
- [ ] **No uncommitted changes** (or explicitly stashed with description)
- [ ] **TODO comments** for tomorrow's first iteration

```python
# Good TODO for iteration:
# TODO: Next iteration - add validation for order status transitions
# Current: Order can transition to any status (hardcoded)
# Next: Add state machine validation (test already written: test_invalid_transition_raises_error)
```

## Recovery Workflow

When you've gone too far without committing:

- [ ] **Stop adding more changes**

- [ ] **Run all tests** - What's working?
  ```bash
  uv run pytest tests/ -v
  ```

- [ ] **Review all changes**
  ```bash
  git diff
  # Too much? Can't explain every line?
  ```

- [ ] **Option 1: Partial commit** (if tests pass)
  ```bash
  git add src/services/order_service.py tests/test_order_service.py
  git commit -m "feat: add order service (partial - validation pending)"
  # Continue with remaining changes
  ```

- [ ] **Option 2: Stash and restart** (if messy)
  ```bash
  git stash push -u -m "WIP: order service attempt 1 - too complex"
  # Start over with smaller iterations
  # Reference stash if needed: git stash show -p stash@{0}
  ```

## Remember

> "At each point in the process, I can re-evaluate and change my mind and the direction of my design and code easily. I keep my options open!" - David Farley

Iteration keeps options open. The moment you commit to a big batch, you lose that flexibility.
