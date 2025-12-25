#!/bin/bash
# CV Synchronization Manager
# Менеджер синхронизации CV

set -e

PROFILE_DIR="/Users/macbook/Documents/Unified_System/Agent_Context/Personal_Profile"
PROFILE_MD="$PROFILE_DIR/PROFILE.md"

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║   CV Synchronization Manager                                 ║"
echo "║   Менеджер синхронизации CV                                  ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Check all CV files
echo "📄 Analyzing CV files..."
echo "📄 Анализ файлов CV..."
echo ""

CV_EN="$PROFILE_DIR/CV_Igor_Goncharenko_EN.pdf"
CV_RU="$PROFILE_DIR/CV_Igor_Goncharenko_RU.pdf"
CV_HE="$PROFILE_DIR/CV_Igor_Goncharenko_HE_RTL.pdf"

# Extract modification dates
extract_date() {
    if [ -f "$1" ]; then
        stat -f "%Sm" -t "%Y-%m-%d" "$1"
    else
        echo "N/A"
    fi
}

EN_DATE=$(extract_date "$CV_EN")
RU_DATE=$(extract_date "$CV_RU")
HE_DATE=$(extract_date "$CV_HE")

echo "CV Files Status:"
echo "├─ EN: $EN_DATE"
echo "├─ RU: $RU_DATE"
echo "└─ HE: $HE_DATE"
echo ""

# Find most recent
LATEST_DATE=$EN_DATE
LATEST_FILE="EN"

if [[ "$RU_DATE" > "$LATEST_DATE" ]]; then
    LATEST_DATE=$RU_DATE
    LATEST_FILE="RU"
fi

if [[ "$HE_DATE" > "$LATEST_DATE" ]]; then
    LATEST_DATE=$HE_DATE
    LATEST_FILE="HE"
fi

echo "📌 Most recent CV: $LATEST_FILE ($LATEST_DATE)"
echo ""

# Check if PROFILE.md needs update
PROFILE_DATE=$(grep "last synced on" "$PROFILE_MD" 2>/dev/null | grep -o '[0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}' || echo "N/A")

if [ "$PROFILE_DATE" != "$LATEST_DATE" ]; then
    echo "🔄 PROFILE.md is out of sync!"
    echo "🔄 PROFILE.md не синхронизирован!"
    echo ""
    echo "   Profile last synced: $PROFILE_DATE"
    echo "   Latest CV date: $LATEST_DATE"
    echo ""
    echo "💡 Recommendation | Рекомендация:"
    echo "   Update PROFILE.md to reflect latest CV changes"
    echo "   Обновите PROFILE.md чтобы отразить последние изменения CV"
    echo ""
    
    # Auto-update if requested
    if [ "$1" == "--auto-update" ]; then
        echo "🤖 Auto-updating PROFILE.md..."
        
        # Update timestamp
        if grep -q "last synced on" "$PROFILE_MD"; then
            sed -i '' "s/last synced on [0-9-]* [0-9:]* UTC/last synced on $(date -u '+%Y-%m-%d %H:%M UTC')/g" "$PROFILE_MD"
        else
            # Add timestamp if not exists
            echo "" >> "$PROFILE_MD"
            echo "**Last CV sync:** $(date -u '+%Y-%m-%d %H:%M UTC')" >> "$PROFILE_MD"
        fi
        
        echo "✅ PROFILE.md updated!"
        echo ""
        echo "📝 Don't forget to commit:"
        echo "   git add $PROFILE_MD"
        echo "   git commit -m 'chore: sync PROFILE with latest CV ($LATEST_FILE)'"
        echo "   git push origin main"
    fi
else
    echo "✅ PROFILE.md is up to date!"
    echo "✅ PROFILE.md актуален!"
fi

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "📊 CV Sync Summary | Сводка синхронизации CV"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "CV Files: 3"
echo "Latest: $LATEST_FILE ($LATEST_DATE)"
echo "Profile sync: $PROFILE_DATE"
echo "Status: $([ "$PROFILE_DATE" == "$LATEST_DATE" ] && echo "✅ Synced" || echo "⚠️  Out of sync")"
echo ""
echo "═══════════════════════════════════════════════════════════════"
