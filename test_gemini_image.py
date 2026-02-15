import os
from google import genai
from google.genai import types
from pathlib import Path
from dotenv import load_dotenv

# Load keys
load_dotenv(".env")
load_dotenv("Projects/AI_Core/.env", override=True)

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("❌ GEMINI_API_KEY not found")
    exit(1)

client = genai.Client(api_key=api_key)

try:
    prompt = "A futuristic city under a dome, high quality, 16:9"
    response = client.models.generate_image(
        model='imagen-3.0-generate-001',
        prompt=prompt
    )
    print(f"✅ Success! Response type: {type(response)}")
    # Save the image if possible
    if hasattr(response, 'generated_images'):
        for i, img in enumerate(response.generated_images):
            img.image.save(f"test_gemini_{i}.png")
            print(f"✅ Image saved: test_gemini_{i}.png")
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents='Generate a prompt for an image of a futuristic laboratory.'
    )
    print(f"Generated prompt: {response.text}")
    print("Note: Direct image generation via gemini-2.0-flash might still be restricted in some regions/tiers.")
except Exception as e:
    print(f"❌ Gemini Image failed: {e}")
