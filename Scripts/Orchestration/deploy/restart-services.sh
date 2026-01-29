#!/bin/bash
# Restart Services - Restart Docker containers and MCP server
# Run AFTER remote-update.sh

set -euo pipefail

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

REMOTE_HOST="${REMOTE_HOST:-gonya@100.110.209.49}"
REMOTE_PATH="${REMOTE_PATH:-/home/gonya/Unified_System}"

echo -e "${GREEN}Restart Services${NC}"
echo "=========================================="

SERVICE="${1:-all}"

restart_bot() {
    echo -e "\n${YELLOW}Restarting AI Bot...${NC}"
    tailscale ssh "$REMOTE_HOST" "
        cd $REMOTE_PATH/Projects/AI_Core
        docker compose --profile local down --remove-orphans || true
        docker compose --profile local build ai-bot-local
        docker compose --profile local up -d ai-bot-local watchtower
    "
    echo -e "${GREEN}AI Bot restarted.${NC}"
}

restart_mcp() {
    echo -e "\n${YELLOW}Restarting MCP Agent Mail...${NC}"
    tailscale ssh "$REMOTE_HOST" "
        pkill -f 'mcp_agent_mail' || true
        cd $REMOTE_PATH
        nohup bash Scripts/External/start_mail_server.sh > mcp_mail.log 2>&1 &
        sleep 2
        pgrep -f 'mcp_server' && echo 'MCP server started' || echo 'MCP server failed to start'
    " || echo "Background job started."
    echo -e "${GREEN}MCP Mail restarted.${NC}"
}

case "$SERVICE" in
    bot)
        restart_bot
        ;;
    mcp)
        restart_mcp
        ;;
    all)
        restart_bot
        restart_mcp
        ;;
    *)
        echo "Usage: $0 [bot|mcp|all]"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}Services restart complete.${NC}"
