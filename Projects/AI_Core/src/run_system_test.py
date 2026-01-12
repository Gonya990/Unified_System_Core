import asyncio
import os
import sqlite3

# Mock bot_config and dependencies before importing target modules
import sys
from datetime import datetime, timedelta
from types import ModuleType
from unittest.mock import MagicMock

mock_bot_config = ModuleType('bot_config')
mock_bot_config.BOT_TOKEN = "TEST_TOKEN"
mock_bot_config.MODEL_NAME = "llama3"
mock_bot_config.ALLOWED_USER_IDS = [12345]
sys.modules['bot_config'] = mock_bot_config

from calendar_client import CalendarClient
from conversation_manager import ConversationManager
from user_context_db import UserContextDB


async def run_integration_test():
    print("🚀 Starting Full System Integration Test...")

    # 1. Database & User Management Test
    print("\n--- 1. Database & User Test ---")
    db_path = "test_user_context.db"
    if os.path.exists(db_path): os.remove(db_path)
    db = UserContextDB(db_path=db_path)

    test_user_id = 999
    db.add_user(test_user_id, "test_user", "Test User Full")
    db.approve_user(test_user_id, True)

    user = db.get_user(test_user_id)
    assert user['username'] == "test_user"
    assert user['is_approved'] == 1
    print("✅ User registration and approval works.")

    # 2. Memory & Conversation Management Test
    print("\n--- 2. Memory & Context Test ---")
    conv = ConversationManager(storage_path="test_conversations")
    conv.add_message(test_user_id, "user", "My favorite color is Blue and I work as a Developer.")
    conv.add_message(test_user_id, "assistant", "That is great! I will remember that.")

    history = conv.get_history(test_user_id)
    assert len(history) == 2

    db.add_memory(test_user_id, "Occupation: Developer", "User works as a software developer.")
    memories = db.get_memories(test_user_id)
    assert len(memories) == 1
    assert memories[0]['fact_short'] == "Occupation: Developer"
    print("✅ Conversation history and long-term memory work.")

    # 3. Calendar Client Logic Test (Mocked API)
    print("\n--- 3. Calendar Client Logic ---")
    mock_creds = {"token": "test_token", "refresh_token": "test_refresh"}
    # We mock the service creation inside the client
    client = CalendarClient(credentials_dict=mock_creds)
    client.service = MagicMock()

    # Mock upcoming events response
    client.service.events().list().execute = MagicMock(return_value={
        'items': [{'summary': 'Integration Meeting', 'start': {'dateTime': '2025-12-31T15:00:00Z'}}]
    })

    events = client.get_upcoming_events(days=1)
    assert len(events) == 1
    assert events[0]['summary'] == 'Integration Meeting'
    print("✅ Calendar client handles events correctly.")

    # 4. Inactive User Detection
    print("\n--- 4. Proactive Logic Test ---")
    # Manually set old last_interaction in DB
    with sqlite3.connect(db_path) as conn:
        old_time = (datetime.now() - timedelta(hours=80)).strftime('%Y-%m-%d %H:%M:%S.%f')
        conn.execute("UPDATE users SET last_interaction = ? WHERE user_id = ?", (old_time, test_user_id))

    inactive = db.get_inactive_users(hours=72)
    assert len(inactive) == 1
    assert inactive[0]['user_id'] == test_user_id
    print("✅ Inactive user detection (72h+) works.")

    print("\n🎉 ALL TESTS PASSED SUCCESSFULLY!")

    # Cleanup
    if os.path.exists(db_path): os.remove(db_path)
    import shutil
    if os.path.exists("test_conversations"): shutil.rmtree("test_conversations")

if __name__ == "__main__":
    asyncio.run(run_integration_test())
