# Task: GCP Monitoring & Apple Integration

## Phase 1: GCP Budget Alerts <!-- id: 100 -->

- [x] Enable Cloud Monitoring API <!-- id: 101 -->
- [x] Create gcp-monitoring-collector service account <!-- id: 102 -->
- [x] Deploy gcp_metrics_collector.py to igor-gaming-1 <!-- id: 103 -->
- [x] Create Pub/Sub topic 'budget-alerts' <!-- id: 104 -->
- [x] Deploy Cloud Function budget-alert-telegram to me-west1 <!-- id: 105 -->
- [x] Connect budgets (₪150, ₪400) to Pub/Sub notifications <!-- id: 106 -->
- [x] Test Telegram notification delivery <!-- id: 107 -->

## Phase 2: Apple Integration <!-- id: 200 -->

- [x] Research Apple Developer APIs (HomeKit, SiriKit, iCloud, Find My) <!-- id: 201 -->
- [x] Add /shortcut/ask endpoint to Vasya Gateway <!-- id: 202 -->
- [x] Rebuild Vasya Gateway container on unified-home-core <!-- id: 203 -->
- [x] Test Vasya API via Tailscale MagicDNS <!-- id: 204 -->
- [x] Add HomeKit Bridge to real Home Assistant (192.168.1.216) <!-- id: 205 -->
- [x] Get HomeKit PIN: 951-74-847 for HASS Bridge G9:21068 <!-- id: 206 -->
- [x] Remove old HA container from igor-gaming-1 <!-- id: 207 -->
- [x] Update shortcut URL to use Tailscale MagicDNS <!-- id: 208 -->

## Phase 3: Verification <!-- id: 300 -->

- [x] Verify Ollama working (qwen2, llama3.2, ministral models) <!-- id: 301 -->
- [x] Verify Vasya Gateway health <!-- id: 302 -->
- [x] All commits pushed to GitHub <!-- id: 303 -->
- [ ] Create working Shortcut on Mac/iPhone <!-- id: 304 --> <!-- CURRENT FOCUS -->
- [ ] Pair HomeKit Bridge with Apple Home app <!-- id: 305 -->

## Commits Today

- c58f821: feat(alerts): add Telegram budget alerts via Cloud Function
- a6dec1b: feat(apple): add Vasya shortcut and HomeKit Bridge integration  
- 7e27747: fix(shortcuts): use Tailscale MagicDNS for mobile network access
