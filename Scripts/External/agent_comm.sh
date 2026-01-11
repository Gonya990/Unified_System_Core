#!/usr/bin/env bash
# agent_comm.sh
# Local wrapper to interact with the Centralized Agent Mail Hub on igor-gaming-1

HUB_URL="http://100.110.209.49:8765/mcp"
AUTH_TOKEN="${AGENT_HUB_TOKEN:-c2bb2cf043ec2ae56a0dec69024e6129eb5cde36a22bddb93afcfa2e71e72afb}"
PROJECT_KEY="/Gonya990/Unified_System_Core" # Logical project name
AGENT_STATE_FILE="$HOME/.cache/agent_comm_state"

call_mcp_tool() {
    local name=$1
    local args=$2
    curl -sS --http1.1 -X POST "$HUB_URL" \
         -H "Authorization: Bearer $AUTH_TOKEN" \
         -H "Content-Type: application/json" \
         -d "{\"jsonrpc\":\"2.0\",\"id\":\"1\",\"method\":\"tools/call\",\"params\":{\"name\":\"$name\",\"arguments\":$args}}"
}

get_agent_name() {
    # Check if we have a registered agent name
    if [ -f "$AGENT_STATE_FILE" ]; then
        cat "$AGENT_STATE_FILE"
    else
        # Register a new agent and store the name
        mkdir -p "$(dirname "$AGENT_STATE_FILE")"
        local name="${AGENT_MAIL_NAME:-}"
        local model="${AGENT_MODEL:-gemini-2.0-pro}"
        local reg_args="{\"project_key\": \"$PROJECT_KEY\", \"program\": \"antigravity\", \"model\": \"$model\"}"
        if [ -n "$name" ]; then
            reg_args="{\"project_key\": \"$PROJECT_KEY\", \"program\": \"antigravity\", \"model\": \"$model\", \"name\": \"$name\"}"
        fi
        
        call_mcp_tool "ensure_project" "{\"human_key\": \"$PROJECT_KEY\"}" > /dev/null
        local result=$(call_mcp_tool "register_agent" "$reg_args")
        local agent_name=$(echo "$result" | python3 -c "import sys, json; data = json.load(sys.stdin); print(data.get('result', {}).get('structuredContent', {}).get('name', ''))" 2>/dev/null)
        
        if [ -n "$agent_name" ]; then
            echo "$agent_name" > "$AGENT_STATE_FILE"
            echo "$agent_name"
        else
            echo "Error: Failed to register agent" >&2
            exit 1
        fi
    fi
}

show_usage() {
    echo "Usage: $0 [send|inbox|whoami]"
    echo "Examples:"
    echo "  $0 send <recipient> \"<message>\""
    echo "  $0 inbox"
    echo "  $0 whoami"
}

if [ "$#" -lt 1 ]; then
    show_usage
    exit 1
fi

COMMAND=$1
shift

case "$COMMAND" in
    send)
        RECIPIENT=$1
        BODY=$2
        AGENT_NAME=$(get_agent_name)
        
        # Send message
        call_mcp_tool "send_message" "{\"project_key\": \"$PROJECT_KEY\", \"sender_name\": \"$AGENT_NAME\", \"to\": [\"$RECIPIENT\"], \"subject\": \"Agent Message\", \"body_md\": \"$BODY\"}"
        ;;
    inbox)
        AGENT_NAME=$(get_agent_name)
        call_mcp_tool "fetch_inbox" "{\"project_key\": \"$PROJECT_KEY\", \"agent_name\": \"$AGENT_NAME\"}"
        ;;
    whoami)
        AGENT_NAME=$(get_agent_name)
        echo "Agent: $AGENT_NAME"
        echo "Project: $PROJECT_KEY"
        echo "Hub: $HUB_URL"
        ;;
    *)
        show_usage
        exit 1
        ;;
esac
