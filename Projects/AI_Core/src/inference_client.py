"""
Unified Inference Client for AI Telegram Bot.
Supports Ollama, OpenAI-compatible, Gemini, and custom endpoints.
"""
import json
import logging
from typing import Optional
import aiohttp
from pathlib import Path
import random

try:
    from .config_manager import ConfigManager
    from .modules.swarm_manager import SwarmManager
except ImportError:
    from config_manager import ConfigManager
    try:
        from modules.swarm_manager import SwarmManager
    except ImportError:
        # Fallback for direct testing
        SwarmManager = None

logger = logging.getLogger(__name__)

# Lazy import for Gemini
_gemini_client = None
_gemini_client_key = None


def _get_gemini_client(api_key: str):
    """Lazy load and configure Gemini client using new SDK."""
    global _gemini_client, _gemini_client_key
    try:
        from google import genai
        # from google.genai.types import GenerateContentConfig
        
        if not _gemini_client or _gemini_client_key != api_key:
            _gemini_client = genai.Client(api_key=api_key)
            _gemini_client_key = api_key
        return _gemini_client
    except ImportError:
        logger.error("google-genai not installed. Run: pip install google-genai")
        return None
    except Exception as e:
        logger.error(f"Failed to configure Gemini: {e}")
        return None

class InferenceClient:
    """Unified client for multiple AI inference providers."""
    
    def __init__(self, config: ConfigManager):
        self.config = config
        self.provider = config.get("INFERENCE_PROVIDER", "ollama")
        self.model = config.get("MODEL_NAME", "llama3")
        self.endpoint = config.get("INFERENCE_ENDPOINT", "http://localhost:11434")
        self.api_key = config.get("INFERENCE_API_KEY", "")
        
        # Load resources for swarm
        resources_path = Path(__file__).parent.parent / "config" / "resources.yaml"
        self.swarm = SwarmManager(resources_path) if SwarmManager else None

    async def chat(self, messages: list, system_prompt: Optional[str] = None):
        """Routed chat request."""
        provider = self.config.get("INFERENCE_PROVIDER", self.provider)
        
        if provider == "gemini":
            return await self._chat_gemini(messages, system_prompt)
        elif provider == "openai":
            return await self._chat_openai(messages, system_prompt)
        elif provider == "openrouter":
            return await self._chat_openrouter(messages, system_prompt)
        else:
            return await self._chat_ollama(messages, system_prompt)

    async def _chat_gemini(self, messages: list, system_prompt: Optional[str] = None):
        """Gemini SDK integration with Swarm support."""
        api_key = self.api_key
        
        # Priority: Swarm Key -> Config Key
        if self.swarm:
            swarm_key = self.swarm.get_gemini_key()
            if swarm_key:
                api_key = swarm_key
                
        client = _get_gemini_client(api_key)
        if not client:
            return "Error: Gemini client not configured.", {}

        try:
            # Prepare contents
            contents = []
            if system_prompt:
                # The new genai SDK handles system prompt in config
                pass
                
            for m in messages:
                contents.append({
                    "role": "user" if m["role"] == "user" else "model",
                    "parts": [{"text": m["content"]}]
                })

            # Call Gemini
            model_name = self.config.get("GEMINI_MODEL", "gemini-2.0-flash-exp")
            
            # Use asyncio loop for blocking SDK call
            import asyncio
            loop = asyncio.get_event_loop()
            
            def call_sdk():
                from google.genai.types import GenerateContentConfig
                return client.models.generate_content(
                    model=model_name,
                    contents=contents,
                    config=GenerateContentConfig(
                        system_instruction=system_prompt if system_prompt else None
                    )
                )
                
            response = await loop.run_in_executor(None, call_sdk)
            
            # Parse usage
            usage = {
                "prompt_tokens": response.usage_metadata.prompt_token_count if response.usage_metadata else 0,
                "completion_tokens": response.usage_metadata.candidates_token_count if response.usage_metadata else 0,
                "total_tokens": response.usage_metadata.total_token_count if response.usage_metadata else 0
            }
            
            return response.text, usage

        except Exception as e:
            logger.error(f"Gemini Chat Error: {e}")
            
            # If 429, mark key as failed in swarm
            if "429" in str(e) and self.swarm:
                self.swarm.mark_key_failed("gemini", api_key)
                # Failover to next key could be implemented here with recursion
                
            return f"Error: {e}", {}

    async def _chat_ollama(self, messages: list, system_prompt: Optional[str] = None):
        """Ollama API request."""
        url = f"{self.endpoint}/api/chat"
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False
        }
        if system_prompt:
            payload["messages"].insert(0, {"role": "system", "content": system_prompt})

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return data.get("message", {}).get("content", ""), {
                            "total_tokens": data.get("prompt_eval_count", 0) + data.get("eval_count", 0)
                        }
                    return f"Error: Ollama status {resp.status}", {}
        except Exception as e:
            return f"Ollama Connection Error: {e}", {}

    async def _chat_openai(self, messages: list, system_prompt: Optional[str] = None):
        """OpenAI API request."""
        # Simplified OpenAI request
        return "OpenAI integration stub", {}
        
    async def _chat_openrouter(self, messages: list, system_prompt: Optional[str] = None):
        """OpenRouter API request."""
        return "OpenRouter integration stub", {}
