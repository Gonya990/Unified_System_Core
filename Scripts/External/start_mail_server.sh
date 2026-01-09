#!/usr/bin/env bash
# Wrapper for mcp_agent_mail server
# Determine script directory and correct relative path
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
MAIL_DIR="$SCRIPT_DIR/../../External_Tools/Stack/mcp_agent_mail"

if [ ! -d "$MAIL_DIR" ]; then
    echo "Error: mcp_agent_mail not found in $MAIL_DIR"
    exit 1
fi

# Set known token for Vibranium System compatibility
export HTTP_BEARER_TOKEN="c2bb2cf043ec2ae56a0dec69024e6129eb5cde36a22bddb93afcfa2e71e72afb"

cd "$MAIL_DIR" || exit 1
bash scripts/run_server_with_token.sh "$@"
