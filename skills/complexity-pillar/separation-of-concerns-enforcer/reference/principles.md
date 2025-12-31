# Separation of Concerns - Primary Design Principle

## The Golden Rule

> "Separation of concerns is the most powerful principle of design in my own work. I apply it everywhere." - David Farley

**The Rule**: "One class, one thing. One method, one thing."

## Essential vs Accidental Complexity

**From Fred Brooks' "No Silver Bullet"**:

**Essential Complexity**: "The complexity that is inherent in solving the problem"
- Calculating interest, adding to cart, validating data

**Accidental Complexity**: "Everything else—the problems that we are forced to solve as a side effect of doing something useful with computers"
- Persistence, HTTP, JSON, transactions, clustering

> "It is in our interests to work to minimize, without ignoring, accidental complexity."

## The Database Swap Story

**Real example from Farley's financial exchange**:

Action:
1. Downloaded open-source RDBMS
2. Made "a few simple changes to the code that interacted with the RDBMS"
3. Two tests failed, fixed problems
4. Deployed to production few days later

**Timeline**: "This whole story took a single morning!"

> "Without good separation of concerns, this would have taken months or years and probably wouldn't even have been contemplated as a result."

## Dependency Injection

> "Dependency injection is where dependencies of a piece of code are supplied to it as parameters, rather than created by it."

**Common Misconception**: "Dependency injection needs a framework"

**Reality**: "Dependency injection is something you can do in most languages...natively, and it is a powerful approach to design."

> "I have even seen it used, to very good effect, in Unix shell scripts."

## Boundaries as Translation Points

> "The seams or boundaries should be treated with more care. They should be translation and validation points for information."

**Common Problem**: "Often the code that represents these boundaries is indistinguishable from the code on either side."

**Solution**: Clear separation between what crosses boundaries vs what stays internal.
