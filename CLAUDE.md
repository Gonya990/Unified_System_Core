# Unified System Core - Development Guide

This is the central routing guide for the Modern Software Engineering skills and AI agent framework.

---

## Quick Navigation

### Skills Framework
**Location**: `skills/`

| Pillar | Purpose | Skills |
|--------|---------|--------|
| `learning-pillar/` | Optimize for learning | iterative-development, feedback-driven-design, experimental-workflow, deployment-pipeline-designer, empirical-measurement |
| `complexity-pillar/` | Manage complexity | separation-of-concerns-enforcer, modularity-architect, cohesion-coach, abstraction-patterns, coupling-minimizer |
| `supporting-skills/` | Supporting practices | refactoring-mastery, high-performance-simplicity, frontend-aesthetics, youth-brand-ux |
| `project-skills/` | Project-specific | continuous-integration-practice, global1sim-development (with subskills) |
| `architecture-skills/` | Architecture patterns | python-hexagonal-development, python-test-strategy |

**Index**: `skills/README.md`

---

### Agent Framework
**Location**: `.claude/agents/`

| Category | Agents |
|----------|--------|
| `discovery/` | code-explorer, api-discoverer, dependency-mapper |
| `architecture/` | code-architect, hexagonal-architecture-guardian, performance-optimizer |
| `implementation/` | implementer, bug-fixer |
| `review/` | code-reviewer |
| `testing/` | tdd-cycle-driver |
| `workflow/` | feedback-loop-optimizer |
| `coordination/` | code-quality-coordinator, devops-workflow-orchestrator |
| `devops/` | security-hardening-worker, performance-optimization-worker |
| `ui-ux/` | senior-ui-ux-designer |

**Index**: `.claude/agents/README.md`

---

### Orchestration Guidelines
**Location**: `docs/agent-guidelines/`

| Document | Purpose |
|----------|---------|
| `velocity-principles.md` | Agent speed optimization |
| `orchestration-principles.md` | Multi-agent coordination |
| `agent-capability-patterns.md` | Agent types and boundaries |
| `context-management.md` | Token efficiency |
| `feedback-optimization.md` | Fast feedback loops |
| `parallel-execution-patterns.md` | Concurrent execution |
| `orchestration-metrics.md` | DORA metrics |
| `IMPLEMENTATION.md` | 5 orchestration patterns |

**Templates**: `docs/agent-guidelines/templates/`
**Test Results**: `docs/agent-guidelines/test-results/`

---

### Programming Patterns
**Location**: `docs/patterns/`

| Category | Patterns |
|----------|----------|
| `workflows/` | tdd-workflow, trunk-based-development |
| `architecture/` | hexagonal-architecture |
| `tooling/` | uv-package-manager, pydantic-patterns, pytest-patterns |

---

## Subagent Orchestration

### Level 0: Direct Tools (< 5 seconds)
```bash
Read file              # Direct Read tool
Grep pattern          # Direct Grep tool
```

### Level 1: Single Subagent (< 60 seconds)
```yaml
Task: "Find authentication patterns"
Agent: code-explorer
```

### Level 2: Sequential Pipeline (< 180 seconds)
```yaml
Pipeline:
  1. code-explorer → understand patterns
  2. code-architect → design blueprint
  3. implementer → implement with tests
  4. code-reviewer → review quality
```

### Level 3: Parallel Execution (< 90 seconds)
```yaml
Parallel:
  - code-explorer(module=auth)
  - code-explorer(module=billing)
Then: Synthesize results
```

### Level 4: Hierarchical Coordination (< 300 seconds)
```yaml
Flow:
  1. code-quality-coordinator discovers scope
  2. Spawns workers in parallel
  3. Aggregates results
```

---

## Two Pillars Always Active

```yaml
learning:
  - iterate (small batches)
  - feedback (fast at all levels)
  - experiment (hypothesis-driven)
  - measure (DORA metrics)

complexity:
  - separate_concerns (essential vs accidental)
  - modularize (clear boundaries)
  - maintain_cohesion (related together)
  - minimize_coupling (loose between modules)
```

---

## Tool Commands

```bash
# UV Package Manager
uv sync                           # Setup
uv run pytest tests/ -v           # Run tests
uv run ruff check src/            # Lint
uv run mypy src/                  # Type check

# TDD Cycle
uv run pytest tests/test_x.py::test_y -v   # Single test
uv run pytest --cov=src           # Coverage
```

---

## Directory Structure

```
Unified_System_Core/
├── .claude/
│   └── agents/           # 16 AI agent definitions
├── skills/               # 18 programming skills (by pillar)
├── docs/
│   ├── agent-guidelines/ # Orchestration framework
│   └── patterns/         # Programming patterns
└── CLAUDE.md             # This file
```

---

**Based on**: "Modern Software Engineering" by Dave Farley
