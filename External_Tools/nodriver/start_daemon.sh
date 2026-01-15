#!/bin/bash
# start_daemon.sh - Start nodriver daemon with UV

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Source UV if needed
if ! command -v uv &> /dev/null; then
    source ~/.local/bin/env 2>/dev/null || true
fi

# Check if UV is available
if ! command -v uv &> /dev/null; then
    echo "❌ UV not found. Install with: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# Check if Chrome is running with debug port
if ! curl -s http://localhost:9222/json/version &>/dev/null; then
    echo "⚠️  Chrome not running with remote debugging."
    echo "   Start Chrome with:"
    echo '   "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --remote-debugging-port=9222'
    echo ""
    read -p "Start Chrome now? [y/N] " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --remote-debugging-port=9222 &
        sleep 2
    fi
fi

cd "$SCRIPT_DIR"
echo "🚀 Starting nodriver daemon in background..."
uv run python nodriver_daemon.py > /tmp/nodriver.log 2>&1 &
echo "✓ Daemon started (PID $!)"
sleep 2
