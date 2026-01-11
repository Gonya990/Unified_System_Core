#!/usr/bin/env python3
"""
Vault Migration Utility for TokenBroker

Migrates existing PBKDF2-encrypted vaults to Argon2id encryption.
Supports --dry-run and --backup options for safe migration.

Usage:
    python migrate_vault.py [--dry-run] [--backup] [--vault-path PATH]
"""

import argparse
import logging
import os
import shutil
import sys
import time
from pathlib import Path

# Add parent directory to path for token_broker import
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import yaml

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("VaultMigration")


def detect_vault_kdf(vault_path: str) -> str:
    """Detect the KDF type used in an existing vault."""
    if not os.path.exists(vault_path):
        return "none"

    try:
        with open(vault_path, "r") as f:
            data = yaml.safe_load(f) or {}

        if "encrypted_data" not in data:
            return "unencrypted"

        return data.get("kdf", "pbkdf2")  # Default to pbkdf2 for old vaults
    except Exception as e:
        logger.error(f"Failed to read vault: {e}")
        return "error"


def migrate_vault(
    vault_path: str = None, dry_run: bool = False, backup: bool = True
) -> bool:
    """
    Migrate a PBKDF2 vault to Argon2id.

    Args:
        vault_path: Path to the vault file (default: ~/.config/unified-system/tokens.yaml)
        dry_run: If True, only report what would be done
        backup: If True, create a backup before migration

    Returns:
        True if migration succeeded, False otherwise
    """
    from token_broker import TokenBroker, HAS_ARGON2, HAS_CRYPTO

    if not HAS_CRYPTO:
        logger.error("cryptography library not available. Cannot migrate.")
        return False

    if not HAS_ARGON2:
        logger.error("argon2-cffi not available. Install with: pip install argon2-cffi")
        return False

    # Use default path if not specified
    if vault_path is None:
        vault_path = os.path.expanduser("~/.config/unified-system/tokens.yaml")

    # Check current KDF type
    current_kdf = detect_vault_kdf(vault_path)
    logger.info(f"Vault path: {vault_path}")
    logger.info(f"Current KDF: {current_kdf}")

    if current_kdf == "none":
        logger.info("No vault found. Nothing to migrate.")
        return True

    if current_kdf == "unencrypted":
        logger.info("Vault is unencrypted. Will encrypt with Argon2id.")
    elif current_kdf == "argon2id":
        logger.info("Vault already uses Argon2id. No migration needed.")
        return True
    elif current_kdf == "error":
        return False

    if dry_run:
        logger.info("[DRY-RUN] Would migrate vault from %s to argon2id", current_kdf)
        return True

    # Create backup if requested
    if backup and os.path.exists(vault_path):
        backup_path = f"{vault_path}.backup.{int(time.time())}"
        shutil.copy2(vault_path, backup_path)
        logger.info(f"Backup created: {backup_path}")

    try:
        # Load vault with current KDF
        broker = TokenBroker(vault_path=vault_path)

        if not broker.key_store:
            logger.warning("Vault is empty. Nothing to migrate.")
            return True

        # Count keys
        total_keys = sum(
            len(pool) for pool in broker.key_store.values() if isinstance(pool, list)
        )
        logger.info(f"Found {total_keys} keys across {len(broker.key_store)} providers")

        # Save with Argon2id
        broker.save_vault(force_kdf="argon2id")
        logger.info("Vault migrated to Argon2id successfully!")

        # Verify migration
        new_kdf = detect_vault_kdf(vault_path)
        if new_kdf == "argon2id":
            logger.info("Migration verified: vault now uses Argon2id")
            return True
        else:
            logger.error(f"Migration verification failed: vault shows KDF={new_kdf}")
            return False

    except Exception as e:
        logger.error(f"Migration failed: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Migrate TokenBroker vault from PBKDF2 to Argon2id"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Only show what would be done, don't actually migrate",
    )
    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Skip creating backup before migration",
    )
    parser.add_argument(
        "--vault-path",
        type=str,
        default=None,
        help="Path to vault file (default: ~/.config/unified-system/tokens.yaml)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Only check current KDF type, don't migrate",
    )

    args = parser.parse_args()

    if args.check:
        vault_path = args.vault_path or os.path.expanduser(
            "~/.config/unified-system/tokens.yaml"
        )
        kdf = detect_vault_kdf(vault_path)
        print(f"Vault: {vault_path}")
        print(f"KDF type: {kdf}")
        return 0 if kdf != "error" else 1

    success = migrate_vault(
        vault_path=args.vault_path,
        dry_run=args.dry_run,
        backup=not args.no_backup,
    )

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
