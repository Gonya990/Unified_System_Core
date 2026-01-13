# 🏗️ Phase 6 Implementation Plan: Distributed Agent Clockwork

> **Status:** 🚧 In Progress
> **Goal:** Transition the Unified System to a Distributed, Non-Federated Agent
> Architecture using Billboard, Mailboxes, Beads, and REP.

---

## 🧭 Vision: The Clockwork

We are moving from a set of scripts to a robust **Engineering System** where:

1. **Billboard (Control Plane):** Shared intent, tasks, and acceptance criteria.
2. **Beads (Execution Log):** Granular commits linking to tasks.
3. **REP (Alignment Signal):** Change sensitivities ("IF X THEN Y") committed
    to the repo.
4. **CI/CD (Sensor/Gate):** "Done" is derived only from merged code + green
    checks.

---

## 📝 Roadmap

### Phase 1: Foundation (The Skeleton) 🏗️

- [ ] **Directory Structure:** Create `billboard/`, `contexts/`, `rep/claims/`.
- [ ] **Domain Vision:** Create `billboard/spec.md` identifying the Core Domain
    and Ubiquitous Language.
- [ ] **Task Template:** Create `billboard/tasks/TEMPLATE.md` with required
    frontmatter (`Task-Id`, `Context`, `Outcome`).
- [ ] **REP Store:** Create `rep/claims/` directory for distilled signals.

### Phase 2: The Mechanisms (Tooling) ⚙️

- [ ] **REP Distiller:** Create `Scripts/Orchestration/rep_distiller.py`.
  - Input: Git commit trailers (free text).
  - Output: Structured JSON in `rep/claims/`.
- [ ] **Task Validator:** Create `Scripts/Orchestration/validate_task.py`.
  - Ensures every task has a valid `Task-Id` and `Context`.
- [ ] **Clockwork CI:** Define GitHub Actions (or local hooks) to enforce:
  - No commit without `Task-Id` trailer.
  - No merge without passing tests.

### Phase 3: Migration & Organization 📦

- [ ] **Context Mapping:** Identify Bounded Contexts for current scripts (e.g.,
    `FamilyAssistant`, `ContentFactory`, `Infrastructure`).
- [ ] **Refactor:** Move `Scripts/` into `contexts/<ContextName>/`.
- [ ] **Backfill:** Create Billboard tasks for active work (e.g., "Fix
    YouTube Uploads").

### Phase 4: Knowledge & Grounding (Vertex AI) 📚

- [ ] **Vertex AI Search:** Index documentation and project logs for static
    grounding.
- [ ] **Unified Function Calling:** Standardize system APIs (MCP, HomeAssistant)
    into Vertex Function schemas.
- [ ] **Grounding Gate:** Implement a check where agent actions are verified
    against the Knowledge Base.

---

## 📐 Architecture Specs

### 1. Billboard (Canonical Truth)

- **Location:** `billboard/tasks/GH-<IssueID>-<SemanticSlug>.md`
- **Format:** Markdown with YAML Frontmatter.
- **Rule:** One file per task.

### 2. Task Identity

- **Immutable ID:** `GH-<Number>` (e.g., `GH-101`)
- **Semantic Slug:** `Context.Capability.Outcome`
    (e.g., `ContentFactory.Youtube.UploadVideo`)

### 3. REP (Ripple Effect Protocol)

- **Authoring:** Commit Trailers.

    ```text
    Task-Id: GH-101
    REP-Sensitivity: IF YouTube API quota limit drops THEN switch to daily-only
    uploads BECAUSE quota is shared.
    REP-Variables: quota, api_policy
    ```

- **Storage:** `rep/claims/<commit_sha>.json` (Distilled by bot/script).

### 4. Bounded Contexts

- `contexts/FamilyAssistant`: Morning Brief, Homework Sentinel.
- `contexts/ContentFactory`: Video production, Social uploads.
- `contexts/Infrastructure`: Mail Processor, TokenBroker.

---

## 🚀 Execution Steps (Next)

1. Initialize Directory Structure.
2. Create `billboard/spec.md`.
3. Create the REP Distiller script.
