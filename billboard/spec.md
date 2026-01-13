# 🌍 System Specification & Domain Vision

> **System:** Distributed, Non-Federated Agent Ecosystem
> **Architecture:** The Clockwork (Billboard + Beads + REP)

---

## 🎯 Core Domain: Autonomous Coordination

The core value of this system is **coordination without centralization**. Agents operate as independent entities (non-federated) but align through a shared "blackboard" and explicit sensitivity signals.

## 🗣️ Ubiquitous Language

* **Billboard:** The shared control plane containing the "desired state" (Intent, Tasks, Decisions).
  * *Source of Truth:* This directory (`billboard/`).
* **Bead:** A granular unit of execution (Git Commit/PR) that transitions the system state.
  * *Rule:* Every Bead must link to a Billboard Task.
* **Mailbox:** A P2P channel for private negotiation between agents (before posting to Billboard).
* **REP (Ripple Effect Protocol):** A mechanism for sharing "sensitivities" (change vectors).
  * *Signal:* "IF X changes THEN Y must adapt."
* **Bounded Context:** A distinct subsystem with its own ubiquitous language and models (e.g., `FamilyAssistant`, `ContentFactory`).
* **Clockwork:** The cyclical process of Intent (Billboard) -> Action (Bead) -> Sensor (CI) -> Alignment (REP).

---

## 🗺️ Context Map

### 1. FamilyAssistant Context

* **Responsibility:** personal life support, school tracking, daily briefs.
* **Key Models:** `Homework`, `Grade`, `MorningBrief`.

### 2. ContentFactory Context

* **Responsibility:** Automated media production and distribution.
* **Key Models:** `Topic`, `Script`, `Video`, `SocialPlatform`.

### 3. Infrastructure Context

* **Responsibility:** The plumbing that enables agents to exist.
* **Key Models:** `MailProcessor`, `TokenBroker`, `AgentIdentity`.

---

## 📏 Invariants & Policies

1. **Traceability:** Every change in code MUST link to a task in `billboard/tasks/`.
2. **Derivation of Done:** A task is DONE only when its code is merged and all CI checks pass.
3. **Sensitivity:** Major architectural decisions MUST be accompanied by an REP sensitivity claim in the commit trailer.
