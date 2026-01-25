#!/bin/bash
echo "=== Tailscale Status ===" > debug_status.txt
tailscale status >> debug_status.txt 2>&1
echo "" >> debug_status.txt

echo "=== Internet Check ===" >> debug_status.txt
ping -c 2 8.8.8.8 >> debug_status.txt 2>&1
echo "" >> debug_status.txt

echo "=== Node/N8N Check ===" >> debug_status.txt
SCRIPT_DIR="$(pwd)"
TOOLS_DIR="$SCRIPT_DIR/tools"
NODE_DIR="$TOOLS_DIR/node-v20.11.0-darwin-arm64"
export PATH="$NODE_DIR/bin:$PATH"

echo "Node version:" >> debug_status.txt
node --version >> debug_status.txt 2>&1
echo "N8N location:" >> debug_status.txt
which n8n >> debug_status.txt 2>&1
echo "N8N version:" >> debug_status.txt
n8n --version >> debug_status.txt 2>&1
