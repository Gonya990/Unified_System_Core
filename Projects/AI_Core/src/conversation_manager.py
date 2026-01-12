"""
Conversation Manager for Telegram Bot
Stores and retrieves conversation history per user.
"""

import json
import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


class ConversationManager:
    """Manage conversation history for users."""

    def __init__(self, storage_path: str = "conversations"):
        """Initialize with storage directory."""
        self.storage = Path(storage_path)
        self.storage.mkdir(exist_ok=True)
        logger.info(f"Conversation storage initialized at {self.storage.absolute()}")

    def _get_file_path(self, user_id: int) -> Path:
        """Get file path for user's conversation history."""
        return self.storage / f"{user_id}.json"

    def get_history(self, user_id: int, limit: int = 10) -> list[dict]:
        """
        Get conversation history for a user.

        Args:
            user_id: Telegram user ID
            limit: Maximum number of recent messages to return

        Returns:
            List of message dictionaries with role, content, timestamp
        """
        file_path = self._get_file_path(user_id)

        if not file_path.exists():
            return []

        try:
            with open(file_path, encoding='utf-8') as f:
                data = json.load(f)

            # Return last N messages
            return data[-limit:]
        except Exception as e:
            logger.error(f"Failed to load history for user {user_id}: {e}")
            return []

    def add_message(self, user_id: int, role: str, content: str) -> None:
        """
        Add a message to user's conversation history.

        Args:
            user_id: Telegram user ID
            role: Message role ('user' or 'assistant')
            content: Message content
        """
        history = self.get_full_history(user_id)

        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }

        history.append(message)

        # Keep last 100 messages max to prevent file growth
        if len(history) > 100:
            history = history[-100:]

        file_path = self._get_file_path(user_id)

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(history, f, indent=2, ensure_ascii=False)
            logger.debug(f"Added {role} message for user {user_id}")
        except Exception as e:
            logger.error(f"Failed to save history for user {user_id}: {e}")

    def get_full_history(self, user_id: int) -> list[dict]:
        """Get all conversation history for a user."""
        file_path = self._get_file_path(user_id)

        if not file_path.exists():
            return []

        try:
            with open(file_path, encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load full history for user {user_id}: {e}")
            return []

    def clear_history(self, user_id: int) -> bool:
        """
        Clear conversation history for a user.

        Returns:
            True if history was cleared, False if no history existed
        """
        file_path = self._get_file_path(user_id)

        if not file_path.exists():
            return False

        try:
            file_path.unlink()
            logger.info(f"Cleared history for user {user_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to clear history for user {user_id}: {e}")
            return False

    def get_context_messages(self, user_id: int, limit: int = 5) -> list[dict]:
        """
        Get recent messages formatted for AI context.

        Returns messages in format: [{"role": "user|assistant", "content": "..."}]
        """
        history = self.get_history(user_id, limit=limit)

        # Strip timestamps, keep only role and content
        return [
            {"role": msg["role"], "content": msg["content"]}
            for msg in history
        ]

    def get_stats(self) -> dict:
        """Get statistics about conversation storage."""
        files = list(self.storage.glob("*.json"))
        total_users = len(files)
        total_messages = 0

        for file in files:
            try:
                with open(file) as f:
                    data = json.load(f)
                    total_messages += len(data)
            except Exception:
                pass

        return {
            "total_users": total_users,
            "total_messages": total_messages,
            "avg_messages_per_user": total_messages / total_users if total_users > 0 else 0
        }


# CLI testing
if __name__ == "__main__":
    import sys

    manager = ConversationManager()

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python conversation_manager.py stats")
        print("  python conversation_manager.py get <user_id>")
        print("  python conversation_manager.py clear <user_id>")
        sys.exit(1)

    command = sys.argv[1]

    if command == "stats":
        stats = manager.get_stats()
        print(json.dumps(stats, indent=2))

    elif command == "get" and len(sys.argv) > 2:
        user_id = int(sys.argv[2])
        history = manager.get_history(user_id)
        print(json.dumps(history, indent=2, ensure_ascii=False))

    elif command == "clear" and len(sys.argv) > 2:
        user_id = int(sys.argv[2])
        if manager.clear_history(user_id):
            print(f"✅ Cleared history for user {user_id}")
        else:
            print(f"⚠️ No history found for user {user_id}")
