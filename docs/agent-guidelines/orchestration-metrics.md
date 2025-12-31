# Orchestration Metrics

**Foundation**: Measure What Matters, Improve Continuously

---

## Core Philosophy

> "Use measures of sensible outcomes to evaluate any change."
> — Modern Software Engineering

**You can't improve what you don't measure.** Define clear metrics, track them consistently, act on insights.

---

## DORA Metrics for Agents

### The Four Key Metrics (Adapted for Agents)

#### 1. Deployment Frequency → Agent Execution Frequency

```yaml
metric: "How often do we successfully execute agents?"

measurement:
  - Count: Agent executions per day
  - Target: > 20 executions/day (active development)
  - Elite: > 50 executions/day

interpretation:
  high: Fast iteration, frequent feedback
  low: Bottlenecks or low activity

improvement_areas:
  - Reduce agent spawn overhead
  - Optimize for quick tasks (< 30s)
  - Make agents more discoverable
```

#### 2. Lead Time for Changes → Agent Task Completion Time

```yaml
metric: "How long from task start to completion?"

measurement:
  - Median: Time from agent spawn to result
  - Target: < 60s for typical tasks
  - Elite: < 30s for typical tasks

breakdown:
  - p50 (median): 30s
  - p75: 45s
  - p90: 75s
  - p99: 150s

interpretation:
  fast: Efficient agents, good tool usage
  slow: Bottlenecks, poor optimization

improvement_areas:
  - Optimize context loading
  - Improve tool selection
  - Parallelize where possible
```

#### 3. Time to Restore → Agent Failure Recovery Time

```yaml
metric: "How quickly can we recover from agent failures?"

measurement:
  - Time from failure detection to successful retry
  - Target: < 15s
  - Elite: < 5s

failure_modes:
  - Invalid input: 2s (validation error)
  - Tool failure: 5s (retry with different approach)
  - Timeout: 10s (spawn new agent with adjusted params)
  - Logic error: 30s (requires human intervention)

interpretation:
  fast: Good error handling, clear feedback
  slow: Poor diagnostics, manual fixes needed

improvement_areas:
  - Better input validation (fail fast)
  - Automatic retry logic
  - Clear error messages
  - Fallback strategies
```

#### 4. Change Failure Rate → Agent Success Rate

```yaml
metric: "What % of agent executions succeed on first attempt?"

measurement:
  - Success rate: (Successful / Total Executions) × 100
  - Target: > 85% first-attempt success
  - Elite: > 95% first-attempt success

categories:
  - Complete success: 85%
  - Partial success: 10%
  - Failure: 5%

interpretation:
  high_success: Well-designed agents, good prompts
  low_success: Poor task decomposition, ambiguous instructions

improvement_areas:
  - Clearer success criteria
  - Better input validation
  - Improved agent prompts
  - Task decomposition refinement
```

---

## Velocity Metrics

### Throughput Metrics

```yaml
tasks_per_hour:
  measurement: "Number of agent tasks completed/hour"
  target: > 30 tasks/hour (active dev)
  calculation: Total_Completions / Hours

agent_utilization:
  measurement: "% of time agents are actively working"
  formula: Active_Time / Total_Time
  target: > 75%
  problems_if_low:
    - Too much coordination
    - Waiting for sequential tasks
    - Over-orchestration

parallel_efficiency:
  measurement: "Speedup from parallelization"
  formula: Sequential_Time / Parallel_Time
  target: > 1.5× for parallelizable tasks
  elite: > 2.0×
```

### Latency Metrics

```yaml
agent_spawn_latency:
  measurement: "Time to spawn and initialize agent"
  target: < 2s
  p50: 1.5s
  p99: 3s

first_output_latency:
  measurement: "Time from spawn to first output"
  target: < 5s
  interpretation: "User sees progress quickly"

tool_call_latency:
  by_tool:
    Read: < 1s (p50)
    Grep: < 3s (p50)
    Glob: < 2s (p50)
    DeepContext: < 8s (p50)
    Bash: Variable (depends on command)
```

---

## Quality Metrics

