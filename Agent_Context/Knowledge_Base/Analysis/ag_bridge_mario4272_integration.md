# ag_bridge Integration Analysis (Mario4272/upstream)

**Generated:** 2026-01-13  
**Author:** Sisyphus  
**Context:** Comparative analysis of `Mario4272/ag_bridge` for AI_Core integration  
**Fork Target:** `KostaGorod/ag_bridge` (fork of Mario4272/ag_bridge - synced, 0 commits ahead)

---

## Executive Summary

**ag_bridge** is a **mobile interface for Antigravity Agent** that enables remote control via phone. It provides mobile chat, remote wake-up ("The Poke"), and MCP integration.

**Verdict for AI_Core:** **HIGH INTEGRATION VALUE** - MCP server patterns, mobile UI patterns, and approval workflow are directly applicable. The "Poke" mechanism needs adaptation for Python.

**Note on Fork:** We should work on **`KostaGorod/ag_bridge`** (our fork) rather than directly on Mario4272/upstream. The fork is currently synced (0 commits ahead, 0 behind).

---

## Repository Metadata

| Attribute | Mario4272/ag_bridge | KostaGorod/ag_bridge (our fork) |
|-----------|---------------------|--------------------------------|
| **Stars** | 19 | 0 |
| **Forks** | 3 | 0 |
| **License** | MIT | MIT |
| **Last Updated** | 2026-01-13 | 2026-01-13 |
| **Status** | Upstream | Synced fork |
| **Languages** | JavaScript (41KB), HTML (20KB) | Same |

---

## Architecture Overview

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

### Component Breakdown

| File | Size | Purpose |
|------|------|---------|
| `server.mjs` | ~400 lines | Express web server, WebSocket, pairing auth, Poke logic |
| `mcp-server.mjs` | ~250 lines | MCP server (14+ tools) for agent communication |
| `policy.json` | ~20 lines | Tool allow/deny patterns for security |
| `request-approval.mjs` | ~150 lines | Human-in-the-loop approval workflow |
| `.ag_Seeds/` | - | Mobile UI assets (HTML/CSS/JS) |
| `scripts/poke.mjs` | - | Chrome DevTools Protocol poke script |

---

## Key Features Analysis

### 1. Mobile Chat UI (`.ag_Seeds/`)

**What it does:**
- Responsive mobile-first chat interface
- Message history with timestamps
- Connection status indicator
- Pairing code authentication

**Code Pattern:**
```javascript
// server.mjs - Express + WebSocket
const wss = new WebSocketServer({ noServer: true });
app.get('/pair', handlePairing);
app.get('/chat', serveChatUI);
app.post('/poke', handlePoke);
```

**AI_Core Gap:**
- AI_Core has `src/dashboard.py` (basic Flask dashboard)
- No mobile-optimized chat UI
- No WebSocket for real-time updates

**Integration Value:** HIGH - Pattern directly applicable

---

### 2. "The Poke" Mechanism (Chrome CDP)

**What it does:**
```javascript
// scripts/poke.mjs
// Connects to Chrome DevTools Protocol at port 9000
// Sends CDP Runtime.enable() and CDP Network.emulateNetworkConditions()
// This "wakes up" the Antigravity agent
```

**AI_Core Problem:**
- AI_Core uses `python-telegram-bot`, not Chrome-based agent
- No Chrome DevTools Protocol available

**Alternative Implementation:**
```python
# For AI_Core, implement "Poke" via:
# 1. Redis pub/sub for signaling
# 2. WebSocket push to connected clients  
# 3. Telegram @mention as fallback
```

**Integration Value:** MEDIUM - Concept applicable, implementation differs

---

### 3. MCP Server Integration (`mcp-server.mjs`)

**Available MCP Tools:**

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

**Security Policy (`policy.json`):**
```json
{
    "allow": [
        "^git (status|diff|log|fetch|pull|push|checkout|switch|commit|restore)\\b",
        "^(npm|pnpm|yarn) (test|run|lint|build)\\b",
        "^pytest\\b",
        "^python -m (pytest|ruff|mypy)\\b"
    ],
    "deny": [
        "\\brm\\b", "\\bdel\\b", "\\bformat\\b",
        "\\bdiskpart\\b", "\\bshutdown\\b", "\\breboot\\b",
        "\\bchmod\\b", "\\bchown\\b"
    ]
}
```

