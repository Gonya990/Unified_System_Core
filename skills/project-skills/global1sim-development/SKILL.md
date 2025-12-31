---
name: global1sim-development
description: Global1SIM telecommunications platform development orchestrator - routes to appropriate Modern SE skills + project-specific subskills; activate for ALL Global1SIM work
activation_triggers:
  - "implementing Global1SIM feature"
  - "working in /mnt/src/agent2"
  - "telecom domain (SIM, subscriber, eSIM)"
  - "FastAPI + Pydantic + UV stack"
routes_to:
  - Modern SE skills (iterative-development, feedback-driven-design, etc.)
  - Project subskills (deepcontext-workflow, pydantic-v2-patterns, etc.)
decision_tree: true
llm_friendly: true
---

# Global1SIM Development Orchestrator

**AGENTIC ACTIVATION**: This skill activates automatically for all Global1SIM project work and routes you to the right skills.

## 🎯 Quick Decision Tree (LLM: Follow This Path)

```
Starting Global1SIM work?
├─ Is this a NEW feature/capability?
│  ├─ YES → Is it experimental or uncertain?
│  │  ├─ EXPERIMENTAL → Route to: `subskill/experimental-features-workflow`
│  │  │                 (Spike → Hypothesis → Build → Measure → Decide)
│  │  │
│  │  └─ CLEAR → Route to: `iterative-development` (start small)
│  │              Then: `feedback-driven-design` (write test first)
│  │
│  └─ NO → Is it a BUG fix?
│     └─ YES → Route to: `feedback-driven-design` (write failing test)
│               Then: `refactoring-mastery` (fix in tiny steps)
│
├─ Need to DESIGN architecture/modules?
│  └─ Route to: `separation-of-concerns-enforcer` (essential vs accidental)
│             + `modularity-architect` (boundaries)
│             + `cohesion-coach` (what belongs together?)
│
├─ Working with EXTERNAL library?
│  └─ Route to: subskill/context7-workflow
│
├─ Looking for EXISTING patterns?
│  └─ Route to: subskill/deepcontext-workflow (optional tool)
│
├─ Writing TESTS?
│  └─ Route to: subskill/pytest-conventions
│             + `python-test-strategy`
│
├─ Creating MODELS?
│  └─ Route to: subskill/pydantic-v2-patterns
│             + `separation-of-concerns-enforcer`
│
├─ Managing DEPENDENCIES?
│  └─ Route to: subskill/uv-toolchain
│
└─ Handling ERRORS?
   └─ Route to: subskill/python-error-patterns
```

---

## 🤖 Agentic Workflow (LLM: Execute This Loop)

### Phase 1: ACTIVATE (Every Session Start)

```yaml
session_start:
  actions:
    - check: "Are we in Global1SIM codebase? (/mnt/src/agent2)"
      if_yes: activate_this_skill
    
    - decide: "What type of work?"
      options:
        new_feature: → iterative-development
        bug_fix: → feedback-driven-design  
        refactoring: → refactoring-mastery
        architecture: → modularity-architect
        
    - check: "Need to discover patterns?"
      if_stuck: → subskill/deepcontext-workflow
      if_clear: → proceed_with_TDD
```

### Phase 2: ITERATE (Continuous Loop)

```yaml
development_loop:
  outer_loop: "Feature development (hours to days)"
    - define: hypothesis (experimental-workflow)
    - break_down: into small batches (iterative-development)
    - measure: success criteria (empirical-measurement)
    
  inner_loop: "TDD cycle (seconds to minutes)"
    - RED: write failing test
      skills: [pytest-conventions, python-test-strategy]
    
    - GREEN: minimal code to pass
      skills: [pydantic-v2-patterns, python-error-patterns, separation-of-concerns-enforcer]
    
    - REFACTOR: improve in tiny steps
      skills: [refactoring-mastery, high-performance-simplicity]
    
  commit_loop: "Integration (3-5+ times per day)"
    - run: quality checks (ruff, mypy)
    - commit: atomic change
    - push: to trigger CI
    - wait: < 10 min for feedback
    
  continuous_practices: "Always active (concurrent)"
    - separate_concerns: essential vs accidental
    - maintain_cohesion: related together
    - minimize_coupling: loose between modules
    - hide_information: appropriate abstraction
```

