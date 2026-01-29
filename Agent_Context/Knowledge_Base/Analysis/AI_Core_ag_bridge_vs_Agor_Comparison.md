# AI_Core Integration Analysis: ag_bridge vs Agor

**Generated:** 2026-01-13  
**Author:** Sisyphus  
**Status:** Analysis Complete

---

## Executive Summary

Two external projects analyzed for AI_Core integration:

| Project | Source | License | Complexity | Key Value |
|---------|--------|---------|------------|-----------|
| **ag_bridge** | Mario4272/ag_bridge (fork: KostaGorod/ag_bridge) | MIT | Low | MCP Server, Mobile UI, Approval Flow |
| **Agor** | preset-io/agor | BSL 1.1 | High | Multi-agent orchestration, Session management |

**Verdict:** **ag_bridge** provides more immediately applicable patterns for AI_Core due to lower complexity and permissive MIT license.

---

## Part 1: ag_bridge Analysis (Mario4272)

### Repository Metadata

| Attribute | Mario4272/ag_bridge | KostaGorod/ag_bridge (our fork) |
|-----------|---------------------|--------------------------------|
| **Stars** | 19 | 0 (fork) |
| **Forks** | 3 | 0 |
| **License** | MIT | MIT |
| **Last Updated** | 2026-01-13 | 2026-01-13 |
| **Status** | Upstream | **Synced, 0 commits ahead** |
| **Languages** | JavaScript (41KB), HTML (20KB) | Same |

### Architecture

```
┌──────────┐     ┌──────────────┐     ┌─────────────────┐     ┌──────────────┐
│  Phone   │────>│ Bridge Server│────>│ Antigravity     │     │ MCP Client   │
│ (Mobile) │     │ (Node.js)    │     │ (Chrome CDP)    │<───>│ (Claude Code)│
└──────────┘     └──────────────┘     └─────────────────┘     └──────────────┘
                      │
                 WebSocket
                 Pairing Code
                 LAN-only
```

### Components

| File | Purpose |
|------|---------|
| `server.mjs` | Express web server, WebSocket, pairing auth, Poke logic |
| `mcp-server.mjs` | MCP server (14+ tools) for agent communication |
| `policy.json` | Tool allow/deny patterns for security |
| `request-approval.mjs` | Human-in-the-loop approval workflow |
| `.ag_Seeds/` | Mobile UI assets (HTML/CSS/JS) |
| `scripts/poke.mjs` | Chrome DevTools Protocol poke script |

### MCP Tools Available

| Tool | Purpose | Policy Pattern |
|------|---------|----------------|
| `messages_inbox` | Read messages (agent/user) | Allow all |
| `messages_send` | Send message to agent/user | Allow all |
| `messages_ack` | Acknowledge message (read/done) | Allow all |
| `agent_heartbeat` | Report agent state (idle/working) | Allow all |
| `checkpoint_post` | Post progress checkpoint | Allow all |
| `poke_agent` | Wake up agent remotely | Allow all |
| `agent_status` | Get agent current status | Allow all |
| `tasks_list` | List pending tasks | Allow all |
| `tasks_get` | Get task details | Allow all |
| `files_list` | List files in directory | `^ls\b`, `^dir\b` |
| `files_read` | Read file contents | `.*` (all) |
| `files_write` | Write/create files | Deny: rm, del, format |

### Top 4 Integration Opportunities (ag_bridge)

| Priority | Feature | Value | Effort | Decision |
|----------|---------|-------|--------|----------|
| **P0** | MCP Server | HIGH | Medium | ✅ Adopt |
| **P1** | Mobile UI Patterns | HIGH | Low | ✅ Adopt |
| **P1** | Approval Workflow | MEDIUM | Medium | ✅ Adopt |
| **P2** | Poke Mechanism | MEDIUM | Low | ✅ Adapt |

### Anti-Patterns to Avoid (ag_bridge)

1. ❌ Node.js sidecar (keep Python-only)
2. ❌ Chrome CDP dependency (use Redis/webhooks)
3. ❌ JSON file state (use Firestore/SQLite)
4. ❌ Hardcoded policies (use database)

---

## Part 2: Agor Analysis (Preset)

### Repository Metadata

