"""
Tests for Core Components (Usage Tracker, Task Manager).
"""
import pytest
import os
import sqlite3
from src.usage_tracker import UsageTracker
from src.task_manager import TaskManager

# Use in-memory DB or temp file
TEST_DB = "test_core.db"

@pytest.fixture
def clean_db():
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    yield TEST_DB
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

def test_usage_tracker(clean_db):
    tracker = UsageTracker(db_path=clean_db)
    
    # Log usage
    tracker.log_usage(
        user_id=123,
        username="test_user",
        provider="openai",
        model="gpt-4",
        usage_stats={"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30}
    )
    
    # Verify
    stats = tracker.get_user_stats(123)
    assert stats is not None
    assert stats["requests"] == 1
    assert stats["total_tokens"] == 30
    assert stats["by_model"]["gpt-4"] == 30

def test_task_manager(clean_db):
    tm = TaskManager(db_path=clean_db)
    user_id = 999
    
    # Add task
    task_id = tm.add_task(user_id, "Buy milk")
    assert task_id > 0
    
    # List tasks
    tasks = tm.list_tasks(user_id)
    assert len(tasks) == 1
    assert tasks[0]["text"] == "Buy milk"
    assert tasks[0]["status"] == "pending"
    
    # Complete task
    success = tm.complete_task(user_id, task_id)
    assert success
    
    # Verify list empty (pending)
    tasks = tm.list_tasks(user_id)
    assert len(tasks) == 0

