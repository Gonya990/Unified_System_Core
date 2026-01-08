# End-to-End Ticket Workflow

Complete ticket workflow from reading to PR creation.

## Input
$ARGUMENTS - Ticket ID (JIRA, Linear, GitHub Issue, or Beads ID)

## Workflow

### 1. Read the Ticket
- Fetch ticket details using appropriate tool:
  - Beads: `bd show <id>`
  - GitHub: `gh issue view <id>`
  - JIRA/Linear: Use MCP if configured
- Extract: title, description, acceptance criteria, priority, labels

### 2. Create Onboarding
- Run the `/onboard` command with ticket context
- Review the generated analysis

### 3. Create Branch
```bash
# Format: <type>/<ticket-id>-<brief-description>
git checkout -b feat/TICKET-123-add-user-auth
```

Branch type prefixes:
- `feat/` - New features
- `fix/` - Bug fixes
- `refactor/` - Code refactoring
- `docs/` - Documentation
- `test/` - Test additions

### 4. Implement with TDD
1. Write failing test first
2. Implement minimum code to pass
3. Refactor if needed
4. Repeat for each requirement

### 5. Update Ticket Status
- Mark as "In Progress" when starting
- Add comments for significant decisions
- Mark as "In Review" when PR is ready

### 6. Create Pull Request
```bash
gh pr create --title "<type>: <description>" --body "
## Summary
Brief description of changes

## Ticket
Closes #<ticket-id>

## Changes
- Change 1
- Change 2

## Testing
- [ ] Unit tests added
- [ ] Manual testing performed

## Checklist
- [ ] Code follows project conventions
- [ ] Documentation updated if needed
- [ ] No console.log or debug code
"
```

### 7. Link PR to Ticket
- Add PR link to ticket
- Request review if needed

## Example Flow
```
User: /ticket PROJ-456

Agent:
1. Fetches PROJ-456 details
2. Creates onboarding doc
3. Creates branch: feat/PROJ-456-user-preferences
4. Implements feature with tests
5. Updates ticket to "In Review"
6. Creates PR and links to ticket
7. Reports completion with PR URL
```
