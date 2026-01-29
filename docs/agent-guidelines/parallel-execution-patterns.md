# Parallel Execution Patterns

**Foundation**: Independent Work, Concurrent Execution, Efficient Aggregation

---

## Core Philosophy

> "The most scalable approach to software development is to distribute it."
> — Modern Software Engineering

**True parallelism requires true independence.** Agents must not share mutable state or depend on each other's results.

---

## When to Parallelize

### Independence Test

```yaml
task_analysis:
  question_1: "Can subtasks run without knowing others' results?"
    yes: Candidate for parallelism
    no: Must be sequential

  question_2: "Can subtasks share read-only context?"
    yes: Parallel with shared context
    no: Completely independent parallel

  question_3: "Can results be combined in any order?"
    yes: Ideal for parallelism (commutative)
    no: May need coordination

  question_4: "Is coordination overhead < 20% of task time?"
    yes: Parallelism beneficial
    no: Sequential may be faster
```

### Benefit Calculation

```yaml
formula: |
  Speedup = Sequential_Time / (Parallel_Time + Coordination_Overhead)

  Worthwhile if: Speedup > 1.3

example_1_good:
  sequential_time: 45s (3 tasks × 15s each)
  parallel_time: 15s (max of 3 parallel tasks)
  coordination: 3s (spawn + aggregate)
  speedup: 45 / (15 + 3) = 2.5× ✓

example_2_bad:
  sequential_time: 12s (3 tasks × 4s each)
  parallel_time: 4s (max of 3 parallel tasks)
  coordination: 5s (heavy coordination)
  speedup: 12 / (4 + 5) = 1.33× ⚠ (Barely worth it)
```

---

## Parallel Execution Patterns

### Pattern 1: Scatter-Gather (Independent Search)

**Use Case**: Search different scopes simultaneously

```yaml
pattern_name: "Scatter-Gather"
coupling: None (completely independent)

scatter_phase:
  - agent_1: Search API routes (scope: src/api/)
  - agent_2: Search services (scope: src/services/)
  - agent_3: Search models (scope: src/models/)

  independence: Each agent works on disjoint scope
  shared_state: None
  communication: None during execution

gather_phase:
  - Collect results from all agents
  - Merge/synthesize findings
  - Present unified view

timing:
  sequential: 3 × 15s = 45s
  parallel: max(15s) + 3s gather = 18s
  speedup: 2.5×
```

**Implementation**:
```python
# Spawn all agents in single message (parallel)
agents = [
    spawn_agent("search-api", scope="src/api/"),
    spawn_agent("search-services", scope="src/services/"),
    spawn_agent("search-models", scope="src/models/")
]

# Gather results
results = aggregate([a.results for a in agents])
```

### Pattern 2: Parallel Pipelines

**Use Case**: Multiple independent workflows

```yaml
pattern_name: "Parallel Pipelines"
coupling: None between pipelines

pipeline_1: "Implement Feature A"
  - Explorer → Architect → Implementer
  - Time: 90s

pipeline_2: "Implement Feature B"
  - Explorer → Architect → Implementer
  - Time: 85s

pipeline_3: "Implement Feature C"
  - Explorer → Architect → Implementer
  - Time: 95s

execution: All 3 pipelines run concurrently

timing:
  sequential: 90 + 85 + 95 = 270s
  parallel: max(90, 85, 95) + 5s coordination = 100s
  speedup: 2.7×
```

### Pattern 3: Fan-Out/Fan-In

**Use Case**: One input → many processors → one output

```yaml
pattern_name: "Fan-Out/Fan-In"

fan_out:
  input: "Refactor all service modules"
  decompose:
    - module_1: auth-service
    - module_2: billing-service
    - module_3: notification-service
    - module_4: user-service

  spawn: One refactoring agent per module (parallel)

parallel_work:
  - refactor_agent_1(auth-service) [45s]
  - refactor_agent_2(billing-service) [52s]
  - refactor_agent_3(notification-service) [38s]
  - refactor_agent_4(user-service) [50s]

fan_in:
  aggregate: Collect all refactored modules
  verify: Run cross-module tests
  report: Unified refactoring report

timing:
  sequential: 45 + 52 + 38 + 50 = 185s
  parallel: max(45, 52, 38, 50) + 10s fan-in = 62s
  speedup: 3.0×
```

### Pattern 4: Map-Reduce

**Use Case**: Apply operation to many items, reduce results

