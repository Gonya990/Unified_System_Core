#!/bin/bash
# ChatGPT Integration Automation System
# Система автоматизации интеграции с ChatGPT

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
UNIFIED_SYSTEM="/Users/macbook/Documents/Unified_System"
PROFILE_DIR="$UNIFIED_SYSTEM/Agent_Context/Personal_Profile"
KNOWLEDGE_BASE="$UNIFIED_SYSTEM/Agent_Context/Knowledge_Base"

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║   ChatGPT Integration Automation                             ║"
echo "║   Автоматизация интеграции с ChatGPT                         ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Function to check if files changed
check_file_changes() {
    local file=$1
    local last_hash_file="${file}.sha256"
    
    if [ -f "$file" ]; then
        current_hash=$(shasum -a 256 "$file" | awk '{print $1}')
        
        if [ -f "$last_hash_file" ]; then
            last_hash=$(cat "$last_hash_file")
            if [ "$current_hash" != "$last_hash" ]; then
                echo "✅ Changes detected in: $(basename $file)"
                echo "$current_hash" > "$last_hash_file"
                return 0
            fi
        else
            echo "$current_hash" > "$last_hash_file"
            return 0
        fi
    fi
    return 1
}

# 1. Check for CV changes
echo "📄 Checking CV files for changes..."
echo "📄 Проверка изменений в CV файлах..."
echo ""

CV_CHANGED=0
for cv_file in "$PROFILE_DIR"/CV_*.pdf "$PROFILE_DIR"/CV_*.docx; do
    if [ -f "$cv_file" ]; then
        if check_file_changes "$cv_file"; then
            CV_CHANGED=1
        fi
    fi
done

if [ $CV_CHANGED -eq 1 ]; then
    echo "🔄 CV files changed! Updating PROFILE.md..."
    echo "🔄 Файлы CV изменились! Обновляю PROFILE.md..."
    
    # Update timestamp in PROFILE.md
    sed -i '' "s/This PROFILE.md was read and recorded.*/This PROFILE.md was last synced on $(date -u '+%Y-%m-%d %H:%M UTC')./g" "$PROFILE_DIR/PROFILE.md"
    
    # Commit changes
    cd "$UNIFIED_SYSTEM"
    git add "$PROFILE_DIR/PROFILE.md"
    git commit -m "chore: auto-sync PROFILE.md after CV changes" || true
    git push origin main || echo "⚠️  Push failed, will retry later"
    
    echo "✅ PROFILE.md updated and pushed to GitHub"
fi

# 2. Pull latest changes from GitHub (ChatGPT might have updated)
echo ""
echo "🔄 Checking for updates from ChatGPT..."
echo "🔄 Проверка обновлений от ChatGPT..."
echo ""

cd "$UNIFIED_SYSTEM"
git fetch origin
LOCAL=$(git rev-parse main)
REMOTE=$(git rev-parse origin/main)

if [ "$LOCAL" != "$REMOTE" ]; then
    echo "📥 New changes from ChatGPT detected! Pulling..."
    echo "📥 Обнаружены новые изменения от ChatGPT! Загружаю..."
    
    git pull origin main
    
    echo "✅ Successfully synced with GitHub"
    echo "✅ Успешно синхронизировано с GitHub"
    
    # Check what changed
    echo ""
    echo "📊 Recent changes:"
    git log -1 --pretty=format:"Commit: %h%nAuthor: %an%nDate: %ad%nMessage: %s%n" --date=short
fi

# 3. Check OpenAI conversations export status
echo ""
echo "💬 Checking for new OpenAI conversations..."
echo "💬 Проверка новых разговоров OpenAI..."
echo ""

EXPORT_DIR="$UNIFIED_SYSTEM/Scripts/openai_data_integration/data/raw"
LATEST_EXPORT=$(find "$EXPORT_DIR" -name "*.zip" -type f -mtime -7 2>/dev/null | head -1)

if [ -n "$LATEST_EXPORT" ]; then
    echo "✅ Found recent export: $(basename $LATEST_EXPORT)"
    echo "📌 You can process it with:"
    echo "   cd $UNIFIED_SYSTEM/Scripts/openai_data_integration"
    echo "   ./quickstart.sh"
else
    echo "ℹ️  No recent exports found (last 7 days)"
    echo "💡 To export conversations:"
    echo "   1. Go to https://chatgpt.com/settings"
    echo "   2. Data Controls → Export data"
    echo "   3. Download ZIP to: $EXPORT_DIR"
fi

# 4. Sync Shared Agent Memory
echo ""
echo "🧠 Syncing Shared Agent Memory..."
echo "🧠 Синхронизация общей памяти агента..."
echo ""

SHARED_MEMORY="$UNIFIED_SYSTEM/Agent_Context/Shared_Memory.md"
if [ -f "$SHARED_MEMORY" ]; then
    cd "$UNIFIED_SYSTEM"
    git add "$SHARED_MEMORY"
    # Only commit if there are changes
    if ! git diff --cached --quiet; then
        git commit -m "chore: auto-sync Shared_Memory.md"
        git push origin main || echo "⚠️  Push failed for Shared_Memory.md"
        echo "✅ Shared_Memory.md synced and pushed"
    else
        echo "✅ No changes in Shared_Memory.md"
    fi
fi

# 5. Autosave all other changes
echo ""
echo "💾 Running global autosave..."
echo "💾 Запуск глобального автосохранения..."
echo ""
"$SCRIPT_DIR/autosave_changes.sh"

# 5. Generate summary report
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "📊 Automation Summary | Сводка автоматизации"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "✅ CV Change Detection: Active"
echo "✅ GitHub Sync: Active"
echo "✅ OpenAI Export Check: Active"
echo "✅ Shared Memory Sync: Active"
echo "✅ Global Autosave: Active"
echo ""
echo "📁 Monitored locations:"
echo "   - Personal Profile: $PROFILE_DIR"
echo "   - Knowledge Base: $KNOWLEDGE_BASE"
echo "   - OpenAI Exports: $EXPORT_DIR"
echo ""
echo "🕐 Last run: $(date)"
echo ""
echo "═══════════════════════════════════════════════════════════════"

# Save run log
LOG_DIR="$UNIFIED_SYSTEM/logs/automation"
mkdir -p "$LOG_DIR"
echo "$(date -u '+%Y-%m-%d %H:%M:%S UTC') - Automation run completed" >> "$LOG_DIR/chatgpt_integration.log"