### Phase 3: VALIDATE (After Each Change)

```yaml
validation_checks:
  immediate: "After every tiny change (seconds)"
    - run_test: uv run pytest path/to/test.py -v
    - expect: GREEN (if RED, undo last change)
  
  commit: "Before pushing (minutes)"
    - run: uv run ruff check && uv run ruff format
    - run: uv run mypy src/
    - run: uv run pytest tests/
    - if_all_pass: git commit
  
  integration: "After CI completes (< 10 min)"
    - check: CI status
    - if_red: fix immediately (highest priority)
    - if_green: continue next iteration
  
  periodic: "Track improvement (weekly)"
    - measure: DORA metrics
    - validate: assumptions with data
    - adjust: practices based on evidence
```

---

## 📚 Skill Routing Map (LLM: Use This Lookup)

### Modern SE Skills (Foundation - Always Available)

| When LLM Needs To... | Route To Skill | Quick Reference |
|---------------------|---------------|-----------------|
| Start new work in small batches | `iterative-development` | RED→GREEN→REFACTOR, commit 3-5x/day |
| Optimize feedback speed | `feedback-driven-design` | IDE→tests→CI→prod hierarchy |
| Test hypothesis scientifically | `experimental-workflow` | Hypothesis→Predict→Experiment→Measure |
| Separate essential from accidental | `separation-of-concerns-enforcer` | One class/method one thing |
| Design module boundaries | `modularity-architect` | Monolith OR microservices, no middle |
| Keep related code together | `cohesion-coach` | Related together, unrelated apart |
| Hide implementation details | `abstraction-patterns` | Information hiding, prevent leaks |
| Minimize dependencies | `coupling-minimizer` | DRY is too simplistic, async decoupling |
| Make tiny safe changes | `refactoring-mastery` | One IDE refactoring at a time |
| Optimize performance | `high-performance-simplicity` | Simple = fast, measure don't guess |
| Design deployment pipeline | `deployment-pipeline-designer` | Commit to prod < 1 hour |
| Track improvement | `empirical-measurement` | DORA metrics validate all changes |

### Global1SIM Subskills (Project-Specific)

| When LLM Needs To... | Route To Subskill | Quick Reference |
|---------------------|------------------|-----------------|
| Build experimental features | `subskill/experimental-features-workflow` | Spike → Hypothesis → Build → Measure → Decide |
| Search existing codebase | `subskill/deepcontext-workflow` | Optional discovery tool, not gate |
| Research external library | `subskill/context7-workflow` | resolve-library-id → get-library-docs |
| Create Pydantic models | `subskill/pydantic-v2-patterns` | frozen=True, field_validator, why immutability |
| Manage dependencies | `subskill/uv-toolchain` | NEVER pip, always uv |
| Handle errors properly | `subskill/python-error-patterns` | Exceptions vs Optional[T] |
| Write project tests | `subskill/pytest-conventions` | Naming, fixtures, parametrize patterns |
### Existing Project Skills (Specialized)

| When LLM Needs To... | Route To Skill | Quick Reference |
|---------------------|---------------|-----------------||
| Implement hexagonal architecture | `python-hexagonal-development` | Ports & adapters, dependency injection |
| Design test strategy | `python-test-strategy` | Test pyramid, adapter tests, acceptance tests |
| Design distinctive frontend UI | `frontend-aesthetics` | Youthful, brand-forward visuals (typography, color, motion, backgrounds) |
| Design youth-focused UX flows | `youth-brand-ux` | Flows, tone, and microcopy for confident youth engagement |

---
---

## 🎓 The Two Pillars (LLM: Keep Both Active)

**From Modern Software Engineering book** - These are concurrent, not sequential:

### Pillar 1: Optimize for Learning
```yaml
always_active:
  - iterate: Small batches, frequent commits
  - feedback: Fast at all levels (IDE→tests→CI→prod)
  - experiment: Hypothesis-driven development
  - measure: DORA metrics validate assumptions
  
skills:
  - iterative-development
  - feedback-driven-design
  - experimental-workflow
  - empirical-measurement
```

