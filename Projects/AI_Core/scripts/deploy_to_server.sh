#!/bin/bash
# Deploy script for igor-gaming-1
set -e

echo "🚀 Starting Deployment on $(hostname)..."

# Expected path
PROJECT_DIR="$HOME/Unified_System"

if [ ! -d "$PROJECT_DIR" ]; then
    echo "❌ Project directory not found at $PROJECT_DIR"
    echo "➡️  Please clone the repo to $HOME/Unified_System first."
    exit 1
fi

cd "$PROJECT_DIR"

echo "📥 Pulling latest changes..."
git pull

echo "📦 Updating dependencies..."
# Try activation
if [ -f "Projects/AI_Core/venv/bin/activate" ]; then
    source Projects/AI_Core/venv/bin/activate
else
    echo "⚠️  Venv not found at Projects/AI_Core/venv, creating..."
    python3 -m venv Projects/AI_Core/venv
    source Projects/AI_Core/venv/bin/activate
fi

pip install -r Projects/AI_Core/requirements.txt

echo "♻️  Restarting Service..."
# Assuming systemd user service named ai-bot as per infrastructure.yaml
SERVICE_NAME="ai-bot"

if systemctl --user list-units --full -all | grep -Fq "$SERVICE_NAME.service"; then
    echo "🔄 Restarting existing service..."
    systemctl --user restart $SERVICE_NAME
else
    echo "⚙️  Service not found. Installing..."
    mkdir -p ~/.config/systemd/user
    cp Projects/AI_Core/scripts/ai-bot.service ~/.config/systemd/user/
    systemctl --user daemon-reload
    systemctl --user enable $SERVICE_NAME
    systemctl --user start $SERVICE_NAME
    echo "✅ Service installed and started!"
fi

echo "✅ Deployment Script Finished!"
systemctl --user status $SERVICE_NAME --no-pager
