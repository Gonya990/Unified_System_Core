import os
import sys
from pathlib import Path

import yaml
from token_broker import TokenBroker

# Path setup for TokenBroker
ROOT_DIR = Path(__file__).resolve().parent
SRC_DIR = ROOT_DIR / "Projects/AI_Core/src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


def migrate_from_raw():
    raw_path = os.path.expanduser("~/.config/unified-system/tokens.yaml.raw")
    if not os.path.exists(raw_path):
        print(f"❌ Raw file not found at {raw_path}")
        return

    with open(raw_path) as f:
        tokens = yaml.safe_load(f)

    broker = TokenBroker()
    print("🚀 Encrypting and saving tokens to vault...")
    broker.save_vault(tokens=tokens, force_kdf="argon2id")
    print("✅ Vault updated successfully.")


if __name__ == "__main__":
    migrate_from_raw()
