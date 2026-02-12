import subprocess
from pathlib import Path

VAULT_PATH = Path("~/.config/unified-system/tokens.yaml").expanduser()
NAMESPACE = "trading"
SECRET_NAME = "vibranium-tokens"


def sync_tokens():
    if not VAULT_PATH.exists():
        print(f"❌ Vault not found at {VAULT_PATH}")
        return

    print(f"🚀 Syncing Vibranium Vault to GKE ({NAMESPACE}/{SECRET_NAME})...")

    # Create secret via kubectl
    # We use --from-file to handle binary data if necessary, though it's YAML
    cmd = [
        "kubectl",
        "create",
        "secret",
        "generic",
        SECRET_NAME,
        f"--from-file=tokens.yaml={VAULT_PATH}",
        "-n",
        NAMESPACE,
        "--dry-run=client",
        "-o",
        "yaml",
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Failed to generate secret YAML: {result.stderr}")
        return

    # Apply to cluster
    apply_cmd = ["kubectl", "apply", "-f", "-"]
    apply_result = subprocess.run(
        apply_cmd, input=result.stdout, capture_output=True, text=True
    )

    if apply_result.returncode == 0:
        print(
            f"✅ Vault synced successfully to '{SECRET_NAME}' "
            f"in namespace '{NAMESPACE}'."
        )
    else:
        print(f"❌ Sync failed: {apply_result.stderr}")


if __name__ == "__main__":
    sync_tokens()
