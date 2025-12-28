#!/bin/bash
# remind_kostya.sh - Send reminder to Kostya about Agent Mail setup
# Runs via cron twice daily (10:00 and 18:00)

TELEGRAM_BOT_TOKEN="${TELEGRAM_BOT_TOKEN:-8518131338:AAFzuwI6PJ7ftiZVe3u8cWtjYz1pSU_QIqQ}"
KOSTYA_CHAT_ID="578363419"

MESSAGE="🤖 *Напоминание от Antigravity*

Привет! Это автоматическое напоминание.

📬 Система Agent Mail ждёт твоего агента!

Подключи своего агента:
\`\`\`
Server: http://100.88.65.71:8765
Token: antigravity_secret
Project: main
\`\`\`

📚 Инструкция: \`Agent_Context/Knowledge_Base/HOW_TO_GIVE_ANOTHER_AGENT_ACCESS_TO_MCP_AGENT_MAIL.md\`

GitHub Repo: github.com/Gonya990/Unified_System_Core

Ответь 'done' когда подключишься! 🚀"

curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
  -d chat_id="${KOSTYA_CHAT_ID}" \
  -d text="${MESSAGE}" \
  -d parse_mode="Markdown" > /dev/null

echo "$(date): Reminder sent to Kostya" >> /tmp/remind_kostya.log
