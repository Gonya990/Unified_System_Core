

ENV_FILE = "/home/gonya/Unified_System_Core/Projects/AI_Core/.env"

def patch_env():
    # Read existing env
    try:
        with open(ENV_FILE) as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error reading .env: {e}")
        return

    new_lines = []
    # Keys to update/add
    updates = {
        "OLLAMA_BASE_URL": "http://host.docker.internal:11434",
        "INFERENCE_BASE_URL": "http://host.docker.internal:11434",
        "HA_URL": "http://100.118.179.47:8123" # Tailscale IP
    }

    updated_keys = set()

    for line in lines:
        if line.strip() and not line.startswith("#"):
            key = line.split("=")[0].strip()
            if key in updates:
                new_lines.append(f"{key}={updates[key]}\n")
                updated_keys.add(key)
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)

    # Add missing keys
    for k, v in updates.items():
        if k not in updated_keys:
            new_lines.append(f"\n{k}={v}\n")

    with open(ENV_FILE, "w") as f:
        f.writelines(new_lines)

    print("✅ .env patched successfully!")

if __name__ == "__main__":
    patch_env()
