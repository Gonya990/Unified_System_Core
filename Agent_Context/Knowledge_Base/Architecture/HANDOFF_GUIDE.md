# 🔄 Multi-Machine Context Handoff Guide

This guide explains how to collect and consolidate AI agent context from multiple machines into this unified repository.

## 🎯 Goal

Create one central repository containing all AI agent context from:

- Linux hosts (WSL2, native)
- macOS machines
- Windows machines
- Any other machines running AI agents

---

## 📍 Context Locations by Platform

### Linux / WSL2 (Antigravity)

```plaintext
~/.gemini/antigravity/brain/           # Session artifacts
~/antigravity-mcp-server/              # MCP server
~/00_NAV/                              # Navigation docs
~/01_Projects/                         # Project files
```

### macOS (Claude/Antigravity)

```plaintext
~/.gemini/antigravity/brain/           # Session artifacts
~/Library/Application Support/Claude/  # Claude desktop data
~/.claude/                             # Claude CLI config
```

### Windows (Antigravity)

```plaintext
%USERPROFILE%\.gemini\antigravity\brain\   # Session artifacts
%APPDATA%\Claude\                          # Claude desktop data
```

---

## 🚀 Quick Handoff Script

Run this on each machine to collect context:

### For Linux/macOS

```bash
#!/bin/bash
# context_handoff.sh - Run on source machine

REPO_URL="https://github.com/Gonya990/Unified_System_Core.git"
MACHINE_NAME=$(hostname)
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BRAIN_SRC="$HOME/.gemini/antigravity/brain"
WORK_DIR="/tmp/context_handoff_$TIMESTAMP"

# 1. Clone the repo
git clone "$REPO_URL" "$WORK_DIR/Unified_System_Core"
cd "$WORK_DIR/Unified_System_Core"

# 2. Create machine-specific folder
mkdir -p "Agent_Context/machines/$MACHINE_NAME/brain"

# 3. Copy brain artifacts
if [ -d "$BRAIN_SRC" ]; then
    for conv in $(ls "$BRAIN_SRC"); do
        mkdir -p "Agent_Context/machines/$MACHINE_NAME/brain/$conv"
        cp "$BRAIN_SRC/$conv"/*.md "Agent_Context/machines/$MACHINE_NAME/brain/$conv/" 2>/dev/null || true
    done
fi

# 4. Create machine inventory
cat > "Agent_Context/machines/$MACHINE_NAME/MACHINE_INFO.md" << EOF
# Machine: $MACHINE_NAME
**Collected:** $(date)
**Platform:** $(uname -s)
**User:** $USER

## Brain Sessions Collected
$(ls "$BRAIN_SRC" 2>/dev/null | wc -l) conversations

## Session List
$(ls "$BRAIN_SRC" 2>/dev/null)
EOF

# 5. Scan for secrets before commit
echo "Scanning for secrets..."
grep -r "token.*=.*['\"][^'\"]*['\"]" "Agent_Context/machines/$MACHINE_NAME" --include="*.md" --include="*.py" || true

# 6. Commit and push
git config user.email "agent@$MACHINE_NAME"
git config user.name "Agent-$MACHINE_NAME"
git add "Agent_Context/machines/$MACHINE_NAME/"
git commit -m "context: Add context from $MACHINE_NAME ($TIMESTAMP)"
git push origin main

echo "✅ Context from $MACHINE_NAME pushed to repository"
```

### For Windows (PowerShell)

