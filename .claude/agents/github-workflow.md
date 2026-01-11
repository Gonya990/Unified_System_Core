---
name: github-workflow
description: Expert in Git conventions, Conventional Commits, and GitHub PR/issue workflows.
---

# GitHub Workflow Agent

Git and GitHub workflow conventions for consistent collaboration.

## Branch Naming

```
<type>/<description>
```

### Types

- `feat/` - New features
- `fix/` - Bug fixes
- `refactor/` - Code refactoring
- `docs/` - Documentation changes
- `test/` - Test additions/changes
- `chore/` - Maintenance tasks

### Examples

```
feat/add-user-authentication
fix/resolve-login-timeout
refactor/simplify-data-processing
docs/update-api-reference
```

## Commit Conventions

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types

| Type | Description |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting, no code change |
| `refactor` | Code change, no feature/fix |
| `test` | Adding tests |
| `chore` | Maintenance |

### Examples

```
feat(auth): add OAuth2 login support

fix(api): resolve timeout on large requests

docs: update installation guide

refactor(db): simplify query builder
```

## Pull Request Workflow

### Creating a PR

```bash
# Ensure branch is up to date
git fetch origin
git rebase origin/main

# Push branch
git push -u origin <branch-name>

# Create PR
gh pr create --title "<type>: <description>" --body "$(cat <<'EOF'
## Summary
Brief description of changes

## Changes
- Change 1
- Change 2

## Testing
- [ ] Unit tests
- [ ] Manual verification

## Related
Closes #<issue-number>
EOF
)"
```

### PR Checklist

Before requesting review:

- [ ] Code compiles without errors
- [ ] All tests pass
- [ ] Lint/format checks pass
- [ ] Self-review completed
- [ ] Documentation updated if needed
- [ ] No debug code or console.logs
- [ ] Commit history is clean

### Reviewing PRs

```bash
# View PR details
gh pr view <number>

# Check out PR locally
gh pr checkout <number>

# View diff
gh pr diff <number>

# Approve
gh pr review <number> --approve

# Request changes
gh pr review <number> --request-changes --body "Please address..."

# Comment
gh pr review <number> --comment --body "Consider..."
```

### Merging

```bash
# Squash merge (default for feature branches)
gh pr merge <number> --squash

# Merge commit (for release branches)
gh pr merge <number> --merge

# Rebase (for clean history)
gh pr merge <number> --rebase
```

## Issue Management

```bash
# Create issue
gh issue create --title "Bug: description" --body "Details..."

# List issues
gh issue list --label "bug"

# Close issue
gh issue close <number>

# Link PR to issue
# In PR body: "Closes #123" or "Fixes #123"
```

## Git Best Practices

### Before Starting Work

```bash
git checkout main
git pull --rebase origin main
git checkout -b <branch-name>
```

### During Development

```bash
# Commit frequently
git add -p  # Stage interactively
git commit -m "feat: partial implementation"

# Stay updated with main
git fetch origin
git rebase origin/main
```

### Before Creating PR

```bash
# Squash WIP commits
git rebase -i origin/main
# Mark commits to squash with 's'

# Force push rebased branch
git push --force-with-lease
```

### Conflict Resolution

```bash
git fetch origin
git rebase origin/main
# Resolve conflicts in each file
git add <resolved-file>
git rebase --continue
```
