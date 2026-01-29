# Agent Capability Patterns

**Foundation**: Specialized Agents with Clear Boundaries

---

## Core Philosophy

> "A modular approach frees teams to work more independently. They can each make small incremental steps forward without needing to coordinate."
> — Modern Software Engineering

Apply the same principle to agents: **Specialized capabilities reduce coordination overhead and increase reusability.**

---

## Agent Capability Categories

### 1. Discovery Agents (Read-Only, Search-Focused)

**Purpose**: Understand what exists, find information

**Capabilities**:
- ✓ Read files
- ✓ Search code (Grep, Glob)
- ✓ Analyze patterns
- ✓ Index codebases (DeepContext)
- ✗ No writes
- ✗ No execution
- ✗ No modifications

**Examples**:
```yaml
code-explorer:
  tools: [Read, Grep, Glob, DeepContext]
  output: Understanding of existing patterns
  time_budget: 20-30s
  scope: Exploration only

api-discoverer:
  tools: [Grep, Read]
  output: List of API endpoints
  time_budget: 10-15s
  scope: API surface area

dependency-mapper:
  tools: [Read, Grep]
  output: Dependency graph
  time_budget: 15-20s
  scope: Import/export relationships
```

**Best Practices**:
- Start broad (Glob), narrow focus (Grep), confirm (Read)
- Use DeepContext for semantic search
- Produce structured output (JSON, Markdown tables)
- Include confidence levels in findings

### 2. Architecture Agents (Analysis & Design)

**Purpose**: Design solutions based on understanding

**Capabilities**:
- ✓ Read files
- ✓ Search code
- ✓ Analyze patterns
- ✓ Design architectures
- ✓ Create blueprints
- ✗ No code writing
- ✗ No execution

**Examples**:
```yaml
code-architect:
  input: Feature requirements + existing patterns
  tools: [Read, Grep, DeepContext]
  output: Implementation blueprint
  time_budget: 30-45s
  deliverable: |
    - Files to create/modify
    - Component designs
    - Data flow diagrams
    - Implementation sequence

hexagonal-architecture-guardian:
  input: Code changes or module design
  tools: [Read, Grep]
  output: Architecture compliance report
  time_budget: 20-30s
  deliverable: |
    - Violations identified
    - Recommendations
    - Refactoring suggestions

performance-optimizer:
  input: Performance bottleneck description
  tools: [Read, Grep, WebSearch]
  output: Optimization strategy
  time_budget: 30-40s
  deliverable: |
    - Hotspot analysis
    - Optimization techniques
    - Expected improvements
```