**Integration Value:** HIGH - Directly applicable to AI_Core

---

### 4. Human-in-the-Loop Approval (`request-approval.mjs`)

**What it does:**
- Agent can request human approval for actions
- Pending approvals stored in `data/approvals.json`
- Mobile UI shows approval requests
- Agent waits for approval before proceeding

**Code Pattern:**
```javascript
// request-approval.mjs
class ApprovalFlow {
    async requestApproval(action, details) {
        const approval = {
            id: crypto.randomUUID(),
            action,
            details,
            status: 'pending',
            createdAt: Date.now()
        };
        await saveApproval(approval);
        return approval;
    }
    
    async waitForApproval(approvalId, timeoutMs = 300000) {
        // Poll for approval status changes
    }
}
```

**AI_Core Gap:**
- No approval workflow
- No cost control for expensive operations
- No family/household approval flows

**Integration Value:** MEDIUM - Security/cost control feature

---

### 5. LAN-Only Security Model

**What it does:**
- No cloud databases
- All data stays on local network
- Pairing code expires after 10 minutes
- No internet required

**Security Features:**
- `x-ag-token` header for API authentication
- Pairing code-based device registration
- Local-only server (port 8787)

**AI_Core Context:**
- Already runs locally
- Telegram auth via `ALLOWED_USERS`
- Environment-based API keys

**Integration Value:** LOW - AI_Core already has similar security model

---

## AI_Core Gap Analysis

### Current AI_Core Capabilities

| Capability | AI_Core | ag_bridge | Gap |
|------------|---------|-----------|-----|
| **Chat Interface** | ✅ Telegram | ✅ Mobile Web | Mobile-optimized UI |
| **Remote Control** | ✅ Telegram | ✅ MCP + Poke | MCP server missing |
| **Agent Status** | ✅ /health | ✅ /agent/status | More detailed in ag_bridge |
| **Task Management** | ✅ task_manager.py | ✅ tasks_list/get | Similar |
| **File Operations** | ✅ Direct | ✅ files_list/read/write | Policy-controlled in ag_bridge |
| **Human Approval** | ❌ None | ✅ request-approval.mjs | MISSING |
| **Real-time Updates** | ⚠️ Polling | ✅ WebSocket | MISSING |
| **Mobile UI** | ⚠️ Responsive | ✅ Mobile-first | MISSING |

### Top Integration Opportunities

| Rank | Feature | Value | Effort | Priority |
|------|---------|-------|--------|----------|
| 1 | **MCP Server** | HIGH | Medium | P0 |
| 2 | **Mobile UI Patterns** | HIGH | Low | P1 |
| 3 | **Approval Workflow** | MEDIUM | Medium | P1 |
| 4 | **Poke Mechanism** | MEDIUM | Low | P2 |
| 5 | **Security Policy** | MEDIUM | Low | P2 |

---

## Brittle Areas & Concerns

### Critical Concerns

#### 1. Chrome DevTools Protocol Dependency
- **Issue:** "The Poke" assumes Antigravity runs with `--remote-debugging-port=9000`
- **Impact:** Cannot directly use `scripts/poke.mjs` for AI_Core
- **Mitigation:** Reimplement "Poke" using Redis pub/sub or Telegram inline queries

#### 2. Node.js Runtime
- **Issue:** ag_bridge is Node.js, AI_Core is Python
- **Impact:** Cannot run ag_bridge as-is alongside AI_Core
- **Mitigation:** Reimplement server components in Python (FastAPI) or run as sidecar

### Moderate Concerns

#### 3. MCP Protocol Compatibility
- **Issue:** ag_bridge MCP tools designed for Antigravity's message format
- **Impact:** May need translation layer for AI_Core's chat format
- **Mitigation:** Design AI_Core-specific MCP tool schema

#### 4. State Management
- **Issue:** ag_bridge uses local JSON files (`data/state.json`, `data/approvals.json`)
- **Impact:** AI_Core uses Firestore + SQLite
- **Mitigation:** Adapt to AI_Core's existing data layer

### Low Concerns

#### 5. Pairing Code Overhead
- **Issue:** Time-limited pairing codes add complexity
- **Impact:** Not needed for Telegram-connected users
- **Mitigation:** Make optional, skip for existing Telegram users

---

