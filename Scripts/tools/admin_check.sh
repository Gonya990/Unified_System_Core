#!/bin/bash

# Конфигурация / Configuration
ALLOWED_USERS=("igor" "gonya" "macbook")
REQUIRED_LOCALE="ru_RU.UTF-8"
SYSTEM_ROOT="/Users/macbook/Documents/Unified_System"

# Цвета для вывода / Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== СИСТЕМНАЯ ПРОВЕРКА / SYSTEM CHECK ===${NC}"
echo -e "${BLUE}=== Дата: $(date) ===${NC}"

# 1. Проверка пользователя / Check User
CURRENT_USER=$(whoami)
echo -n "Проверка пользователя [$CURRENT_USER]... "
if [[ " ${ALLOWED_USERS[*]} " =~ " ${CURRENT_USER} " ]]; then
    echo -e "${GREEN}ДОСТУП РАЗРЕШЕН${NC}"
else
    echo -e "${RED}ДОСТУП ЗАПРЕЩЕН. Требуется: igor/gonya${NC}"
fi

# 2. Проверка локали / Check Locale
echo -n "Проверка языковой среды... "
if [[ "$LANG" == *"$REQUIRED_LOCALE"* ]] || [[ "$LC_ALL" == *"$REQUIRED_LOCALE"* ]]; then
     echo -e "${GREEN}Русская локаль активна${NC}"
else
    echo -e "${RED}ВНИМАНИЕ: Текущая локаль $LANG. Рекомендуется установить $REQUIRED_LOCALE${NC}"
    export LANG="$REQUIRED_LOCALE"
    export LC_ALL="$REQUIRED_LOCALE"
    echo -e "${GREEN}Переменные среды временно обновлены для этой сессии.${NC}"
fi

# 3. Инвентаризация ресурсов / Resource Inventory
echo -e "\n${BLUE}=== РЕСУРСЫ СИСТЕМЫ (Inventory) ===${NC}"

# Функция проверки папки
check_dir() {
    local path="$1"
    local name="$2"
    if [ -d "$path" ]; then
        echo -e "${GREEN}[OK]${NC} $name найден: $path"
        return 0
    else
        echo -e "${RED}[FAIL]${NC} $name НЕ найден: $path"
        return 1
    fi
}

echo "1. Хост: $(hostname)"
echo "2. Проверка рабочих зон:"

check_dir "$SYSTEM_ROOT/Projects/AI_Core" "AI Core (Unified)"
check_dir "$SYSTEM_ROOT/Home_Assistant_Config" "Home Assistant"
check_dir "$SYSTEM_ROOT/Sandbox" "Песочница"

# Проверка на чувствительные файлы
echo -e "\n${YELLOW}=== ПРОВЕРКА БЕЗОПАСНОСТИ ===${NC}"
SENSITIVE_FILES=("Токен ХА для Васи.odt" "ключи Ngrok.odt")
FOUND_SENSITIVE=0
for file in "${SENSITIVE_FILES[@]}"; do
    if [ -f "$SYSTEM_ROOT/Home_Assistant_Config/$file" ]; then
        echo -e "${RED}[WARNING]${NC} Обнаружен чувствительный файл: $file"
        FOUND_SENSITIVE=1
    fi
done

if [ $FOUND_SENSITIVE -eq 1 ]; then
    echo -e "${RED}РЕКОМЕНДАЦИЯ: Переместить эти файлы в защищенное хранилище!${NC}"
else
    echo -e "${GREEN}Чувствительные файлы в открытом виде не найдены (из списка известных).${NC}"
fi

echo -e "\n${GREEN}Системная проверка завершена.${NC}"
