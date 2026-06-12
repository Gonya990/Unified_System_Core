# Yandex Alice Dialogs Integration

## Overview
This document outlines how Yandex Alice integrates with the Unified System Core. 
Alice sends requests to a designated public endpoint, which routes commands into the `mobile_commands` Firestore collection (or directly to Home Assistant).

## Architecture
1. **Yandex Alice Request**: A user says a command (e.g., "Алиса, включи свет").
2. **Webhook Endpoint**: `https://<YOUR_PUBLIC_DOMAIN>/alice-webhook` receives the request.
3. **Processing**:
   - The webhook parses the Alice JSON payload.
   - It determines the intent and entity.
   - It writes a document to Firestore `mobile_commands` with type `ha_control`.
4. **Relay Listener**: `mobile_relay_listener.py` running on `igor-gaming` picks up the command from Firestore and executes it via the local Home Assistant API.

## Webhook Payload Example (Mock)
```json
{
  "meta": {
    "locale": "ru-RU",
    "timezone": "Europe/Moscow",
    "client_id": "ru.yandex.searchplugin/7.16 (none none; android 4.4.2)"
  },
  "request": {
    "command": "включи свет",
    "original_utterance": "включи свет",
    "type": "SimpleUtterance"
  },
  "session": {
    "message_id": 1,
    "session_id": "...",
    "skill_id": "..."
  },
  "version": "1.0"
}
```

## Security
- Alice requests should be verified using Yandex signature validation.
- Only known `skill_id`s should be processed.
