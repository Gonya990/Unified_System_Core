---
name: deployment-pipeline-designer
description: Designs deployment pipelines as mechanized routes from commit to production achieving releasable software in <1 hour; use when establishing CD practices or optimizing feedback cycles.
---

# Deployment Pipeline Designer

## Core Principle

**"A deployment pipeline is not simply a little workflow of build or test steps; it is a mechanized route from commit to production."**

**Critical**: "If the pipeline says everything is good, there should be no more work to do to make you comfortable to release—nothing…no more integration checks, sign-offs, or staging tests. If the pipeline says it is 'good,' then it is 'good to go!'"

## The One-Hour Rule

**From the book**: "I advise the companies that I work with to aim for creating 'releasable software' at least once per hour."

**Implication**: If any single test takes >1 hour OR deploy takes >1 hour, you can't achieve CD regardless of hardware.

**This constraint FORCES architectural decisions**: Fast tests require modular, testable design.

## Pipeline Scope = Deployable Unit

**Quote**: "The scope of an effective deployment pipeline is always an 'independently deployable unit of software.'"

**Two valid architectures**:
1. **Monolith**: One pipeline for entire system
2. **Microservices**: One pipeline per service

**No middle ground**: Testing services together means they're not independent.

## Integration with Skills

- Requires: `feedback-driven-design`, `modularity-architect`
- Validates: `iterative-development`, `experimental-workflow`

See [reference/principles.md](reference/principles.md) for CD fundamentals.
