# AI_Core MCP Bridge: Draft Technical Specification

**Version:** 1.0-draft  
**Date:** 2026-01-13  
**Author:** Sisyphus  
**Status:** Draft - Pending Igor Review  
**Related:** AI_Core_ag_bridge_vs_Agor_Comparison.md

---

## 1. Overview

### 1.1 Purpose

This specification defines the **AI_Core MCP Bridge** - a Python-based MCP (Model Context Protocol) server that exposes AI_Core capabilities as tools, enabling integration with Claude Code, Cursor, and other MCP-compatible clients.

### 1.2 Scope

| In Scope | Out of Scope |
|----------|--------------|
| MCP server implementation | Frontend UI (handled separately) |
| Tool definitions and policies | Multi-agent orchestration (future) |
| Transport (SSE + HTTP) | Worktree isolation |
| Authentication | Agor-style executor isolation |
| Dashboard integration | React canvas UI |

### 1.3 References

| Reference | Description |
|-----------|-------------|
| `ag_bridge_mario4272_integration.md` | Source patterns from Mario4272/ag_bridge |
| `AI_Core_ag_bridge_vs_Agor_Comparison.md` | Full comparative analysis |
| `Agent_Context/Knowledge_Base/mcp-server/` | Existing Node/TS MCP server |
| `HOW_TO_GIVE_ANOTHER_AGENT_ACCESS_TO_MCP_AGENT_MAIL.md` | Existing MCP Agent Mail docs |

---

## 2. Architecture

### 2.1 System Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                        AI_Core MCP Bridge                           │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                      FastAPI Server                         │   │
│  │  ┌───────────┐  ┌───────────┐  ┌─────────────────────────┐  │   │
│  │  │   /sse    │  │ /message  │  │  /tools/call (REST)     │  │   │
│  │  │ (Stream)  │  │  (POST)   │  │  (JSON-RPC fallback)    │  │   │
│  │  └───────────┘  └───────────┘  └─────────────────────────┘  │   │
│  │  ┌───────────────────────────────────────────────────────┐  │   │
│  │  │              MCP Protocol Handler                     │  │   │
│  │  │  ┌─────────────┐  ┌─────────────┐  ┌───────────────┐ │  │   │
│  │  │  │ ListTools   │  │ CallTool    │  │ ListResources │ │  │   │
│  │  │  │  Handler    │  │  Handler    │  │   Handler     │ │  │   │
│  │  │  └─────────────┘  └─────────────┘  └───────────────┘ │  │   │
│  │  └───────────────────────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                      │
│              ┌───────────────┼───────────────┐                     │
│              ▼               ▼               ▼                     │
│      ┌─────────────┐ ┌─────────────┐ ┌─────────────┐              │
│      │   Policy    │ │   Tool      │ │  Agent      │              │
│      │   Engine    │ │  Registry   │ │  Orchestrator│             │
│      └─────────────┘ └─────────────┘ └─────────────┘              │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
              ┌───────────────────────────────────┐
              │         AI_Core Modules           │
              │  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ │
              │  │Chat │ │Task │ │File │ │Health│ │
              │  └─────┘ └─────┘ └─────┘ └─────┘ │
              └───────────────────────────────────┘
