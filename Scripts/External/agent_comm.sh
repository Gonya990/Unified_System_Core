#!/usr/bin/env bash
# agent_comm.sh
# Local wrapper to interact with the Centralized Agent Mail Hub on igor-gaming-1

HUB_URL="http://100.88.65.71:8765"
AUTH_TOKEN="antigravity_secret" # Should be moved to .env in production

show_usage() {
    echo "Usage: $0 [send|check|inbox|outbox] [args...]"
    echo "Example: $0 send kostya \"Hello from Antigravity\""
}

if [ "$#" -lt 1 ]; then
    show_usage
    exit 1
fi

COMMAND=$1
shift

case "$COMMAND" in
    send)
        # Simple send via curl to the hub
        RECIPIENT=$1
        MESSAGE=$2
        curl -X POST "$HUB_URL/messages/send" \
             -H "Authorization: Bearer $AUTH_TOKEN" \
             -H "Content-Type: application/json" \
             -d "{\"recipient\": \"$RECIPIENT\", \"body\": \"$MESSAGE\"}"
        ;;
    check|inbox)
        curl -X GET "$HUB_URL/messages/inbox" \
             -H "Authorization: Bearer $AUTH_TOKEN"
        ;;
    outbox)
        curl -X GET "$HUB_URL/messages/outbox" \
             -H "Authorization: Bearer $AUTH_TOKEN"
        ;;
    *)
        show_usage
        exit 1
        ;;
esac
