#!/bin/bash
set -e

echo "=========================================="
echo "🚀 AI Telegram Bot Starting..."
echo "=========================================="
echo "Inference URL: ${INFERENCE_BASE_URL}"
echo "Model: ${MODEL_NAME}"
echo "Log Level: ${LOG_LEVEL}"
echo "=========================================="

# Validate required environment variables
if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
    echo "❌ ERROR: TELEGRAM_BOT_TOKEN is not set!"
    exit 1
fi

# Start the bot
exec python -m src.main
