# Systematic Debugging Skill

A four-phase framework for debugging issues without random trial-and-error.

## Core Principle

**NO FIXES WITHOUT ROOT CAUSE UNDERSTANDING**

Random changes hoping something works = wasted time and potential new bugs.

## Phase 1: Root Cause Investigation

Before ANY code changes:

1. **Reproduce the Issue**
   - Get exact steps to trigger the bug
   - Verify you can reproduce it consistently
   - Note the exact error message/behavior

2. **Gather Evidence**
   - Read error messages completely
   - Check logs at all levels (app, server, browser console)
   - Identify the exact line/function where failure occurs

3. **Form Hypothesis**
   - What do you think is happening?
   - What evidence supports this?
   - What would disprove it?

## Phase 2: Pattern Analysis

Find working examples to understand the gap:

1. **Find Similar Working Code**
   - Search codebase for similar functionality that works
   - Compare the working code with the broken code
   - Note differences in patterns, inputs, or context

2. **Check Recent Changes**
   ```bash
   git log --oneline -20 -- <file>
   git diff HEAD~5 -- <file>
   ```

3. **Verify Assumptions**
   - Is the input data what you expect?
   - Are dependencies loaded correctly?
   - Is the environment configured properly?

## Phase 3: Hypothesis Testing

Scientific method applied to debugging:

1. **Single Variable Testing**
   - Change ONE thing at a time
   - Verify the result
   - Revert if it doesn't fix the issue

2. **Add Diagnostic Code**
   ```javascript
   console.log('DEBUG: value=', value, 'type=', typeof value);
   ```
   - Log inputs, outputs, and intermediate values
   - Log at function entry/exit points
   - Remove ALL debug code before committing

3. **Binary Search**
   - If unclear where the bug is, narrow down by half
   - Comment out half the code, does it still fail?
   - Repeat until isolated

## Phase 4: Implementation

Only after root cause is confirmed:

1. **Write Failing Test First**
   ```javascript
   it('should handle edge case X', () => {
     expect(functionUnderTest(edgeCaseInput)).toBe(expectedOutput);
   });
   ```

2. **Implement Minimal Fix**
   - Fix the root cause, not the symptom
   - Smallest change that fixes the issue
   - NO refactoring during bug fixes

3. **Verify Completely**
   - New test passes
   - All existing tests pass
   - Manual verification matches expected behavior

## Red Flags - STOP and Reassess

Stop immediately if you notice:

- [ ] You've made 3+ changes without understanding why
- [ ] You're copying code hoping it "just works"
- [ ] The fix is getting larger than expected
- [ ] You're suppressing errors instead of handling them
- [ ] You don't understand why the fix works

## After 3 Consecutive Failed Fixes

**MANDATORY PROTOCOL:**

1. **STOP** all further changes
2. **REVERT** to last known working state
3. **DOCUMENT** what you've tried and what happened
4. **ESCALATE** - consult Oracle or ask for help
5. **DO NOT** continue random attempts

## Anti-Patterns

| Bad | Good |
|-----|------|
| "Let me try this..." | "Based on X evidence, I hypothesize Y" |
| Changing multiple things | Single variable testing |
| Suppressing errors | Understanding and handling errors |
| "It works now" (no idea why) | "It works because X was causing Y" |
| Large refactor during fix | Minimal targeted change |

## Debugging Checklist

Before declaring a bug fixed:

- [ ] I can explain the root cause
- [ ] I wrote a test that catches this bug
- [ ] The fix is minimal and targeted
- [ ] All tests pass
- [ ] I removed all debug code
- [ ] The fix doesn't introduce new issues
