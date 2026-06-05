# Telegram app-layer crypto & Alisa edge

## Telegram (MVP)

1. Bot API is **not** E2EE for bots — use `lib/telegram_crypto.py` before `sendMessage`.
2. Keys distributed via PKI onboarding (ECDH + NaCl Box).
3. iPhone decrypts in trusted app after optional YubiKey approval for sensitive actions.

## Standalone VPN app (later)

- Tailscale always-on on iPhone.
- WebSocket to `approval-gateway` / OpenClaw on LAN — no Apple APNs required.
- Critical alerts as local notification from WebSocket payload.

## Yandex Alisa (phase 6)

Goals:

- Remove vendor cloud dependency.
- Repurpose speaker as LAN microphone/speaker for local STT/TTS.

Steps (high risk):

1. Document hardware revision; check community jailbreak guides.
2. Flash custom Android/AOSP if UART/debug available — **may brick device**.
3. Point wake-word pipeline to local Whisper on RTX node via Tailscale.
4. Block outbound DNS except allowlist.

Do **not** block PKI/MCP rollout on Alisa completion.
