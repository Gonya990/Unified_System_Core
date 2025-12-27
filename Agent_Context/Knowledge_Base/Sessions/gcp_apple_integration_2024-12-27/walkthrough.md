# Walkthrough: GCP Budget Alerts & Apple Device Integration

> **Date:** 2024-12-27
> **Session:** gcp_apple_integration_2024-12-27

## Summary

Implemented comprehensive GCP budget monitoring with Telegram alerts and Apple device integration for smart home control via Shortcuts and HomeKit.

## Changes Made

### 1. GCP Monitoring & Alerts

- **Cloud Function `budget-alert-telegram`** deployed to `me-west1`
  - Receives Pub/Sub messages from budget alerts
  - Sends formatted notifications to Telegram (chat IDs: 708531393, 1881720235)
  - Russian localization with urgency indicators (50%, 90%, 100%, 150%)
  
- **Budgets Connected:**
  - ₪150/month (billing account 011CFE-33CC55-CEFB8F) for Gemini
  - ₪400/month (billing account 012C93-524151-CC901F) for my-home

### 2. Vasya Gateway Enhancement

- Added `/shortcut/ask` endpoint for Apple Shortcuts
- Simple JSON response `{"answer": "...", "provider": "..."}` for Siri to speak
- Works with both Ollama and Gemini via round-robin load balancing
- URL: `http://unified-home-core-cloud.tail5e8a72.ts.net:8080/shortcut/ask`

### 3. HomeKit Bridge

- Added HomeKit Bridge integration to real Home Assistant (192.168.1.216)
- **Name:** HASS Bridge G9:21068
- **PIN:** 951-74-847
- **Port:** 21068
- Removed stale HA container from igor-gaming-1

### 4. Apple Shortcut Template

- Created `shortcuts/ask_vasya.shortcut` with Tailscale MagicDNS URL
- Works over mobile network when connected to Tailscale VPN

## Verification

- [x] Budget alert test message delivered to Telegram
- [x] Vasya API responds: `{"answer":"Двенадцать.","provider":"gemini"}`
- [x] Ollama models available: qwen2:0.5b, llama3.2, ministral
- [x] HomeKit Bridge registered in HA

## Key URLs (Tailscale)

| Service | URL |
|---------|-----|
| Home Assistant | <http://smart.tail5e8a72.ts.net:8123> |
| Vasya API | <http://unified-home-core-cloud.tail5e8a72.ts.net:8080> |
| Vasya Health | <http://unified-home-core-cloud.tail5e8a72.ts.net:8080/health> |

## Next Steps

- [ ] Pair HomeKit Bridge with Apple Home app (PIN: 951-74-847)
- [ ] Create working Shortcut on Mac/iPhone
- [ ] Test voice command: "Hey Siri, Спросить Васю"
