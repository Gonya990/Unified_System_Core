# RUNBOOK: GKE Bot + Cloud Factory + ByBit + Home Assistant

Дата: 2026-02-13

## Цель

Собрать в одну рабочую схему 4 контура:

1. Telegram Bot (работает в GKE)
2. Content Factory (работает на Cloud Server)
3. Crypto ByBit Bot (работает на Cloud Server, мониторинг из Telegram)
4. Home Assistant (управление из Telegram)

---

## 1) Архитектура (рабочая идея)

- **GKE (AI Bot):** принимает команды Telegram (`/factory`, `📈 Крипто`, HA-команды).
- **Cloud Server:** выполняет тяжелые задачи (рендер/пайплайн/PM2 процессы).
- **Связь GKE -> Cloud:** SSH-триггер из бота (настраивается через env).
- **HA:** bot -> `ha_controller` -> `ha_client` -> HA REST API.

Поток для фабрики:

`Telegram command -> GKE bot -> SSH trigger -> Cloud factory_scheduler -> output/logs`

Поток для крипто:

`ByBit bot (PM2, Cloud) -> logs -> GKE bot reads logs (path from env) -> Telegram status`

Поток для HA:

`Telegram -> HA controller -> HA API (HA_URL + HA_TOKEN)`

---

## 2) Обязательные переменные окружения (AI_Core/.env)

```env
FACTORY_REMOTE_HOST=unified-home-core-cloud
FACTORY_REMOTE_USER=gonya
FACTORY_REMOTE_ROOT=/home/gonya/Unified_System_Core
CRYPTO_BOT_LOG_PATH=/home/gonya/.pm2/logs/crypto-bot-error.log
HA_URL=http://<your-ha-host>:8123
HA_TOKEN=<long_lived_token>
```

---

## 3) Что уже исправлено в коде

Файл: `Projects/AI_Core/src/ai_telegram_bot_v2.py`

- `/factory` теперь:
  - сначала ищет локальный `factory_scheduler.py` (для dev/mount),
  - если не найден — автоматически делает SSH trigger на Cloud Server.
- `📈 Крипто` теперь:
  - читает логи из `CRYPTO_BOT_LOG_PATH` или стандартных PM2 путей,
  - не зависает на вечном `Loading...`,
  - показывает источник данных/диагностику.

---

## 4) Быстрый запуск по шагам

### Шаг A. Cloud Server готовность

- Убедиться, что `Content_Factory` существует по пути:
  `/home/gonya/Unified_System_Core/Projects/Content_Factory`
- Убедиться, что зависимости установлены (как минимум `schedule`).
- Убедиться, что crypto-bot работает под PM2 и пишет логи.

### Шаг B. GKE bot

- Подтянуть обновленный `ai_telegram_bot_v2.py`
- Перезапустить bot deployment
- Проверить команду `/factory` с темой и без темы

### Шаг C. Home Assistant

- Проверить доступность `HA_URL` из окружения, где работает бот
- Проверить валидность `HA_TOKEN`
- Прогнать health-check через команды бота / debug endpoint

---

## 5) Критерии “всё работает”

- `/factory` возвращает `Factory trigger sent to Cloud Server` или `Pipeline started (local execution)`
- `📈 Крипто` показывает не `Loading...`, а реальный баланс/рынок или честный диагностический статус
- HA команды отвечают не `Client not loaded`, а реальным статусом/действием

---

## 6) Частые проблемы

1. **"scripts not found"**
   - Причина: нет `Projects/Content_Factory` в контейнере GKE
   - Решение: использовать cloud trigger (уже внедрено)

2. **`ModuleNotFoundError: schedule` в фабрике**
   - Причина: не установлены зависимости на Cloud Server
   - Решение: установить requirements в окружении фабрики

3. **`Баланс: Loading...` у крипто**
   - Причина: бот смотрит не в тот лог
   - Решение: выставить `CRYPTO_BOT_LOG_PATH`

4. **HA недоступен**
   - Причина: токен/URL/сетевая доступность
   - Решение: проверить `HA_URL`, `HA_TOKEN`, маршрутизацию между средами