**Best Practices**:
- Base designs on discovered patterns (don't guess)
- Provide rationale for architectural decisions
- Include alternatives considered
- Specify acceptance criteria

### 3. Implementation Agents (Write Code)

**Purpose**: Transform designs into working code

**Capabilities**:
- ✓ Read files
- ✓ Write files
- ✓ Edit files
- ✓ Search for context
- ✓ Run tools (limited)
- ⚠ Execution only for verification

**Examples**:
```yaml
feature-implementer:
  input: Blueprint from architect
  tools: [Read, Write, Edit]
  output: Working code
  time_budget: 60-90s
  deliverable: |
    - Implementation code
    - Self-verification results

tdd-cycle-driver:
  input: Feature description
  tools: [Read, Write, Edit, Bash]
  output: Test + implementation
  time_budget: 90-120s
  cycle: RED → GREEN → REFACTOR

refactor-agent:
  input: Code to improve
  tools: [Read, Edit, Bash (tests)]
  output: Refactored code
  time_budget: 45-60s
  constraint: Must keep tests passing
```

**Best Practices**:
- Read before writing (understand context)
- Write minimal code (YAGNI principle)
- Verify immediately (run tests if available)
- Follow project conventions
- Comment non-obvious decisions

### 4. Review Agents (Quality Assurance)

**Purpose**: Verify quality, find issues

**Capabilities**:
- ✓ Read files
- ✓ Analyze code
- ✓ Run tools (linters, tests)
- ✓ Check patterns
- ✗ No writes (reports only)

**Examples**:
```yaml
code-reviewer:
  input: Code changes
  tools: [Read, Grep, Bash (tests)]
  output: Review feedback
  time_budget: 25-40s
  checks:
    - Logic errors
    - Security vulnerabilities
    - Code quality issues
    - Convention adherence

test-quality-checker:
  input: Test files
  tools: [Read, Bash (coverage)]
  output: Test quality report
  time_budget: 15-25s
  checks:
    - Coverage metrics
    - Assertion quality
    - Test independence
    - Edge case coverage

architecture-reviewer:
  input: Module or system design
  tools: [Read, Grep]
  output: Architecture review
  time_budget: 30-45s
  checks:
    - Separation of concerns
    - Coupling levels
    - Modularity
    - Pattern compliance
```

**Best Practices**:
- Use confidence-based filtering (report only high-confidence issues)
- Prioritize by severity
- Provide actionable feedback
- Include positive observations (what's done well)

### 5. Execution Agents (Run & Verify)

**Purpose**: Execute commands, gather results

**Capabilities**:
- ✓ Run commands (Bash)
- ✓ Parse output
- ✓ Verify results
- ✓ Read files (for context)
- ⚠ Write only for fixes

**Examples**:
```yaml
test-runner:
  input: Test suite to run
  tools: [Bash]
  output: Test results + analysis
  time_budget: Varies by test suite
  deliverable: |
    - Pass/fail status
    - Failure analysis
    - Coverage report

build-verifier:
  input: Build command
  tools: [Bash]
  output: Build status
  time_budget: Varies by build
  deliverable: |
    - Success/failure
    - Error analysis
    - Build artifacts verification

linter-runner:
  input: Files to lint
  tools: [Bash (lint), Read]
  output: Lint report
  time_budget: 10-20s
  deliverable: |
    - Issues found
    - Auto-fix suggestions
    - Severity ratings
```

**Best Practices**:
- Set appropriate timeouts
- Capture both stdout and stderr
- Parse errors intelligently
- Provide context for failures
- Suggest fixes when possible

---

## Capability Matrix

| Agent Type | Read | Write | Execute | Search | Design | Review |
|-----------|------|-------|---------|--------|--------|--------|
| **Discovery** | ✓ | ✗ | ✗ | ✓ | ✗ | ✗ |
| **Architecture** | ✓ | ✗ | ✗ | ✓ | ✓ | ✓ |
| **Implementation** | ✓ | ✓ | ⚠ | Limited | ✗ | ✗ |
| **Review** | ✓ | ✗ | ⚠ | ✓ | ✗ | ✓ |
| **Execution** | ✓ | ⚠ | ✓ | ✗ | ✗ | ✗ |

**Legend**:
- ✓ = Primary capability
- ⚠ = Limited/constrained capability
- ✗ = Not allowed

---

## Composition Patterns

### Pattern 1: Discovery → Architecture → Implementation
```yaml
workflow: "New Feature Development"

step_1_discover:
  agent: code-explorer
  output: patterns.md
  duration: 20s

step_2_design:
  agent: code-architect
  input: patterns.md + feature_spec
  output: blueprint.md
  duration: 35s

step_3_implement:
  agent: feature-implementer
  input: blueprint.md
  output: code_changes
  duration: 75s

total: 130s
```

### Pattern 2: Parallel Discovery → Synthesis
```yaml
workflow: "Comprehensive Analysis"

parallel_discovery:
  - api-discoverer → api_endpoints.json (12s)
  - dependency-mapper → dependencies.json (18s)
  - pattern-analyzer → patterns.json (15s)

synthesis:
  agent: architecture-synthesizer
  inputs: [api_endpoints, dependencies, patterns]
  output: architecture_report.md
  duration: 20s

total: 38s (vs 65s sequential)
```

### Pattern 3: TDD Cycle (Iterative)
```yaml
workflow: "Test-Driven Development"

iteration_1:
  - tdd-cycle-driver: Write failing test (15s)
  - tdd-cycle-driver: Minimal implementation (30s)
  - test-runner: Verify pass (5s)
  cycle_time: 50s

iteration_2:
  - tdd-cycle-driver: Add edge case test (10s)
  - tdd-cycle-driver: Handle edge case (20s)
  - test-runner: Verify pass (5s)
  cycle_time: 35s

iteration_3:
  - refactor-agent: Improve design (25s)
  - test-runner: Verify still passes (5s)
  cycle_time: 30s

total: 115s for full feature
```

---

## Capability Selection Guide

### Decision Tree

```
Task Analysis:
  │
  ├─ Need to understand existing code?
  │  └─ Use Discovery Agent
  │
  ├─ Need to design solution?
  │  └─ Use Architecture Agent
  │
  ├─ Need to write code?
  │  ├─ Have clear design? → Implementation Agent
  │  └─ No design? → Discovery → Architecture → Implementation
  │
  ├─ Need to verify quality?
  │  └─ Use Review Agent
  │
  └─ Need to run commands?
     └─ Use Execution Agent
```

### Capability Boundaries

```yaml
✓ GOOD - Respects Boundaries:
  code-explorer:
    - Searches for authentication patterns
    - Outputs findings
    - DOES NOT design solution
    - DOES NOT implement changes

✗ BAD - Violates Boundaries:
  code-explorer:
    - Searches for patterns
    - Decides architecture
    - Implements changes
    - Problem: Too many responsibilities
```

---

## Specialized Agent Examples (Global1SIM)

### 1. Hexagonal Architecture Guardian
```yaml
specialization: Architecture compliance

capabilities:
  - Detect architecture violations
  - Validate ports & adapters structure
  - Ensure domain purity
  - Check dependency directions

tools: [Read, Grep, Bash (tests)]

typical_workflow:
  1. Read module structure
  2. Check for violations:
     - Domain depends on infrastructure?
     - Business logic in routes?
     - Database in domain models?
  3. Generate compliance report
  4. Suggest refactorings

time_budget: 30-45s
```

### 2. TDD Cycle Driver
```yaml
specialization: RED-GREEN-REFACTOR discipline

capabilities:
  - Write failing tests (RED)
  - Minimal implementation (GREEN)
  - Refactor with test safety (REFACTOR)
  - Continuous test execution

tools: [Read, Write, Edit, Bash (pytest)]

typical_workflow:
  1. Write simplest failing test
  2. Run test (verify RED)
  3. Write minimal code to pass
  4. Run test (verify GREEN)
  5. Refactor if needed
  6. Run test after each tiny change

time_budget: 60-90s per cycle
cycles: Multiple iterations
```

### 3. Pydantic V2 Patterns Enforcer
```yaml
specialization: Pydantic model quality

capabilities:
  - Enforce frozen=True (immutability)
  - Validate field validators
  - Check type hints
  - Ensure proper error handling

tools: [Read, Edit, Bash (mypy)]

typical_workflow:
  1. Read model definitions
  2. Check for violations:
     - Missing frozen=True?
     - Missing type hints?
     - Missing validators?
  3. Apply fixes
  4. Verify with mypy

time_budget: 20-30s per model
```

---

## Anti-Patterns to Avoid

### 1. Swiss Army Knife Agent
```yaml
❌ ANTI-PATTERN:
  god-agent:
    capabilities: [Read, Write, Execute, Search, Design, Review]
    problem: "Does everything, masters nothing"

✓ PATTERN:
  specialized_agents:
    - explorer: [Read, Search]
    - implementer: [Write, Edit]
    - reviewer: [Read, Review]
    benefit: "Each excels at its specialty"
```

### 2. Capability Creep
```yaml
❌ ANTI-PATTERN:
  code_explorer:
    original: "Find existing patterns"
    creep: "Also fix bugs I find"
    creep: "Also update documentation"
    creep: "Also refactor while exploring"
    problem: "Mission creep violates separation"

✓ PATTERN:
  code_explorer:
    scope: "Find and report patterns only"
    output: "Structured findings"
    action: "Let other agents handle fixes"
```

### 3. Overlapping Capabilities
```yaml
❌ ANTI-PATTERN:
  both_agents_can:
    - Write code
    - Run tests
    - Fix bugs
    - Review changes
  confusion: "Which agent should I use?"

✓ PATTERN:
  clear_boundaries:
    implementer: Write code
    test-runner: Run tests
    bug-fixer: Fix bugs
    reviewer: Review changes
  clarity: "Each has unique primary capability"
```

---

## Capability Evolution

### Adding New Capabilities

```yaml
before_adding:
  questions:
    - Does any existing agent handle this?
    - Can existing agent be extended?
    - Is this truly a distinct capability?
    - Will this create overlap/confusion?

if_new_capability_needed:
  steps:
    1. Define clear boundaries
    2. Specify inputs/outputs
    3. Document tool usage
    4. Set time budgets
    5. Create examples
    6. Test with real scenarios
```

### Refining Existing Capabilities

```yaml
continuous_improvement:
  - Monitor agent performance
  - Gather feedback on results
  - Identify bottlenecks
  - Refine tool usage patterns
  - Update time budgets based on reality
  - Document learnings
```

---

## References

- **Modern Software Engineering** by Dave Farley
  - Chapter 9: Modularity
  - Chapter 11: Separation of Concerns
  - Chapter 12: Information Hiding and Abstraction

- **Related Guidelines**:
  - `velocity-principles.md`: Speed optimization per capability
  - `orchestration-principles.md`: How capabilities compose
  - `feedback-optimization.md`: Fast feedback per capability
