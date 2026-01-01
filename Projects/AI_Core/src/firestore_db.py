"""
Firestore Database Integration for AI Telegram Bot.
Uses Google Cloud Firestore (free tier: 50K reads, 20K writes/day, 1GB storage).

Falls back to SQLite if Firestore is not configured.
"""
import os
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List

logger = logging.getLogger(__name__)

# Try to import Firestore
try:
    from google.cloud import firestore
    from google.oauth2 import service_account
    FIRESTORE_AVAILABLE = True
except ImportError:
    FIRESTORE_AVAILABLE = False
    logger.warning("google-cloud-firestore not installed. Using SQLite fallback.")


class FirestoreDB:
    """
    Firestore-backed database with SQLite fallback.

    Free tier limits (per day):
    - 50,000 document reads
    - 20,000 document writes
    - 20,000 document deletes
    - 1 GB storage

    For a personal bot with 1-5 users, this is more than enough.
    """

    def __init__(self, credentials_path: Optional[str] = None, project_id: Optional[str] = None):
        self.db = None
        self.use_firestore = False

        # Try to initialize Firestore
        if FIRESTORE_AVAILABLE:
            try:
                creds_path = credentials_path or os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
                proj_id = project_id or os.environ.get("GCP_PROJECT_ID", "my-home-435112")

                if creds_path and os.path.exists(creds_path):
                    credentials = service_account.Credentials.from_service_account_file(creds_path)
                    self.db = firestore.Client(project=proj_id, credentials=credentials)
                    self.use_firestore = True
                    logger.info(f"Firestore initialized for project: {proj_id}")
                elif os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
                    # Use default credentials
                    self.db = firestore.Client(project=proj_id)
                    self.use_firestore = True
                    logger.info(f"Firestore initialized with default credentials: {proj_id}")
                else:
                    logger.warning("No Firestore credentials found. Using SQLite fallback.")
            except Exception as e:
                logger.error(f"Failed to initialize Firestore: {e}. Using SQLite fallback.")

        # Fallback to SQLite
        if not self.use_firestore:
            from user_context_db import UserContextDB
            self._sqlite = UserContextDB()
            logger.info("Using SQLite database (local mode)")

    # ==================== USER OPERATIONS ====================

    def add_user(self, user_id: int, username: str, full_name: str):
        """Add or update user in database."""
        if self.use_firestore:
            doc_ref = self.db.collection("users").document(str(user_id))
            doc = doc_ref.get()
            if not doc.exists:
                doc_ref.set({
                    "user_id": user_id,
                    "username": username,
                    "full_name": full_name,
                    "is_approved": False,
                    "is_google_connected": False,
                    "google_creds": None,
                    "last_interaction": firestore.SERVER_TIMESTAMP,
                    "created_at": firestore.SERVER_TIMESTAMP
                })
                logger.debug(f"User {user_id} added to Firestore")
        else:
            self._sqlite.add_user(user_id, username, full_name)

    def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user by ID."""
        if self.use_firestore:
            doc = self.db.collection("users").document(str(user_id)).get()
            if doc.exists:
                data = doc.to_dict()
                # Convert Firestore timestamps to datetime
                for key in ["last_interaction", "created_at"]:
                    if key in data and data[key]:
                        data[key] = data[key].isoformat() if hasattr(data[key], 'isoformat') else str(data[key])
                return data
            return None
        else:
            return self._sqlite.get_user(user_id)

    def update_last_interaction(self, user_id: int):
        """Update user's last interaction timestamp."""
        if self.use_firestore:
            self.db.collection("users").document(str(user_id)).update({
                "last_interaction": firestore.SERVER_TIMESTAMP
            })
        else:
            self._sqlite.update_last_interaction(user_id)

    def is_approved(self, user_id: int) -> bool:
        """Check if user is approved."""
        user = self.get_user(user_id)
        if user:
            return bool(user.get('is_approved', False))
        return False

    def approve_user(self, user_id: int, approve: bool = True):
        """Approve or unapprove user."""
        if self.use_firestore:
            self.db.collection("users").document(str(user_id)).update({
                "is_approved": approve
            })
        else:
            self._sqlite.approve_user(user_id, approve)

    def set_google_connected(self, user_id: int, connected: bool = True):
        """Set Google connection status."""
        if self.use_firestore:
            self.db.collection("users").document(str(user_id)).update({
                "is_google_connected": connected
            })
        else:
            self._sqlite.set_google_connected(user_id, connected)

    def get_inactive_users(self, hours: int = 72) -> List[Dict[str, Any]]:
        """Get users who haven't interacted for N hours.

        Note: For hours=0, returns all users (for admin panel).
        """
        if self.use_firestore:
            # Simple query to avoid needing composite index
            if hours == 0:
                # Return all users (admin panel use case)
                docs = self.db.collection("users").stream()
                return [doc.to_dict() for doc in docs]
            else:
                # Filter client-side to avoid composite index requirement
                cutoff = datetime.now() - timedelta(hours=hours)
                docs = self.db.collection("users").stream()
                results = []
                for doc in docs:
                    data = doc.to_dict()
                    if data.get("is_approved") and data.get("last_interaction"):
                        last_int = data["last_interaction"]
                        # Handle Firestore timestamp
                        if hasattr(last_int, 'timestamp'):
                            last_int = datetime.fromtimestamp(last_int.timestamp())
                        if last_int < cutoff:
                            results.append(data)
                return results
        else:
            return self._sqlite.get_inactive_users(hours)

    # ==================== MEMORY OPERATIONS ====================

    def add_memory(self, user_id: int, fact_short: str, fact_full: str):
        """Add a memory/fact for user."""
        if self.use_firestore:
            self.db.collection("users").document(str(user_id))\
                .collection("memories").add({
                    "fact_short": fact_short,
                    "fact_full": fact_full,
                    "source_date": firestore.SERVER_TIMESTAMP,
                    "created_at": firestore.SERVER_TIMESTAMP
                })
        else:
            self._sqlite.add_memory(user_id, fact_short, fact_full)

    def get_memories(self, user_id: int, limit: int = 10) -> List[Dict[str, Any]]:
        """Get user's memories."""
        if self.use_firestore:
            docs = self.db.collection("users").document(str(user_id))\
                .collection("memories")\
                .order_by("created_at", direction=firestore.Query.DESCENDING)\
                .limit(limit)\
                .stream()
            return [doc.to_dict() for doc in docs]
        else:
            return self._sqlite.get_memories(user_id, limit)

    def clear_memories(self, user_id: int):
        """Clear all memories for user."""
        if self.use_firestore:
            memories_ref = self.db.collection("users").document(str(user_id)).collection("memories")
            docs = memories_ref.stream()
            for doc in docs:
                doc.reference.delete()
        else:
            self._sqlite.clear_memories(user_id)

    # ==================== EVENT CONTEXT OPERATIONS ====================

    def add_event_context(self, user_id: int, event_title: str, context_description: str, event_time: datetime):
        """Add context for a calendar event."""
        if self.use_firestore:
            self.db.collection("users").document(str(user_id))\
                .collection("event_contexts").add({
                    "event_title": event_title,
                    "context_description": context_description,
                    "event_time": event_time,
                    "created_at": firestore.SERVER_TIMESTAMP
                })
        else:
            self._sqlite.add_event_context(user_id, event_title, context_description, event_time)

    def get_event_contexts(self, user_id: int) -> Dict[str, str]:
        """Get all event contexts for user (title -> description mapping)."""
        if self.use_firestore:
            docs = self.db.collection("users").document(str(user_id))\
                .collection("event_contexts").stream()
            return {doc.to_dict()['event_title']: doc.to_dict()['context_description'] for doc in docs}
        else:
            # SQLite version - need to query directly
            import sqlite3
            with sqlite3.connect(self._sqlite.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT event_title, context_description FROM event_contexts WHERE user_id = ?",
                    (user_id,)
                )
                return {row['event_title']: row['context_description'] for row in cursor.fetchall()}

    # ==================== USAGE TRACKING ====================

    def log_usage(self, user_id: int, provider: str, model: str, tokens: int, request_type: str = "chat"):
        """Log API usage for cost tracking."""
        if self.use_firestore:
            self.db.collection("usage_logs").add({
                "user_id": user_id,
                "provider": provider,
                "model": model,
                "tokens": tokens,
                "request_type": request_type,
                "timestamp": firestore.SERVER_TIMESTAMP
            })

    def get_usage_stats(self, user_id: int, days: int = 30) -> Dict[str, Any]:
        """Get usage statistics for user."""
        if self.use_firestore:
            cutoff = datetime.now() - timedelta(days=days)
            docs = self.db.collection("usage_logs")\
                .where("user_id", "==", user_id)\
                .where("timestamp", ">=", cutoff)\
                .stream()

            stats = {"total_tokens": 0, "requests": 0, "by_model": {}}
            for doc in docs:
                data = doc.to_dict()
                stats["total_tokens"] += data.get("tokens", 0)
                stats["requests"] += 1
                model = data.get("model", "unknown")
                stats["by_model"][model] = stats["by_model"].get(model, 0) + data.get("tokens", 0)

            return stats
        return {}

    # ==================== KV STORE ====================

    def set_kv(self, key: str, value: str):
        """Set a key-value pair."""
        if self.use_firestore:
            self.db.collection("kv_store").document(key).set({"value": value})
        else:
            import sqlite3
            with sqlite3.connect(self._sqlite.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT OR REPLACE INTO kv_store (key, value) VALUES (?, ?)", (key, value))
                conn.commit()

    def get_kv(self, key: str) -> Optional[str]:
        """Get a value by key."""
        if self.use_firestore:
            doc = self.db.collection("kv_store").document(key).get()
            if doc.exists:
                return doc.to_dict().get("value")
            return None
        else:
            import sqlite3
            with sqlite3.connect(self._sqlite.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT value FROM kv_store WHERE key = ?", (key,))
                row = cursor.fetchone()
                return row[0] if row else None

    # ==================== CONVERSATION HISTORY ====================

    def save_conversation(self, user_id: int, messages: List[Dict[str, str]]):
        """Save conversation history."""
        if self.use_firestore:
            self.db.collection("users").document(str(user_id)).update({
                "conversation_history": messages,
                "conversation_updated": firestore.SERVER_TIMESTAMP
            })

    def get_conversation(self, user_id: int) -> List[Dict[str, str]]:
        """Get conversation history."""
        if self.use_firestore:
            doc = self.db.collection("users").document(str(user_id)).get()
            if doc.exists:
                return doc.to_dict().get("conversation_history", [])
        return []

    # ==================== HEALTH CHECK ====================

    def health_check(self) -> Dict[str, Any]:
        """Check database health and connection."""
        result = {
            "backend": "firestore" if self.use_firestore else "sqlite",
            "connected": False,
            "error": None
        }

        try:
            if self.use_firestore:
                # Try a simple read
                self.db.collection("_health").document("check").get()
                result["connected"] = True
            else:
                result["connected"] = True  # SQLite is always available
        except Exception as e:
            result["error"] = str(e)

        return result


# Singleton instance
_db_instance: Optional[FirestoreDB] = None

def get_db() -> FirestoreDB:
    """Get or create database instance."""
    global _db_instance
    if _db_instance is None:
        _db_instance = FirestoreDB()
    return _db_instance