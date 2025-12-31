# Context Management Guidelines

**Foundation**: Optimize Token Usage, Minimize Context Overhead

---

## Core Philosophy

> "Control the variables to make your releases reliable."
> — Modern Software Engineering

Control context size to make agents fast and cost-effective. **Context is a limited resource—spend it wisely.**

---

## Context Budget Model

### Token Allocation Strategy

```yaml
typical_agent_budget: 200,000 tokens total

allocation:
  input_context: 50,000 tokens (25%)
    - System prompt: ~5,000
    - Conversation history: ~15,000
    - Tool results: ~30,000

  working_space: 100,000 tokens (50%)
    - Agent reasoning
    - Tool calls
    - Intermediate results

  output_generation: 50,000 tokens (25%)
    - Final response
    - Structured outputs
    - Reports

warning_threshold: 80% utilization (160,000 tokens)
critical_threshold: 95% utilization (190,000 tokens)
```

---

## Context Optimization Techniques

### 1. Progressive Disclosure

```yaml
✓ GOOD - Start Small, Expand as Needed:
  step_1:
    - Glob "**/*.ts" to find files
    - tokens: ~500
    - time: 2s

  step_2:
    - Read most relevant files (3 files)
    - tokens: ~5,000
    - time: 3s

  step_3:
    - Read additional context if needed (2 more files)
    - tokens: ~3,000
    - time: 2s

  total_tokens: ~8,500
  total_time: 7s

✗ BAD - Load Everything Upfront:
  step_1:
    - Read all 50 TypeScript files
    - tokens: ~80,000
    - time: 20s

  problem:
    - Most files irrelevant
    - Wasted tokens
    - Slow feedback
```

### 2. Selective Reading

```yaml
✓ GOOD - Read What Matters:
  technique: "Use offset + limit parameters"

  example:
    - Read large_file.ts (2000 lines)
    - Strategy: Read function signatures first (lines 1-100)
    - Then: Read relevant function (lines 523-580)
    - Tokens saved: ~90% of file content

✗ BAD - Read Entire Files:
  approach: "Read complete file always"
  problem: "Pay for unused content"
```

### 3. Summarization Over Full Content

```yaml
✓ GOOD - Compress Information:
  large_search_results:
    raw: 50 files found, 15,000 tokens
    summarized: |
      - 30 files in src/api/ (REST endpoints)
      - 15 files in src/services/ (business logic)
      - 5 files in src/models/ (data models)
    tokens: ~200

✗ BAD - Include Everything:
  listing: "All 50 file paths with full content preview"
  tokens: 15,000
```

### 4. Stateless Agents (Where Possible)

```yaml
✓ GOOD - Minimal State Transfer:
  agent_a_output:
    full_analysis: 20,000 tokens (kept internal)
    summary_for_agent_b: 500 tokens (key findings only)

  agent_b_input:
    receives: 500 token summary
    benefit: Fast startup, focused work

✗ BAD - Full State Transfer:
  agent_a_output: "Entire 20,000 token analysis"
  agent_b_input: "Must process all 20,000 tokens"
  overhead: Wasted time and tokens
```

---

## Tool-Specific Context Strategies

### Read Tool
```yaml
optimization_strategies:
  1. Check file size first (Bash: wc -l)
  2. Read strategically:
     - Small files (<200 lines): Read completely
     - Medium files (200-1000 lines): Read sections
     - Large files (>1000 lines): Read targeted portions
  3. Use offset+limit for large files
  4. Prefer multiple targeted reads over one full read

example:
  file: "large_service.ts" (1500 lines)
  approach:
    - Read lines 1-50 (imports + exports)
    - Read lines 523-675 (target function)
    - Skip remaining 825 lines
  tokens_saved: ~12,000
```

### Grep Tool
```yaml
optimization_strategies:
  1. Use specific patterns (not .*)
  2. Limit output with head_limit parameter
  3. Use type/glob filters to reduce scope
  4. Prefer files_with_matches over full content
  5. Use -A/-B/-C context sparingly

example:
  bad_grep:
    pattern: ".*function.*"
    output_mode: "content"
    result: 10,000 lines of matches

  good_grep:
    pattern: "export function authenticate"
    output_mode: "files_with_matches"
    glob: "src/auth/**/*.ts"
    result: 3 file paths

  tokens_saved: ~15,000
```

