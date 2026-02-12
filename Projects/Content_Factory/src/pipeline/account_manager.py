import json
import os
from pathlib import Path

from dotenv import load_dotenv

# Load environment
ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent
load_dotenv(ROOT_DIR / ".env")

ACCOUNTS_CONFIG = ROOT_DIR / "accounts_config.json"


class AccountManager:
    """Manages multiple social media accounts for content distribution."""

    def __init__(self):
        self.accounts = self._load_accounts()

    def _load_accounts(self):
        if ACCOUNTS_CONFIG.exists():
            with open(ACCOUNTS_CONFIG) as f:
                return json.load(f)
        return {
            "instagram": [
                {
                    "username": os.getenv("INSTAGRAM_USERNAME"),
                    "session_id": os.getenv("INSTAGRAM_SESSION_ID"),
                }
            ],
            "youtube": [{"name": "Main Channel", "token_file": "youtube_token.json"}],
            "threads": [
                {
                    "username": os.getenv("INSTAGRAM_USERNAME"),
                    "session_id": os.getenv("INSTAGRAM_SESSION_ID"),
                }
            ],
        }

    def get_accounts(self, platform):
        return self.accounts.get(platform, [])

    def save_accounts(self):
        with open(ACCOUNTS_CONFIG, "w") as f:
            json.dump(self.accounts, f, indent=4)

    def add_account(self, platform, data):
        if platform not in self.accounts:
            self.accounts[platform] = []
        self.accounts[platform].append(data)
        self.save_accounts()


if __name__ == "__main__":
    manager = AccountManager()
    print(f"Loaded accounts: {json.dumps(manager.accounts, indent=2)}")
    if not ACCOUNTS_CONFIG.exists():
        manager.save_accounts()
        print(f"Created default config at {ACCOUNTS_CONFIG}")
