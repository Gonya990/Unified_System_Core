---
Task-Id: GH-003
Task-Semantic: Core.Governance.Conscience
Context: Core
Owner: Antigravity
Status: Done
Lease-Until: 2026-01-20
---

# 📋 Task: Implement "System Conscience" (Governance Layer)

## Objective

Integrate a morality/rules engine that parses `NOTEBOOK.md` to enforce
operational constraints on the Unified System controller.

## 📝 Description

The system needs a way to respect "soft rules" (like "don't deploy if broken" or
"don't spam") dynamically without hardcoding them into every script.
The `conscience.py` module acts as a middleware in `unified.py`.

## ✅ Acceptance Criteria

- [x] `Scripts/Core/conscience.py` exists and parses `NOTEBOOK.md`.
- [x] `unified.py` imports and uses Conscience to check critical actions.
- [x] Menu option "7. Conscience" displays active rules.
- [x] Deploy actions (Sync) are blocked if a rule forbids deployment.

## 🔗 Traceability

- **Parent Goal:** Unified System Intelligence
- **Relates to:** `NOTEBOOK.md` (Source of Truth)

## 📡 REP Sensitivities

- IF `NOTEBOOK.md` is missing, THEN Conscience warns but allows actions
  (fail-open).
- IF `unified.py` structure changes, THEN Conscience integration must be
  preserved.
