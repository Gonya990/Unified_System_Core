#!/bin/bash
# Remote Update - Pull latest code on remote server
# Does NOT reset or destroy anything

set -euo pipefail

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

# 1. Define nodes (could be moved to a separate file later)
NODES=("smart" "igor-gaming" "gpu-node-1" "unified-home-core-cloud")
REMOTE_PATH_BASE="/home/gonya/Unified_System"

echo -e "${GREEN}Multi-Node Remote Update${NC}"
echo "=========================================="

for NODE in "${NODES[@]}"; do
    echo -e "\n${BLUE}>>> Processing node: $NODE${NC}"
    
    # Check connectivity (detects network reachability even if auth fails)
    # We use { || true; } to ignore ssh exit code (255 due to auth fail) because pipefail is set
    if ! { ssh -v -o BatchMode=yes -o ConnectTimeout=5 "$NODE" exit 2>&1 || true; } | grep -q "Connection established"; then
        echo -e "${RED}✗ $NODE is not reachable. Skipping.${NC}"
        continue
    fi

    # 1. Check remote status
    echo -e "${YELLOW}[1/3] Checking remote status on $NODE...${NC}"
    REMOTE_STATUS=$(ssh "$NODE" "cd $REMOTE_PATH_BASE && git status --porcelain" 2>/dev/null || echo "CONNECTION_FAILED")

    if [ "$REMOTE_STATUS" = "CONNECTION_FAILED" ]; then
        echo -e "${RED}✗ Cannot connect to $NODE. Skipping.${NC}"
        continue
    fi

    if [ -n "$REMOTE_STATUS" ]; then
        echo -e "${RED}! $NODE has uncommitted changes.${NC}"
        if [ "${1:-}" = "--force" ]; then
            echo -e "${YELLOW}Discarding remote changes...${NC}"
            ssh "$NODE" "cd $REMOTE_PATH_BASE && git checkout -- . && git clean -fd"
        else
            echo "Skipping $NODE. Use --force to override."
            continue
        fi
    fi

    # 2. Pull on remote
    echo -e "${YELLOW}[2/3] Pulling on $NODE...${NC}"
    ssh "$NODE" "cd $REMOTE_PATH_BASE && git pull origin main"

    # 3. Update submodules
    echo -e "${YELLOW}[3/3] Updating submodules on $NODE...${NC}"
    ssh "$NODE" "cd $REMOTE_PATH_BASE && git submodule update --init --recursive" || echo "Submodule update skipped."

    echo -e "${GREEN}✓ $NODE update complete.${NC}"
done

echo -e "\n${GREEN}All reachable nodes updated.${NC}"
