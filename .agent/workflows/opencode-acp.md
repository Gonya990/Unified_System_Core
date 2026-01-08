# OpenCode ACP Integration

> Connect to OpenCode server for ACP-based task management.
> // turbo

## Workflow

> Connect to an OpenCode server to view and manage tasks via the ACP protocol.

---

## Prerequisites

- `opencode` CLI installed: `brew install opencode`
- Tailscale active for remote connections

---

## Step 1: Check Local Server

```bash
nc -zv 127.0.0.1 4096 || echo "Local server not running"
```

If local server is needed:

```bash
opencode serve --port 4096 --hostname 0.0.0.0 &
```

---

## Step 2: Attach to Remote Server

For the central ACP server on unified-home-core-cloud (VM 106):

```bash
opencode attach http://100.110.209.49:4096
```

Alternative using Tailscale hostname:

```bash
opencode attach http://unified-home-core-cloud.tail5e8a72.ts.net:4096
```

**Note:** Server started via:
`nohup opencode serve --port 4096 --hostname 0.0.0.0 &`

---

## Step 3: List Sessions/Tasks

Once attached, you can:

- View sessions: `opencode session list`
- Check stats: `opencode stats`
- List models: `opencode models`

---

## Step 4: Start Local TUI (Alternative)

If you prefer interactive mode:

```bash
opencode /Users/macbook/Documents/Unified_System
```

This starts the Terminal UI for direct interaction.

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Connection refused | Ensure server is running: `opencode serve --port 4096` |
| Invalid URL error | Add `http://` prefix to URL |
| Auth issues | Run `opencode auth login` |

---

## Related

- Agent Communication: `Scripts/External/agent_comm.sh`
- Agent Registry: `Agent_Context/agents/REGISTRY.md`
- Agent Onboarding: `Agent_Context/Knowledge_Base/Docs/AGENT_ONBOARDING.md`
