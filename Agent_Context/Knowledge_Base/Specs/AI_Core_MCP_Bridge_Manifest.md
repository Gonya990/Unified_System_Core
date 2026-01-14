# AI_Core MCP Bridge: Implementation Manifest

**Version:** 1.0  
**Date:** 2026-01-13  
**Author:** Sisyphus  
**Status:** Draft  
**Related Spec:** `Specs/AI_Core_MCP_Bridge_Spec.md`

---

## Manifest Overview

| Field | Value |
|-------|-------|
| **Project** | AI_Core MCP Bridge |
| **Purpose** | Python MCP server for AI_Core capabilities |
| **Source Patterns** | Mario4272/ag_bridge (MIT license) |
| **Dependencies** | FastAPI, python-multipart, pydantic |
| **Output Port** | 8766 (default) |
| **Auth** | API key (`x-mcp-api-key`) |

---

## Goals

### Primary Goals

1. **Enable MCP clients** (Claude Code, Cursor) to call AI_Core tools
2. **Expose AI_Core capabilities** as MCP tools with policy control
3. **Integrate with existing** AI_Core infrastructure

### Secondary Goals

1. **Reuse patterns** from ag_bridge (MIT-licensed)
2. **Leverage existing** AgentMail MCP server as reference
3. **Minimize new dependencies** (use existing FastAPI stack)

---

## Non-Goals

1. ❌ Replace existing AgentMail MCP server
2. ❌ Implement multi-agent orchestration
3. ❌ Add worktree isolation
4. ❌ Create new frontend UI (reuse existing dashboard)

---

## Success Criteria

### Functional

| Criterion | Metric | Target |
|-----------|--------|--------|
| MCP tools callable | Tools available via MCP protocol | 12+ tools |
| Message operations | Send/receive messages via MCP | All 3 tools work |
| Agent status | Get/set status via MCP | 2 tools work |
| Task operations | List/get tasks via MCP | 2 tools work |
| Policy enforcement | Denied tools rejected | 100% blocked |

### Observable

| Criterion | Evidence |
|-----------|----------|
| SSE stream connects | `curl -N http://localhost:8766/sse` returns events |
| Tool call succeeds | `curl -X POST /tools/call` returns valid JSON |
| Policy enforced | Denied tool returns error |

### Pass/Fail

| Test | Expected |
|------|----------|
| `agent_status` tool | Returns `{state, task, last_activity}` |
| `messages_inbox` tool | Returns message list |
| `files_write` tool | Blocked by policy (if denied) |

---

## Scope

### In Scope

| Component | Description |
|-----------|-------------|
| FastAPI server | SSE + HTTP transport |
| MCP protocol | ListTools, CallTool, ListResources |
| 12 core tools | Messages, Status, Tasks, Files |
| Policy engine | Allow/deny pattern matching |
| Authentication | API key header validation |
| Integration | Connect to AI_Core modules |

### Out of Scope

| Component | Reason |
|-----------|--------|
| Frontend UI | Handled by existing dashboard.py |
| Worktree isolation | Too complex, future work |
| Multi-agent | Agor patterns, later phase |
| HTTPS | Development first, add later |
| Rate limiting | Add after MVP |

---

## Deliverables

### Code

| File | Description |
|------|-------------|
| `src/mcp_server/__init__.py` | Package init |
| `src/mcp_server/server.py` | FastAPI server with SSE |
| `src/mcp_server/protocol.py` | MCP request handlers |
| `src/mcp_server/auth.py` | API key authentication |
| `src/mcp_server/policy.py` | Policy engine |
| `src/mcp_server/tools/__init__.py` | Tools package |
| `src/mcp_server/tools/base.py` | Tool base class |
| `src/mcp_server/tools/messages.py` | Message tools |
| `src/mcp_server/tools/agent.py` | Agent status tools |
| `src/mcp_server/tools/tasks.py` | Task tools |
| `src/mcp_server/tools/files.py` | File tools |
| `src/mcp_server/main.py` | Entry point |

### Configuration

| File | Description |
|------|-------------|
| `config/mcp_policy.json` | Policy allow/deny rules |
| `.env.mcp` | Environment variables template |

### Documentation

| File | Description |
|------|-------------|
| `Specs/AI_Core_MCP_Bridge_Spec.md` | Technical specification |
| `Docs/MCP_BRIDGE_README.md` | Usage documentation |
| `.mcp_config/claude_code.json` | Claude Code configuration |
| `.mcp_config/cursor.json` | Cursor configuration |

### Tests

| File | Description |
|------|-------------|
| `tests/test_mcp_server.py` | Unit tests |
| `tests/test_tools.py` | Tool integration tests |
| `tests/test_policy.py` | Policy tests |

---

## Dependencies

### Python Dependencies

```toml
# pyproject.toml additions

[project.dependencies]
fastapi = ">=0.109.0"
uvicorn = ">=0.27.0"
python-multipart = ">=0.0.6"
pydantic = ">=2.5.0"
httpx = ">=0.26.0"
sse-starlette = ">=2.0.0"
```

### System Dependencies

