# 🧠 FORMA_MEMORY.md — Суверенная Память Архитектора
>
> **СТАТУС**: ЖИВОЙ ДОКУМЕНТ | Не редактировать вручную без понимания последствий  
> **Версия памяти**: v0.2  
> **Последнее обновление**: 2026-06-11  
> **Автор**: Evolving Sovereign Systems Architect (FORMA)

---

## 📌 SECTION 1 — Внутренняя модель пользователя (Igor Goncharenko)

### Идентичность и контекст

- **Имя**: Игорь Гончаренко
- **Локация**: Израиль (с 2024-2025, из контекста файлов)
- **Профиль**: Основатель-технолог, Software Architect, AI Systems Builder
- **GitHub**: gonya990 / gonya90.gg

### Стиль мышления и работы

- Мыслит **системами**, а не фичами. Строит не приложения — строит **Суверенные Системы**
- Архитектурное мышление: предпочитает сначала карту, потом детали
- **Высокая нетерпимость к Rework Tax** — всё делается правильно с первого раза
- Работает **параллельными потоками**: одновременно несколько проектов в разных доменах
- Документирует систему через `.md` файлы (VISION, SYSTEM_MAP, CLAUDE, STATUS_NOW, CHANGELOG)
- Использует **несколько AI-ассистентов** параллельно (Claude, Gemini Antigravity, Copilot, Codex)

### Язык и коммуникация

- Основной язык работы: **Русский**
- Технические термины и код: **English**
- Ожидает: системные ответы, чёткую структуру, ссылки на предыдущий опыт

### Ценности (из VISION.md + поведенческих паттернов)

1. **Суверенитет данных** — абсолютный приоритет
2. **Автономия системы** — цель: 30 дней без ручного вмешательства
3. **Ноль шума** — только критически важные уведомления
4. **Финансовая независимость** — торговые боты, пассивный доход
5. **Контентное господство** — 10+ клипов/день на 5+ платформах

---

## 📌 SECTION 2 — Карта Unified_System_Core

### Топология системы

```
Unified_System_Core/                          ← Корень суверенной системы
├── Projects/                                 ← Кодовые базы
│   ├── UnifiedCoreMobile/                    ← 🔴 АКТИВНЫЙ: iOS командный центр
│   ├── AI_Core/                              ← Telegram AI бот (основной агент)
│   ├── AgentBridge/                          ← Мост агентов
│   ├── Business_Intelligence/                ← BI система
│   ├── Bybit_Bot/ + Bybit_Arb_Bot/          ← Криптотрейдинг
│   ├── Content_Factory/                      ← Фабрика контента (видео, TikTok)
│   ├── ChatKit_Dashboard/                    ← Веб-дашборд
│   ├── Personal_Assistant/                   ← Персональный ассистент
│   ├── connect-landing-page/                 ← Лендинг
│   └── telegram_bot/                         ← Telegram бот (другой экземпляр?)
├── Scripts/
│   ├── Orchestration/                        ← full_sync.sh — главный оркестратор
│   └── Production_Factory/                   ← Видео-пайплайн
├── Agent_Context/                            ← Контекст для агентов
├── Agent_Workflows/                          ← Воркфлоу агентов
├── LLM_Council/                              ← Совет LLM-моделей
├── sovereign-core/                           ← Суверенное ядро
├── Home_Assistant_Config/                    ← Умный дом
├── services/                                 ← Сервисы
├── functions/                                ← Firebase Cloud Functions
└── [System docs: VISION, SYSTEM_MAP, CLAUDE, CHANGELOG, STATUS_NOW...]
```

### Инфраструктура (обнаруженная)

- **Cloud**: Firebase (project: `unified-core-agent-db`), GKE (Google Kubernetes Engine)
- **CI/CD**: EAS Build (Expo), GitHub Actions
- **Database**: Firestore, SQLite (локальные: health.db, tasks.db, usage.db)
- **AI Stack**: Vertex AI (Gemini), OpenAI (GPT), ElevenLabs (TTS)
- **Bot**: Telegram (основной интерфейс управления)
- **Home**: Home Assistant (RTSP, умные устройства)
- **Trading**: Bybit API (криптотрейдинг)

---

## 📌 SECTION 3 — UnifiedCoreMobile (АКТИВНЫЙ ПРОЕКТ)

### Технический стек

```
Framework:     Expo SDK 56 + React Native 0.85.3
Language:      TypeScript 6.0
Navigation:    expo-router (file-based) + Drawer Navigation
State:         React useState (локальный, пока без глобального стора)
Backend:       Firebase (Firestore + Auth анонимная)
Build:         EAS Build → iOS Production
```

