#!/bin/bash
# Auto Commit - Generates a descriptive commit message based on changed files
# Usage: ./auto-commit.sh

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Check if there are changes
if [[ -z $(git status -s) ]]; then
    echo -e "${GREEN}✓ Nothing to commit.${NC}"
    exit 0
fi

# Generate message based on files
FILES=$(git status --porcelain | awk '{print $2}')
CHANGES=""

# Identify key areas
if echo "$FILES" | grep -q "docker-compose.yml\|Dockerfile\|infra/docker"; then
    CHANGES="infra: optimize container orchestration & docker configs"
elif echo "$FILES" | grep -q "vibranium-sync.sh\|remote-update.sh\|sync.sh"; then
    CHANGES="sync: enhance cross-node synchronization logic"
elif echo "$FILES" | grep -q "Projects/AI_Core"; then
    CHANGES="feat(ai-core): update telegram bot v2 and k8s configuration"
elif echo "$FILES" | grep -q "Projects/Content_Factory"; then
    CHANGES="feat(factory): update content automation pipeline"
elif echo "$FILES" | grep -q "markitdown_server.py"; then
    CHANGES="feat(mcp): add markitdown server for document processing"
else
    # Fallback to a listing of first few files
    SUMMARY=$(echo "$FILES" | head -n 3 | tr '\n' ',' | sed 's/,$//')
    CHANGES="chore: update $SUMMARY and related files"
fi

# Apply the commit
git add .
git commit -m "$CHANGES"
echo -e "${GREEN}✓ Auto-committed: $CHANGES${NC}"
