#!/bin/bash
# Autosave Changes Script
# Automatically commits and pushes all changes to GitHub

set -e

REPO_DIR="/home/gonya/Unified_System_Core"
cd "$REPO_DIR"

echo "🔍 Checking for changes..."
if [[ -z $(git status --porcelain) ]]; then
    echo "✅ No changes to autosave"
    exit 0
fi

echo "📝 Changes detected:"
git status --short

echo ""
echo "➕ Staging all changes..."
git add -A

echo "💾 Committing changes..."
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
git commit -m "autosave: $TIMESTAMP"

echo "🚀 Pushing to GitHub..."
git push origin main

echo "✅ Autosave complete!"