### DeepContext Search
```yaml
optimization_strategies:
  1. Craft precise queries
  2. Use max_results wisely (default: 5)
  3. Follow up with Read for details
  4. Don't increase max_results without reason

example:
  bad_search:
    query: "code"  # Too vague
    max_results: 20
    result: Noisy, irrelevant results

  good_search:
    query: "subscriber activation business logic"
    max_results: 5  # Default is good
    result: Precisely relevant code chunks
```

---

## Context Handoff Patterns

### Pattern 1: Compressed Summary
```yaml
use_case: "Agent A completes discovery, passes to Agent B"

agent_a_internal: |
  - Analyzed 30 files
  - Found 15 patterns
  - Detailed notes: 18,000 tokens

agent_a_to_agent_b: |
  Key Findings (compressed to 800 tokens):
  - Auth pattern: JWT in src/auth/jwt.service.ts
  - Database: SQLAlchemy ORM, repositories in src/repos/
  - API: FastAPI, routes in src/api/routes/
  - Recommendation: Follow existing patterns

benefit: Agent B starts fast with essentials
```

### Pattern 2: Pointer-Based Context
```yaml
use_case: "Avoid duplicating large content"

agent_a_output:
  findings_document: "analysis_results.md" (written to disk)
  pointer_to_agent_b: "See analysis_results.md for details"

agent_b:
  action: Read analysis_results.md only if needed
  benefit: Agent B decides what context to load

technique: "Externalize large context"
```

### Pattern 3: Layered Context
```yaml
use_case: "Progressive detail levels"

layer_1_summary: |
  Feature: Subscriber activation
  Files: 3 to modify
  Time estimate: 30 minutes
  (200 tokens)

layer_2_details: |
  [Only loaded if agent needs more]
  - File 1: src/models/subscriber.py (add status field)
  - File 2: src/services/activation.py (add activate method)
  - File 3: src/api/routes/subscribers.py (add POST endpoint)
  (1,000 tokens)

layer_3_implementation: |
  [Only loaded if agent implements]
  - Full code examples
  - Test cases
  - Error handling
  (8,000 tokens)

benefit: Load only what's needed for current task
```

---

## Context Management Anti-Patterns

### 1. Context Bloat
```yaml
❌ ANTI-PATTERN:
  agent: "Load all project files into context"
  reason: "Might need them"
  result:
    - 150,000 tokens consumed
    - 90% unused
    - Slow agent startup
    - High cost

✓ PATTERN:
  agent: "Load files on-demand"
  approach: "Search → Identify → Read targeted"
  result:
    - 8,000 tokens consumed
    - 95% utilization
    - Fast execution
    - Low cost
```

### 2. Redundant Context
```yaml
❌ ANTI-PATTERN:
  agent_handoff:
    agent_a: Sends full 20,000 token analysis
    agent_b: Also re-reads all source files (15,000 tokens)
    agent_c: Receives both contexts (35,000 tokens)

  duplication: "Same information, multiple representations"

✓ PATTERN:
  agent_handoff:
    agent_a: Sends compressed summary (1,000 tokens)
    agent_b: Uses summary, reads only new files (3,000 tokens)
    agent_c: Receives synthesis (2,000 tokens)

  deduplication: "No redundant information"
```

### 3. Premature Context Loading
```yaml
❌ ANTI-PATTERN:
  agent_start:
    step_1: "Read all configuration files"
    step_2: "Read all model definitions"
    step_3: "Read all test files"
    step_4: "NOW determine what task needs"

  problem: "Loaded 90% unnecessary context"

✓ PATTERN:
  agent_start:
    step_1: "Understand task requirements"
    step_2: "Identify relevant files"
    step_3: "Load only those files"
    step_4: "Proceed with work"

  benefit: "Loaded only 10% necessary context"
```

### 4. Context Retention Without Need
```yaml
❌ ANTI-PATTERN:
  long_running_agent:
    minute_1: Load 20 files (30,000 tokens)
    minute_2: Use 2 of those files
    minute_3: Load 15 more files (22,000 tokens)
    minute_4: Still carrying all 35 files in context

  problem: "Accumulating context garbage"

✓ PATTERN:
  long_running_agent:
    minute_1: Load relevant 2 files (3,000 tokens)
    minute_2: Complete work
    minute_3: Load next relevant 3 files (4,500 tokens)
    minute_4: Previous context not retained

  benefit: "Lean context throughout"
```

