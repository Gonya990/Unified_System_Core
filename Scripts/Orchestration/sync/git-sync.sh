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

# 0. Verify remote exists
if ! git remote get-url origin >/dev/null 2>&1; then
    echo -e "${RED}No git remote named 'origin' configured.${NC}"
    echo "Add a remote before syncing, for example:"
    echo "  git remote add origin git@github.com:<org>/<repo>.git"
    exit 1
fi

# Resolve upstream branch (prefer tracking branch, then origin/HEAD)
UPSTREAM=""
if git rev-parse --abbrev-ref --symbolic-full-name @{u} >/dev/null 2>&1; then
    UPSTREAM=$(git rev-parse --abbrev-ref --symbolic-full-name @{u})
else
    ORIGIN_HEAD=$(git symbolic-ref -q --short refs/remotes/origin/HEAD 2>/dev/null || true)
    if [ -n "$ORIGIN_HEAD" ]; then
        UPSTREAM="origin/${ORIGIN_HEAD#origin/}"
    else
        for CANDIDATE in origin/main origin/master; do
            if git show-ref --verify --quiet "refs/remotes/${CANDIDATE}"; then
                UPSTREAM="$CANDIDATE"
                break
            fi
        done
    fi
fi

if [ -z "$UPSTREAM" ]; then
    echo -e "${RED}No upstream branch configured for this repo.${NC}"
    echo "Set one with:"
    echo "  git branch --set-upstream-to=origin/<branch>"
    exit 1
fi

REMOTE_NAME="${UPSTREAM%%/*}"
REMOTE_BRANCH="${UPSTREAM#*/}"

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
git fetch "$REMOTE_NAME"

# 3. Check if we're behind/ahead
LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse "$UPSTREAM")
BASE=$(git merge-base HEAD "$UPSTREAM")

if [ "$LOCAL" = "$REMOTE" ]; then
    echo -e "${GREEN}Already up to date.${NC}"
elif [ "$LOCAL" = "$BASE" ]; then
    echo -e "\n${YELLOW}[3/4] Pulling changes...${NC}"
    git pull "$REMOTE_NAME" "$REMOTE_BRANCH" --rebase
    echo -e "${GREEN}Pulled $(git rev-list --count $LOCAL..$REMOTE) commits.${NC}"
elif [ "$REMOTE" = "$BASE" ]; then
    echo -e "\n${YELLOW}[3/4] Pushing local commits...${NC}"
    git push "$REMOTE_NAME" "$REMOTE_BRANCH"
    echo -e "${GREEN}Pushed $(git rev-list --count $REMOTE..$LOCAL) commits.${NC}"
else
    echo -e "\n${YELLOW}[3/4] Branches diverged. Rebasing...${NC}"
    if git pull "$REMOTE_NAME" "$REMOTE_BRANCH" --rebase; then
        echo -e "${GREEN}Rebase successful.${NC}"
        echo -e "\n${YELLOW}[4/4] Pushing...${NC}"
        git push "$REMOTE_NAME" "$REMOTE_BRANCH"
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