## Anti-Patterns to Avoid

### 1. Running Node.js Sidecar
**ag_bridge Pattern:** Separate Node.js process for web server
**Avoid:** Additional runtime complexity, npm dependency management
**Alternative:** Reimplement in Python (FastAPI) or use existing Flask/Aiohttp

### 2. Hardcoded Chrome CDP
**ag_bridge Pattern:** Assumes Antigravity via Chrome DevTools Protocol
**Avoid:** Tight coupling to browser automation
**Alternative:** Abstract "poke" as generic signaling mechanism

### 3. JSON File State Storage
**ag_bridge Pattern:** Local JSON files for state (`data/state.json`)
**Avoid:** No versioning, no conflict resolution
**Alternative:** Use AI_Core's existing Firestore/SQLite

### 4. Hardcoded Policy Rules
**ag_bridge Pattern:** Policy in `policy.json` as regex patterns
**Avoid:** No dynamic policy updates
**Alternative:** Store policy in database with admin UI

---

## Recommended Integration Strategy

### Phase 1: MCP Server Implementation (Week 1-2)

```
Goals:
- Implement Python MCP server for AI_Core
- Reuse ag_bridge tool schema patterns
- Integrate with AgentOrchestrator

Deliverables:
- mcp_server.py (FastAPI-based MCP server)
- Tool implementations (messages, status, tasks, files)
- Policy system for tool permissions
```

**MCP Tools to Implement:**

| Tool | Description | Priority |
|------|-------------|----------|
| `messages_inbox` | Read chat messages | P0 |
| `messages_send` | Send message to agent | P0 |
| `agent_status` | Get agent status | P0 |
| `tasks_list` | List pending tasks | P1 |
| `checkpoint_post` | Post progress update | P1 |
| `files_list` | List directory contents | P2 |
| `files_read` | Read file contents | P2 |
| `poke_agent` | Wake up idle agent | P2 |

### Phase 2: Dashboard Enhancement (Week 2-3)

```
Goals:
- Enhance existing dashboard with mobile-optimized UI
- Add WebSocket for real-time updates
- Integrate MCP server status

Deliverables:
- Responsive chat UI (mobile-first)
- WebSocket endpoint for real-time messages
- MCP server status panel
```

### Phase 3: Approval Workflow (Week 3-4)

```
Goals:
- Implement human-in-the-loop approval
- Telegram notification for approval requests
- /approve and /reject commands

Deliverables:
- approval_flow.py module
- Pending approvals queue (Firestore)
- Telegram inline keyboards for approval
```

### Phase 4: "Poke" Alternative (Week 4-5)

```
Goals:
- Reimplement "Poke" for Python/telegram-bot
- WebSocket push for real-time wake-up
- Redis pub/sub for multi-instance support

Deliverables:
- poke_handler.py (signaling mechanism)
- WebSocket push to connected clients
- Redis pub/sub integration
```

---

## Code Comparison

### ag_bridge (Node.js) - MCP Server

```javascript
// mcp-server.mjs
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

const server = new Server({ name: "ag-bridge" });

const TOOLS = {
    messages_inbox: {
        schema: z.object({ to: z.enum(["agent", "user"]), ... }),
        handler: async (args) => {
            const res = await api("GET", `/messages/inbox?${q.toString()}`);
            return { content: [{ type: "text", text: JSON.stringify(res) }] };
        }
    },
    messages_send: { ... },
    checkpoint_post: { ... }
};

server.setRequestHandler(ListToolsRequestSchema, () => ({ tools: Object.keys(TOOLS) }));
server.setRequestHandler(CallToolRequestSchema, async (request) => {
    const tool = TOOLS[request.params.name];
    const result = await tool.handler(request.params.arguments);
    return { content: result.content };
});
```

### AI_Core (Python) - Current

```python
# src/chat_llm.py
async def handle_message(update, context):
    response = await council.generate(prompt)
    await update.message.reply_text(response)

# src/agent_orchestrator.py
class AgentOrchestrator:
    async def run_agent(self, config: dict):
        # YAML-defined agent execution
```

### AI_Core (Python) - Target (MCP Server)

