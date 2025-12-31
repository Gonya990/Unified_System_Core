# AI Agent Framework

**Total Agents**: 16 specialized agents for software development

---

## Agent Categories

### Discovery (3 agents)
| Agent | Purpose |
|-------|---------|
| `code-explorer` | Find patterns, structures, relationships |
| `api-discoverer` | Discover API endpoints and contracts |
| `dependency-mapper` | Map dependencies between modules |

### Architecture (3 agents)
| Agent | Purpose |
|-------|---------|
| `code-architect` | Design blueprints, architecture decisions |
| `hexagonal-architecture-guardian` | Enforce hexagonal architecture |
| `performance-optimizer` | Identify and fix performance issues |

### Implementation (2 agents)
| Agent | Purpose |
|-------|---------|
| `implementer` | Implement features with tests |
| `bug-fixer` | Fix bugs following TDD |

### Review (1 agent)
| Agent | Purpose |
|-------|---------|
| `code-reviewer` | Quality feedback, improvements |

### Testing (1 agent)
| Agent | Purpose |
|-------|---------|
| `tdd-cycle-driver` | Run RED-GREEN-REFACTOR cycle |

### Workflow (1 agent)
| Agent | Purpose |
|-------|---------|
| `feedback-loop-optimizer` | Optimize development workflow |

### Coordination (2 agents)
| Agent | Purpose |
|-------|---------|
| `code-quality-coordinator` | Multi-module quality improvements |
| `devops-workflow-orchestrator` | DevOps workflow orchestration |

### DevOps (2 agents)
| Agent | Purpose |
|-------|---------|
| `performance-optimization-worker` | Execute performance tasks |
| `security-hardening-worker` | Execute security tasks |

### UI/UX (1 agent)
| Agent | Purpose |
|-------|---------|
| `senior-ui-ux-designer` | Design UI/UX, implement interfaces |

---

## Orchestration Patterns

### Level 1: Single Agent (< 60s)
```yaml
Task: "Find authentication patterns"
Agent: code-explorer
```

### Level 2: Sequential Pipeline (< 180s)
```yaml
Pipeline:
  1. code-explorer → understand patterns
  2. code-architect → design blueprint
  3. implementer → implement with tests
  4. code-reviewer → review quality
```

### Level 3: Parallel Execution (< 90s)
```yaml
Parallel:
  - code-explorer(module=auth)
  - code-explorer(module=billing)
  - code-explorer(module=orders)
Then: Synthesize results
```

### Level 4: Hierarchical Coordination (< 300s)
```yaml
Flow:
  1. code-quality-coordinator discovers modules
  2. Spawns code-reviewer for each (parallel)
  3. Aggregates quality reports
```

---

## Quick Reference by Use Case

- **Exploring code?** → `code-explorer`
- **Designing architecture?** → `code-architect`
- **Implementing features?** → `implementer`, `tdd-cycle-driver`
- **Fixing bugs?** → `bug-fixer`
- **Reviewing code?** → `code-reviewer`
- **Performance issues?** → `performance-optimizer`
- **Multi-module work?** → `code-quality-coordinator`

---

## See Also

- `../orchestration/` - Agent orchestration framework
- `../skills/` - Programming skills
- `../patterns/` - Development patterns
