#!/bin/bash
# Unified Repository Sync Script
# Синхронизирует изменения между всеми remotes

set -e

echo "🔄 Starting repository synchronization..."

# Fetch from all remotes
echo "📥 Fetching from all remotes..."
git fetch --all --prune

# Get current branch
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
echo "📍 Current branch: $CURRENT_BRANCH"

# Sync main branch with origin (Unified_System_Core)
if [ "$CURRENT_BRANCH" = "main" ]; then
    echo "✅ On main branch, syncing with origin..."
    
    # Pull latest from origin
    git pull origin main --rebase
    
    # Push to origin
    git push origin main
    
    # Also push to antibridge_fixed (optional mirror)
    echo "📤 Pushing to antibridge_fixed..."
    git push antibridge_fixed main || echo "⚠️  antibridge_fixed push failed (might be expected)"
else
    echo "⚠️  Not on main branch, skipping sync"
fi

echo "✅ Synchronization complete!"
