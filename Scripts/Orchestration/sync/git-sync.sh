#!/bin/bash
# Git Sync - Safe bidirectional git synchronization
# Does NOT auto-commit or force push

set -euo pipefail

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}Git Sync${NC}"
echo "=========================================="

# 1. Check current status
echo -e "\n${YELLOW}[1/4] Checking local status...${NC}"
if ! git diff-index --quiet HEAD -- 2>/dev/null; then
    echo -e "${RED}Uncommitted changes detected:${NC}"
    git status --short
    echo ""
    echo "Please commit or stash changes before syncing."
    exit 1
fi

# 2. Fetch remote
echo -e "\n${YELLOW}[2/4] Fetching remote...${NC}"
git fetch origin

# 3. Check if we're behind/ahead
LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/main)
BASE=$(git merge-base HEAD origin/main)

if [ "$LOCAL" = "$REMOTE" ]; then
    echo -e "${GREEN}Already up to date.${NC}"
elif [ "$LOCAL" = "$BASE" ]; then
    echo -e "\n${YELLOW}[3/4] Pulling changes...${NC}"
    git pull origin main --rebase
    echo -e "${GREEN}Pulled $(git rev-list --count $LOCAL..$REMOTE) commits.${NC}"
elif [ "$REMOTE" = "$BASE" ]; then
    echo -e "\n${YELLOW}[3/4] Pushing local commits...${NC}"
    git push origin main
    echo -e "${GREEN}Pushed $(git rev-list --count $REMOTE..$LOCAL) commits.${NC}"
else
    echo -e "\n${YELLOW}[3/4] Branches diverged. Rebasing...${NC}"
    if git pull origin main --rebase; then
        echo -e "${GREEN}Rebase successful.${NC}"
        echo -e "\n${YELLOW}[4/4] Pushing...${NC}"
        git push origin main
    else
        echo -e "${RED}Rebase conflict! Resolve manually:${NC}"
        echo "  git status"
        echo "  # fix conflicts"
        echo "  git add ."
        echo "  git rebase --continue"
        exit 1
    fi
fi

echo ""
echo -e "${GREEN}Git sync complete.${NC}"
