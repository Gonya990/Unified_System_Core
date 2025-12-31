---
name: empirical-measurement
description: DORA metrics (stability + throughput) to evaluate ANY change objectively; use when tracking improvement or making process/tech/org decisions.
---

# Empirical Measurement

## Core Principle

**"This is an enormous step forward. Now we can use these measures of efficiency and quality, which are measures of sensible, useful outcomes to evaluate almost any kind of change."**

## The DORA Metrics

**From Google DORA group, emphasized in book**:

### Throughput Measures
1. **Deployment Frequency**: How often you deploy to production
2. **Lead Time for Changes**: Time from commit to production

### Stability Measures  
3. **Mean Time to Recovery (MTTR)**: Time to restore service after incident
4. **Change Failure Rate**: % of deployments causing failures

## Why These Matter

**Quote**: "Stability and throughput are important because they are the best that we currently understand, not because they are perfect."

**Use case**: Evaluate ANYTHING - process change, new technology, org restructure

**Example**: 
- Try new practice → measure throughput & stability
- Improves → keep it
- Degrades → revert

## What NOT to Measure

**Bad Metrics** (from book):
- Lines of code (more = worse, not better)
- Developer days (effort ≠ value)
- Test coverage without quality (meaningless)

**Quote**: "More lines of code doesn't mean better code; it probably means worse code. Test coverage is meaningless unless the tests are testing something useful."

## Avoiding Self-Deception

**From the book**: Most organizations don't track if "business case" was actually met.

**Quote**: "How many of those organizations go on to track the cost of development and evaluate it...to validate that their 'business case' was met?"

**Solution**: Define success metrics BEFORE starting, measure AFTER completing.

## The Model

**Important**: DORA model is **correlative**, not **causative**.

Can't say "X causes Y" - but can say "Teams with X tend to have better Y".

**Use**: Track your scores, measure changes, see what improves outcomes.

## Integration with Skills

- Validates: ALL other skills (measure their impact)
- Requires: `experimental-workflow` (metrics = measurements)
- Enables: Data-driven decisions vs guesswork

## Target Metrics (Elite Performers)

- **Deploy frequency**: Multiple times per day
- **Lead time**: <1 hour
- **MTTR**: <1 hour  
- **Change failure rate**: <15%

See [reference/principles.md](reference/principles.md) for DORA research details.
See [reference/examples.md](reference/examples.md) for tracking implementation.
