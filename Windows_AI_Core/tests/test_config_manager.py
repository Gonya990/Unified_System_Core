import pytest
import os
import json
from pathlib import Path
from src.config_manager import ConfigManager

@pytest.fixture
def temp_config_file(tmp_path):
    config_file = tmp_path / "bot_config.json"
    os.environ["CONFIG_PATH"] = str(config_file)
    os.environ["TELEGRAM_BOT_TOKEN"] = "test_token_123456789"
    return config_file

def test_config_manager_init(temp_config_file):
    cm = ConfigManager()
    assert cm.get("TELEGRAM_BOT_TOKEN") == "test_token_123456789"
    assert cm.get("MODEL_NAME") == "llama3.2"

def test_config_manager_set_get(temp_config_file):
    cm = ConfigManager()
    cm.set("MODEL_NAME", "phi3")
    assert cm.get("MODEL_NAME") == "phi3"
    
    # Reload to verify persistence
    cm2 = ConfigManager()
    assert cm2.get("MODEL_NAME") == "phi3"

def test_config_manager_encryption(temp_config_file):
    cm = ConfigManager()
    test_key = "secret_api_key_value"
    cm.set("INFERENCE_API_KEY", test_key)
    
    # Check that the file content is actually encrypted
    with open(temp_config_file, "r") as f:
        data = json.load(f)
        encrypted_val = data["INFERENCE_API_KEY"]
        assert encrypted_val != test_key
    
    # Reload to verify decryption
    cm2 = ConfigManager()
    assert cm2.get("INFERENCE_API_KEY") == test_key

def test_config_manager_status(temp_config_file):
    cm = ConfigManager()
    cm.set("INFERENCE_BASE_URL", "http://test-url")
    status = cm.get_status()
    assert status["inference_url"] == "http://test-url"
    assert status["api_key_set"] == False
    
    cm.set("INFERENCE_API_KEY", "some-key")
    status = cm.get_status()
    assert status["api_key_set"] == True
