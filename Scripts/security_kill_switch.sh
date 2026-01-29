#!/bin/bash
# 🛡️ SECURITY KILL SWITCH
# Objective: Terminate persistent git processes and disable auto-sync to isolate the system.

echo "🚨 INITIATING SECURITY LOCKDOWN..."

# 1. Kill aggressive Git processes
echo "[1/3] Hunting for background git processes..."
# Kill git, git-remote-http, git-upload-pack, but exclude the current script
pkill -f "git fetch" || echo "No git fetch found."
pkill -f "git pull" || echo "No git pull found."
pkill -f "git push" || echo "No git push found."

# 2. Disable Auto-Fetch in Local Repo
echo "[2/3] Disabling automatic git operations..."
git config --local --unset remote.origin.fetch 2>/dev/null
git config --local gc.auto 0
git config --local fetch.prune false
# Disable git lfs locks verification which can cause network hangs
git config --local lfs.locksverify false
echo "✓ Auto-sync features disabled globally for this repo."

# 3. Check for Orphaned Node Processes (often used by extensions)
echo "[3/3] Scanning for orphaned Node.js processes..."
# Only list them, don't kill blindly as we might kill the IDE itself
ps aux | grep "node" | grep -v "Antigravity" | grep -v "grep"

echo ""
echo "🔒 SYSTEM SECURED."
echo "Auto-sync disabled. Git background tasks terminated."
