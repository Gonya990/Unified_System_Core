#!/usr/bin/env python3
import json
import sys
from pathlib import Path
from typing import Any, Optional

# Constants
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
ACCOUNTS_FILE = ROOT_DIR / "accounts_config.json"
KEYS_FILE = ROOT_DIR / "secrets/keys.json"


class AccountVizier:
    """Master controller for all system credentials and accounts."""

    def __init__(self):
        self.accounts = self._load_json(ACCOUNTS_FILE)
        self.keys = self._load_json(KEYS_FILE)

    def _load_json(self, path: Path) -> dict:
        if path.exists():
            try:
                with open(path) as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading {path}: {e}")
                return {}
        return {}

    def _save_json(self, path: Path, data: dict):
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, "w") as f:
                json.dump(data, f, indent=4)
            print(f"✅ Saved updates to {path.name}")
        except Exception as e:
            print(f"❌ Error saving {path}: {e}")

    def list_all(self):
        print("\n--- 📱 SOCIAL ACCOUNTS ---")
        for platform, accs in self.accounts.items():
            if platform == "gemini_keys":
                continue  # Handled in keys
            print(f"\n[{platform.upper()}]")
            for i, acc in enumerate(accs):
                username = acc.get("username") or acc.get("name", "Unknown")
                status = "✅ Active" if acc.get("session_id") or acc.get("token_file") else "⚠️ Incomplete"
                print(f"  {i + 1}. {username} ({status})")

        print("\n--- 🔑 API KEYS ---")
        for service, pool in self.keys.items():
            if not pool:
                continue
            print(f"\n[{service.upper()}]")
            for i, key_data in enumerate(pool):
                alias = key_data.get("alias", "No Alias")
                tier = key_data.get("tier", "unknown")
                print(f"  {i + 1}. {alias} ({tier})")

    def get_social_account(self, platform: str, index: int = 0) -> Optional[dict]:
        accs = self.accounts.get(platform, [])
        if 0 <= index < len(accs):
            return accs[index]
        return None

    def get_api_key(self, service: str, alias: str = None) -> Optional[str]:
        pool = self.keys.get(service, [])
        if not pool:
            return None
        if alias:
            for k in pool:
                if k.get("alias") == alias:
                    return k.get("key")
        return pool[0].get("key")

    def update_social_session(self, platform: str, username: str, session_id: str):
        if platform not in self.accounts:
            self.accounts[platform] = []

        found = False
        for acc in self.accounts[platform]:
            if acc.get("username") == username:
                acc["session_id"] = session_id
                found = True
                break

        if not found:
            self.accounts[platform].append({"username": username, "session_id": session_id})

        self._save_json(ACCOUNTS_FILE, self.accounts)

    def add_api_key(self, service: str, key: str, alias: str, owner: str = "Admin", tier: str = "tier1"):
        if service not in self.keys:
            self.keys[service] = []

        self.keys[service].append({"alias": alias, "key": key, "tier": tier, "owner": owner})
        self._save_json(KEYS_FILE, self.keys)


def main():
    vizier = AccountVizier()

    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        if cmd == "list":
            vizier.list_all()
        elif cmd == "get-key":
            if len(sys.argv) > 2:
                print(vizier.get_api_key(sys.argv[2]))
        elif cmd == "update-insta":
            if len(sys.argv) > 3:
                vizier.update_social_session("instagram", sys.argv[2], sys.argv[3])
                vizier.update_social_session("threads", sys.argv[2], sys.argv[3])
        else:
            print("Unknown command. Try: list, get-key [service], update-insta [user] [session]")
    else:
        # Mini Interactive Menu
        print("\n🧙 ACCOUNT VIZIER - Command Center")
        print("1. List All Accounts & Keys")
        print("2. Update Instagram Session")
        print("3. Add API Key")
        print("0. Exit")

        choice = input("\nSelect [1-3]: ")
        if choice == "1":
            vizier.list_all()
        elif choice == "2":
            user = input("Instagram Username: ")
            sid = input("New Session ID: ")
            vizier.update_social_session("instagram", user, sid)
            vizier.update_social_session("threads", user, sid)
        elif choice == "3":
            svc = input("Service (openai/gemini/claude/pexels): ")
            key = input("Key: ")
            alias = input("Alias (e.g. MyKey): ")
            vizier.add_api_key(svc, key, alias)
        elif choice == "0":
            sys.exit(0)


if __name__ == "__main__":
    main()
