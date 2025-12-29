# 📋 MASTER TASKS - Consolidated

**Updated:** 2025-12-29 12:52 IST

---

## ✅ Сегодня выполнено / Completed Today

- [x] Telegram Bot deployed on igor-gaming-1 (running 2h+)
- [x] Tailscale SSH configured on all 4 hosts
- [x] sudo NOPASSWD configured on all hosts
- [x] gonya user created on PVE with Administrator role
- [x] kosta user created on PVE with Administrator role
- [x] lenovo-tb-j606f restored to online
- [x] Unified_System synced to all hosts
- [x] Bluetooth DBus fix for HA ✅ (verified on smart)

---

## 🔴 Высокий приоритет / High Priority

- [x] **Bluetooth Fix для HA** - ✅ DBus mounted in Docker (`/run/dbus:/run/dbus:ro`)
- [x] **SmartThings** - Guide exists (SMARTTHINGS_FIX_GUIDE.md), needs manual PAT
- [ ] **Алиса → Home Assistant** - Решение найдено! (см. ниже)
- [~] **BIOS Update для Proxmox** - Назначено Косте (Rocinante)

### 🎯 Алиса → HA: Решение

**Компоненты:**

1. **Yandex Smart Home** - HACS component для экспорта устройств
2. **Yaha Cloud** - Облачный навык для быстрого подключения
3. **YandexStation** - Управление колонками из HA

**Шаги:**

```bash
# 1. Установить через HACS:
# Настройки → HACS → Интеграции → "Yandex Smart Home"

# 2. Добавить интеграцию в HA:
# Настройки → Устройства и службы → + → "Yandex Smart Home"

# 3. В приложении "Дом с Алисой":
# Устройства → + → По производителю → "Yaha Cloud"

# 4. Авторизоваться с кодом из HA
```

**URL:** <https://yaha-cloud.ru>

---

## ✅ Средний приоритет - Проверено / Verified

- [x] **Ollama** - ✅ 5 моделей (qwen3:4b, llama3:8b, qwen2:0.5b, llama3.2, ministral)
- [x] **Vasya Gateway** - ✅ Running (round_robin: ollama+gemini)
- [x] **Test AI providers** - ✅ Ollama работает
- [x] **SerpApi** - ✅ Интегрирован в бота
- [x] **Image Generation** - `/imagine` через Gemini Vision

---

## 🟢 Низкий приоритет / Low Priority

- [ ] Shopping integrations (Amazon, eBay, AliExpress) - Будущее
- [ ] Bank integrations IL (הפועלים, לאומי) - Будущее
- [ ] Gov Services IL (gov.il) - Будущее
- [ ] ChromeOS Flex setup - Для Артура
- [x] GCP Алерты - Отменены по запросу

---

## ✅ Ранее выполнено / Previously Completed

### Telegram Bot Features

- [x] Голосовое управление (Whisper API)
- [x] Vision (Gemini анализ изображений)
- [x] Инфраструктура мониторинг `/infra`
- [x] Watchdog самовосстановление
- [x] Auto-update (Git Pull + Restart)
- [x] Todo/Remind (SQLite)
- [x] Dashboard (FastAPI + графики)
- [x] HA Integration (sensors, scripts, scenes)
- [x] HomeKit Bridge
- [x] Linear API integration
- [x] Daily Digest 09:00
- [x] Google Calendar
- [x] Cost Tracking
- [x] Notification Manager

### Infrastructure

- [x] Distributed AI (pve-antigravity-1 Ollama Worker)
- [x] Vasya Gateway (unified-home-core)
- [x] Central Hub MCP Agent Mail
- [x] GCP Metrics Collector
- [x] Node-RED automation

### Home Assistant (smart)

- [x] Home Assistant - Up 11h
- [x] n8n - Up 2 weeks
- [x] NodeRED - Up 2 weeks  
- [x] Zigbee2MQTT - Up 2 weeks
- [x] Bluetooth DBus - Mounted

---

## 📊 Статистика

| Категория | Готово | В работе |
|-----------|--------|----------|
| **Bot Features** | 20+ | 0 |
| **Infrastructure** | 10+ | 0 |
| **Integrations** | 10 | 1 (Alice) |
| **Системы** | 4/4 hosts | ✅ |

---

## 🔗 Быстрый доступ

```bash
# Tailscale SSH:
tailscale ssh gonya@igor-gaming-1
tailscale ssh gonya@unified-home-core-cloud
tailscale ssh igor@smart
tailscale ssh gonya@pve-antigravity-1

# Proxmox: https://192.168.190.113:8006 (gonya@pam)
# Home Assistant: http://100.81.133.25:8123
# Vasya Gateway: http://100.110.209.49:8080
```
