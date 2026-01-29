# Agent Orchestration Principles

**Foundation**: Minimize Coupling, Maximize Autonomy, Optimize Communication

---

## Core Philosophy

> "The most scalable approach to software development is to distribute it. Reduce the coupling and dependencies between teams and their products to the degree that each team can, independently, create, test, and deploy their work with no reference to another team."
> — Modern Software Engineering, Chapter 9

The same principles apply to agents. **Orchestration is not about control—it's about coordination with minimal coupling.**

---

## The Orchestration Hierarchy

### Level 0: Tool Usage (No Orchestration)
```yaml
context: Simple, direct task
pattern: Main agent → Tools → Result
example: "Read file X and summarize"
coordination: None needed
```

### Level 1: Sequential Agent Chain
```yaml
context: Task requires multiple specialized steps
pattern: Agent A → Agent B → Agent C
example: "Explore → Design → Implement"
coordination: Output of A feeds input of B
coupling: Medium (chain dependency)
```

### Level 2: Parallel Agent Execution
```yaml
context: Independent subtasks can run concurrently
pattern:
  ├─ Agent A
  ├─ Agent B
  └─ Agent C
  → Synthesize results
example: "Search 3 different codebases simultaneously"
coordination: Scatter-gather pattern
coupling: Low (no inter-agent dependencies)
```

### Level 3: Hierarchical Orchestration
```yaml
context: Complex task requiring orchestrator agent
pattern:
  Orchestrator
    ├─ Spawns Agent A
    ├─ Spawns Agent B (based on A's result)
    └─ Spawns Agent C (parallel with B)
coordination: Dynamic agent spawning
coupling: Managed through orchestrator
```

---

## Core Orchestration Patterns

### Pattern 1: Pipeline (Sequential Flow)

**When to Use**: Tasks have clear order dependency

```yaml
# Feature Implementation Pipeline
pipeline:
  1. code-explorer:
      input: Feature description
      output: Existing patterns understanding
      time: ~20s

  2. code-architect:
      input: Feature description + patterns
      output: Implementation blueprint
      time: ~30s

  3. implementer:
      input: Blueprint
      output: Code changes
      time: ~60s

  4. code-reviewer:
      input: Code changes
      output: Review feedback
      time: ~30s

total_time: ~140s (2.3 minutes)
parallelizable: No (strict dependencies)
```

**Coupling Management**:
```yaml
✓ GOOD - Loose Coupling:
  Agent A output: Structured data (JSON, clear schema)
  Agent B input: Accepts standardized format
  Interface: Well-defined contract

✗ BAD - Tight Coupling:
  Agent A output: Unstructured text
  Agent B input: Must parse A's specific output format
  Interface: Implicit, fragile
```

### Pattern 2: Scatter-Gather (Parallel Execution)

**When to Use**: Independent subtasks, results must be combined

```yaml
# Codebase Analysis
scatter_gather:
  scatter:
    - agent: "search-api-endpoints"
      scope: "src/api/**/*.ts"
      time: ~10s

    - agent: "search-database-models"
      scope: "src/models/**/*.ts"
      time: ~10s

    - agent: "search-business-logic"
      scope: "src/services/**/*.ts"
      time: ~10s

  gather:
    - Synthesize all results
    - Create unified architecture view
    - time: ~5s

total_time: ~15s (not 30s!)
speedup: 2x due to parallelism
```

**Key Principles**:
```yaml
independence:
  - Agents MUST NOT depend on each other's results
  - Agents MUST NOT share mutable state
  - Agents CAN work on different parts of system

aggregation:
  - Results must be combinable (commutative)
  - Order of completion doesn't matter
  - Partial results are acceptable
```

### Pattern 3: Coordinator-Worker

**When to Use**: Dynamic task distribution, unknown workload

```yaml
# Comprehensive Refactoring
coordinator:
  role: "Orchestrate refactoring across modules"

  discover_work:
    - Find all modules needing refactoring
    - Prioritize by complexity
    - Estimate effort

  distribute_work:
    - Spawn worker agent per module
    - Monitor progress
    - Collect results

  workers:
    - agent: "refactor-worker-1"
      module: "authentication"
      status: "complete"
      time: 45s

    - agent: "refactor-worker-2"
      module: "billing"
      status: "in_progress"
      time: 30s (so far)

    - agent: "refactor-worker-3"
      module: "notifications"
      status: "queued"

  aggregation:
    - Wait for all workers
    - Run cross-module tests
    - Report unified results
```

**Coordinator Responsibilities**:
1. **Discovery**: Understand full scope
2. **Decomposition**: Break into worker tasks
3. **Distribution**: Spawn appropriate workers
4. **Monitoring**: Track progress (without micromanaging)
5. **Aggregation**: Combine results
6. **Reporting**: Unified status to user

