# Cursor ↔ OpenClaw via MCP

## Roles

| Component | Role |
|-----------|------|
| Cursor Agent | MCP **client** — coding, risk checks |
| `openclaw-mcp-bridge` | MCP **server** (stdio) — tools proxy |
| OpenClaw Gateway | 24/7 orchestration, memory-wiki, Task Flows |
| approval-gateway | Policy + YubiKey leases |

## Config

Project: [`.cursor/mcp.json`](../../.cursor/mcp.json)

```json
{
  "mcpServers": {
    "unified-openclaw": {
      "command": "python3",
      "args": ["/Users/igorgoncharenko/unified-core-staging/services/openclaw-mcp-bridge/server.py"]
    }
  }
}
```

Production on NUC:

```json
"command": "ssh",
"args": ["smart.ayu-altair.ts.net", "/opt/unified/openclaw-mcp-bridge/server.py"]
```

Set `OPENCLAW_BASE_URL=http://127.0.0.1:18789` on gateway host.

## Tools

| Tool | Purpose |
|------|---------|
| `get_recent_alerts` | Heartbeat / Task Flow failures |
| `memory_search` | Long-term wiki with provenance |
| `get_risk_score` | Visual Guards (→ approval-gateway) |
| `enqueue_background_task` | Non-critical background work |

## Example flow

1. OpenClaw night benchmark on `gpu-node-1` → Task Flow completes.
2. Morning: Cursor Agent calls `get_recent_alerts(hours=8)`.
3. Agent calls `get_risk_score` before `terraform apply`.
4. If score ≥ 0.7 → user touches YubiKey → `POST /v1/approve`.
