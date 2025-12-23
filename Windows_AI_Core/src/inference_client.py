"""
Unified Inference Client for AI Telegram Bot.
Supports Ollama, OpenAI-compatible, and custom endpoints.
"""
import json
import logging
from typing import Optional
import aiohttp

from .config_manager import ConfigManager

logger = logging.getLogger(__name__)


class InferenceClient:
    """Unified client for multiple LLM backends."""
    
    def __init__(self, config: ConfigManager):
        self.config = config
        self._session: Optional[aiohttp.ClientSession] = None
        self._session_api_key: str = ""  # Track the API key used for current session
    
    @property
    def base_url(self) -> str:
        return self.config.get("INFERENCE_BASE_URL", "http://localhost:11434")
    
    @property
    def api_key(self) -> str:
        return self.config.get("INFERENCE_API_KEY", "")
    
    @property
    def model(self) -> str:
        return self.config.get("MODEL_NAME", "llama3.2")
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session. Recreates if API key changed."""
        current_key = self.api_key
        
        # Recreate session if API key changed or session is closed
        if self._session is None or self._session.closed or self._session_api_key != current_key:
            if self._session and not self._session.closed:
                await self._session.close()
            
            headers = {"Content-Type": "application/json"}
            if current_key:
                headers["Authorization"] = f"Bearer {current_key}"
            self._session = aiohttp.ClientSession(headers=headers)
            self._session_api_key = current_key
        return self._session
    
    async def close(self) -> None:
        """Close the HTTP session."""
        if self._session and not self._session.closed:
            await self._session.close()
    
    async def chat(self, messages: list[dict], system_prompt: str = "") -> str:
        """
        Send chat completion request to configured endpoint.
        
        Supports both Ollama and OpenAI-compatible APIs.
        """
        session = await self._get_session()
        
        # Build messages list with system prompt
        full_messages = []
        if system_prompt:
            full_messages.append({"role": "system", "content": system_prompt})
        full_messages.extend(messages)
        
        # Detect endpoint type and build request
        if "openai" in self.base_url.lower() or self.api_key:
            # OpenAI-compatible API
            url = f"{self.base_url.rstrip('/')}/v1/chat/completions"
            payload = {
                "model": self.model,
                "messages": full_messages,
                "temperature": 0.7,
                "max_tokens": 500,
            }
        else:
            # Ollama API
            url = f"{self.base_url.rstrip('/')}/api/chat"
            payload = {
                "model": self.model,
                "messages": full_messages,
                "stream": False,
            }
        
        try:
            logger.info(f"Sending request to {url} with model {self.model}")
            async with session.post(url, json=payload, timeout=60) as response:
                if response.status != 200:
                    error_text = await response.text()
                    logger.error(f"Inference error {response.status}: {error_text}")
                    return f"[Error {response.status}]: Failed to get response from AI"
                
                data = await response.json()
                
                # Parse response based on API type
                if "choices" in data:
                    # OpenAI format
                    return data["choices"][0]["message"]["content"]
                elif "message" in data:
                    # Ollama format
                    return data["message"]["content"]
                else:
                    logger.warning(f"Unknown response format: {data}")
                    return str(data)
                    
        except aiohttp.ClientError as e:
            logger.error(f"Connection error: {e}")
            return f"[Connection Error]: Cannot reach inference server at {self.base_url}"
        except Exception as e:
            logger.exception(f"Unexpected error during inference: {e}")
            return f"[Error]: {str(e)}"
    
    async def health_check(self) -> bool:
        """Check if the inference endpoint is reachable."""
        session = await self._get_session()
        try:
            # Try Ollama health endpoint
            url = f"{self.base_url.rstrip('/')}/api/tags"
            async with session.get(url, timeout=5) as response:
                return response.status == 200
        except Exception:
            return False
    
    async def list_models(self) -> list[str]:
        """Get list of available models from the provider."""
        session = await self._get_session()
        models = []
        
        try:
            # Try Ollama format first
            if "openai" not in self.base_url.lower():
                url = f"{self.base_url.rstrip('/')}/api/tags"
                async with session.get(url, timeout=10) as response:
                    if response.status == 200:
                        data = await response.json()
                        if "models" in data:
                            models = [m.get("name", m.get("model", "unknown")) for m in data["models"]]
                            return models
            
            # Try OpenAI format
            url = f"{self.base_url.rstrip('/')}/v1/models"
            async with session.get(url, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    if "data" in data:
                        models = [m.get("id", "unknown") for m in data["data"]]
                        return models
        except Exception as e:
            logger.error(f"Failed to list models: {e}")
        
        return models
