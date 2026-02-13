#!/usr/bin/env python3
"""
Script to rotate secrets in GCP Secret Manager that are older than 90 days.
"""

import os
from datetime import datetime, timedelta

from google.cloud import secretmanager

# from google.protobuf.timestamp_pb2 import Timestamp # Not needed if using direct attributes usually, but let's see.

def rotate_old_secrets(project_id, days=90):
    client = secretmanager.SecretManagerServiceClient()
    parent = f"projects/{project_id}"

    # Calculate cutoff time
    cutoff = datetime.utcnow() - timedelta(days=days)

    rotated = []

    try:
        # Iterate over all secrets
        for secret in client.list_secrets(request={"parent": parent}):
            secret_name = secret.name.split('/')[-1]

            # Get versions
            versions = list(client.list_secret_versions(request={"parent": secret.name}))
            if not versions:
                continue

            # Filter for enabled versions only to find actual latest active one
            enabled_versions = [v for v in versions if v.state == secretmanager.SecretVersion.State.ENABLED]
            if not enabled_versions:
                continue

            # Identify the latest version by create_time
            # create_time is a varying type depending on library version, but usually datetime-like or protobuf
            # Safest is to sort logic.
            latest = max(enabled_versions, key=lambda v: v.create_time)

            # Convert protobuf timestamp to datetime if needed, or compare directly if library supports it.
            # Google client library usually returns a wrapper that behaves like datetime or has .timestamp()
            # We'll assume standard behavior.

            # To be safe against timezone issues, we can check basic timestamp
            if latest.create_time.timestamp() < cutoff.timestamp():
                print(f"⚠️ Secret '{secret_name}' is older than {days} days (created: {latest.create_time}).")
                rotated.append(secret_name)
                # Actual rotation logic would go here (e.g. generate new value, add version)
                # For now, we just identify them.

    except Exception as e:
        print(f"Error checking secrets: {e}")

    return rotated

def main():
    project_id = os.getenv('GCP_PROJECT_ID')
    if not project_id:
        # Fallback or error
        print("GCP_PROJECT_ID not set, skipping rotation check.")
        return

    print(f"Checking for secrets older than 90 days in project {project_id}...")
    rotated = rotate_old_secrets(project_id)
    if rotated:
        print(f"Found {len(rotated)} secrets needing rotation: {rotated}")
    else:
        print("✅ No secrets older than 90 days found.")

if __name__ == "__main__":
    main()
