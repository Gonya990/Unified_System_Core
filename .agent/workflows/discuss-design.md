---
description: Iterative design discussion with user - refine requirements before implementing
---

# Discuss & Design Workflow

> 💬 Use this workflow when the user wants to discuss, refine, or iterate on a design before implementation.

This workflow captures the iterative process of:

1. Understanding user requirements
2. Proposing a solution
3. Getting feedback
4. Refining based on feedback
5. Reaching agreement before implementing

---

## Step 1: Understand the Request

Before proposing anything:

1. **Read the request carefully** — identify the core goal
2. **Check existing context:**

   ```bash
   # Check relevant existing files
   ls -la .agent/workflows/
   cat AGENTS.md | head -50
   ```

3. **Identify constraints** — what limitations apply?
4. **Ask clarifying questions** if the request is ambiguous

---

## Step 2: Propose Initial Solution

Present a structured proposal:

```markdown
### Proposed Approach

**Goal:** [What we're trying to achieve]

**Constraints:**
- [Constraint 1]
- [Constraint 2]

**Proposed Solution:**
1. [Step 1]
2. [Step 2]

**Trade-offs:**
| Option A | Option B |
|----------|----------|
| Pros/cons | Pros/cons |

**Recommendation:** [Your recommendation and why]
```

---

## Step 3: Gather Feedback

After presenting proposal:

1. **Wait for user response** — don't implement yet
2. **Listen to concerns** — user may have context you don't
3. **Note specific objections** — address them directly

Common feedback patterns:

- "What about X?" → Address the gap
- "That won't work because..." → Revise approach
- "Good, but also..." → Expand scope
- "Let's simplify" → Reduce complexity

---

## Step 4: Iterate on Design

For each round of feedback:

1. **Acknowledge the feedback:**
   > "Good point about X. You're right that..."

2. **Revise the proposal:**
   - Show what changed
   - Explain why it addresses the concern

3. **Check for new issues:**
   > "This change also affects Y. Should we adjust that too?"

---

## Step 5: Confirm Before Implementing

Before writing any code or making changes:

```markdown
### Final Design Summary

**We agreed on:**
1. [Decision 1]
2. [Decision 2]

**Key design choices:**
- [Choice 1]: [Rationale]
- [Choice 2]: [Rationale]

**Ready to implement?**
```

Wait for explicit approval:

- ✅ "Yes", "Do it", "Implement" → Proceed to implementation
- ❓ "What about..." → Back to Step 4
- ❌ "Wait", "Stop" → Pause and clarify

---

## Step 6: Implement and Document

Once approved:

1. **Implement the agreed design**
2. **Document design decisions:**
   - Create or update `DESIGN_DECISIONS.md` in session folder
   - Capture constraints, options considered, and rationale

3. **Suggest next workflow:**
   > 🎯 "Implementation complete. Ready to run `/commit-push`?"

---

## Multi-Agent Safety

During design discussions:

- ✅ **Safe:** Reading files, proposing changes, creating docs
- ⚠️ **Wait for approval:** Modifying shared config files
- ❌ **Never:** Implementing before user confirms

---

## When to Use This Workflow

| Scenario | Use This Workflow? |
|----------|-------------------|
| User says "I want to..." | ✅ Yes — clarify first |
| User says "Create X for me" | 🟡 Maybe — depends on complexity |
| User says "Fix this bug" | ❌ No — just fix it |
| User says "What do you think about..." | ✅ Yes — they want discussion |
| User provides detailed spec | ❌ No — implement directly |
| User gives feedback on your work | ✅ Yes — iterate |

---

## Example Flow

```
User: "the workflows should be multi-agent aware"

Agent: "Good point. Currently workflows might conflict. 
        I propose adding:
        1. Workflow locks
        2. WIP commits instead of stash
        3. Append-only shared file edits
        
        Does this address your concern?"

User: "what about stash - another agent might need those changes"

Agent: "You're right - stash is local-only and dangerous.
        Revised: Explicitly prohibit stash, use WIP commits instead.
        
        Ready to implement?"

User: "yes"

Agent: [Implements] → [Documents] → Suggests /commit-push
```

---

## Output Artifacts

After completing this workflow, you should have:

1. **Design decisions document** — `Sessions/<id>/DESIGN_DECISIONS.md`
2. **Updated task.md** — tracking what was discussed and decided
3. **Implementation** — the actual changes
4. **Commit** — with clear message referencing the design discussion