### Correctness Metrics

```yaml
accuracy_rate:
  measurement: "% of agent outputs that are correct"
  target: > 95%
  verification: Manual review sampling

false_positive_rate:
  measurement: "% of reported issues that aren't real"
  target: < 10%
  important_for: Review agents

false_negative_rate:
  measurement: "% of real issues missed"
  target: < 15%
  important_for: Security, architecture reviews

precision_recall:
  precision: True_Positives / (True_Positives + False_Positives)
  recall: True_Positives / (True_Positives + False_Negatives)
  target: F1 > 0.85
```

### Reliability Metrics

```yaml
retry_rate:
  measurement: "Average retries per task"
  formula: Total_Retries / Total_Tasks
  target: < 1.3 (most tasks succeed first time)

timeout_rate:
  measurement: "% of agents that timeout"
  target: < 5%
  causes: Poor time budgets, inefficient operations

cascading_failure_rate:
  measurement: "% of failures causing downstream failures"
  target: < 10%
  indicates: Poor error isolation
```

---

## Efficiency Metrics

### Resource Utilization

```yaml
token_efficiency:
  measurement: "Tokens used / Task value delivered"
  formula: Total_Tokens / Tasks_Completed
  target: < 50,000 tokens/task (typical)

  breakdown:
    simple_task: < 10,000 tokens
    medium_task: 10,000-30,000 tokens
    complex_task: 30,000-80,000 tokens

context_waste_rate:
  measurement: "% of loaded context actually used"
  formula: (Tokens_Used / Tokens_Loaded) × 100
  target: > 70%
  problems_if_low: Loading too much context

tool_efficiency:
  measurement: "Average tools per task"
  target: < 5 tool calls
  elite: < 3 tool calls
  problems_if_high: Inefficient exploration
```

### Cost Metrics

```yaml
cost_per_task:
  measurement: "Average cost per completed task"
  factors:
    - Token usage (input + output)
    - Model used (haiku vs sonnet vs opus)
    - Tool costs

  typical_costs:
    simple: $0.01 - $0.05
    medium: $0.05 - $0.15
    complex: $0.15 - $0.50

cost_efficiency_ratio:
  formula: Value_Delivered / Cost
  interpretation: "ROI of agent executions"
```

---

## Orchestration-Specific Metrics

### Coordination Metrics

```yaml
coordination_overhead:
  formula: (Coordination_Time / Total_Time) × 100
  target: < 20%
  warning: > 30%

  breakdown:
    agent_spawn: Time to spawn agents
    message_passing: Inter-agent communication
    result_aggregation: Combining results
    synchronization: Waiting at barriers

agent_idle_time:
  measurement: "Time agents wait unnecessarily"
  formula: Sum(Wait_Time) / Total_Agent_Time
  target: < 15%
  causes:
    - Poor parallelization
    - Over-synchronization
    - Resource contention
```

### Composition Metrics

```yaml
reuse_rate:
  measurement: "% of tasks using existing agents"
  formula: (Reused_Agents / Total_Agent_Uses) × 100
  target: > 70%
  interpretation: "High reuse = good abstractions"

composition_depth:
  measurement: "Levels of agent nesting"
  target: ≤ 3 levels
  warning: > 4 levels (over-orchestration)

  example:
    level_1: Main agent
    level_2: Spawned sub-agents
    level_3: Sub-agents spawn workers (OK)
    level_4: Workers spawn more agents (WARNING)
```

---

## Metric Collection Strategies

### Instrumentation Points

```yaml
agent_lifecycle:
  on_spawn:
    - Record spawn time
    - Log agent type
    - Note task description

  on_tool_call:
    - Record tool type
    - Measure latency
    - Track token usage

  on_completion:
    - Record completion time
    - Log success/failure
    - Calculate duration
    - Measure token usage

  on_failure:
    - Record failure mode
    - Capture error details
    - Note retry attempts
```

### Aggregation Strategy

