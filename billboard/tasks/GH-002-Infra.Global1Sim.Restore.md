---
Task-Id: GH-0000 # Replace with Issue Number
Task-Semantic: Context.Capability.Outcome # e.g. ContentFactory.Youtube.UploadVideo
Context: ContextName
Owner: AgentOrHuman
Status: Proposed # Proposed | Claimed | Verified | Done
Lease-Until: YYYY-MM-DD # Optional
---
Task-Id: GH-002
Task-Semantic: Infrastructure.Git.Global1Sim
Context: Infrastructure
Owner: Kostya
Status: Blocked
Lease-Until: 2026-01-20
---

Restore Global1Sim Submodule Access
====================================

**Objective:**
Fix the `Repository not found` error for `Projects/global1sim` which is causing
sync warnings. This is a High Priority blocker for clean deployment.

Description
------------

The submodule defined in `.gitmodules` points to
`https://github.com/KostaGorod/global1sim.git`, but authentication fails during
cloning on both local and remote environments.

Acceptance Criteria
--------------------

- [ ] Repository `KostaGorod/global1sim` is accessible via HTTPS or SSH.
- [ ] `git submodule update --init --recursive` completes without errors.
- [ ] Sync script output is free of "Failed to clone" warnings.

Traceability
-------------

- **Parent Goal:** Unified System Stability
- **Blocking:** Full System Sync (Clean State)

REP Sensitivities
------------------

- IF `global1sim` repo is deleted, THEN remove it from `.gitmodules` entirely.
- IF specific SSH keys are needed, THEN update `~/.ssh/config` on the remote
  server.
