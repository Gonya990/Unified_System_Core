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
- [x] **Linear API:** Интеграция с Linear.app для профессионального таск-менеджмента (`/linear`).
- [x] **Daily Digest:** Ежедневная сводка (статистика, задачи, мотивация) каждое утро в 09:00.
- [x] **Google Calendar:** Интеграция календаря (события в digest, `/calendar`).
- [x] **HomeKit Bridge:** Мост для Apple Home (автоматическое добавление устройств из HA).

## 📋 Ближайшие шаги

- [x] **HA Диагностика:** Полный аудит Home Assistant (329 сущностей, 32 интеграции).
- [x] **HA Исправления:** Автоматические исправления (HACS cleanup, vacuum activation).
- [x] **HA Скрипты:** Созданы инструменты диагностики (`quick_diag.py`, `fix_integrations.py`).
- [x] **Yandex.Station:** Отсканировать QR-код для завершения авторизации.
- [x] **SmartThings Guide:** Полное руководство по исправлению + автоматический скрипт.
- [x] **iPhone HA Guide:** Инструкция по включению фонового обновления.
- [x] **Bluetooth Guide:** Инструкция по пробросу DBus в Docker.
- [ ] **SmartThings CLI:** Запустить cleanup_smartthings_api.py (требует PAT).
- [ ] **Bluetooth Fix:** Следовать инструкции из BLUETOOTH_FIX_GUIDE.md на хосте.
- [ ] **iPhone HA App:** Следовать инструкции из IPHONE_HA_SETUP.md.
- [x] **Проверка:** Протестировать все новые функции (HomeKit, Calendar, Linear, Digest).
- [x] **Документация:** Обновить ALICE_SETUP.md с новыми командами.

## 🔮 Будущее / Бэклог

- [ ] BIOS Update для Proxmox Host (Re-size BAR, IOMMU).
- [x] Голосовые ответы (Text-to-Speech через `/speak`).
- [x] Интеграция с Notion для заметок (`/note` - требует `NOTION_API_KEY`).
- [x] Мониторинг здоровья (`/health add/goal` - база для Apple Shortcuts).
- [x] Настройка мониторинга доступности устройств HA (DeviceMonitor service).
- [x] Автоматизации самовосстановления для HA интеграций (Reload on failure).
