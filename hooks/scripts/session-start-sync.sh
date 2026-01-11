#!/bin/bash
# Auto-sync with Agent Mail on session start
# Triggered by SessionStart hook

set -euo pipefail

# Load configuration from .env if exists
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

if [[ -f "${PROJECT_ROOT}/.env" ]]; then
    source "${PROJECT_ROOT}/.env"
fi

# Configuration
PROJECT_KEY="${AGENT_MAIL_PROJECT:-/Gonya990/Unified_System_Core}"
AGENT_NAME="${AGENT_MAIL_NAME:-Antigravity}"
MCP_SERVER="${AGENT_MAIL_SERVER:-http://100.110.209.49:8765}"

# Check server health first
check_server() {
    curl -fsS --max-time 3 "${MCP_SERVER}/health/liveness" >/dev/null 2>&1
}

# Output sync reminder for Claude
if check_server; then
    # Load language preference for current agent
    PREF_FILE="${PROJECT_ROOT}/.claude/settings/language-preferences.json"
    if [[ -f "$PREF_FILE" ]]; then
        # Use jq if available, otherwise fallback to simple grep
        if command -v jq >/dev/null 2>&1; then
            USER_NAME=$(jq -r ".agents[\"$AGENT_NAME\"].user // \"default\"" "$PREF_FILE")
            LANG=$(jq -r ".users[\"$USER_NAME\"].output_language // .defaults.output_language" "$PREF_FILE")
            TAG=$(jq -r ".users[\"$USER_NAME\"].translation_tag // .defaults.translation_tag" "$PREF_FILE")
            STRIP=$(jq -r ".users[\"$USER_NAME\"].strip_original // .defaults.strip_original" "$PREF_FILE")
        else
            # Best effort grep
            USER_NAME=$(grep -A 2 "\"$AGENT_NAME\":" "$PREF_FILE" | grep "\"user\":" | cut -d'"' -f4 || echo "default")
            USER_NAME="${USER_NAME:-default}"
            
            if [[ "$USER_NAME" != "default" ]]; then
                LANG=$(grep -A 5 "\"$USER_NAME\":" "$PREF_FILE" | grep "\"output_language\":" | cut -d'"' -f4 || echo "en")
                TAG=$(grep -A 5 "\"$USER_NAME\":" "$PREF_FILE" | grep "\"translation_tag\":" | cut -d'"' -f4 || echo "[translated]")
                STRIP=$(grep -A 5 "\"$USER_NAME\":" "$PREF_FILE" | grep "\"strip_original\":" | cut -d' ' -f6 | tr -d ',' || echo "true")
            else
                LANG="en"
                TAG="[translated]"
                STRIP="true"
            fi
        fi
    else
        USER_NAME="default"
        LANG="en"
        TAG="[translated]"
        STRIP="true"
    fi

    cat << EOF

## Agent Mail Sync Required

Server: ${MCP_SERVER} (online)
Agent: ${AGENT_NAME} (User: ${USER_NAME})
Project: ${PROJECT_KEY}

**MANDATORY Language Protocol**:
- Output Language: **${LANG}**
- Translation Tag: **${TAG}**
- Strip Original: **${STRIP}**
- (Refer to language-preferences.json for details)

Run sync workflow:
\`\`\`
agent_mail_register_agent(
  project_key="${PROJECT_KEY}",
  program="antigravity",
  model="gemini-2.0-pro",
  name="${AGENT_NAME}",
  task_description="Session started - Operating in ${LANG}"
)

agent_mail_fetch_inbox(
  project_key="${PROJECT_KEY}",
  agent_name="${AGENT_NAME}",
  include_bodies=true,
  limit=10
)
\`\`\`

EOF
else
    echo "Agent Mail server offline - skipping sync"
fi
