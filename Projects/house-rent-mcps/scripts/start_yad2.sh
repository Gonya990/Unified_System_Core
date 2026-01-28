#!/bin/bash
# Wrapper to run Yad2 MCP server via devenv in HTTP mode
export TRANSPORT=http
export PORT=3001
cd /home/kosta/Documents/Unified_System_Core
# We run in the background so the script doesn't block, but for a service manager we might want foreground.
# Since this is a helper script likely to be run manually or by a process manager, keeping it simple.
# If this script is called by something expecting to hold the process, we should just run it.
/run/current-system/sw/bin/devenv shell -- bash -c "cd Projects/house-rent-mcps && bun run index.ts > yad2_server.log 2>&1"
