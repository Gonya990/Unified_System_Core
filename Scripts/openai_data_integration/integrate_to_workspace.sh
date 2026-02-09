#!/bin/bash
# Workspace Integration Script | Скрипт интеграции в рабочее пространство
# English: Integrate processed OpenAI data into Unified_System workspace
# Russian: Интеграция обработанных данных OpenAI в рабочее пространство Unified_System

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Directories
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/../.." && pwd)"
CONFIG_FILE="${SCRIPT_DIR}/config.json"
PROCESSED_DIR="${SCRIPT_DIR}/data/processed"
KNOWLEDGE_BASE="${ROOT_DIR}/Agent_Context/Knowledge_Base"
OPENAI_KB_DIR="${KNOWLEDGE_BASE}/OpenAI_Conversations"

echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}   Workspace Integration | Интеграция в рабочее пространство${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo ""

# Check if processed data exists
if [ ! -d "${PROCESSED_DIR}" ] || [ -z "$(ls -A ${PROCESSED_DIR})" ]; then
    echo -e "${RED}English: No processed data found. Run process_conversations.py first.${NC}"
    echo -e "${RED}Russian: Обработанные данные не найдены. Сначала запустите process_conversations.py.${NC}"
    exit 1
fi

# Create backup if enabled
BACKUP_ENABLED=$(python3 -c "import json; print(json.load(open('${CONFIG_FILE}'))['integration']['backup_before_integration'])")

if [ "$BACKUP_ENABLED" = "True" ]; then
    echo -e "${YELLOW}English: Creating backup...${NC}"
    echo -e "${YELLOW}Russian: Создание резервной копии...${NC}"
    
    if [ -d "${OPENAI_KB_DIR}" ]; then
        BACKUP_DIR="${SCRIPT_DIR}/data/archive/backup_$(date +%Y%m%d_%H%M%S)"
        mkdir -p "${BACKUP_DIR}"
        cp -r "${OPENAI_KB_DIR}" "${BACKUP_DIR}/"
        echo -e "${GREEN}✓ Backup saved to ${BACKUP_DIR}${NC}"
    fi
fi

# Create OpenAI knowledge base directory
echo -e "${YELLOW}English: Creating knowledge base directory...${NC}"
echo -e "${YELLOW}Russian: Создание директории базы знаний...${NC}"
mkdir -p "${OPENAI_KB_DIR}"

# Copy processed conversations
echo -e "${YELLOW}English: Copying conversations...${NC}"
echo -e "${YELLOW}Russian: Копирование разговоров...${NC}"

COUNT=0
for file in "${PROCESSED_DIR}"/*.md; do
    if [ -f "$file" ]; then
        cp "$file" "${OPENAI_KB_DIR}/"
        COUNT=$((COUNT + 1))
    fi
done

echo -e "${GREEN}✓ Copied ${COUNT} conversation files${NC}"
echo -e "${GREEN}✓ Скопировано ${COUNT} файлов разговоров${NC}"

# Update AGENTS.md
UPDATE_AGENTS=$(python3 -c "import json; print(json.load(open('${CONFIG_FILE}'))['integration']['update_agents_md'])")

if [ "$UPDATE_AGENTS" = "True" ]; then
    echo -e "${YELLOW}English: Updating AGENTS.md...${NC}"
    echo -e "${YELLOW}Russian: Обновление AGENTS.md...${NC}"
    
    AGENTS_MD="${ROOT_DIR}/AGENTS.md"
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
    
    # Add entry to AGENTS.md if not exists
    if ! grep -q "OpenAI_Conversations" "${AGENTS_MD}"; then
        cat >> "${AGENTS_MD}" << EOF

## OpenAI ChatGPT Conversations Knowledge Base

**Location:** \`Agent_Context/Knowledge_Base/OpenAI_Conversations/\`

**Description:**
- **English:** Historical ChatGPT conversations imported from OpenAI export
- **Russian:** Исторические разговоры ChatGPT, импортированные из экспорта OpenAI

**Last Updated:** ${TIMESTAMP}

**Contents:** ${COUNT} conversation files

**Purpose:** Reference material for continuity, context, and learning from past interactions.

---
EOF
        echo -e "${GREEN}✓ Updated AGENTS.md${NC}"
    else
        echo -e "${YELLOW}ℹ AGENTS.md already contains OpenAI_Conversations section${NC}"
    fi
fi

# Create summary document
echo -e "${YELLOW}English: Creating integration summary...${NC}"
echo -e "${YELLOW}Russian: Создание сводки интеграции...${NC}"

SUMMARY_FILE="${OPENAI_KB_DIR}/INTEGRATION_SUMMARY.md"
cat > "${SUMMARY_FILE}" << EOF
# OpenAI Data Integration Summary
# Сводка интеграции данных OpenAI

**Integration Date | Дата интеграции:** $(date '+%Y-%m-%d %H:%M:%S')

## Statistics | Статистика

- **Total Conversations | Всего разговоров:** ${COUNT}
- **Source | Источник:** OpenAI ChatGPT Export
- **Format | Формат:** Markdown
- **Location | Расположение:** ${OPENAI_KB_DIR}

## Contents | Содержимое

See [INDEX.md](INDEX.md) for a complete list of conversations organized by date.

Смотрите [INDEX.md](INDEX.md) для полного списка разговоров, организованных по датам.

## Usage | Использование

**English:**
- These conversations serve as historical context
- Use them to maintain continuity across agent sessions
- Reference past solutions and approaches
- Learn from previous interactions

**Russian:**
- Эти разговоры служат историческим контекстом
- Используйте их для поддержания непрерывности между сессиями агента
- Ссылайтесь на прошлые решения и подходы
- Учитесь на предыдущих взаимодействиях

## Next Steps | Следующие шаги

1. Review the [INDEX.md](INDEX.md) to browse conversations
2. Configure profile mapping in \`config.json\`
3. Set up automated exports if desired

---

*Generated by OpenAI Data Integration System*
EOF

echo -e "${GREEN}✓ Created integration summary${NC}"

# Final summary
echo ""
echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}   Integration Complete | Интеграция завершена${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${BLUE}Integrated to: ${OPENAI_KB_DIR}${NC}"
echo -e "${BLUE}Интегрировано в: ${OPENAI_KB_DIR}${NC}"
echo ""
echo -e "${YELLOW}Next: Review the conversations and configure profile mapping${NC}"
echo -e "${YELLOW}Далее: Просмотрите разговоры и настройте сопоставление профиля${NC}"
echo ""
