#!/bin/bash
# Script to run GitHub MCP Server using local gh CLI credentials

# Get token from local gh CLI
TOKEN=$(gh auth token 2>/dev/null)

if [ -z "$TOKEN" ]; then
  echo "Error: Not logged into GitHub CLI. Run 'gh auth login' first."
  exit 1
fi

echo "Starting GitHub MCP Server..."
# GITHUB_PERSONAL_ACCESS_TOKEN is required by @modelcontextprotocol/server-github
export GITHUB_PERSONAL_ACCESS_TOKEN=$TOKEN

npx -y @modelcontextprotocol/server-github
