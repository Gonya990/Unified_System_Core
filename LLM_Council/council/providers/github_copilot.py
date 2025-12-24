"""
GitHub Copilot Provider for LLM Council.
Uses GitHub's API with Copilot-enabled tokens.
"""

import logging
from typing import Optional
import httpx

from .base import BaseProvider, ProviderResponse

logger = logging.getLogger(__name__)


class GitHubCopilotProvider(BaseProvider):
    """GitHub Copilot API provider."""
    
    name = "github_copilot"
    
    # GitHub Copilot uses OpenAI-compatible API via GitHub
    DEFAULT_BASE_URL = "https://api.githubcopilot.com"
    
    def __init__(
        self, 
        api_key: str,  # GitHub token (ghp_...)
        model: str = "gpt-4o",
        base_url: Optional[str] = None
    ):
        super().__init__(api_key, model, base_url or self.DEFAULT_BASE_URL)
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "Editor-Version": "vscode/1.85.0",
                "Editor-Plugin-Version": "copilot/1.0.0",
            },
            timeout=60.0
        )
    
    async def generate(self, prompt: str, system_prompt: str = "") -> ProviderResponse:
        """Generate response using GitHub Copilot API."""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        with self._measure_time() as timer:
            try:
                response = await self._client.post(
                    "/chat/completions",
                    json={
                        "model": self.model,
                        "messages": messages,
                        "temperature": 0.7,
                        "max_tokens": 2000,
                    }
                )
                response.raise_for_status()
                data = response.json()
                
                content = data["choices"][0]["message"]["content"]
                tokens = data.get("usage", {}).get("total_tokens", 0)
                
                return ProviderResponse(
                    provider_name=self.name,
                    model=self.model,
                    content=content,
                    latency_ms=timer.elapsed_ms,
                    tokens_used=tokens,
                    metadata={"source": "github_copilot"}
                )
                
            except httpx.HTTPStatusError as e:
                logger.error(f"GitHub Copilot HTTP error: {e.response.status_code}")
                return ProviderResponse(
                    provider_name=self.name,
                    model=self.model,
                    content="",
                    latency_ms=getattr(timer, 'elapsed_ms', 0),
                    error=f"HTTP {e.response.status_code}: {e.response.text}"
                )
            except Exception as e:
                logger.error(f"GitHub Copilot error: {e}")
                return ProviderResponse(
                    provider_name=self.name,
                    model=self.model,
                    content="",
                    latency_ms=getattr(timer, 'elapsed_ms', 0),
                    error=str(e)
                )
    
    async def health_check(self) -> bool:
        """Check if GitHub Copilot API is reachable."""
        try:
            # Simple test request
            response = await self._client.get("/")
            return response.status_code < 500
        except Exception as e:
            logger.warning(f"GitHub Copilot health check failed: {e}")
            return False
    
    async def close(self):
        """Close the HTTP client."""
        await self._client.aclose()
