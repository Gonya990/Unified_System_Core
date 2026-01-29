# Agent Execution Test Plan
## Testing 6 New Agents (2025-11-16)

**Purpose**: Validate execution of newly created agents following successful code-explorer test

**Date**: 2025-11-16
**Agents to Test**: 6 (code-architect, api-discoverer, dependency-mapper, performance-optimizer, implementer, bug-fixer)
**Current Testing Rate**: 50% (6/12) → Target: 100% (12/12)

---

## Test Strategy

### Approach
- **Individual execution tests** (not parallel) - validate each agent works independently
- **Real codebase analysis** - use actual Global1SIM code
- **Measure performance** - track execution time, success rate, output quality
- **Document results** - update agent-guidelines README with findings

### Success Criteria
- ✅ Agent completes task without errors
- ✅ Execution time within specified budget
- ✅ Output is actionable and follows guidelines
- ✅ No hallucinations or false information
- ✅ Follows Modern SE principles and skills routing

---

## Test Scenarios

### Test 1: code-architect
**Category**: Architecture
**Time Budget**: 30-45 seconds
**Test Scenario**: Design a new feature for subscriber activation workflow

**Input Task**:
> "Design the architecture for an automated subscriber activation feature that validates ICCID, provisions eSIM profile, and sends activation confirmation. Follow hexagonal architecture patterns."

**Expected Outputs**:
- [ ] Complete architectural blueprint with all layers (models, services, repositories, routes)
- [ ] Pydantic V2 models with frozen=True
- [ ] Clear separation of concerns (business logic in services, DB in repositories)
- [ ] Validation strategy documented
- [ ] Error handling strategy defined
- [ ] Test strategy included
- [ ] Implementation order specified

**Quality Checks**:
- Follows hexagonal architecture patterns
- Uses existing codebase patterns
- Includes all required components
- Actionable for implementer agent

---

### Test 2: api-discoverer
**Category**: Discovery
**Time Budget**: 15-25 seconds
**Test Scenario**: Catalog all FastAPI endpoints in the codebase

**Input Task**:
> "Discover and catalog all API endpoints in the Global1SIM codebase. Identify endpoints, HTTP methods, request/response models, authentication requirements, and common patterns."

**Expected Outputs**:
- [ ] List of all API endpoints with decorators (@router.get, @router.post, etc.)
- [ ] HTTP methods identified
- [ ] Request/response models cataloged
- [ ] Authentication requirements noted
- [ ] Endpoints grouped by module/router
- [ ] Common patterns identified (pagination, error handling, etc.)
- [ ] Execution time < 25s

**Quality Checks**:
- Finds all FastAPI routes in src/api/routes/ (if they exist)
- No hallucinations about non-existent endpoints
- Accurately identifies patterns
- Clear, structured output

---

### Test 3: dependency-mapper
**Category**: Discovery
**Time Budget**: 20-30 seconds
**Test Scenario**: Map dependencies for the services layer

**Input Task**:
> "Map the dependencies for all service modules in src/services/. Identify what each service imports, which repositories it depends on, and calculate coupling metrics."

**Expected Outputs**:
- [ ] Dependency graph for service layer
- [ ] Import statements cataloged
- [ ] Repository dependencies identified
- [ ] Coupling metrics calculated (fan-in, fan-out)
- [ ] Circular dependencies identified (if any)
- [ ] Recommendations for reducing coupling
- [ ] Execution time < 30s

**Quality Checks**:
- Accurate import analysis
- Correct coupling calculations
- Identifies actual dependencies (not guessed)
- Actionable recommendations

---

### Test 4: performance-optimizer
**Category**: Architecture
**Time Budget**: 30-45 seconds
**Test Scenario**: Analyze performance of existing code for bottlenecks

**Input Task**:
> "Analyze the Global1SIM codebase for performance anti-patterns. Look for N+1 queries, blocking I/O in async functions, missing pagination, and inefficient loops. Prioritize findings by impact."

**Expected Outputs**:
- [ ] List of performance anti-patterns found with file:line locations
- [ ] Code examples showing current pattern
- [ ] Code examples showing optimized pattern
- [ ] Impact estimation (10x, 2-5x, <20% improvement)
- [ ] Effort estimation (hours/days)
- [ ] Prioritized optimization recommendations
- [ ] Execution time < 45s

**Quality Checks**:
- Identifies real anti-patterns (not false positives)
- Provides actionable code examples
- Accurate impact/effort estimates
- Follows high-performance-simplicity skill

---

### Test 5: implementer
**Category**: Implementation
**Time Budget**: 45-60 seconds
**Test Scenario**: Implement a simple feature following TDD

**Input Task**:
> "Implement a simple utility function to validate ICCID format (19-20 digits, passes Luhn algorithm check). Follow TDD: write failing test first, minimal implementation, then refactor."

