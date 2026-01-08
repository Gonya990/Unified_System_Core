# Deep Task Onboarding

Perform comprehensive task exploration and create detailed onboarding documentation.

## Input
$ARGUMENTS - Task ID or description to onboard

## Process

1. **Understand the Task**
   - Parse the task/ticket ID or description
   - If a ticket system is available (JIRA, Linear, GitHub Issues), fetch full details
   - Extract requirements, acceptance criteria, and constraints

2. **Explore the Codebase**
   - Identify all files and modules related to the task
   - Map dependencies and relationships
   - Find similar implementations or patterns already in the codebase
   - Note any potential conflicts or integration points

3. **Analyze Technical Context**
   - Review relevant tests to understand expected behavior
   - Check for existing documentation
   - Identify affected APIs or interfaces
   - List potential risks or edge cases

4. **Create Onboarding Document**
   Create `.claude/tasks/[TASK_ID]/onboarding.md` with:
   
   ```markdown
   # Task: [Title]
   
   ## Summary
   [Brief description of what needs to be done]
   
   ## Requirements
   - [ ] Requirement 1
   - [ ] Requirement 2
   
   ## Technical Analysis
   
   ### Files to Modify
   - `path/to/file.ts` - [reason]
   
   ### Related Code
   - `path/to/related.ts` - [how it relates]
   
   ### Patterns to Follow
   [Existing patterns in the codebase to match]
   
   ### Risks & Edge Cases
   - Risk 1
   - Edge case 1
   
   ## Implementation Plan
   1. Step 1
   2. Step 2
   
   ## Testing Strategy
   - Unit tests for...
   - Integration tests for...
   
   ## Questions / Blockers
   - [ ] Question needing clarification
   ```

5. **Report Summary**
   - Present key findings to the user
   - Highlight any blockers or questions
   - Recommend next steps

## Output
A comprehensive onboarding document and summary ready for implementation.
