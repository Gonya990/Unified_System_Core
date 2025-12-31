# Feedback Optimization Guidelines

**Foundation**: Fail Fast, Learn Fast, Iterate Fast

---

## Core Philosophy

> "Without feedback, there is no opportunity to learn."
> — Modern Software Engineering

**Fast feedback is the #1 velocity multiplier.** Optimize for the shortest possible feedback loop at every level.

---

## The Feedback Hierarchy

### Level 1: Immediate Validation (< 100ms)
```yaml
examples:
  - Schema validation (before tool execution)
  - Type checking (parameters)
  - Basic input validation

benefit: "Fail before wasting time"

implementation:
  if not valid_schema(input):
      raise ValidationError("Invalid input")  # < 1ms
  # Proceed with work
```

### Level 2: Quick Checks (< 1s)
```yaml
examples:
  - File existence checks
  - Bash command validation
  - Permission checks
  - Quick regex matches

benefit: "Fail before expensive operations"

implementation:
  if not file_exists(path):
      return Error("File not found")  # < 100ms
  # Proceed to read file
```

### Level 3: Fast Operations (< 10s)
```yaml
examples:
  - File reads (small-medium files)
  - Grep searches (constrained)
  - Glob patterns
  - Simple bash commands

benefit: "Primary feedback loop"

implementation:
  results = grep_search(pattern, scope)  # 3-8s
  if no_results(results):
      return "Pattern not found, try broader search"
  # Proceed with analysis
```

### Level 4: Medium Operations (< 30s)
```yaml
examples:
  - Agent primary tasks
  - Multiple file reads
  - DeepContext searches
  - Code analysis

benefit: "Task completion feedback"

implementation:
  analysis = analyze_codebase(scope)  # 15-25s
  return structured_results(analysis)
```

### Level 5: Verification Operations (< 60s)
```yaml
examples:
  - Test suite execution
  - Build verification
  - Integration checks
  - Full agent workflows

benefit: "Quality feedback"

implementation:
  test_results = run_tests(suite)  # 30-50s
  if failures(test_results):
      return failure_analysis(test_results)
```

---

## Feedback Optimization Strategies

### 1. Fail Fast Principle

```yaml
✓ GOOD - Early Validation:
  def process_file(path):
      # Level 1: Validate immediately
      if not path:
          raise ValueError("Path required")  # < 1ms

      # Level 2: Check existence
      if not exists(path):
          raise FileNotFoundError(f"{path} not found")  # < 100ms

      # Level 3: Proceed with work
      content = read_file(path)  # 1-3s
      return process(content)

✗ BAD - Late Validation:
  def process_file(path):
      # Do expensive work first
      setup_environment()  # 5s
      initialize_tools()   # 3s

      # Then discover problem
      if not exists(path):
          raise FileNotFoundError(f"{path} not found")  # Wasted 8s!
```

### 2. Progressive Validation

```yaml
✓ GOOD - Validate as You Go:
  step_1: Quick validation (file exists)
    feedback: < 1s

  step_2: Read first 10 lines (verify format)
    feedback: < 2s

  step_3: Process full file
    feedback: < 5s

  total_wasted_on_failure: 1-2s (caught early)

✗ BAD - Validate at End:
  step_1: Read entire file
  step_2: Process all content
  step_3: Discover format invalid

  total_wasted_on_failure: Full processing time
```

### 3. Hypothesis-Driven Exploration

```yaml
✓ GOOD - Test Hypotheses Quickly:
  hypothesis_1: "Auth logic in src/auth/"
    test: Grep "authenticate" in src/auth/ (2s)
    result: Found 5 matches ✓
    confidence: High

  hypothesis_2: "Uses JWT tokens"
    test: Grep "jwt" in src/auth/ (1s)
    result: Found 3 matches ✓
    confidence: High

  proceed: Read confirmed files (5s)

  total_time: 8s to high confidence

✗ BAD - Exhaustive Search:
  approach: Search entire codebase for everything
  time: 30s
  result: 90% irrelevant findings
  wasted: 22s on noise
```

### 4. Incremental Feedback

