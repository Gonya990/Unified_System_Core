#!/usr/bin/env bash
# mission_sync.sh
# Enhanced task synchronization using MCP Agent Mail for coordination

HUB_URL="http://100.88.65.71:8765/mcp"
AUTH_TOKEN="antigravity_secret"
PROJECT_KEY="/main"
AGENT_STATE_FILE="$HOME/.cache/agent_comm_state"
TASK_CACHE_DIR="$HOME/.cache/mission_tasks"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

call_mcp_tool() {
    local name=$1
    local args=$2
    curl -sS --http1.1 -X POST "$HUB_URL" \
         -H "Authorization: Bearer $AUTH_TOKEN" \
         -H "Content-Type: application/json" \
         -d "{\"jsonrpc\":\"2.0\",\"id\":\"1\",\"method\":\"tools/call\",\"params\":{\"name\":\"$name\",\"arguments\":$args}}"
}

get_agent_name() {
    if [ -f "$AGENT_STATE_FILE" ]; then
        cat "$AGENT_STATE_FILE"
    else
        echo "Error: Agent not registered. Run 'agent_comm.sh whoami' first." >&2
        exit 1
    fi
}

show_usage() {
    echo "Usage: $0 [status|claim|complete|list]"
    echo ""
    echo "Commands:"
    echo "  status              - Show current task status"
    echo "  claim <task_id>     - Claim a task for execution"
    echo "  complete <task_id>  - Mark task as complete"
    echo "  list                - List available tasks"
    echo ""
    echo "Example:"
    echo "  $0 list"
    echo "  $0 claim deployment-123"
    echo "  $0 complete deployment-123"
}

format_message() {
    local json_result=$1
    echo "$json_result" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    if data.get('result', {}).get('isError'):
        print('❌ Error:', data['result']['content'][0]['text'])
    else:
        content = data.get('result', {}).get('structuredContent', {})
        print('✅ Success')
        if 'deliveries' in content:
            print(f\"   Delivered to {len(content['deliveries'])} recipient(s)\")
except Exception as e:
    print(f'Error parsing response: {e}')
    sys.exit(1)
"
}

list_tasks() {
    AGENT_NAME=$(get_agent_name)
    echo -e "${BLUE}📋 Fetching tasks from hub...${NC}"
    
    result=$(call_mcp_tool "fetch_inbox" "{\"project_key\": \"$PROJECT_KEY\", \"agent_name\": \"$AGENT_NAME\", \"limit\": 20}")
    
    echo "$result" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    content = data.get('result', {}).get('structuredContent', {})
    messages = content.get('result', []) if isinstance(content, dict) else []
    
    # Filter for task messages
    tasks = [m for m in messages if '[TASK]' in m.get('subject', '')]
    
    if not tasks:
        print('No tasks found.')
    else:
        print(f'\nFound {len(tasks)} task(s):\n')
        for msg in tasks:
            print(f\"• [{msg.get('id')}] {msg.get('subject', 'No subject')}\")
            print(f\"  From: {msg.get('from', 'Unknown')}\")
            print(f\"  Priority: {msg.get('importance', 'normal')}\")
            print()
except Exception as e:
    print(f'Error listing tasks: {e}')
    sys.exit(1)
"
}

claim_task() {
    local task_id=$1
    AGENT_NAME=$(get_agent_name)
    
    echo -e "${YELLOW}🏷️  Claiming task $task_id...${NC}"
    
    result=$(call_mcp_tool "send_message" "{
        \"project_key\": \"$PROJECT_KEY\",
        \"sender_name\": \"$AGENT_NAME\",
        \"to\": [\"TaskCoordinator\"],
        \"subject\": \"[CLAIM] Task $task_id\",
        \"body_md\": \"Agent **$AGENT_NAME** is claiming task \\\`$task_id\\\` for execution.\",
        \"importance\": \"high\"
    }")
    
    format_message "$result"
}

complete_task() {
    local task_id=$1
    AGENT_NAME=$(get_agent_name)
    
    echo -e "${GREEN}✅ Marking task $task_id as complete...${NC}"
    
    result=$(call_mcp_tool "send_message" "{
        \"project_key\": \"$PROJECT_KEY\",
        \"sender_name\": \"$AGENT_NAME\",
        \"to\": [\"TaskCoordinator\"],
        \"subject\": \"[COMPLETE] Task $task_id\",
        \"body_md\": \"## Task Complete\n\nAgent **$AGENT_NAME** has successfully completed task \\\`$task_id\\\`.\n\n**Completed:** $(date -u +%Y-%m-%dT%H:%M:%SZ)\",
        \"importance\": \"high\",
        \"ack_required\": true
    }")
    
    format_message "$result"
}

show_status() {
    AGENT_NAME=$(get_agent_name)
    
    echo -e "${BLUE}📊 Mission Status${NC}"
    echo "================================"
    echo "Agent: $AGENT_NAME"
    echo "Project: $PROJECT_KEY"
    echo "Hub: $HUB_URL"
    echo ""
    
    # Check for pending acknowledgements
    result=$(call_mcp_tool "fetch_inbox" "{\"project_key\": \"$PROJECT_KEY\", \"agent_name\": \"$AGENT_NAME\", \"limit\": 5}")
    
    echo "$result" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    content = data.get('result', {}).get('structuredContent', {})
    messages = content.get('result', []) if isinstance(content, dict) else []
    
    pending = [m for m in messages if m.get('ack_required') and m.get('kind') == 'to']
    tasks = [m for m in messages if '[TASK]' in m.get('subject', '')]
    
    print(f'📬 Inbox: {len(messages)} message(s)')
    print(f'⚠️  Pending ACKs: {len(pending)}')
    print(f'📋 Active Tasks: {len(tasks)}')
    print()
    
    if pending:
        print('Pending acknowledgements:')
        for msg in pending[:3]:
            print(f\"  • {msg.get('subject', 'No subject')} (from {msg.get('from')})\")
except Exception as e:
    print(f'Error checking status: {e}')
"
}

# Main command processing
if [ "$#" -lt 1 ]; then
    show_usage
    exit 1
fi

# Ensure cache directory exists
mkdir -p "$TASK_CACHE_DIR"

COMMAND=$1
shift

case "$COMMAND" in
    status)
        show_status
        ;;
    list)
        list_tasks
        ;;
    claim)
        if [ -z "$1" ]; then
            echo "Error: Task ID required"
            show_usage
            exit 1
        fi
        claim_task "$1"
        ;;
    complete)
        if [ -z "$1" ]; then
            echo "Error: Task ID required"
            show_usage
            exit 1
        fi
        complete_task "$1"
        ;;
    *)
        show_usage
        exit 1
        ;;
esac
