---
name: iterative-development
description: Enforces small-batch, incremental work with fast feedback loops based on Dave Farley's Modern Software Engineering; use when starting any feature or refactoring work to maintain forward momentum when answers are unknown.
---

# Iterative Development

Activate this skill whenever you need to make progress on a feature or problem where you don't have all the answers yet. This is the foundational practice that enables all other engineering disciplines.

## Core Principle

**"Begin work before you know the answer to everything"** - Software development is discovery and learning. Working iteratively allows us to make progress in small steps, learn from reality, and adapt our direction.

## Quick Start

1. **Work in smallest possible batches** - Reduce scope of each change to absolute minimum
2. **Commit multiple times per day** - At least once, preferably 3-5+ times (CI requirement)
3. **Each change is atomic** - Works independently even if feature incomplete
4. **Keep options open** - Always close to a "safe place" to retreat to

## The Alphabet vs Pictograph Mental Model

**From the book**: 
- **Waterfall = Pictographic writing** (~50,000 Chinese characters - must know each symbol before proceeding)
- **Iterative = Alphabetic writing** (26 letters - infinite combinations, can spell anything even if you've never seen it)

**Quote**: "One is a scalable approach to representing ideas; the other is not. A waterfall approach is sequential. You must answer the questions of the stage that you are in before proceeding to the next stage."

## Mandatory Workflow

### RED → GREEN → REFACTOR Cycle

```bash
# 1. RED: Write failing test first
uv run pytest tests/test_feature.py::test_new_behavior -v
# Expected: Test fails (verifying test is correct)

# 2. GREEN: Minimal code to make it pass
# Write simplest possible implementation
uv run pytest tests/test_feature.py::test_new_behavior -v
# Expected: Test passes

# 3. REFACTOR: Improve while tests stay green
# Make tiny refactoring steps, run test after EACH step
uv run pytest tests/test_feature.py::test_new_behavior -v
# After each tiny change: Test still passes
```

**Critical**: Feedback cycles measured in seconds or milliseconds, not minutes or hours

## When Answers Are Unknown - Checklist

Use this when starting work where destination is unclear:

- [ ] **Define observable outcome** (not mechanism) - "Shopping cart has item" not "Database insert succeeds"
- [ ] **Write smallest possible test** that describes next tiny step toward outcome
- [ ] **Run test to see it fail** (RED phase - validates test correctness)
- [ ] **Write absolute minimum code** to pass (GREEN phase)
- [ ] **Evaluate current position** - Are we closer to desired outcome?
- [ ] **Decide next tiny step** based on current reality (not original plan)
- [ ] **Commit atomic change** - Even if feature incomplete, this step is stable
- [ ] **Repeat** - Build value incrementally through many small iterations

**Quote**: "This allows us to refine our thinking, identify the next small step, and then take that step...This is a profoundly more organic, evolutionary, unbounded approach to problem solving."

## Practical Limits on Batch Size

### Code Level
- **Function/Method**: One concern per function (see `separation-of-concerns-enforcer`)
- **Refactoring**: Extract method, introduce parameter - one transformation at a time
- **Run test after every tiny change** - Keep cycle <5 seconds

### Commit Level
- **Target**: 3-5 commits per day minimum
- **Each commit**: Passes all tests (always releasable)
- **Atomic**: Change stands alone, even if feature partially complete
- **Small**: <200 lines changed (smaller is better)

### Feature Level
- **Break into vertical slices** - Each slice delivers end-to-end value
- **Deploy behind feature flag** if incomplete
- **Get to production fast** - Learn from real usage

## Anti-Patterns to Avoid

❌ **"Let me finish this feature first, then I'll commit"**
- Result: Merge hell, late feedback, big-bang integration
- Instead: Commit incomplete but atomic steps multiple times daily

❌ **"I need to design the whole system before coding"**
- Result: Paralysis, waterfall thinking, wrong assumptions baked in
- Instead: Design one small piece, code it, learn, adapt design

❌ **"These tests are slowing me down"**
- Result: Skipping RED phase, losing design feedback, brittle code
- Instead: If tests are slow, your architecture needs improvement (see `feedback-driven-design`)

❌ **"Feature branches let us work independently"**
- Result: Deferred integration, merge conflicts, duplicate work
- Instead: Trunk-based development with atomic commits (see `continuous-integration-practice`)

## Integration with Other Skills

- **Pairs with**: `feedback-driven-design` (optimizes feedback speed)
- **Enables**: `experimental-workflow` (each iteration is an experiment)
- **Requires**: `continuous-integration-practice` (validates integration continuously)
- **Supports**: `refactoring-mastery` (tiny safe steps)

## Guardrails

1. **Never skip the RED phase** - How do you know test is correct if it never failed?
2. **Commit at least once per day** - If you can't, batch size is too large
3. **Each commit passes all tests** - Broken commits block everyone else
4. **Can't deploy in <1 hour?** - Architecture problem, not process problem (see `deployment-pipeline-designer`)

## Success Metrics

- **Commit frequency**: 3-5+ per day per developer
- **Time to feedback**: Unit tests <100ms, full suite <10min
- **Work-in-progress**: <3 uncommitted changes at any time
- **Rollback capability**: Can revert to "safe place" in <1 minute

## Real-World Application

**From the book - SpaceX Starship example**:
- Switching from 4mm to 3mm stainless steel
- Had all the tensile strength data and calculations
- Still built experimental prototypes and tested to destruction
- "SpaceX collected data and validated its models because these models will certainly be wrong in some maybe esoteric, difficult-to-predict way"

**Our application**: Even "simple" changes deserve experimental validation through iterative testing.

## Related References

See [reference/principles.md](reference/principles.md) for book quotes and deeper philosophy.
See [reference/workflow.md](reference/workflow.md) for detailed step-by-step checklists.
See [examples/](examples/) for code samples showing iteration at different scales.
