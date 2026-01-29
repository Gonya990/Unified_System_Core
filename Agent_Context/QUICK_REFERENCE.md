# Agent Quick Reference Index

> Fast lookup for specific topics. Use `Read file.md` with line numbers or section names.

---

## Constants

```
PROJECT_KEY = "home-gonya-unified-system"
AGENT_MAIL_SERVER = "http://127.0.0.1:8765"
BEADS_SYNC_BRANCH = "beads-sync"
```

---

## Agent Mail

| Need | File | Section |
| --- | --- | --- |
| Register agent | `AGENTS.md` | `#agent-mail-system` |
| Project key explanation | `agents/REGISTRY.md` | `#project-key-important` |
| Full setup guide | `Knowledge_Base/HOW_TO_GIVE_ANOTHER_AGENT_ACCESS_TO_MCP_AGENT_MAIL.md` | Full file |
| Tool reference | `AGENTS.md` | `#agent-mail-system` → Core Tools table |
| Cross-project messaging | `Knowledge_Base/HOW_TO_GIVE_ANOTHER_AGENT_ACCESS_TO_MCP_AGENT_MAIL.md` | `#step-5-cross-project-communication` |

### Quick Tool Signatures

```python
# Register (at session start)
agent_mail_register_agent(
  project_key="home-gonya-unified-system",
  program="opencode",
  model="claude-sonnet-4",
  task_description="..."
)

# Fetch inbox
agent_mail_fetch_inbox(
  project_key="home-gonya-unified-system",
  agent_name="YourName",
  include_bodies=True,
  limit=20
)

# Send message
agent_mail_send_message(
  project_key="home-gonya-unified-system",
  sender_name="YourName",
  to=["RecipientName"],
  subject="...",
  body_md="..."
)

# Reserve files
agent_mail_file_reservation_paths(
  project_key="home-gonya-unified-system",
  agent_name="YourName",
  paths=["path/to/file.py"],
  ttl_seconds=3600,
  exclusive=True,
  reason="..."
)
```

---

## Beads (Task Management)

| Need | File | Section |
| --- | --- | --- |
| Basic commands | `AGENTS.md` | `#beads-workflow` |
| Priority levels | `AGENTS.md` | `#priority-levels` |
| Sync mechanism | `.beads/config.yaml` | `sync-branch` setting |
| Multi-agent sync | `.beads/README.md` | Full file |

### Quick Commands

```bash
bd sync                    # Sync with remote
bd ready                   # Show unblocked work
bd list --status=open      # All open issues
bd update <id> --status=in_progress  # Claim work
bd close <id>              # Complete work
```

---

## Git Workflow

| Need | File | Section |
| --- | --- | --- |
| Commit types | `AGENTS.md` | `#commit-types` |
| WIP commits | `AGENTS.md` | `#git-coordination` |
| Multi-agent safety | `AGENTS.md` | `#file-safety` |
| Session completion | `AGENTS.md` | `#landing-the-plane-session-completion` |

---

## Workflows (Slash Commands)

| Command | Purpose | File |
| --- | --- | --- |
| `/sync-mail` | Sync inbox, beads, check locks | `.agent/workflows/sync-mail.md` |
| `/commit-push` | Stage, commit, push | `.agent/workflows/commit-push.md` |
| `/update-progress` | Update task status | `.agent/workflows/update-progress.md` |

---

## Machine Info

| Machine | File |
| --- | --- |
| igor-gaming-1 (WSL2) | `Agent_Context/machines/igor-gaming-1/MACHINE_INFO.md` |
| MacBook-Air | `Agent_Context/machines/MacBook-Air/MACHINE_INFO.md` |
| igor-gaming (Windows) | `Agent_Context/machines/igor-gaming/MACHINE_INFO.md` |
| pve (Proxmox) | `Agent_Context/machines/pve/MACHINE_INFO.md` |

---

## Architecture

| Need | File |
| --- | --- |
| System overview | `Knowledge_Base/Architecture/SYSTEM_ARCHITECTURE.md` |
| Context handoff | `Knowledge_Base/Architecture/CONTEXT_HANDOFF.md` |
| Multi-agent config | `Knowledge_Base/Architecture/MULTI_AGENT_CONFIG.md` |

---

## Onboarding

| Need | File |
| --- | --- |
| New agent setup | `Knowledge_Base/Docs/AGENT_ONBOARDING.md` |
| Agent registry | `agents/REGISTRY.md` |
| Project navigation | `Knowledge_Base/Docs/NAVIGATION.md` |

---

## Safety Rules

| Need | File | Section |
| --- | --- | --- |
| Never auto-run | `AGENTS.md` | `#never-auto-run` |
| Confirm with user | `AGENTS.md` | `#always-confirm-with-user` |
| File reservations | `AGENTS.md` | `#file-reservations-leases` |
| Process safety | `AGENTS.md` | `#process-safety` |

---

## UBS (Bug Scanner)

| Need | File | Section |
| --- | --- | --- |
| Quick reference | `AGENTS.md` | `#ubs-quick-reference-for-ai-agents` |
| Commands | `AGENTS.md` | Search for `ubs` commands block |

```bash
ubs <changed-files>        # Before every commit
ubs $(git diff --name-only --cached)  # Staged files
```

---

*Last updated: 2026-01-07*