| Dependency | Version | Reason |
|------------|---------|--------|
| Python | 3.11+ | async/await, pydantic v2 |

---

## Risks

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Tool integration fails | High | Medium | Mock tools initially, iterate |
| Policy too restrictive | Medium | High | Start permissive, narrow later |
| Port conflict | Low | Low | Use 8766 (next to 8765) |
| Performance issues | Medium | Low | Profile after implementation |

---

## Timeline

### Week 1: Core Infrastructure

| Day | Task | Output |
|-----|------|--------|
| 1-2 | Create directory structure, dependencies | Code scaffold |
| 3-4 | Implement FastAPI + SSE transport | Server runs |
| 5 | Implement MCP protocol handlers | Protocol works |

### Week 2: Tools + Integration

| Day | Task | Output |
|-----|------|--------|
| 1-2 | Implement 12 core tools | Tools callable |
| 3 | Add policy engine | Policy enforced |
| 4 | Integrate with AI_Core modules | Real data |
| 5 | Write unit tests | Tests pass |

### Week 3: Testing + Documentation

| Day | Task | Output |
|-----|------|--------|
| 1-2 | Integration testing | All tests pass |
| 3-4 | Documentation | README, configs |
| 5 | Final review, merge | Code merged |

---

## Resources

### Reference Implementations

| Source | URL | Purpose |
|--------|-----|---------|
| ag_bridge (Mario4272) | https://github.com/Mario4272/ag_bridge | MCP patterns |
| Existing MCP Agent Mail | `Agent_Context/Knowledge_Base/mcp-server/` | Server pattern |
| MCP SDK Python | https://github.com/anthropics/mcp-python | Protocol reference |

### Key Files to Reference

| File | Description |
|------|-------------|
| `Projects/AI_Core/src/dashboard.py` | FastAPI + WebSocket pattern |
| `Scripts/Orchestration/agent_mail_client.py` | Agent Mail CLI wrapper over Python SDK |
| `Scripts/Orchestration/agent_sync.py` | Unified sync flow: inbox + beads |
| `infra/mcp-agent-mail-config.md` | Agent Mail MCP client configuration (no secrets) |
| `Agent_Context/Knowledge_Base/mcp-server/src/index.ts` | Node MCP server |

### Agent Mail + Agent Sync (Operational Workflow)

- Agent Mail is the reference “MCP server in production” pattern for this bridge.
- Agent Sync (`Scripts/Orchestration/agent_sync.py`) is the recommended operator workflow to:
  - register/heartbeat,
  - fetch inbox,
  - run `bd sync` + show ready queue.
- Secrets policy: config docs must use placeholders like `<AGENT_MAIL_TOKEN>` and rely on `.env` for real values.

---

## Acceptance Criteria

### Must Have (MVP)

- [ ] Server starts without errors
- [ ] SSE endpoint responds to connections
- [ ] At least 8 tools are callable
- [ ] Authentication rejects invalid API keys
- [ ] Policy blocks at least one tool
- [ ] Integration tests pass

### Should Have

- [ ] All 12 tools implemented
- [ ] Claude Code configuration provided
- [ ] Cursor configuration provided
- [ ] Documentation complete
- [ ] Performance acceptable (< 1s per tool call)

### Could Have

- [ ] Rate limiting
- [ ] HTTPS support
- [ ] Metrics endpoint
- [ ] WebSocket alternative to SSE

---

## Success Metrics

| Metric | Baseline | Target | How to Measure |
|--------|----------|--------|----------------|
| Tool count | 0 | 12+ | `list_tools` response |
| Response time | N/A | < 1s | Tool call latency |
| Test coverage | 0% | 80% | pytest --cov |
| Documentation | 0% | 100% | Files created |

---

## Communication

### Status Updates

- **Daily:** Short sync in agent mail
- **Weekly:** Progress report in #dev
- **Blockers:** Immediate notification

### Review Points

| Phase | Review | Approver |
|-------|--------|----------|
| Spec Final | Before implementation | Igor |
| Code Review | After each phase | Peer |
| Final Sign-off | Before merge | Lead |

---

## Appendix: Tool List

### Core Tools (12)

| Category | Tool | Status |
|----------|------|--------|
| **Messages** | `messages_inbox` | ⏳ |
| **Messages** | `messages_send` | ⏳ |
| **Messages** | `messages_ack` | ⏳ |
| **Agent** | `agent_status` | ⏳ |
| **Agent** | `agent_heartbeat` | ⏳ |
| **Agent** | `checkpoint_post` | ⏳ |
| **Tasks** | `tasks_list` | ⏳ |
| **Tasks** | `tasks_get` | ⏳ |
| **Files** | `files_list` | ⏳ |
| **Files** | `files_read` | ⏳ |
| **Files** | `files_write` | ⏳ |
| **System** | `poke_agent` | ⏳ |

### Future Tools (Consider Later)

| Tool | Description |
|------|-------------|
| `linear_.*` | Linear API integration |
| `notion_.*` | Notion integration |
| `ha_.*` | Home Assistant integration |
| `calendar_.*` | Calendar integration |

---

**End of Manifest**
