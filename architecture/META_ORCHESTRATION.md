# 🏛️ Unified System: Meta-Orchestration Architecture
>
> **Status:** Draft (Waiting for Council Approval)
> **Author:** LLM Council (via OrangeStone)
> **Date:** 2026-01-10

## 1. Executive Summary

The Unified System has grown beyond simple scripts into a multi-agent, multi-user ecosystem. We propose a **Meta-Orchestration Layer** to centralize control over Resources (Keys), Identities (Accounts), and Processes (Automations). This eliminates hardcoded dependencies and enables "Family Swarm" capabilities.

---

## 2. The Three Pillars of Control

### 🔐 A. Resource Orchestrator (The Vault)

**Purpose:** Dynamic management of API tokens, quotas, and billing aggregation.
**Problem Solved:** "Who's paying for this generation? Which key is not rate-limited?"

**Structure:**

- **`TokenBroker` Service:** A local API/Library that agents call to get a valid key.
  - `get_key(provider="openai", capability="gpt-4", cost_tier="high")` -> Returns `sk-proj-777...`
- **Family Pools:**
  - `Pool_Igor`: High priority, Dev usage.
  - `Pool_Artur`: Production content, Bypass age limits.
  - `Pool_Kosta`: Remote agent operations.
- **Policies:**
  - *Load Balancing:* Round-robin keys to avoid strict rate limits.
  - *Failover:* If Key A fails (429/401), automatically retry with Key B.

### 🆔 B. Identity Orchestrator (The Passport)

**Purpose:** Managing external accounts (Google, Telegram, Instagram, GitHub) and Auth sessions.
**Problem Solved:** "Bot lost Google access", "Script needs to post to Instagram as 'ContentFarm'".

**Structure:**

- **`SessionStore` (Encrypted DB):** Secure storage for OAuth tokens (Google), Session IDs (Insta), SSH keys.
- **RBAC (Role-Based Access Control):**
  - Agent `FuchsiaCat` can *read* Mail but *cannot* delete Repositories.
  - Script `DailyFactory` can *post* to Instagram but *cannot* change passwords.

### ⚙️ C. Automation Orchestrator (The Conductor)

**Purpose:** Defining and executing complex, multi-step workflows across agents.
**Problem Solved:** "Daily Research -> Generate Video -> Review by Human -> Post".

**Structure:**

- **`Mission definitions` (YAML):** declarative workflow files.

  ```yaml
  name: "Daily Viral Video"
  trigger: "cron(0 10 * * *)"
  steps:
    - task: "research_topic"
      agent: "OrangeStone"
      resource_tier: "low"
    - task: "generate_assets"
      agent: "OrangeStone"
      resource_tier: "high" (Pool_Artur)
    - task: "approve_content"
      agent: "Human (Igor)"
      timeout: "2h"
  ```

- **State Machine:** Tracks progress. If step 2 fails, it alerts Human, doesn't crash silently.

---

## 3. Implementation Roadmap

### Phase 1: Foundation (Immediate)

1. **Define `resources.yaml` v2:** Standardized format for Multi-Key Pools.
2. **Deploy `TokenBroker`:** Simple Python class to load keys and rotate them.
3. **Update `docker-compose`:** Mount `secrets/` volume globally for all containers.

### Phase 2: Integration (Next Week)

1. **Refactor Factory:** Update `daily_researcher.py` to use `TokenBroker.get_key()`.
2. **Refactor Bot:** Update Telegram Bot to use `IdentityOrchestrator` for Google Auth.

### Phase 3: Autonomy (Future)

1. **Agent Council:** Agents (PinkLake, FuchsiaCat) vote on resource allocation.
2. **Self-Healing:** System automatically replaces expired keys/tokens if possible.

---

## 4. Request for Approval

**To:** FuchsiaCat (Kostya), PinkLake
**Action:** Review this architecture.
**Vote:**

- [ ] **Approve:** Proceed to implementation.
- [ ] **Reject:** Propose changes.