```yaml
time_windows:
  realtime: Last 5 minutes (for monitoring)
  hourly: Last hour (for debugging)
  daily: Last 24 hours (for trends)
  weekly: Last 7 days (for patterns)

aggregation_functions:
  - count: Total executions
  - sum: Total tokens, time
  - avg: Average duration, tokens
  - percentiles: p50, p75, p90, p95, p99
  - rate: Executions per hour
```

---

## Monitoring Dashboards

### Real-Time Dashboard

```yaml
widgets:
  current_agents:
    - Active agents: 3
    - Queued tasks: 2
    - Failed (last hour): 1

  performance_now:
    - Avg completion: 32s
    - Token usage rate: 15k/min
    - Success rate: 89%

  alerts:
    - [WARNING] High token usage
    - [INFO] 5 agents completed
```

### Trends Dashboard

```yaml
charts:
  success_rate_over_time:
    - Last 7 days
    - Target line: 85%
    - Actual: Trending at 87% ✓

  completion_time_distribution:
    - p50: 28s
    - p75: 45s
    - p90: 72s
    - p99: 135s

  cost_over_time:
    - Daily cost: $12.50
    - Weekly cost: $87.50
    - Trend: Stable
```

---

## Improvement Workflows

### Metric-Driven Optimization

```yaml
workflow:
  1. Identify_Bottleneck:
      - Review dashboard
      - Find worst metric
      - Investigate root cause

  2. Form_Hypothesis:
      - "High token usage due to reading full files"
      - "Low success rate from unclear prompts"

  3. Implement_Fix:
      - Change agent behavior
      - Update prompts
      - Optimize tools

  4. Measure_Impact:
      - Compare before/after metrics
      - Validate hypothesis
      - Iterate if needed

example:
  problem: "Agent completion time p90 = 120s (target: 75s)"
  hypothesis: "Too much sequential work, should parallelize"
  fix: "Decompose into 3 parallel subtasks"
  result: "p90 = 65s (13% better than target)"
```

---

## Alerting Rules

### Critical Alerts

```yaml
agent_timeout_spike:
  condition: Timeout_Rate > 15%
  severity: Critical
  action: "Investigate immediately, likely systemic issue"

success_rate_drop:
  condition: Success_Rate < 70%
  severity: Critical
  action: "Check for breaking changes in agents or tools"

cost_explosion:
  condition: Hourly_Cost > 2× baseline
  severity: Critical
  action: "Identify runaway agents, check for loops"
```

### Warning Alerts

```yaml
slow_completion:
  condition: p90_Time > 90s
  severity: Warning
  action: "Review agent efficiency, consider optimization"

high_retry_rate:
  condition: Retry_Rate > 1.5
  severity: Warning
  action: "Check for intermittent failures"
```

---

## Benchmarking

### Baseline Metrics (Global1SIM)

```yaml
typical_agent_performance:
  code_explorer:
    duration: 20-30s
    success_rate: 92%
    tokens: 8,000

  code_architect:
    duration: 30-45s
    success_rate: 88%
    tokens: 12,000

  feature_implementer:
    duration: 60-90s
    success_rate: 85%
    tokens: 25,000

  code_reviewer:
    duration: 25-40s
    success_rate: 94%
    tokens: 10,000
```

---

## Continuous Improvement

### Weekly Review

```yaml
agenda:
  1. Review_Key_Metrics:
      - DORA metrics
      - Velocity metrics
      - Quality metrics

  2. Identify_Trends:
      - Improving: Celebrate and understand why
      - Degrading: Investigate root causes

  3. Prioritize_Improvements:
      - Biggest impact on velocity
      - Lowest effort to implement

  4. Experiment:
      - Try new approaches
      - Measure impact
      - Keep what works
```

---

## References

- **Modern Software Engineering** by Dave Farley
  - Chapter 7: Empiricism (measurement-driven improvement)
  - Chapter 8: Experimental (hypothesis testing)
  - Accelerate book: DORA metrics foundation

- **Related Guidelines**:
  - `velocity-principles.md`: What metrics optimize for
  - `feedback-optimization.md`: Metrics for feedback loops
  - `orchestration-principles.md`: Multi-agent metrics
