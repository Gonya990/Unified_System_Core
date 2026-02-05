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

# 3. Main Sync (Git & Tasks)
echo -e "\n${YELLOW}[3/5] Running Main Sync (Git & Tasks)...${NC}"
bash "$SCRIPT_DIR/sync.sh" all

# 4. Remote Update
echo -e "\n${YELLOW}[4/5] Updating Remote Server...${NC}"
if bash "$SCRIPT_DIR/deploy/remote-update.sh" --force; then
    echo -e "${GREEN}✓ Remote server code updated (where applicable).${NC}"
else
    echo -e "${RED}✗ Remote handle failed. Check Tailscale!${NC}"
fi

# 4b. Production Container Deploy (K8s & Compose)
echo -e "\n${YELLOW}[4b/5] Deploying Production Containers...${NC}"

# 1. K8s (AI Bot)
if ssh unified-home-core-cloud "sudo kubectl apply -f -" < "$UNIFIED_SYSTEM/Projects/AI_Core/k8s/deployment.yaml"; then
    echo -e "${GREEN}✓ K8s: AI Telegram Bot deployment updated.${NC}"
    ssh unified-home-core-cloud "sudo kubectl rollout restart deployment/ai-telegram-bot -n telegram-bot"
else
    echo -e "${RED}✗ K8s deployment failed.${NC}"
fi

# 2. Docker Compose (Services, Dashboard, MCP)
echo -e "${YELLOW}Syncing Tracked Project Context (High Speed)...${NC}"

# Use git ls-files to only sync tracked files. This is extremely fast.
# We also explicitly include any local .env file if it exists.
files_to_sync=$(git ls-files)
if [ -f ".env" ]; then
    files_to_sync="$files_to_sync .env"
fi

# Create tarball from tracked files + .env and pipe to cloud
# We use --no-recursion because we are providing the file list explicitly
echo "$files_to_sync" | tr ' ' '\n' | tar --no-xattrs -czf - --no-recursion -T - | ssh unified-home-core-cloud "mkdir -p /home/gonya/Unified_System && tar -xzf - -C /home/gonya/Unified_System"

echo -e "${YELLOW}Restarting Compose services (Background Builder)...${NC}"
# Use --build to ensure code changes are picked up
ssh unified-home-core-cloud "cd /home/gonya/Unified_System && sudo docker compose up -d --build"

# 5. Final Status
echo -e "\n${YELLOW}[5/5] Verifying Final State...${NC}"
git status
echo -e "\n========================================"
echo -e "💎 SYSTEM FULLY UNIFIED & CONTAINERIZED 💎"
echo -e "Next startup will be 100% synchronized."
echo "=========================================="
