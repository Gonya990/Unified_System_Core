import aiohttp
import logging
from typing import Optional
from .base import BaseProvider, ProviderResponse

logger = logging.getLogger(__name__)

class OllamaProvider(BaseProvider):
    """Ollama provider for local/node inference (Windows Node)."""

    name: str = "ollama"

    def __init__(self, base_url: str, model: str = "llama3.2"):
        super().__init__(api_key="local", model=model, base_url=base_url)
        self.base_url = base_url.rstrip("/")
        self.session: Optional[aiohttp.ClientSession] = None

    async def _get_session(self) -> aiohttp.ClientSession:
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
        return self.session

    async def generate(self, prompt: str, system_prompt: str = "") -> ProviderResponse:
        import time
        start_time = time.time()
        
        url = f"{self.base_url}/api/chat"
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "options": {
                "num_predict": 1024,
                "temperature": 0.7,
            }
        }

        try:
            session = await self._get_session()
            async with session.post(url, json=payload, timeout=60) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    content = data.get("message", {}).get("content", "")
                    prompt_tokens = data.get("prompt_eval_count", 0)
                    completion_tokens = data.get("eval_count", 0)
                    
                    return ProviderResponse(
                        provider_name=self.name,
                        model=self.model,
                        content=content,
                        latency_ms=(time.time() - start_time) * 1000,
                        tokens_used=prompt_tokens + completion_tokens,
                        error=None
                    )
                else:
                    err_text = await resp.text()
                    logger.error(f"Ollama error: {resp.status} - {err_text}")
                    return ProviderResponse(
                        provider_name=self.name,
                        model=self.model,
                        content="",
                        latency_ms=(time.time() - start_time) * 1000,
                        error=f"Error: {resp.status}"
                    )
        except Exception as e:
            logger.error(f"Ollama exception: {e}")
            return ProviderResponse(
                provider_name=self.name,
                model=self.model,
                content="",
                latency_ms=(time.time() - start_time) * 1000,
                error=f"Exception: {str(e)}"
            )

    async def health_check(self) -> bool:
        try:
            session = await self._get_session()
            async with session.get(f"{self.base_url}/api/tags", timeout=5) as resp:
                return resp.status == 200
        except Exception:
            return False

    async def close(self):
        if self.session and not self.session.closed:
            await self.session.close()
