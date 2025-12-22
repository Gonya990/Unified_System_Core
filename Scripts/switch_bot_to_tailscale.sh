#!/bin/bash
VM_IP="192.168.190.180"
SSH_KEY="Sandbox/id_rsa_proxmox"
USER="gonya"
WIN_IP="100.127.194.111"

echo "Reconfiguring Bot to use Windows Tailscale IP ($WIN_IP)..."
# Replace any 'localhost' or old IP with the Tailscale IP
ssh -i $SSH_KEY -o StrictHostKeyChecking=no $USER@$VM_IP "sed -i 's/localhost:11434/$WIN_IP:11434/g' ~/bot/bot.py"
# Just in case it was tunnel IP, make sure it's correct
ssh -i $SSH_KEY -o StrictHostKeyChecking=no $USER@$VM_IP "sed -i 's/127.0.0.1:11434/$WIN_IP:11434/g' ~/bot/bot.py"

echo "Restarting Bot..."
ssh -i $SSH_KEY -o StrictHostKeyChecking=no $USER@$VM_IP "pkill -f 'python3 bot.py'; cd ~/bot && source venv/bin/activate && nohup python3 bot.py > bot.log 2>&1 &"

echo "Bot switched to Tailscale Network."
