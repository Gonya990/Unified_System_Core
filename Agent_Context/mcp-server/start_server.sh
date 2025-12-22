#!/bin/bash
# Antigravity MCP Server Startup Script
cd /home/gonya/antigravity-mcp-server

# Check if running
if pgrep -f "antigravity-mcp-server/dist/index.js" > /dev/null; then
    echo "Server is already running."
    exit 0
fi

echo "Starting Antigravity MCP Server on Port 3005..."
nohup node dist/index.js --transport=sse > mcp-server.log 2>&1 &
echo "Server started (PID $!). Log: tail -f mcp-server.log"
