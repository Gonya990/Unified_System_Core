#!/bin/bash
# Autosave Changes System
# Система автосохранения изменений

# Detect repository root
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$REPO_ROOT"

echo "🔍 Repository root: $REPO_ROOT"

# Check for changes
if [[ -n $(git status -s) ]]; then
    echo "🔄 Changes detected! Autosaving..."
    echo "🔄 Обнаружены изменения! Автосохранение..."
    
    # Check if we are already in a git add/commit process by another agent
    if [ -f "$REPO_ROOT/.agent/.workflow-lock" ]; then
        echo "⚠️ Workflow lock detected. Skipping autosave to avoid conflicts."
        exit 0
    fi

    echo "📝 Changes:"
    git status -s

    git add .
    git commit -m "chore: autosave changes $(date '+%Y-%m-%d %H:%M:%S')"
    git push origin main || echo "⚠️ Push failed"
    
    echo "✅ Changes autosaved and pushed."
else
    echo "✅ No changes to save."
fi
