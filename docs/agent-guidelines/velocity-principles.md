# Agent Velocity Principles

**Foundation**: Modern Software Engineering Principles Applied to Agent Development

---

## Core Philosophy

> "The most significant constraint on the ability of teams to implement new ideas is the quality of their systems, not the skills or experience of the people who build them"
> — Modern Software Engineering

Agent velocity is not about speed alone—it's about **sustainable throughput with stability**. Fast agents that produce unreliable results or block orchestration create negative velocity.

---

## The Two Pillars of Agent Velocity

### 1. Optimize for Learning (Fast Feedback)

#### Principle: Work in Small Batches
**For Agents**: Break tasks into atomic, testable operations

```yaml
✓ GOOD - Small Batch Agent Task:
  task: "Find all API endpoints in src/api/"
  scope: Single directory, clear output
  feedback_time: < 10 seconds

✗ BAD - Large Batch Agent Task:
  task: "Analyze entire codebase architecture"
  scope: Everything, vague output
  feedback_time: Minutes to hours
```

**Implementation**:
- Agents should complete primary objectives in < 30 seconds
- If task takes > 1 minute, decompose into subagents
- Each agent action should produce immediate, verifiable output

#### Principle: Optimize for Fast Feedback
**For Agents**: Minimize feedback loops at every level

**Feedback Hierarchy** (fail soonest):
1. **< 100ms**: Schema validation, type checking (before execution)
2. **< 1s**: Tool parameter validation, file existence checks
3. **< 10s**: Read/Grep/Glob operations, quick searches
4. **< 30s**: Primary agent task completion
5. **< 2min**: Agent self-verification and result validation

```python
# Agent Feedback Pattern
def execute_agent_task():
    # Level 1: Immediate validation (< 100ms)
    validate_inputs()  # Fail fast if invalid

    # Level 2: Quick checks (< 1s)
    verify_file_exists()  # Don't waste time on missing files

    # Level 3: Core work (< 10s)
    results = search_codebase()

    # Level 4: Verification (< 5s)
    validate_results(results)

    return results
```

#### Principle: Begin Before Knowing Everything
**For Agents**: Start with hypothesis, iterate based on evidence

```yaml
Hypothesis-Driven Agent Execution:
  1. Form hypothesis: "User authentication is likely in src/auth/"
  2. Quick test: Grep for "authenticate" in src/auth/
  3. Observe results: Found 3 matches
  4. Refine hypothesis: "Core auth in src/auth/service.ts"
  5. Deeper investigation: Read src/auth/service.ts
  6. Update understanding and proceed

DON'T:
  - Read entire codebase before forming hypothesis
  - Execute all possible searches "just in case"
  - Wait for complete information before starting
```

#### Principle: Experiment with Confidence
**For Agents**: Use controlled experiments, not exhaustive searches

```yaml
Experimental Search Strategy:
  iteration_1:
    hypothesis: "Config in root directory"
    action: Glob "*.config.{js,ts,json}"
    result: Found 3 files
    time: 2s

  iteration_2:
    hypothesis: "Specific config in package.json"
    action: Read package.json
    result: Confirmed
    time: 1s

  total_time: 3s

AVOID:
  - Reading all files hoping to find config
  - Parallel search of every directory
  - Exhaustive grep without hypothesis
```

---

### 2. Optimize for Managing Complexity

#### Principle: Separation of Concerns
**For Agents**: One agent, one clear responsibility

```yaml
✓ GOOD - Focused Agent:
  agent: "code-explorer"
  responsibility: "Understand existing code patterns"
  tools: [Read, Grep, Glob]
  does_not: Write, Edit, or modify code

✗ BAD - Mixed Concerns:
  agent: "code-explorer-and-fixer"
  responsibility: "Understand AND fix code"
  problem: Violates separation, unclear success criteria
```

**Agent Responsibility Matrix**:
| Agent Type | Reads | Writes | Executes | Searches |
|-----------|-------|--------|----------|----------|
| Explorer  | ✓     | ✗      | ✗        | ✓        |
| Architect | ✓     | ✗      | ✗        | ✓        |
| Implementer| ✓    | ✓      | ✓        | Limited  |
| Reviewer  | ✓     | ✗      | ✓        | ✓        |

#### Principle: Modularity
**For Agents**: Compose complex tasks from simple, reusable agents

