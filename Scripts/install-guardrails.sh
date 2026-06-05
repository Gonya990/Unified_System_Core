#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

python3 -m venv .venv
source .venv/bin/activate
pip install -q -r services/approval-gateway/requirements.txt
pip install -q -r services/openclaw-mcp-bridge/requirements.txt
pip install -q -r services/finance-tracker/requirements.txt
pip install -q pynacl pytest

chmod +x scripts/*.sh scripts/pki/*.sh services/openclaw-mcp-bridge/server.py services/monitoring-bridge/bridge.py 2>/dev/null || true

echo "Guardrails installed. Start approval-gateway:"
echo "  source .venv/bin/activate && uvicorn app.main:app --app-dir services/approval-gateway --host 127.0.0.1 --port 8790"