**Expected Outputs**:
- [ ] Test file created with failing test (RED)
- [ ] Implementation created to pass test (GREEN)
- [ ] Code refactored if needed (REFACTOR)
- [ ] Type hints included
- [ ] Docstring added
- [ ] Test passes
- [ ] Execution time < 60s

**Quality Checks**:
- Follows TDD cycle (RED-GREEN-REFACTOR)
- Tests actually fail before implementation
- Tests pass after implementation
- Code follows project standards (type hints, Pydantic, etc.)
- No shortcuts (e.g., skipping tests)

---

### Test 6: bug-fixer
**Category**: Implementation
**Time Budget**: 45-60 seconds
**Test Scenario**: Fix a hypothetical bug using TDD

**Input Task**:
> "There's a bug: the validate_email function accepts emails without '@' symbol. Write a test that reproduces the bug (should fail), fix the validation logic, and verify the test passes."

**Expected Outputs**:
- [ ] Test written that reproduces bug (fails initially)
- [ ] Bug fix implemented
- [ ] Test now passes
- [ ] Regression tests added for edge cases
- [ ] Root cause documented
- [ ] Execution time < 60s

**Quality Checks**:
- Test actually reproduces the bug (fails before fix)
- Fix addresses root cause (not just symptom)
- Test passes after fix
- No new bugs introduced
- Follows TDD principles

---

## Execution Plan

### Phase 1: Discovery Agents (Expected: 45-80s total)
1. **api-discoverer** (15-25s) - Catalog API endpoints
2. **dependency-mapper** (20-30s) - Map service dependencies
3. **Measure**: execution time, completeness, accuracy

### Phase 2: Architecture Agents (Expected: 60-90s total)
1. **code-architect** (30-45s) - Design subscriber activation feature
2. **performance-optimizer** (30-45s) - Analyze performance anti-patterns
3. **Measure**: execution time, blueprint quality, recommendations accuracy

### Phase 3: Implementation Agents (Expected: 90-120s total)
1. **implementer** (45-60s) - Implement ICCID validation with TDD
2. **bug-fixer** (45-60s) - Fix email validation bug with TDD
3. **Measure**: execution time, TDD adherence, code quality

### Total Expected Time: ~3.5-5 minutes for all 6 agents

---

## Metrics to Track

### Performance Metrics
```yaml
per_agent:
  execution_time: measured in seconds
  first_attempt_success: true/false
  time_budget_adherence: within/exceeded

aggregate:
  total_execution_time: sum of all agents
  success_rate: successful/total
  average_execution_time: mean
```

### Quality Metrics
```yaml
per_agent:
  completeness: all expected outputs present
  accuracy: no hallucinations or false info
  actionability: outputs are usable
  guideline_adherence: follows Modern SE principles

aggregate:
  overall_quality_score: percentage
  agents_meeting_standards: count
```

### Efficiency Metrics
```yaml
per_agent:
  tool_calls: number of tool invocations
  context_usage: estimated token usage

aggregate:
  average_tool_calls: mean
  total_context: sum
```

---

## Test Execution Log

### Test 1: code-architect
- **Status**: ⏳ Pending
- **Start Time**:
- **End Time**:
- **Duration**:
- **Result**:
- **Notes**:

### Test 2: api-discoverer
- **Status**: ⏳ Pending
- **Start Time**:
- **End Time**:
- **Duration**:
- **Result**:
- **Notes**:

### Test 3: dependency-mapper
- **Status**: ⏳ Pending
- **Start Time**:
- **End Time**:
- **Duration**:
- **Result**:
- **Notes**:

### Test 4: performance-optimizer
- **Status**: ⏳ Pending
- **Start Time**:
- **End Time**:
- **Duration**:
- **Result**:
- **Notes**:

### Test 5: implementer
- **Status**: ⏳ Pending
- **Start Time**:
- **End Time**:
- **Duration**:
- **Result**:
- **Notes**:

### Test 6: bug-fixer
- **Status**: ⏳ Pending
- **Start Time**:
- **End Time**:
- **Duration**:
- **Result**:
- **Notes**:

---

## Next Steps After Testing

1. **Update README** - Document test results in agent-guidelines/README.md
2. **Create Test Report** - Detailed report in test-results/2025-11-16-new-agents-execution.md
3. **Update Agent Status** - Mark agents as tested in documentation
4. **Identify Issues** - Document any problems or improvements needed
5. **Plan Improvements** - Create follow-up tasks for any failures or enhancements

---

## References

- **Template**: `templates/PARALLEL_EXECUTION_TEST_TEMPLATE.md`
- **Previous Test**: `test-results/2025-11-16-scatter-gather-pattern.md`
- **Agent Guidelines**: `docs/agent-guidelines/README.md`
- **Agent Files**: `.claude/agents/*/`
