# Scripts - Agent Knowledge Base

**Generated:** 2026-01-04T11:45:00Z | **Commit:** 0a4ad48 | **Branch:** main

## OVERVIEW

Automation, deployment, and tooling scripts for the distributed AI cluster. Heavy use of Expect for remote node management over Tailscale mesh.

## STRUCTURE

```
Scripts/
├── automation/         # Background tasks (Gmail, CV sync, ChatGPT)
│   ├── run_all.sh      # Master orchestrator
│   └── gmail_agent.py  # Email monitoring
├── bot/                # AI bot management (remote .exp scripts)
├── deployment/         # VM/Cloud setup
├── External/           # Inter-agent communication (ACP)
│   ├── agent_comm.sh   # MCP Agent Mail wrapper
│   └── mission_sync.sh # Task claiming from hub
├── homeassistant/      # HA integration clients
├── tools/              # Admin utilities
├── gcp/                # GCP metrics
├── network/            # Tailscale setup
└── openai_data_integration/  # ChatGPT import pipeline
```

## WHERE TO LOOK

| Task | Location | Notes |
|------|----------|-------|
| Add automation | `automation/` | Add to `run_all.sh` if scheduled |
| Bot remote control | `bot/*.exp` | Uses SSH over Tailscale |
| Inter-agent messaging | `External/agent_comm.sh` | JSON-RPC to mcp_agent_mail |
| HA automation | `homeassistant/ha_client.py` | Domain-specific client |
| Admin utility | `tools/` | General-purpose scripts |
| Deploy to VM | `deployment/` | Bash + Expect combo |

## KEY PATTERNS

### Domain-Specific Clients
Each integration has a "client" script centralizing API logic:
```
homeassistant/ → ha_client.py
External/      → agent_comm.sh
gcp/           → gcp_metrics_collector.py
```

### Remote-First Execution
Scripts assume Tailscale mesh connectivity. Common pattern:
```bash
ssh gonya@100.78.x.x "command"  # Direct SSH
./script.exp 100.78.x.x         # Expect for interactive
```

### Base Directory Resolution
Python scripts use:
```python
BASE_DIR = Path(__file__).resolve().parent.parent.parent
```

## CONVENTIONS

| Type | Convention | Example |
|------|------------|---------|
| Shell | `snake_case.sh` | `autosave_changes.sh` |
| Python | `snake_case.py` | `gmail_agent.py` |
| Expect | `snake_case.exp` | `debug_bot.exp` |
| Dirs | Functional domain | `bot/`, `homeassistant/` |

### Shebang Standards
```bash
#!/usr/bin/env python3   # Python
#!/bin/bash              # Shell
#!/usr/bin/expect        # Expect
```

## ANTI-PATTERNS (THIS DIRECTORY)

| Forbidden | Why |
|-----------|-----|
| `pip install` | Use `uv` exclusively |
| Hardcoded secrets | Use `.env` or `.credentials/` |
| Killing random PIDs | Only kill YOUR processes |

## COMMANDS

```bash
# Run all automations
./Scripts/automation/run_all.sh

# Remote bot debug
./Scripts/bot/debug_bot.exp

# Send agent message
./Scripts/External/agent_comm.sh send "message"

# HA status check
python3 Scripts/homeassistant/ha_client.py status
```

## NOTES

- **Logs**: Output to `logs/automation/`
- **Credentials**: Local `.credentials/` subdirs (gitignored)
- **Tailscale IPs**: `100.x.x.x` range for mesh nodes
- **Bilingual**: READMEs often in English + Russian
