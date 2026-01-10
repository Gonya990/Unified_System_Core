#!/bin/bash
# Remote Update - Pull latest code on remote server
# Does NOT reset or destroy anything

set -euo pipefail

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

REMOTE_HOST="${REMOTE_HOST:-gonya@100.110.209.49}"
REMOTE_PATH="${REMOTE_PATH:-/home/gonya/Unified_System}"

echo -e "${GREEN}Remote Update${NC}"
echo "=========================================="
echo "Host: $REMOTE_HOST"
echo "Path: $REMOTE_PATH"

# 1. Check remote status first
echo -e "\n${YELLOW}[1/3] Checking remote status...${NC}"
REMOTE_STATUS=$(tailscale ssh "$REMOTE_HOST" "cd $REMOTE_PATH && git status --porcelain" 2>/dev/null || echo "CONNECTION_FAILED")

if [ "$REMOTE_STATUS" = "CONNECTION_FAILED" ]; then
    echo -e "${RED}Cannot connect to remote. Check Tailscale.${NC}"
    exit 1
fi

if [ -n "$REMOTE_STATUS" ]; then
    echo -e "${RED}Remote has uncommitted changes:${NC}"
    echo "$REMOTE_STATUS"
    echo ""
    echo "Options:"
    echo "  1. SSH in and commit/stash changes"
    echo "  2. Run with --force to discard remote changes (DANGEROUS)"

    if [ "${1:-}" = "--force" ]; then
        echo -e "\n${YELLOW}--force specified. Discarding remote changes...${NC}"
        tailscale ssh "$REMOTE_HOST" "cd $REMOTE_PATH && git checkout -- . && git clean -fd"
    else
        exit 1
    fi
fi

# 2. Pull on remote
echo -e "\n${YELLOW}[2/3] Pulling on remote...${NC}"
tailscale ssh "$REMOTE_HOST" "cd $REMOTE_PATH && git pull origin main"

# 3. Update submodules
echo -e "\n${YELLOW}[3/3] Updating submodules...${NC}"
tailscale ssh "$REMOTE_HOST" "cd $REMOTE_PATH && git submodule update --init --recursive" || echo "Submodule update skipped."

echo ""
echo -e "${GREEN}Remote update complete.${NC}"
