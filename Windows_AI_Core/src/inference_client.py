"""
Unified Inference Client for AI Telegram Bot.
Supports Ollama, OpenAI-compatible, Gemini, and custom endpoints.
"""
import json
import logging
from typing import Optional
import aiohttp

from .config_manager import ConfigManager

logger = logging.getLogger(__name__)

# Lazy import for Gemini
_gemini_client = None


def _get_gemini_model(api_key: str, model_name: str):
    """Lazy load and configure Gemini client."""
    global _gemini_client
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        return genai.GenerativeModel(model_name)
    except ImportError:
        logger.error("google-generativeai not installed. Run: pip install google-generativeai")
        return None
    except Exception as e:
        logger.error(f"Failed to configure Gemini: {e}")
        return None


class InferenceClient:
    """Unified client for multiple LLM backends."""
    
    PROVIDERS = ["ollama", "openai", "gemini"]
    
    def __init__(self, config: ConfigManager):
        self.config = config
        self._session: Optional[aiohttp.ClientSession] = None
        self._session_api_key: str = ""  # Track the API key used for current session
    
    @property
    def provider(self) -> str:
        """Get current inference provider."""
        return self.config.get("INFERENCE_PROVIDER", "ollama").lower()
    
    @property
    def base_url(self) -> str:
        """Get base URL based on provider."""
        provider = self.provider
        if provider == "openai":
            return self.config.get("OPENAI_BASE_URL", self.config.get("INFERENCE_BASE_URL", "https://api.openai.com"))
        elif provider == "gemini":
            return "https://generativelanguage.googleapis.com"
        else:  # ollama
            return self.config.get("OLLAMA_BASE_URL", self.config.get("INFERENCE_BASE_URL", "http://localhost:11434"))
    
    @property
    def api_key(self) -> str:
        """Get API key based on provider."""
        provider = self.provider
        if provider == "openai":
            return self.config.get("OPENAI_API_KEY", self.config.get("INFERENCE_API_KEY", ""))
        elif provider == "gemini":
            return self.config.get("GEMINI_API_KEY", self.config.get("INFERENCE_API_KEY", ""))
        else:  # ollama
            return self.config.get("INFERENCE_API_KEY", "")
    
    @property
    def model(self) -> str:
        """Get model name based on provider."""
        provider = self.provider
        if provider == "openai":
            return self.config.get("OPENAI_MODEL", self.config.get("MODEL_NAME", "gpt-4o-mini"))
        elif provider == "gemini":
            return self.config.get("GEMINI_MODEL", self.config.get("MODEL_NAME", "gemini-1.5-flash"))
        else:  # ollama
            return self.config.get("OLLAMA_MODEL", self.config.get("MODEL_NAME", "llama3.2"))
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session. Recreates if API key changed."""
        current_key = self.api_key
        
        # Recreate session if API key changed or session is closed
        if self._session is None or self._session.closed or self._session_api_key != current_key:
            if self._session and not self._session.closed:
                await self._session.close()
            
            headers = {"Content-Type": "application/json"}
            if current_key and self.provider != "gemini":
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
        
        Supports Ollama, OpenAI-compatible, and Gemini APIs.
        """
        provider = self.provider
        
        # Handle Gemini separately (uses SDK)
        if provider == "gemini":
            return await self._chat_gemini(messages, system_prompt)
        
        session = await self._get_session()
        
        # Build messages list with system prompt
        full_messages = []
        if system_prompt:
            full_messages.append({"role": "system", "content": system_prompt})
        full_messages.extend(messages)
        
        # Detect endpoint type and build request
        if provider == "openai" or "openai" in self.base_url.lower() or self.api_key:
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
            logger.info(f"[{provider}] Sending request to {url} with model {self.model}")
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
    
    async def _chat_gemini(self, messages: list[dict], system_prompt: str = "") -> str:
        """Handle Gemini API calls using the SDK."""
        try:
            model = _get_gemini_model(self.api_key, self.model)
            if not model:
                return "[Error]: Gemini client not configured. Check API key."
            
            # Build prompt from messages
            prompt_parts = []
            if system_prompt:
                prompt_parts.append(f"System: {system_prompt}\n\n")
            
            for msg in messages:
                role = msg.get("role", "user")
                content = msg.get("content", "")
                if role == "user":
                    prompt_parts.append(f"User: {content}\n")
                elif role == "assistant":
                    prompt_parts.append(f"Assistant: {content}\n")
            
            prompt = "".join(prompt_parts) + "Assistant:"
            
            logger.info(f"[gemini] Sending request with model {self.model}")
            
            # Gemini SDK is synchronous, run in executor
            import asyncio
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(None, model.generate_content, prompt)
            
            return response.text
            
        except Exception as e:
            logger.exception(f"Gemini error: {e}")
            return f"[Gemini Error]: {str(e)}"
    
    async def health_check(self) -> bool:
        """Check if the inference endpoint is reachable."""
        provider = self.provider
        
        if provider == "gemini":
            # For Gemini, just check if API key is set
            return bool(self.api_key)
        
        session = await self._get_session()
        try:
            if provider == "openai":
                url = f"{self.base_url.rstrip('/')}/v1/models"
            else:
                url = f"{self.base_url.rstrip('/')}/api/tags"
            async with session.get(url, timeout=5) as response:
                return response.status == 200
        except Exception:
            return False
    
    async def list_models(self) -> list[str]:
        """Get list of available models from the provider."""
        provider = self.provider
        models = []
        
        if provider == "gemini":
            # Return known Gemini models
            return [
                "gemini-1.5-flash",
                "gemini-1.5-flash-8b", 
                "gemini-1.5-pro",
                "gemini-1.0-pro",
                "gemini-2.0-flash-exp",
            ]
        
        session = await self._get_session()
        
        try:
            # Try Ollama format first
            if provider == "ollama" or "openai" not in self.base_url.lower():
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
