# Задача проекта: Unified System (Recovery & Evolution)

## 🚀 Реализованные функции (Сессия: 10.01.2026)

### 🔴 System Recovery (Critical)

- [x] **MCP Mail:** Агент `mcp-agent-mail` восстановлен после сбоя.
  "Zombie" процессы убиты.
- [x] **Communication:** Связь с `FuchsiaCat` (Kostya) и `VioletCastle`
  восстановлена.
- [x] **Bot Auth:** Реализовано персистентное хранение Google Tokens (`secrets/`).
  Бот больше не теряет доступ к календарю при рестарте.

### 🏭 Content Factory (Evolution)

- [x] **Pipeline Integration:** Скрипт `daily_researcher.py` интегрирован
  с `orchestrator_v3_no_face`.
- [x] **Autonomous Loop:** Теперь один запуск создает Рисерч -> Картинки -> Видео.
- [x] **Pause Logic:** Процесс остановлен до внедрения пула токенов
  (экономия ресурсов).

### 🏛️ Meta-Orchestration (New!)

- [x] **Proposal:** Разработан документ `architecture/META_ORCHESTRATION.md`.
- [x] **Notification:** Предложение отправлено Совету (Kostya/VioletCastle)
  на утверждение.
- [x] **Clarification:** Дан ответ на вопросы VioletCastle о планах.
- [x] **Phase 1 Complete:** `TokenBroker` реализован и интегрирован.

## 📋 Ближайшие шаги (Next Actions)

### 🤖 Фаза 5: Продвинутая Автоматизация (Advanced Automation)
>
> *Статус: В РАБОТЕ (ПО ЗАПРОСУ)*

- [x] **Семейный Ассистент (Family Assistant):**
  - [x] **Morning Brief:** Скрипт для утренних брифингов (Календарь + Погода + Задачи) для Артура (07:00).
  - [x] **Homework Sentinel:** Сканирование почты Артура на предмет "Homework" / "School" и саммари дедлайнов.
- [ ] **Интеграция Фабрики Контента 2.0:**
  - [x] **Orchestrator Link:** Добавить команду `/factory` в бота для ручного запуска генерации видео.
  - [ ] **Status Monitoring:** Уведомления в Telegram о статусе рендера (`daily_researcher` -> Bot).
- [ ] **MCP Mail Intelligence:**
  - [ ] **Council Feedback:** Авто-обработка ответов от Кости (FuchsiaCat/VioletCastle).
  - [ ] **Alert System:** Уведомлять Админа только о важных письмах ("High Priority").

### 🏗️ Интеграция Инфраструктуры (Meta-Orchestration)

- [x] **TokenBroker Integration:** Обновить `daily_researcher.py` для использования семейных ключей через Брокера.
- [ ] **Account Vizier:** Создать систему управления аккаунтами (Google/Insta) для агентов.

## 🔮 Бэклог (Backlog)

- [ ] **Dashboard:** Починить UI для `/stats` (API готово, нужен фронт).
- [ ] **Git Worktree:** Безопасные тесты веток.
- [ ] **SmartThings:** Добить очистку API.
