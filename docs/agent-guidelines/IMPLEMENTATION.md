# Orchestration Implementation Guide

**How to realize agent velocity and orchestration using agents, subagents, and skills**

---

## System Architecture

### Three-Layer Model

```yaml
layer_1_main_agent:
  component: "Claude (main conversation)"
  role: "Orchestrator and user interface"
  tools: [Task, Read, Write, Edit, Bash, Grep, Glob]
  spawns: Subagents via Task tool

layer_2_subagents:
  location: ".claude/agents/**/*.md"
  role: "Specialized capabilities"
  examples:
    - tdd-cycle-driver
    - hexagonal-architecture-guardian
    - code-explorer
    - code-reviewer
  routes_to: Skills

layer_3_skills:
  location: "agent2/skills/**/"
  role: "Reusable workflows and patterns"
  examples:
    - iterative-development
    - feedback-driven-design
    - separation-of-concerns-enforcer
    - python-hexagonal-development
  composes: Multiple skills can work together
```

---

## How Orchestration Works

### Pattern 1: Direct Tool Usage (No Agent Needed)

**When**: Simple, fast operations (< 5s)

```yaml
example: "Read a specific file"
approach: Main agent uses Read tool directly
time: 1-2s
no_agent_needed: Task is trivial
```

**Implementation**:
```
User: "Show me src/config.ts"
Main Agent: [Uses Read tool directly]
  → Result in 1-2s
```