```yaml
pattern_name: "Map-Reduce"

map_phase:
  input: List of 20 files to analyze
  operation: "Extract dependencies"

  parallel_map:
    - agent_group_1: Files 1-5
    - agent_group_2: Files 6-10
    - agent_group_3: Files 11-15
    - agent_group_4: Files 16-20

  each_agent: Independent analysis

reduce_phase:
  collect: Dependency lists from all agents
  reduce: Build unified dependency graph
  analyze: Identify circular dependencies

timing:
  sequential: 20 files × 3s = 60s
  parallel: 4 groups × 5 files × 3s = 15s + 5s reduce = 20s
  speedup: 3.0×
```

---

## Parallelization Anti-Patterns

### 1. False Parallelism (Hidden Dependencies)

```yaml
❌ ANTI-PATTERN:
  appears_parallel:
    - agent_1: "Process data"
    - agent_2: "Also process data"

  reality:
    - Both read from shared mutable database
    - Race condition on writes
    - Results depend on execution order

✓ PATTERN:
  true_parallel:
    - agent_1: "Process partition 1 (read-only)"
    - agent_2: "Process partition 2 (read-only)"
    - Write results to separate outputs
    - Combine in deterministic fan-in phase
```

### 2. Over-Parallelization

```yaml
❌ ANTI-PATTERN:
  task: "Process 3 small files (2s each)"
  approach: Spawn 3 agents (5s overhead each)

  timing:
    sequential: 3 × 2s = 6s
    parallel: max(2s) + 3 × 5s overhead = 17s
    speedup: 0.35× (SLOWER!)

✓ PATTERN:
  task: "Process 3 small files"
  approach: Sequential processing (single agent)

  timing: 6s
  speedup: 1.0× (baseline, but faster than false parallel)
```

### 3. Premature Aggregation

```yaml
❌ ANTI-PATTERN:
  orchestrator_pattern:
    - Spawn agent_1
    - Wait for agent_1 result
    - Spawn agent_2 (uses agent_1 result)
    - Wait for agent_2 result
    - Spawn agent_3 (uses agent_2 result)

  problem: "Not actually parallel, just complex"

✓ PATTERN:
  true_parallel:
    - Spawn agent_1, agent_2, agent_3 simultaneously
    - Each works independently
    - Aggregate all results at end
```

### 4. Chatty Coordination

```yaml
❌ ANTI-PATTERN:
  parallel_agents_with_coordination:
    agent_1: "Status update every 5s"
    agent_2: "Status update every 5s"
    agent_3: "Status update every 5s"
    orchestrator: "Acknowledge each update"

  overhead: 60+ messages for 60s of work

✓ PATTERN:
  fire_and_gather:
    agents: "Work silently, report at end"
    orchestrator: "Collect final results only"
    overhead: 3 messages total (start + result)
```

---

## Synchronization Strategies

### Strategy 1: No Synchronization (Best)

```yaml
use_case: "Completely independent work"

approach:
  - Spawn all agents
  - Each works autonomously
  - Collect results when all done
  - No inter-agent communication

benefit: Maximum parallelism, zero overhead
```

### Strategy 2: Barrier Synchronization

```yaml
use_case: "Phase-based execution"

approach:
  phase_1:
    - All agents explore (parallel)
    - BARRIER: Wait for all to complete

  phase_2:
    - All agents implement based on exploration (parallel)
    - BARRIER: Wait for all to complete

  phase_3:
    - Single reviewer checks all implementations

benefit: Phases can parallelize, dependencies respected
```

### Strategy 3: Partial Order

```yaml
use_case: "Some dependencies, some independence"

dependency_graph:
  agent_A: No dependencies (start immediately)
  agent_B: No dependencies (start immediately)
  agent_C: Depends on A
  agent_D: Depends on A
  agent_E: Depends on B and C

execution_order:
  time_0: Start A, B (parallel)
  time_15: A completes → Start C, D (parallel)
  time_20: B completes
  time_30: C completes
  time_32: D completes, B complete → Start E

benefit: Maximum parallelism given constraints
```

---

## Aggregation Patterns

### Pattern 1: Simple Concatenation

```yaml
use_case: "Independent lists to merge"

agents_return:
  agent_1: [file_a, file_b, file_c]
  agent_2: [file_d, file_e]
  agent_3: [file_f, file_g, file_h]

aggregation:
  result: [file_a, file_b, ..., file_h]
  time: < 1s (simple append)
```

### Pattern 2: Set Union/Intersection

