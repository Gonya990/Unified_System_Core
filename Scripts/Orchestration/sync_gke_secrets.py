import base64
import os
import subprocess
import sys

# Add src to path for TokenBroker
sys.path.insert(0, "/Users/igorgoncharenko/Documents/Unified_System_Core/Projects/AI_Core/src")

from token_broker import TokenBroker


def sync_secrets():
    broker = TokenBroker()
    bybit_data = broker.key_store.get("bybit", [{}])[0]
    api_key = bybit_data.get("key")
    api_secret = bybit_data.get("secret")

    github_data = broker.key_store.get("github", [{}])[0]
    github_token = github_data.get("key")

    if not api_key:
        print("❌ No keys to sync.")
        return

    # Create YAML for secret
    secret_yaml = f"""
apiVersion: v1
kind: Secret
metadata:
  name: bybit-secrets
  namespace: trading
type: Opaque
data:
  api-key: {base64.b64encode(api_key.encode()).decode()}
  api-secret: {base64.b64encode(api_secret.encode()).decode()}
  github-token: {base64.b64encode(github_token.encode()).decode() if github_token else ""}
"""
    with open("temp_secret.yaml", "w") as f:
        f.write(secret_yaml)

    print("🚀 Applying secret to GKE...")
    res = subprocess.run(["kubectl", "apply", "-f", "temp_secret.yaml"], capture_output=True, text=True)
    if res.returncode == 0:
        print("✅ Secret updated successfully.")
        print("♻️ Restarting trading deployment...")
        subprocess.run(["kubectl", "rollout", "restart", "deployment/bybit-ai-alpha-agent", "-n", "trading"])
    else:
        print(f"❌ Error: {res.stderr}")

    os.remove("temp_secret.yaml")

if __name__ == "__main__":
    sync_secrets()
