#!/bin/bash
# OpenAI Data Export Script | Скрипт экспорта данных OpenAI
# English: Automates the process of exporting ChatGPT data
# Russian: Автоматизирует процесс экспорта данных ChatGPT

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Directories
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="${SCRIPT_DIR}/config.json"
DOWNLOAD_DIR="${SCRIPT_DIR}/data/raw"
NODRIVER_DIR="/Users/macbook/Documents/Unified_System/External_Tools/nodriver"
NDC="${NODRIVER_DIR}/ndc"

# Ensure directories exist
mkdir -p "${DOWNLOAD_DIR}"

echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}   OpenAI Data Export | Экспорт данных OpenAI${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo ""

# Check if nodriver daemon is running
echo -e "${YELLOW}English: Checking nodriver daemon status...${NC}"
echo -e "${YELLOW}Russian: Проверка статуса демона nodriver...${NC}"

if ! "${NDC}" status &>/dev/null; then
    echo -e "${YELLOW}English: Starting nodriver daemon...${NC}"
    echo -e "${YELLOW}Russian: Запуск демона nodriver...${NC}"
    cd "${NODRIVER_DIR}"
    ./start_daemon.sh
    sleep 3
fi

echo -e "${GREEN}✓ Daemon is running | Демон запущен${NC}"
echo ""

# Step 1: Navigate to ChatGPT
echo -e "${BLUE}Step 1 | Шаг 1: Opening ChatGPT...${NC}"
"${NDC}" goto "https://chatgpt.com"
sleep 2

echo -e "${YELLOW}English: Please log in to your OpenAI account in the opened browser window.${NC}"
echo -e "${YELLOW}Russian: Пожалуйста, войдите в свою учетную запись OpenAI в открытом окне браузера.${NC}"
echo ""
echo -e "${YELLOW}Press ENTER when you are logged in...${NC}"
echo -e "${YELLOW}Нажмите ENTER, когда войдете в систему...${NC}"
read -r

# Step 2: Navigate to Settings
echo -e "${BLUE}Step 2 | Шаг 2: Opening Settings...${NC}"
"${NDC}" click 'button[aria-label="Settings"]' || "${NDC}" click 'div[class*="settings"]' || true
sleep 1

# Try multiple selectors for the settings menu
echo -e "${BLUE}Step 3 | Шаг 3: Finding Data Controls...${NC}"
"${NDC}" click 'text=Data controls' || "${NDC}" click 'a:has-text("Data controls")' || true
sleep 1

# Step 4: Click Export
echo -e "${BLUE}Step 4 | Шаг 4: Clicking Export button...${NC}"
"${NDC}" click 'button:has-text("Export")' || "${NDC}" click 'button[type="button"]:has-text("Export")' || true
sleep 1

# Step 5: Confirm Export
echo -e "${BLUE}Step 5 | Шаг 5: Confirming export...${NC}"
"${NDC}" click 'button:has-text("Confirm export")' || "${NDC}" click 'button:has-text("Confirm")' || true

echo ""
echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}   Export Request Sent | Запрос на экспорт отправлен${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}English: Check your email for the download link from OpenAI.${NC}"
echo -e "${YELLOW}Russian: Проверьте вашу электронную почту на наличие ссылки для скачивания от OpenAI.${NC}"
echo ""
echo -e "${YELLOW}English: The link will expire in 24 hours.${NC}"
echo -e "${YELLOW}Russian: Ссылка истечет через 24 часа.${NC}"
echo ""
echo -e "${BLUE}When you receive the email with the download link:${NC}"
echo -e "${BLUE}Когда вы получите письмо со ссылкой для скачивания:${NC}"
echo ""
echo -e "  ${YELLOW}1. Download the .zip file to: ${DOWNLOAD_DIR}${NC}"
echo -e "  ${YELLOW}2. Run: ./process_conversations.py${NC}"
echo ""

# Check for auto-integrate flag
if [[ "$1" == "--auto-integrate" ]]; then
    echo -e "${YELLOW}Waiting for downloaded file...${NC}"
    echo -e "${YELLOW}Ожидание загруженного файла...${NC}"
    
    # Wait for zip file to appear (max 5 minutes)
    TIMEOUT=300
    ELAPSED=0
    while [ $ELAPSED -lt $TIMEOUT ]; do
        ZIP_FILE=$(find "${DOWNLOAD_DIR}" -name "*.zip" -type f -mmin -10 2>/dev/null | head -n 1)
        if [[ -n "$ZIP_FILE" ]]; then
            echo -e "${GREEN}✓ Found downloaded file: ${ZIP_FILE}${NC}"
            
            # Extract
            echo -e "${BLUE}Extracting...${NC}"
            unzip -o "$ZIP_FILE" -d "${DOWNLOAD_DIR}"
            
            # Process
            echo -e "${BLUE}Processing conversations...${NC}"
            python3 "${SCRIPT_DIR}/process_conversations.py" "${DOWNLOAD_DIR}/conversations.json"
            
            # Integrate
            echo -e "${BLUE}Integrating to workspace...${NC}"
            "${SCRIPT_DIR}/integrate_to_workspace.sh"
            
            echo -e "${GREEN}✓ Complete! | Завершено!${NC}"
            exit 0
        fi
        sleep 10
        ELAPSED=$((ELAPSED + 10))
    done
    
    echo -e "${RED}Timeout waiting for download. Please run manually.${NC}"
    echo -e "${RED}Тайм-аут ожидания загрузки. Пожалуйста, запустите вручную.${NC}"
fi

echo -e "${GREEN}Done! | Готово!${NC}"
