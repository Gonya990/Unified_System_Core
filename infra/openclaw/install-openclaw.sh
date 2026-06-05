#!/usr/bin/env bash
# Run on NUC / smart node (Linux)
set -euo pipefail

if ! command -v npm >/dev/null 2>&1; then
  echo "Install Node.js 20+ first" >&2
  exit 1
fi

echo "Installing OpenClaw CLI (pin version in production)..."
npm install -g openclaw@latest

mkdir -p /opt/unified/openclaw
cp "$(dirname "$0")/../systemd/openclaw-gateway.service" /etc/systemd/system/ 2>/dev/null || \
  echo "Copy infra/systemd/openclaw-gateway.service manually"

echo "Enable: systemctl enable --now openclaw-gateway"
echo "MCP: openclaw mcp serve"
