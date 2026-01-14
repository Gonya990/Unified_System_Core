import os
import logging
from pathlib import Path
from typing import Optional
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa

# Configuration
VAULT_DIR = Path(__file__).parent.parent.parent / "secure_vault"
KEYS_DIR = VAULT_DIR / "keys"
BIOMETRICS_DIR = VAULT_DIR / "biometrics"

logger = logging.getLogger("IdentityManager")


class SecurityError(Exception):
    pass


class IdentityManager:
    def __init__(self):
        self._ensure_setup()
        self.private_key = self._load_private_key()
        self.public_key = self._load_public_key()

    def _ensure_setup(self):
        """Ensures the vault exists and has keys. Generates them if missing."""
        if not KEYS_DIR.exists():
            KEYS_DIR.mkdir(parents=True, exist_ok=True)
            os.chmod(KEYS_DIR, 0o700)  # RESTRICT ACCESS

        priv_path = KEYS_DIR / "private_key.pem"
        pub_path = KEYS_DIR / "public_key.pem"

        if not priv_path.exists():
            logger.warning("🔑 No identity keys found. Generating new Sovereign Identity...")
            self._generate_keys(priv_path, pub_path)

    def _generate_keys(self, priv_path: Path, pub_path: Path):
        """Generates 4096-bit RSA keys."""
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=4096,
        )

        # Save Private Key
        with open(priv_path, "wb") as f:
            f.write(
                private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption(),  # Local vault is physically secured
                )
            )
        os.chmod(priv_path, 0o600)  # Read/Write only by owner

        # Save Public Key
        public_key = private_key.public_key()
        with open(pub_path, "wb") as f:
            f.write(
                public_key.public_bytes(
                    encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo
                )
            )

        logger.info(f"✅ Identity Keys generated at {KEYS_DIR}")

    def _load_private_key(self):
        with open(KEYS_DIR / "private_key.pem", "rb") as f:
            return serialization.load_pem_private_key(f.read(), password=None)

    def _load_public_key(self):
        with open(KEYS_DIR / "public_key.pem", "rb") as f:
            return serialization.load_pem_public_key(f.read())

    def sign_content(self, content_path: str) -> str:
        """Signs a file to prove ownership. Returns the signature hex string."""
        path = Path(content_path)
        if not path.exists():
            raise FileNotFoundError(f"Content not found: {path}")

        # Hash the content
        digest = hashes.Hash(hashes.SHA256())
        with open(path, "rb") as f:
            while chunk := f.read(4096):
                digest.update(chunk)
        data_hash = digest.finalize()

        # Sign the hash
        signature = self.private_key.sign(
            data_hash,
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            prehashed=True,
            algorithm=hashes.SHA256(),
        )

        # Save signature file
        sig_path = path.parent / f"{path.name}.sig"
        with open(sig_path, "wb") as f:
            f.write(signature)

        return signature.hex()

    def get_biometric_path(self, bio_id: str) -> Path:
        """
        Safely resolves a biometric file path.
        Enforces that it stays within BIOMETRICS_DIR.
        """
        target = (BIOMETRICS_DIR / bio_id).resolve()
        if not str(target).startswith(str(BIOMETRICS_DIR.resolve())):
            raise SecurityError(f"🚨 ACCESS DENIED: Attempt to access biometric data outside vault: {target}")

        if not target.exists():
            raise FileNotFoundError(f"Biometric data not found: {bio_id}")

        return target

    def verify_ownership(self, content_path: str, signature_path: str) -> bool:
        """Verifies that the content was signed by THIS identity."""
        # Implementation would mirror signing logic with verify()
        pass


if __name__ == "__main__":
    # Test Run
    logging.basicConfig(level=logging.INFO)
    mgr = IdentityManager()
    print("Identity System Active. Physical Sovereignty Secured.")
