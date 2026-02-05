#!/bin/bash
# Prompt Commit - Interactively asks for a commit message or uses a generated one
# Usage: ./prompt-commit.sh [default_message]

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

DEFAULT_MSG="${1:-chore: update system}"

echo -e "\n${BLUE}📝 Preparing Commit...${NC}"
git status --short

echo -e "\n${YELLOW}Current uncommitted changes found.${NC}"
echo -e "Enter commit message (or press Enter for: ${GREEN}$DEFAULT_MSG${NC}):"
read -r USER_MSG

FINAL_MSG="${USER_MSG:-$DEFAULT_MSG}"

git add .
git commit -m "$FINAL_MSG"

echo -e "${GREEN}✓ Committed: $FINAL_MSG${NC}"
