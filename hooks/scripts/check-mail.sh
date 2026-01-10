#!/bin/bash
# Check agent-mail inbox and alert on new messages
# Triggered after SubagentStop events

set -euo pipefail

# Configuration from environment
PROJECT_KEY="${AGENT_MAIL_PROJECT:-/home/kosta/Documents/Unified_System_Core}"
AGENT_NAME="${AGENT_MAIL_NAME:-VioletCastle}"
MCP_SERVER="${AGENT_MAIL_SERVER:-http://igor-macbook:8765}"

# Try to check mail via HTTP (if server supports it)
check_mail() {
    # Attempt to reach the MCP server's health endpoint first
    if ! curl -fsS --max-time 2 "${MCP_SERVER}/health/liveness" >/dev/null 2>&1; then
        return 1
    fi

    # Server is reachable - output reminder with actual call syntax
    cat << EOF

📬 Agent Mail server is online. Check for new messages:

\`\`\`
mcp__mcp-agent-mail__fetch_inbox(
  project_key="${PROJECT_KEY}",
  agent_name="${AGENT_NAME}",
  limit=5,
  include_bodies=false
)
\`\`\`

EOF
    return 0
}

# Main execution
if check_mail; then
    exit 0
else
    # Server unreachable - silent exit (don't block agent workflow)
    exit 0
fi