### Pillar 2: Optimize for Managing Complexity
```yaml
always_active:
  - separate_concerns: Essential vs accidental
  - modularize: Clear boundaries, information hiding
  - maintain_cohesion: Related together, unrelated apart
  - minimize_coupling: Loose between modules
  
skills:
  - separation-of-concerns-enforcer
  - modularity-architect
  - cohesion-coach
  - abstraction-patterns
  - coupling-minimizer
```

**Critical**: These are NOT priority ranks 1-8. They work together simultaneously.

---

## 🚦 Decision Points (LLM: Choose Path)

### When Starting Feature Work

```python
# DECISION: Do I know how to implement this?

if have_clear_approach:
    # Route to: iterative-development
    # Start with failing test (RED)
    activate(pytest_conventions)
    activate(pydantic_v2_patterns)
    
elif uncertain_about_approach:
    # Route to: experimental-workflow
    # Define hypothesis first, then spike
    activate(experimental_workflow)
    # THEN decide:
    if need_existing_patterns:
        activate(deepcontext_workflow)  # Optional
    if need_library_docs:
        activate(context7_workflow)  # Optional
        
else:  # completely_stuck
    # Route to: deepcontext-workflow
    # Search for similar features
    search_codebase("similar to [feature]")
    # Then route to iterative-development
```

### When Writing Code

```python
# DECISION: What am I creating?

if creating_domain_model:
    # Route to: pydantic-v2-patterns
    # + separation-of-concerns-enforcer
    use_frozen_true = True
    separate_essential_from_accidental = True
    
elif creating_service:
    # Route to: separation-of-concerns-enforcer
    # + python-hexagonal-development
    inject_dependencies = True
    keep_business_logic_pure = True
    
elif creating_repository:
    # Route to: separation-of-concerns-enforcer
    # + abstraction-patterns
    hide_database_details = True
    translate_at_boundary = True
    
elif creating_api_endpoint:
    # Route to: separation-of-concerns-enforcer
    # Handle only HTTP concerns
    delegate_to_service = True
```

### When Test Fails

```python
# DECISION: Why did test fail?

if test_never_passed_before:
    # Expected (RED phase)
    # Route to: iterative-development
    write_minimal_code_to_pass()
    
elif test_passed_then_failed:
    # Regression
    # Route to: refactoring-mastery
    git diff  # What changed?
    undo_last_change()  # Back to safe place
    
elif test_is_slow:
    # Architecture problem
    # Route to: feedback-driven-design
    # + separation-of-concerns-enforcer
    refactor_for_testability()
    # Slow test = poor separation of concerns
```

### When Committing

```python
# DECISION: Is this ready to commit?

checks = {
    "tests_pass": run("uv run pytest"),
    "type_check": run("uv run mypy src/"),
    "lint_clean": run("uv run ruff check"),
    "formatted": run("uv run ruff format"),
}

if all(checks.values()):
    # Route to: continuous-integration-practice
    git commit -m "atomic change message"
    git push  # Trigger CI (should complete < 10 min)
else:
    # Fix issues before committing
    # Route to: refactoring-mastery (fix in tiny steps)
```

---

## 🔧 Tool Usage Patterns (LLM: When to Use Each)

### DeepContext (Optional Discovery)

```yaml
use_when:
  - Stuck on implementation after 15+ min
  - Suspect similar feature exists
  - Exploring unfamiliar domain area
  - Refactoring across modules

dont_wait_for:
  - Starting new feature (begin before knowing everything!)
  - Simple CRUD operations (follow patterns)
  - Have clear hypothesis (test it first!)
  
workflow:
  1. Try implementing for 15-30 min
  2. If stuck, search DeepContext
  3. Find pattern, adapt to your case
  4. Continue with TDD

skill: subskill/deepcontext-workflow
```

### Context7 (Library Research)

```yaml
use_when:
  - Using unfamiliar library first time
  - Library behavior unclear from docs
  - Need best practices for library
  
dont_wait_for:
  - Familiar libraries (FastAPI, Pydantic)
  - Standard library (typing, dataclasses)
  
workflow:
  1. resolve-library-id
  2. get-library-docs
  3. Write test based on docs
  4. Implement following best practices

skill: subskill/context7-workflow
```

### UV (Always, Exclusively)

