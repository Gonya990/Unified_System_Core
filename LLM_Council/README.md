# 🏛️ LLM Council

> **Multi-LLM Deliberation System** inspired by [Karpathy's llm-council](https://github.com/karpathy/llm-council)

## 🎯 Концепция

Система, где несколько AI-моделей совещаются как экспертная панель:

1. **Stage 1**: Каждая модель отвечает независимо
2. **Stage 2**: Peer Review — модели оценивают ответы друг друга
3. **Stage 3**: Chairman синтезирует финальный консенсус

## 🔌 Поддерживаемые провайдеры

| Provider | Models | Status |
|----------|--------|--------|
| **OpenAI** | GPT-4o, GPT-4-turbo, o1 | ✅ Ready |
| **GitHub Copilot** | Codex, GPT-4 | ✅ Ready |
| **NVIDIA NIM** | Llama, Mixtral, Nemotron | ✅ Ready |

## 🚀 Quick Start

```bash
# 1. Активировать venv
source /Users/macbook/Documents/.venv/bin/activate

# 2. Установить зависимости
pip install -r requirements.txt

# 3. Настроить API ключи
cp .env.example .env
# Заполнить .env своими ключами

# 4. Запустить демо
python council_demo.py "Как оптимизировать Python код?"
```

## 📁 Структура

```
LLM_Council/
├── council/
│   ├── __init__.py
│   ├── providers/           # LLM провайдеры
│   │   ├── base.py          # Базовый класс
│   │   ├── openai_provider.py
│   │   ├── github_copilot.py
│   │   └── nvidia_nim.py
│   ├── council.py           # Основная логика Council
│   └── chairman.py          # Chairman LLM (синтез)
├── .env.example
├── requirements.txt
└── council_demo.py
```

## ⚙️ Конфигурация

```env
# OpenAI
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o

# GitHub Copilot
GITHUB_TOKEN=ghp_...

# NVIDIA NIM
NVIDIA_API_KEY=nvapi-...
NVIDIA_MODEL=meta/llama-3.1-70b-instruct
```

## 🧠 Как это работает

```
User Query
    │
    ▼
┌───────────────────────────────────────┐
│  STAGE 1: Independent Responses       │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐     │
│  │GPT-4│ │Copilot│ │Llama│ │Mixtral│ │
│  └──┬──┘ └──┬───┘ └──┬──┘ └──┬───┘    │
└─────┼───────┼────────┼───────┼────────┘
      │       │        │       │
      ▼       ▼        ▼       ▼
┌───────────────────────────────────────┐
│  STAGE 2: Peer Review                 │
│  Each model rates others (1-10)       │
└───────────────────┬───────────────────┘
                    │
                    ▼
┌───────────────────────────────────────┐
│  STAGE 3: Chairman Synthesis          │
│  👑 Antigravity (Claude/GPT-4o)       │
│  → Combines best insights             │
│  → Resolves conflicts                 │
│  → Outputs final consensus            │
└───────────────────┬───────────────────┘
                    │
                    ▼
            Final Response
```

---

**Author:** Unified System  
**Created:** 2024-12-24
