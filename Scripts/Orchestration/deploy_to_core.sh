#!/bin/bash
#
# Deploy Unified System to CORE Server (100.110.209.49)
#
# This script migrates the entire codebase and configuration
# from local MacBook to the CORE server.
#

set -e

CORE_IP="100.110.209.49"
CORE_USER="gonya"
CORE_PATH="/home/gonya/Unified_System"
LOCAL_PATH="/Users/macbook/Documents/Unified_System"

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║     Unified System - CORE Server Deployment                   ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Step 1: Pre-flight checks
echo "🔍 Step 1: Pre-flight Checks"
echo "------------------------------------------------------------"

# Check Tailscale connectivity
if ! tailscale status | grep -q "$CORE_IP"; then
    echo "❌ ERROR: CORE server ($CORE_IP) not accessible via Tailscale"
    exit 1
fi
echo "✅ Tailscale connectivity OK"

# Check SSH access
if ! tailscale ssh ${CORE_USER}@${CORE_IP} "echo 'SSH OK'" >/dev/null 2>&1; then
    echo "❌ ERROR: Cannot SSH to CORE server"
    exit 1
fi
echo "✅ SSH access OK"

echo ""

# Step 2: Backup current CORE state
echo "💾 Step 2: Backing up CORE server state"
echo "------------------------------------------------------------"

tailscale ssh ${CORE_USER}@${CORE_IP} "
    if [ -d $CORE_PATH ]; then
        BACKUP_DIR=\${HOME}/Unified_System_Backup_\$(date +%Y%m%d_%H%M%S)
        echo '📦 Creating backup: '\$BACKUP_DIR
        cp -r $CORE_PATH \$BACKUP_DIR
        echo '✅ Backup created'
    else
        echo '⏭️  No existing installation to backup'
    fi
"

echo ""

# Step 3: Sync codebase
echo "🚀 Step 3: Syncing codebase to CORE"
echo "------------------------------------------------------------"

# Stop bots on CORE first
tailscale ssh ${CORE_USER}@${CORE_IP} "
    echo '⏹️  Stopping services...'
    sudo pkill -f 'ai_telegram_bot_v2.py' 2>/dev/null || true
    sudo systemctl stop telegram-bot-* 2>/dev/null || true
"

# Rsync with Tailscale
echo "📤 Transferring files (this may take a while)..."
rsync -avz --exclude='.git' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='.venv' \
    --exclude='node_modules' \
    --exclude='Knowledge_Base' \
    --exclude='*.log' \
    -e "ssh -o 'ProxyCommand=tailscale nc %h %p'" \
    ${LOCAL_PATH}/ ${CORE_USER}@${CORE_IP}:${CORE_PATH}/

echo "✅ Codebase synced"
echo ""

# Step 4: Setup environment on CORE
echo "⚙️  Step 4: Setting up environment on CORE"
echo "------------------------------------------------------------"

tailscale ssh ${CORE_USER}@${CORE_IP} "
    cd $CORE_PATH
    
    # Create venv if not exists
    if [ ! -d .venv ]; then
        echo '🐍 Creating Python virtual environment...'
        python3 -m venv .venv
    fi
    
    # Install dependencies
    echo '📦 Installing dependencies...'
    .venv/bin/pip install -q --upgrade pip
    .venv/bin/pip install -q -r requirements.txt 2>/dev/null || echo '⚠️  No requirements.txt found'
    
    # Setup RBAC
    echo '🔐 Configuring Network RBAC...'
    .venv/bin/python Scripts/Orchestration/setup_network_rbac.py
    
    echo '✅ Environment setup complete'
"

echo ""

# Step 5: Configure systemd services
echo "🔧 Step 5: Configuring systemd services"
echo "------------------------------------------------------------"

tailscale ssh ${CORE_USER}@${CORE_IP} "
    cd $CORE_PATH
    
    # Create systemd service for Igor's bot
    sudo tee /etc/systemd/system/telegram-bot-igor.service > /dev/null << 'EOF'
[Unit]
Description=Unified System - Igor's Telegram Bot
After=network.target

[Service]
Type=simple
User=$CORE_USER
WorkingDirectory=$CORE_PATH
ExecStart=$CORE_PATH/.venv/bin/python $CORE_PATH/Projects/AI_Core/src/ai_telegram_bot_v2.py --env $CORE_PATH/.env --port 8096
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

    # Create systemd service for Kostya's bot
    sudo tee /etc/systemd/system/telegram-bot-kostya.service > /dev/null << 'EOF'
[Unit]
Description=Unified System - Kostya's Telegram Bot
After=network.target

[Service]
Type=simple
User=$CORE_USER
WorkingDirectory=$CORE_PATH
ExecStart=$CORE_PATH/.venv/bin/python $CORE_PATH/Projects/AI_Core/src/ai_telegram_bot_v2.py --env $CORE_PATH/Projects/AI_Core/.env.kostya --port 8098
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

    # Reload systemd
    sudo systemctl daemon-reload
    
    # Enable services
    sudo systemctl enable telegram-bot-igor telegram-bot-kostya
    
    echo '✅ Systemd services configured'
"

echo ""

# Step 6: Start services
echo "▶️  Step 6: Starting services on CORE"
echo "------------------------------------------------------------"

tailscale ssh ${CORE_USER}@${CORE_IP} "
    sudo systemctl start telegram-bot-igor
    sudo systemctl start telegram-bot-kostya
    
    sleep 5
    
    echo '📊 Service Status:'
    sudo systemctl status telegram-bot-igor --no-pager | head -10
    echo ''
    sudo systemctl status telegram-bot-kostya --no-pager | head -10
"

echo ""

# Step 7: Verification
echo "✅ Step 7: Verification"
echo "------------------------------------------------------------"

echo "Checking bot health endpoints..."
curl -s http://${CORE_IP}:8095/health > /dev/null 2>&1 && echo "✅ Igor's bot: Online" || echo "❌ Igor's bot: Offline"
curl -s http://${CORE_IP}:8097/health > /dev/null 2>&1 && echo "✅ Kostya's bot: Online" || echo "❌ Kostya's bot: Offline"

echo ""

# Step 8: Stop local bots
echo "⏹️  Step 8: Stopping local bots on MacBook"
echo "------------------------------------------------------------"

read -p "Stop local bots and switch to CORE? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    launchctl unload ~/Library/LaunchAgents/com.unified.telegram-bot-igor.plist 2>/dev/null || true
    launchctl unload ~/Library/LaunchAgents/com.unified.telegram-bot-kostya.plist 2>/dev/null || true
    pkill -f "ai_telegram_bot_v2.py" || true
    echo "✅ Local bots stopped"
else
    echo "⏭️  Keeping local bots running"
fi

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                   🎉 Deployment Complete! 🎉                   ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "📊 Summary:"
echo "   • CORE Server: $CORE_IP"
echo "   • Igor's Dashboard: http://$CORE_IP:8096"
echo "   • Kostya's Dashboard: http://$CORE_IP:8098"
echo ""
echo "🔧 Management Commands (on CORE):"
echo "   sudo systemctl status telegram-bot-igor"
echo "   sudo systemctl restart telegram-bot-kostya"
echo "   sudo journalctl -u telegram-bot-igor -f"
echo ""
echo "📝 Logs:"
echo "   tailscale ssh $CORE_USER@$CORE_IP 'tail -f ~/Unified_System/Reports/*.log'"
echo ""
