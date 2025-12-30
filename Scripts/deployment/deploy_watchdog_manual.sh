#!/bin/bash
# Manual Deployment Script for Watchdog Fix
# Скрипт ручного обновления watchdog.py

TARGET_HOST="100.127.194.111" # igor-gaming-1 (Windows PC) via Tailscale
TARGET_USER="igor"
SSH_KEY="$HOME/.ssh/id_rsa" # Adjust if needed

echo "🟦 === Manual Deployment: Watchdog Fix ==="
echo "Target: $TARGET_USER@$TARGET_HOST"
echo ""

# Check for SSH key
if [ ! -f "$SSH_KEY" ]; then
    echo "⚠️  SSH Key not found at $SSH_KEY. Using default agent."
    SSH_OPT=""
else
    SSH_OPT="-i $SSH_KEY"
fi

# 1. Copy file
echo "📦 Copying watchdog.py..."
# Assuming standard path structure on remote. If it fails, user might need to adjust path.
# PATH A: ~/Documents/Unified_System/Windows_AI_Core/src/watchdog.py (WSL Dev)
scp $SSH_OPT Windows_AI_Core/src/watchdog.py $TARGET_USER@$TARGET_HOST:~/Documents/Unified_System/Windows_AI_Core/src/watchdog.py

if [ $? -eq 0 ]; then
    echo "✅ File copied successfully."
else
    echo "❌ Copy failed. Check paths and permissions."
    echo "Attempting alternative path (deployment folder)..."
    # PATH B: ~/bot/src/watchdog.py (VM Deploy)
    scp $SSH_OPT Windows_AI_Core/src/watchdog.py $TARGET_USER@$TARGET_HOST:~/bot/src/watchdog.py
fi

# 2. Restart Service
echo "🔄 Restarting AI Bot Service..."
ssh $SSH_OPT $TARGET_USER@$TARGET_HOST "sudo systemctl restart ai-bot || echo '⚠️ Could not restart service automatically. Please restart manually.'"

echo ""
echo "✅ Deployment attempt finished."