```python
# mcp_server.py
from mcp.server.fastapi import MCPServer
from mcp.server.stdio import stdio_server
import mcp.types as types

app = MCPServer("ai-core-bridge")

@app.tool()
async def messages_inbox(to: str, status: str = "new") -> dict:
    """Read messages from inbox"""
    messages = await get_messages(to=to, status=status)
    return {"messages": [msg.to_dict() for msg in messages]}

@app.tool()
async def messages_send(to: str, text: str, channel: str = "work") -> dict:
    """Send message to agent or user"""
    message = await send_message(to=to, text=text, channel=channel)
    return {"message_id": message.id}

@app.tool()
async def checkpoint_post(n: int = None, N: int = None, note: str = None) -> dict:
    """Post progress checkpoint"""
    checkpoint = await post_checkpoint(n=n, N=N, note=note)
    return {"checkpoint_id": checkpoint.id}

@app.tool()
async def agent_status() -> dict:
    """Get current agent status"""
    return {
        "state": current_state,
        "task": current_task,
        "last_activity": last_activity
    }
```

---

## Files Generated

| File | Location | Purpose |
|------|----------|---------|
| `ag_bridge_integration_analysis.md` | `Agent_Context/Knowledge_Base/Analysis/` | This document |

---

## Comparison: ag_bridge vs Agor vs AI_Core

| Dimension | ag_bridge (Mario4272) | Agor (Preset) | AI_Core (Current) |
|-----------|----------------------|---------------|-------------------|
| **Architecture** | Node.js + CDP | FeathersJS + executors | Python + Telegram |
| **Complexity** | Low | High | Medium |
| **Maturity** | Established (19 stars) | Early 2025 | Established |
| **License** | MIT | BSL 1.1 | Custom |
| **Mobile UI** | Native | React Canvas | Telegram |
| **Multi-Agent** | No | Native | Limited (YAML) |
| **Isolation** | None | Worktree + Unix | Process |
| **MCP** | 14+ tools | 14+ tools | None |

**Integration Recommendation:**

| Source | Use For | Skip |
|--------|---------|------|
| **ag_bridge** | MCP server, mobile UI, approval flow | Node.js sidecar, Chrome CDP |
| **Agor** | Multi-agent patterns, session management | Full stack (FeathersJS, canvas) |
| **AI_Core** | Keep Telegram-first, existing modules | N/A |

---

## Beads Tracking

| ID | Status | Description |
|----|--------|-------------|
| US-aca | completed | Agor integration analysis |
| US-abb | pending | ag_bridge MCP implementation |
| US-abc | pending | ag_bridge dashboard enhancement |
| US-abd | pending | ag_bridge approval workflow |

---

## Fork Management Notes

### Working on KostaGorod/ag_bridge

Our fork is located at: `https://github.com/KostaGorod/ag_bridge`

**Current Status:**
- Synced with upstream (Mario4272/ag_bridge)
- 0 commits ahead, 0 commits behind
- No local modifications

**Workflow for Contributions:**
1. Create branch from `main` in our fork
2. Make changes
3. Test locally
4. Submit PR to upstream (Mario4272/ag_bridge)
5. Sync changes back to our fork

**Sync Command:**
```bash
# Sync our fork with upstream
gh repo sync KostaGorod/ag_bridge --base-owner Mario4272 --force
```

---

## Conclusion

**ag_bridge provides immediately applicable patterns for AI_Core:**

✅ **Adopt (High Priority):**
- MCP server implementation (14+ tools)
- Mobile UI patterns (responsive design)
- Policy-based tool permissions
- Human-in-the-loop approval workflow

✅ **Adopt (Medium Priority):**
- "Poke" concept (reimplemented for Python)
- LAN-only security model
- WebSocket for real-time updates

❌ **Skip:**
- Node.js sidecar (keep Python-only)
- Chrome CDP dependency (use Redis/webhooks)
- Pairing code auth (Telegram auth already exists)

**Recommended Priority:**
1. **MCP Server** - Highest value, enables Claude Code integration
2. **Dashboard Enhancement** - Improves existing web component
3. **Approval Flow** - Security/cost control
4. **Poke Mechanism** - Nice to have, lower priority

---

## Next Actions

1. **Review this analysis** - Confirm priorities
2. **Create beads** for Phase 1 (MCP Server)
3. **Prototype MCP tools** (messages_inbox, messages_send)
4. **Test with existing AI_Core infrastructure**
5. **Contribute improvements** back to upstream (Mario4272/ag_bridge)
