#!/bin/bash
set -e

echo "🚀 Начинаем изолированную сборку iOS (Fake Monorepo Strategy)..."

# Пути
TMP_DIR="/tmp/Monorepo_Fake_$$"
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 1. Очистка и создание структуры
echo "🧹 Создание временной структуры сервера Expo..."
rm -rf $TMP_DIR
mkdir -p $TMP_DIR/Projects

# 2. Копирование проекта
echo "📂 Копирование мобильного приложения (отсечение тяжелых медиафайлов)..."
cp -r $PROJECT_DIR $TMP_DIR/Projects/

# 3. Инициализация фейкового Git-репозитория
echo "🔧 Инициализация чистого Git-репозитория..."
cd $TMP_DIR
git init > /dev/null
git add .
git commit -m "fake monorepo init" > /dev/null

# 4. Подготовка проекта
echo "📦 Установка зависимостей (npm install)..."
cd Projects/UnifiedCoreMobile
# Удаляем тяжелые папки, если они скопировались, чтобы npm install установил всё начисто
rm -rf node_modules ios ios_backup .expo
npm install --silent

# 5. Запуск сборки
echo "🏗 Запуск EAS Build..."
# Запускаем сборку. Вы можете убрать флаг --non-interactive, если хотите отвечать на вопросы CLI.
npx eas-cli build --platform ios --profile production

echo "✅ Сборка завершена!"
echo "🗑 Удаление временных файлов..."
rm -rf $TMP_DIR
