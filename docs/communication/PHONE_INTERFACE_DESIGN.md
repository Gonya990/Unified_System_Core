# Phone Interface Design Document

**Task**: US-w7y  
**Date**: 2026-01-12  
**Status**: ✅ Design Complete

---

## Overview

The **Phone Interface** is a real-time, low-latency communication channel
between agents and human operators. It complements the existing MCP Mail
(high-latency, async) with voice calls and interactive push notifications.

---

## Use Cases

| Scenario | Current Solution | Phone Solution |
|:---------|:-----------------|:---------------|
| Critical alert | Telegram message | Voice call + TTS |
| Approval required | Mail + wait | Push notification with buttons |
| Urgent escalation | Mail (may be missed) | Phone call (impossible to miss) |
| Real-time guidance | Not possible | Voice conversation |

---

## Proposed Stack

### Voice Layer: VAPI.ai

**Why VAPI**:

- Python SDK available (`pip install vapi_python`)
- Abstracts STT + LLM + TTS pipeline
- Supports custom assistants
- Handles interruptions, recording

**Integration**:

```python
from vapi_python import Vapi

vapi = Vapi(api_key="...")

# Trigger outbound call
vapi.start(
    assistant_id="unified-system-agent",
    phone_number="+972XXXXXXXXX",
    first_message="This is PinkLake. Urgent escalation required."
)
```

### Interactive Push: Firebase Cloud Messaging (FCM)

**Why FCM**:

- Free tier sufficient
- Android/iOS/Web support
- Action buttons in notifications
- Already have Google Cloud project

**Integration**:

```python
import firebase_admin
from firebase_admin import messaging

message = messaging.Message(
    notification=messaging.Notification(
        title="🚨 Agent Escalation",
        body="PinkLake needs approval for file deletion"
    ),
    android=messaging.AndroidConfig(
        notification=messaging.AndroidNotification(
            click_action="APPROVE_ACTION"
        )
    ),
    token=user_fcm_token
)
```

---

## Phone Tool Interface

Add to `docs/communication/CAPABILITIES_MATRIX.md`:

```yaml
phone:
  call:
    - recipient: phone_number or user_id
    - message: string (TTS)
    - priority: normal | urgent | critical
    - wait_for_response: bool
  push:
    - recipient: user_id
    - title: string
    - body: string
    - actions: list of {label, callback}
```

### Escalation Protocol Integration

Update escalation rules:

| Priority | Channel Sequence |
|:---------|:-----------------|
| Low | Mail only |
| Normal | Mail → Push (after 5 min) |
| High | Mail + Push simultaneously |
| Critical | Mail + Push + Voice Call |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Unified Phone Interface                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │  VoiceCall   │    │    Push      │    │   Callback   │  │
│  │   (VAPI)     │    │   (FCM)      │    │   Handler    │  │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘  │
│         │                   │                   │          │
│         └─────────────┬─────┴───────────────────┘          │
│                       ▼                                     │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              PhoneInterface (Python SDK)              │  │
│  │                                                       │  │
│  │  phone.call(to="+972...", message="...", urgent=True) │  │
│  │  phone.push(to="igor", title="...", actions=[...])    │  │
│  └──────────────────────────────────────────────────────┘  │
│                       ▲                                     │
│                       │                                     │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  mail_processor.py / escalation_handler.py            │  │
│  │  (Triggers phone based on priority/timeout)           │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Implementation Plan

### Phase 1: POC (This Week)

1. Create VAPI account and assistant
2. Implement `phone_interface.py` with `call()` method
3. Test outbound call to admin phone

### Phase 2: Push Notifications

1. Configure FCM in Google Cloud
2. Implement `push()` method
3. Create mobile/web receiver for actions

### Phase 3: Integration

1. Update `mail_processor.py` to use PhoneInterface
2. Add timeout-based escalation (Mail → Push → Call)
3. Document in CAPABILITIES_MATRIX.md

---

## Required Credentials

| Service | Credential | Storage |
|:--------|:-----------|:--------|
| VAPI | API Key | `.env` as `VAPI_API_KEY` |
| FCM | Service Account JSON | `secrets/firebase-admin.json` |

---

## Agno Integration (Future)

Once Agno is adopted (per US-du5), PhoneInterface becomes an Agno tool:

```python
from agno import Agent, tool

@tool
def phone_call(recipient: str, message: str, urgent: bool = False):
    """Make a voice call to a human operator."""
    phone.call(to=recipient, message=message, priority="urgent" if urgent else "normal")

agent = Agent(tools=[phone_call])
```

---

## References

- VAPI Docs: <https://docs.vapi.ai>
- VAPI Python SDK: <https://pypi.org/project/vapi-python/>
- FCM Docs: <https://firebase.google.com/docs/cloud-messaging>