**Guideline Reference**: [Velocity Principles - Tool Selection](./velocity-principles.md#tool-selection)

---

### Pattern 2: Single Subagent Execution

**When**: Specialized task requiring expertise (< 60s)

```yaml
example: "Drive TDD cycle for new feature"
approach: Spawn tdd-cycle-driver subagent
time: 50-90s
agent_value: Specialized workflow + skill routing
```

**Implementation**:
```
User: "Implement subscriber activation with TDD"

Main Agent:
  1. Recognize TDD requirement
  2. Spawn tdd-cycle-driver subagent

Subagent (tdd-cycle-driver):
  3. Routes to `iterative-development` skill (RED phase)
  4. Routes to `feedback-driven-design` skill (test execution)
  5. Routes to `pytest-conventions` subskill (structure)
  6. Writes failing test
  7. Implements minimal code
  8. Routes to `refactoring-mastery` skill (REFACTOR phase)
  9. Returns complete TDD cycle results

Main Agent:
  10. Reports results to user
```

**File Structure**:
```
.claude/agents/testing/tdd-cycle-driver.md
  ↓ routes to
agent2/skills/iterative-development/
agent2/skills/feedback-driven-design/
agent2/skills/pytest-conventions/  (subskill)
```

**Guideline Reference**: [Agent Capability Patterns - Implementation Agents](./agent-capability-patterns.md#3-implementation-agents-write-code)

---

### Pattern 3: Sequential Agent Chain (Pipeline)

**When**: Multi-phase work with dependencies

```yaml
example: "Implement feature following architecture"
phases:
  1. exploration (code-explorer)
  2. design (code-architect)
  3. implementation (implementer)
  4. review (code-reviewer)
time: 120-180s
orchestration: Main agent coordinates sequence
```

**Implementation**:
```
User: "Implement new billing integration"

Main Agent (Orchestrator):
  Phase 1 - Exploration:
    1. Spawn code-explorer subagent
    2. Exploration results → patterns.md

  Phase 2 - Architecture:
    3. Spawn code-architect subagent
    4. Input: patterns.md + feature requirements
    5. Architecture results → blueprint.md

  Phase 3 - Implementation:
    6. Spawn implementer subagent
    7. Input: blueprint.md
    8. Implementation results → code_changes

  Phase 4 - Review:
    9. Spawn code-reviewer subagent
    10. Input: code_changes
    11. Review results → feedback
    12. Report complete workflow to user
```

**Agent Definitions**:
```
.claude/agents/discovery/code-explorer.md
.claude/agents/architecture/code-architect.md
.claude/agents/implementation/implementer.md
.claude/agents/review/code-reviewer.md
```

**Guideline Reference**: [Orchestration Principles - Pattern 1: Pipeline](./orchestration-principles.md#pattern-1-pipeline-sequential-flow)

---

### Pattern 4: Parallel Execution (Scatter-Gather)

**When**: Independent subtasks can run concurrently

```yaml
example: "Analyze codebase architecture"
parallel_work:
  - Analyze API routes (agent_1)
  - Analyze domain logic (agent_2)
  - Analyze database layer (agent_3)
time: 25s (vs 65s sequential)
speedup: 2.6×
```

**Implementation**:
```
User: "Analyze hexagonal architecture compliance"

Main Agent (Orchestrator):
  Scatter Phase (single message, parallel spawning):
    1. Spawn 3 agents simultaneously:
       - ports-analyzer (scope: src/ports/**)
       - adapters-analyzer (scope: src/adapters/**)
       - domain-analyzer (scope: src/domain/**)

  [Agents work independently, no communication]

  Gather Phase:
    2. Collect all results
    3. Synthesize findings
    4. Report unified analysis
```

**Key Implementation Detail**:
```python
# Main agent sends ONE message with multiple Task calls
Task(
  subagent_type="ports-analyzer",
  prompt="Analyze src/ports/ for interface compliance"
)
Task(
  subagent_type="adapters-analyzer",
  prompt="Analyze src/adapters/ for dependency direction"
)
Task(
  subagent_type="domain-analyzer",
  prompt="Analyze src/domain/ for purity"
)
# All spawn and execute in parallel
```

**Guideline Reference**: [Parallel Execution Patterns - Scatter-Gather](./parallel-execution-patterns.md#pattern-1-scatter-gather-independent-search)

---

### Pattern 5: Hierarchical Orchestration (Coordinator-Worker)

**When**: Dynamic workload distribution

```yaml
example: "Refactor multiple modules"
coordinator: hexagonal-architecture-guardian
workers: module-refactor-agent (spawned per module)
time: Depends on module count
pattern: Coordinator discovers work, spawns workers
```

**Implementation**:
```
User: "Refactor all services to follow hexagonal architecture"

Main Agent:
  1. Spawn hexagonal-architecture-guardian (coordinator)

Coordinator (hexagonal-architecture-guardian):
  2. Routes to `modularity-architect` skill (analyze structure)
  3. Discovers: 5 services need refactoring
  4. Prioritizes by complexity
  5. Spawns workers:
     - refactor-worker-1 (auth service)
     - refactor-worker-2 (billing service)
     - refactor-worker-3 (notification service)
     - refactor-worker-4 (user service)
     - refactor-worker-5 (reporting service)

  [Workers execute independently]

  6. Aggregates results
  7. Routes to `empirical-measurement` skill (track metrics)
  8. Returns unified report

Main Agent:
  9. Reports to user
```

**Guideline Reference**: [Orchestration Principles - Pattern 3: Coordinator-Worker](./orchestration-principles.md#pattern-3-coordinator-worker)

---

## Creating New Agents

### Agent Template Structure

```markdown
---
name: agent-name
description: When to use this agent with examples
color: blue|red|green|yellow
---

You are an elite [Agent Role] with expertise in [domains]...

## Skills Integration and Routing

This agent routes to these skills:

### Primary Skills:
- **`skill-name`** - Purpose
- **`another-skill`** - Purpose

### Supporting Skills:
- **`helper-skill`** - Purpose

### Skill Routing Decision Tree:
```
Task Type?
├─ Condition A → Route to: `skill-a`
├─ Condition B → Route to: `skill-b`
└─ Condition C → Route to: `skill-c`
```

When performing [agent's primary function], you will:

1. **Phase 1**: Description with skill routing
2. **Phase 2**: Description with skill routing
3. **Phase 3**: Description with skill routing

[Agent-specific implementation details]

## Project-Specific Standards

[Code examples, commands, patterns]
```

### Applying Guidelines to Agent Design

```yaml
velocity_principles:
  time_budget: < 60s for primary task
  feedback: Emit progress every 15-20s
  validation: Fail fast (< 1s input checks)
  tools: Use simplest tool that works

capability_patterns:
  responsibility: ONE clear primary capability
  tools_allowed: Specific to capability category
  no_capability_creep: Reject scope expansion

context_management:
  load_progressively: Don't read everything upfront
  targeted_reads: Use offset+limit for large files
  handoff_strategy: Compress summaries for next agent

feedback_optimization:
  early_validation: Check inputs immediately
  incremental_output: Report as you go
  fail_fast: Don't waste time on invalid inputs
```

**Example Agent Definition**:
```markdown
---
name: api-endpoint-discoverer
description: Discovers and catalogs REST API endpoints in codebase
color: green
---

## Skills Integration
- **`separation-of-concerns-enforcer`** - Identify route handlers
- **`modularity-architect`** - Understand API structure

## Implementation

When discovering endpoints, you will:

1. **Quick Discovery** (< 10s)
   - Glob "**/*route*.{ts,js,py}"
   - Grep for route decorators (@app.get, @router.post)
   - Routes to `feedback-driven-design` (report findings)

2. **Detailed Analysis** (< 15s)
   - Read identified files (targeted sections)
   - Extract endpoint paths, methods, handlers
   - Routes to `separation-of-concerns-enforcer` (check violations)

3. **Reporting** (< 5s)
   - Structured output (JSON/Markdown)
   - Categorized by module
   - Flag any architecture issues

**Time Budget**: 30s total
**Success Criteria**: Complete endpoint catalog
```

---

## Skill Composition

### How Skills Work Together

```yaml
skill_integration_example:
  scenario: "TDD cycle for new feature"

  skill_flow:
    1. iterative-development:
        phase: "RED"
        action: "Break feature into smallest testable behavior"
        output: "Single focused test case"

    2. feedback-driven-design:
        phase: "RED"
        action: "Optimize test execution speed"
        validates: "Test runs in < 100ms"

    3. pytest-conventions:
        phase: "RED"
        action: "Apply project test structure"
        ensures: "Arrange-Act-Assert pattern"

    4. separation-of-concerns-enforcer:
        phase: "GREEN"
        action: "Guide implementation structure"
        prevents: "Mixing business logic with infrastructure"

    5. refactoring-mastery:
        phase: "REFACTOR"
        action: "Improve design in tiny steps"
        maintains: "Tests stay green throughout"

    6. empirical-measurement:
        phase: "COMPLETE"
        action: "Track cycle time metrics"
        improves: "Identify bottlenecks for next cycle"
```

### Creating Skill-Based Agents

**Pattern**: Agent = Workflow Orchestrator + Skill Router

```yaml
agent_design:
  agent_role: "TDD Cycle Driver"

  workflow_phases:
    - RED: Write failing test
    - GREEN: Minimal implementation
    - REFACTOR: Improve design

  skill_routing:
    RED:
      primary: iterative-development (small batch)
      supporting: [feedback-driven-design, pytest-conventions]

    GREEN:
      primary: separation-of-concerns-enforcer (clean structure)
      supporting: [python-hexagonal-development]

    REFACTOR:
      primary: refactoring-mastery (tiny safe steps)
      supporting: [feedback-driven-design, high-performance-simplicity]

  agent_value_add:
    - Knows when to apply which skill
    - Maintains workflow discipline
    - Provides project-specific guidance
    - Integrates multiple skills seamlessly
```

---

## Practical Examples

### Example 1: Simple Task (No Agent)

```yaml
task: "Find all API endpoints in src/api/"

solution: Direct tool usage
  Main Agent:
    1. Grep "(@app\\.|@router\\.)" in src/api/ (3s)
    2. Read key files if needed (5s)
    3. Report findings (1s)

  total_time: 9s
  no_agent_needed: Task too simple for agent overhead
```

### Example 2: TDD Cycle (Single Agent)

```yaml
task: "Implement subscriber activation with TDD"

solution: tdd-cycle-driver agent
  Main Agent:
    1. Spawn tdd-cycle-driver (2s overhead)

  tdd-cycle-driver:
    2. RED Phase (20s)
       - Route to iterative-development skill
       - Route to pytest-conventions subskill
       - Write failing test

    3. GREEN Phase (30s)
       - Route to separation-of-concerns-enforcer
       - Implement minimal code

    4. REFACTOR Phase (25s)
       - Route to refactoring-mastery skill
       - Improve design, tests stay green

    5. Return results (2s)

  total_time: 79s
  agent_value: Enforces TDD discipline, skill integration
```

### Example 3: Feature Implementation (Sequential Chain)

```yaml
task: "Implement new eSIM provisioning feature"

solution: Multi-agent pipeline
  Main Agent (orchestrates):
    1. Spawn code-explorer (20s)
       Output: existing_patterns.md

    2. Spawn code-architect (35s)
       Input: existing_patterns.md
       Output: architecture_blueprint.md

    3. Spawn implementer (75s)
       Input: architecture_blueprint.md
       Output: code_changes

    4. Spawn code-reviewer (30s)
       Input: code_changes
       Output: review_feedback

  total_time: 160s
  parallelization_opportunity: None (sequential dependencies)
```

### Example 4: Architecture Analysis (Parallel)

```yaml
task: "Comprehensive hexagonal architecture audit"

solution: Scatter-gather pattern
  Main Agent (orchestrates):
    Scatter (single message, parallel spawn):
      1. Spawn domain-analyzer (20s)
      2. Spawn ports-analyzer (15s)
      3. Spawn adapters-analyzer (18s)
      4. Spawn dependency-checker (22s)

    [All execute simultaneously]

    Gather:
      5. Synthesize results (5s)
      6. Identify violations
      7. Generate report

  total_time: 27s (vs 75s sequential)
  speedup: 2.78×
```

### Example 5: Multi-Module Refactoring (Coordinator)

```yaml
task: "Refactor all services for hexagonal compliance"

solution: Hierarchical orchestration
  Main Agent:
    1. Spawn hexagonal-architecture-guardian (coordinator)

  Coordinator:
    2. Discover modules needing work (10s)
       - 5 services identified
       - Prioritized by complexity

    3. Spawn workers (parallel):
       - refactor-agent-1: auth-service (45s)
       - refactor-agent-2: billing-service (52s)
       - refactor-agent-3: notification-service (38s)
       - refactor-agent-4: user-service (50s)
       - refactor-agent-5: reporting-service (48s)

    4. Aggregate results (10s)
    5. Run integration tests (15s)
    6. Report unified results

  total_time: 87s (vs 253s sequential)
  speedup: 2.9×
```

---

## Decision Trees for Implementation

### Should I Create a New Agent?

```
Task Analysis:
  │
  ├─ Can be done with 1-2 tool calls?
  │  └─ NO AGENT - Use tools directly
  │
  ├─ Existing agent covers this?
  │  └─ USE EXISTING - Don't duplicate
  │
  ├─ Requires specialized workflow (> 3 steps)?
  │  └─ CREATE AGENT - With skill routing
  │
  └─ Would be reused for similar tasks?
     └─ CREATE AGENT - Reusable capability
```

### How Should I Orchestrate?

```
Task Structure:
  │
  ├─ Single agent sufficient?
  │  └─ SPAWN ONE AGENT
  │
  ├─ Sequential phases with dependencies?
  │  └─ PIPELINE PATTERN
  │     Main agent spawns agents in sequence
  │
  ├─ Independent parallel subtasks?
  │  └─ SCATTER-GATHER PATTERN
  │     Main agent spawns all in single message
  │
  ├─ Dynamic workload distribution?
  │  └─ COORDINATOR-WORKER PATTERN
  │     Spawn coordinator agent
  │     Coordinator spawns workers
  │
  └─ Reactive/event-based workflow?
     └─ EVENT-DRIVEN PATTERN
        Agents trigger subsequent agents
```

### Which Skills Should Agent Use?

```
Agent Purpose:
  │
  ├─ Discovery/Exploration?
  │  └─ Skills: separation-of-concerns-enforcer, modularity-architect
  │
  ├─ Architecture/Design?
  │  └─ Skills: modularity-architect, python-hexagonal-development,
  │               abstraction-patterns, cohesion-coach
  │
  ├─ Implementation?
  │  └─ Skills: iterative-development, separation-of-concerns-enforcer,
  │               refactoring-mastery, feedback-driven-design
  │
  ├─ Review/Quality?
  │  └─ Skills: coupling-minimizer, cohesion-coach,
  │               high-performance-simplicity
  │
  └─ Execution/Testing?
     └─ Skills: feedback-driven-design, empirical-measurement,
                 python-test-strategy
```

---

## File Organization

### Recommended Structure

```
.claude/
└── agents/
    ├── discovery/
    │   ├── code-explorer.md
    │   ├── api-discoverer.md
    │   └── dependency-mapper.md
    │
    ├── architecture/
    │   ├── code-architect.md
    │   ├── hexagonal-architecture-guardian.md
    │   └── performance-optimizer.md
    │
    ├── implementation/
    │   ├── feature-implementer.md
    │   ├── bug-fixer.md
    │   └── refactor-agent.md
    │
    ├── review/
    │   ├── code-reviewer.md
    │   ├── security-reviewer.md
    │   └── architecture-reviewer.md
    │
    ├── testing/
    │   ├── tdd-cycle-driver.md
    │   ├── test-runner.md
    │   └── coverage-analyzer.md
    │
    └── workflow/
        ├── feature-dev-orchestrator.md
        └── feedback-loop-optimizer.md

agent2/
└── skills/
    ├── README.md
    ├── MODERN_SOFTWARE_ENGINEERING_SKILLS.md
    │
    ├── iterative-development/
    │   └── SKILL.md
    │
    ├── feedback-driven-design/
    │   └── SKILL.md
    │
    ├── separation-of-concerns-enforcer/
    │   └── SKILL.md
    │
    └── [other skills...]

docs/
└── agent-guidelines/
    ├── README.md
    ├── velocity-principles.md
    ├── orchestration-principles.md
    ├── agent-capability-patterns.md
    ├── context-management.md
    ├── feedback-optimization.md
    ├── parallel-execution-patterns.md
    ├── orchestration-metrics.md
    └── IMPLEMENTATION.md (this file)
```

---

## Metrics Collection

### Instrumentation Points

```yaml
agent_lifecycle_hooks:
  on_spawn:
    log: {timestamp, agent_type, task_description}
    metric: spawn_count++

  on_skill_route:
    log: {agent, skill, phase}
    metric: skill_usage[skill]++

  on_tool_call:
    log: {tool, parameters, agent}
    metric: tool_latency[tool].append(duration)

  on_completion:
    log: {duration, success, token_usage}
    metrics:
      - completion_time.append(duration)
      - success_rate.update(success)
      - token_efficiency.append(tokens/complexity)

  on_failure:
    log: {error, agent, phase}
    metric: failure_rate[agent]++
```

### Dashboard Visualization

```yaml
real_time_dashboard:
  widgets:
    active_agents: Current agents running
    queue_depth: Tasks waiting
    success_rate: Last hour %
    avg_completion: p50, p90, p99

  alerts:
    - success_rate < 80%: WARNING
    - avg_completion > 90s: WARNING
    - token_usage > 100k/hour: INFO
```

---

## Best Practices

### DO:
- ✓ Use tools directly for simple tasks (< 5s)
- ✓ Create specialized agents for reusable workflows
- ✓ Route agents to appropriate skills
- ✓ Spawn agents in parallel when independent
- ✓ Set clear time budgets per agent
- ✓ Emit progress updates every 15-20s
- ✓ Fail fast on invalid inputs (< 1s validation)
- ✓ Compress context in agent handoffs
- ✓ Measure and track performance metrics

### DON'T:
- ✗ Spawn agents for trivial operations
- ✗ Create duplicate agent capabilities
- ✗ Mix multiple responsibilities in one agent
- ✗ Run sequential when parallel is possible
- ✗ Load full context upfront
- ✗ Silent execution (no progress updates)
- ✗ Ignore negative feedback signals
- ✗ Over-coordinate (chatty agents)

---

## Next Steps

1. **Review Existing Agents**: Check `.claude/agents/` for current capabilities
2. **Study Skills**: Read `agent2/skills/README.md` for available patterns
3. **Apply Guidelines**: Use templates and patterns from this guide
4. **Measure Performance**: Implement metrics from orchestration-metrics.md
5. **Iterate**: Continuously improve based on data

---

## References

- **Agent Guidelines**: `docs/agent-guidelines/README.md`
- **Skills Framework**: `agent2/skills/README.md`
- **Project Guide**: `CLAUDE.md`
- **Modern SE Book**: `/mnt/src/docs/Modern Software Engineering/`

---

**Remember**: Agents orchestrate workflows, Skills provide patterns, Main agent coordinates everything. Keep it simple, measure everything, improve continuously.
