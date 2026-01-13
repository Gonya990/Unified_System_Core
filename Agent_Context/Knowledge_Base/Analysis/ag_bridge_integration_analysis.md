# ag_bridge Integration Analysis

**Generated:** 2026-01-13  
**Author:** Sisyphus  
**Context:** Comparative analysis of `KostaGorod/ag_bridge` for AI_Core integration

---

## Overview

**ag_bridge** is a **mobile interface for Antigravity Agent** that enables remote control via phone. It was forked from `Mario4272/ag_bridge` and modified by KostaGorod.

**Key Distinction:** This is NOT related to the "rproj" you mentioned (Antigravity RProj project). It's a mobile bridge for the Antigravity Agent (a Claude Code alternative).

---

## ag_bridge Architecture

```
┌──────────┐     ┌──────────────┐     ┌─────────────────┐
│  Phone   │────>│ Bridge Server│────>│ Antigravity     │
│ (Mobile) │     │ (Node.js)    │     │ (Chrome CDP)    │
└──────────┘     └──────────────┘     └─────────────────┘
                      │
                      ├── MCP Server (mcp-server.mjs)
                      ├── Pairing Code Auth
                      └── LAN Only (no cloud)
```

### Components

| File | Purpose |
|------|---------|
| `server.mjs` | Express web server, serves mobile UI, handles pairing |
| `mcp-server.mjs` | MCP tools for agent communication |
| `policy.json` | MCP tool policies/permissions |
| `request-approval.mjs` | Human-in-the-loop approval flow |
| `.ag_Seeds/` | Mobile UI assets |
| `data/` | Runtime data storage |

### Key Features

1. **Mobile Chat UI** - Full chat interface with history
2. **The Poke** - Remotely wakes up the agent (no manual typing)
3. **LAN Only** - Data stays on local network, no cloud databases
4. **MCP Integration** - Agent can read messages and report status

---

## AI_Core Gap Analysis

### What AI_Core Has (Overlap)

| Feature | AI_Core | ag_bridge |
|---------|---------|-----------|
| Chat Interface | ✅ Telegram | ✅ Mobile Web |
| Agent Control | ✅ Commands | ✅ MCP + Poke |
| Network Security | ✅ Local | ✅ LAN Only |
| MCP Tools | ❌ None | ✅ 14+ tools |

### What AI_Core Lacks (Value Add)

| Gap | ag_bridge Solution | Integration Value |
|-----|-------------------|-------------------|
| No mobile web UI | Mobile-first design | **HIGH** |
| No remote wake-up | "The Poke" mechanism | **MEDIUM** |
| No MCP server | Full MCP implementation | **HIGH** |
| No human approval | request-approval.mjs | **MEDIUM** |
| Phone-only access | Pairing code + LAN | **LOW** (Telegram already mobile) |

---

## Top 5 Integration Opportunities

### 1. MCP Server Integration (HIGH VALUE)

**ag_bridge provides:**
- Complete MCP server implementation (`mcp-server.mjs`)
- Policy-based tool permissions (`policy.json`)
- Agent-to-agent communication

**AI_Core Benefit:**
- Programmatic access to AI_Core capabilities
- Enables Claude Code / Cursor integration
- Foundation for multi-agent workflows

**Implementation:**
```python
# Convert mcp-server.mjs patterns to Python
# Reuse policy.json structure for tool permissions
# Integrate with existing AgentOrchestrator
```

### 2. Mobile Web Interface (HIGH VALUE)

**ag_bridge provides:**
- Responsive mobile UI (`.ag_Seeds/`)
- Chat history management
- Pairing code authentication

**AI_Core Benefit:**
- Alternative to Telegram dependency
- Dashboard enhancement (already has web component)
- Offline-capable mobile access

**Implementation:**
```python
# Extract UI patterns from ag_bridge
# Integrate with existing src/dashboard.py
# Add pairing code auth to web endpoints
```

### 3. "The Poke" Mechanism (MEDIUM VALUE)

**ag_bridge provides:**
- Chrome DevTools Protocol integration
- Remote agent wake-up via `--remote-debugging-port=9000`

**AI_Core Benefit:**
- Wake idle bot for urgent messages
- Alternative to polling-based checks

**Challenge:** AI_Core uses `python-telegram-bot`, not Chrome CDP

**Alternative Implementation:**
```python
# Poke mechanism for AI_Core:
# - Redis pub/sub for inter-process signaling
# - WebSocket push to connected clients
# - Telegram @mention triggers
```

### 4. Human-in-the-Loop Approval (MEDIUM VALUE)

**ag_bridge provides:**
- `request-approval.mjs` workflow
- Blocked actions requiring human confirmation

**AI_Core Benefit:**
- Security for sensitive commands
- Cost control for expensive operations
- Family/household approval flows

**Implementation:**
```python
# approval_flow.py module
# - Pending approval queue
# - Telegram notification for approval
# - Approval via /approve command
```

### 5. Pairing Code Authentication (LOW VALUE)

**ag_bridge provides:**
- Time-limited pairing codes
- LAN-only device registration

**AI_Core Benefit:**
- Additional auth layer for web dashboard
- Device management

**Assessment:** Telegram already handles auth via `ALLOWED_USERS`. Lower priority.

---

## Brittle Areas & Concerns

### Critical Concerns

#### 1. Chrome DevTools Protocol Dependency
- **Issue:** ag_bridge assumes Antigravity runs with `--remote-debugging-port=9000`
- **Problem:** AI_Core is Python, not a Chrome-based agent
- **Mitigation:** Reimplement "Poke" using Redis/webhooks instead of CDP

