import sys
import os
import json
from pathlib import Path

# Add Utilities to path
sys.path.append(os.path.join(os.getcwd(), "Scripts", "Utilities"))
from token_broker import TokenBroker

def refresh():
    # Load keys.json
    keys_path = os.path.join(os.getcwd(), "secrets", "keys.json")
    if not os.path.exists(keys_path):
        print(f"❌ {keys_path} not found.")
        return

    with open(keys_path, 'r') as f:
        keys = json.load(f)

    # Initialize TokenBroker (uses AGENT_MAIL_TOKEN from env)
    # Ensure AGENT_MAIL_TOKEN matches the one used by others
    os.environ.setdefault("AGENT_MAIL_TOKEN", "c2bb2cf043ec2ae56a0dec69024e6129eb5cde36a22bddb93afcfa2e71e72afb")
    
    broker = TokenBroker()
    print(f"🔄 Migrating {sum(len(v) for v in keys.values())} keys to encrypted vault...")
    broker.save_vault(keys)
    print("✅ Vault refreshed and encrypted.")

if __name__ == "__main__":
    refresh()
