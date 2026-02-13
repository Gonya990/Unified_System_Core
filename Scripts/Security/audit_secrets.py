#!/usr/bin/env python3
"""
Audit script to detect drift between GCP Secret Manager and Kubernetes manifests.
Checks if secrets referenced in k8s manifests exist and match in Secret Manager.
"""

import os
import re
import yaml
from google.cloud import secretmanager_v1
from pathlib import Path

def get_secret_manager_secrets(project_id):
    client = secretmanager_v1.SecretManagerServiceClient()
    parent = f"projects/{project_id}"
    secrets = {}
    for secret in client.list_secrets(request={"parent": parent}):
        name = secret.name.split('/')[-1]
        secrets[name] = secret
    return secrets

def parse_k8s_manifests(manifest_dir):
    secrets_used = set()
    for file in Path(manifest_dir).rglob('*.yaml'):
        try:
            with open(file, 'r') as f:
                docs = yaml.safe_load_all(f)
                for doc in docs:
                    if doc and doc.get('kind') in ['Deployment                    if doc and doc.get('kind') in ['Deployment                    if doc and doc.get( d                    i                          if doc and doc.get('kind') in ['Deployment                                     for env_from in template_spec.get('envFrom', []):
                            if 'secretRef' in env_f   :
                                secre   used.add(env_from['secretRef']['name'])
                        # Check env secretKeyRef
                        for env in template_spec.get('env', []):
                                                                                       ]:
                                            .a                         etKeyR                                                       ecret
                        for volume in template_spec.get('volumes', []):
                            if 'secret' in volume:
                                secrets_used.add(volume['secret']['secretName'])
                                                                                                                                                                                                                                                                                                                                                    t_                                                   = par                                   
    print(f"📋 Secret Manager secrets: {list(sm_secrets.keys())}")
    print(f"📋 K8s referenced secrets: {list(k8s_secrets)}")
    
    missing_in_sm = k8s_secrets - set(sm_secrets.keys())
    if missing_in_sm:
        print(f"❌ Secrets miss        print(f"❌ Secrets miss        print(f"❌ Secrets miss        print(f"❌ Secrets miss        print(f"❌ Secrets miss         return 0

if __name__ == "__main__":
    exit(main())
