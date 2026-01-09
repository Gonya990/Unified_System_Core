"""
Unified Inference Client for AI Telegram Bot.
Supports Ollama, OpenAI-compatible, Gemini, and custom endpoints.
"""
import json
import logging
from typing import Optional
import aiohttp

try:
    from .config_manager import ConfigManager
except ImportError:
    from config_manager import ConfigManager

logger = logging.getLogger(__name__)

# Lazy import for Gemini
_gemini_client = None
_gemini_client_key = None


def _get_gemini_client(api_key: str):
    """Lazy load and configure Gemini client using new SDK."""
    global _gemini_client, _gemini_client_key
    try:
        from google import genai
        from google.genai.types import GenerateContentConfig
        
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
    """Unified client for multiple LLM backends."""
    
    PROVIDERS = ["ollama", "openai", "gemini", "openrouter", "council"]
    
    def __init__(self, config: ConfigManager):
        self.config = config
        self._session: Optional[aiohttp.ClientSession] = None
        self._session_api_key: str = ""  # Track the API key used for current session
    
    @property
    def provider(self) -> str:
        """Get current inference provider."""
        prov = self.config.get("INFERENCE_PROVIDER", "ollama").lower()
        if prov == "gemini" and not self.config.get("GEMINI_API_KEY"):
            # Fallback to Ollama if Gemini key is missing
            logger.warning("Gemini API key missing, falling back to Ollama")
            return "ollama"
        return prov
    
    @provider.setter
    def provider(self, value: str):
        """Set inference provider."""
        self.config.set("INFERENCE_PROVIDER", value.lower())
    
    @property
    def base_url(self) -> str:
        """Get base URL based on provider."""
        provider = self.provider
        if provider == "openai":
            return self.config.get("OPENAI_BASE_URL", self.config.get("INFERENCE_BASE_URL", "https://api.openai.com"))
        elif provider == "gemini":
            return "https://generativelanguage.googleapis.com"
        elif provider == "openrouter":
            return self.config.get("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
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
        elif provider == "openrouter":
            return self.config.get("OPENROUTER_API_KEY", "")
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
        elif provider == "openrouter":
            return self.config.get("OPENROUTER_MODEL", "anthropic/claude-3.5-sonnet")
        else:  # ollama
            return self.config.get("OLLAMA_MODEL", self.config.get("MODEL_NAME", "llama3.2"))
            
    @model.setter
    def model(self, value: str):
        """Set inference model."""
        self.config.set("MODEL_NAME", value)
    
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
        """
        provider = self.provider
        
        # Council Mode (Parallel Ensemble)
        if provider == "council":
            return await self._chat_council(messages, system_prompt)
        
        # Handle Gemini separately (uses SDK)
        if provider == "gemini":
            return await self._chat_gemini(messages, system_prompt)
        
        # Generic HTTP (Ollama/OpenAI)
        return await self._chat_generic(provider, messages, system_prompt)

    async def _chat_council(self, messages: list[dict], system_prompt: str = "") -> tuple[str, dict]:
        """
        Carpathian Council: Query multiple models in parallel.
        Maximize Logic (Gemini/Cloud) + Reliability (Ollama/Local).
        Strategy: Race them, prefer Gemini if successful and fast.
        """
        import asyncio
        
        # Define tasks
        tasks = []
        providers = []
        
        # 0. OpenRouter Task (Claude - The Supreme Judge)
        if self.config.get("OPENROUTER_API_KEY"):
            tasks.append(self._chat_generic("openrouter", messages, system_prompt))
            providers.append("openrouter")
            
        # 1. Gemini Task (The Brain - Free Tier)
        if self.config.get("GEMINI_API_KEY"):
            tasks.append(self._chat_gemini(messages, system_prompt))
            providers.append("gemini")
            
        # 2. OpenAI Task (The Sage - Paid Tier)
        # We add it to the council if key exists
        if self.config.get("OPENAI_API_KEY"):
            # Use generic handler but with specific provider
            tasks.append(self._chat_generic("openai", messages, system_prompt))
            providers.append("openai")
            
        # 3. Ollama Task (The Soul/Backup - Local)
        tasks.append(self._chat_generic("ollama", messages, system_prompt))
        providers.append("ollama")
        
        if not tasks:
            return "[Error]: No providers available for Council.", {}
            
        logger.info(f"🦾 Council Assembled: {providers}. Thinking...")
        
        # Race/Gather
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        combined_usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
        responses = {}
        
        for i, res in enumerate(results):
            prov = providers[i]
            if isinstance(res, Exception):
                logger.error(f"Council Member {prov} failed: {res}")
                responses[prov] = None
            else:
                text, usage = res
                responses[prov] = text
                for k in combined_usage:
                    combined_usage[k] += usage.get(k, 0)

        # Decision Strategy: Hierarchy of Intelligence
        
        # 0. OpenRouter (Claude 3.5 Sonnet - Supreme Intelligence)
        or_resp = responses.get("openrouter")
        if or_resp and not or_resp.startswith("[Error]"):
            logger.info("👑 Council Decision: Claude (OpenRouter) selected (Supreme Intelligence).")
            return or_resp, combined_usage
        
        # 1. OpenAI (Most capable for logic, if available)
        openai_resp = responses.get("openai")
        if openai_resp and not openai_resp.startswith("[Error]"):
            logger.info("🏆 Council Decision: OpenAI selected (Best Logic).")
            return openai_resp, combined_usage

        # 2. Gemini (Strong logic, free tier)
        gemini_resp = responses.get("gemini")
        if gemini_resp and not gemini_resp.startswith("[Error]"):
            logger.info("🥈 Council Decision: Gemini selected.")
            return gemini_resp, combined_usage
            
        # 3. Ollama (Local backup)
        ollama_resp = responses.get("ollama")
        if ollama_resp:
            logger.info("🛡️ Council Decision: Falling back to Ollama.")
            return ollama_resp, combined_usage
            
        return "[Error]: Council failed to reach a consensus (All models failed).", combined_usage

    async def _chat_generic(self, provider: str, messages: list[dict], system_prompt: str = "") -> tuple[str, dict]:
        """Generic HTTP handler for Ollama/OpenAI."""
        session = await self._get_session()
        
        # Build messages list with system prompt
        full_messages = []
        if system_prompt:
            full_messages.append({"role": "system", "content": system_prompt})
        full_messages.extend(messages)
        
        # Detect endpoint parameters
        if provider == "openai":
            base_url = self.config.get("OPENAI_BASE_URL", "https://api.openai.com")
            url = f"{base_url.rstrip('/')}/v1/chat/completions"
            model = self.config.get("OPENAI_MODEL", "gpt-4o-mini")
            headers = {"Authorization": f"Bearer {self.config.get('OPENAI_API_KEY')}"}
            payload = {
                "model": model,
                "messages": full_messages,
                "temperature": 0.7,
                "max_completion_tokens": 500,
            }
        elif provider == "openrouter":
            base_url = self.config.get("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
            url = f"{base_url.rstrip('/')}/chat/completions"
            model = self.config.get("OPENROUTER_MODEL", "anthropic/claude-3.5-sonnet")
            headers = {
                "Authorization": f"Bearer {self.config.get('OPENROUTER_API_KEY')}",
                "HTTP-Referer": "https://github.com/Gonya990/Unified_System_Core",
                "X-Title": "Unified System Bot"
            }
            payload = {
                "model": model,
                "messages": full_messages,
                "temperature": 0.7,
                "max_tokens": 1000,
            }

        else: # ollama
            # Distributed AI Routing
            # Primary: Linux (Titan RTX) - http://host.docker.internal:11434
            # Secondary: Windows (Igor Gaming) - http://100.127.194.111:11434
            
            default_url = self.config.get("OLLAMA_BASE_URL", "http://host.docker.internal:11434")
            windows_url = "http://100.127.194.111:11434"
            
            model = self.config.get("OLLAMA_MODEL", self.config.get("MODEL_NAME", "llama3.2"))
            
            # Models delegated to Windows (Fast/Light)
            WINDOWS_MODELS = ["mistral", "gemma", "codellama", "qwen:0.5b", "qwen:1.8b"]
            
            if any(m in model.lower() for m in WINDOWS_MODELS):
                base_url = windows_url
                logger.info(f"⚡️ Distributed AI: Routing '{model}' to Windows Node (Igor Gaming)")
            else:
                base_url = default_url
                logger.info(f"🧠 Distributed AI: Routing '{model}' to Primary Linux Node (Titan RTX)")

            url = f"{base_url.rstrip('/')}/api/chat"
            headers = {}
            payload = {
                "model": model,
                "messages": full_messages,
                "stream": False,
            }
        
        usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
        
        try:
            # logger.info(f"[{provider}] Request -> {model}") # Reduced spam
            timeout = aiohttp.ClientTimeout(total=60)
            async with session.post(url, json=payload, headers=headers, timeout=timeout) as response:
                if response.status != 200:
                    error_text = await response.text()
                    logger.error(f"[{provider}] Error {response.status}: {error_text}")
                    return f"[Error {response.status}]: {provider} failed", usage
                
                data = await response.json()
                
                # Parse
                if "choices" in data:
                    text = data["choices"][0]["message"]["content"]
                    if "usage" in data: usage = data["usage"]
                    return text, usage
                elif "message" in data:
                    text = data["message"]["content"]
                    if "prompt_eval_count" in data:
                         usage["prompt_tokens"] = data.get("prompt_eval_count", 0)
                         usage["completion_tokens"] = data.get("eval_count", 0)
                         usage["total_tokens"] = usage["prompt_tokens"] + usage["completion_tokens"]
                    return text, usage
                else:
                    return str(data), usage
                    
        except Exception as e:
            logger.error(f"[{provider}] Exception: {e}")
            return f"[Error]: {str(e)}", usage
    
    async def _chat_gemini(self, messages: list[dict], system_prompt: str = "") -> tuple[str, dict]:
        """Handle Gemini API calls using the SDK."""
        usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
        try:
            # Always fetch key from config, don't rely on self.api_key (which fails in Council mode)
            api_key = self.config.get("GEMINI_API_KEY") or self.config.get("GOOGLE_API_KEY")
            
            if not api_key:
                logger.error("Gemini API key missing in config.")
                return "[Error]: Gemini API key not found. Use /set_key GEMINI_API_KEY <key>", usage
                
            client = _get_gemini_client(api_key)
            if not client:
                return "[Error]: Failed to initialize Gemini client.", usage
            
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
            
            config = GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0.7,
                max_output_tokens=1000
            ) if system_prompt else GenerateContentConfig(temperature=0.7, max_output_tokens=1000)
            
            loop = asyncio.get_event_loop()
            
            def call_gemini():
                try:
                    # Determine model name explicitly
                    model_name = self.config.get("GEMINI_MODEL", "gemini-2.0-flash-exp")
                    return client.models.generate_content(
                        model=model_name,
                        contents=gemini_contents,
                        config=config
                    )
                except Exception as inner_e:
                    logger.error(f"Error inside call_gemini: {inner_e}")
                    raise
            
            try:
                # Add a wrapper for the executor call with a local timeout if needed
                response = await loop.run_in_executor(None, call_gemini)
                
                # Extract usage metadata if available
                if hasattr(response, "usage_metadata") and response.usage_metadata:
                    usage["prompt_tokens"] = response.usage_metadata.prompt_token_count
                    usage["completion_tokens"] = response.usage_metadata.candidates_token_count
                    usage["total_tokens"] = response.usage_metadata.total_token_count
                    
                if not response.text:
                    logger.warning("Gemini returned empty text")
                    return "[Error]: Gemini вернул пустой ответ", usage
                    
                return response.text, usage
            except asyncio.TimeoutError:
                logger.error("Gemini request timed out in executor")
                return "[Error]: Превышено время ожидания ответа от Gemini", usage
            
        except Exception as e:
            logger.exception(f"Gemini error: {e}")
            return f"[Gemini Error]: {str(e)}", usage
            
    async def transcribe_audio(self, file_path: str) -> str:
        """Transcribe audio file using OpenAI Whisper API."""
        # Use OpenAI Key (either specific or generic)
        api_key = self.config.get("OPENAI_API_KEY", self.config.get("INFERENCE_API_KEY"))
        if not api_key:
            return "[Error]: No OpenAI API key found for transcription."
            
        url = "https://api.openai.com/v1/audio/transcriptions"
        headers = {"Authorization": f"Bearer {api_key}"}
        
        try:
            data = aiohttp.FormData()
            data.add_field("model", "whisper-1")
            data.add_field("file", open(file_path, "rb"))
            
            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.post(url, data=data) as response:
                    if response.status != 200:
                        text = await response.text()
                        logger.error(f"Whisper error: {text}")
                        return f"[Error {response.status}]: Transcription failed"
                        
                    result = await response.json()
                    return result.get("text", "")
                    
        except Exception as e:
            logger.error(f"Transcription failed: {e}")
            return f"[Error]: {str(e)}"

    async def generate_speech(self, text: str, voice: str = "alloy") -> Optional[bytes]:
        """Generate speech from text using OpenAI TTS."""
        api_key = self.config.get("OPENAI_API_KEY", self.config.get("INFERENCE_API_KEY"))
        if not api_key:
            logger.error("No OpenAI API key found for TTS.")
            return None
            
        url = "https://api.openai.com/v1/audio/speech"
        headers = {"Authorization": f"Bearer {api_key}"}
        payload = {
            "model": "tts-1",
            "input": text,
            "voice": voice
        }
        
        try:
            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.post(url, json=payload) as response:
                    if response.status == 200:
                        return await response.read()
                    else:
                        error_text = await response.text()
                        logger.error(f"TTS Error {response.status}: {error_text}")
                        return None
        except Exception as e:
            logger.error(f"TTS Failed: {e}")
            return None
            
    async def generate_image(self, prompt: str, size: str = "1024x1024", quality: str = "standard") -> Optional[str]:
        """
        Generate image using OpenAI DALL-E 3.
        Returns URL of generated image or None on failure.
        """
        api_key = self.config.get("OPENAI_API_KEY")
        if not api_key:
            logger.error("No OpenAI API key found for image generation.")
            return None

        url = "https://api.openai.com/v1/images/generations"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "dall-e-3",
            "prompt": prompt,
            "n": 1,
            "size": size,
            "quality": quality
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload, headers=headers, timeout=aiohttp.ClientTimeout(total=120)) as response:
                    if response.status == 200:
                        data = await response.json()
                        image_url = data.get("data", [{}])[0].get("url")
                        logger.info(f"Image generated successfully: {image_url[:50]}...")
                        return image_url
                    else:
                        error_text = await response.text()
                        logger.error(f"DALL-E Error {response.status}: {error_text}")
                        return None
        except Exception as e:
            logger.error(f"Image generation failed: {e}")
            return None

    async def analyze_image(self, image_path: str, prompt: str = "Describe this image") -> str:
        """Analyze image using Gemini Vision."""
        if self.provider != "gemini":
            return "❌ Image analysis is currently only supported with Gemini provider."
            
        try:
            from PIL import Image
            img = Image.open(image_path)
            
            client = await self._get_gemini_client()
            response = client.models.generate_content(
                model=self.model,
                contents=[prompt, img]
            )
            return response.text
        except Exception as e:
            logger.error(f"Image analysis failed: {e}")
            return f"❌ Vision Error: {str(e)}"

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
            try:
                # Use the client to fetch actual available models
                client = _get_gemini_client(self.api_key)
                if client:
                    # Sync call in async context (should be wrapped, but fast enough for now)
                    all_models = list(client.models.list())
                    
                    # Filter for generateContent support and clean names
                    valid_models = []
                    for m in all_models:
                        if "generateContent" in (m.supported_generation_methods or []):
                            # Name is usually 'models/gemini-1.5-flash'
                            # We strip 'models/' prefix for user convenience
                            name = m.name.split("/")[-1]
                            valid_models.append(name)
                    
                    if valid_models:
                        return sorted(valid_models, reverse=True)
            except Exception as e:
                logger.error(f"Failed to list Gemini models dynamically: {e}")
            
            # Fallback if dynamic fails
            return [
                "gemini-2.0-flash-exp",
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
