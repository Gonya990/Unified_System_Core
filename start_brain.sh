#!/bin/bash

# Vibranium Engine - Start Script
# This script sets up the local environment and launches n8n (the Brain).

# Resolve the directory of the script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOOLS_DIR="$SCRIPT_DIR/tools"

# Path to the portable Node.js
NODE_DIR="$TOOLS_DIR/node-v20.11.0-darwin-arm64"
NPM_GLOBAL="$TOOLS_DIR/npm-global"

# Check if Node exists
if [ ! -d "$NODE_DIR" ]; then
    echo "❌ Node.js not found in $NODE_DIR"
    echo "Please ensure the Vibranium setup has completed successfully."
    exit 1
fi

# Set Environment Variables
export PATH="$NODE_DIR/bin:$NPM_GLOBAL/bin:$PATH"
export NPM_CONFIG_PREFIX="$NPM_GLOBAL"
export NPM_CONFIG_CACHE="$TOOLS_DIR/npm-cache"

# Check if n8n is installed
if ! command -v n8n &> /dev/null; then
    echo "⚠️ n8n is not finding in PATH."
    echo "Checking if it is installed in global bin..."
    if [ -f "$NPM_GLOBAL/bin/n8n" ]; then
        echo "Found n8n manual path."
        export PATH="$NPM_GLOBAL/bin:$PATH"
    else
        echo "⏳ n8n seems to be missing. Installation might still be in progress."
        exit 1
    fi
fi

echo "🚀 Starting Vibranium Brain (n8n)..."
echo "Tunnel URL should appear shortly."
n8n start --tunnel
