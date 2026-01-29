---
name: context7-workflow
description: Library documentation research - use when unfamiliar with external library; supports experimental-workflow (research then test)
parent: global1sim-development
activation_triggers:
  - "using unfamiliar library"
  - "unclear library behavior"
  - "need best practices for library"
optional: true
---

# Context7 Workflow (Library Research)

**AGENTIC**: Research unfamiliar libraries, then test, then implement.

## Decision Tree

```yaml
use_context7_when:
  - first_time_using: "Library you haven't used before"
  - unclear_behavior: "Docs unclear or incomplete"
  - best_practices: "Want library-specific patterns"
  
skip_context7_when:
  - familiar_library: "FastAPI, Pydantic, pytest (you know these)"
  - standard_library: "typing, dataclasses, datetime"
  - internal_code: "Use DeepContext for our code"
```

## Workflow

```python
# 1. Resolve library ID
mcp__context7__resolve_library_id(libraryName="stripe")

# 2. Get documentation
mcp__context7__get_library_docs(
    context7CompatibleLibraryID="/stripe/stripe-python",
    topic="payment intents"  # Optional focus
)

# 3. Write test based on docs
def test_stripe_payment():
    # Based on docs, write expected behavior
    pass

# 4. Implement following best practices
def process_payment():
    # Follow patterns from docs
    pass
```

## Integration

- Parent: `global1sim-development`
- Supports: `experimental-workflow`, `iterative-development`
- Skills: `feedback-driven-design` (test first, even for libraries)

**Quick**: resolve-library-id → get-library-docs → write test → implement
