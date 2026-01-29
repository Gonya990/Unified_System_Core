#!/bin/bash
HOST="igor-windows"
MAX_RETRIES=60 # 5 minutes (5s * 60)
 
echo "Waiting for $HOST to come back online..."

# 1. Wait for Ping
count=0
while ! ping -c 1 -W 2 $HOST &> /dev/null; do
    echo "[$count/$MAX_RETRIES] Pinging $HOST..."
    sleep 5
    ((count++))
    if [ $count -ge $MAX_RETRIES ]; then
        echo "Timed out waiting for Ping."
        exit 1
    fi
done

echo "$HOST is pingable! Waiting for SSH..."

# 2. Wait for SSH
count=0
while ! ssh -o ConnectTimeout=5 -o BatchMode=yes $HOST "echo ready" &> /dev/null; do
    echo "[$count/$MAX_RETRIES] Waiting for SSH service..."
    sleep 5
    ((count++))
    if [ $count -ge $MAX_RETRIES ]; then
        echo "Timed out waiting for SSH."
        exit 1
    fi
done

echo "✅ $HOST is back online and SSH is ready!"
