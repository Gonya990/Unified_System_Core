#!/bin/bash
set -e

# Setup SSH Keys for AI Consortium
# This script generates an SSH key pair on the Linux host and copies it to the remote nodes.

NucIP="100.81.133.25"
WslIP="100.88.65.71"
User="gonya"
KeyPath="$HOME/.ssh/id_ai_consortium"

# 1. Generate FRESH Key for AI Agent (No Passphrase)
if [ ! -f "$KeyPath" ]; then
    echo "Generating New AI SSH Key..."
    ssh-keygen -t rsa -b 4096 -f "$KeyPath" -N ""
else
    echo "Key already exists at $KeyPath, skipping generation."
fi

# 2. Function to copy key
copy_key() {
    local target_ip=$1
    local name=$2
    
    echo "--------------------------------------------------"
    echo "Processing $name ($target_ip)..."
    
    # Check if target is self
    if ip addr | grep -q "$target_ip"; then
        echo "Target $target_ip appears to be the local machine. Skipping copy to self to avoid redundancy."
        return
    fi

    echo "Copying Key to $name ($target_ip)..."
    echo "You may be prompted for $User@$target_ip's password."
    
    # Use ssh-copy-id if available, otherwise manual method
    if command -v ssh-copy-id &> /dev/null; then
        ssh-copy-id -i "$KeyPath.pub" -o PubkeyAuthentication=no "$User@$target_ip"
    else
        cat "$KeyPath.pub" | ssh -o PubkeyAuthentication=no "$User@$target_ip" "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
    fi
}

# 3. Copy Key to Remote Nodes
copy_key "$NucIP" "NUC"
copy_key "$WslIP" "WSL"

echo "--------------------------------------------------"
echo "SSH Keys Configured! You can now use these keys in n8n."
