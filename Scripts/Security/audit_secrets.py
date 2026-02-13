#!/usr/bin/env python3
"""
Audit script to detect drift between GCP Secret Manager and Kubernetes manifests.
Checks if secrets referenced in k8s manifests exist and match in Secret Manager.
"""

import os
from pathlib import Path

import yaml
from google.cloud import secretmanager


def get_secret_manager_secrets(project_id):
    """
    Retrieves all secrets from Google Secret Manager for the given project.
    Returns a dictionary mapping secret names to their Secret objects.
    """
    client = secretmanager.SecretManagerServiceClient()
    parent = f"projects/{project_id}"
    secrets = {}
    # Iterate over all secrets
    for secret in client.list_secrets(request={"parent": parent}):
        # The resource name is in the format projects/*/secrets/*
        name = secret.name.split('/')[-1]
        secrets[name] = secret
    return secrets

def parse_k8s_manifests(manifest_dir):
    """
    Parses Kubernetes manifests in the given directory to find secret references.
    Returns a set of secret names referenced in the manifests.
    """
    secrets_used = set()
    manifest_path = Path(manifest_dir)

    if not manifest_path.exists():
        print(f"⚠️ Warning: Manifest directory '{manifest_dir}' does not exist.")
        return secrets_used

    for file_path in manifest_path.rglob('*.yaml'):
        try:
            with open(file_path) as f:
                docs = yaml.safe_load_all(f)
                for doc in docs:
                    if not doc or not isinstance(doc, dict):
                        continue

                    kind = doc.get('kind')
                    if kind not in ['Deployment', 'StatefulSet', 'DaemonSet', 'Job', 'CronJob']:
                        continue

                    # Drill down to the pod spec template
                    spec = doc.get('spec', {})
                    if kind == 'CronJob':
                        spec = spec.get('jobTemplate', {}).get('spec', {})

                    template_spec = spec.get('template', {}).get('spec', {})
                    if not template_spec:
                        continue

                    # Check containers for envFrom (secretRef) and env (valueFrom secretKeyRef)
                    containers = template_spec.get('containers', []) + template_spec.get('initContainers', [])
                    for container in containers:
                        # envFrom
                        for env_from in container.get('envFrom', []):
                            if 'secretRef' in env_from:
                                secret_name = env_from['secretRef'].get('name')
                                if secret_name:
                                    secrets_used.add(secret_name)

                        # env
                        for env in container.get('env', []):
                            value_from = env.get('valueFrom', {})
                            if 'secretKeyRef' in value_from:
                                secret_name = value_from['secretKeyRef'].get('name')
                                if secret_name:
                                    secrets_used.add(secret_name)

                    # Check volumes for secret
                    for volume in template_spec.get('volumes', []):
                        if 'secret' in volume:
                            secret_name = volume['secret'].get('secretName')
                            if secret_name:
                                secrets_used.add(secret_name)

        except Exception as e:
            print(f"⚠️ Error parsing {file_path}: {e}")

    return secrets_used

def main():
    project_id = os.environ.get('GCP_PROJECT_ID')
    if not project_id:
        print("❌ GCP_PROJECT_ID environment variable not set.")
        return 1

    # Assuming manifests are in a standard location relative to this script or root
    # Adjust path as necessary. Using current directory/k8s or similar.
    # The previous code implied parsing k8s manifests, but the path was not clear from the snippet.
    # I'll default to searching from the current working directory's 'k8s' or 'deploy' folder if they exist,
    # or just the current directory recursively if specified.
    # Let's try to infer from typical structure: root/k8s or root/deployment

    root_dir = Path(__file__).resolve().parent.parent.parent
    manifest_dirs = [root_dir / 'k8s', root_dir / 'deployment', root_dir / 'Projects'] # Broad search

    k8s_secrets = set()
    for d in manifest_dirs:
      if d.exists():
          k8s_secrets.update(parse_k8s_manifests(d))

    try:
        sm_secrets = get_secret_manager_secrets(project_id)
    except Exception as e:
        print(f"❌ Failed to list secrets from Secret Manager: {e}")
        return 1

    print(f"📋 Secret Manager secrets count: {len(sm_secrets)}")
    print(f"📋 K8s referenced secrets count: {len(k8s_secrets)}")

    missing_in_sm = k8s_secrets - set(sm_secrets.keys())

    if missing_in_sm:
        print(f"❌ Referenced secrets missing in Secret Manager: {missing_in_sm}")
        return 1

    print("✅ All referenced secrets exist in Secret Manager.")
    return 0

if __name__ == "__main__":
    exit(main())