| Attribute | preset-io/agor |
|-----------|----------------|
| **Organization** | Preset (Maxime Beauchemin) |
| **License** | BSL 1.1 |
| **Maturity** | Early 2025 |
| **Complexity** | High |

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Agor Daemon                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │  Sessions   │  │   Tasks     │  │  MCP Server         │  │
│  │  Service    │  │   Service   │  │  (14 tools)         │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │ Worktrees   │  │   Users     │  │  Context Service    │  │
│  │ Service     │  │   Service   │  │                     │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                         │
           ┌─────────────┼─────────────┐
           ▼             ▼             ▼
    ┌───────────┐ ┌───────────┐ ┌───────────┐
    │  Executor │ │  Executor │ │  Executor │
    │  (alice)  │ │   (bob)   │ │  (carol)  │
    │ (isolated)│ │ (isolated)│ │ (isolated)│
    └───────────┘ └───────────┘ └───────────┘
```

### Components

| Service | Purpose |
|---------|---------|
| `sessions` | Session lifecycle, spawning, genealogy |
| `tasks` | Task management and tracking |
| `worktrees` | Git worktree isolation per session |
| `users` | User authentication and management |
| `mcp-servers` | MCP tool registry |
| `context` | Agent context sharing |
| `terminals` | Terminal session management |
| `health-monitor` | System health checking |

### Top 10 Domains Where Agor Assists AI_Core

| # | Domain | Value | Decision |
|---|--------|-------|----------|
| 1 | Multi-agent orchestration | HIGH | ✅ Adopt patterns |
| 2 | Secure executor isolation | HIGH | ✅ Adapt for Python |
| 3 | Git-based worktree isolation | HIGH | ⏸️ Defer |
| 4 | Service layer architecture | HIGH | ✅ Adopt patterns |
| 5 | Real-time collaboration | MEDIUM | ⏸️ Future |
| 6 | Structured MCP communication | MEDIUM | ✅ Adopt |
| 7 | Enterprise CLI/DX | MEDIUM | ✅ Adopt patterns |
| 8 | Type-safe database layer | MEDIUM | ✅ Consider Drizzle |
| 9 | Authentication & security | MEDIUM | ✅ Adopt patterns |
| 10 | Agent management UI | LOW | ❌ Skip (out of scope) |

### Brittle Areas (Agor)

| Concern | Severity | Mitigation |
|---------|----------|------------|
| Executor isolation complexity | Critical | Start unified, add isolation later |
| Worktree dependency overhead | Moderate | Make optional |
| FeathersJS learning curve | Moderate | Consider FastAPI alternative |
| BSL 1.1 license | Low | Keep as reference only |
| Early stage project | Moderate | Extract patterns, not APIs |

### Anti-Patterns to Avoid (Agor)

1. ❌ Worktree requirement for every session
2. ❌ Opaque session tokens (not JWTs)
3. ❌ Hybrid JSON schema as default
4. ❌ Executor isolation for local dev
5. ❌ No built-in RBAC

---

## Part 3: AI_Core Current State

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    AI_Core (Monolithic)                     │
│  ┌─────────────────────────────────────────────────────┐   │
│  │            python-telegram-bot (Main Entry)         │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │AgentOrchestrator│ │ChatLLM  │  │  Dashboard (FastAPI)│ │
│  │ (YAML-based)│  │(Council)   │  │  + WebSocket        │ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │ AgentMail   │  │ Firestore   │  │  40+ Feature Modules│ │
│  │ Client      │  │ + SQLite    │  │  (calendar, linear, │ │
│  └─────────────┘  └─────────────┘  │  gmail, ha, etc.)   │ │
│                                    └─────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Existing MCP Integration

AI_Core already has MCP infrastructure:

| Component | Location | Purpose |
|-----------|----------|---------|
| `agent_mail_client.py` | `Projects/AI_Core/src/` | CLI for AgentMail MCP Client |
| `dashboard.py` | `Projects/AI_Core/src/` | Checks MCP Mail server reachability |
| `mcp-server/` | `Agent_Context/Knowledge_Base/` | Existing Node/TS MCP server |
| `HOW_TO_GIVE_ANOTHER_AGENT_ACCESS_TO_MCP_AGENT_MAIL.md` | Knowledge Base | MCP Agent Mail documentation |

### Existing MCP Server Pattern

From `Agent_Context/Knowledge_Base/mcp-server/src/index.ts`:
- Uses `@modelcontextprotocol/sdk` with SSE transport
- Express server with `/sse` and `/message` endpoints
- Simple API key auth via `x-mcp-api-key` header
- 3 tools: `check_docker`, `restart_container`, `check_gpu`

### Gap Analysis

| Capability | AI_Core | ag_bridge | Agor | Gap |
|------------|---------|-----------|------|-----|
| **MCP Server** | Partial (AgentMail) | Full | Full | ✅ Has foundation |
| **Mobile UI** | Telegram only | Native | React Canvas | ❌ Gap |
| **Approval Workflow** | None | Full | Future | ❌ Gap |
| **Multi-Agent** | YAML static | None | Native | ❌ Gap |
| **Session Management** | None | None | Native | ❌ Gap |
| **Tool Policies** | None | Full | Full | ❌ Gap |
| **Real-time Updates** | Polling | WebSocket | WebSocket | ❌ Gap |
| **Service Architecture** | Monolithic | Server-based | 12 services | ❌ Gap |

---

## Part 4: Comparative Matrix

| Dimension | ag_bridge | Agor | AI_Core (Current) |
|-----------|-----------|------|-------------------|
| **Architecture** | Node.js + CDP | FeathersJS + executors | Python + Telegram |
| **Complexity** | Low | High | Medium |
| **License** | MIT | BSL 1.1 | Custom |
| **Maturity** | Established (19 stars) | Early 2025 | Established |
| **Mobile UI** | Native | React Canvas | Telegram |
| **Multi-Agent** | No | Native | Limited (YAML) |
| **Isolation** | None | Worktree + Unix | Process |
| **MCP Tools** | 14+ | 14+ | 4+ (AgentMail) |
| **Real-time** | WebSocket | WebSocket | Polling |
| **Approval Flow** | Yes | Future | No |

---

## Part 5: Integration Recommendations

### Recommended: ag_bridge Patterns

| Priority | Feature | Source | Implementation |
|----------|---------|--------|----------------|
| **P0** | MCP Server (enhanced) | ag_bridge + existing | Python MCP server with 14+ tools |
| **P1** | Dashboard Enhancement | ag_bridge | Mobile-optimized UI, WebSocket |
| **P1** | Approval Workflow | ag_bridge | Human-in-the-loop for sensitive ops |
| **P2** | Poke Mechanism (adapted) | ag_bridge | Redis pub/sub instead of CDP |

### Consider: Agor Patterns (Selective)

| Priority | Feature | Implementation |
|----------|---------|----------------|
| **P1** | Session Management | YAML → Session-based (lighter than Agor) |
| **P2** | Service Architecture | Modular services (FastAPI, not FeathersJS) |
| **P3** | Multi-Agent Spawning | Parent-child agent relationships |

### Skip: Full Agor Adoption

- ❌ Worktree isolation (overkill)
- ❌ FeathersJS backend (learning curve)
- ❌ React canvas UI (out of scope)
- ❌ Executor isolation (complexity)

---

## Part 6: Files Generated

| File | Location | Purpose |
|------|----------|---------|
| `ag_bridge_mario4272_integration.md` | `Analysis/` | Full ag_bridge integration analysis |
| `agor_vs_ai_core_comparison.md` | `Analysis/` | Full Agor comparison |
| `agor_integration_final_report.md` | `Analysis/` | Agor final recommendations |
| `ag_bridge_integration_analysis.md` | `Analysis/` | Previous ag_bridge analysis |
| `THIS FILE` | `Analysis/` | **Combined comparison analysis** |

---

## Part 7: Beads Tracking

| ID | Status | Description |
|----|--------|-------------|
| US-aca | completed | Agor integration analysis |
| US-abb | pending | ag_bridge MCP implementation |
| US-abc | pending | ag_bridge dashboard enhancement |
| US-abd | pending | ag_bridge approval workflow |

---

## Part 8: Fork Management

### ag_bridge Fork Workflow

```
Our fork: KostaGorod/ag_bridge
         ↑
         │ Sync from upstream
         │
Upstream: Mario4272/ag_bridge

# Sync command when upstream updates:
gh repo sync KostaGorod/ag_bridge --base-owner Mario4272 --force
```

---

## Conclusion

### Key Takeaways

1. **ag_bridge** provides immediately applicable patterns (MCP, Mobile UI, Approval)
2. **Agor** provides architectural patterns for future multi-agent evolution
3. **AI_Core** has MCP foundation (AgentMail) to build upon
4. **Selective adoption** from both projects is recommended

### Recommended Next Steps

1. **Phase 1 (Week 1-2):** Implement Python MCP server with ag_bridge patterns
2. **Phase 2 (Week 2-3):** Enhance dashboard with mobile UI patterns
3. **Phase 3 (Week 3-4):** Add approval workflow for sensitive operations
4. **Phase 4 (Week 4-5):** Adapt "Poke" mechanism using Redis pub/sub
5. **Phase 5 (Future):** Consider Agor patterns for multi-agent evolution

### Success Criteria

- ✅ MCP tools callable from Claude Code / Cursor
- ✅ Mobile-friendly dashboard access
- ✅ Human approval for sensitive commands
- ✅ Real-time status updates via WebSocket
- ✅ Policy-controlled tool permissions
