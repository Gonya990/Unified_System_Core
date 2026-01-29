#!/bin/bash

# GitHub Token Setup and Verification Script
# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║       GitHub Token Setup & Verification Tool            ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""

# Функция для проверки токена
check_token() {
    local token=$1
    echo -e "${YELLOW}🔍 Проверка токена...${NC}"
    
    # Проверка базовой авторизации
    response=$(curl -s -H "Authorization: token $token" https://api.github.com/user)
    
    if echo "$response" | grep -q "\"login\""; then
        username=$(echo "$response" | grep -o '"login": *"[^"]*"' | cut -d'"' -f4)
        echo -e "${GREEN}✅ Токен действителен!${NC}"
        echo -e "${GREEN}   Пользователь: $username${NC}"
        
        # Проверка прав доступа
        echo -e "\n${YELLOW}🔐 Проверка прав доступа...${NC}"
        scopes=$(curl -s -I -H "Authorization: token $token" https://api.github.com/user | grep -i "x-oauth-scopes" | cut -d':' -f2- | tr -d ' \r')
        
        if [ -n "$scopes" ]; then
            echo -e "${BLUE}   Доступные права:${NC}"
            IFS=',' read -ra SCOPE_ARRAY <<< "$scopes"
            for scope in "${SCOPE_ARRAY[@]}"; do
                echo -e "${GREEN}   ✓ $scope${NC}"
            done
        else
            echo -e "${YELLOW}   ⚠️  Не удалось получить список прав${NC}"
        fi
        
        # Проверка доступа к репозиториям
        echo -e "\n${YELLOW}📦 Проверка доступа к репозиториям...${NC}"
        repos=$(curl -s -H "Authorization: token $token" "https://api.github.com/user/repos?per_page=5" | grep -o '"full_name": *"[^"]*"' | cut -d'"' -f4)
        
        if [ -n "$repos" ]; then
            echo -e "${GREEN}   Доступные репозитории (первые 5):${NC}"
            echo "$repos" | while read -r repo; do
                echo -e "${GREEN}   ✓ $repo${NC}"
            done
        fi
        
        return 0
    else
        echo -e "${RED}❌ Токен недействителен или истек!${NC}"
        echo -e "${RED}   Ответ API: $response${NC}"
        return 1
    fi
}

# Главное меню
echo -e "${YELLOW}Выберите действие:${NC}"
echo "1. Проверить текущий токен из переменной окружения"
echo "2. Проверить новый токен (временно, не сохраняя)"
echo "3. Сохранить новый токен в ~/.zshrc"
echo "4. Открыть GitHub Settings для создания/отзыва токена"
echo "5. Показать рекомендуемые права для токена"
echo ""
read -p "$(echo -e ${BLUE}Ваш выбор [1-5]: ${NC})" choice

case $choice in
    1)
        if [ -n "$GITHUB_TOKEN" ]; then
            check_token "$GITHUB_TOKEN"
        else
            echo -e "${RED}❌ Переменная GITHUB_TOKEN не установлена!${NC}"
            echo -e "${YELLOW}Выполните: source ~/.zshrc${NC}"
        fi
        ;;
    2)
        read -sp "$(echo -e ${BLUE}Введите токен для проверки: ${NC})" test_token
        echo ""
        if [ -n "$test_token" ]; then
            check_token "$test_token"
        else
            echo -e "${RED}❌ Токен не может быть пустым${NC}"
        fi
        ;;
    3)
        read -sp "$(echo -e ${BLUE}Введите новый токен: ${NC})" new_token
        echo ""
        if [ -n "$new_token" ]; then
            # Сначала проверяем токен
            if check_token "$new_token"; then
                # Обновляем ~/.zshrc
                if grep -q "export GITHUB_TOKEN=" ~/.zshrc; then
                    # Заменяем существующую строку (безопасно)
                    sed -i '' "s|export GITHUB_TOKEN=.*|export GITHUB_TOKEN=\"$new_token\"|" ~/.zshrc
                    echo -e "\n${GREEN}✅ Токен обновлен в ~/.zshrc${NC}"
                else
                    # Добавляем новую строку
                    echo "" >> ~/.zshrc
                    echo "# GitHub Personal Access Token (автоматически добавлено)" >> ~/.zshrc
                    echo "export GITHUB_TOKEN=\"$new_token\"" >> ~/.zshrc
                    echo -e "\n${GREEN}✅ Токен добавлен в ~/.zshrc${NC}"
                fi
                echo -e "${YELLOW}Выполните: source ~/.zshrc${NC}"
            fi
        else
            echo -e "${RED}❌ Токен не может быть пустым${NC}"
        fi
        ;;
    4)
        echo -e "${BLUE}🌐 Открываю GitHub Settings...${NC}"
        open "https://github.com/settings/tokens"
        echo -e "${GREEN}✅ Откройте браузер для управления токенами${NC}"
        ;;
    5)
        echo -e "\n${BLUE}╔══════════════════════════════════════════════════════════╗${NC}"
        echo -e "${BLUE}║     Рекомендуемые права для GitHub токена (IDE)         ║${NC}"
        echo -e "${BLUE}╚══════════════════════════════════════════════════════════╝${NC}"
        echo ""
        echo -e "${GREEN}Обязательные права для работы с IDE:${NC}"
        echo -e "  ${YELLOW}✓${NC} repo                 - Полный доступ к приватным репозиториям"
        echo -e "  ${YELLOW}✓${NC} workflow             - Управление GitHub Actions workflows"
        echo -e "  ${YELLOW}✓${NC} read:org             - Чтение организационных данных"
        echo -e "  ${YELLOW}✓${NC} user                 - Доступ к профилю пользователя"
        echo ""
        echo -e "${BLUE}Дополнительные права (опционально):${NC}"
        echo -e "  ${YELLOW}○${NC} gist                 - Создание и управление gists"
        echo -e "  ${YELLOW}○${NC} notifications        - Доступ к уведомлениям"
        echo -e "  ${YELLOW}○${NC} read:discussion      - Чтение обсуждений"
        echo ""
        echo -e "${RED}⚠️  Не давайте права:${NC}"
        echo -e "  ${RED}✗${NC} delete_repo          - Удаление репозиториев (опасно!)"
        echo -e "  ${RED}✗${NC} admin:public_key     - Управление SSH ключами (если не нужно)"
        echo ""
        ;;
    *)
        echo -e "${RED}❌ Неверный выбор${NC}"
        ;;
esac

echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