```

### 2.2 Components

| Component | Description | Location |
|-----------|-------------|----------|
| **FastAPI Server** | HTTP/SSE server for MCP transport | `src/mcp_server/server.py` |
| **MCP Protocol Handler** | MCP request/response handling | `src/mcp_server/protocol.py` |
| **Tool Registry** | Tool definitions and schemas | `src/mcp_server/tools/*.py` |
| **Policy Engine** | Allow/deny rule evaluation | `src/mcp_server/policy.py` |
| **Auth Middleware** | API key and session validation | `src/mcp_server/auth.py` |

---

## 3. Transport Layer

### 3.1 Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/sse` | GET | Server-Sent Events stream for MCP messages |
| `/message` | POST | Receive MCP messages (POST to SSE stream) |
| `/tools/call` | POST | JSON-RPC fallback (no SSE) |
| `/health` | GET | Health check |
| `/n8n` | POST | Non-MCP friendly endpoint (tools/call) |

### 3.2 Transport Options

```python
# Option 1: SSE Transport (Primary)
# Client connects to /sse, receives messages as SSE events
# Client sends messages to /message (POST)

# Option 2: JSON-RPC Fallback (Simpler)
# Client sends to /tools/call (POST)
# Response returned immediately (no streaming)
```

### 3.3 Authentication

```python
# Header-based API key authentication
headers = {
    "x-mcp-api-key": os.getenv("MCP_API_KEY")
}

# Optional: Session-based auth
headers = {
    "Authorization": "Bearer <session_token>"
}
```

---

## 4. Tool Definitions

### 4.1 Core Tools

#### 4.1.1 Message Tools

| Tool Name | Description | Parameters |
|-----------|-------------|------------|
| `messages_inbox` | Read messages from inbox | `to: "agent" \| "user"`, `status: str` |
| `messages_send` | Send message to agent/user | `to: str`, `text: str`, `channel: str` |
| `messages_ack` | Acknowledge message | `message_id: str`, `action: "read" \| "done"` |

#### 4.1.2 Agent Status Tools

| Tool Name | Description | Parameters |
|-----------|-------------|------------|
| `agent_status` | Get current agent status | None |
| `agent_heartbeat` | Report agent state | `state: "idle" \| "working"` |
| `checkpoint_post` | Post progress checkpoint | `n: int`, `N: int`, `note: str` |

#### 4.1.3 Task Tools

| Tool Name | Description | Parameters |
|-----------|-------------|------------|
| `tasks_list` | List pending tasks | `status: str` |
| `tasks_get` | Get task details | `task_id: str` |

#### 4.1.4 File Tools

| Tool Name | Description | Parameters |
|-----------|-------------|------------|
| `files_list` | List files in directory | `path: str` |
| `files_read` | Read file contents | `path: str` |
| `files_write` | Write/create file | `path: str`, `content: str` |

### 4.2 Tool Schema Example

```python
from pydantic import BaseModel, Field
from typing import Literal

class MessagesInboxParams(BaseModel):
    to: Literal["agent", "user"] = Field(
        description="Message recipient type"
    )
    status: str = Field(
        default="new",
        description="Filter by message status"
    )

class MessagesInboxTool:
    name = "messages_inbox"
    description = "Read messages from the inbox"
    parameters = MessagesInboxParams
    
    async def handler(args: MessagesInboxParams) -> dict:
        messages = await get_messages(to=args.to, status=args.status)
        return {
            "content": [{
                "type": "text",
                "text": json.dumps([m.to_dict() for m in messages])
            }]
        }
```

---

## 5. Policy Engine

### 5.1 Policy Structure

```python
# src/mcp_server/policy.py

class PolicyEngine:
    def __init__(self, policy_file: str = "mcp_policy.json"):
        self.policy = self._load_policy(policy_file)
    
    def _load_policy(self, path: str) -> dict:
        with open(path) as f:
            return json.load(f)
    
    async def check(self, tool_name: str, args: dict) -> tuple[bool, str]:
        """Check if tool call is allowed"""
        # Check deny patterns first
        for pattern in self.policy.get("deny", []):
            if re.search(pattern, tool_name):
                return False, f"Tool '{tool_name}' is denied"
        
        # Check allow patterns
        for pattern in self.policy.get("allow", []):
            if re.search(pattern, tool_name):
                return True, "Allowed"
        
        # Default: deny if not matched
        return False, f"Tool '{tool_name}' not in allow list"
```

### 5.2 Policy File Format

```json
{
    "version": "1.0",
    "allow": [
        "^messages_",
        "^agent_",
        "^tasks_",
        "^checkpoint_",
        "^git (status|diff|log|fetch|pull|push|checkout|switch|commit|restore)\\b",
        "^(npm|pnpm|yarn) (test|run|lint|build)\\b",
        "^python -m (pytest|ruff|mypy)\\b",
        "^ls\\b",
        "^dir\\b",
        "^cat\\b",
        "^head\\b",
        "^tail\\b"
    ],
    "deny": [
        "\\brm\\b",
        "\\bdel\\b",
        "\\bformat\\b",
        "\\bdiskpart\\b",
        "\\bshutdown\\b",
        "\\breboot\\b",
        "\\bchmod\\b",
        "\\bchown\\b",
        "\\bsudo\\b",
        "^files_write"
    ]
}
```

---

## 6. Integration Points

### 6.1 AI_Core Modules

| Module | Integration | Tool |
|--------|-------------|------|
| `chat_llm.py` | Send/receive messages | `messages_send`, `messages_inbox` |
| `task_manager.py` | Task list/get | `tasks_list`, `tasks_get` |
| `health.py` | Agent status | `agent_status`, `agent_heartbeat` |
| `conversation_manager.py` | Checkpoints | `checkpoint_post` |

### 6.2 Existing Dashboard

The MCP Bridge will integrate with existing `src/dashboard.py`:

```python
# dashboard.py already has:
# - FastAPI server on port 8000
# - WebSocket support
# - Session verification

# MCP Bridge can:
# - Run as separate server on port 8765 (like existing MCP Agent Mail)
# - Share session verification logic
# - Expose dashboard status via tools
```

### 6.3 Existing MCP Agent Mail

```python
# Existing AgentMail MCP runs on http://localhost:8765
# New MCP Bridge should:
# - Use different port (e.g., 8766) OR
# - Merge into single server with namespaced tools
```

---

## 7. Implementation Plan

### 7.1 Phase 1: Core Server (Week 1)

| Task | Description | Status |
|------|-------------|--------|
| 1.1 | Create `src/mcp_server/` directory structure | ⏳ |
| 1.2 | Implement FastAPI server with SSE transport | ⏳ |
| 1.3 | Implement MCP protocol handler | ⏳ |
| 1.4 | Add authentication middleware | ⏳ |
| 1.5 | Create tool registry base class | ⏳ |

### 7.2 Phase 2: Core Tools (Week 1-2)

| Task | Description | Status |
|------|-------------|--------|
| 2.1 | Implement message tools | ⏳ |
| 2.2 | Implement agent status tools | ⏳ |
| 2.3 | Implement task tools | ⏳ |
| 2.4 | Add policy engine | ⏳ |
| 2.5 | Write unit tests | ⏳ |

### 7.3 Phase 3: Integration (Week 2)

| Task | Description | Status |
|------|-------------|--------|
| 3.1 | Integrate with AI_Core modules | ⏳ |
| 3.2 | Add to existing dashboard.py | ⏳ |
| 3.3 | Create policy file | ⏳ |
| 3.4 | Integration testing | ⏳ |

### 7.4 Phase 4: Client Configuration (Week 2)

| Task | Description | Status |
|------|-------------|--------|
| 4.1 | Document Claude Code configuration | ⏳ |
| 4.2 | Document Cursor configuration | ⏳ |
| 4.3 | Create `.mcp_config/` directory | ⏳ |

---

## 8. Security Considerations

### 8.1 Authentication

- API key required via `x-mcp-api-key` header
- Session token validation for dashboard integration
- Rate limiting (TODO)

### 8.2 Tool Policies

- Default deny policy
- Explicit allow patterns
- Dangerous tools (rm, format, etc.) always denied

### 8.3 Network

- LAN-only by default
- Configurable bind address
- HTTPS in production (TODO)

---

## 9. Testing Strategy

### 9.1 Unit Tests

```python
# tests/test_mcp_server.py

import pytest
from mcp_server import MCPServer

@pytest.fixture
def server():
    return MCPServer()

@pytest.mark.asyncio
async def test_list_tools(server):
    tools = await server.list_tools()
    assert len(tools) > 0
    assert "messages_inbox" in [t.name for t in tools]

@pytest.mark.asyncio
async def test_call_tool_auth_failure(server):
    with pytest.raises(AuthenticationError):
        await server.call_tool("messages_inbox", {}, api_key="invalid")
```

### 9.2 Integration Tests

```bash
# Test MCP connection
curl -N http://localhost:8766/sse \
  -H "x-mcp-api-key: $MCP_API_KEY" &

# Test tool call
curl -X POST http://localhost:8766/tools/call \
  -H "x-mcp-api-key: $MCP_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"tool": "agent_status", "args": {}}'
```

---

## 10. Configuration

### 10.1 Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `MCP_API_KEY` | Yes | - | API key for authentication |
| `MCP_HOST` | No | `0.0.0.0` | Bind address |
| `MCP_PORT` | No | `8766` | Server port |
| `AI_CORE_PATH` | Yes | - | Path to AI_Core project |
| `POLICY_FILE` | No | `mcp_policy.json` | Policy file path |

### 10.2 Example .env

```bash
# .env.mcp
MCP_API_KEY=your-secret-api-key-here
MCP_HOST=0.0.0.0
MCP_PORT=8766
AI_CORE_PATH=/mnt/src/Unified_System_Core/Projects/AI_Core
POLICY_FILE=/mnt/src/Unified_System_Core/Projects/AI_Core/config/mcp_policy.json
```

---

## 11. Open Questions (For Igor Review)

1. **Port Selection:** Use 8766 (next to existing MCP Agent Mail on 8765) or merge into single server?
2. **Tool Scope:** Start with 12 tools (ag_bridge pattern) or add more AI_Core-specific tools?
3. **Policy Defaults:** Should we start permissive (easy testing) or restrictive (secure by default)?
4. **Integration:** Should MCP Bridge run as part of `ai_telegram_bot_v2.py` or separate process?
5. **Dashboard:** Integrate MCP status into existing dashboard.py or create separate page?

---

## 12. Appendix: File Structure

```
Projects/AI_Core/
├── src/
│   └── mcp_server/
│       ├── __init__.py
│       ├── server.py          # FastAPI + SSE
│       ├── protocol.py        # MCP handlers
│       ├── auth.py            # API key auth
│       ├── policy.py          # Policy engine
│       ├── tools/
│       │   ├── __init__.py
│       │   ├── base.py        # Tool base class
│       │   ├── messages.py    # Message tools
│       │   ├── agent.py       # Status tools
│       │   ├── tasks.py       # Task tools
│       │   └── files.py       # File tools
│       └── main.py            # Entry point
├── config/
│   └── mcp_policy.json        # Policy rules
├── tests/
│   └── test_mcp_server.py     # Unit tests
├── .env.mcp                   # Environment config
└── pyproject.toml             # Dependencies
```

---

**Next Steps:**
1. Igor to review and provide feedback
2. Finalize spec based on feedback
3. Begin Phase 1 implementation
