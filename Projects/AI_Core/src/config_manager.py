"""
Configuration Manager for AI Telegram Bot.
Handles persistent storage with encryption for sensitive values.
"""

import base64
import json
import os
from pathlib import Path
from typing import Optional

# Load .env file automatically or from specified path
from dotenv import load_dotenv

env_file = os.environ.get("ENV_FILE", ".env")
load_dotenv(env_file)

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class ConfigManager:
    """Manages bot configuration with persistence and encryption."""

    CONFIG_FILE = Path(os.environ.get("CONFIG_PATH", "config/bot_config.json"))
    SENSITIVE_KEYS = {
        "INFERENCE_API_KEY",
        "TELEGRAM_BOT_TOKEN",
        "GEMINI_API_KEY",
        "OPENAI_API_KEY",
        "OPENROUTER_API_KEY",
    }

    def __init__(self):
        self._config: dict = {}
        self._fernet: Optional[Fernet] = None
        self._init_encryption()
        self._load_config()

    def _init_encryption(self) -> None:
        """Initialize Fernet encryption using a derived key."""
        # Use TELEGRAM_BOT_TOKEN as salt for key derivation (always available)
        salt = os.environ.get("TELEGRAM_BOT_TOKEN", "default-salt")[:16].encode()
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(b"ai-telegram-bot-key"))
        self._fernet = Fernet(key)

    def _load_config(self) -> None:
        """Load configuration from file or environment."""
        # Start with environment variables - load ALL provider configurations
        self._config = {
            "TELEGRAM_BOT_TOKEN": os.environ.get("TELEGRAM_BOT_TOKEN", ""),
            # Provider selection
            "INFERENCE_PROVIDER": os.environ.get("INFERENCE_PROVIDER", "gemini"),
            # Ollama settings
            "OLLAMA_BASE_URL": os.environ.get(
                "OLLAMA_BASE_URL", "http://localhost:11434"
            ),
            "OLLAMA_MODEL": os.environ.get("OLLAMA_MODEL", "llama3.2"),
            # OpenAI settings
            "OPENAI_BASE_URL": os.environ.get(
                "OPENAI_BASE_URL", "https://api.openai.com"
            ),
            "OPENAI_API_KEY": os.environ.get("OPENAI_API_KEY", ""),
            "OPENAI_MODEL": os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
            # Gemini settings
            "GEMINI_API_KEY": os.environ.get(
                "GEMINI_API_KEY", os.environ.get("GOOGLE_API_KEY", "")
            ),
            "GEMINI_MODEL": os.environ.get("GEMINI_MODEL", "gemini-2.0-flash-exp"),
            # OpenRouter settings
            "OPENROUTER_API_KEY": os.environ.get("OPENROUTER_API_KEY", ""),
            "OPENROUTER_BASE_URL": os.environ.get(
                "OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"
            ),
            "OPENROUTER_MODEL": os.environ.get(
                "OPENROUTER_MODEL", "anthropic/claude-3.5-sonnet"
            ),
            # Legacy settings (backwards compatibility)
            "INFERENCE_BASE_URL": os.environ.get(
                "INFERENCE_BASE_URL", "http://localhost:11434"
            ),
            "INFERENCE_API_KEY": os.environ.get("INFERENCE_API_KEY", ""),
            "MODEL_NAME": os.environ.get("MODEL_NAME", "llama3.2"),
            "LOG_LEVEL": os.environ.get("LOG_LEVEL", "INFO"),
            # User management
            "ALLOWED_USERS": os.environ.get("ALLOWED_USERS", ""),
        }

        # Override with persisted config if exists
        if self.CONFIG_FILE.exists():
            try:
                with open(self.CONFIG_FILE) as f:
                    stored = json.load(f)
                    for key, value in stored.items():
                        # Skip empty values to preserve Environment Variables precedence if config is broken
                        if not value:
                            continue

                        if key in self.SENSITIVE_KEYS:
                            # Decrypt sensitive values
                            if self._fernet:
                                try:
                                    value = self._fernet.decrypt(
                                        value.encode()
                                    ).decode()
                                except Exception:
                                    pass  # Use as-is if decryption fails

                        # Update config only if we have a valid value
                        if value:
                            self._config[key] = value
            except Exception:
                pass  # Use defaults if file is corrupted

    def _save_config(self) -> None:
        """Persist configuration to file."""
        self.CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)

        to_save = {}
        for key, value in self._config.items():
            if key in self.SENSITIVE_KEYS and value and self._fernet:
                # Encrypt sensitive values
                value = self._fernet.encrypt(value.encode()).decode()
            to_save[key] = value

        with open(self.CONFIG_FILE, "w") as f:
            json.dump(to_save, f, indent=2)

    def get(self, key: str, default: str = "") -> str:
        """Get a configuration value."""
        return self._config.get(key, default)

    def set(self, key: str, value: str) -> None:
        """Set a configuration value and persist it."""
        self._config[key] = value
        self._save_config()

    def get_status(self) -> dict:
        """Get current configuration status (safe for display)."""
        provider = self._config.get("INFERENCE_PROVIDER", "ollama").lower()

        # Check API key based on current provider
        if provider == "gemini":
            api_key_set = bool(self._config.get("GEMINI_API_KEY"))
        elif provider == "openai":
            api_key_set = bool(self._config.get("OPENAI_API_KEY"))
        elif provider == "openrouter":
            api_key_set = bool(self._config.get("OPENROUTER_API_KEY"))
        else:  # ollama
            api_key_set = bool(self._config.get("INFERENCE_API_KEY"))

        return {
            "inference_url": self._config.get("INFERENCE_BASE_URL", "not set"),
            "model": self._config.get("MODEL_NAME", "not set"),
            "api_key_set": api_key_set,
        }