### Экраны приложения (из _layout.tsx)

| Экран | Route | Назначение |
|---|---|---|
| Chat | `index.tsx` | 💬 AI-чат (главный) — сейчас Mock |
| Dashboard | `dashboard.tsx` | 📊 Системный дашборд |
| Services | `services.tsx` | 🔧 Управление сервисами |
| Commands | `commands.tsx` | ⌨️ Командный терминал |
| Logs | `logs.tsx` | 📋 Логи системы |
| Settings | `settings.tsx` | ⚙️ Настройки |

### Архитектура кода

```
src/
├── app/            ← Expo Router экраны (8 файлов)
├── components/     ← UI компоненты (themed-text, animated-icon, etc.)
├── constants/      ← Тема (Colors, Spacing)
├── hooks/          ← Кастомные хуки
└── firebaseConfig.ts ← Firebase + анонимная аутентификация
```

### Известные особенности и паттерны

- **Fake Monorepo Strategy** в `build-ios.sh` — создаёт временную структуру для обхода проблем EAS с монорепо
- **Анонимная аутентификация** Firebase — устройство получает уникальный identity без логина
- Chat в `index.tsx` работает на **Mock-ответах** — реального подключения к AI_Core пока нет
- Дизайн: тёмная тема (`#000` / `#1A1A1A`), акцент цвет из `Colors.dark.accent`
- Компоненты: `ThemedText`, `ThemedView`, `AnimatedSplashOverlay`

### 🚨 Обнаруженные риски

1. `firebaseConfig.ts` содержит **открытый API ключ** в коде — нарушение безопасности (должно быть в .env)
2. Chat (`index.tsx`) — **заглушка** (Mock), реального AI-бэкенда нет
3. Отсутствует **глобальное управление состоянием** (нет Zustand/Redux/Context)
4. `explore.tsx` (6.5kb) — файл не зарегистрирован в Drawer, возможно устаревший
5. **Нет тестов** (unit/e2e)

---

## 📌 SECTION 4 — Стратегические цели системы (из VISION.md)

| Цель | Статус | Приоритет |
|---|---|---|
| Автономная работа 30 дней | 🔄 В работе | ВЫСШИЙ |
| Ноль техно-спама | ✅ Достигнуто | — |
| Бесконечный контент (10+ клипов/день) | 🔄 В работе | ВЫСОКИЙ |
| Финансовый суверенитет (1-2%/мес) | 🔄 В работе | ВЫСОКИЙ |
| UnifiedCoreMobile — командный центр | 🔴 В разработке | КРИТИЧЕСКИЙ |

---

## 📌 SECTION 5 — Clockwork Evolution Log

### Итерация #002 — 2026-06-11 (CRITICAL EXECUTION)

**Тип**: Полный запуск UnifiedCoreMobile  
**Выполнено**: Все 8 фаз

**Что сделано:**

- ✅ БЕЗОПАСНОСТЬ: Firebase apiKey вынесен из кода → app.json extra + expo-constants
- ✅ ГЛОБАЛЬНЫЙ СТЕЙТ: Zustand systemStore (chat, services, HA, scrubber, mode)
- ✅ LIVE CHAT: Firestore Command Relay Bus (заменяет Telegram)
- ✅ SMART HOME: Полный экран управления HA через Firestore relay
- ✅ SCRUBBER: Суверенный Скрабер с 6 типами задач + live log stream
- ✅ LIVE DASHBOARD: Метрики в реальном времени из Firestore
- ✅ BACKEND LISTENER: mobile_relay_listener.py для igor-gaming (PM2 ready)
- ✅ LAYOUT: Все экраны зарегистрированы (smart-home, scrubber)
- ✅ TS: 0 ошибок компиляции

**Ключевое архитектурное решение:**
> Telegram offline → Firestore как Command Bus.
> Mobile → Firestore(mobile_commands) → igor-gaming → Firestore(mobile_responses) → Mobile
> HA states → Firestore(ha_states) → реал-тайм на экране Smart Home

**Новые паттерны:**

- Пользователь в кризисном режиме принимает решения мгновенно ("ВЧЕРА")
- "igor-gaming" = основной backend. Всегда сначала искать там.
- Scrubber = Слой 2 Системы (Sovereign Scrubber)
- Smart Home = отдельный слой управления физическим окружением

**Memory Consolidation:**
> Добавлено: архитектура Firestore relay, PM2 процессы на igor-gaming,
> полная карта экранов приложения (8 экранов), Zustand store schema.

**ДЕПЛОЙ НА IGOR-GAMING — КРИТИЧНО:**

```
git pull
cd Projects/AI_Core
pm2 start mobile_relay_pm2.json
pm2 save
```
