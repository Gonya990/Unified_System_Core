# Generate PR Summary

Analyze changes and generate a comprehensive PR description.

## Input
$ARGUMENTS - Base branch (optional, defaults to main)

## Process

### 1. Analyze Changes
```bash
# Get commit history
git log origin/main..HEAD --oneline

# Get file changes
git diff origin/main --stat

# Get detailed diff
git diff origin/main
```

### 2. Categorize Changes

Group changes by type:
- **Features**: New functionality
- **Fixes**: Bug corrections
- **Refactoring**: Code improvements without behavior change
- **Tests**: Test additions or modifications
- **Documentation**: Doc updates
- **Configuration**: Config file changes

### 3. Generate PR Body

```markdown
## Summary
[1-2 sentence overview of what this PR accomplishes]

## Motivation
[Why are these changes needed? Link to issue/ticket if applicable]

## Changes

### [Category 1]
- [Specific change 1]
- [Specific change 2]

### [Category 2]
- [Specific change]

## Technical Details
[Any important implementation details, trade-offs, or decisions]

## Testing

### Automated Tests
- [x] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] E2E tests added/updated

### Manual Testing
Steps to manually verify:
1. [Step 1]
2. [Step 2]
3. [Expected result]

## Screenshots
[If UI changes, include before/after screenshots]

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No secrets or sensitive data included
- [ ] Breaking changes documented (if any)

## Related
- Closes #[issue-number]
- Related to #[other-pr]
```

### 4. Output Options

**Copy to clipboard:**
```bash
# macOS
echo "$PR_BODY" | pbcopy
# Linux
echo "$PR_BODY" | xclip -selection clipboard
```

**Create PR directly:**
```bash
gh pr create --title "[type]: [description]" --body "$PR_BODY"
```

## Output
Ready-to-use PR description that can be copied or used to create a PR.
