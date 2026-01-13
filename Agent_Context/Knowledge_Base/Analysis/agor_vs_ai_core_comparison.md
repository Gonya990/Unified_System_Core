# Agor vs AI_Core: Comparative Analysis

**Generated:** 2026-01-13 | **Author:** Sisyphus | **Context:** Unified System Core

---

## Executive Summary

**Agor** (by Preset) is a **multi-client agent orchestration platform** with real-time collaboration, worktree isolation, and enterprise-grade architecture. **AI_Core** is a **monolithic Telegram bot** with multi-LLM support and smart home integration.

| Aspect | Agor | AI_Core |
|--------|------|---------|
| **Architecture** | Distributed, multi-process (daemon + executors) | Monolithic async Python |
| **Communication** | FeathersJS REST + WebSocket | Telegram Bot API |
| **Multi-Agent** | Native (spawn, fork, genealogy) | AgentOrchestrator (limited YAML agents) |
| **Isolation** | Worktree-based (git) | Process-level only |
| **Database** | LibSQL/Drizzle + JSON blobs | Firestore + SQLite |
| **Frontend** | React + Ant Design + React Flow | Minimal web dashboard |
| **Maturity** | Early 2025, actively developed | Established 2024-2025 |
| **License** | BSL 1.1 | Custom (Unified System) |

---

## Top 10 Domains Where Agor Will Assist AI_Core

### 1. Agent Orchestration & Multi-Agent Workflows

**Agor Strengths:**
- Native session spawning with parent-child relationships
- Worktree-based isolation per session
- Agent genealogy tracking
- Multi-player real-time canvas

**AI_Core Gap:**
- AgentOrchestrator exists but is YAML-based and static
- No real multi-agent delegation
- No session isolation

**Migration Value:** HIGH - This is the core architectural gap

### 2. Real-Time Collaboration & State Sync

**Agor Strengths:**
- FeathersJS real-time events (created/patched/removed/updated)
- WebSocket broadcasting to all clients
- Cursor position + presence updates (100ms throttle)
- Optimistic UI via React hooks

**AI_Core Gap:**
- Telegram is async, no real-time state sync
- No collaboration features
- Dashboard is polling-based

**Migration Value:** MEDIUM - Nice to have for future expansion

### 3. Structured Agent Communication (MCP)

**Agor Strengths:**
- 14 MCP tools (sessions, worktrees, boards, tasks, users)
- Self-aware agents (can query their own session context)
- Session-scoped security tokens
- No manual MCP configuration needed

**AI_Core Gap:**
- No MCP server
- Manual API integrations
- No structured programmatic access

**Migration Value:** MEDIUM - Enables better automation

### 4. Secure Executor Isolation

**Agor Strengths:**
- Executor Isolation model (process separation)
- Unix user isolation per session (agor_alice, agor_bob, etc.)
- No direct database access for executors
- Just-in-time API keys via IPC
- Session token authentication (not JWTs)

**AI_Core Gap:**
- All code runs in single process
- No credential isolation
- Direct environment variable access

**Migration Value:** HIGH - Security improvement

### 5. Git-Based Worktree Isolation

**Agor Strengths:**
- Every session requires a worktree (foreign key)
- Parallel development without branch switching
- Natural fork/spawn operation mapping
- Credential isolation via ~/.ssh/ ownership

**AI_Core Gap:**
- No git integration for sessions
- No worktree concept
- No parallel session isolation

**Migration Value:** HIGH - Critical for agent development workflows

### 6. Enterprise-Grade CLI & DX

**Agor Strengths:**
- oclif-based CLI
- Comprehensive SDK (Claude, Codex, Gemini)
- Development guide + architecture docs
- Docker + containerized execution modes

**AI_Core Gap:**
- No structured CLI
- ad-hoc command handlers
- Minimal documentation

**Migration Value:** MEDIUM - Developer experience

### 7. Type-Safe Database Layer

**Agor Strengths:**
- Drizzle ORM with type safety
- LibSQL (SQLite-compatible) for local
- Hybrid schema (indexed columns + JSON blobs)
- Cross-database compatibility

**AI_Core Gap:**
- Mixed Firestore + SQLite
- No ORM layer
- Manual JSON serialization

**Migration Value:** MEDIUM - Maintainability improvement

### 8. Service Layer Architecture

**Agor Strengths:**
- 12 FeathersJS services (sessions, tasks, messages, boards, worktrees, repos, users, mcp-servers, context, terminals, health-monitor)
- Hooks for validation/auth
- Consistent business logic
- Future RBAC support

**AI_Core Gap:**
- Monolithic modules with mixed concerns
- No service abstraction
- Tight coupling throughout

**Migration Value:** HIGH - Foundation for future growth

### 9. User Interface for Agent Management

**Agor Strengths:**
- React 18 + Vite with HMR
- Ant Design enterprise components
- React Flow for interactive session canvas
- Real-time multiplayer visualization

**AI_Core Gap:**
- Minimal dashboard (status + logs)
- Telegram-only UI
- No visual workflow representation

**Migration Value:** LOW - Out of scope for current use case

### 10. Authentication & Security Model

**Agor Strengths:**
- 4 authentication strategies (Anonymous, Local, JWT, Session Token)
- FeathersJS authentication with configurable storage
- Session token strategy (opaque UUIDs, 24h expiration)
- Credential isolation via Unix users

