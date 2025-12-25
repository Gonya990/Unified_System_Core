#!/usr/bin/env bash
# Wrapper for mcp_agent_mail server
MAIL_DIR="/Users/macbook/Documents/Unified_System/External_Tools/Stack/mcp_agent_mail"

if [ ! -d "$MAIL_DIR" ]; then
    echo "Error: mcp_agent_mail not found in $MAIL_DIR"
    exit 1
fi

cd "$MAIL_DIR" || exit 1
bash scripts/run_server_with_token.sh "$@"
