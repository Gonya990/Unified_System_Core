#!/bin/bash
# Quick Start - OpenAI Data Integration
# Быстрый старт - Интеграция данных OpenAI

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

clear

echo -e "${BLUE}"
cat << "EOF"
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   OpenAI ChatGPT Data Integration System                    ║
║   Система интеграции данных OpenAI ChatGPT                   ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

echo ""
echo -e "${YELLOW}English: Welcome to the OpenAI Data Integration System!${NC}"
echo -e "${YELLOW}Russian: Добро пожаловать в систему интеграции данных OpenAI!${NC}"
echo ""
echo -e "${GREEN}This tool will help you:${NC}"
echo -e "${GREEN}Этот инструмент поможет вам:${NC}"
echo ""
echo "  1. Export your ChatGPT conversation history"
echo "     Экспортировать историю разговоров ChatGPT"
echo ""
echo "  2. Extract your profile and preferences"
echo "     Извлечь ваш профиль и настройки"
echo ""
echo "  3. Integrate everything into Unified_System"
echo "     Интегрировать все в Unified_System"
echo ""
echo -e "${BLUE}═════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}Choose an option | Выберите опцию:${NC}"
echo ""
echo "  1) Full automated export and integration"
echo "     Полностью автоматизированный экспорт и интеграция"
echo ""
echo "  2) Manual step-by-step process"
echo "     Пошаговый ручной процесс"
echo ""
echo "  3) Extract profile only"
echo "     Извлечь только профиль"
echo ""
echo "  4) View documentation"
echo "     Просмотреть документацию"
echo ""
echo "  5) Exit | Выход"
echo ""
echo -n "Enter choice [1-5]: "
read -r choice

case $choice in
    1)
        echo ""
        echo -e "${BLUE}Starting automated export...${NC}"
        echo -e "${BLUE}Запуск автоматизированного экспорта...${NC}"
        echo ""
        ./export_openai_data.sh --auto-integrate
        ;;
    2)
        echo ""
        echo -e "${BLUE}Step 1: Export data from OpenAI${NC}"
        echo -e "${BLUE}Шаг 1: Экспорт данных из OpenAI${NC}"
        echo ""
        echo "Run: ./export_openai_data.sh"
        echo ""
        echo -e "${YELLOW}Press ENTER to continue...${NC}"
        read -r
        ./export_openai_data.sh
        
        echo ""
        echo -e "${BLUE}Step 2: After downloading, process conversations${NC}"
        echo -e "${BLUE}Шаг 2: После загрузки обработайте разговоры${NC}"
        echo ""
        echo "Run: python3 process_conversations.py data/raw/conversations.json"
        echo ""
        echo -e "${YELLOW}Have you downloaded and extracted the data? (y/n):${NC}"
        read -r downloaded
        
        if [[ "$downloaded" == "y" ]]; then
            python3 process_conversations.py data/raw/conversations.json
            
            echo ""
            echo -e "${BLUE}Step 3: Integrate to workspace${NC}"
            echo -e "${BLUE}Шаг 3: Интеграция в рабочее пространство${NC}"
            echo ""
            ./integrate_to_workspace.sh
            
            echo ""
            echo -e "${BLUE}Step 4: Extract profile${NC}"
            echo -e "${BLUE}Шаг 4: Извлечение профиля${NC}"
            echo ""
            python3 extract_profile.py
        fi
        ;;
    3)
        echo ""
        echo -e "${BLUE}Extracting profile...${NC}"
        echo -e "${BLUE}Извлечение профиля...${NC}"
        echo ""
        python3 extract_profile.py
        ;;
    4)
        echo ""
        less README.md
        ;;
    5)
        echo ""
        echo -e "${GREEN}Goodbye! | До свидания!${NC}"
        echo ""
        exit 0
        ;;
    *)
        echo ""
        echo -e "${YELLOW}Invalid choice | Неверный выбор${NC}"
        echo ""
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}═════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}   Process Complete! | Процесс завершен!${NC}"
echo -e "${GREEN}═════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}Your data is now integrated into:${NC}"
echo -e "${YELLOW}Ваши данные теперь интегрированы в:${NC}"
echo ""
echo "  📁 Agent_Context/Knowledge_Base/OpenAI_Conversations/"
echo "  📁 Agent_Context/agent_preferences.json"
echo ""
echo -e "${BLUE}You can find the index at:${NC}"
echo -e "${BLUE}Вы можете найти индекс в:${NC}"
echo ""
echo "  📄 Agent_Context/Knowledge_Base/OpenAI_Conversations/INDEX.md"
echo ""
