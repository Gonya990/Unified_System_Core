#!/usr/bin/env python3
"""
Domain A: Intent Manager
Handles the 'Lease' mechanism for decentralized agents.
Architecture: Git-native stigmergy.
"""

from datetime import datetime, timedelta
from pathlib import Path

import yaml

LEDGER_PATH = Path(__file__).resolve().parent.parent.parent / "INTENT_LEDGER.yaml"


def load_ledger():
    if not LEDGER_PATH.exists():
        return {"intents": [], "constraints": []}
    with open(LEDGER_PATH) as f:
        return yaml.safe_load(f) or {"intents": [], "constraints": []}


def save_ledger(data):
    with open(LEDGER_PATH, "w") as f:
        yaml.dump(data, f, sort_keys=False, allow_unicode=True)


def claim_intent(intent_id, agent_id, human_owner, ttl_minutes=60):
    ledger = load_ledger()
    now = datetime.now()

    for intent in ledger["intents"]:
        if intent["id"] == intent_id:
            # Check if lease expired
            expires = datetime.fromisoformat(intent["lease_ttl"])
            if intent["status"] == "claimed" and expires > now and intent["owner"] != agent_id:
                return False, f"Intent {intent_id} is already claimed by {intent['owner']}"

            # Claim or Renew
            intent["status"] = "claimed"
            intent["owner"] = agent_id
            intent["human_owner"] = human_owner
            intent["lease_ttl"] = (now + timedelta(minutes=ttl_minutes)).isoformat()
            if intent["owner"] == agent_id:
                intent["renewal_count"] = intent.get("renewal_count", 0) + 1
            else:
                intent["renewal_count"] = 0

            save_ledger(ledger)
            return True, f"Intent {intent_id} claimed by {agent_id}"

    return False, f"Intent {intent_id} not found"


if __name__ == "__main__":
    # Internal test/example
    print("📋 Current Intent Ledger status...")
    current = load_ledger()
    for i in current["intents"]:
        print(f" - [{i['status'].upper()}] {i['id']} (Owner: {i.get('owner', 'None')})")
