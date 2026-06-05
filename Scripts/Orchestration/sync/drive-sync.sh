#!/bin/bash

# ==========================================
# Google Drive Sync (NotebookLM) Wrapper
# ==========================================

set -e

BASE_DIR="/Users/igorgoncharenko/Documents/Unified_System_Core"
SCRIPT_PATH="${BASE_DIR}/Scripts/automation/sync_notebooklm_drive.py"

echo "=========================================="
echo "Starting Google Drive Sync (NotebookLM)..."
echo "=========================================="

# Ensure dependencies are installed (in global or default python environment)
pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib >/dev/null 2>&1 || true

# Run the Python script
python3 "${SCRIPT_PATH}"

echo ""
echo "Google Drive Sync completed successfully."
