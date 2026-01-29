---
name: high-performance-simplicity
description: Simple code equals fast code - complex code prevents compiler optimization; use when optimizing performance or designing for speed.
---

# High-Performance Simplicity

## Core Insight

**"High-performance systems demand simple, well-designed code."**

Counter-intuitive but proven: The route to fast code is simple, easy-to-understand code.

## The Reasoning

**Quote**: "To achieve 'high performance,' we need to do the maximum amount of work for the smallest number of instructions. The more complex our code, the more likely that the paths through our code are not optimal, because the 'simplest possible route' through our code is obscured by the complexity of the code itself."

## Compiler Optimization

**From the book**: "Modern compilers do a fantastic job of optimizing code to run efficiently on modern hardware. They excel when the code is simple and predictable."

**Critical point**: "Most optimizers in compilers simply give up trying once the cyclomatic complexity of a block of code exceeds some threshold."

**Implication**: Complex code actually PREVENTS optimization.

## Method Call Overhead Myth

**Common belief**: "Extracting methods adds overhead"

**Reality**: Modern compilers inline methods automatically when code is simple.

**From book's benchmark**: No measurable difference between code with extracted methods vs monolithic code.

## Optimize for Reading, Not Writing

**Quote**: "It is a mistake to optimize code to reduce typing. We are optimizing for the wrong things."

**The primary goal**: "The primary goal of code is to communicate ideas to humans!"

**Principle**: "I prefer to optimize to reduce thinking rather than to reduce typing."

## Don't Guess - Measure

**Quote**: "If you are really interested in the performance of your code, don't guess about what will be fast and what will be slow; measure it!"

**Practice**:
```python
# Use profilers, benchmarks, load tests
# Measure before and after optimization
# Data over intuition
```

## Integration with Skills

- Supports: All development skills
- Validated by: `experimental-workflow` (measure performance)
- Enabled by: `separation-of-concerns-enforcer` (simple = fast)

See [reference/principles.md](reference/principles.md) for performance philosophy.
See [reference/examples.md](reference/examples.md) for benchmark comparisons.
