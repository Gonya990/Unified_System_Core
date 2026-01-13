# Agor Integration: Final Analysis & Recommendations

**Generated:** 2026-01-13  
**Author:** Sisyphus  
**Status:** Analysis Complete - Ready for Implementation Planning

---

## Executive Summary

Analyzed **Agor** (preset-io/agor) as a potential architectural reference for evolving **AI_Core** from a monolithic Telegram bot to a multi-agent orchestration platform.

**Verdict:** **Selective Adoption Recommended** - Agor provides enterprise-grade patterns for agent orchestration, but full adoption is over-engineered for current needs. Extract key patterns (sessions, spawning, MCP) while maintaining Telegram-first architecture.

---

## Comparative Overview

| Dimension | AI_Core (Current) | Agor (Reference) |
|-----------|-------------------|------------------|
| **Architecture** | Monolithic async Python | Distributed multi-process (daemon + executors) |
| **Entry Point** | python-telegram-bot | FeathersJS REST + WebSocket |
| **Multi-Agent** | YAML-based static orchestration | Native spawning, fork, genealogy |
| **Isolation** | Process-level | Worktree + Unix user isolation |
| **Database** | Firestore + SQLite mixed | LibSQL/Drizzle + JSON blobs |
| **Frontend** | Minimal dashboard | React + Ant Design + React Flow |
| **Agents** | 46 Python modules | 12 FeathersJS services + MCP tools |
| **License** | Custom | BSL 1.1 |
| **Maturity** | Established 2024-2025 | Early 2025 (active dev) |

---

## Top 10 Domains Where Agor Assists AI_Core

### HIGH VALUE (Critical Gaps)

#### 1. Multi-Agent Orchestration
**Problem:** AgentOrchestrator is YAML-based, static, no spawning
**Agor Solution:** Native session spawning with parent-child relationships
**Migration Value:** HIGH - Core architectural gap

#### 2. Secure Executor Isolation  
**Problem:** Single process, no credential isolation, direct env var access
**Agor Solution:** Process separation, Unix user isolation, IPC with JSON-RPC 2.0
**Migration Value:** HIGH - Security hardening

#### 3. Git-Based Worktree Isolation
**Problem:** No parallel session isolation, no git integration
**Agor Solution:** Every session requires worktree, parallel development without branch switching
**Migration Value:** HIGH - Critical for agent development workflows

#### 4. Service Layer Architecture
**Problem:** Monolithic modules with mixed concerns, tight coupling
**Agor Solution:** 12 FeathersJS services with hooks for validation/auth
**Migration Value:** HIGH - Foundation for future growth

### MEDIUM VALUE (Nice to Have)

#### 5. Real-Time Collaboration & State Sync
**Problem:** Telegram is async-only, no real-time state sync, polling-based dashboard
**Agor Solution:** WebSocket broadcasting, cursor presence (100ms throttle), optimistic UI
**Migration Value:** MEDIUM - Future expansion

#### 6. Structured Agent Communication (MCP)
**Problem:** No MCP server, manual API integrations, no programmatic access
**Agor Solution:** 14 MCP tools (sessions, worktrees, boards, tasks, users)
**Migration Value:** MEDIUM - Enables automation

#### 7. Enterprise-Grade CLI & DX
**Problem:** ad-hoc command handlers, minimal documentation
**Agor Solution:** oclif-based CLI, comprehensive SDK (Claude, Codex, Gemini)
**Migration Value:** MEDIUM - Developer experience

#### 8. Type-Safe Database Layer
**Problem:** Mixed Firestore + SQLite, manual JSON serialization, no ORM
**Agor Solution:** Drizzle ORM with type safety, hybrid schema (columns + JSON blobs)
**Migration Value:** MEDIUM - Maintainability

#### 9. Authentication & Security Model
**Problem:** Simple ALLOWED_USERS list, no formal auth, API keys in env vars
**Agor Solution:** 4 auth strategies (Anonymous, Local, JWT, Session Token)
**Migration Value:** MEDIUM - Security hardening

### LOW VALUE (Out of Scope)

#### 10. Agent Management UI
**Problem:** Telegram-only UI, no visual workflow representation
**Agor Solution:** React + Ant Design + React Flow for interactive canvas
**Migration Value:** LOW - Out of scope for Telegram-first use case

---

## Brittle Areas & Concerns

### Critical Concerns (Must Address)

#### 1. Executor Isolation Complexity
- **Issue:** Requires separate Unix users per session (agor_alice, agor_bob, etc.)
- **Risk:** HIGH - Operational complexity, may not work in containers without root
- **Mitigation:** Start with unified model, add isolation only for production

#### 2. Worktree Dependency Overhead
- **Issue:** Every session requires a git worktree (500ms+ overhead)
- **Risk:** MEDIUM - AI_Core handles non-code tasks (chat, HA control)
- **Mitigation:** Make worktree optional, fallback to temp directories

### Moderate Concerns (Should Evaluate)