**Worker Responsibilities**:
1. **Execute**: Complete assigned task autonomously
2. **Report**: Clear success/failure status
3. **Isolate**: Don't interfere with other workers

### Pattern 4: Event-Driven Orchestration

**When to Use**: Reactive workflows, trigger-based coordination

```yaml
# Continuous TDD Cycle
events:
  on_test_written:
    trigger: "New test file detected"
    action: Spawn "implementation-agent"

  on_implementation_complete:
    trigger: "Code written"
    actions:
      - Spawn "test-runner-agent"
      - Spawn "lint-checker-agent"  # Parallel

  on_tests_passing:
    trigger: "All tests pass"
    action: Spawn "refactor-agent"

  on_refactor_complete:
    trigger: "Refactoring done"
    action: Run tests again (cycle continues)
```

---

## Coupling Management Strategies

### 1. Interface-Based Coupling (Preferred)

```yaml
✓ GOOD - Contract-Based:
  agent_a:
    output_contract:
      type: "ArchitectureAnalysis"
      fields:
        - patterns: List[str]
        - recommendations: List[str]
        - confidence: float

  agent_b:
    input_contract:
      accepts: "ArchitectureAnalysis"
      validates: Schema check before processing

benefit: Any agent producing valid output can replace Agent A
```

### 2. Message Passing (Loose Coupling)

```yaml
✓ GOOD - Decoupled Communication:
  agent_a:
    action: Write results to structured log
    notification: Emit "task_complete" event

  agent_b:
    trigger: Subscribe to "task_complete"
    action: Read structured log
    independence: Doesn't know about Agent A

benefit: Agents never directly reference each other
```

### 3. Shared Context (Acceptable with Constraints)

```yaml
⚠ ACCEPTABLE - Shared Read-Only State:
  shared_context:
    codebase_index: Read-only DeepContext index
    project_config: Read-only configuration
    domain_model: Read-only understanding

  agents:
    - All can read shared context
    - None can modify shared context
    - Each maintains own working memory

benefit: Avoids re-indexing, shared knowledge
constraint: Must be read-only (immutable)
```

### 4. Direct Dependencies (Avoid)

```yaml
✗ BAD - Tight Coupling:
  agent_a:
    code: |
      results = agent_b.execute_specific_method()
      # Directly calling another agent

problems:
  - Can't test Agent A without Agent B
  - Can't swap Agent B implementation
  - Breaks on Agent B changes
  - No clear interface
```

---

## Orchestration Anti-Patterns

### 1. The God Orchestrator
```yaml
❌ ANTI-PATTERN:
  orchestrator:
    responsibilities:
      - Decides every detail for workers
      - Micromanages worker execution
      - Workers are just "dumb" tool callers

  problems:
    - Bottleneck (everything waits for orchestrator)
    - Single point of failure
    - Can't scale
    - Workers have no autonomy

✓ BETTER:
  orchestrator:
    - Defines goals, not methods
    - Spawns autonomous workers
    - Trusts workers to solve assigned problems
    - Intervenes only on failure
```

### 2. Chatty Agents
```yaml
❌ ANTI-PATTERN:
  agent_a: "What should I do next?"
  orchestrator: "Do X"
  agent_a: "Done X, what now?"
  orchestrator: "Do Y"
  agent_a: "Done Y, what now?"
  # Repeat 20 times...

  overhead: ~2s per message * 20 = 40s wasted

✓ BETTER:
  orchestrator: "Here's your complete task: [X, Y, Z]"
  agent_a: [Works autonomously]
  agent_a: "All complete, here are results"

  overhead: 2 messages total, ~4s
  time_saved: 36s
```

### 3. Sequential When Parallel is Possible
```yaml
❌ ANTI-PATTERN:
  step1: Search API endpoints (10s)
  step2: Search models (10s)  # WAIT
  step3: Search services (10s)  # WAIT

  total: 30s

✓ BETTER:
  parallel:
    - Search API endpoints (10s)
    - Search models (10s)
    - Search services (10s)

  total: 10s
  speedup: 3x
```

### 4. Over-Orchestration
```yaml
❌ ANTI-PATTERN:
  task: "Read src/config.ts and summarize"

  approach:
    1. Spawn explorer agent
    2. Explorer spawns reader agent
    3. Reader reads file
    4. Reader reports to explorer
    5. Explorer reports to main agent
    6. Main agent reports to user

  overhead: 3 agent spawns, 5 message passes

✓ BETTER:
  task: "Read src/config.ts and summarize"

  approach:
    1. Use Read tool directly
    2. Summarize
    3. Done

  overhead: 1 tool call
```

---

## Orchestration Decision Tree

