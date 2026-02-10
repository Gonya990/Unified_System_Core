#!/bin/bash

# Multi-Admin Bot Manager Script
# Manages Igor and Kostya bot instances via PM2

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_header() {
    echo -e "${BLUE}=== $1 ===${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

check_pm2() {
    if ! command -v pm2 &> /dev/null; then
        print_error "PM2 is not installed"
        echo "Install with: npm install -g pm2"
        exit 1
    fi
    print_success "PM2 found: $(pm2 --version)"
}

check_env_files() {
    print_header "Checking configuration files"

    if [[ ! -f "$PROJECT_ROOT/.env.igor" ]]; then
        print_error ".env.igor not found"
        exit 1
    fi
    print_success ".env.igor exists"
}

start_bots() {
    print_header "Starting both bots with PM2"

    cd "$PROJECT_ROOT"

    if pm2 start ecosystem.config.js; then
        print_success "Both bots started"
        sleep 2
        pm2 status
    else
        print_error "Failed to start bots"
        exit 1
    fi
}

stop_bots() {
    print_header "Stopping bots"
    pm2 stop all
    print_success "All bots stopped"
}

restart_bots() {
    print_header "Restarting bots"
    pm2 restart all
    print_success "All bots restarted"
}

status() {
    print_header "Bot Status"
    pm2 status
}

logs_igor() {
    print_header "Igor's Bot Logs (last 50 lines)"
    pm2 logs ai-bot-igor --nostream --lines 50
}

logs_kostya() {
    print_header "Kostya's Bot Logs (last 50 lines)"
    pm2 logs ai-bot-kostya --nostream --lines 50
}

monit() {
    print_header "Live Monitoring (press 'q' to exit)"
    pm2 monit
}

health_check() {
    print_header "Health Checks"

    echo "Igor's bot health (port 8095):"
    curl -s http://localhost:8095/health 2>/dev/null | jq . || echo "  - Unreachable"

    echo ""
    echo "Kostya's bot health (port 8097):"
    curl -s http://localhost:8097/health 2>/dev/null | jq . || echo "  - Unreachable"
}

setup_autostart() {
    print_header "Setting up auto-start on boot"

    pm2 startup
    pm2 save

    print_success "Auto-start enabled"
    echo "To disable: pm2 unstartup"
}

cleanup() {
    print_header "Cleanup (removing from PM2)"

    pm2 delete all
    print_success "Removed from PM2"
}

# Main
case "${1:-}" in
    start)
        check_pm2
        check_env_files
        start_bots
        ;;
    stop)
        check_pm2
        stop_bots
        ;;
    restart)
        check_pm2
        restart_bots
        ;;
    status)
        check_pm2
        status
        ;;
    logs-igor)
        check_pm2
        logs_igor
        ;;
    logs-kostya)
        check_pm2
        logs_kostya
        ;;
    logs)
        check_pm2
        echo "Igor's logs:"
        pm2 logs ai-bot-igor --nostream --lines 20
        echo ""
        echo "Kostya's logs:"
        pm2 logs ai-bot-kostya --nostream --lines 20
        ;;
    monit)
        check_pm2
        monit
        ;;
    health)
        health_check
        ;;
    setup-autostart)
        check_pm2
        setup_autostart
        ;;
    cleanup)
        check_pm2
        cleanup
        ;;
    *)
        cat << 'EOF'
Multi-Admin Bot Manager

Usage: ./scripts/manage-bots.sh <command>

Commands:
  start              Start both bots (Igor + Kostya)
  stop               Stop both bots
  restart            Restart both bots
  status             Show bot status
  logs-igor          Show Igor's bot logs (last 50 lines)
  logs-kostya        Show Kostya's bot logs (last 50 lines)
  logs               Show both bots' logs (last 20 lines each)
  monit              Live monitoring dashboard
  health             Check health endpoints
  setup-autostart    Enable auto-start on boot
  cleanup            Remove from PM2 (no auto-start)

Examples:
  ./scripts/manage-bots.sh start
  ./scripts/manage-bots.sh monit
  ./scripts/manage-bots.sh logs-igor
  ./scripts/manage-bots.sh health

Configuration:
  Igor:   .env.igor (ADMIN_ID: 708531393, Token: 8518131338:...)
  Kostya: .env.kostya (ADMIN_ID: 578363419, Token: 7998292224:...)

Ports:
  Igor's health:   http://localhost:8095/health
  Kostya's health: http://localhost:8097/health
  Igor's dashboard:   http://localhost:8096/dashboard
  Kostya's dashboard: http://localhost:8098/dashboard
EOF
        exit 0
        ;;
esac