```yaml
✓ GOOD - Continuous Progress Updates:
  task: "Analyze 10 modules"

  feedback_pattern:
    - Module 1 complete (5s) → Report
    - Module 2 complete (5s) → Report
    - ...
    - All complete (50s) → Final report

  benefit: User sees progress, can interrupt if wrong direction

✗ BAD - Batch Feedback:
  task: "Analyze 10 modules"

  feedback_pattern:
    - [Silent for 50s]
    - Report all results at end

  problem: No way to know if on right track
```

---

## Tool-Specific Feedback Optimization

### Read Tool
```yaml
optimization:
  before_reading:
    - Verify file exists (Bash: test -f) < 100ms
    - Check file size (Bash: wc -l) < 200ms
    - Decide read strategy based on size

  feedback_checkpoints:
    - Small file (<200 lines): Read all, immediate feedback
    - Medium file (200-1000): Read sections, verify relevance
    - Large file (>1000): Read targeted portions only

  fail_fast:
    if file_too_large_and_no_strategy:
        return "File too large, specify sections to read"
```

### Grep Tool
```yaml
optimization:
  progressive_search:
    attempt_1: Specific pattern, constrained scope
      time: 2-3s
      if found: Success (fast feedback)

    attempt_2: Broader pattern, same scope
      time: 3-5s
      if found: Success (still fast)

    attempt_3: Specific pattern, broader scope
      time: 5-8s
      if found: Success

  fail_fast:
    if no_results_after_3_attempts:
        return "Pattern not found, suggest alternatives"
        # Don't keep searching indefinitely
```

### DeepContext Search
```yaml
optimization:
  query_refinement:
    initial_query: Broad but relevant
      results: 5 chunks (default)
      time: 5-8s
      evaluate: Are results relevant?

    if_not_relevant:
      refined_query: More specific terms
      time: 5-8s
      evaluate: Better results?

  feedback_loop:
    - Query → Results (5-8s)
    - Evaluate relevance
    - Refine if needed (don't increase max_results first)
    - Maximum 2-3 query iterations
```

---

## Feedback Loop Patterns

### Pattern 1: Rapid Iteration Loop

```yaml
use_case: "Exploring unknown codebase"

loop_structure:
  iteration_time: < 10s each
  max_iterations: 5
  total_budget: < 50s

example:
  iteration_1:
    hypothesis: "Auth in src/auth/"
    action: Glob "src/auth/**/*.ts"
    feedback: "Found 8 files" (2s)
    decision: "Look promising, investigate"

  iteration_2:
    hypothesis: "Main auth logic in service file"
    action: Grep "class.*Service" in src/auth/
    feedback: "Found AuthService" (2s)
    decision: "Read this file"

  iteration_3:
    action: Read src/auth/auth.service.ts (first 100 lines)
    feedback: "Confirmed JWT authentication" (2s)
    decision: "Found it!"

  total_time: 6s to high confidence
```

### Pattern 2: Checkpoint-Driven Execution

```yaml
use_case: "Long-running analysis"

checkpoint_strategy:
  every_10_seconds:
    - Checkpoint progress
    - Report findings so far
    - Verify still on track

example:
  minute_1: Analyzed API routes → Report
  minute_2: Analyzed services → Report
  minute_3: Analyzed models → Report

  benefit: Can course-correct at each checkpoint
```

### Pattern 3: Fail-Fast Cascade

```yaml
use_case: "Validation chain"

cascade_structure:
  validation_1: Input schema (< 1ms)
    if_fail: Return immediately

  validation_2: File exists (< 100ms)
    if_fail: Return immediately

  validation_3: File readable (< 500ms)
    if_fail: Return immediately

  work: Process file (5s)

benefit: Never waste time on invalid inputs
```

---

## Feedback Anti-Patterns

### 1. No Early Validation
```yaml
❌ ANTI-PATTERN:
  approach:
    - Start expensive operation
    - Discover input invalid after 30s
    - Waste user's time

✓ PATTERN:
  approach:
    - Validate immediately (< 1s)
    - Fail fast if invalid
    - Save 29s of wasted work
```

### 2. Silent Execution
```yaml
❌ ANTI-PATTERN:
  agent_runs_for_2_minutes:
    - No progress updates
    - No intermediate results
    - User doesn't know if it's working

✓ PATTERN:
  agent_provides_feedback:
    - Progress every 15-20s
    - Intermediate findings
    - User confidence maintained
```

