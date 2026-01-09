# 🧠 Consilium Knowledge Pack: Family Swarm Architecture

## Overview

The "Family Swarm" is a distributed resource pooling strategy designed to maximize AI throughput by aggregating individual family member quotes (Google Gemini Free Tier).

## Implementation Details

### 1. Identity & Registration

- **Bot**: `GonyaHomeBot`
- **Link**: `https://t.me/GonyaHomeBot`
- **Flow**: New users hit `/start` -> Admin gets approval buttons -> Approved users are added to `config/users.yaml`.

### 2. Resource Pooling (The Swarm)

- **File**: `config/resources.yaml`
- **Structure**:

```yaml
gemini_pool:
  - id: "Member1"
    api_key: "AIza..."
  - id: "Member2"
    api_key: "AIza..."
```

- **Logic**: `swarm_manager.py` implements Round-Robin rotation. If a key hits 429 (Rate Limit), it transitions to the next available key.

### 3. Integration

- `InferenceClient` (the brain) now Queries `SwarmManager` before any Gemini call.
- This effectively multiplies the RPM (Requests Per Minute) by the number of family accounts (5 accounts = 75 RPM).

## Recommendations for Agents (FuchsiaCat/Kostik)

1. Adopt the `resources.yaml` format for consistent cross-agent resource sharing.
2. Implement similar "Swarm" decorators for critical API calls to ensure extreme reliability.
3. Use `users.yaml` as the source of truth for family member roles.
