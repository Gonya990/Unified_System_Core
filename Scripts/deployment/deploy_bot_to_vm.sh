#!/bin/bash
# Deploy Bot to Proxmox VM (Ubuntu)
VM_IP="192.168.190.180"
SSH_KEY="Sandbox/id_rsa_proxmox"
USER="gonya"

echo "[1/4] Preparing VM environment..."
ssh -i $SSH_KEY -o StrictHostKeyChecking=no $USER@$VM_IP "sudo apt update && sudo apt install -y python3-pip python3-venv && mkdir -p ~/bot"

echo "[2/4] Copying files..."
scp -i $SSH_KEY -o StrictHostKeyChecking=no Windows_AI_Core/src/ai_telegram_bot_v2.py $USER@$VM_IP:~/bot/bot.py
scp -i $SSH_KEY -o StrictHostKeyChecking=no Windows_AI_Core/src/bot_config_live.py $USER@$VM_IP:~/bot/bot_config.py

echo "[3/4] Installing dependencies on VM..."
ssh -i $SSH_KEY -o StrictHostKeyChecking=no $USER@$VM_IP "cd ~/bot && python3 -m venv venv && source venv/bin/activate && pip install python-telegram-bot aiohttp"

echo "[4/4] Configuring OLLAMA Host IP..."
# We need to point the bot to Windows IP for Ollama instead of localhost
# We can use sed to replace localhost with Windows Tailscale IP
WINDOWS_IP="100.127.194.111"
ssh -i $SSH_KEY -o StrictHostKeyChecking=no $USER@$VM_IP "sed -i 's/localhost:11434/$WINDOWS_IP:11434/g' ~/bot/bot.py"

echo "[5/4] Starting Bot service..."
ssh -i $SSH_KEY -o StrictHostKeyChecking=no $USER@$VM_IP "cd ~/bot && source venv/bin/activate && nohup python3 bot.py > bot.log 2>&1 &"

echo "DEPLOY COMPLETE. Bot is running on VM."
