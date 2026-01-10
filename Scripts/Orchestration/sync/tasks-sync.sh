#!/bin/bash
# Tasks Sync - Sync Beads task board
# Shows current task status after sync

set -euo pipefail

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}Tasks Sync (Beads)${NC}"
echo "=========================================="

# 1. Sync beads
echo -e "\n${YELLOW}[1/2] Syncing task board...${NC}"
if command -v bd &> /dev/null; then
    bd sync
else
    echo "Beads (bd) not installed. Skipping."
    exit 0
fi

# 2. Show ready tasks
echo -e "\n${YELLOW}[2/2] Ready tasks:${NC}"
bd ready 2>/dev/null || echo "No ready tasks."

echo ""
echo -e "${GREEN}Tasks sync complete.${NC}"
