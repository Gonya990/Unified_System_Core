#!/usr/bin/env bash
# opencode_api.sh - Interact with OpenCode server via REST API
# Usage: ./opencode_api.sh <command> [args]

OPENCODE_URL="${OPENCODE_URL:-http://100.110.209.49:4096}"
SESSION_FILE="$HOME/.cache/opencode_session"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

show_usage() {
    echo "OpenCode API Client"
    echo ""
    echo "Usage: $0 <command> [args]"
    echo ""
    echo "Commands:"
    echo "  health              - Check server health"
    echo "  sessions            - List all sessions"
    echo "  new [path]          - Create new session"
    echo "  chat <message>      - Send message to current session"
    echo "  ask <message>       - Send message and get response (one-liner)"
    echo ""
    echo "Environment:"
    echo "  OPENCODE_URL        - Server URL (default: http://100.110.209.49:4096)"
}

cmd_health() {
    curl -s "$OPENCODE_URL/global/health" | jq .
}

cmd_sessions() {
    curl -s "$OPENCODE_URL/session" | jq .
}

cmd_new() {
    local path="${1:-/home/gonya}"
    local response=$(curl -s -X POST "$OPENCODE_URL/session" \
        -H "Content-Type: application/json" \
        -d "{\"path\":\"$path\"}")
    
    local session_id=$(echo "$response" | jq -r '.id')
    echo "$session_id" > "$SESSION_FILE"
    echo -e "${GREEN}Created session:${NC} $session_id"
    echo "$response" | jq .
}

get_session() {
    if [ -f "$SESSION_FILE" ]; then
        cat "$SESSION_FILE"
    else
        echo ""
    fi
}

cmd_chat() {
    local message="$1"
    local session_id=$(get_session)
    
    if [ -z "$session_id" ]; then
        echo "No active session. Create one with: $0 new"
        exit 1
    fi
    
    curl -s -X POST "$OPENCODE_URL/session/$session_id/message" \
        -H "Content-Type: application/json" \
        -d "{\"parts\":[{\"type\":\"text\",\"text\":\"$message\"}]}" | jq .
}

cmd_ask() {
    local message="$1"
    local session_id=$(get_session)
    
    if [ -z "$session_id" ]; then
        # Auto-create session
        local response=$(curl -s -X POST "$OPENCODE_URL/session" \
            -H "Content-Type: application/json" \
            -d '{"path":"/home/gonya"}')
        session_id=$(echo "$response" | jq -r '.id')
        echo "$session_id" > "$SESSION_FILE"
        echo -e "${BLUE}Auto-created session:${NC} $session_id"
    fi
    
    local response=$(curl -s -X POST "$OPENCODE_URL/session/$session_id/message" \
        -H "Content-Type: application/json" \
        -d "{\"parts\":[{\"type\":\"text\",\"text\":\"$message\"}]}")
    
    # Extract text response
    echo "$response" | jq -r '.parts[] | select(.type=="text") | .text'
}

# Main
if [ "$#" -lt 1 ]; then
    show_usage
    exit 1
fi

COMMAND=$1
shift

case "$COMMAND" in
    health)   cmd_health ;;
    sessions) cmd_sessions ;;
    new)      cmd_new "$@" ;;
    chat)     cmd_chat "$*" ;;
    ask)      cmd_ask "$*" ;;
    *)        show_usage; exit 1 ;;
esac