```powershell
# context_handoff.ps1 - Run on Windows machine

$RepoUrl = "https://github.com/Gonya990/Unified_System_Core.git"
$MachineName = $env:COMPUTERNAME
$Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$BrainSrc = "$env:USERPROFILE\.gemini\antigravity\brain"
$WorkDir = "$env:TEMP\context_handoff_$Timestamp"

# 1. Clone the repo
git clone $RepoUrl "$WorkDir\Unified_System_Core"
Set-Location "$WorkDir\Unified_System_Core"

# 2. Create machine-specific folder
New-Item -ItemType Directory -Force -Path "Agent_Context\machines\$MachineName\brain"

# 3. Copy brain artifacts
if (Test-Path $BrainSrc) {
    Get-ChildItem $BrainSrc -Directory | ForEach-Object {
        $convDir = "Agent_Context\machines\$MachineName\brain\$($_.Name)"
        New-Item -ItemType Directory -Force -Path $convDir
        Copy-Item "$($_.FullName)\*.md" $convDir -ErrorAction SilentlyContinue
    }
}

# 4. Create machine inventory
$SessionCount = (Get-ChildItem $BrainSrc -Directory -ErrorAction SilentlyContinue).Count
@"
# Machine: $MachineName
**Collected:** $(Get-Date)
**Platform:** Windows
**User:** $env:USERNAME

## Brain Sessions Collected
$SessionCount conversations
"@ | Out-File "Agent_Context\machines\$MachineName\MACHINE_INFO.md"

# 5. Commit and push
git config user.email "agent@$MachineName"
git config user.name "Agent-$MachineName"
git add "Agent_Context\machines\$MachineName\"
git commit -m "context: Add context from $MachineName ($Timestamp)"
git push origin main

Write-Host "✅ Context from $MachineName pushed to repository"
```

---

## 📁 Unified Repository Structure

```plaintext
Unified_System_Core/
├── Agent_Context/
│   ├── README.md               # Folder overview
│   ├── Knowledge_Base/         # Central unified storage
│   │   ├── Sessions/           # Consolidated brain sessions
│   │   ├── Architecture/       # Handoff guides & system architecture
│   │   ├── Docs/               # Unified documentation
│   │   ├── Scripts/            # Universal tools
│   │   ├── Configs/            # Shared configs
│   │   └── mcp-server/         # MCP Server source
│   └── machines/               # Machine-specific overrides
│       ├── igor-gaming-1/      # WSL2 metadata
│       ├── MacBook-Air/        # macOS metadata
│       └── ...
└── ...
```

---

## ✅ Handoff Checklist

### Before Collection

- [ ] Ensure git is installed on source machine
- [ ] Have write access to the repository
- [ ] Know the Antigravity brain location

### During Collection

- [ ] Run the appropriate script for your platform
- [ ] Review the secret scan output
- [ ] Remove any actual secrets before pushing

### After Collection

- [ ] Verify files appear in GitHub
- [ ] Update main CONTEXT_HANDOFF.md if needed
- [ ] Mark machine as collected below

---

## 🖥️ Machine Collection Status

| Machine | Platform | Status | Date | Sessions |
| ------- | -------- | ------ | ---- | -------- |
| **igor-gaming-1** | Linux/WSL2 | ✅ Complete | 2025-12-22 | 18 |
| igor-gaming | Windows | ✅ Complete | 2025-12-22 | 2 (LMStudio) |
| MacBook-Air | macOS | ✅ Complete | 2025-12-22 | 14 |
| pve | Linux | ✅ Complete | 2025-12-22 | 0 (hypervisor) |
| iphone-15-pro | iOS | ✅ Complete | 2025-12-22 | Commander Node |

---

## 🔐 Security Notes

1. **Always scan for secrets** before pushing
2. **Remove API keys, tokens, passwords** - replace with placeholders
3. **Tailscale IPs (100.x.x.x)** are safe - they're private
4. **Check .gitignore** is working for sensitive files

### Quick Secret Scan

```bash
grep -rE "(token|password|secret|api_key|apikey).*[=:].*['\"][^'\"]{10,}['\"]" Agent_Context/
```

---

## 🔄 Merging Conflicts

If multiple machines push simultaneously:

```bash
git pull --rebase origin main
# Resolve any conflicts
git push origin main
```

---

## 📊 Post-Collection Tasks

After all machines are collected:

1. **Consolidate** - Review all brain sessions, identify duplicates
2. **Summarize** - Update main CONTEXT_HANDOFF.md with unified view
3. **Clean** - Remove outdated or irrelevant artifacts
4. **Document** - Add any cross-machine insights

---

---

### Last Updated

2025-12-22
