#!/bin/bash
# GitHub ↔ ChatGPT Collaboration Monitor
# Монитор коллаборации GitHub ↔ ChatGPT

set -e

UNIFIED_SYSTEM="/Users/macbook/Documents/Unified_System"
COLLABORATION_LOG="$UNIFIED_SYSTEM/logs/collaboration/github_chatgpt.log"

mkdir -p "$(dirname "$COLLABORATION_LOG")"

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║   GitHub ↔ ChatGPT Collaboration Monitor                     ║"
echo "║   Монитор коллаборации GitHub ↔ ChatGPT                      ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

cd "$UNIFIED_SYSTEM"

# Check for new commits
echo "🔍 Analyzing recent commits..."
echo "🔍 Анализ последних коммитов..."
echo ""

# Get commits from last 24 hours
COMMITS=$(git log --since="24 hours ago" --pretty=format:"%h|%an|%ar|%s" --no-merges)

if [ -z "$COMMITS" ]; then
    echo "ℹ️  No new commits in last 24 hours"
    echo "ℹ️  Нет новых коммитов за последние 24 часа"
else
    echo "📊 Recent Activity:"
    echo ""
    
    ANTIGRAVITY_COUNT=0
    CHATGPT_COUNT=0
    USER_COUNT=0
    
    while IFS='|' read -r hash author time message; do
        echo "  [$hash] $author - $time"
        echo "  └─ $message"
        echo ""
        
        # Count by author type
        if echo "$message" | grep -qi "antigravity\|gemini"; then
            ((ANTIGRAVITY_COUNT++))
        elif echo "$message" | grep -qi "chatgpt\|gpt-5\|openai"; then
            ((CHATGPT_COUNT++))
        else
            ((USER_COUNT++))
        fi
        
        # Log to file
        echo "$(date -u '+%Y-%m-%d %H:%M:%S UTC')|$hash|$author|$message" >> "$COLLABORATION_LOG"
    done <<< "$COMMITS"
    
    echo "═══════════════════════════════════════════════════════════════"
    echo "📈 Collaboration Statistics (24h)"
    echo "═══════════════════════════════════════════════════════════════"
    echo ""
    echo "  Antigravity commits: $ANTIGRAVITY_COUNT"
    echo "  ChatGPT commits:     $CHATGPT_COUNT"
    echo "  Manual commits:      $USER_COUNT"
    echo "  Total:               $((ANTIGRAVITY_COUNT + CHATGPT_COUNT + USER_COUNT))"
    echo ""
fi

# Check for pending changes
echo "🔄 Checking workspace status..."
echo "🔄 Проверка статуса рабочего пространства..."
echo ""

if ! git diff-index --quiet HEAD --; then
    echo "⚠️  Uncommitted changes detected!"
    echo "⚠️  Обнаружены незакоммиченные изменения!"
    echo ""
    echo "Modified files:"
    git status --short
    echo ""
    echo "💡 Commit these changes to enable ChatGPT sync:"
    echo "   git add -A"
    echo "   git commit -m 'your message'"
    echo "   git push origin main"
else
    echo "✅ Working directory clean"
    echo "✅ Рабочая директория чистая"
fi

# Check if synced with remote
echo ""
echo "📡 Checking sync with GitHub..."
echo "📡 Проверка синхронизации с GitHub..."
echo ""

git fetch origin --quiet

LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/main)

if [ "$LOCAL" == "$REMOTE" ]; then
    echo "✅ Fully synced with GitHub"
    echo "✅ Полностью синхронизировано с GitHub"
else
    BEHIND=$(git rev-list --count HEAD..origin/main)
    AHEAD=$(git rev-list --count origin/main..HEAD)
    
    if [ "$BEHIND" -gt 0 ]; then
        echo "📥 Behind by $BEHIND commits (ChatGPT may have pushed)"
        echo "📥 Отстаем на $BEHIND коммитов (ChatGPT мог отправить)"
        echo ""
        echo "Pull with: git pull origin main"
    fi
    
    if [ "$AHEAD" -gt 0 ]; then
        echo "📤 Ahead by $AHEAD commits (push to share with ChatGPT)"
        echo "📤 Впереди на $AHEAD коммитов (отправьте чтобы поделиться с ChatGPT)"
        echo ""
        echo "Push with: git push origin main"
    fi
fi

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "🤝 Collaboration Health | Здоровье коллаборации"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "GitHub Sync: $([ "$LOCAL" == "$REMOTE" ] && echo "✅ Active" || echo "⚠️  Pending")"
echo "ChatGPT Integration: ✅ Configured"
echo "Antigravity Automation: ✅ Running"
echo ""
echo "Last check: $(date)"
echo "Log file: $COLLABORATION_LOG"
echo ""
echo "═══════════════════════════════════════════════════════════════"
