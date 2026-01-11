#!/bin/bash
# Check agent-mail inbox and alert on new messages
# Triggered after Task tool use (subagent completions)

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

# Track last check time to avoid spamming
LAST_CHECK_FILE="/tmp/agent-mail-last-check-${AGENT_NAME}"
MIN_CHECK_INTERVAL=300  # 5 minutes between reminders

should_check() {
    if [[ ! -f "${LAST_CHECK_FILE}" ]]; then
        return 0
    fi

    local last_check=$(cat "${LAST_CHECK_FILE}")
    local now=$(date +%s)
    local elapsed=$((now - last_check))

    [[ ${elapsed} -ge ${MIN_CHECK_INTERVAL} ]]
}

update_check_time() {
    date +%s > "${LAST_CHECK_FILE}"
}

# Check server health
check_server() {
    curl -fsS --max-time 2 "${MCP_SERVER}/health/liveness" >/dev/null 2>&1
}

# Main execution
if ! should_check; then
    exit 0
fi

if check_server; then
    update_check_time
    cat << EOF

## Agent Mail Reminder

Check for urgent messages:
\`\`\`
agent_mail_fetch_inbox(
  project_key="${PROJECT_KEY}",
  agent_name="${AGENT_NAME}",
  urgent_only=true,
  limit=5,
  include_bodies=true
)
\`\`\`

EOF
fi

exit 0
