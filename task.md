# Задача проекта: Windows AI Core (Telebot)

## 🚀 Реализованные функции (Сессия: 27.12.2025)

- [x] **Голосовое управление:** Поддержка через OpenAI Whisper API (`inference_client.py`).
- [x] **Зрение (Vision):** Анализ изображений через Gemini Vision (`handle_photo`).
- [x] **Карта инфраструктуры:** Мониторинг статуса серверов через команду `/infra`.
- [x] **Самовосстановление:** Сервис Watchdog (`ai-watchdog`) для авто-перезапуска.
- [x] **Авто-обновление:** Механизм обновления через `/update` (Git Pull + Pip + Restart).
- [x] **Менеджер задач:** Список дел на базе SQLite (`/todo`).
- [x] **Напоминания:** Планировщик уведомлений (`/remind`).
- [x] **Backup:** Бэкап БД в чат (`/backup`, Auto-Daily).
- [x] **Sudo Fix:** Перезапуск сервиса без ввода пароля.
- [x] **Документация:** Обновлен `ALICE_SETUP.md` с новыми командами.
- [x] **Web Dashboard:** FastAPI панель на порту 8096 (логи, инфра).
- [x] **SerpApi:** Интеграция Google Search (Knowledge Graph).
- [x] **HA Расширение:** Сенсоры, скрипты, сцены (`/ha sensors`, `/ha script`, `/ha scene`).
- [x] **Notification Manager:** Умные уведомления с тихими часами (`/notify`).
- [x] **Dashboard v2:** Графики токенов, кнопки управления (Backup, Restart).
- [x] **Cost Tracking Pro:** Детальная статистика по моделям и пользователям (`/costs`).

## 📋 Ближайшие шаги

- [ ] **Проверка:** Вручную проверить работу Watchdog на `igor-gaming-1` (требует настройки sudo).
- [ ] **Тестирование:** Протестировать все новые функции (Dashboard, SerpApi, HA sensors, /costs).

## 🔮 Будущее / Бэклог

- [ ] Интеграция сопряжения HomeKit Bridge.
- [ ] Настройка Linear API для продвинутого управления задачами.
- [ ] BIOS Update для Proxmox Host (Re-size BAR, IOMMU).
- [ ] Реализация Daily Digest (сводка дня в одном сообщении).
- [ ] Интеграция с Календарем (Google Calendar / Outlook).
