#!/bin/bash
VM_IP="192.168.190.180"
SSH_KEY="Sandbox/id_rsa_proxmox"
USER="gonya"

echo "Installing Tailscale on VM..."
ssh -i $SSH_KEY -o StrictHostKeyChecking=no $USER@$VM_IP "curl -fsSL https://tailscale.com/install.sh | sh"

echo "Starting Tailscale..."
# Run 'tailscale up' and capture the AUTH URL if needed
ssh -i $SSH_KEY -o StrictHostKeyChecking=no $USER@$VM_IP "sudo tailscale up 2>&1 | grep 'https://login.tailscale.com'"
