# Modern Software Engineering Skills & Agent Framework

**Based on**: "Modern Software Engineering: Doing What Works to Build Better Software Faster" by David Farley

> "Software engineering is the application of an empirical, scientific approach to finding efficient, economic solutions to practical problems in software."

---

## Overview

This framework provides:
- **18 Programming Skills** - Based on Modern Software Engineering principles
- **16 AI Agents** - Specialized subagents for development tasks
- **Orchestration Framework** - Patterns for coordinating agents
- **Programming Patterns** - Workflows, architecture, and tooling

---

## Quick Navigation

### Skills (./skills/)

| When You Need To... | Use This Skill |
|---------------------|----------------|
| Start new work | [iterative-development](learning-pillar/iterative-development/) |
| Speed up tests | [feedback-driven-design](learning-pillar/feedback-driven-design/) |
| Handle uncertainty | [experimental-workflow](learning-pillar/experimental-workflow/) |
| Design code | [separation-of-concerns-enforcer](complexity-pillar/separation-of-concerns-enforcer/) |
| Design systems | [modularity-architect](complexity-pillar/modularity-architect/) |
| Clarify code | [cohesion-coach](complexity-pillar/cohesion-coach/) |
| Create interfaces | [abstraction-patterns](complexity-pillar/abstraction-patterns/) |
| Manage dependencies | [coupling-minimizer](complexity-pillar/coupling-minimizer/) |
| Refactor safely | [refactoring-mastery](supporting-skills/refactoring-mastery/) |
| Optimize performance | [high-performance-simplicity](supporting-skills/high-performance-simplicity/) |
| Set up CI/CD | [deployment-pipeline-designer](learning-pillar/deployment-pipeline-designer/) |
| Track improvement | [empirical-measurement](learning-pillar/empirical-measurement/) |

### Agents (./agents/)

| Category | Agents |
|----------|--------|
| Discovery | code-explorer, api-discoverer, dependency-mapper |
| Architecture | code-architect, hexagonal-architecture-guardian, performance-optimizer |
| Implementation | implementer, bug-fixer |
| Review | code-reviewer |
| Testing | tdd-cycle-driver |
| Workflow | feedback-loop-optimizer |
| Coordination | code-quality-coordinator, devops-workflow-orchestrator |
| DevOps | security-hardening-worker, performance-optimization-worker |
| UI/UX | senior-ui-ux-designer |

### Orchestration (./orchestration/)

- **Guidelines** - Core principles for agent velocity and coordination
- **Implementation** - Patterns for single agents, pipelines, parallel execution
- **Templates** - Templates for creating new agents
- **Test Results** - Validated performance metrics

### Patterns (./patterns/)

- **Workflows** - TDD, trunk-based development, experimental features
- **Architecture** - Hexagonal architecture, separation of concerns
- **Tooling** - UV package manager, Pydantic, pytest

---

## The Two Foundational Pillars

### Pillar 1: Optimize for Learning

Software development is discovery. To succeed, we must become **experts at learning**.

**Skills:**
- `iterative-development` - Work in small batches
- `feedback-driven-design` - Fast feedback at all levels
- `experimental-workflow` - Treat work as experiments
- `empirical-measurement` - DORA metrics

### Pillar 2: Optimize for Managing Complexity

Systems are complex. To succeed, we must become **experts at managing complexity**.

**Skills:**
- `separation-of-concerns-enforcer` - One thing per unit
- `modularity-architect` - Clear boundaries
- `cohesion-coach` - Related together
- `abstraction-patterns` - Information hiding
- `coupling-minimizer` - Minimize dependencies

---

## Success Metrics (Elite Performers)

| Metric | Target |
|--------|--------|
| Deploy frequency | Multiple times/day |
| Lead time | < 1 hour |
| MTTR | < 1 hour |
| Change failure rate | < 15% |

### Development Cycle Times

| Phase | Target |
|-------|--------|
| Unit test | < 100ms each |
| Full unit suite | < 10 seconds |
| CI pipeline | < 10 minutes |
| Deployment | < 10 minutes |

---

## Getting Started

1. **Start with learning skills**:
   - `iterative-development` - Foundation for everything
   - `feedback-driven-design` - Fast feedback loops

2. **Add complexity management**:
   - `separation-of-concerns-enforcer` - Primary design tool
   - `modularity-architect` - System organization

3. **Use agents for specialized tasks**:
   - `code-explorer` - Understand codebases
   - `tdd-cycle-driver` - Drive TDD workflow
   - `code-reviewer` - Quality feedback

4. **Orchestrate for speed**:
   - See `orchestration/` for coordination patterns
   - Parallel execution for 1.5-2x speedups

---

## Directory Structure

```
skills/
├── learning-pillar/          # Learning optimization skills (5)
├── complexity-pillar/        # Complexity management skills (5)
├── supporting-skills/        # Supporting practices (4)
├── project-skills/           # Project-specific skills (2)
└── architecture-skills/      # Architecture patterns (2)

agents/
├── discovery/                # Code exploration agents (3)
├── architecture/             # Design agents (3)
├── implementation/           # Coding agents (2)
├── review/                   # Review agents (1)
├── testing/                  # Testing agents (1)
├── workflow/                 # Workflow agents (1)
├── coordination/             # Coordination agents (2)
├── devops/                   # DevOps workers (2)
└── ui-ux/                    # UI/UX agents (1)

orchestration/
├── guidelines/               # Core principles (7 docs)
├── implementation/           # Patterns (5 docs)
├── templates/                # Agent templates
└── test-results/             # Validated metrics

patterns/
├── workflows/                # TDD, CI, experiments
├── architecture/             # Hexagonal, separation
└── tooling/                  # UV, Pydantic, pytest
```

---

## Key Principles

> "If the practices that we choose to identify as 'engineering' don't allow us to make better software faster, then they don't qualify as engineering!"

> "Without feedback, there is no opportunity to learn."

> "Separation of concerns is the most powerful principle of design."

> "TDD applies a pressure to create code that is objectively 'higher quality.'"

> "High-performance systems demand simple, well-designed code."

---

## License

MIT License - See LICENSE file

---

## Further Reading

- **Book**: "Modern Software Engineering" by David Farley
- **Orchestration**: See `orchestration/README.md` for agent coordination
- **Patterns**: See `patterns/README.md` for workflows

---

**Remember**: Engineering is about applying scientific thinking to build better software faster.
