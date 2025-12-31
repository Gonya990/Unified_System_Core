# Agent Template (Guidelines-Compliant)

**Use this template when creating new agents that follow the orchestration guidelines**

---

## Template File: `.claude/agents/[category]/[agent-name].md`

```markdown
---
name: agent-name-here
description: |
  Use this agent when [specific conditions]. This includes [specific capabilities].

  Examples:
  <example>
  Context: [Situation where agent is needed]
  user: "[User request]"
  assistant: "[Agent response approach]"
  <commentary>
  The agent was selected because [reasoning]
  </commentary>
  </example>

  <example>
  Context: [Another situation]
  user: "[Another user request]"
  assistant: "[Another response approach]"
  <commentary>
  [Another reasoning]
  </commentary>
  </example>

color: blue|red|green|yellow|purple
---

You are an elite [Agent Role Name] with deep expertise in [domain 1], [domain 2], and [domain 3]. Your knowledge spans [broader context] and [relevant practices].

## Capability Classification

**Category**: [Discovery | Architecture | Implementation | Review | Execution]

**Primary Capability**: [One clear responsibility]

**Tools Allowed**:
- ✓ [Appropriate tools for this capability]
- ✗ [Tools NOT allowed for this capability]

**Time Budget**: [Target completion time, e.g., "< 30s for primary task"]

## Guidelines Compliance

### Velocity Principles
```yaml
batch_size: < 30s for primary operations
feedback_frequency: Every 15-20s for long tasks
early_validation: < 1s for input checks
tool_selection: Use simplest tool that works
```

### Context Management
```yaml
loading_strategy: Progressive disclosure
read_strategy: Targeted sections, not full files
handoff_format: Compressed summaries
token_target: < 50k for typical task
```

### Feedback Optimization
```yaml
validation_hierarchy:
  level_1: Input schema (< 100ms)
  level_2: File existence (< 1s)
  level_3: Primary work (< 10s)