```yaml
use_for_everything:
  - Adding dependencies: uv add package
  - Dev dependencies: uv add --dev pytest
  - Running tests: uv run pytest
  - Running scripts: uv run python script.py
  
never_use:
  - pip install (NEVER)
  - pip freeze (use uv.lock)
  
why:
  - Faster than pip
  - Deterministic dependencies
  - Project-level isolation
  
skill: subskill/uv-toolchain
```

---

## 📏 Quality Gates (LLM: Enforce These)

### Before Every Commit (Automated)

```bash
# These must all pass:
uv run pytest tests/              # All tests green
uv run ruff check src/ tests/     # No lint errors
uv run ruff format src/ tests/    # Formatted
uv run mypy src/                  # Type check passes

# If any fail → Fix before commit
# Route to: refactoring-mastery (fix in tiny steps)
```

### After Every Commit (CI Pipeline)

```yaml
ci_must_complete_within: 10 minutes

if_ci_fails:
  priority: HIGHEST (stop everything else)
  action: Fix immediately
  skill: continuous-integration-practice
  
if_ci_takes_longer_than_10_min:
  problem: Architecture issue
  skill: deployment-pipeline-designer
  quote: "If any single test takes longer than an hour..."
```

### Periodically (Weekly/Sprint)

```yaml
track_dora_metrics:
  deployment_frequency: "Multiple times per day (target)"
  lead_time: "< 1 hour (target)"
  mttr: "< 1 hour (target)"
  change_failure_rate: "< 15% (target)"

skill: empirical-measurement
validate: "Did our changes improve metrics?"
```

---

## 🎯 Success Criteria (LLM: Measure These)

### Daily Targets

- [ ] Committed 3-5+ times
- [ ] All commits passed CI < 10 min
- [ ] Tests run in <10 seconds locally
- [ ] No long-lived branches (trunk-based only)

### Weekly Targets

- [ ] Deployed to production 10+ times
- [ ] DORA metrics improving or stable
- [ ] No features taking >1 week
- [ ] Test coverage increasing

### Code Quality Targets

- [ ] All business logic pure functions
- [ ] All models immutable (frozen=True)
- [ ] All functions fully type-hinted
- [ ] All code separated (essential vs accidental)

---

## 🔗 Integration Points

### With Modern SE Skills
```
This skill ORCHESTRATES Modern SE skills for Global1SIM context:
├─ Routes feature work → iterative-development
├─ Routes design decisions → separation-of-concerns-enforcer
├─ Routes testing → feedback-driven-design + python-test-strategy
├─ Routes architecture → modularity-architect + cohesion-coach
└─ Routes measurement → empirical-measurement
```

### With Project Subskills
```
This skill DELEGATES to project-specific subskills:
├─ Experimental features → subskill/experimental-features-workflow
├─ Pattern discovery → subskill/deepcontext-workflow
├─ Library research → subskill/context7-workflow
├─ Model creation → subskill/pydantic-v2-patterns
├─ Dependency mgmt → subskill/uv-toolchain
├─ Error handling → subskill/python-error-patterns
└─ Test conventions → subskill/pytest-conventions
```

---

## 📖 Related Documentation

- **Modern SE Skills**: `/mnt/src/agent2/skills/README.md`
- **Book Insights**: `/mnt/src/agent2/docs/Modern_Software_Engineering_Insights.md`
- **Alignment Analysis**: `/mnt/src/agent2/PROMPT_ALIGNMENT_ANALYSIS.md`
- **Project Structure**: [reference/project-structure.md](reference/project-structure.md)

---

## 🚀 Quick Start (LLM: First Time Activation)

1. **Activate this skill** when working in Global1SIM codebase
2. **Follow decision tree** above to route to appropriate skills
3. **Keep both pillars active** (learning + complexity management)
4. **Use tools when needed** (DeepContext, Context7 = optional, not mandatory)
5. **Measure continuously** (DORA metrics validate all changes)

**Remember**: 
- Skills work together (concurrent, not sequential)
- Tools are optional discovery aids (not gates)
- TDD drives design quality (write test first)
- Small batches enable learning (commit 3-5x/day)
- Feedback speed matters (< 10 sec tests, < 10 min CI)

---

**AGENTIC NOTE**: This skill is your routing orchestrator. Always consult the decision tree when uncertain which skill to activate next.
