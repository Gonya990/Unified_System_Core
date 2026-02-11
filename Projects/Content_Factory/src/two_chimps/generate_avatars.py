import os
import openai
import requests
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent
load_dotenv(ROOT_DIR / '.env')
load_dotenv(ROOT_DIR / 'Projects/AI_Core/.env', override=True)

ASSETS_DIR = Path(__file__).parent / "assets"
if not ASSETS_DIR.exists():
    ASSETS_DIR.mkdir()

PROMPTS = {
    "dino_skeptic": (
        "A hyper-realistic, cinematic portrait of a Tyrannosaurus Rex (T-Rex) wearing a tweed jacket and round glasses. "
        "He looks skeptical, analytical, holding a tiny tea cup (comically). "
        "High detail, 8k resolution, studio lighting, dark academic background."
    ),
    "dino_enthusiast": (
        "A hyper-realistic, cinematic portrait of a Triceratops wearing a colorful hoodie and modern headphones on its horns. "
        "He looks excited, energetic, mouth open as if speaking. "
        "High detail, 8k resolution, neon studio lighting, tech startup background."
    ),
    "dino_studio_background": (
        "A modern, high-tech podcast studio inside a cave with stalactites. "
        "Two large custom chairs, microphones, neon sign saying 'DINO TALK'. "
        "Cinematic lighting, depth of field, 8k resolution."
    )
}

def generate_image(prompt, filename):
    print(f"🎨 Generating {filename}...")
    try:
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        
        image_url = response.data[0].url
        
        # Download image
        img_data = requests.get(image_url).content
        output_path = ASSETS_DIR / f"{filename}.png"
        
        with open(output_path, 'wb') as handler:
            handler.write(img_data)
            
        print(f"✅ Saved: {output_path.name}")
        
    except Exception as e:
        print(f"❌ Error generating {filename}: {e}")

if __name__ == "__main__":
    for name, prompt in PROMPTS.items():
        output_file = ASSETS_DIR / f"{name}.png"
        if not output_file.exists():
            generate_image(prompt, name)
        else:
            print(f"ℹ️ {name}.png already exists.")
