# 📋 MASTER TASKS - Consolidated

**Updated:** 2025-12-29 12:43 IST

---

## ✅ Сегодня выполнено / Completed Today

- [x] Telegram Bot deployed on igor-gaming-1 (running 2h+)
- [x] Tailscale SSH configured on all 4 hosts
- [x] sudo NOPASSWD configured on all hosts
- [x] gonya user created on PVE with Administrator role
- [x] lenovo-tb-j606f restored to online
- [x] Unified_System synced to all hosts

---

## 🔴 Высокий приоритет / High Priority

- [ ] **Bluetooth Fix для HA** - Проброс DBus в Docker (см. BLUETOOTH_FIX_GUIDE.md)
- [ ] **BIOS Update для Proxmox** - Re-size BAR, IOMMU, SVM Mode
- [ ] **SmartThings CLI cleanup** - Требует PAT токен
- [ ] **Алиса → Home Assistant** - OAuth настройка

---

## 🟡 Средний приоритет / Medium Priority

- [ ] **Image Generation** - `/imagine` command (DALL-E/Stable Diffusion)
- [ ] **iPhone HA App** - Background refresh setup
- [ ] **GCP Алерты** - Telegram + email уведомления
- [ ] **SerpApi** - Google Search для бота (RAG)
- [ ] **Test all AI providers** - Ollama, OpenAI, Gemini verification

---

## 🟢 Низкий приоритет / Low Priority

- [ ] Shopping integrations (Amazon, eBay, AliExpress)
- [ ] Bank integrations IL (הפועלים, לאומי, דיסקונט)
- [ ] Gov Services IL (gov.il, ביטוח לאומי)
- [ ] ChromeOS Flex setup on old device
- [ ] Directory reorganization (Shared/Private)
- [ ] Kubernetes deployment for bot

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

---

## 📊 Статистика

| Категория | Готово | В работе |
|-----------|--------|----------|
| **Bot Features** | 20+ | 3 |
| **Infrastructure** | 10+ | 2 |
| **Integrations** | 8 | 5 |
| **Системы** | 4/4 hosts | ✅ |

---

## 🔗 Быстрый доступ / Quick Access

```bash
# SSH ко всем хостам:
tailscale ssh gonya@igor-gaming-1
tailscale ssh gonya@unified-home-core-cloud
tailscale ssh igor@smart
tailscale ssh gonya@pve-antigravity-1

# Проверка бота:
tailscale ssh gonya@igor-gaming-1 'systemctl --user status telegram_ai_bot'

# Proxmox:
https://192.168.190.113:8006 (gonya@pam)

# Home Assistant:
http://100.81.133.25:8123
```
