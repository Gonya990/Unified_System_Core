#!/bin/bash
# iOS Context Sync Script
# Monitors iCloud Downloads for new files and copies them to the repo

ICLOUD_DOWNLOADS="$HOME/Library/Mobile Documents/com~apple~CloudDocs/Downloads"
DEST_DIR="/Users/macbook/Documents/Unified_System/Agent_Context/machines/iphone-15-pro/exports"

mkdir -p "$DEST_DIR"

echo "📱 Monitoring iCloud Downloads for iOS exports..."
echo "Source: $ICLOUD_DOWNLOADS"
echo "Destination: $DEST_DIR"
echo ""

# Check for new files
if [ -d "$ICLOUD_DOWNLOADS" ]; then
    NEW_FILES=$(find "$ICLOUD_DOWNLOADS" -type f -mmin -60 2>/dev/null)
    
    if [ -n "$NEW_FILES" ]; then
        echo "Found recent files:"
        echo "$NEW_FILES"
        echo ""
        
        # Copy new files
        for file in $NEW_FILES; do
            filename=$(basename "$file")
            echo "Copying: $filename"
            cp "$file" "$DEST_DIR/"
        done
        
        echo ""
        echo "✅ Files copied to $DEST_DIR"
    else
        echo "No new files in the last hour."
        echo ""
        echo "📋 Current contents of iCloud Downloads:"
        ls -la "$ICLOUD_DOWNLOADS" 2>/dev/null
    fi
else
    echo "❌ iCloud Downloads folder not found"
fi
