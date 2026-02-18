from huggingface_hub import model_info

token = "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"
repo_id = "black-forest-labs/FLUX.1-schnell"

try:
    info = model_info(repo_id, token=token)
    print(f"✅ Success! Repository {repo_id} is accessible.")
    print(f"🔒 Gated: {getattr(info, 'gated', 'Unknown')}")
except Exception as e:
    print(f"❌ Error accessing {repo_id}: {e}")
    if "gated" in str(e).lower():
        print("💡 Recommendation: Please go to https://huggingface.co/black-forest-labs/FLUX.1-schnell and accept the terms.")
