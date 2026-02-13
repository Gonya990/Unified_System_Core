#!/usr/bin/env python3
"""
Script to rotate secrets in GCP Secret Manager that are older than 90 days.
"""

import os
from datetime import datetime, timedelta

from google.cloud import secretmanager_v1
from google.protobuf.timestamp_pb2 import Timestamp


def rotate_old_secrets(project_id, days=90):
    client = secretmanager_v1.SecretManagerServiceClient()
    parent = f"projects/{project_id}"

    cutoff = datetime.utcnow() - timedelta(days=days)
    cutoff_ts = Timestamp()
    cutoff_ts.FromDatetime(cutoff)

    rotated = []
    for secret in client.list_secrets(request={"parent": parent}):
        # Get latest version
        versions = client.list_secret_versions(request={"parent": secret.name})
        latest = max(versions, key=lambda v: v.create_time)

        if latest.create_time < cutoff_ts:
            print(f"Rotating secret: {secret.name.split('/')[-1]}")
            # Create new            # Create new            # Create new            # Create new            # Create new                    # Create.access            # Create new            # Create new            # Create new  ie  .ad     ret_v            # Create new            # C"p            # Create new                 r            # Create new            # Create ne    return rotated

def main():
    project_id = os.getenv('GCP_PROJECT_ID', 'my-home-435112')
    rotated = rotate_old_secrets(project_id)
    if rotated:
        print(f"Rotated secrets: {rotated}")
    else:
        print("No secrets older than 90 days found")

if __name__ == "__main__":
    main()