**AI_Core Gap:**
- Simple ALLOWED_USERS list
- No formal auth layer
- API keys in environment variables

**Migration Value:** MEDIUM - Security hardening

---

## Brittle Areas & Concerns in Adopting Agor Patterns

### Critical Concerns

#### 1. Executor Isolation Complexity

**Problem:** Agor's executor isolation model requires:
- Separate Unix users per session
- Custom session token strategy in FeathersJS
- IPC via Unix sockets with JSON-RPC 2.0

**Risk:** HIGH - Significant operational complexity, may not work in containerized environments without root

**Recommendation:** Start with unified model, add isolation later if needed

#### 2. Worktree Dependency

**Problem:** Every session requires a git worktree, which:
- Requires bare repo infrastructure
- May not work for non-code tasks
- Adds 500ms+ overhead per session

**Risk:** MEDIUM - AI_Core handles non-code tasks (chat, HA control) that don't need worktrees

**Recommendation:** Make worktree optional, fallback to temp directories

#### 3. FeathersJS Learning Curve

**Problem:** Adopting Agor means adopting:
- FeathersJS service patterns
- Hook-based middleware
- Socket.IO real-time events

**Risk:** MEDIUM - Team is familiar with async/await patterns, not service hooks

**Recommendation:** Consider FastAPI + async SQLAlchemy as alternative

### Moderate Concerns

#### 4. BSL 1.1 License

**Problem:** Agor is under Business Source License 1.1:
- Free for development/internal use
- Requires license for production/commercial use
- Changes must be shared with Preset

**Risk:** LOW - Internal use is free, but limits future distribution

#### 5. Early Stage Project

**Problem:** Agor is new (late 2025):
- Limited community
- API may change
- Few real-world deployments

**Risk:** MEDIUM - Could face unexpected issues

#### 6. Frontend Dependency

**Problem:** Full Agor experience requires React + Ant Design + React Flow stack:
- Requires frontend expertise
- Adds deployment complexity
- May not integrate with Telegram-first workflow

**Risk:** LOW - Can use CLI/MCP only without frontend

### Low Concerns

#### 7. LibSQL Choice

**Problem:** Using LibSQL (fork of SQLite) for production:
- Less battle-tested than PostgreSQL/MySQL
- May have edge case bugs
- Limited hosting options

**Risk:** LOW - Can switch to PostgreSQL later (hybrid schema)

#### 8. MCP Server Integration

**Problem:** MCP server runs on same process as daemon:
- If daemon crashes, MCP goes down
- No horizontal scaling without changes

**Risk:** LOW - Acceptable for single-node deployments

---

## Bad Parts of Agor (Anti-Patterns)

### 1. Over-Engineered for Simple Use Cases

Agor assumes you need:
- Worktrees for every task
- Real-time multiplayer for single users
- MCP tools for everything

**For AI_Core:** Start with CLI only, skip canvas/MCP if not needed

### 2. Opaque Session Tokens (Not JWTs)

Session tokens are opaque UUIDs without claims:
- Can't inspect token contents
- Requires database lookup for every validation
- No offline validation possible

**For AI_Core:** JWTs would be simpler for user authentication

### 3. Hybrid Schema as Default

Using JSON blobs for flexible data:
- Loses type safety
- Harder to query
- Migration-free but also migration-*less* (no schema evolution)

**For AI_Core:** Use proper typed schemas, only use JSON for truly dynamic fields

### 4. Executor Isolation Overkill for Local Use

For local development, the isolation model adds:
- Process overhead
- User management complexity
- IPC latency

**For AI_Core:** Provide both unified (dev) and isolated (prod) modes

### 5. No Built-in RABC Yet

Role-based access control is "future work":
- Currently all-or-nothing access
- No per-service permissions
- No user roles

**For AI_Core:** Implement RBAC before production use

---

## Recommended Integration Strategy

### Phase 1: Learn & Prototype (Week 1-2)

1. Deploy Agor locally alongside AI_Core
2. Test MCP tools with Claude Code
3. Understand worktree workflow
4. Identify which patterns apply to AI_Core

### Phase 2: Selective Adoption (Week 3-6)

1. **Adopt:** AgentOrchestrator upgrade (structured YAML → Agor sessions)
2. **Adopt:** Multi-agent spawning (limited use for complex tasks)
3. **Adopt:** Drizzle ORM for new modules
4. **Skip:** Frontend + Canvas (out of scope)
5. **Skip:** Worktree isolation (use temp directories instead)

### Phase 3: Hybrid Architecture (Week 7+)

1. Run Agor daemon for multi-agent tasks
2. Keep Telegram bot for user interaction
3. Bridge via MCP tools
4. Share database layer (Agor's services + AI_Core's modules)

---

## Conclusion

Agor provides **enterprise-grade patterns** for agent orchestration that would significantly improve AI_Core's:
- Multi-agent capabilities
- Security isolation
- Developer experience
- Maintainability

However, the full Agor stack is **over-engineered** for AI_Core's current needs. A **selective adoption** strategy—taking only the useful patterns (sessions, spawning, MCP tools)—while keeping the Telegram-first architecture is recommended.

**Next Steps:**
1. Create beads for deeper analysis
2. Draft integration specs
3. Prototype session management
4. Evaluate MCP tool utility