#### 3. FeathersJS Learning Curve
- **Issue:** Adopting Agor means adopting service hooks + Socket.IO patterns
- **Risk:** MEDIUM - Team familiar with async/await, not service hooks
- **Mitigation:** Consider FastAPI + async SQLAlchemy as alternative

#### 4. BSL 1.1 License
- **Issue:** Free for internal use, requires license for production/commercial
- **Risk:** LOW - Internal use is free, limits future distribution
- **Mitigation:** Keep Agor as reference architecture only

#### 5. Early Stage Project
- **Issue:** Late 2025 release, limited community, API may change
- **Risk:** MEDIUM - Could face unexpected issues
- **Mitigation:** Extract patterns, don't depend on specific APIs

### Low Concerns (Acceptable)

#### 6. Frontend Dependency - Canvas/UI
- **Issue:** Full experience requires React stack
- **Risk:** LOW - Can use CLI/MCP only without frontend

#### 7. LibSQL Choice
- **Issue:** Fork of SQLite, less battle-tested
- **Risk:** LOW - Can switch to PostgreSQL later

#### 8. MCP Server Single Point
- **Issue:** MCP runs on daemon process
- **Risk:** LOW - Acceptable for single-node deployments

---

## Anti-Patterns to Avoid

### 1. Worktree Requirement for Every Session
**Agor Pattern:** Foreign key relationship - every session requires worktree
**Problem:** Adds overhead for non-code tasks (chat, HA control)
**Avoid:** Make worktree optional

### 2. Opaque Session Tokens (Not JWTs)
**Agor Pattern:** UUID-based opaque tokens, database lookup for every validation
**Problem:** No offline validation, extra DB load
**Avoid:** Use JWTs for user authentication

### 3. Hybrid JSON Schema as Default
**Agor Pattern:** JSON blobs for flexible data (loses type safety)
**Problem:** Harder to query, no schema evolution
**Avoid:** Use proper typed schemas, only JSON for truly dynamic fields

### 4. Executor Isolation Overkill for Local
**Agor Pattern:** Process separation + Unix users for every session
**Problem:** Overhead for local development
**Avoid:** Provide unified (dev) and isolated (prod) modes

### 5. No Built-in RBAC
**Agor Pattern:** All-or-nothing access, per-service permissions future work
**Problem:** No user roles, no granular permissions
**Avoid:** Implement RBAC before production use

---

## Recommended Integration Strategy

### Phase 1: Learn & Prototype (Week 1-2)
```
1. Deploy Agor locally alongside AI_Core
2. Test MCP tools with Claude Code
3. Understand worktree workflow
4. Identify which patterns apply to AI_Core
```

### Phase 2: Selective Adoption (Week 3-6)
```
✓ Adopt:   AgentOrchestrator upgrade (structured YAML → Agor sessions)
✓ Adopt:   Multi-agent spawning (limited use for complex tasks)
✓ Adopt:   Drizzle ORM for new modules
✗ Skip:    Frontend + Canvas (out of scope)
✗ Skip:    Worktree isolation (use temp directories instead)
```

### Phase 3: Hybrid Architecture (Week 7+)
```
1. Run Agor daemon for multi-agent tasks
2. Keep Telegram bot for user interaction
3. Bridge via MCP tools
4. Share database layer (Agor's services + AI_Core's modules)
```

---

## Technical Specifications Needed

### Spec 1: Session Management Design
- Session lifecycle (create, fork, terminate)
- Parent-child relationship tracking
- State persistence strategy

### Spec 2: Agent Spawning Protocol
- Spawn API design
- Resource limits per agent
- Communication channels (IPC vs message queue)

### Spec 3: MCP Integration Layer
- Which MCP tools to implement
- Security model for MCP access
- Integration with existing modules

### Spec 4: Isolation Strategy
- Dev mode (unified process)
- Prod mode (isolated executors)
- Hybrid approach with temp directories

---

## Files Generated

| File | Location | Purpose |
|------|----------|---------|
| `agor_vs_ai_core_comparison.md` | `Agent_Context/Knowledge_Base/Analysis/` | Full comparative analysis |
| `agor_integration_final_report.md` | `Agent_Context/Knowledge_Base/Analysis/` | This document |

---

## Beads Tracking

| ID | Status | Description |
|----|--------|-------------|
| US-aca | in_progress | Agor Integration: Deep Analysis & Specs Draft |

---

## Conclusion

Agor provides **enterprise-grade patterns** for agent orchestration that would significantly improve AI_Core's multi-agent capabilities, security isolation, and maintainability.

However, the **full Agor stack is over-engineered** for AI_Core's current Telegram-first architecture. A **selective adoption strategy**—taking only the useful patterns (sessions, spawning, MCP tools)—while keeping the core architecture intact is the recommended approach.

**Next Immediate Actions:**
1. Igor agents to review analysis and provide feedback
2. Draft integration specs for Phase 1 (Session Management)
3. Prototype session-based AgentOrchestrator v2
4. Evaluate MCP tool utility for AI_Core use cases
