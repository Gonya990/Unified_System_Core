# Home Assistant API Access

## 🔑 Authentication

**Token Name:** Antigravity Agent API  
**Created:** 2025-12-27  
**Expires:** 2082 (10 years)

Token stored in: `Scripts/homeassistant/ha_client.py`

## 🌐 Endpoints

**Base URL:** `http://192.168.1.216:8123`  
**Tailscale URL:** `http://smart.tail5e8a72.ts.net:8123`

## 📊 Available Entities

Total entities discovered: **100+**

Includes:

- Lights (Tuya, Xiaomi)
- Scripts (good_morning, good_night, etc.)
- Sensors (backup, energy monitoring)
- Input booleans (TV controls)
- HomeKit Bridge integration

## 🛠️ Usage

```bash
# Check HA health
python3 Scripts/homeassistant/ha_client.py health

# Get HomeKit status
python3 Scripts/homeassistant/ha_client.py homekit

# List all entities
python3 Scripts/homeassistant/ha_client.py states

# Restart HomeKit Bridge
python3 Scripts/homeassistant/ha_client.py restart_homekit
```

## 🔐 Security

- Token has read/write access to ALL integrations
- Never commit token to public repos
- Token stored in `.py` file (in `.gitignore`)

## ✅ Verified Components

- ✅ `homekit` - HomeKit Bridge active
- ✅ `ollama` - AI integration
- ✅ `tuya` - Smart devices
- ✅ `xiaomi_miot` - Xiaomi devices
- ✅ `yandex_station` - Yandex Smart Speaker
- ✅ `api` - REST API enabled
