# Installation Guide / Инструкция по установке

## 1. Transfer Files / Перенос файлов

Run this command from your MacBook to copy the project to the Windows machine:
Выполните эту команду на MacBook для копирования проекта на Windows машину:

```bash
scp -r /Users/macbook/Documents/Unified_System/Projects/AI_Core gonya@100.127.194.111:Desktop/
```

## 2. Remote Setup / Удаленная установка

Connect via SSH and run the setup script:
Подключитесь по SSH и запустите скрипт настройки:

```bash
ssh gonya@100.127.194.111
cd Desktop/AI_Core/scripts
powershell -ExecutionPolicy Bypass -File setup_with_uv.ps1
```

## 3. Run AI Agent / Запуск AI Агента

```bash
cd ../src
python ai_telegram_bot.py
```
