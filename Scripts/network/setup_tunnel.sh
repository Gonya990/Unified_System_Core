#!/bin/bash
VM_IP="192.168.190.180"
SSH_KEY="Sandbox/id_rsa_proxmox"
USER="gonya"
WIN_USER="gonya"
WIN_IP="100.127.194.111"
WIN_PASS="GarYk6550"

echo "[1/4] Installing sshpass on Ubuntu..."
ssh -i $SSH_KEY -o StrictHostKeyChecking=no $USER@$VM_IP "sudo apt update && sudo apt install -y sshpass"

echo "[2/4] Setting up persistent SSH tunnel..."
# Kill old tunnels
ssh -i $SSH_KEY -o StrictHostKeyChecking=no $USER@$VM_IP "pkill -f 'ssh -L 11434'"

# Start new tunnel in background
# We bind remote 11434 to local 11434
ssh -i $SSH_KEY -o StrictHostKeyChecking=no $USER@$VM_IP "nohup sshpass -p '$WIN_PASS' ssh -o StrictHostKeyChecking=no -N -L 11434:localhost:11434 $WIN_USER@$WIN_IP > tunnel.log 2>&1 &"

echo "[3/4] Testing Tunnel..."
sleep 5
ssh -i $SSH_KEY -o StrictHostKeyChecking=no $USER@$VM_IP "curl -s http://localhost:11434"
if [ $? -eq 0 ]; then
    echo "TUNNEL SUCCESS!"
else
    echo "TUNNEL FAILED. Checking logs..."
    ssh -i $SSH_KEY -o StrictHostKeyChecking=no $USER@$VM_IP "cat tunnel.log"
fi

echo "[4/4] Reconfiguring Bot to use localhost..."
# Switch bot back to localhost since tunnel is local now
ssh -i $SSH_KEY -o StrictHostKeyChecking=no $USER@$VM_IP "sed -i 's/$WIN_IP:11434/localhost:11434/g' ~/bot/bot.py"
# Restart bot
ssh -i $SSH_KEY -o StrictHostKeyChecking=no $USER@$VM_IP "pkill -f 'python3 bot.py'; cd ~/bot && source venv/bin/activate && nohup python3 bot.py > bot.log 2>&1 &"

echo "DONE."
