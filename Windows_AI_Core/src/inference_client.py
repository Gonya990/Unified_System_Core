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


def _get_gemini_client(api_key: str):
    """Lazy load and configure Gemini client using new SDK."""
    global _gemini_client
    try:
        from google import genai
        from google.genai.types import GenerateContentConfig
        
        if not _gemini_client or _gemini_client.api_key != api_key:
            _gemini_client = genai.Client(api_key=api_key)
        return _gemini_client
    except ImportError:
        logger.error("google-genai not installed. Run: pip install google-genai")
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
    
    async def chat(self, messages: list[dict], system_prompt: str = "") -> tuple[str, dict]:
        """
        Send chat completion request to configured endpoint.
        
        Supports Ollama, OpenAI-compatible, and Gemini APIs.
        Returns: (response_text, usage_stats)
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
        
        usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
        
        try:
            logger.info(f"[{provider}] Sending request to {url} with model {self.model}")
            async with session.post(url, json=payload, timeout=60) as response:
                if response.status != 200:
                    error_text = await response.text()
                    logger.error(f"Inference error {response.status}: {error_text}")
                    return f"[Error {response.status}]: Failed to get response from AI", usage
                
                data = await response.json()
                
                # Parse response based on API type
                if "choices" in data:
                    # OpenAI format
                    text = data["choices"][0]["message"]["content"]
                    if "usage" in data:
                        usage = data["usage"]
                    return text, usage
                elif "message" in data:
                    # Ollama format
                    text = data["message"]["content"]
                    if "prompt_eval_count" in data:
                         usage["prompt_tokens"] = data.get("prompt_eval_count", 0)
                         usage["completion_tokens"] = data.get("eval_count", 0)
                         usage["total_tokens"] = usage["prompt_tokens"] + usage["completion_tokens"]
                    return text, usage
                else:
                    logger.warning(f"Unknown response format: {data}")
                    return str(data), usage
                    
        except aiohttp.ClientError as e:
            logger.error(f"Connection error: {e}")
            return f"[Connection Error]: Cannot reach inference server at {self.base_url}", usage
        except Exception as e:
            logger.exception(f"Unexpected error during inference: {e}")
            return f"[Error]: {str(e)}", usage
    
    async def _chat_gemini(self, messages: list[dict], system_prompt: str = "") -> tuple[str, dict]:
        """Handle Gemini API calls using the SDK."""
        usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
        try:
            client = _get_gemini_client(self.api_key)
            if not client:
                return "[Error]: Gemini client not configured. Check API key.", usage
            
            # Convert messages to Gemini format
            # Gemini 2.0 / 1.5 uses 'contents' list with 'role' and 'parts'
            # roles: 'user' or 'model' (not 'assistant')
            gemini_contents = []
            
            # Add system prompt? 
            # The new SDK supports 'config' with 'system_instruction'
            
            for msg in messages:
                role = msg.get("role", "user")
                content = msg.get("content", "")
                
                # Map 'assistant' to 'model'
                if role == "assistant":
                    role = "model"
                elif role == "system":
                    # System prompt is handled separately in config, but if passed in messages list,
                    # we might need to extract it or handle it. 
                    # For now, simplistic handling:
                    continue
                
                gemini_contents.append({
                    "role": role,
                    "parts": [{"text": content}]
                })

            logger.info(f"[{self.provider}] Sending request to Gemini with model {self.model}")
            
            # Gemini SDK is synchronous, run in executor
            import asyncio
            from google.genai.types import GenerateContentConfig
            
            config = None
            if system_prompt:
                config = GenerateContentConfig(system_instruction=system_prompt)
            
            loop = asyncio.get_event_loop()
            
            def call_gemini():
                return client.models.generate_content(
                    model=self.model,
                    contents=gemini_contents,
                    config=config
                )

            response = await loop.run_in_executor(None, call_gemini)
            
            # Extract usage metadata if available
            if hasattr(response, "usage_metadata"):
                usage["prompt_tokens"] = response.usage_metadata.prompt_token_count
                usage["completion_tokens"] = response.usage_metadata.candidates_token_count
                usage["total_tokens"] = response.usage_metadata.total_token_count
                
            return response.text, usage
            
        except Exception as e:
            logger.exception(f"Gemini error: {e}")
            return f"[Gemini Error]: {str(e)}", usage
    
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
            # Return known Gemini models from Google AI Studio
            return [
                "gemini-2.0-flash-exp",
                "gemini-exp-1206",
                "gemini-1.5-flash",
                "gemini-1.5-flash-8b", 
                "gemini-1.5-pro",
                "gemini-1.0-pro",
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
