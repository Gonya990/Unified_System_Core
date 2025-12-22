# 🤖 Agent Context Repository

This folder contains context handoff documentation for AI agents working on this system. It enables seamless knowledge transfer between sessions and across different agent instances.

## 📁 Structure

```
Agent_Context/
├── CONTEXT_HANDOFF.md       # Main context document (read this first)
├── README.md                # This file - how to use & contribute
├── .env.example             # Environment variables template
├── .gitignore               # Files to exclude from git
│
├── docs/                    # System documentation
│   ├── NAVIGATION.md        # Project navigation guide
│   ├── PROJECTS.yaml        # Project registry
│   └── RULES.md             # File organization rules
│
├── scripts/                 # Utility scripts
│   ├── install_antigravity.sh
│   ├── debug_telegram.py
│   └── ...
│
├── configs/                 # Service configurations
│   ├── antigravity-mcp.service
│   └── docker_gpu_check_workflow.json
│
├── mcp-server/              # MCP Server source code
│   └── src/
│
└── brain/                   # Session artifacts by conversation
    └── [conversation-id]/
        ├── task.md
        ├── implementation_plan.md
        └── walkthrough.md
```

---

## 🚀 For New Agents: Quick Start

1. **Read `CONTEXT_HANDOFF.md`** - Contains complete system knowledge
2. **Check `brain/` folder** - Review recent session artifacts for context
3. **Refer to `docs/PROJECTS.yaml`** - Understand project structure

---

## 📝 How to Add Context (For Agents)

When completing a significant task, add your context to this repository:

### 1. Create a Session Artifact Folder

```bash
mkdir -p brain/<your-conversation-id>
```

Use your conversation ID (found in your session metadata) as the folder name.

### 2. Include These Files

| File | Purpose | When to Create |
|------|---------|----------------|
| `task.md` | Checklist of work done | Always |
| `implementation_plan.md` | Technical design | For complex changes |
| `walkthrough.md` | Summary of what was accomplished | After completing work |

### 3. File Templates

**task.md:**

```markdown
# Task: [Description]

## Phase 1: [Phase Name]
- [x] Completed item
- [/] In progress item
- [ ] Pending item

## Phase 2: [Next Phase]
- [ ] ...
```

**walkthrough.md:**

```markdown
# [Task Title] Walkthrough

## Summary
Brief description of what was accomplished.

## Changes Made
- File 1: Description
- File 2: Description

## Verification
How the changes were tested.

## Notes for Future Agents
Any important context for continuity.
```

### 4. Update CONTEXT_HANDOFF.md

If your work introduces significant changes:

- Add new services to the Network Topology section
- Update the Active Todos section
- Add new projects to the inventory

---

## 🔐 Security Guidelines

Before committing:

1. **NEVER commit real secrets** - Use `.env.example` with placeholders
2. **Scan for secrets:**

   ```bash
   grep -r "token\|password\|secret\|api_key" . --include="*.md" --include="*.py" --include="*.ts"
   ```

3. **Tailscale IPs (100.x.x.x)** are fine - they're private addresses
4. **Check `.gitignore`** includes sensitive patterns

---

## 🔄 Git Workflow

### Adding Your Context

```bash
cd Agent_Context

# Add your session artifacts
git add brain/<your-conversation-id>/

# Commit with descriptive message
git commit -m "context: Add session artifacts for [task description]"

# Push to remote
git push origin main
```

### Updating Main Documentation

```bash
git add CONTEXT_HANDOFF.md
git commit -m "docs: Update context handoff with [changes]"
git push origin main
```

---

## 🧠 Brain Folder Naming Convention

Use the format: `<conversation-id>`

Example: `0866ee1f-5969-46a1-9ab8-ee14130c2bc1`

This allows tracing artifacts back to specific sessions.

---

## 📊 Current Agent Sessions

| Session ID | Title | Status | Date |
|------------|-------|--------|------|
| `0866ee1f-...` | Unified Topology Setup | ✅ Complete | Dec 2024 |
| `a1c2070a-...` | Proxmox Reconnaissance | 🔄 In Progress | Dec 2024 |
| `b64b29bb-...` | Hybrid Cortex Activation | ✅ Complete | Dec 2024 |
| `bc334b70-...` | Mac Service Access | ✅ Complete | Dec 2024 |
| `b32255f1-...` | Docker GPU Check | ✅ Complete | Dec 2024 |
| `eb70130d-...` | Context Handoff Docs | ✅ Complete | Dec 2024 |

---

## 🆘 Troubleshooting

**Can't find context?**

- Check `brain/` for recent session artifacts
- Read `CONTEXT_HANDOFF.md` for system overview
- Check `docs/NAVIGATION.md` for project locations

**Need to update secrets?**

- Copy `.env.example` to `.env` (gitignored)
- Fill in actual values locally

**Git push fails?**

- Ensure you have write access to the repository
- Try: `git pull --rebase origin main` then push again

---

*Last updated: 2025-12-22*
