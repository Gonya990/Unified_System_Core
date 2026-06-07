#!/bin/bash
# 💎 Vibranium Sync - Official Unified System Entry Point
# Core of the /sync workflow. Combines local save, git sync, task sync, and deployment.
# Logic: Save Progress -> Sync (pull/push/tasks) -> Deploy (remote update)

set -euo pipefail

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
UNIFIED_SYSTEM="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo -e "${GREEN}💎 VIBRANIUM SYNC STARTED${NC}"
echo "=========================================="

# 1. Linting & Quality Check
echo -e "\n${YELLOW}[1/5] Running Quality Check (Ruff)...${NC}"
if command -v ruff &> /dev/null; then
    RUFF_BIN="$(command -v ruff)"
    if "$RUFF_BIN" check Scripts/ Projects/AI_Core/src/ --fix; then
        echo -e "${GREEN}✓ Code quality check passed (and auto-fixed).${NC}"
    else
        echo -e "${YELLOW}! Linting found issues that require manual attention.${NC}"
    fi
else
    # Fallback to check specific path if command not found, or just skip
    RUFF_BIN="$HOME/Library/Python/3.9/bin/ruff"
    if [ -f "$RUFF_BIN" ]; then
         if "$RUFF_BIN" check Scripts/ Projects/AI_Core/src/ --fix; then
            echo -e "${GREEN}✓ Code quality check passed (and auto-fixed).${NC}"
        else
            echo -e "${YELLOW}! Linting found issues that require manual attention.${NC}"
        fi
    else
        echo -e "${YELLOW}! Ruff not found. Skipping quality check.${NC}"
    fi
fi

# 2. Local Commit (Mandatory)
echo -e "\n${YELLOW}[2/5] Finalizing Local Changes...${NC}"
cd "$UNIFIED_SYSTEM"

# Run the automated descriptive committer
if [[ -n $(git status -s) ]]; then
    if bash "$SCRIPT_DIR/sync/auto-commit.sh"; then
        echo -e "${GREEN}✓ Local changes committed with descriptive title.${NC}"
    else
        echo -e "${RED}✗ Auto-commit failed. Please resolve manual conflicts.${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✓ Working tree clean. Ready to sync.${NC}"
fi

# Double check status - sync MUST fail if uncommitted
if [[ -n $(git status -s) ]]; then
    echo -e "${RED}✗ SHUTDOWN: Working directory is still dirty. Aborting sync for safety.${NC}"
    exit 1
fi

# 3. Main Sync (Git, Tasks & Tokens)
echo -e "\n${YELLOW}[3/5] Running Main Sync (Git, Tasks & Tokens)...${NC}"
bash "$SCRIPT_DIR/sync.sh" all
bash "$SCRIPT_DIR/sync/token-sync.sh"

# 4. Remote Update
echo -e "\n${YELLOW}[4/5] Updating Remote Server...${NC}"
if bash "$SCRIPT_DIR/deploy/remote-update.sh" --force; then
    echo -e "${GREEN}✓ Remote server code updated (where applicable).${NC}"
else
    echo -e "${RED}✗ Remote handle failed. Check Tailscale!${NC}"
fi

# 4b. Production Container Deploy (Docker Compose on igor-gaming)
echo -e "\n${YELLOW}[4b/5] Deploying Production Containers to igor-gaming (WSL2)...${NC}"

echo -e "${YELLOW}Syncing Project Context & Secrets...${NC}"

# Compile the list of files to sync (tracked files + .env + Secrets + service account keys)
files_to_sync=$(git ls-files)
if [ -f ".env" ]; then
    files_to_sync="$files_to_sync .env"
fi

if [ -d "Secrets" ]; then
    secrets_files=$(find Secrets -type f 2>/dev/null || true)
    files_to_sync="$files_to_sync $secrets_files"
fi

if [ -f "Projects/AI_Core/unified-core-service-account.json" ]; then
    files_to_sync="$files_to_sync Projects/AI_Core/unified-core-service-account.json"
fi

if [ -f "Projects/AI_Core/gcp-service-account.json" ]; then
    files_to_sync="$files_to_sync Projects/AI_Core/gcp-service-account.json"
fi

# Create tarball and pipe to igor-gaming WSL2
echo "$files_to_sync" | tr ' ' '\n' | tar --no-xattrs -czf - --no-recursion -T - 2>/dev/null | ssh igor-gaming "wsl bash -c 'mkdir -p /home/gonya/Unified_System_Core && tar -xzf - -C /home/gonya/Unified_System_Core'"



echo -e "${YELLOW}Restarting Compose services on igor-gaming WSL2...${NC}"
# Use docker compose up -d --build to update container builds with new code
ssh igor-gaming "wsl docker compose -f /home/gonya/Unified_System_Core/docker-compose.yml up -d --build"


# 5. Final Status
echo -e "\n${YELLOW}[5/5] Verifying Final State...${NC}"
git status
echo -e "\n========================================"
echo -e "💎 SYSTEM FULLY UNIFIED & CONTAINERIZED 💎"
echo -e "Next startup will be 100% synchronized."
echo "=========================================="