#### 2. Node.js Dependency
- **Issue:** ag_bridge is a Node.js application
- **Problem:** AI_Core is Python (uv/poetry)
- **Mitigation:** Reimplement server as Python (FastAPI) or run as sidecar

### Moderate Concerns

#### 3. MCP Protocol Compatibility
- **Issue:** ag_bridge uses specific MCP tool schema
- **Problem:** May not match AI_Core's capability model
- **Mitigation:** Design translation layer or new MCP implementation

#### 4. UI Framework Differences
- **Issue:** ag_bridge mobile UI vs AI_Core dashboard
- **Problem:** Different design patterns
- **Mitigation:** Extract patterns, not copy code

### Low Concerns

#### 5. Pairing Code Overhead
- **Issue:** Time-limited codes add complexity
- **Problem:** Not needed for Telegram-connected users
- **Mitigation:** Make optional, skip for existing users

---

## Anti-Patterns to Avoid

### 1. Running Node.js Sidecar
**ag_bridge Pattern:** Separate Node.js process for web server
**Avoid:** Additional runtime complexity
**Alternative:** Reimplement in Python (FastAPI) or use existing Flask/Aiohttp

### 2. Hardcoded Chrome CDP
**ag_bridge Pattern:** Assumes Antigravity via Chrome DevTools
**Avoid:** Tight coupling to browser automation
**Alternative:** Abstract "poke" as a generic signaling mechanism

### 3. Custom Auth Protocol
**ag_bridge Pattern:** Pairing code authentication
**Avoid:** When Telegram auth already exists
**Alternative:** Extend Telegram auth to web endpoints

---

## Recommended Integration Strategy

### Phase 1: Extract MCP Patterns (Week 1)

```
1. Analyze mcp-server.mjs implementation
2. Design Python MCP server architecture
3. Implement core MCP tools:
   - send_message
   - get_status
   - list_capabilities
4. Define policy.json equivalent
```

**Deliverable:** Python MCP server for AI_Core

### Phase 2: Enhance Dashboard (Week 2)

```
1. Study ag_bridge mobile UI patterns
2. Extract responsive chat interface
3. Add to existing src/dashboard.py
4. Integrate with AI_Core's chat system
```

**Deliverable:** Mobile-friendly dashboard enhancement

### Phase 3: Implement Approval Flow (Week 3)

```
1. Design approval request schema
2. Create approval queue storage
3. Implement Telegram notification
4. Add /approve /reject commands
```

**Deliverable:** Human-in-the-loop approval system

### Phase 4: "Poke" Alternative (Week 4)

```
1. Design signaling mechanism (Redis pub/sub)
2. Implement WebSocket push
3. Add "wake up" endpoints
4. Document usage patterns
```

**Deliverable:** Wake-up mechanism for idle bot

---

## Code Comparison

### ag_bridge (Node.js)

```javascript
// server.mjs - Express server
app.get('/pair', handlePairing);
app.get('/chat', serveChatUI);
app.post('/poke', handlePoke);

// mcp-server.mjs - MCP implementation
class MCPServer {
  async handleRequest(toolName, params) {
    // Route to appropriate handler
  }
}
```

### AI_Core (Python) - Current

```python
# src/main.py - Entry point
application = ApplicationBuilder().token(TOKEN).build()

# src/chat_llm.py - Chat handling
async def handle_message(update, context):
    response = await council.generate(prompt)
```

### AI_Core (Python) - Target

```python
# mcp_server.py - MCP implementation (NEW)
from mcp.server.fastapi import MCPServer

mcp = MCPServer()

@mcp.tool()
def send_message(chat_id: str, text: str) -> dict:
    """Send message via AI_Core"""
    # Implementation

@mcp.tool()
def get_status() -> dict:
    """Get agent status"""
    # Implementation
```

---

## Files Generated

| File | Location | Purpose |
|------|----------|---------|
| `ag_bridge_integration_analysis.md` | `Agent_Context/Knowledge_Base/Analysis/` | This document |

---

## Comparison Matrix: ag_bridge vs Agor

| Dimension | ag_bridge | Agor | AI_Core |
|-----------|-----------|------|---------|
| **Architecture** | Node.js + CDP | FeathersJS + executors | Python + Telegram |
| **Complexity** | Low | High | Medium |
| **Maturity** | Early (12 commits) | Early 2025 | Established |
| **Mobile UI** | Native | React Canvas | Telegram |
| **Isolation** | None | Worktree + Unix | Process |
| **License** | MIT | BSL 1.1 | Custom |

**Recommendation:** ag_bridge patterns are more immediately applicable to AI_Core due to:
1. Lower complexity
2. MIT license
3. Similar scope (single-agent enhancement)
4. Python reimplementable

---

## Conclusion

**ag_bridge provides valuable patterns for AI_Core:**

✅ **Adopt:** MCP server implementation, mobile UI patterns, approval workflow
✅ **Adopt:** "Poke" concept (reimplemented for Python), LAN-only security
❌ **Skip:** Node.js sidecar, Chrome CDP dependency, pairing code auth

**Priority Order:**
1. **MCP Server** - Highest value, enables multi-agent future
2. **Dashboard Enhancement** - Improves existing web component
3. **Approval Flow** - Security/cost control
4. **Poke Mechanism** - Nice to have, lower priority

---

## Beads Tracking

| ID | Status | Description |
|----|--------|-------------|
| US-aca | completed | Agor integration analysis |
| US-abb | pending | ag_bridge MCP implementation |
| US-abc | pending | ag_bridge dashboard enhancement |

---

## Next Actions

1. Review this analysis
2. Prioritize integration phases
3. Create detailed specs for MCP server
4. Prototype MCP tools
5. Test with existing AI_Core infrastructure
