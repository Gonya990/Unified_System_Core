#!/usr/bin/env bash
# mission_sync.sh
# Local wrapper to sync Beads tasks with the central mission state on igor-gaming-1

HUB_IP="100.88.65.71"
BEADS_PATH="/home/ubuntu/mission_state" # Path on the hub

show_usage() {
    echo "Usage: $0 [pull|push]"
}

if [ "$#" -lt 1 ]; then
    show_usage
    exit 1
fi

COMMAND=$1

case "$COMMAND" in
    pull)
        echo "📥 Pulling latest mission state from $HUB_IP..."
        rsync -avz ubuntu@$HUB_IP:$BEADS_PATH/tasks.jsonl ./tasks.jsonl
        ;;
    push)
        echo "📤 Pushing mission state to $HUB_IP..."
        rsync -avz ./tasks.jsonl ubuntu@$HUB_IP:$BEADS_PATH/tasks.jsonl
        ;;
    *)
        show_usage
        exit 1
        ;;
esac
