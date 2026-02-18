import os
from huggingface_hub import InferenceClient
from pathlib import Path
from dotenv import load_dotenv

load_dotenv("/Users/igorgoncharenko/Documents/Unified_System_Core/Projects/AI_Core/.env")

# Try to get HF_TOKEN from env or TokenBroker
token = os.getenv("HF_TOKEN")
if not token:
    print("⚠️ HF_TOKEN not found in .env. Checking TokenBroker...")
    # Add AI_Core to path
    import sys
    sys.path.append("/Users/igorgoncharenko/Documents/Unified_System_Core/Projects/AI_Core/src")
    from token_broker import TokenBroker
    broker = TokenBroker()
    token = broker.get_key("huggingface")

if not token:
    print("❌ No HF_TOKEN found!")
    exit(1)

client = InferenceClient(api_key=token)
prompt = "A futuristic city in the style of solar punk, cinematic lighting, vertical 9:16"

print(f"Testing HF Inference with token: {token[:8]}...")
try:
    image = client.text_to_image(prompt, model="black-forest-labs/FLUX.1-schnell")
    image.save("hf_test_image.jpg")
    print("✅ Successfully generated image: hf_test_image.jpg")
except Exception as e:
    print(f"❌ HF Inference failed: {e}")
