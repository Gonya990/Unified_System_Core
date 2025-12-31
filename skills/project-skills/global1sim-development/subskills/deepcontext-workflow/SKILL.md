---
name: deepcontext-workflow
description: Codebase pattern discovery tool - use when stuck or exploring, NOT mandatory before all work; supports iterative-development principle "begin before knowing everything"
parent: global1sim-development
activation_triggers:
  - "stuck on implementation approach"
  - "suspect similar feature exists"
  - "exploring unfamiliar domain"
  - "need to re-index codebase"
optional: true
replaces: "mandatory DeepContext before implementing"
---

# DeepContext Workflow (Optional Discovery Tool)

**AGENTIC ACTIVATION**: Use when stuck or exploring, NOT as mandatory gate.

## 🎯 Quick Decision (LLM: When to Use)

```yaml
use_deepcontext:
  YES_activate_when:
    - stuck_after: 15+ minutes of trying
    - suspect: "similar feature might exist"
    - exploring: "unfamiliar domain area"
    - refactoring: "across multiple modules"
    - onboarding: "learning codebase structure"
    
  NO_dont_wait_when:
    - have_hypothesis: "Test it first! (experimental-workflow)"
    - simple_crud: "Follow established patterns"
    - familiar_domain: "You know the area well"
    - time_boxed_spike: "Try for 30 min first"

decision:
  if uncertain: → Try implementing for 15-30 min first
  if stuck: → THEN search DeepContext
  if found_pattern: → Adapt and continue with TDD
  if not_found: → Continue with your approach (it's novel!)
```

## 🔄 Workflow (LLM: Execute This)

### Step 1: Try First (Iterative Approach)

```python
# DO NOT start with DeepContext search!
# Book principle: "Begin work before you know the answer to everything"

def feature_workflow():
    # 1. Write hypothesis
    hypothesis = "I think this feature needs X, Y, Z"
    
    # 2. Write failing test
    write_test(hypothesis)  # RED
    
    # 3. Try implementing for 15-30 min
    try_implementation()
    
    # 4. If stuck THEN search
    if still_stuck_after_30_min:
        search_deepcontext()  # Optional discovery
    else:
        continue_with_tdd()   # Keep going!
```

### Step 2: Search When Stuck (Optional)

```bash
# ONLY if stuck after trying first

# Check index status (once per session)
mcp__deepcontext__get_indexing_status

# Search for patterns
mcp__deepcontext__search_codebase
# Query examples:
# - "subscriber service implementation"
# - "FastAPI route with validation"
# - "repository pattern for orders"
# - "Pydantic model with custom validator"
```

### Step 3: Adapt Pattern (Not Copy-Paste)

```python
# Found a pattern? Adapt it, don't copy-paste!

def adapt_pattern(found_pattern):
    # 1. Understand the pattern
    understand_why_it_works(found_pattern)
    
    # 2. Write YOUR test first
    write_test_for_your_use_case()  # TDD!
    
    # 3. Implement using pattern as inspiration
    implement_adapted_version()
    
    # 4. Refactor to your context
    refactor_to_fit_your_domain()
```

### Step 4: Re-index When Needed

```bash
# Re-index AFTER bulk changes, not before every feature

mcp__deepcontext__index_codebase(
    codebase_path="/mnt/src/agent2",
    force_reindex=true
)
```

## 🚦 Re-index Triggers (LLM: Automate This)

```yaml
re_index_after:
  bulk_changes:
    - git pull with 10+ files changed
    - refactoring session (5+ files)
    - running formatters (ruff format on many files)
    - major feature completion
    - between major work sessions (days apart)
    
  dont_re_index:
    - every_commit: "Too frequent, delays feedback"
    - before_starting: "Begin work before knowing everything!"
    - during_active_dev: "Interrupts flow"
    - after_single_file_change: "Unnecessary"

automation:
  check_if_needed: |
    if git_commits_since_last_index > 50:
        re_index()
    elif days_since_last_index > 3:
        re_index()
```

## 🎓 Alignment with Modern SE

**Book Principle**:
> "Encourages us to begin work before we know the answer to everything"

**Application**: DeepContext is a discovery tool, NOT a mandatory gate.

**Skills**:
- `iterative-development`: Work in small steps, learn as you go
- `experimental-workflow`: Try hypothesis first, search if stuck
- `feedback-driven-design`: Fast feedback from tests, not pre-planning

**Anti-pattern**:
```yaml
WRONG_workflow:
  1. Check DeepContext (mandatory gate)
  2. Search for all patterns (analysis paralysis)
  3. Study patterns for hours (delays feedback)
  4. THEN start implementing (too late!)

CORRECT_workflow:
  1. Write failing test (RED - seconds)
  2. Try implementing (GREEN - 15-30 min)
  3. If stuck, search DeepContext (optional discovery)
  4. Continue with TDD (refactor)
```

## 📊 Usage Metrics (LLM: Track These)

```yaml
healthy_usage:
  frequency: "Few times per day when stuck"
  timing: "After trying for 15-30 min"
  outcome: "Found pattern → adapted to context"
  
unhealthy_usage:
  frequency: "Before every feature (gate)"
  timing: "Before writing any code (delays)"
  outcome: "Copy-pasted code without understanding"

self_check:
  question: "Could I have tried implementing first?"
  if_yes: "Don't search, try first!"
  if_no: "Search is appropriate"
```

## 🔗 Integration

- **Parent**: `global1sim-development`
- **Supports**: `iterative-development` (optional discovery within iteration)
- **Not required by**: Any skill (all skills work without DeepContext)
- **Complements**: `experimental-workflow` (search informs experiments)

## Quick Reference

```bash
# Session start (once)
mcp__deepcontext__get_indexing_status

# When stuck (optional)
mcp__deepcontext__search_codebase
# Query: "your search terms"

# After bulk changes (periodic)
mcp__deepcontext__index_codebase(
    codebase_path="/mnt/src/agent2",
    force_reindex=true
)
```

**Remember**: Try first, search when stuck, adapt patterns, continue with TDD.
