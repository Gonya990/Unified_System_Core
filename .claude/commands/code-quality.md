# Code Quality Check

Run comprehensive code quality checks on specified files or the entire project.

## Input
$ARGUMENTS - File paths (optional, defaults to changed files)

## Process

### 1. Identify Target Files
```bash
# If no arguments, check changed files
git diff --name-only HEAD~1
# Or staged files
git diff --cached --name-only
```

### 2. Run Automated Checks

#### Linting
```bash
# JavaScript/TypeScript
npm run lint 2>&1 || npx eslint . 2>&1

# Python
ruff check . 2>&1 || pylint **/*.py 2>&1

# Shell
shellcheck Scripts/*.sh 2>&1
```

#### Type Checking
```bash
# TypeScript
npx tsc --noEmit 2>&1

# Python
mypy . 2>&1 || pyright . 2>&1
```

#### Formatting
```bash
# Check (don't fix)
npx prettier --check . 2>&1
# Or
black --check . 2>&1
```

### 3. Manual Review Checklist

For each changed file, verify:

#### Type Safety
- [ ] No `any` types without justification
- [ ] No `@ts-ignore` or `@ts-expect-error`
- [ ] No type assertions (`as X`) without validation
- [ ] Proper null/undefined handling

#### Error Handling
- [ ] All errors are handled appropriately
- [ ] No empty catch blocks
- [ ] Error messages are informative
- [ ] Async errors are caught

#### Code Patterns
- [ ] Follows existing project patterns
- [ ] No duplicated code
- [ ] Functions are focused and small
- [ ] Dependencies are properly imported

#### Documentation
- [ ] Public APIs have documentation
- [ ] Complex logic is explained
- [ ] README updated if needed

### 4. Report Results

```markdown
## Code Quality Report

### Automated Checks
| Check | Status | Issues |
|-------|--------|--------|
| Lint | PASS/FAIL | N issues |
| Types | PASS/FAIL | N issues |
| Format | PASS/FAIL | N issues |

### Issues Found

#### Critical
- `file.ts:42` - [description]

#### Warnings
- `file.ts:78` - [description]

### Recommendations
1. [Recommendation]

### Summary
[Overall quality assessment]
```

## Output
Comprehensive quality report with actionable items.