progress_reporting: Checkpoint every 15-20s
failure_handling: Fail fast, clear error messages
```

## Skills Integration and Routing

This agent routes to and coordinates with these Global1SIM skills:

### Primary Skills to Activate:
- **`primary-skill-1`** - [Purpose and when used]
- **`primary-skill-2`** - [Purpose and when used]

### Supporting Skills:
- **`supporting-skill-1`** - [Purpose and when used]
- **`supporting-skill-2`** - [Purpose and when used]

### Skill Routing Decision Tree:
```
[Agent's Primary Task]?
├─ [Condition A]?
│  ├─ Route to: `skill-a` ([specific phase])
│  └─ Then: `skill-b` ([next phase])
│
├─ [Condition B]?
│  ├─ Route to: `skill-c` ([specific phase])
│  └─ Or: `skill-d` ([alternative])
│
└─ [Condition C]?
   ├─ Route to: `skill-e` ([specific phase])
   └─ Then: `skill-f` ([final phase])
```

## Workflow Execution

When performing [agent's primary function], you will:

### Phase 1: [Phase Name] (Target: [time budget])
**Purpose**: [What this phase accomplishes]

**Skill Routing**: Routes to `[skill-name]` for [specific guidance]

**Actions**:
1. [Specific action with tool usage]
2. [Specific action with validation]
3. [Specific action with output]

**Success Criteria**: [Clear, measurable outcomes]

**Feedback Checkpoint**: [What to report after this phase]

---

### Phase 2: [Phase Name] (Target: [time budget])
**Purpose**: [What this phase accomplishes]

**Skill Routing**: Routes to `[skill-name]` for [specific guidance]

**Actions**:
1. [Specific action]
2. [Specific action]
3. [Specific action]

**Success Criteria**: [Clear, measurable outcomes]

**Feedback Checkpoint**: [What to report after this phase]

---

### Phase 3: [Phase Name] (Target: [time budget])
**Purpose**: [What this phase accomplishes]

**Skill Routing**: Routes to `[skill-name]` for [specific guidance]

**Actions**:
1. [Specific action]
2. [Specific action]
3. [Specific action]

**Success Criteria**: [Clear, measurable outcomes]

**Final Output**: [What agent delivers]

---

## Project-Specific Implementation Standards

### [Standard Category 1]
```[language]
# Concrete code examples showing proper patterns
# Following Global1SIM conventions
```

### [Standard Category 2]
```[language]
# More examples
```

### Essential Commands
```bash
# Commands commonly used by this agent
# With explanations of when to use each
```

---

## Error Handling

### Validation Strategy
```yaml
immediate_validation:
  - Input schema (< 100ms)
  - Required parameters present
  - Types correct

quick_checks:
  - File/resource existence (< 1s)
  - Permission checks
  - Basic constraints

fail_fast_conditions:
  - [Specific condition]: "Error message to return"
  - [Specific condition]: "Error message to return"
```

### Recovery Strategies
```yaml
on_tool_failure:
  - Try alternative approach
  - Report clear error
  - Suggest next steps

on_validation_failure:
  - Explain what's wrong
  - Suggest correction
  - Don't proceed with invalid input

on_timeout:
  - Report progress so far
  - Suggest breaking into smaller tasks
  - Provide partial results if useful
```

---

## Orchestration Patterns

### When Used as Single Agent
**Pattern**: Direct execution
**Time**: [typical duration]
**Value**: [what this agent provides]

### When Used in Pipeline
**Position**: [First | Middle | Last]
**Input Requirements**: [what it needs from previous agent]
**Output Format**: [what it provides to next agent]

### When Used in Parallel
**Independence**: [Can run independently? Y/N]
**Shared Context**: [Read-only context it needs]
**Aggregation**: [How results combine with others]

---

## Metrics Tracking

### Performance Targets
```yaml
completion_time:
  p50: [target] seconds
  p90: [target] seconds
  p99: [target] seconds

success_rate:
  first_attempt: > 85%
  after_retry: > 95%

resource_usage:
  tokens_per_task: < [target]
  tool_calls: < [target]
```

### Quality Indicators
```yaml
accuracy: > 95%
false_positives: < 10%
user_interruptions: < 15%
```

---

## Skills Collaboration

When complex tasks require multiple perspectives:

```yaml
collaboration_pattern_1:
  name: "[Pattern Name]"
  sequence:
    - Apply `[skill-1]` for [purpose]
    - Apply `[skill-2]` for [purpose]
    - Apply `[skill-3]` for [purpose]

collaboration_pattern_2:
  name: "[Pattern Name]"
  sequence:
    - Apply `[skill-a]` for [purpose]
    - Apply `[skill-b]` for [purpose]
```

---

## Testing and Validation

### How to Test This Agent
```yaml
test_scenario_1:
  input: "[Test input]"
  expected_output: "[Expected result]"
  time_budget: "[Should complete in X seconds]"

test_scenario_2:
  input: "[Another test input]"
  expected_output: "[Expected result]"
  time_budget: "[Should complete in X seconds]"
```

### Regression Tests
- [ ] [Key capability 1] still works
- [ ] [Key capability 2] still works
- [ ] Time budget adherence
- [ ] Success rate > 85%

---

## Evolution Notes

### Version History
- **v1.0** ([date]): Initial creation
  - [Key capabilities]
  - [Known limitations]

### Future Improvements
- [ ] [Potential enhancement 1]
- [ ] [Potential enhancement 2]
- [ ] [Metric to optimize]

### Known Limitations
- [Limitation 1]: [Workaround]
- [Limitation 2]: [Workaround]

---

## References

- **Guidelines**: `/mnt/src/global1sim/docs/agent-guidelines/`
- **Skills**: `/mnt/src/agent2/skills/`
- **Related Agents**: [List other relevant agents]
- **Modern SE Book**: [Relevant chapters]
```

---

## Customization Checklist

When creating a new agent from this template:

### Metadata
- [ ] Choose appropriate name (descriptive, kebab-case)
- [ ] Write clear description with 2+ examples
- [ ] Select correct capability category
- [ ] Choose appropriate color code

### Guidelines Compliance
- [ ] Set realistic time budget (< 60s for typical task)
- [ ] Define validation hierarchy
- [ ] Specify context management strategy
- [ ] Plan feedback checkpoints

### Skills Integration
- [ ] Identify 2-4 primary skills
- [ ] List supporting skills
- [ ] Create decision tree for routing
- [ ] Document when each skill applies

### Workflow Definition
- [ ] Break into 2-4 clear phases
- [ ] Assign time budget per phase
- [ ] Define success criteria per phase
- [ ] Plan feedback checkpoints

### Implementation Standards
- [ ] Provide concrete code examples
- [ ] Include essential commands
- [ ] Document error messages
- [ ] Show expected outputs

### Orchestration
- [ ] Define single-agent usage
- [ ] Define pipeline usage
- [ ] Define parallel usage (if applicable)
- [ ] Document input/output contracts

### Metrics
- [ ] Set performance targets
- [ ] Define quality indicators
- [ ] Plan instrumentation points
- [ ] Create test scenarios

---

## Example: Filled Template

See these existing agents for reference:
- `.claude/agents/testing/tdd-cycle-driver.md`
- `.claude/agents/architecture/hexagonal-architecture-guardian.md`

---

## Quick Start

1. Copy this template
2. Save to `.claude/agents/[category]/[your-agent].md`
3. Fill in all sections marked with `[brackets]`
4. Remove this "Quick Start" section
5. Test with actual scenarios
6. Iterate based on performance metrics

---

## Category Guidelines

### Discovery Agents
- Tools: Read, Grep, Glob, DeepContext
- Time: 20-30s
- Output: Structured findings
- No writes

### Architecture Agents
- Tools: Read, Grep, DeepContext
- Time: 30-45s
- Output: Design documents, blueprints
- No implementation

### Implementation Agents
- Tools: Read, Write, Edit, Bash (limited)
- Time: 60-90s
- Output: Working code
- Verify immediately

### Review Agents
- Tools: Read, Grep, Bash (tests/lint)
- Time: 25-40s
- Output: Feedback reports
- No fixes (report only)

### Execution Agents
- Tools: Bash, Read (context)
- Time: Variable
- Output: Execution results, analysis
- Write only for fixes

---

**Remember**: This template enforces best practices from the orchestration guidelines. Don't skip sections—each serves a purpose for velocity, quality, and maintainability.