### 3. Ignoring Negative Feedback
```yaml
❌ ANTI-PATTERN:
  search_1: No results
  search_2: No results (try again)
  search_3: No results (try harder)
  search_4: No results (keep trying)
  # Never admits pattern not found

✓ PATTERN:
  search_1: No results
  search_2: No results (refine approach)
  search_3: No results
  conclusion: "Pattern not found in scope, suggest alternatives"
```

### 4. Batching Too Much Work
```yaml
❌ ANTI-PATTERN:
  task: "Analyze 20 modules, report at end"
  time: 5 minutes
  feedback: Single report after 5 minutes

✗ Problem: No way to know if on right track

✓ PATTERN:
  task: "Analyze 20 modules, report per module"
  feedback_every: 15s
  benefit: Can interrupt and redirect
```

---

## Feedback Metrics

### Velocity Metrics
```yaml
time_to_first_feedback:
  target: < 5s
  measure: Time from agent start to first output
  optimization: Emit progress immediately

feedback_frequency:
  target: Every 15-20s for long tasks
  measure: Time between progress updates
  optimization: Checkpoint regularly

time_to_failure_detection:
  target: < 10s
  measure: Time to discover task will fail
  optimization: Validate early, fail fast
```

### Quality Metrics
```yaml
first_attempt_success_rate:
  target: > 80%
  measure: % of tasks succeeding without retry
  improvement: Better hypothesis formation

false_positive_rate:
  target: < 10%
  measure: % of "success" reports that were wrong
  improvement: Better validation

user_interruption_rate:
  target: < 15%
  measure: % of tasks user stops mid-execution
  cause: Wrong direction, poor feedback
  improvement: More frequent checkpoints
```

---

## Feedback in Different Agent Types

### Discovery Agents
```yaml
feedback_pattern: "Progressive narrowing"

example:
  step_1: "Searching for auth patterns..." (Start: 0s)
  step_2: "Found 15 candidates..." (Feedback: 5s)
  step_3: "Narrowed to 3 likely files..." (Feedback: 10s)
  step_4: "Confirmed: src/auth/service.ts" (Complete: 15s)

benefit: User sees progression toward answer
```

### Implementation Agents
```yaml
feedback_pattern: "Checkpoint verification"

example:
  step_1: "Reading existing patterns..." (Start: 0s)
  step_2: "Patterns understood, designing..." (Feedback: 20s)
  step_3: "Writing implementation..." (Feedback: 40s)
  step_4: "Self-verification..." (Feedback: 70s)
  step_5: "Complete, tests pass" (Complete: 90s)

benefit: Confidence at each stage
```

### Review Agents
```yaml
feedback_pattern: "Incremental findings"

example:
  step_1: "Reviewing module 1..." (Start: 0s)
  step_2: "Module 1: 2 issues found" (Feedback: 8s)
  step_3: "Reviewing module 2..." (Feedback: 9s)
  step_4: "Module 2: Clean" (Feedback: 15s)
  step_5: "Complete: 2 issues total" (Complete: 20s)

benefit: Issues reported as found, not batched
```

---

## Practical Checklist

### Before Starting Work:
- [ ] Validate all inputs (< 1s)
- [ ] Verify files/resources exist (< 1s)
- [ ] Check permissions/access (< 1s)
- [ ] Emit "starting" message immediately

### During Execution:
- [ ] Report progress every 15-20s
- [ ] Checkpoint after each major step
- [ ] Fail fast on errors (don't continue)
- [ ] Emit intermediate findings

### After Completion:
- [ ] Report success/failure clearly
- [ ] Include relevant metrics (time, tokens)
- [ ] Provide actionable next steps
- [ ] Log for future optimization

---

## References

- **Modern Software Engineering** by Dave Farley
  - Chapter 5: Feedback (Core principles)
  - Chapter 8: Experimental (Hypothesis testing)
  - Chapter 6: Incrementalism (Small batches)

- **Related Guidelines**:
  - `velocity-principles.md`: Fast feedback enables velocity
  - `context-management.md`: Less context = faster feedback
  - `orchestration-principles.md`: Feedback in multi-agent systems