```
Task Analysis:
  │
  ├─ Can be done with direct tools (Read/Grep/Glob)?
  │  └─ YES → Use tools directly (NO orchestration)
  │
  ├─ Requires < 3 specialized steps?
  │  └─ YES → Sequential agent chain
  │
  ├─ Has independent parallel subtasks?
  │  └─ YES → Scatter-gather pattern
  │
  ├─ Requires dynamic work distribution?
  │  └─ YES → Coordinator-worker pattern
  │
  └─ Complex multi-stage with conditionals?
     └─ YES → Hierarchical orchestration
```

---

## Orchestration Metrics

### Efficiency Metrics
```yaml
agent_utilization:
  formula: (Agent_Active_Time) / (Agent_Total_Time)
  target: > 80%
  problem_if_low: Too much waiting/coordination overhead

parallelism_factor:
  formula: (Total_Sequential_Time) / (Actual_Elapsed_Time)
  target: > 1.5 (for parallelizable tasks)
  perfect: Number of parallel agents

coordination_overhead:
  formula: (Coordination_Time) / (Total_Time)
  target: < 20%
  problem_if_high: Over-orchestration
```

### Quality Metrics
```yaml
first_time_success_rate:
  measure: % of orchestrated workflows completing successfully
  target: > 85%

retry_rate:
  measure: Average retries per orchestrated task
  target: < 1.3
  problem_if_high: Poor task decomposition

cascading_failure_rate:
  measure: % of failures causing downstream failures
  target: < 10%
  mitigation: Defensive programming, fallback strategies
```

---

## Practical Guidelines

### When Spawning an Agent:
```yaml
checklist:
  - [ ] Is the task too complex for direct tools?
  - [ ] Does the agent have a clear, singular goal?
  - [ ] Can the agent work autonomously (minimal back-and-forth)?
  - [ ] Is the expected completion time < 2 minutes?
  - [ ] Are success criteria clear and verifiable?
  - [ ] Can results be combined with other agents' results?
```

### When Coordinating Multiple Agents:
```yaml
checklist:
  - [ ] Are agents truly independent (can run in parallel)?
  - [ ] Is there a clear aggregation strategy?
  - [ ] Have I minimized coupling (loose interfaces)?
  - [ ] Is coordination overhead < 20% of total time?
  - [ ] Can I handle partial failures gracefully?
  - [ ] Is the orchestration pattern the simplest that works?
```

### When Debugging Orchestration:
```yaml
questions:
  - "Where is the bottleneck?" (Sequential when should be parallel?)
  - "What's the coordination overhead?" (Too much messaging?)
  - "Are agents waiting unnecessarily?" (Blocking on non-dependencies?)
  - "Can I eliminate an orchestration layer?" (Over-engineered?)
  - "Are failures cascading?" (Need better isolation?)
```

---

## Examples from Global1SIM Project

### Example 1: Feature Development Orchestration
```yaml
# /feature-dev:feature-dev command
task: "Implement new subscriber activation feature"

orchestration:
  phase_1_explore:  # Sequential (must understand first)
    - code-explorer:
        goal: "Understand existing subscriber patterns"
        time: ~20s
        output: patterns.md

  phase_2_architect:  # Sequential (needs exploration results)
    - code-architect:
        input: patterns.md
        goal: "Design activation feature"
        time: ~30s
        output: blueprint.md

  phase_3_implement:  # Can be parallel
    parallel:
      - implementer:
          task: "Write domain logic"
          time: ~45s

      - implementer:
          task: "Write API endpoints"
          time: ~40s

      - implementer:
          task: "Write tests"
          time: ~50s

    sync_point: "All implementations complete"

  phase_4_review:  # Sequential (needs all code)
    - code-reviewer:
        input: all_changes
        goal: "Verify quality"
        time: ~25s

total_time: ~170s (vs ~240s if all sequential)
speedup: 1.4x
```

### Example 2: Architecture Analysis (Scatter-Gather)
```yaml
task: "Analyze hexagonal architecture compliance"

scatter:
  parallel_agents:
    - agent: "ports-analyzer"
      scope: "src/ports/**"
      time: 15s

    - agent: "adapters-analyzer"
      scope: "src/adapters/**"
      time: 15s

    - agent: "domain-analyzer"
      scope: "src/domain/**"
      time: 15s

    - agent: "dependency-analyzer"
      scope: "Check for violations"
      time: 20s

gather:
  synthesize:
    - Combine all findings
    - Identify architecture violations
    - Generate compliance report
    time: 5s

total_time: 25s (vs 65s sequential)
speedup: 2.6x
```

---

## References

- **Modern Software Engineering** by Dave Farley
  - Chapter 9: Modularity
  - Chapter 13: Coupling
  - Chapter 15: Organizational Scaling

- **Related Guidelines**:
  - `velocity-principles.md`: Agent speed optimization
  - `parallel-execution-patterns.md`: Advanced parallelism
  - `agent-capability-patterns.md`: Specialized agent roles
  - `context-management.md`: Shared knowledge strategies
