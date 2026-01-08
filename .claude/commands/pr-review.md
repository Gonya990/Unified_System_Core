# Pull Request Review

Perform comprehensive code review on a pull request.

## Input
$ARGUMENTS - PR number or URL

## Process

### 1. Fetch PR Details
```bash
gh pr view <number> --json title,body,files,additions,deletions,commits
gh pr diff <number>
```

### 2. Review Checklist

#### Logic & Flow
- [ ] Code does what it claims to do
- [ ] Edge cases are handled
- [ ] No obvious bugs or logic errors
- [ ] Error paths are properly handled

#### Code Quality
- [ ] No `any` types (TypeScript) or equivalent type escapes
- [ ] No empty catch blocks
- [ ] No commented-out code
- [ ] No debug statements (console.log, print, etc.)
- [ ] Functions are reasonably sized (<50 lines guideline)

#### Naming & Clarity
- [ ] Variable/function names are descriptive
- [ ] Code is self-documenting
- [ ] Complex logic has necessary comments

#### Testing
- [ ] New code has corresponding tests
- [ ] Tests cover happy path and error cases
- [ ] Tests are meaningful (not just coverage padding)

#### Security
- [ ] No hardcoded secrets or credentials
- [ ] User input is validated/sanitized
- [ ] No SQL injection or XSS vulnerabilities

#### Performance
- [ ] No obvious N+1 queries
- [ ] No unnecessary loops or computations
- [ ] Large data sets are handled appropriately

### 3. Provide Feedback

Format feedback in categories:

```markdown
## Code Review: PR #<number>

### Critical (Must Fix)
- **file.ts:42** - [Issue description and why it's critical]

### Warning (Should Fix)
- **file.ts:78** - [Issue description]

### Suggestion (Nice to Have)
- **file.ts:100** - [Suggestion for improvement]

### Positive Notes
- Good use of [pattern/approach]
- Well-tested [functionality]

### Summary
[Overall assessment: Approve / Request Changes / Needs Discussion]
```

### 4. Post Review
- Add review comments inline if using GitHub
- Request changes or approve as appropriate

## Output
Structured review with actionable feedback categorized by severity.
