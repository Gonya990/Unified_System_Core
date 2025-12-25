# OpenAI Data Integration | Интеграция данных OpenAI

## Overview | Обзор

**English:** This directory contains scripts and automation to extract, process, and integrate your OpenAI ChatGPT data into the Unified_System workspace.

**Russian:** Эта директория содержит скрипты и автоматизацию для извлечения, обработки и интеграции ваших данных OpenAI ChatGPT в рабочее пространство Unified_System.

## Features | Возможности

### 1. Data Export | Экспорт данных

- **English:** Automated browser workflow to export ChatGPT data
- **Russian:** Автоматизированный браузерный процесс для экспорта данных ChatGPT

### 2. Data Processing | Обработка данных

- **English:** Parse and structure conversations.json
- **Russian:** Парсинг и структурирование conversations.json

### 3. Integration | Интеграция

- **English:** Import conversations into Agent_Context/Knowledge_Base
- **Russian:** Импорт разговоров в Agent_Context/Knowledge_Base

### 4. Profile Mapping | Сопоставление профиля

- **English:** Map OpenAI preferences to Antigravity agent settings
- **Russian:** Сопоставление настроек OpenAI с настройками агента Antigravity

## Directory Structure | Структура директории

```
openai_data_integration/
├── README.md                          # This file | Этот файл
├── export_openai_data.sh              # Main export script | Основной скрипт экспорта
├── process_conversations.py           # Process conversations.json | Обработка conversations.json
├── integrate_to_workspace.sh          # Integration script | Скрипт интеграции
├── config.json                        # Configuration | Конфигурация
├── data/                              # Downloaded data | Загруженные данные
│   ├── raw/                           # Raw exports | Исходные экспорты
│   ├── processed/                     # Processed data | Обработанные данные
│   └── archive/                       # Historical exports | Исторические экспорты
└── templates/                         # Document templates | Шаблоны документов
```

## Quick Start | Быстрый старт

### Step 1: Export Data from OpenAI | Шаг 1: Экспорт данных из OpenAI

**English:**

```bash
./export_openai_data.sh
```

This will open Chrome and guide you through the export process.

**Russian:**

```bash
./export_openai_data.sh
```

Это откроет Chrome и проведет вас через процесс экспорта.

### Step 2: Process Data | Шаг 2: Обработка данных

**English:**

```bash
python3 process_conversations.py data/raw/conversations.json
```

**Russian:**

```bash
python3 process_conversations.py data/raw/conversations.json
```

### Step 3: Integrate | Шаг 3: Интеграция

**English:**

```bash
./integrate_to_workspace.sh
```

**Russian:**

```bash
./integrate_to_workspace.sh
```

## Automated Workflow | Автоматизированный процесс

**English:** After initial setup, you can run the complete workflow:

**Russian:** После начальной настройки вы можете запустить полный процесс:

```bash
./export_openai_data.sh --auto-integrate
```

## Configuration | Конфигурация

Edit `config.json` to customize:

- Export frequency | Частота экспорта
- Data retention | Хранение данных
- Integration targets | Цели интеграции
- Profile mapping | Сопоставление профиля

## Data Privacy | Конфиденциальность данных

**English:** All data is stored locally. No external services are used except OpenAI.

**Russian:** Все данные хранятся локально. Никакие внешние сервисы не используются, кроме OpenAI.

## Troubleshooting | Устранение неполадок

### Export link expired | Ссылка на экспорт истекла

**English:** Export links are valid for 24 hours. Request a new export from OpenAI settings.

**Russian:** Ссылки на экспорт действительны 24 часа. Запросите новый экспорт в настройках OpenAI.

### Browser automation fails | Автоматизация браузера не работает

**English:** Make sure nodriver daemon is running:

```bash
cd /Users/macbook/Documents/Unified_System/External_Tools/nodriver
./start_daemon.sh
```

**Russian:** Убедитесь, что демон nodriver запущен:

```bash
cd /Users/macbook/Documents/Unified_System/External_Tools/nodriver
./start_daemon.sh
```
