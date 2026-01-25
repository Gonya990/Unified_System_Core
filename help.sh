#!/bin/bash
# Quick help script for Unified System Core
# Usage: ./help.sh [topic]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$SCRIPT_DIR"

print_help() {
    cat << EOF
🆘 Unified System Core - Help Menu
==========================================

Usage: ./help.sh [topic]

Available Topics:
  check       - Run system health check
  start       - How to start the AI bot
  env         - Environment setup guide  
  git         - Git commands and workflow
  docs        - View documentation links
  
Examples:
  ./help.sh check      # Run diagnostics
  ./help.sh start      # Show how to start bot
  ./help.sh            # Show this menu

For detailed troubleshooting, see: TROUBLESHOOTING.md
==========================================
EOF
}

show_check() {
    echo "🏥 Running System Health Check..."
    echo "=================================="
    python3 "$ROOT_DIR/Scripts/Utilities/system_health_check.py"
}

show_start() {
    cat << EOF
🚀 Starting the AI Bot
======================

1. Install dependencies:
   cd Projects/AI_Core
   pip install -r requirements.txt

2. Setup environment:
   cp .env.example .env.local
   # Edit .env.local with your API keys

3. Run the bot:
   cd Projects/AI_Core
   python3 main.py

For more details: Projects/AI_Core/README.md
EOF
}

show_env() {
    cat << EOF
⚙️ Environment Setup
====================

1. Copy example file:
   cp .env.example .env.local

2. Required API Keys:
   - TELEGRAM_BOT_TOKEN (from @BotFather)
   - OPENAI_API_KEY (from OpenAI)
   - GEMINI_API_KEY (from Google AI)
   - HOME_ASSISTANT_TOKEN (optional)
   - GOOGLE_CALENDAR_CREDS (optional)

3. Test your setup:
   python3 Scripts/Utilities/system_health_check.py

For details: TROUBLESHOOTING.md
EOF
}

show_git() {
    cat << EOF
📦 Git Commands
===============

Check status:
  git status

View changes:
  git diff

Commit changes:
  git add .
  git commit -m "Your message"
  git push

Pull latest:
  git pull

For issues: TROUBLESHOOTING.md (Section 4)
EOF
}

show_docs() {
    cat << EOF
📚 Documentation Links
======================

Main Docs:
- README.md              - Project overview
- TROUBLESHOOTING.md     - Problem solving
- CLAUDE.md              - Agent guidelines
- SYSTEM_MAP.md          - Architecture map

Project Specific:
- Projects/AI_Core/README.md          - AI Bot docs
- Agent_Context/Knowledge_Base/       - AI context
- docs/                              - Additional docs

Quick Start:
  cat README.md | less
EOF
}

# Main logic
case "${1:-}" in
    check)
        show_check
        ;;
    start)
        show_start
        ;;
    env)
        show_env
        ;;
    git)
        show_git
        ;;
    docs)
        show_docs
        ;;
    *)
        print_help
        ;;
esac
