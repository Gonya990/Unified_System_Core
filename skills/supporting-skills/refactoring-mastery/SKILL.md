---
name: refactoring-mastery
description: Tiny safe incremental changes with continuous verification enabling evolutionary design; use during RED-GREEN-REFACTOR cycles and all code improvements.
---

# Refactoring Mastery

## Core Principle

**"In my own coding, I nearly always introduce new classes, variables, functions, and parameters via a multistage series of tiny refactoring steps, frequently checking that my code continues to work, by running my test, as I go." - David Farley**

## The Practice

**Farley's workflow**:
1. Make ONE tiny refactoring (extract method, rename, etc.)
2. Run test (should stay green)
3. If red → undo immediately
4. If green → commit or continue
5. Repeat

**Quote**: "At each point in the process, I can re-evaluate and change my mind and the direction of my design and code easily. I keep my options open!"

## Refactoring Skills

**Undervalued**: "Refactoring skills are often undervalued by developers who seem to miss their import."

**Value**: "If we can make changes in often tiny increments, we can be much more confident in the stability of that change."

## IDE Refactoring Tools

Use IDE refactorings (not manual edits):
- Extract Method
- Introduce Parameter  
- Rename
- Inline Variable
- Move Method/Class

**Advantage**: Deterministic, safe, instant feedback

## With Version Control

**Quote**: "If I combine my fine-grained incrementalism with strong version control, I am always only a small number of steps away from a 'safe place.' I can always withdraw to a position of stability."

**Practice**: 
- Commit after each successful refactoring
- Or commit when tests green after series of steps
- Always have safe rollback point <5 minutes away

## Integration with Skills

- Core to: `iterative-development`
- Enabled by: `feedback-driven-design` (fast tests)
- Supports: All complexity management skills

See [reference/principles.md](reference/principles.md) for refactoring philosophy.
See [reference/examples.md](reference/examples.md) for step-by-step refactoring sequences.
