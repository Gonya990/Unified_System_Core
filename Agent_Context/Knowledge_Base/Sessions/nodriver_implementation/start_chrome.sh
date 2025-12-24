#!/bin/bash
# start_chrome.sh - Start Chrome with Remote Debugging enabled
# This allows nodriver daemon to connect and control the browser

# Load config from .env if available
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ -f "$SCRIPT_DIR/.env" ]; then
    source "$SCRIPT_DIR/.env"
elif [ -f ~/.nodriver.env ]; then
    source ~/.nodriver.env
fi

# Configuration (can be overridden via .env)
CHROME_EXECUTABLE="${CHROME_EXECUTABLE:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
CHROME_DEBUG_PORT="${CHROME_DEBUG_PORT:-9222}"

# Check if Chrome is already running with debug port
if curl -s "http://localhost:$CHROME_DEBUG_PORT/json/version" &>/dev/null; then
    echo "✅ Chrome already running with remote debugging on port $CHROME_DEBUG_PORT"
    curl -s "http://localhost:$CHROME_DEBUG_PORT/json/version" | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'   Browser: {d.get(\"Browser\",\"?\")}')"
    exit 0
fi

# Check if Chrome executable exists
if [ ! -f "$CHROME_EXECUTABLE" ]; then
    echo "❌ Chrome not found at: $CHROME_EXECUTABLE"
    echo "   Set CHROME_EXECUTABLE in ~/.nodriver.env"
    exit 1
fi

echo "🚀 Starting Chrome with remote debugging..."
echo "   Port: $CHROME_DEBUG_PORT"
echo "   Executable: $CHROME_EXECUTABLE"
echo ""

# Start Chrome in background
"$CHROME_EXECUTABLE" \
    --remote-debugging-port="$CHROME_DEBUG_PORT" \
    --remote-allow-origins=* \
    &>/dev/null &

# Wait for Chrome to start
sleep 2

# Verify it started
if curl -s "http://localhost:$CHROME_DEBUG_PORT/json/version" &>/dev/null; then
    echo "✅ Chrome started successfully!"
    echo ""
    echo "Next steps:"
    echo "  1. Start daemon: ./start_daemon.sh"
    echo "  2. Use CLI:      ./ndc status"
else
    echo "⚠️  Chrome may not have started correctly."
    echo "   Try running manually:"
    echo "   \"$CHROME_EXECUTABLE\" --remote-debugging-port=$CHROME_DEBUG_PORT"
fi
