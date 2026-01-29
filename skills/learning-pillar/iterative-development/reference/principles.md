# Iterative Development - Core Principles

## Foundational Quotes from "Modern Software Engineering"

### The Problem with Planning

> "An agile approach to software development actively encourages us to start work on solving problems in smaller pieces. It encourages us to begin work before we know the answer to everything."

> "This doesn't mean that agile thinking is perfect or the final answer. Rather, it is an important, significant, enabling step in the direction of better performance."

### Why Iteration Scales

> "A waterfall approach is sequential. You must answer the questions of the stage that you are in before proceeding to the next stage. This means that however clever we are, there must, at some point, be a limit at which the complexity of the system as a whole goes beyond human understanding."

> "An agile approach to software development actively encourages us to start work on solving problems in smaller pieces...This allows us to refine our thinking, identify the next small step, and then take that step. Agile development is an unbounded, infinite approach."

### The Reality of Software Work

> "We must learn to have the confidence to begin work precisely when we don't yet know the answers and when we don't know how much work will be involved."

> "This is disquieting for some people and for some organizations, but it is only the same as the reality of much of the human experience. When a business starts out on a new venture, they don't really know when, or even whether, it will be a success."

### Practical Application

> "Work in smaller batches. We need to reduce the scope of each change and make change in smaller steps; in general, the smaller the better."

> "Working in small batches also means that we limit the time-horizon over which our assumptions need to hold. The universe has a smaller window of time within which it can intrude on our work, and so things are less likely to change in damaging ways."

> "Finally, if we make small steps, even if a small step is invalidated by changing circumstance or just misunderstanding on our part, there is less work lost. So, small steps really matter."

## Iteration at Different Scales

### Coarse-Grained: Sprints/Iterations

> "The obvious incarnation of this idea in agile teams is the idea of iterations or sprints. Agile disciplines promote the idea of working to completed, production-ready code, within a small, fixed period of time."

**Application**: Our team should target weekly deployable increments.

### Medium-Grained: Continuous Integration

> "At a completely different scale, you can think of the practices of continuous integration (CI) and test-driven development (TDD) as being inherently iterative processes."

> "In CI we are going to commit our changes frequently, multiple times per day. This means that each change needs to be atomic, even if the feature that it contributes to is not yet complete."

**Application**: Commit 3-5+ times per day, each commit atomic and testable.

### Fine-Grained: TDD Cycle

> "TDD is often described by the practices that contribute to it: Red, Green, Refactor."
> - "Red: Write a test, run it, and see it fail."
> - "Green: Write just enough code to make the test pass, run it, and see it pass."
> - "Refactor: Modify the code and the test to make it clear, expressive, elegant and more general. Run the test after every tiny change and see it pass."

**Application**: Run tests after every tiny refactoring step (seconds, not minutes).

### Ultra-Fine-Grained: Code Changes

> "In my own coding, I nearly always introduce new classes, variables, functions, and parameters via a multistage series of tiny refactoring steps, frequently checking that my code continues to work, by running my test, as I go."

> "This is iterative working at a very fine resolution. It means that my code is correct and working for more of the time, and that means that each step is safer."

**Application**: Extract method, introduce parameter - one IDE refactoring at a time, test after each.

## The Evolutionary Model

> "Another way to think of this is that software development is a kind of evolutionary process. Our job as programmers is to guide our learning and our designs through an incremental process of directed evolution toward desirable outcomes."

This is NOT random evolution - it's **guided** evolution:
- We choose direction (tests define desired behavior)
- We take small steps (atomic commits)
- We evaluate fitness (tests pass/fail)
- We adapt based on reality (feedback loop)

## When Iteration Changes Everything

### Impact on Design

> "This approach means that the process to design of our code is more like one of guided evolution, with each small step giving us feedback, but not necessarily yet adding up to a whole feature. This is a very challenging change of perspective for many people, but is a liberating step when embraced and is one that has a positive impact on the quality of our designs."

### Impact on Release

> "Not only does this approach mean that our software is always releasable and that we are getting frequent, fine-grained feedback on the quality and applicability of our work, but it also encourages us to design our work in a way that sustains this approach."

## The Courage to Start Without Knowing

**Kent Beck's Insight** (referenced in book):
> "Embrace change!"

**Farley's Elaboration**:
> "The implications of this are significant. It means that we must...have the confidence to begin work precisely when we don't yet know the answers and when we don't know how much work will be involved."

## Iteration Requires Support

Iteration is not a solo practice - it requires:

1. **Automated Testing** - Fast feedback on correctness
2. **Continuous Integration** - Fast feedback on integration
3. **Version Control** - Ability to retreat to safe places
4. **Modular Design** - Ability to change one piece without breaking others
5. **Team Agreement** - Cultural acceptance of incomplete-but-stable code

## The Trade-Off

> "As ever, there is no free lunch. If we want to work iteratively, we must change the way that we work in many ways to facilitate it."

> "Working iteratively has an impact on the design of the systems that we build, how we organize our work, and how we structure the organizations in which we work."

**This is a feature, not a bug** - The constraints of iteration force better designs.

## Historical Context

### Fred Brooks - "No Silver Bullet" (1986)

> "...the system should first be made to run, even though it does nothing useful except call the proper set of dummy subprograms. Then, bit-by-bit it is fleshed out, with the subprograms in turn being developed into actions or calls to empty stubs in the level below."

**Even in 1986**, the answer was iterative development, not better planning tools.

## Bottom Line

Iteration is not about being "agile" or following a framework. It's about:

1. **Acknowledging uncertainty** - We don't know everything upfront
2. **Exploiting feedback** - Reality teaches us what works
3. **Limiting risk** - Small steps mean small failures
4. **Scaling understanding** - Beyond individual mental capacity
5. **Enabling change** - Direction can shift without catastrophic rework

**Iteration is engineering, not cowboy coding.**
