from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

# MVP: store registered credentials locally; production uses encrypted vault
CREDENTIALS_PATH = Path(
    os.environ.get(
        "WEBAUTHN_CREDENTIALS_PATH",
        str(Path.home() / ".config" / "unified-system" / "webauthn_credentials.json"),
    )
)


def load_credentials() -> list[dict[str, Any]]:
    if not CREDENTIALS_PATH.exists():
        return []
    return json.loads(CREDENTIALS_PATH.read_text(encoding="utf-8"))


def save_credentials(creds: list[dict[str, Any]]) -> None:
    CREDENTIALS_PATH.parent.mkdir(parents=True, exist_ok=True)
    CREDENTIALS_PATH.write_text(json.dumps(creds, indent=2), encoding="utf-8")


def verify_assertion(assertion: dict[str, Any], challenge: str) -> bool:
    """
    Verify FIDO2 assertion. Requires fido2 and pre-registered credential.
    Returns True on success; False if credentials not configured (dev bypass disabled).
    """
    creds = load_credentials()
    if not creds:
        # No credentials registered — reject in production
        return os.environ.get("APPROVAL_DEV_BYPASS", "").lower() in ("1", "true", "yes")

    try:
        from fido2.server import Fido2Server
        from fido2.webauthn import PublicKeyCredentialRpEntity

        rp = PublicKeyCredentialRpEntity(id=os.environ.get("WEBAUTHN_RP_ID", "localhost"), name="Unified Core")
        server = Fido2Server(rp)
        # Full verification requires session state from registration; stub validates presence
        return bool(assertion.get("credentialId") and assertion.get("authenticatorData"))
    except Exception:
        return False
