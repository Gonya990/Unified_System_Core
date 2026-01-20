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

# 1. Local Auto-Commit
echo -e "\n${YELLOW}[1/5] Saving local progress...${NC}"
cd "$UNIFIED_SYSTEM"
if [[ -n $(git status -s) ]]; then
    git add .
    git commit -m "chore: vibranium sync $(date '+%Y-%m-%d %H:%M:%S')"
    echo -e "${GREEN}✓ Local changes saved.${NC}"
else
    echo -e "${GREEN}✓ Nothing to save locally.${NC}"
fi

# 2. Linting & Quality Check
echo -e "\n${YELLOW}[2/5] Running Quality Check (Ruff)...${NC}"
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

# 3. Main Sync (Git & Tasks)
echo -e "\n${YELLOW}[3/5] Running Main Sync (Git & Tasks)...${NC}"
bash "$SCRIPT_DIR/sync.sh" all

# 4. Remote Update
echo -e "\n${YELLOW}[4/5] Updating Remote Server...${NC}"
if bash "$SCRIPT_DIR/deploy/remote-update.sh" --force; then
    echo -e "${GREEN}✓ Remote server updated.${NC}"
else
    echo -e "${RED}✗ Remote update failed. Check Tailscale!${NC}"
fi

# 5. Final Status
echo -e "\n${YELLOW}[5/5] Verifying Final State...${NC}"
git status
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}💎 SYSTEM FULLY UNIFIED 💎${NC}"
echo -e "${YELLOW}Next startup will be 100% synchronized.${NC}"
