# Parallel Execution Test Plan Template

**Date**: [YYYY-MM-DD]
**Purpose**: Verify parallel execution patterns work correctly with implemented agents
**Pattern Tested**: [Pattern Name - e.g., Scatter-Gather, Parallel Pipelines, Fan-out/Fan-in]
**Test ID**: [Unique identifier for this test run]

---

## Test Scenario

**Objective**: [Describe what you're testing - e.g., "Analyze Global1SIM codebase architecture using multiple agents in parallel"]

### Agents Used

1. **[agent-name-1]** ([NEW/EXISTING]) - [Purpose and scope]
2. **[agent-name-2]** ([NEW/EXISTING]) - [Purpose and scope]
3. **[agent-name-3]** ([NEW/EXISTING]) - [Purpose and scope]

### Independence Verification

```yaml
independence_test:
  q1_can_run_without_others: [YES/NO]
    - [Reason 1: e.g., "Each agent has disjoint scope"]
    - [Reason 2: e.g., "No shared mutable state"]
    - [Reason 3: e.g., "Results independent"]

  q2_share_readonly_context: [YES/NO]
    - [Details: e.g., "All read from same codebase (read-only)"]
    - [Details: e.g., "No writes during analysis"]
    - [Details: e.g., "Safe parallel access"]

  q3_results_combinable: [YES/NO]
    - [How: e.g., "All produce structured reports"]
    - [How: e.g., "Can merge in any order"]
    - [How: e.g., "No ordering dependencies"]

  q4_coordination_overhead: [YES/NO - Is overhead acceptable?]
    - Spawn: [ESTIMATE]
    - Gather: [ESTIMATE]
    - Total overhead: [ESTIMATE] ([PERCENTAGE]% of sequential time)
    - Threshold: < 20% [✓/✗]
```

### Expected Performance

```yaml
sequential_approach:
  agent_1_time: [TIME] ([brief description])
  agent_2_time: [TIME] ([brief description])
  agent_3_time: [TIME] ([brief description])
  total_sequential: [SUM]

parallel_approach:
  max_agent_time: [TIME] (longest running agent)
  coordination_overhead: [TIME] (spawn + gather)
  total_parallel: [CALCULATION]

expected_speedup: [sequential / parallel] = [X.XX]×
worthwhile_threshold: > 1.3× [✓/✗]
```

---

## Test Execution Plan

### Phase 1: Baseline (Sequential)
**Purpose**: Establish baseline performance

```bash
# Test 1: Run [agent-1] on [scope] (sequential)
# Expected: [TIME]

# Test 2: Run [agent-2] on [scope] (sequential)
# Expected: [TIME]

# Test 3: Run [agent-3] on [scope] (sequential)
# Expected: [TIME]

# Total Sequential: [SUM]
```

**Execution Instructions**:
1. [Step-by-step instructions for running sequential baseline]
2. [Include exact prompts or commands]
3. [Note timing measurements to capture]

### Phase 2: Parallel Execution
**Purpose**: Verify agents work correctly in parallel

```yaml
# Single message with N Task calls (parallel spawn)
parallel_test:
  spawn_all_at_once:
    - Task([agent-1], prompt="[Exact prompt]")
    - Task([agent-2], prompt="[Exact prompt]")
    - Task([agent-3], prompt="[Exact prompt]")

  verification:
    - All N agents start simultaneously
    - No interference between agents
    - All complete successfully
    - Results are correct and complete
```

**Execution Instructions**:
1. [Exact prompt to trigger parallel execution]
2. [What to observe during execution]
3. [How to verify parallelism occurred]

### Phase 3: Result Verification
**Purpose**: Ensure parallel results match sequential quality

```yaml
quality_checks:
  - [ ] [Agent-1] produces expected output (describe what)
  - [ ] [Agent-2] produces expected output (describe what)
  - [ ] [Agent-3] produces expected output (describe what)
  - [ ] No duplicate work between agents
  - [ ] No missing information
  - [ ] Results are combinable without conflicts
  - [ ] Completeness: [Percentage or description]
```

---

## Actual Results

### Test Run 1: Sequential Baseline

**Execution Date/Time**: [YYYY-MM-DD HH:MM]
**Executor**: [Who/What ran the test]

```yaml
agent: [agent-1-name]
scope: [scope]
time: [MEASURED]
findings: [COUNT/DESCRIPTION]
status: [PASS/FAIL]
notes: [Any observations]

agent: [agent-2-name]
scope: [scope]
time: [MEASURED]
findings: [COUNT/DESCRIPTION]
status: [PASS/FAIL]
notes: [Any observations]

agent: [agent-3-name]
scope: [scope]
time: [MEASURED]
findings: [COUNT/DESCRIPTION]
status: [PASS/FAIL]
notes: [Any observations]

total_sequential_time: [SUM]
```

### Test Run 2: Parallel Execution

**Execution Date/Time**: [YYYY-MM-DD HH:MM]
**Executor**: [Who/What ran the test]

```yaml
spawn_time: [MEASURED]
max_agent_time: [MEASURED] ([which agent])
gather_time: [MEASURED]
total_parallel_time: [CALCULATED]

actual_speedup: [sequential / parallel] = [X.XX]×
overhead_percentage: [(spawn + gather) / total_parallel * 100] = [XX]%

vs_expected:
  expected_speedup: [X.XX]×
  actual_speedup: [X.XX]×
  variance: [±XX]%
```

### Quality Verification

```yaml
[agent-1]_results:
  files_found: [COUNT]
  patterns_identified: [COUNT]
  completeness: [PERCENTAGE]
  key_findings: [SUMMARY]

[agent-2]_results:
  files_found: [COUNT]
  violations_found: [COUNT]
  compliance_rate: [PERCENTAGE]
  key_findings: [SUMMARY]

[agent-3]_results:
  files_found: [COUNT]
  patterns_identified: [COUNT]
  completeness: [PERCENTAGE]
  key_findings: [SUMMARY]

combined_report:
  duplicates: [COUNT - should be 0]
  gaps: [COUNT - should be 0]
  overall_quality: [RATING/DESCRIPTION]
  combinability: [DESCRIPTION]
```

---

## Performance Metrics

```yaml
velocity_metrics:
  sequential_throughput: [tasks/minute]
  parallel_throughput: [tasks/minute]
  efficiency_gain: [PERCENTAGE] improvement

coordination_metrics:
  spawn_overhead: [SECONDS]
  gather_overhead: [SECONDS]
  total_overhead: [SECONDS]
  overhead_percentage: [PERCENTAGE]

resource_metrics:
  peak_parallel_agents: [COUNT]
  token_usage_sequential: [TOTAL tokens]
  token_usage_parallel: [TOTAL tokens]
  token_efficiency: [RATIO]× ([PERCENTAGE] token savings)

comparison_to_targets:
  parallelism_factor: [ACTUAL]× vs [TARGET]× ✓/✗
  coordination_overhead: [ACTUAL]% vs < 20% ✓/✗
  speedup: [ACTUAL]× vs > 1.3× ✓/✗
```

---

## Pattern Validation

### ✓ Pattern Elements Checklist

```yaml
[pattern_name]_phase_1:
  - [ ] [Element 1 - e.g., "Single message with multiple Task calls"]
  - [ ] [Element 2 - e.g., "Independent scopes (no overlap)"]
  - [ ] [Element 3 - e.g., "No inter-agent communication"]
  - [ ] [Element 4 - e.g., "Read-only shared context"]

[pattern_name]_phase_2:
  - [ ] [Element 1 - e.g., "Collect all results"]
  - [ ] [Element 2 - e.g., "Merge without conflicts"]
  - [ ] [Element 3 - e.g., "Synthesize unified view"]
  - [ ] [Element 4 - e.g., "No data loss"]

independence_verification:
  - [ ] Agents don't wait for each other
  - [ ] No shared mutable state
  - [ ] Results order-independent
  - [ ] Failures isolated (one agent failing doesn't block others)
```

---

## Issues Discovered

### Blockers
- [ ] [Issue description]

### Performance Issues
- [ ] Coordination overhead > 20%? [YES/NO - details]
- [ ] Agents taking longer than expected? [YES/NO - details]
- [ ] Resource contention? [YES/NO - details]
- [ ] [Other performance issue]

### Quality Issues
- [ ] Incomplete results? [YES/NO - details]
- [ ] Duplicate findings? [YES/NO - details]
- [ ] Agent interference? [YES/NO - details]
- [ ] [Other quality issue]

### Observations
- [Observation 1]
- [Observation 2]
- [Observation 3]

---

## Recommendations

Based on test results:

### ✅ DO Use [Pattern Name] When:
- [Use case 1]
- [Use case 2]
- [Use case 3]
- [Criteria: e.g., "Coordination overhead < 20%"]
- [Criteria: e.g., "Expected speedup > 1.3×"]

### ⚠️ DON'T Use [Pattern Name] When:
- [Anti-pattern 1]
- [Anti-pattern 2]
- [Anti-pattern 3]

### Optimization Opportunities
- [Opportunity 1 - what could be improved]
- [Opportunity 2 - what could be improved]

---

## Next Tests

Based on this test, recommend:

1. **[Next Pattern Name]**
   - [Description]
   - [Expected benefit]

2. **[Variation of Current Pattern]**
   - [What to change]
   - [What to measure]

3. **[Related Pattern]**
   - [Description]
   - [Prerequisites]

---

## Conclusion

**[Pattern Name] Status**: [PASS/FAIL/PARTIAL]

**Key Findings**:
- Actual speedup: [X.XX]×
- Coordination overhead: [XX]%
- Quality maintained: [YES/NO]
- Token efficiency: [Description]

**Ready for Production**: [YES/NO/CONDITIONAL]

**Conditions for Production Use** (if conditional):
- [Condition 1]
- [Condition 2]

**Recommended Use Cases**:
1. [Use case 1 - specific scenario]
2. [Use case 2 - specific scenario]
3. [Use case 3 - specific scenario]

**Success Criteria Met**:
- [ ] Speedup > 1.3× (achieved [X.XX]×)
- [ ] Overhead < 20% (achieved [XX]%)
- [ ] Quality maintained ([PERCENTAGE]% completeness)
- [ ] No interference between agents
- [ ] Results combinable

---

## Appendix: Test Execution Guide

### Prerequisites
- [Prerequisite 1 - e.g., "Agents must be implemented"]
- [Prerequisite 2 - e.g., "Test data must exist"]
- [Prerequisite 3 - e.g., "Clean context window recommended"]

### Exact User Prompt (Copy-Paste Ready)

```
[EXACT PROMPT TEXT TO TRIGGER PARALLEL EXECUTION]

Example:
"Analyze the Global1SIM codebase using parallel agents:

1. Use code-explorer to analyze [scope-1]
2. Use [agent-2] to [task-2] in [scope-2]
3. Use [agent-3] to [task-3] in [scope-3]

Run these N agents in parallel and combine their findings into a unified report."
```

### Expected System Behavior

```yaml
step_1_spawn:
  action: "Main agent spawns N subagents in single message"
  time: [ESTIMATE]
  verification: "All N Task() calls in same message"

step_2_execute:
  action: "Agents run simultaneously"
  agent_1_time: [ESTIMATE]
  agent_2_time: [ESTIMATE]
  agent_3_time: [ESTIMATE]
  wall_clock_time: [MAX] (max of parallel tasks)

step_3_gather:
  action: "Main agent collects results"
  time: [ESTIMATE]
  verification: "All results available"

step_4_synthesize:
  action: "Main agent combines findings"
  time: [ESTIMATE]
  output: "[Description of expected output]"
```

### Troubleshooting

#### If Agents Run Sequentially
**Problem**: Agents execute one after another
**Cause**: [Likely cause]
**Fix**: [How to fix]

#### If Results Incomplete
**Problem**: Missing findings in combined report
**Cause**: [Likely cause]
**Fix**: [How to fix]

#### If Performance Poor
**Problem**: Parallel slower than sequential
**Cause**: [Likely cause]
**Fix**: [How to fix]

---

## Test Metadata

**Test Status**: [PLANNED/IN PROGRESS/COMPLETED/ARCHIVED]
**Test Executor**: [Name/Role]
**Test Date**: [YYYY-MM-DD]
**Pattern Tested**: [Pattern number and name]
**Agents Tested**: [List]
**Related Documents**:
- Test results file: `test-results/[YYYY-MM-DD]-[test-id].md`
- Agent definitions: `.claude/agents/[agent-names]/`
- Pattern documentation: `parallel-execution-patterns.md`

**Maintainer**: [Team/Person]
**Last Updated**: [YYYY-MM-DD]
**Next Review**: [YYYY-MM-DD or condition]
