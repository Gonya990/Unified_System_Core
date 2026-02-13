#!/usr/bin/env python3
import argparse
import logging
import sys
from datetime import datetime, timedelta, timezone
from typing import Any

from google.cloud import secretmanager

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Configuration
PROJECT_ID = "my-home-435112"
ROTATION_THRESHOLD_DAYS = 90

# List of expected secrets (could be parsed from manifests, but hardcoding
# critical ones for MVP)
EXPECTED_SECRETS = [
    "ai-core-secrets",
    "bybit-api-key",
    "bybit-api-secret",
    "telegram-bot-token",
    "openai-api-key",
    "gemini-api-key",
    "anthropic-api-key",
    "github-token",
]

# Audit policies (e.g., ensure replication is set to 'user-managed' or 'automatic')
AUDIT_POLICIES = {
    # Check if replication is automatic (standard for high availability)
    "replication_automatic": True,
}

SECRET_ID_PATTERN = r"projects/(?P<project>\d+)/secrets/(?P<secret>[\w\-]+)/versions/(?P<version>\d+)"


def main():
    parser = argparse.ArgumentParser(description="Audit GCP Secret Manager for drift and rotation compliance.")
    parser.add_argument("--project", default=PROJECT_ID, help="GCP Project ID")
    args = parser.parse_args()

    logger.info(f"🔍 Auditing Secrets for project: {args.project}...")

    try:
        client = secretmanager.SecretManagerServiceClient()
    except Exception as e:
        logger.error(f"❌ Failed to initialize SecretManager client: {e}")
        sys.exit(1)

    parent = f"projects/{args.project}"

    # storage for findings
    missing_secrets: list[str] = []
    stale_secrets: list[dict[str, Any]] = []
    orphaned_secrets: list[str] = []
    # drift_secrets = [] # Secrets found but not in expected list (optional check)

    # 1. List all secrets in GCP
    found_secrets: dict[str, Any] = {}
    try:
        for secret in client.list_secrets(request={"parent": parent}):
            secret_name = secret.name.split("/")[-1]
            found_secrets[secret_name] = secret
    except Exception as e:
        logger.error(f"❌ Failed to list secrets: {e}")
        sys.exit(1)

    # 2. Check Expected vs Found
    for expected in EXPECTED_SECRETS:
        if expected not in found_secrets:
            missing_secrets.append(expected)
        else:
            # Check rotation (created time of latest version)
            secret_obj = found_secrets[expected]

            # Check audit policies for the secret itself
            violations: list[str] = []
            replication = secret_obj.replication.automatic or secret_obj.replication.user_managed
            if AUDIT_POLICIES.get("replication_automatic") and "automatic" not in str(replication):
                violations.append(f"Secret {secret_obj.name} does not have automatic replication.")

            if violations:
                logger.warning(f"⚠️ Policy violations for secret {expected}: {', '.join(violations)}")

            try:
                # get latest version
                versions = client.list_secret_versions(request={"parent": secret_obj.name})
                latest_version = None
                for version in versions:
                    if version.state == secretmanager.SecretVersion.State.ENABLED:
                        # logic to find actual latest created
                        if latest_version is None or version.create_time > latest_version.create_time:
                            latest_version = version

                if latest_version:
                    age = datetime.now(timezone.utc) - latest_version.create_time
                    if age > timedelta(days=ROTATION_THRESHOLD_DAYS):
                        stale_secrets.append(
                            {
                                "name": expected,
                                "age_days": age.days,
                                "latest_version": latest_version.name.split("/")[-1],
                            }
                        )
                else:
                    stale_secrets.append(
                        {"name": expected, "age_days": -1, "latest_version": "None (No enabled versions)"}
                    )

            except Exception as e:
                logger.warning(f"⚠️ Could not check version for {expected}: {e}")

    # Identify orphaned secrets (found in GCP but not in EXPECTED_SECRETS)
    for found_secret_name in found_secrets:
        if found_secret_name not in EXPECTED_SECRETS:
            orphaned_secrets.append(found_secret_name)

    # 3. Report
    # report_path = "audit_report.json" # Placeholder for actual report generation
    logger.info("📊 Audit Report:")

    if missing_secrets:
        logger.error("\n❌ MISSING SECRETS (Configuration Drift):")
        for s in missing_secrets:
            print(f"   - {s}")
    else:
        print("\n✅ No missing secrets detected.")

    if stale_secrets:
        print(f"\n⚠️ STALE SECRETS (> {ROTATION_THRESHOLD_DAYS} days):")
        for s in stale_secrets:
            print(f"   - {s['name']}: {s['age_days']} days old (Version: {s['latest_version']})")
            print("     -> Action: Rotate this secret immediately.")
    else:
        print("\n✅ All secrets are valid and rotated.")

    # 4. Summary for CI automation (exit code)
    if missing_secrets or stale_secrets:
        print("\n❌ Audit FAILED.")
        sys.exit(1)

    print("\n✅ Audit PASSED.")
    sys.exit(0)


if __name__ == "__main__":
    main()
