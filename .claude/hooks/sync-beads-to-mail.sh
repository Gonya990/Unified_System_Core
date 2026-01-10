#!/bin/bash
# Sync Beads Status to Agent Mail
# Usage: ./sync-beads-to-mail.sh <issue_id> <status> <notes>

PROJECT_KEY="/home/kosta/Documents/Unified_System_Core"
AGENT_NAME="VioletCastle" # Persistent identity from .env

ISSUE_ID=$1
STATUS=$2
NOTES=$3

TASK_DESC="Beads Update: $ISSUE_ID is now $STATUS. $NOTES"

# Use register_agent to update the billboard status
# This is the most efficient way to 'broadcast' current task
mcp__mcp-agent-mail__register_agent(
  project_key="$PROJECT_KEY",
  program="claude-code",
  model="opus-4.5",
  name="$AGENT_NAME",
  task_description="$TASK_DESC"
)
