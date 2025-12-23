#!/bin/bash
# Start/Stop AI Telegram Bot in Debug Mode
# Usage: ./start-debug-telegram.sh [start|stop|restart|status|logs]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

BOT_NAME="ai-telegram-bot"
PID_FILE="/tmp/${BOT_NAME}.pid"
LOG_FILE="${SCRIPT_DIR}/logs/bot_debug.log"

# Create logs directory if not exists
mkdir -p "${SCRIPT_DIR}/logs"

# Load environment from .env if exists
if [ -f ".env" ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Default environment variables
export TELEGRAM_BOT_TOKEN="${TELEGRAM_BOT_TOKEN:-}"
export INFERENCE_BASE_URL="${INFERENCE_BASE_URL:-http://localhost:11434}"
export MODEL_NAME="${MODEL_NAME:-llama3.2}"
export LOG_LEVEL="${LOG_LEVEL:-DEBUG}"
export CONFIG_PATH="${CONFIG_PATH:-/tmp/bot_config.json}"

start_bot() {
    if [ -f "$PID_FILE" ] && kill -0 "$(cat $PID_FILE)" 2>/dev/null; then
        echo "❌ Bot is already running (PID: $(cat $PID_FILE))"
        return 1
    fi

    if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
        echo "❌ Error: TELEGRAM_BOT_TOKEN not set"
        echo "   Set it in .env file or export it manually"
        return 1
    fi

    echo "=========================================="
    echo "🚀 Starting AI Telegram Bot (Debug Mode)"
    echo "=========================================="
    echo "Token: ${TELEGRAM_BOT_TOKEN:0:10}..."
    echo "Inference URL: $INFERENCE_BASE_URL"
    echo "Model: $MODEL_NAME"
    echo "Log Level: $LOG_LEVEL"
    echo "Log File: $LOG_FILE"
    echo "=========================================="

    # Check if uv is available
    if command -v uv &> /dev/null; then
        echo "📦 Using uv package manager"
        uv sync 2>/dev/null || uv pip install -e . 2>/dev/null || true
        nohup uv run python -m src.main >> "$LOG_FILE" 2>&1 &
    else
        echo "📦 Using pip (uv not found)"
        nohup python3 -m src.main >> "$LOG_FILE" 2>&1 &
    fi

    echo $! > "$PID_FILE"
    sleep 2

    if kill -0 "$(cat $PID_FILE)" 2>/dev/null; then
        echo "✅ Bot started successfully (PID: $(cat $PID_FILE))"
        echo "📋 View logs: tail -f $LOG_FILE"
    else
        echo "❌ Bot failed to start. Check logs:"
        tail -20 "$LOG_FILE"
        rm -f "$PID_FILE"
        return 1
    fi
}

stop_bot() {
    if [ ! -f "$PID_FILE" ]; then
        echo "⚠️  No PID file found. Bot may not be running."
        # Try to find and kill by name
        pkill -f "python.*src.main" 2>/dev/null && echo "✅ Killed bot process" || echo "No bot process found"
        return 0
    fi

    PID=$(cat "$PID_FILE")
    if kill -0 "$PID" 2>/dev/null; then
        echo "🛑 Stopping bot (PID: $PID)..."
        kill "$PID"
        sleep 2
        if kill -0 "$PID" 2>/dev/null; then
            echo "⚠️  Bot didn't stop gracefully, forcing..."
            kill -9 "$PID" 2>/dev/null || true
        fi
        echo "✅ Bot stopped"
    else
        echo "⚠️  Bot process not found (stale PID file)"
    fi
    rm -f "$PID_FILE"
}

status_bot() {
    if [ -f "$PID_FILE" ] && kill -0 "$(cat $PID_FILE)" 2>/dev/null; then
        echo "✅ Bot is running (PID: $(cat $PID_FILE))"
        echo "📂 Log file: $LOG_FILE"
        echo ""
        echo "📋 Last 10 log lines:"
        tail -10 "$LOG_FILE" 2>/dev/null || echo "No logs yet"
    else
        echo "❌ Bot is not running"
        rm -f "$PID_FILE" 2>/dev/null
    fi
}

show_logs() {
    if [ -f "$LOG_FILE" ]; then
        tail -f "$LOG_FILE"
    else
        echo "❌ Log file not found: $LOG_FILE"
    fi
}

case "${1:-start}" in
    start)
        start_bot
        ;;
    stop|off|turnoff)
        stop_bot
        ;;
    restart)
        stop_bot
        sleep 1
        start_bot
        ;;
    status)
        status_bot
        ;;
    logs)
        show_logs
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status|logs}"
        echo ""
        echo "Commands:"
        echo "  start   - Start the bot in background"
        echo "  stop    - Stop the running bot (alias: off, turnoff)"
        echo "  restart - Restart the bot"
        echo "  status  - Show bot status and recent logs"
        echo "  logs    - Follow log output (Ctrl+C to exit)"
        exit 1
        ;;
esac