---

## Context-Aware Tool Selection

### Decision Matrix

```yaml
task_context_requirements:

  find_files:
    tool: Glob
    context_cost: ~500 tokens
    time: 1-2s
    use_when: "Need file list"

  search_patterns:
    tool: Grep (files_with_matches)
    context_cost: ~1,000 tokens
    time: 2-5s
    use_when: "Need to locate code"

  understand_code:
    tool: DeepContext
    context_cost: ~3,000 tokens per query
    time: 3-8s
    use_when: "Semantic understanding needed"

  read_specific_files:
    tool: Read
    context_cost: ~1,000-5,000 tokens per file
    time: 1-3s per file
    use_when: "Need actual code content"

  avoid:
    - Reading all files "just in case"
    - Multiple redundant searches
    - Loading full files when excerpts suffice
```

---

## Context Monitoring & Alerts

### Usage Tracking

```yaml
monitor_during_execution:
  current_tokens: Track accumulation
  threshold_warnings:
    - 50% (100k tokens): "Normal"
    - 75% (150k tokens): "Warning - optimize if possible"
    - 90% (180k tokens): "Critical - must reduce context"
    - 95% (190k tokens): "Emergency - stop non-essential loading"

optimization_triggers:
  at_75_percent:
    - Review loaded content
    - Identify unused context
    - Summarize large sections
    - Consider agent handoff

  at_90_percent:
    - Force summarization
    - Drop non-essential context
    - Complete critical tasks only
    - Plan for agent spawn if more work needed
```

---

## Best Practices Summary

### DO:
- ✓ Load context progressively (start small)
- ✓ Use targeted reads (offset+limit)
- ✓ Compress summaries for handoffs
- ✓ Monitor token usage
- ✓ Prefer search → target → read pattern
- ✓ Use appropriate tool for task (don't over-tool)

### DON'T:
- ✗ Load all files upfront
- ✗ Read entire large files
- ✗ Transfer full context between agents
- ✗ Retain context after use
- ✗ Use overly broad searches
- ✗ Spawn agents for trivial context loads

---

## Context Budget Examples

### Example 1: Code Exploration (Well-Optimized)
```yaml
task: "Find authentication implementation"

execution:
  step_1: Grep "authenticate" in src/ (files_with_matches)
    tokens: 300
    time: 2s

  step_2: Read 3 relevant files (targeted)
    tokens: 4,500
    time: 3s

  step_3: Understand pattern
    tokens: 500 (reasoning)
    time: 2s

total_tokens: 5,300
total_time: 7s
efficiency: Excellent
```

### Example 2: Feature Implementation (Optimized)
```yaml
task: "Implement subscriber activation"

execution:
  step_1: DeepContext search for patterns
    tokens: 3,000
    time: 5s

  step_2: Read 5 relevant files (sections only)
    tokens: 7,000
    time: 5s

  step_3: Design implementation
    tokens: 2,000
    time: 3s

  step_4: Write code
    tokens: 5,000 (includes reading target files)
    time: 8s

total_tokens: 17,000
total_time: 21s
efficiency: Good
```

### Example 3: Comprehensive Analysis (Context-Heavy)
```yaml
task: "Analyze entire system architecture"

execution:
  step_1: Index codebase (DeepContext)
    tokens: 10,000
    time: 15s

  step_2: Multiple searches (6 queries)
    tokens: 18,000
    time: 30s

  step_3: Read key files (15 files, sections)
    tokens: 22,000
    time: 15s

  step_4: Synthesize findings
    tokens: 8,000
    time: 10s

total_tokens: 58,000
total_time: 70s
efficiency: Acceptable (complex task justifies cost)
```

---

## References

- **Modern Software Engineering** by Dave Farley
  - Chapter 8: Experimental (controlling variables)
  - Chapter 12: Information Hiding and Abstraction

- **Related Guidelines**:
  - `velocity-principles.md`: Fast feedback reduces context needs
  - `agent-capability-patterns.md`: Specialized agents need less context
  - `feedback-optimization.md`: Quick feedback minimizes context accumulation