```yaml
# Modular Agent Composition
feature_implementation:
  agents:
    - code-explorer: Understand patterns
    - code-architect: Design approach
    - implementer: Write code
    - code-reviewer: Verify quality

  each_agent:
    - Has clear input/output contract
    - Can be tested independently
    - Can be swapped for alternatives
    - Doesn't know about other agents
```

#### Principle: Cohesion
**For Agents**: Related operations stay together, unrelated stay apart

```yaml
✓ COHESIVE - TDD Cycle Agent:
  operations:
    - Write failing test (related)
    - Implement minimal code (related)
    - Verify test passes (related)
    - Refactor if needed (related)
  context: All operations serve TDD cycle

✗ NOT COHESIVE - "Development Agent":
  operations:
    - Write tests (different context)
    - Update documentation (different context)
    - Fix linting errors (different context)
    - Deploy to production (different context)
  problem: Unrelated operations bundled together
```

---

## Velocity Anti-Patterns to Avoid

### 1. Premature Optimization
```yaml
❌ ANTI-PATTERN: "I'll search everywhere to be thorough"
  problem: Wastes time on unlikely paths

✓ PATTERN: "I'll search likely locations first"
  benefit: Fast feedback, iterate if needed
```

### 2. Analysis Paralysis
```yaml
❌ ANTI-PATTERN: "Read entire codebase before starting"
  problem: Delays feedback indefinitely

✓ PATTERN: "Quick search → hypothesis → verify → proceed"
  benefit: Immediate progress, learn as you go
```

### 3. Tool Misuse
```yaml
❌ ANTI-PATTERN: Using Task tool for simple file reads
  problem: Overhead of agent spawning for trivial work

✓ PATTERN: Use Read/Grep directly for simple operations
  benefit: < 1s feedback vs agent spawn overhead
```

### 4. Unbounded Search
```yaml
❌ ANTI-PATTERN: Grep entire codebase without constraints
  problem: Slow, noisy results, high token usage

✓ PATTERN: Constrained search with glob patterns
  benefit: Fast, focused results
```

---

## Velocity Metrics (DORA-Aligned)

### Throughput Indicators
- **Agent Completion Time**: Target < 30s for primary task
- **Task Decomposition Ratio**: > 80% of tasks completable by single agent
- **Tool Call Efficiency**: Average < 5 tool calls per agent task

### Stability Indicators
- **First-Attempt Success Rate**: > 80% of agents complete without retry
- **Result Accuracy**: > 95% of agent outputs are correct
- **Rollback Rate**: < 5% of agent actions need to be undone

### Combined Velocity Score
```
Velocity = (Throughput × Stability) / (Feedback_Latency)

High Velocity Agent:
  - Completes tasks quickly (< 30s)
  - High success rate (> 80%)
  - Minimal feedback loops (< 3 iterations)

Low Velocity Agent:
  - Takes long time (> 2min)
  - Requires retries (< 50% first-time success)
  - Many feedback cycles (> 5 iterations)
```

---

## Practical Application Checklist

### Before Creating an Agent:
- [ ] Can this task be completed in < 30 seconds?
- [ ] Is there exactly ONE clear success criterion?
- [ ] Does the agent have access to fast feedback?
- [ ] Can results be verified immediately?
- [ ] Is the responsibility clearly separated from other concerns?

### During Agent Execution:
- [ ] Am I working in small batches?
- [ ] Am I getting feedback quickly (< 10s)?
- [ ] Am I iterating based on evidence, not guesses?
- [ ] Am I using the simplest tool that works?
- [ ] Can I verify my results immediately?

### After Agent Completion:
- [ ] Did the agent complete its primary task?
- [ ] Was the result correct on first attempt?
- [ ] Could this agent be reused for similar tasks?
- [ ] Did the agent produce clear, actionable output?
- [ ] Would I be confident running this agent again?

---

## References

- **Modern Software Engineering** by Dave Farley
  - Chapter 5: Feedback
  - Chapter 6: Incrementalism
  - Chapter 7: Empiricism
  - Chapter 8: Experimental

- **Related Guidelines**:
  - `feedback-optimization.md`: Detailed feedback loop patterns
  - `orchestration-principles.md`: Multi-agent coordination
  - `context-management.md`: Token efficiency strategies
