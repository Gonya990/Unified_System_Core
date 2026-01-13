---
Task-Id: GH-0000 # Replace with Issue Number
Task-Semantic: Context.Capability.Outcome # e.g. ContentFactory.Youtube.UploadVideo
Context: ContextName
Owner: AgentOrHuman
Status: Proposed # Proposed | Claimed | Verified | Done
Lease-Until: YYYY-MM-DD # Optional
---

# 📋 Task: [Human Readable Title]

## 🎯 Objective

Briefly explain *what* needs to be done and *why*.

## ✅ Acceptance Criteria (The Definition of Done)

*Criteria must be machine-checkable where possible.*

- [ ] **Given** [Initial State], **When** [Action], **Then** [Result] (Test: `test_name.py`)
- [ ] Policy/Check 2

## 🔗 Traceability

- **Discussion:** [Link to GitHub Issue]
- **PRs:**
  - [ ] [PR-123](url)
- **Decisions (ADRs):**
  - [ ] [ADR-001](url)

## 📡 REP Sensitivities (Planned)

*What environmental variables does this task depend on?*

- IF `API_VERSION` changes, THEN `Client` must update.
