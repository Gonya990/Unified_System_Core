"""
Application-layer encryption for Telegram bot payloads.
Telegram bot API is NOT E2EE — encrypt before send, decrypt on trusted device after YubiKey gate.
"""

from __future__ import annotations

import base64
import os
from typing import Tuple

try:
    from nacl.public import Box, PrivateKey, PublicKey
    from nacl.encoding import Base64Encoder
except ImportError as exc:
    raise ImportError("pip install pynacl") from exc


def generate_keypair() -> Tuple[bytes, bytes]:
    sk = PrivateKey.generate()
    pk = sk.public_key
    return bytes(sk), bytes(pk)


def encrypt_message(plaintext: str, recipient_public_key_b64: str, sender_private_key_b64: str) -> str:
    pk = PublicKey(recipient_public_key_b64.encode(), encoder=Base64Encoder)
    sk = PrivateKey(sender_private_key_b64.encode(), encoder=Base64Encoder)
    box = Box(sk, pk)
    encrypted = box.encrypt(plaintext.encode("utf-8"))
    return base64.b64encode(encrypted).decode("ascii")


def decrypt_message(ciphertext_b64: str, sender_public_key_b64: str, recipient_private_key_b64: str) -> str:
    pk = PublicKey(sender_public_key_b64.encode(), encoder=Base64Encoder)
    sk = PrivateKey(recipient_private_key_b64.encode(), encoder=Base64Encoder)
    box = Box(sk, pk)
    raw = base64.b64decode(ciphertext_b64.encode("ascii"))
    return box.decrypt(raw).decode("utf-8")


def keys_from_env() -> Tuple[str, str]:
    """Load base64 NaCl keys from env (set after PKI onboarding)."""
    pub = os.environ.get("TELEGRAM_E2E_PUBLIC_KEY", "")
    priv = os.environ.get("TELEGRAM_E2E_PRIVATE_KEY", "")
    if not pub or not priv:
        raise ValueError("TELEGRAM_E2E_PUBLIC_KEY and TELEGRAM_E2E_PRIVATE_KEY required")
    return pub, priv
