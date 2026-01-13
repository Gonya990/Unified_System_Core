import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

from src.config_manager import ConfigManager
from src.inference_client import InferenceClient


def test_inference_client_ollama_format():
    async def run_test():
        cm = MagicMock(spec=ConfigManager)
        cm.get.side_effect = lambda k, d="": {
            "INFERENCE_PROVIDER": "ollama",
            "INFERENCE_BASE_URL": "http://localhost:11434",
            "INFERENCE_API_KEY": "",
            "MODEL_NAME": "llama3.2",
            "OLLAMA_BASE_URL": "http://localhost:11434",
            "OLLAMA_MODEL": "llama3.2"
        }.get(k, d)

        client = InferenceClient(cm)

        # Mock aiohttp response
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={"message": {"content": "Hello from Ollama"}})

        # Create async context managers for both session and response
        class PostContextManager:
            async def __aenter__(self):
                return mock_response
            async def __aexit__(self, *args):
                return None

        class SessionContextManager:
            async def __aenter__(self):
                return self
            async def __aexit__(self, *args):
                return None
            def post(self, *args, **kwargs):
                return PostContextManager()

        mock_session_cm = SessionContextManager()
        mock_client_session = MagicMock(return_value=mock_session_cm)

        with patch("src.inference_client.aiohttp.ClientSession", mock_client_session):
            # Unpack response tuple (content, usage)
            response, _ = await client.chat([{"role": "user", "content": "Hi"}])
            assert response == "Hello from Ollama"

    asyncio.run(run_test())
