#!/bin/bash
# Remote Update - Pull latest code on remote server
# Usage: ./remote-update.sh [--force]

set -euo pipefail

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

# Define Node Configurations
# Format: "Host:RemotePath"
NODES=(
    "unified-home-core-cloud:/home/gonya/Unified_System"
    "gpu-node-1:/home/gonya990/Unified_System_Core"
    "igor-gaming:Unified_System_Core"
)

REPO_URL="git@github.com:Gonya990/Unified_System_Core.git"

echo -e "${GREEN}💎 Multi-Node Remote Update${NC}"
echo "=========================================="

for CONFIG in "${NODES[@]}"; do
    NODE="${CONFIG%%:*}"
    REMOTE_PATH="${CONFIG#*:}"
    
# Nodes that use Container-Only mode (No Git)
PRODUCTION_NODES=("unified-home-core-cloud")

echo -e "\n${BLUE}>>> Processing node: $NODE${NC}"

# 1. Connectivity Check
if ssh -q -o BatchMode=yes -o ConnectTimeout=5 "$NODE" exit; then
    echo -e "${GREEN}✓ Connected to $NODE${NC}"
else
    echo -e "${RED}✗ Cannot connect to $NODE. Skipping.${NC}"
    continue
fi

# 2. Skip Git for Production Cloud Nodes
IS_PRODUCTION=false
for P_NODE in "${PRODUCTION_NODES[@]}"; do
    if [[ "$NODE" == "$P_NODE" ]]; then
        IS_PRODUCTION=true
        break
    fi
done

if [ "$IS_PRODUCTION" = true ]; then
    echo -e "${YELLOW}>>> NODE is Production (Container-Only). Skipping Git...${NC}"
    continue
fi

    # 3. Check/Setup Remote Directory
    echo -e "${YELLOW}[1/3] Checking remote filesystem...${NC}"
    
    # Use 'cd && echo OK' which works on both Linux (bash) and Windows (cmd)
    if ssh "$NODE" "cd $REMOTE_PATH && echo OK" | grep -q "OK"; then
        # 4. Check Git Status
        REMOTE_STATUS=$(ssh "$NODE" "cd $REMOTE_PATH && git status --porcelain" 2>/dev/null || echo "GIT_ERROR")
        
        if [ "$REMOTE_STATUS" = "GIT_ERROR" ]; then
             echo -e "${RED}! Git error on $NODE (Not a repo or git missing).${NC}"
             continue
        fi

        if [ -n "$REMOTE_STATUS" ]; then
            echo -e "${RED}! $NODE has uncommitted changes.${NC}"
            if [ "${1:-}" = "--force" ]; then
                STASH_NAME="AUTO_SYNC_$(date '+%Y%m%d_%H%M%S')"
                echo -e "${YELLOW}Safely stashing remote changes as: $STASH_NAME...${NC}"
                
                # Capture the diff before stashing to show the user
                ssh "$NODE" "cd $REMOTE_PATH && echo 'Stashed Files:' && git diff --name-only && git stash push -m '$STASH_NAME' && echo '✓ Stash created: \$(git stash list | head -n 1)'"
            else
                echo -e "${RED}Skipping $NODE (Dirty). Use --force to stash and update.${NC}"
                ssh "$NODE" "cd $REMOTE_PATH && git status --short"
                continue
            fi
        fi
        
        # 5. Pull Updates (using Agent Forwarding)
        echo -e "${YELLOW}[2/3] Pulling updates...${NC}"
        
        GIT_CMD="git pull origin main"
        if [ "${1:-}" = "--force" ]; then
             echo -e "${YELLOW}Force mode: Resetting to origin/main...${NC}"
             GIT_CMD="git fetch origin && git reset --hard origin/main"
        fi

        if ssh -A "$NODE" "cd $REMOTE_PATH && $GIT_CMD"; then
             echo -e "${GREEN}✓ Code updated.${NC}"
        else
             echo -e "${RED}✗ Git update failed.${NC}"
             continue
        fi

    else
        echo -e "${YELLOW}Directory not found. Cloning repo...${NC}"
        # Clone Repos (using Agent Forwarding)
        if ssh -A "$NODE" "git -c core.sshCommand=\"ssh -o StrictHostKeyChecking=no\" clone $REPO_URL $REMOTE_PATH"; then
            echo -e "${GREEN}✓ Repository cloned to $REMOTE_PATH.${NC}"
        else
            echo -e "${RED}✗ Git clone failed. Check SSH keys/Agent forwarding.${NC}"
            continue
        fi
    fi

    # 6. Update Submodules
    echo -e "${YELLOW}[3/3] Updating submodules...${NC}"
    ssh -A "$NODE" "cd $REMOTE_PATH && git submodule update --init --recursive" || echo "Submodule warning."

    echo -e "${GREEN}✓ $NODE fully synced.${NC}"
done

echo -e "\n${GREEN}All reachable nodes processed.${NC}"
