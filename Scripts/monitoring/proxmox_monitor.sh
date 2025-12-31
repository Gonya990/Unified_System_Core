#!/bin/bash
# Proxmox Monitoring Script for N8N Integration
# Скрипт мониторинга Proxmox для интеграции с N8N
# 
# This script can be called from N8N as a webhook or scheduled trigger
# to monitor Proxmox cluster health and send alerts.

set -e

# Configuration
PVE_HOST="${PVE_HOST:-pve-antigravity-1}"
TELEGRAM_BOT_TOKEN="${TELEGRAM_BOT_TOKEN:-}"
TELEGRAM_CHAT_ID="${TELEGRAM_CHAT_ID:-}"

# Colors and formatting
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Output format (json for N8N, text for CLI)
OUTPUT_FORMAT="${OUTPUT_FORMAT:-text}"

# Function to send Telegram alert
send_telegram_alert() {
    local message="$1"
    local severity="${2:-info}"
    
    if [ -n "$TELEGRAM_BOT_TOKEN" ] && [ -n "$TELEGRAM_CHAT_ID" ]; then
        local emoji="ℹ️"
        case "$severity" in
            critical) emoji="🔴" ;;
            warning) emoji="⚠️" ;;
            ok) emoji="✅" ;;
        esac
        
        curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
            -d "chat_id=${TELEGRAM_CHAT_ID}" \
            -d "text=${emoji} ${message}" \
            -d "parse_mode=HTML" > /dev/null
    fi
}

# Function to check Proxmox health via SSH
check_pve_health() {
    local result=$(ssh -o ConnectTimeout=10 "$PVE_HOST" 'cat /proc/uptime && free -m && df -h /' 2>/dev/null)
    
    if [ $? -ne 0 ]; then
        echo "ERROR: Cannot connect to $PVE_HOST"
        send_telegram_alert "Proxmox ($PVE_HOST) недоступен!" "critical"
        return 1
    fi
    
    echo "$result"
}

# Function to get VM/CT status
get_vm_status() {
    local result=$(ssh -o ConnectTimeout=10 "$PVE_HOST" 'qm list 2>/dev/null; echo "---"; pct list 2>/dev/null' 2>/dev/null)
    
    if [ $? -ne 0 ]; then
        echo "ERROR: Cannot get VM status from $PVE_HOST"
        return 1
    fi
    
    echo "$result"
}

# Function to check Tailscale status
check_tailscale() {
    local result=$(ssh -o ConnectTimeout=10 "$PVE_HOST" 'tailscale status --json 2>/dev/null' 2>/dev/null)
    
    if [ $? -ne 0 ]; then
        echo "ERROR: Cannot get Tailscale status"
        return 1
    fi
    
    echo "$result"
}

# Function to generate JSON report for N8N
generate_json_report() {
    local uptime=$(ssh -o ConnectTimeout=10 "$PVE_HOST" 'cat /proc/uptime | cut -d" " -f1' 2>/dev/null)
    local load=$(ssh -o ConnectTimeout=10 "$PVE_HOST" 'cat /proc/loadavg | cut -d" " -f1-3' 2>/dev/null)
    local mem_info=$(ssh -o ConnectTimeout=10 "$PVE_HOST" 'free -m | grep Mem' 2>/dev/null)
    local disk_info=$(ssh -o ConnectTimeout=10 "$PVE_HOST" 'df -h / | tail -1' 2>/dev/null)
    
    local mem_total=$(echo "$mem_info" | awk '{print $2}')
    local mem_used=$(echo "$mem_info" | awk '{print $3}')
    local mem_pct=$((mem_used * 100 / mem_total))
    
    local disk_used_pct=$(echo "$disk_info" | awk '{print $5}' | tr -d '%')
    
    local status="ok"
    if [ "$mem_pct" -gt 90 ] || [ "$disk_used_pct" -gt 90 ]; then
        status="critical"
    elif [ "$mem_pct" -gt 80 ] || [ "$disk_used_pct" -gt 80 ]; then
        status="warning"
    fi
    
    cat << EOF
{
    "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
    "host": "$PVE_HOST",
    "status": "$status",
    "uptime_seconds": ${uptime:-0},
    "load_average": "$load",
    "memory": {
        "total_mb": ${mem_total:-0},
        "used_mb": ${mem_used:-0},
        "used_percent": ${mem_pct:-0}
    },
    "disk": {
        "used_percent": ${disk_used_pct:-0}
    }
}
EOF
}

# Main execution
main() {
    case "${1:-status}" in
        status)
            if [ "$OUTPUT_FORMAT" = "json" ]; then
                generate_json_report
            else
                echo "=== Proxmox Health Check ==="
                echo "Host: $PVE_HOST"
                echo ""
                check_pve_health
            fi
            ;;
        vms)
            get_vm_status
            ;;
        tailscale)
            check_tailscale
            ;;
        alert)
            local report=$(generate_json_report)
            local status=$(echo "$report" | grep -o '"status": "[^"]*"' | cut -d'"' -f4)
            
            if [ "$status" = "critical" ]; then
                send_telegram_alert "🚨 Proxmox Critical: CPU/RAM/Disk overload detected!" "critical"
            elif [ "$status" = "warning" ]; then
                send_telegram_alert "⚠️ Proxmox Warning: Resource usage is high" "warning"
            fi
            
            echo "$report"
            ;;
        json)
            generate_json_report
            ;;
        *)
            echo "Usage: $0 {status|vms|tailscale|alert|json}"
            echo ""
            echo "Commands:"
            echo "  status    - Show system health (default)"
            echo "  vms       - List VMs and containers"
            echo "  tailscale - Show Tailscale status"
            echo "  alert     - Check and send Telegram alerts if needed"
            echo "  json      - Output status as JSON for N8N"
            exit 1
            ;;
    esac
}

main "$@"
