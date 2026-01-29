#!/bin/bash
# Unified Sync - Safe orchestration of sync operations
# Usage: ./sync.sh [git|tasks|all]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

show_help() {
    echo "Unified Sync"
    echo ""
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  git      Sync git repository (pull/push)"
    echo "  tasks    Sync Beads task board"
    echo "  all      Run all syncs (default)"
    echo ""
    echo "Deployment (separate from sync):"
    echo "  deploy/remote-update.sh     Pull code on remote server"
    echo "  deploy/restart-services.sh  Restart services"
}

sync_git() {
    bash "$SCRIPT_DIR/sync/git-sync.sh"
}

sync_tasks() {
    bash "$SCRIPT_DIR/sync/tasks-sync.sh"
}

CMD="${1:-all}"

case "$CMD" in
    git)
        sync_git
        ;;
    tasks)
        sync_tasks
        ;;
    all)
        echo -e "${GREEN}Running full sync...${NC}\n"
        sync_git
        echo ""
        sync_tasks
        echo ""
        echo -e "${GREEN}========================================${NC}"
        echo -e "${GREEN}All syncs complete.${NC}"
        echo -e "${YELLOW}To deploy to remote, run:${NC}"
        echo "  bash Scripts/Orchestration/deploy/remote-update.sh"
        ;;
    -h|--help|help)
        show_help
        ;;
    *)
        echo "Unknown command: $CMD"
        show_help
        exit 1
        ;;
esac
