#!/bin/bash
# Setup automated Telegram channel monitoring with Agent Mail integration

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"

echo "🔧 Setting up Telegram Channel Monitor"
echo "======================================"

# Create launchd plist for macOS (runs every 6 hours)
PLIST_FILE="$HOME/Library/LaunchAgents/com.unified.telegram-monitor.plist"

cat > "$PLIST_FILE" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.unified.telegram-monitor</string>

    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>-c</string>
        <string>cd $PROJECT_ROOT/Scripts/Research && python3 scrape_telegram_web.py && cd $PROJECT_ROOT/Scripts/Orchestration && python3 telegram_to_mail.py</string>
    </array>

    <key>StartInterval</key>
    <integer>21600</integer>

    <key>StandardOutPath</key>
    <string>$PROJECT_ROOT/Reports/.telegram_monitor.log</string>

    <key>StandardErrorPath</key>
    <string>$PROJECT_ROOT/Reports/.telegram_monitor.error.log</string>

    <key>WorkingDirectory</key>
    <string>$PROJECT_ROOT</string>

    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin</string>
    </dict>
</dict>
</plist>
EOF

echo "✅ Created launchd plist: $PLIST_FILE"

# Load the service
launchctl unload "$PLIST_FILE" 2>/dev/null
launchctl load "$PLIST_FILE"

echo "✅ Service loaded (runs every 6 hours)"

# Create manual run script
cat > "$SCRIPT_DIR/run_telegram_monitor.sh" << 'EOF'
#!/bin/bash
# Manual run of Telegram monitor

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"

echo "🔍 Running Telegram Monitor (Manual)"

cd "$PROJECT_ROOT/Scripts/Research"
python3 scrape_telegram_web.py

cd "$PROJECT_ROOT/Scripts/Orchestration"
python3 telegram_to_mail.py

echo "✅ Monitor complete"
EOF

chmod +x "$SCRIPT_DIR/run_telegram_monitor.sh"

echo "✅ Created manual run script: run_telegram_monitor.sh"
echo ""
echo "📋 Setup Complete!"
echo ""
echo "Commands:"
echo "  Manual run:  ./Scripts/Orchestration/run_telegram_monitor.sh"
echo "  Check logs:  tail -f Reports/.telegram_monitor.log"
echo "  Stop service: launchctl unload $PLIST_FILE"
echo ""
echo "🔔 Monitor will run automatically every 6 hours"