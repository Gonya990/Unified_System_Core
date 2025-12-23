import pytest
import aiohttp
from unittest.mock import AsyncMock, patch
from src.inference_client import InferenceClient
from src.config_manager import ConfigManager

@pytest.fixture
def mock_config():
    cm = MagicMock(spec=ConfigManager)
    cm.get.side_effect = lambda k, d="": {
        "INFERENCE_BASE_URL": "http://localhost:11434",
        "INFERENCE_API_KEY": "",
        "MODEL_NAME": "llama3.2"
    }.get(k, d)
    return cm

from unittest.mock import MagicMock

@pytest.mark.asyncio
async def test_inference_client_ollama_format():
    cm = MagicMock(spec=ConfigManager)
    cm.get.side_effect = lambda k, d="": {
        "INFERENCE_BASE_URL": "http://localhost:11434",
        "INFERENCE_API_KEY": "",
        "MODEL_NAME": "llama3.2"
    }.get(k, d)
    
    client = InferenceClient(cm)
    
    # Mock aiohttp response
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.json.return_value = {"message": {"content": "Hello from Ollama"}}
    
    mock_session = AsyncMock()
    mock_session.post.return_value.__aenter__.return_value = mock_response
    
    with patch("aiohttp.ClientSession", return_value=mock_session):
        response = await client.chat([{"role": "user", "content": "Hi"}])
        assert response == "Hello from Ollama"
        
    await client.close()

@pytest.mark.asyncio
async def test_inference_client_openai_format():
    cm = MagicMock(spec=ConfigManager)
    cm.get.side_effect = lambda k, d="": {
        "INFERENCE_BASE_URL": "https://api.openai.com",
        "INFERENCE_API_KEY": "sk-test",
        "MODEL_NAME": "gpt-4"
    }.get(k, d)
    
    client = InferenceClient(cm)
    
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.json.return_value = {
        "choices": [{"message": {"content": "Hello from OpenAI"}}]
    }
    
    mock_session = AsyncMock()
    mock_session.post.return_value.__aenter__.return_value = mock_response
    
    with patch("aiohttp.ClientSession", return_value=mock_session):
        response = await client.chat([{"role": "user", "content": "Hi"}])
        assert response == "Hello from OpenAI"
        
    await client.close()
