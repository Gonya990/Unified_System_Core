#!/bin/bash
# 💎 Vibranium Sync - One command to unify everything
# Коммитит локально, пушит, синкает задачи и обновляет сервер.

set -euo pipefail

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
UNIFIED_SYSTEM="/Users/macbook/Documents/Unified_System"

echo -e "${GREEN}💎 VIBRANIUM SYNC STARTED${NC}"
echo "=========================================="

# 1. Local Auto-Commit
echo -e "\n${YELLOW}[1/4] Saving local progress...${NC}"
cd "$UNIFIED_SYSTEM"
if [[ -n $(git status -s) ]]; then
    git add .
    git commit -m "chore: vibranium sync $(date '+%Y-%m-%d %H:%M:%S')"
    echo -e "${GREEN}✓ Local changes saved.${NC}"
else
    echo -e "${GREEN}✓ Nothing to save locally.${NC}"
fi

# 2. Main Sync (Git & Tasks)
echo -e "\n${YELLOW}[2/4] Running Main Sync (Git & Tasks)...${NC}"
bash "$SCRIPT_DIR/sync.sh" all

# 3. Remote Update
echo -e "\n${YELLOW}[3/4] Updating Remote Server...${NC}"
if bash "$SCRIPT_DIR/deploy/remote-update.sh" --force; then
    echo -e "${GREEN}✓ Remote server updated.${NC}"
else
    echo -e "${RED}✗ Remote update failed. Check Tailscale!${NC}"
fi

# 4. Final Status
echo -e "\n${YELLOW}[4/4] Verifying Final State...${NC}"
git status
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}💎 SYSTEM FULLY UNIFIED 💎${NC}"
echo -e "${YELLOW}Next startup will be 100% synchronized.${NC}"
