#!/bin/bash
# Sync Beads Status to Agent Mail
# Usage: ./beads_status_hook.sh <issue_id> <status> <notes>

PROJECT_KEY="/home/kosta/Documents/Unified_System_Core"
AGENT_NAME="VioletCastle"
HUB_URL="http://100.110.209.49:8765/mcp"
AUTH_TOKEN="${AGENT_HUB_TOKEN:-antigravity_secret}"

ISSUE_ID=$1
STATUS=$2
NOTES=$3

# Extract title: it's the first line starting with ID: Title
TITLE=$(bd show "$ISSUE_ID" 2>/dev/null | grep "^$ISSUE_ID:" | head -n 1 | sed "s/^$ISSUE_ID: //")

if [ -z "$TITLE" ]; then
    TITLE="Unknown Task"
fi

TASK_DESC="Beads Update: $ISSUE_ID is now $STATUS - $TITLE. $NOTES"

# Update Agent Status
curl -sS --http1.1 -X POST "$HUB_URL" \
     -H "Authorization: Bearer $AUTH_TOKEN" \
     -H "Content-Type: application/json" \
     -d "{\"jsonrpc\":\"2.0\",\"id\":\"1\",\"method\":\"tools/call\",\"params\":{\"name\":\"register_agent\",\"arguments\":{\"project_key\": \"$PROJECT_KEY\", \"program\": \"claude-code\", \"model\": \"opus-4.5\", \"name\": \"$AGENT_NAME\", \"task_description\": \"$TASK_DESC\"}}}" > /dev/null

echo "✅ Status synced to Agent Mail: $TASK_DESC"
