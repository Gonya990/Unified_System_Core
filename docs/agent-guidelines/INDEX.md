# Agent Guidelines - Navigation Index

**Quick Links**: [Core Guidelines](#core-guidelines) | [Templates](#templates) | [Test Results](#test-results) | [Implementation Guides](#implementation-guides)

---

## 📚 Core Guidelines

Foundational principles and patterns for agent development and orchestration.

### Individual Agent Design
- **[velocity-principles.md](./velocity-principles.md)** - Individual agent speed and efficiency
  - Topics: Small batches, fast feedback, progressive disclosure, hypothesis-driven execution
  - Use when: Designing new agents, optimizing performance, debugging slow agents

- **[agent-capability-patterns.md](./agent-capability-patterns.md)** - Specialized agent types and boundaries
  - Topics: 5 agent categories, capability matrix, composition patterns
  - Use when: Creating agent types, defining responsibilities, preventing capability creep

- **[context-management.md](./context-management.md)** - Token efficiency and context optimization
  - Topics: Context budgets, progressive disclosure, selective reading, handoff patterns
  - Use when: Optimizing token usage, preventing context bloat, managing large codebases

- **[feedback-optimization.md](./feedback-optimization.md)** - Fast feedback at every level
  - Topics: Feedback hierarchy (5 levels), fail-fast, progressive validation
  - Use when: Reducing latency, implementing validation, designing error handling

### Multi-Agent Coordination
- **[orchestration-principles.md](./orchestration-principles.md)** - Multi-agent coordination and composition
  - Topics: Orchestration hierarchy, core patterns (pipeline, scatter-gather, etc.)
  - Use when: Coordinating multiple agents, designing complex workflows

- **[parallel-execution-patterns.md](./parallel-execution-patterns.md)** - Concurrent agent execution
  - Topics: Independence test, 4 patterns (scatter-gather, pipelines, fan-out, map-reduce)
  - Use when: Speeding up independent tasks, designing concurrent workflows

### Measurement & Improvement
- **[orchestration-metrics.md](./orchestration-metrics.md)** - Measurement and continuous improvement
  - Topics: DORA metrics, velocity/quality/efficiency metrics, monitoring
  - Use when: Establishing baselines, tracking performance, continuous improvement

---

## 🎯 Implementation Guides

Step-by-step guides for implementing specific patterns and workflows.

- **[IMPLEMENTATION.md](./IMPLEMENTATION.md)** - Orchestration patterns implementation guide
  - Topics: 5 orchestration levels (0-4), decision trees, examples
  - Use when: Implementing multi-agent workflows, choosing orchestration approach

- **[README.md](./README.md)** - Framework overview and status
  - Topics: Philosophy, structure, metrics dashboard, roadmap, version history
  - Start here: Comprehensive overview of the entire framework

---

## 📋 Templates

Reusable templates for creating agents and running tests.

### Agent Creation
- **[templates/AGENT_TEMPLATE.md](./AGENT_TEMPLATE.md)** - Standard agent creation template
  - Use: Copy this to create new agent guideline files
  - Sections: Purpose, capabilities, workflow, constraints, metrics

### Testing & Validation
- **[templates/PARALLEL_EXECUTION_TEST_TEMPLATE.md](./templates/PARALLEL_EXECUTION_TEST_TEMPLATE.md)** - Parallel execution test plan
  - Use: Plan and execute parallel execution tests
  - Sections: Scenario, independence verification, execution plan, results, metrics

- **[PARALLEL_EXECUTION_DEMO.md](./PARALLEL_EXECUTION_DEMO.md)** - Scatter-gather demonstration guide
  - Use: Walkthrough for testing scatter-gather pattern
  - Status: Demo script with expected outcomes

---

## 📊 Test Results

Actual test execution results with performance data.

### 2025-11-16
- **[test-results/2025-11-16-scatter-gather-pattern.md](./test-results/2025-11-16-scatter-gather-pattern.md)** - Scatter-gather parallel execution test
  - Pattern: Scatter-Gather (Pattern 4)
  - Agents: code-explorer (2×), hexagonal-architecture-guardian
  - Results: ✅ PASS - 1.75× speedup, 2% overhead, 68% token savings
  - Status: Production-ready for multi-module analysis

### Summary Reports
- **[TEST_RESULTS_2025-11-16.md](../../TEST_RESULTS_2025-11-16.md)** - Comprehensive test summary (root level)
  - All test details, findings, and metrics from 2025-11-16 session

---

## 📝 Session Summaries

Documentation of development sessions and progress.

- **[SESSION_2025-11-16_SUMMARY.md](./SESSION_2025-11-16_SUMMARY.md)** - Agent creation session summary
  - Created: code-explorer, code-reviewer agents
  - Status: Test plans created, execution completed

---

## 🗂️ Directory Structure

```
docs/agent-guidelines/
├── INDEX.md (this file)                         # Navigation hub
├── README.md                                    # Framework overview and status
│
├── Core Guidelines/
│   ├── velocity-principles.md
│   ├── orchestration-principles.md
│   ├── agent-capability-patterns.md
│   ├── context-management.md
│   ├── feedback-optimization.md
│   ├── parallel-execution-patterns.md
│   └── orchestration-metrics.md
│
├── Implementation Guides/
│   ├── IMPLEMENTATION.md
│   ├── PARALLEL_EXECUTION_DEMO.md
│   └── SESSION_2025-11-16_SUMMARY.md
│
├── templates/
│   ├── AGENT_TEMPLATE.md                       # Agent creation template
│   └── PARALLEL_EXECUTION_TEST_TEMPLATE.md     # Test plan template
│
└── test-results/
    └── 2025-11-16-scatter-gather-pattern.md   # Actual test results
```

---

## 🔍 Quick Reference

### For Humans

**I want to...**
- Create a new agent → [AGENT_TEMPLATE.md](./AGENT_TEMPLATE.md)
- Make agents faster → [velocity-principles.md](./velocity-principles.md)
- Run multiple agents → [orchestration-principles.md](./orchestration-principles.md)
- Run agents in parallel → [parallel-execution-patterns.md](./parallel-execution-patterns.md)
- Test parallel execution → [templates/PARALLEL_EXECUTION_TEST_TEMPLATE.md](./templates/PARALLEL_EXECUTION_TEST_TEMPLATE.md)
- Reduce token usage → [context-management.md](./context-management.md)
- Measure performance → [orchestration-metrics.md](./orchestration-metrics.md)
- Understand the framework → [README.md](./README.md)

### For Agents

**Route to appropriate guideline based on task:**

```yaml
task_type:
  create_agent: templates/AGENT_TEMPLATE.md
  optimize_speed: velocity-principles.md
  coordinate_agents: orchestration-principles.md
  run_parallel: parallel-execution-patterns.md
  test_parallel: templates/PARALLEL_EXECUTION_TEST_TEMPLATE.md
  manage_context: context-management.md
  measure_performance: orchestration-metrics.md

agent_category:
  discovery: agent-capability-patterns.md#discovery-agents
  architecture: agent-capability-patterns.md#architecture-agents
  implementation: agent-capability-patterns.md#implementation-agents
  review: agent-capability-patterns.md#review-agents
  execution: agent-capability-patterns.md#execution-agents

pattern_selection:
  single_task: IMPLEMENTATION.md#level-1-direct-tool-usage
  single_agent: IMPLEMENTATION.md#level-2-single-subagent
  sequential: IMPLEMENTATION.md#level-3-sequential-pipeline
  parallel: parallel-execution-patterns.md
  hierarchical: IMPLEMENTATION.md#level-4-hierarchical-coordination
```

---

## 📖 Reading Order

### For New Users

1. **[README.md](./README.md)** - Start here for overview
2. **[velocity-principles.md](./velocity-principles.md)** - Core principles for fast agents
3. **[agent-capability-patterns.md](./agent-capability-patterns.md)** - Agent types and boundaries
4. **[orchestration-principles.md](./orchestration-principles.md)** - Multi-agent coordination
5. **[IMPLEMENTATION.md](./IMPLEMENTATION.md)** - Practical implementation guide

### For Implementing Parallel Execution

1. **[parallel-execution-patterns.md](./parallel-execution-patterns.md)** - Theory and patterns
2. **[PARALLEL_EXECUTION_DEMO.md](./PARALLEL_EXECUTION_DEMO.md)** - Walkthrough example
3. **[templates/PARALLEL_EXECUTION_TEST_TEMPLATE.md](./templates/PARALLEL_EXECUTION_TEST_TEMPLATE.md)** - Test plan template
4. **[test-results/2025-11-16-scatter-gather-pattern.md](./test-results/2025-11-16-scatter-gather-pattern.md)** - Real results

### For Creating New Agents

1. **[agent-capability-patterns.md](./agent-capability-patterns.md)** - Choose agent category
2. **[velocity-principles.md](./velocity-principles.md)** - Speed and efficiency principles
3. **[templates/AGENT_TEMPLATE.md](./AGENT_TEMPLATE.md)** - Fill out template
4. **[context-management.md](./context-management.md)** - Optimize token usage
5. **[feedback-optimization.md](./feedback-optimization.md)** - Fast feedback loops

---

## 🎯 Current Status (v1.3 - 2025-11-16)

- **Documentation**: ✅ 100% (7 core guidelines + 3 implementation guides)
- **Agents**: ✅ 50% (6/12 created, all tested)
- **Parallel Execution**: ✅ Validated (Pattern 4 - scatter-gather)
- **Metrics**: 🚧 Baseline Established (actual performance data captured)

**Latest Update**: Parallel execution validation completed with 1.75× speedup, 2% overhead, 68% token savings.

---

## 📞 Support

- **Framework Location**: `/home/user/global1sim/docs/agent-guidelines/`
- **Agent Definitions**: `/.claude/agents/`
- **Test Results**: `/home/user/global1sim/docs/agent-guidelines/test-results/`
- **Project Guidelines**: `/home/user/global1sim/CLAUDE.md`

**For questions or improvements**, consult the README.md version history and contribution guidelines.

---

**Last Updated**: 2025-11-16
**Version**: 1.3
**Maintainer**: Global1SIM Agent Team
