# 📋 Billboard Spec: The Engineering Truth

## Vision

The Billboard is the centralized control plane for all agents and automation loops
within the Unified System Core. It represents the "Immutable Truth" of tasks,
intents, and capabilities.

## Architecture

### 1. Bounded Contexts

All system logic is mapped to discrete Bounded Contexts:

- **FamilyAssistant**: Managing home life, morning briefs, schedules.
- **ContentFactory**: Video processing, TikTok/Reels uploads, voice synthesis.
- **Infrastructure**: GKE Bot management, proxy routing, token rotation.

### 2. Task Definition (`billboard/tasks/`)

Each task is an independent Markdown document with YAML frontmatter:

```yaml
Task-Id: GH-[Number]
Context: [ContextName]
Capability: [CapabilityName]
Status: Pending | Active | Completed
```

The body must define the exact **Outcome** and **Verification** steps.

### 3. REP (Ripple Effect Protocol)

Agents will trace logical dependencies by writing output claims to `rep/claims/`.
When an agent completes a task, it generates a JSON artifact containing:

- Output variables
- Sensitivities (e.g. IF YouTube quota changes THEN alert)

## Rules of Execution

1. No agent can act without an assigned `Task-Id`.
2. A task is not "Done" until the corresponding CI/CD pipeline or verification
   check passes.
3. Errors must be logged to the task's issue, not just swallowed in standard out.