```yaml
use_case: "Finding common elements"

agents_return:
  agent_1: {pattern_A, pattern_B, pattern_C}
  agent_2: {pattern_B, pattern_D}
  agent_3: {pattern_C, pattern_D, pattern_E}

aggregation_union:
  result: {pattern_A, B, C, D, E}
  time: < 1s

aggregation_intersection:
  result: {} (no common patterns in all 3)
  time: < 1s
```

### Pattern 3: Synthesis/Merge

```yaml
use_case: "Combining insights"

agents_return:
  agent_1: "API uses REST pattern"
  agent_2: "Database uses SQLAlchemy ORM"
  agent_3: "Tests use pytest fixtures"

aggregation:
  synthesize: |
    Architecture Analysis:
    - API Layer: REST (FastAPI)
    - Data Layer: SQLAlchemy ORM
    - Test Strategy: pytest with fixtures
    - Recommendation: Follow existing patterns

  time: 3-5s (requires reasoning)
```

---

## Parallel Execution Metrics

### Efficiency Metrics

```yaml
parallelism_factor:
  formula: Sequential_Time / Parallel_Time
  ideal: Number of parallel agents
  typical: 0.7 × Number of agents (due to overhead)

  example:
    sequential: 90s
    parallel: 35s (3 agents)
    factor: 90/35 = 2.57×
    efficiency: 2.57 / 3 = 85.7%

coordination_overhead:
  formula: (Parallel_Time - Longest_Agent_Time) / Parallel_Time
  target: < 20%
  warning: > 30%

  example:
    parallel_time: 35s
    longest_agent: 30s
    overhead: (35-30)/35 = 14.3% ✓

resource_utilization:
  formula: Sum(Agent_Active_Time) / (Num_Agents × Parallel_Time)
  target: > 75%
  problem_if_low: "Agents waiting unnecessarily"
```

---

## Practical Guidelines

### When to Use Parallel Execution:
```yaml
checklist:
  - [ ] Tasks are truly independent
  - [ ] No shared mutable state
  - [ ] Task duration > 15s each
  - [ ] Number of tasks ≥ 2
  - [ ] Coordination overhead < 20%
  - [ ] Results can be combined
```

### Parallelization Decision Tree:
```
Task Analysis:
  │
  ├─ Task duration < 10s?
  │  └─ NO parallel (overhead too high)
  │
  ├─ Subtasks have dependencies?
  │  └─ YES → Use partial order or sequential
  │  └─ NO → Can parallelize
  │
  ├─ Coordination overhead > 20% of task time?
  │  └─ YES → Sequential may be faster
  │  └─ NO → Parallelize
  │
  └─ Number of subtasks × subtask_time > 30s?
     └─ YES → Parallelize
     └─ NO → Sequential fine
```

---

## Examples from Global1SIM

### Example 1: Parallel Feature Implementation

```yaml
task: "Implement 3 independent features"

parallel_approach:
  feature_a: "Subscriber activation"
    agents: [explorer, architect, implementer]
    time: 85s

  feature_b: "Billing integration"
    agents: [explorer, architect, implementer]
    time: 95s

  feature_c: "Notification system"
    agents: [explorer, architect, implementer]
    time: 90s

  execution: All 3 workflows run in parallel

timing:
  sequential: 85 + 95 + 90 = 270s
  parallel: max(85, 95, 90) + 10s = 105s
  speedup: 2.57×
```

### Example 2: Comprehensive Code Analysis

```yaml
task: "Analyze hexagonal architecture compliance"

parallel_decomposition:
  domain_analysis:
    agent: "Analyze src/domain/**"
    time: 20s

  ports_analysis:
    agent: "Analyze src/ports/**"
    time: 15s

  adapters_analysis:
    agent: "Analyze src/adapters/**"
    time: 18s

  dependency_check:
    agent: "Check dependency violations"
    time: 22s

  execution: All 4 agents run in parallel

timing:
  sequential: 20 + 15 + 18 + 22 = 75s
  parallel: max(20, 15, 18, 22) + 5s = 27s
  speedup: 2.78×
```

---

## References

- **Modern Software Engineering** by Dave Farley
  - Chapter 9: Modularity (independence for parallelism)
  - Chapter 13: Coupling (minimizing for concurrency)
  - Part 2: Optimize for Learning (feedback in parallel systems)

- **Related Guidelines**:
  - `orchestration-principles.md`: Patterns for coordinating parallel agents
  - `velocity-principles.md`: Speed through parallelism
  - `context-management.md`: Shared context in parallel execution
