#!/usr/bin/env python3
"""Simple test runner that captures output."""
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def run_tests():
    print("=" * 60)
    print("AI Telegram Bot - Test Suite")
    print("=" * 60)

    # Test 1: Import tests
    print("\n[1/4] Testing imports...")
    try:
        from src.config_manager import ConfigManager
        from src.health import start_health_server
        from src.inference_client import InferenceClient
        from src.logging_config import setup_logging
        print("✅ All imports successful")
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return 1

    # Test 2: ConfigManager
    print("\n[2/4] Testing ConfigManager...")
    try:
        os.environ["TELEGRAM_BOT_TOKEN"] = "test_token_123"
        os.environ["CONFIG_PATH"] = "/tmp/test_config.json"
        cm = ConfigManager()
        assert cm.get("TELEGRAM_BOT_TOKEN") == "test_token_123"
        cm.set("MODEL_NAME", "test-model")
        assert cm.get("MODEL_NAME") == "test-model"
        status = cm.get_status()
        assert "inference_url" in status
        print("✅ ConfigManager tests passed")
    except Exception as e:
        print(f"❌ ConfigManager test failed: {e}")
        return 1

    # Test 3: InferenceClient initialization
    print("\n[3/4] Testing InferenceClient...")
    try:
        client = InferenceClient(cm)
        assert client.base_url is not None
        assert client.model == "test-model"
        print("✅ InferenceClient tests passed")
    except Exception as e:
        print(f"❌ InferenceClient test failed: {e}")
        return 1

    # Test 4: Health server
    print("\n[4/4] Testing Health server...")
    try:
        from src.health import HealthHandler
        assert HealthHandler is not None
        print("✅ Health module tests passed")
    except Exception as e:
        print(f"❌ Health test failed: {e}")
        return 1

    print("\n" + "=" * 60)
    print("🎉 ALL TESTS PASSED!")
    print("=" * 60)
    return 0

if __name__ == "__main__":
    sys.exit(run_tests())
