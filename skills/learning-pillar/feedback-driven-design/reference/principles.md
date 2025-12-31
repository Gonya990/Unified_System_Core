# Feedback-Driven Design - Core Principles from Book

## The Broom Balancing Analogy

**Predictive Approach (Waterfall)**:
> "Carefully analyze the structure of the broom, work out its center of gravity, closely examine the structure of the handle, and calculate exactly the point at which the broom will be perfectly balanced."

**Result**: "Incredibly unlikely that it will [work]. The result is extremely unstable."

**Feedback-Driven Approach (Agile)**:
> "Put the broom on our hand and move our hand in response to how it tipped!"

**Result**: "This is how space rockets 'balance' on the thrust of their engines."

**Conclusion**: "The second approach, although it may seem more ad hoc, more like 'winging it,' is actually profoundly more effective and more stable in terms of outcome."

## Feedback is Essential

> "Without feedback, there is no opportunity to learn. We can only guess, rather than make decisions based on reality."

> "Unless we can know and understand the results of our choices and actions, we cannot tell if we are making progress."

## TDD as Design Feedback

> "One of the reasons that I value TDD so highly, as a practice, is the feedback that it gives me on the quality of my design. If my tests are hard to write, that tells me something important about the quality of my code."

> "TDD applies a pressure to create code that is objectively 'higher quality.' This is irrespective of the talent or experience of the software developer."

> "It doesn't make bad software developers great, but it does make 'bad software developers' better and 'great software developers' greater."

## Deployment Pipeline as Feedback

> "A deployment pipeline is not simply a little workflow of build or test steps; it is a mechanized route from commit to production."

> "If the pipeline says everything is good, there should be no more work to do to make you comfortable to release—nothing…no more integration checks, sign-offs, or staging tests."

## The One-Hour Rule

> "I advise the companies that I work with to aim for creating 'releasable software' at least once per hour."

> "If any single test takes longer than an hour to run or if your software takes longer than an hour to deploy, it won't be possible to run your tests this quickly, however much money you spend on hardware."

## CI vs Feature Branching

> "Continuous integration and feature branching (FB) are not really compatible with each other. One aims to expose change as early as possible; the other works to defer that exposure."

**CI Definition**: "Merging all developers' working copies to a shared mainline several times a day."

**The Problem**: "It is always possible to write code that merge tools will miss; merging code is not necessarily the same as merging behavior."
