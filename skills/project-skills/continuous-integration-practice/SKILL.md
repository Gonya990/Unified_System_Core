---
name: continuous-integration-practice
description: True CI - merge to main multiple times per day, NOT feature branching; supports iterative-development (small batches expose change early)
activation_triggers:
  - "committing code"
  - "branching strategy decision"
  - "merge conflicts"
replaces: "feature branching"
book_quote: "CI and feature branching are not compatible"
---

# Continuous Integration Practice (True CI)

**AGENTIC RULE**: Trunk-based development. Merge to main 3-5+ times per day.

## 🎯 Decision Tree (LLM: Branching Strategy)

```yaml
branching_decision:
  question: "Should I create a feature branch?"
  
  answer: NO (use trunk-based development)
  
  why_no_feature_branches:
    book_quote: >
      "Continuous integration and feature branching (FB) are not really
      compatible with each other. One aims to expose change as early as
      possible; the other works to defer that exposure."
    
    problem: "Merging code ≠ merging behavior"
    example: >
      Two developers independently add "increment by one" to different
      parts of same function. Merge succeeds, but value incremented by TWO.
      
  correct_approach:
    strategy: "Trunk-based development"
    commits: "Direct to main branch, 3-5+ times per day"
    incomplete_features: "Use feature flags, not branches"
```

## 🔄 True CI Definition

**From book**:
> "Merging all developers' working copies to a shared mainline several times a day."

**Minimum**: At least once per day  
**Target**: 3-5+ commits per day  
**Goal**: Continuous exposure of changes

## 🚦 Workflow (LLM: Execute This)

### Before Committing

```bash
# 1. All tests pass
uv run pytest tests/

# 2. Code quality checks
uv run ruff check src/ tests/
uv run ruff format src/ tests/
uv run mypy src/

# 3. Atomic change (even if feature incomplete)
git add .
git commit -m "feat: add order validation (partial - UI pending)

- Validates order data structure
- Raises ValidationError for invalid data
- TODO: Add UI error handling

Co-authored-by: factory-droid[bot] <138933559+factory-droid[bot]@users.noreply.github.com>"
```

### After Committing

```bash
# Push immediately (expose change)
git push origin main

# CI must complete within 10 minutes
# If longer → architecture problem (deployment-pipeline-designer)
```

### If CI Fails

```yaml
priority: HIGHEST (stop all other work)

actions:
  1. Check CI output immediately
  2. Two options:
     quick_fix: < 5 min → fix and push
     complex_fix: > 5 min → revert, fix locally, recommit
  3. Never leave CI red > 30 minutes (blocks team)
```

## 🏗️ Feature Flags for Incomplete Work

**Problem**: Feature spans multiple days but need to commit daily

**Solution**: Feature flags (NOT feature branches)

```python
# In code
from src.config.settings import settings

if settings.ENABLE_NEW_ORDER_FLOW:
    # New incomplete feature
    return handle_order_v2(order)
else:
    # Old working code
    return handle_order_v1(order)
```

```bash
# In .env (disabled in production)
ENABLE_NEW_ORDER_FLOW=false
```

**Benefits**:
- Commit to main daily (CI exposed)
- Deploy to production safely (flag off)
- Test in development (flag on)
- Remove flag when complete

## 🎓 Book Alignment

**Quote**:
> "For CI to work, we have to commit our changes frequently enough to gain that feedback...This means working very differently."

**Skills**:
- `iterative-development`: Small batches enable frequent commits
- `feedback-driven-design`: CI provides integration feedback quickly
- `deployment-pipeline-designer`: Fast CI (< 10 min) required

**Anti-pattern**:
```yaml
WRONG:
  - Create feature branch
  - Work for days/weeks
  - Merge when "done"
  - Result: Merge hell, late feedback

CORRECT:
  - Work on main branch
  - Commit 3-5+ times per day
  - Use feature flags for incomplete work
  - Result: Early feedback, small integrations
```

## 📏 Success Metrics

```yaml
team_metrics:
  commits_per_dev_per_day: ">= 3"
  ci_duration: "< 10 minutes"
  ci_failure_rate: "< 15%"
  time_to_fix_red_ci: "< 30 minutes"
  
individual_metrics:
  longest_time_without_commit: "< 4 hours"
  merge_conflicts: "Rare (small batches prevent)"
  feature_branch_age: "0 days (don't use them!)"
```

## 🔧 CI Pipeline Requirements

**Must complete within 10 minutes**:
```yaml
stages:
  1_unit_tests: "< 10 seconds"
  2_integration_tests: "< 5 minutes"
  3_linting: "< 1 minute"
  4_type_checking: "< 1 minute"
  5_build: "< 2 minutes"
  6_deploy_to_staging: "< 1 minute"
  
total: "< 10 minutes"

if_slower:
  skill: deployment-pipeline-designer
  action: Parallelize or refactor architecture
```

## 🚫 Anti-Patterns

```yaml
feature_branching:
  problem: "Defers integration, causes merge hell"
  fix: "Trunk-based + feature flags"
  
pull_request_delays:
  problem: "Waiting days for PR review breaks CI"
  fix: "Pair programming or quick reviews (< 1 hour)"
  
large_commits:
  problem: "Changes not exposed continuously"
  fix: "Atomic commits 3-5+ per day"
  
broken_ci_ignored:
  problem: "Team continues working on red CI"
  fix: "Stop everything, fix within 30 min"
```

## 🔗 Integration

- **Requires**: `iterative-development` (small batches)
- **Enables**: `feedback-driven-design` (fast integration feedback)
- **Validates**: `deployment-pipeline-designer` (CI duration < 10 min)
- **Measured by**: `empirical-measurement` (DORA deployment frequency)

## Quick Reference

```bash
# Daily workflow
git pull --rebase origin main  # Start of day
# Work in small batches
git commit -m "atomic change"  # 3-5+ times per day
git push origin main           # Expose immediately

# CI must be:
# - Fast (< 10 min)
# - Reliable (< 15% failure rate)
# - Respected (fix red CI immediately)
```

**Remember**: "Merge to main multiple times per day" is the definition of CI. Feature branches break this.
