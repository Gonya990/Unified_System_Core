#!/bin/bash
# Cloudflare Tunnel Manager for Alice Skill
# Automatically starts tunnel and displays URL for Yandex Dialogs configuration

set -e

ALICE_PORT=8090
TUNNEL_LOG="/tmp/cloudflare_tunnel.log"
TUNNEL_PID="/tmp/cloudflare_tunnel.pid"

echo "🌐 Cloudflare Tunnel Manager for Alice Skill"
echo "=============================================="

# Check if cloudflared is installed
if ! command -v cloudflared &> /dev/null; then
    echo "❌ cloudflared not found. Installing..."
    
    # Download and install
    curl -L --output /tmp/cloudflared.deb https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
    sudo dpkg -i /tmp/cloudflared.deb
    rm /tmp/cloudflared.deb
    
    echo "✅ cloudflared installed"
fi

# Check if tunnel is already running
if [ -f "$TUNNEL_PID" ]; then
    OLD_PID=$(cat "$TUNNEL_PID")
    if ps -p "$OLD_PID" > /dev/null 2>&1; then
        echo "⚠️  Tunnel already running (PID: $OLD_PID)"
        echo "To restart, run: kill $OLD_PID && $0"
        exit 0
    fi
fi

# Check if Alice Skill is running
if ! curl -s http://localhost:$ALICE_PORT/health > /dev/null 2>&1; then
    echo "⚠️  Warning: Alice Skill (port $ALICE_PORT) is not responding"
    echo "Make sure ai-bot service is running: sudo systemctl status ai-bot"
fi

# Start tunnel in background
echo "🚀 Starting Cloudflare Tunnel..."
cloudflared tunnel --url http://localhost:$ALICE_PORT > "$TUNNEL_LOG" 2>&1 &
TUNNEL_PID_NUM=$!
echo $TUNNEL_PID_NUM > "$TUNNEL_PID"

# Wait for URL to appear in logs
echo "⏳ Waiting for tunnel URL..."
sleep 5

# Extract URL from logs
TUNNEL_URL=$(grep -oP 'https://[a-z0-9-]+\.trycloudflare\.com' "$TUNNEL_LOG" | head -1)

if [ -z "$TUNNEL_URL" ]; then
    echo "❌ Failed to get tunnel URL. Check logs: $TUNNEL_LOG"
    exit 1
fi

echo ""
echo "✅ Tunnel started successfully!"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 CONFIGURATION FOR YANDEX DIALOGS:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Webhook URL: ${TUNNEL_URL}/alice"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📝 Steps to configure:"
echo "1. Go to: https://dialogs.yandex.ru/developer/skills/e6dacdd4-f553-407e-a847-8be932d0d696/draft/settings/main"
echo "2. Set Webhook URL to: ${TUNNEL_URL}/alice"
echo "3. Save and test with: 'Попроси Гоню включить свет'"
echo ""
echo "🔄 Tunnel PID: $TUNNEL_PID_NUM"
echo "📄 Logs: $TUNNEL_LOG"
echo "⏹  To stop: kill $TUNNEL_PID_NUM"
echo ""
echo "✨ Tunnel is running. Press Ctrl+C to view logs..."

# Follow logs
tail -f "$TUNNEL_LOG"
