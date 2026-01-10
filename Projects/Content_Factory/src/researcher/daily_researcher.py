#!/usr/bin/env python3
import os
import sys
import feedparser
import json
import requests
import random
import re
import time
from bs4 import BeautifulSoup
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

# Setup paths
SRC_DIR = Path(__file__).parent.parent.resolve()
FACTORY_DIR = SRC_DIR.parent
ROOT_DIR = FACTORY_DIR.parent # Unified_System

# Add all source subdirectories to path
for d in ["researcher", "pipeline", "assets", "video", "uploaders"]:
    sys.path.append(str(SRC_DIR / d))

load_dotenv(ROOT_DIR / ".env")
load_dotenv(ROOT_DIR / "Projects/AI_Core/.env", override=True)

# Import TokenBroker
try:
    from Scripts.Utilities.token_broker import TokenBroker
    BROKER = TokenBroker()
    print("✅ TokenBroker imported successfully")
except ImportError:
    print("⚠️ TokenBroker not found, falling back to ENV")
    BROKER = None

# Configuration
def get_key(provider, owner=None):
    if BROKER:
        k = BROKER.get_key(provider, owner)
        if k: return k
    
    # Fallback
    if provider == "openai": return os.getenv("OPENAI_API_KEY")
    if provider == "gemini": return os.getenv("GEMINI_API_KEY")
    if provider == "pexels": return os.getenv("PEXELS_API_KEY")
    return None

PEXELS_API_KEY = get_key("pexels") or "5KikfJFyT75Rlibf2u829q4qZOTm0FVfttKCb5znbJSYqb96qAKarEDY"

def get_client():
    """Lazy initialization of OpenAI client with TokenBroker"""
    api_key = get_key("openai")
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    org_id = os.getenv("OPENAI_ORG_ID")
    return OpenAI(api_key=api_key, base_url=base_url, organization=org_id)

def get_latest_tech_news():
    """Fetches news from Google News RSS"""
    topics = [
        "artificial intelligence future tech", "quantum computing breakthroughs 2026",
        "neuralink brain computer interface", "humanoid robots boston dynamics",
        "biotechnology longevity research", "autonomous vehicles level 5",
        "nanotechnology in medicine", "6G network release", "smart cities"
    ]
    query = random.choice(topics)
    print(f"📡 Researching topic: {query}")
    import urllib.parse
    encoded_query = urllib.parse.quote(query)
    url = f"https://news.google.com/rss/search?q={encoded_query}+when:1d&hl=en-US&gl=US&ceid=US:en"
    try:
        feed = feedparser.parse(url)
        items = [{"title": entry.title, "link": entry.link} for entry in feed.entries[:5]]
        print(f"✅ Found {len(items)} news items.")
        return items
    except Exception as e:
        print(f"❌ News fetch failed: {e}")
        return []

def get_page_content(url):
    """Extracts text from a web page"""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        for s in soup(["script", "style"]): s.decompose()
        return " ".join(soup.get_text(separator=' ').split())[:3000]
    except Exception as e:
        print(f"⚠️ Failed to browse {url}: {e}")
        return ""

def run_daily_research(style="impact"):
    """Deep research with failover between OpenAI and Gemini"""
    print(f"🧠 Starting DEEP RESEARCH (Style: {style.upper()}) [Strategy: Multi-Model]")
    news = get_latest_tech_news()
    if not news: return None
        
    context = ""
    for item in news[:2]:
        print(f"🔍 Browsing: {item['title']}...")
        context += f"TOPIC: {item['title']}\nCONTENT: {get_page_content(item['link'])}\n\n"

    style_prompt = f"""
    Tone: {'Enthusiastic, Pixar-like, fun' if style == 'cartoon' else 'Epic, deep, motivational'}.
    Language: RUSSIAN. Length: 15 scenes.
    Keywords: {'3d render, cartoon style, cute, colorful, animation' if style == 'cartoon' else 'cinematic 4k, futuristic, high quality'}.
    """
    
    prompt = f"""
    Context: {context}
    Task: Viral RUSSIAN script for 15 scenes + 15 keywords.
    Target Audience: Tech enthusiasts, futurists, AI early adopters.
    
    {style_prompt}
    
    CRITICAL RESTRICTIONS:
    1. NO ANIMALS. NO MICE. NO FAIRY TALES. NO "ONCE UPON A TIME".
    2. STRICTLY FUTURISTIC / TECH / AI themes.
    3. If news/context is weak, invent a realistic near-future AI scenario (e.g., "AI cures disease", "Robots build Mars base", "Neuralink update").
    4. Tone must be grounded in sci-fi reality, not fantasy.
    5. No scene labels. No "Scene 1:". ONLY spoken words. Use "..." for pauses.

    Format: JSON {{"selected_topic": "", "description": "", "script_ru": "", "scenes": [{{"image": "scene_1", "keyword": ""}}]}}
    """
    
    data = None
    # Strategy 1: OpenAI
    try:
        print("🤖 Attempting Research via OpenAI (GPT-4o)...")
        res = get_client().chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": "Return ONLY JSON."}, {"role": "user", "content": prompt}]
        )
        content = res.choices[0].message.content
        if "```json" in content: content = content.split("```json")[1].split("```")[0].strip()
        data = json.loads(content)
    except Exception as e:
        print(f"⚠️ OpenAI Research failed: {e}. Falling back to Gemini...")
        
    # Strategy 2: Gemini Fallback
    if not data:
        try:
            print("🌠 Attempting Research via Gemini 2.0...")
            import google.generativeai as genai
            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
            model = genai.GenerativeModel("models/gemini-2.0-flash")
            res = model.generate_content(prompt)
            content = res.text
            if "```json" in content: content = content.split("```json")[1].split("```")[0].strip()
            data = json.loads(content)
        except Exception as e:
            print(f"⚠️ Gemini Research failed: {e}. Falling back to Ollama (Rock Solid)...")
            
    # Strategy 3: Ollama (Rock Solid Local Fallback)
    if not data:
        try:
            print("🦙 Attempting Research via Ollama (llama3)...")
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "llama3",
                    "prompt": f"{prompt}\nReturn ONLY JSON.",
                    "stream": False,
                    "format": "json"
                },
                timeout=60
            )
            data = response.json().get('response')
            if isinstance(data, str): data = json.loads(data)
            print("✅ Ollama Research successful!")
        except Exception as e:
            print(f"❌ All Research models failed (including Ollama): {e}")
            return None

    # Strict Scene Label Cleanup
    script = data.get('script_ru', '')
    script = re.sub(r'(?i)(сцена|scene|кадр|shot|narrator|диктор|voiceover)\s*\d*[:.-]*\s*', '', script)
    data['script_ru'] = script.strip()
    return data

def generate_gemini_images(scenes, output_dir: Path):
    """💎 Gemini 2.0 Flash Image - DISABLED (API not available yet)"""
    print(f"⚠️ Gemini Image Generation not available (experimental API)")
    return []  # Skip for now, will be enabled when API is stable

def generate_flux_images(scenes, output_dir: Path):
    """⚡ Flux.1 Schnell - FREE Local (Fast & Quality)"""
    print(f"⚡ Checking Flux.1 Schnell server...")
    resolved = []
    try:
        import requests
        flux_url = "http://localhost:8080/generate"
        
        # Quick health check (1 second timeout)
        try:
            requests.get("http://localhost:8080/", timeout=1)
        except:
            print(f"❌ Flux server not running (install in progress)")
            return []
        
        print(f"✅ Flux server online! Generating {len(scenes)} scenes...")
        for s in scenes:
            time.sleep(0.5)
            try:
                prompt = f"cartoon style, 3d animation, pixar quality, vibrant colors, vertical 9:16 format, {s['keyword']}"
                response = requests.post(flux_url, json={
                    "prompt": prompt,
                    "width": 1080,
                    "height": 1920,
                    "num_steps": 4,
                    "guidance": 3.5
                }, timeout=30)
                
                if response.status_code == 200:
                    path = output_dir / f"{s['image']}.jpg"
                    with open(path, "wb") as f:
                        f.write(response.content)
                    s["resolved_path"] = str(path)
                    resolved.append(s)
                    print(f"   ✅ Flux: {s['image']}")
            except Exception as e:
                print(f"   ⚠️ Flux failed for {s['image']}: {e}")
                break  # Stop trying if one fails
    except Exception as e:
        print(f"❌ Flux error: {e}")
    return resolved

def generate_sdxl_images(scenes, output_dir: Path):
    """🎨 Stable Diffusion XL - FREE Local (Backup)"""
    print(f"🎨 Checking SDXL server...")
    resolved = []
    try:
        import requests
        sdxl_url = "http://localhost:8188/generate"
        
        # Quick health check (1 second timeout)
        try:
            requests.get("http://localhost:8188/", timeout=1)
        except:
            print(f"❌ SDXL server not running (install in progress)")
            return []
        
        print(f"✅ SDXL server online! Generating {len(scenes)} scenes...")
        for s in scenes:
            time.sleep(1.0)
            try:
                prompt = f"cartoon illustration, pixar style, 3d render, colorful, vibrant, vertical composition, {s['keyword']}"
                response = requests.post(sdxl_url, json={
                    "prompt": prompt,
                    "negative_prompt": "ugly, blurry, low quality, distorted",
                    "width": 1080,
                    "height": 1920,
                    "steps": 25
                }, timeout=60)
                
                if response.status_code == 200:
                    path = output_dir / f"{s['image']}.jpg"
                    with open(path, "wb") as f:
                        f.write(response.content)
                    s["resolved_path"] = str(path)
                    resolved.append(s)
                    print(f"   ✅ SDXL: {s['image']}")
            except Exception as e:
                print(f"   ⚠️ SDXL failed for {s['image']}: {e}")
                break  # Stop trying if one fails
    except Exception as e:
        print(f"❌ SDXL error: {e}")
    return resolved

def generate_dalle_assets(scenes, output_dir: Path):
    """DALL-E 3 Image generation (PAID FALLBACK)"""
    time.sleep(1.2) # Vibranium Pause
    print(f"💰 Trying DALL-E 3 for {len(scenes)} scenes (PAID)...")
    resolved = []
    client = get_client()
    for s in scenes:
        time.sleep(2.0) # User requested tactical pause
        try:
            prompt = f"3D animation style, Pixar inspired, high quality, vibrant colors, VERTICAL 9:16, {s['keyword']}"
            res = client.images.generate(model="dall-e-3", prompt=prompt, size="1024x1792", n=1)
            img_data = requests.get(res.data[0].url).content
            path = output_dir / f"{s['image']}.jpg"
            with open(path, "wb") as f: f.write(img_data)
            s["resolved_path"] = str(path)
            resolved.append(s)
            print(f"   ✅ DALL-E: {s['image']}")
        except Exception as e: print(f"   ⚠️ DALL-E failed: {e}")
    return resolved

def generate_banana_assets(scenes, output_dir: Path):
    """Banana.dev Image generation"""
    api_key = os.getenv("BANANA_API_KEY")
    if not api_key: return []
    print(f"🍌 Trying Banana.dev for {len(scenes)} scenes...")
    import banana_dev as banana
    resolved = []
    model_key = os.getenv("BANANA_MODEL_KEY", "stable-diffusion-xl")
    for s in scenes:
        time.sleep(2.0) # Tactical pause
        try:
            inputs = {"prompt": f"Cartoon style, 3d animation, vibrant, vertical, {s['keyword']}"}
            res = banana.run(api_key, model_key, inputs)
            img_b64 = res["modelOutputs"][0]["image_base64"]
            path = output_dir / f"{s['image']}.jpg"
            import base64
            with open(path, "wb") as f: f.write(base64.b64decode(img_b64))
            s["resolved_path"] = str(path)
            resolved.append(s)
            print(f"   ✅ Banana: {s['image']}")
        except Exception as e: print(f"   ⚠️ Banana failed: {e}")
    return resolved

def generate_pexels_assets(scenes, output_dir: Path, style="impact"):
    """Pexels search with style-augmented keywords"""
    print(f"🎬 Trying Pexels ({style}) for {len(scenes)} scenes...")
    resolved = []
    for s in scenes:
        time.sleep(1.0) # Tactical pause
        try:
            kw = s['keyword']
            if style == "cartoon": kw = f"cartoon illustration animation {kw}"
            url = f"https://api.pexels.com/v1/search?query={kw}&per_page=1&orientation=portrait"
            res = requests.get(url, headers={"Authorization": PEXELS_API_KEY}).json()
            if res.get("photos"):
                img_data = requests.get(res["photos"][0]["src"]["large2x"]).content
                path = output_dir / f"{s['image']}.jpg"
                with open(path, "wb") as f: f.write(img_data)
                s["resolved_path"] = str(path)
                resolved.append(s)
                print(f"   ✅ Pexels: {s['image']}")
        except Exception as e: print(f"   ⚠️ Pexels failed: {e}")
    return resolved

def generate_vision_assets(scenes, output_dir: Path, style="impact"):
    """💎 VIBRANIUM TRIPLE-THREAT: Free-First Failover Chain"""
    if style != "cartoon":
        return generate_pexels_assets(scenes, output_dir, style="impact")

    print("🚀 VIBRANIUM TRIPLE-THREAT PIPELINE: Free → Paid Failover")
    print("   Priority: Gemini 2.0 → Flux.1 → SDXL → DALL-E → Banana → Pexels")
    
    # FREE TIER 1: Gemini 2.0 Flash Image (Best Quality, Free)
    resolved = generate_gemini_images(scenes, output_dir)
    if len(resolved) == len(scenes): 
        print("✅ All images generated via Gemini 2.0 (FREE)")
        return resolved
    
    # FREE TIER 2: Flux.1 Schnell (Fast, Local)
    missing = [s for s in scenes if s['image'] not in {r['image'] for r in resolved}]
    if missing:
        flux_results = generate_flux_images(missing, output_dir)
        resolved.extend(flux_results)
        if len(resolved) == len(scenes):
            print("✅ All images completed via Gemini + Flux (FREE)")
            return resolved
    
    # FREE TIER 3: SDXL (Backup, Local)
    missing = [s for s in scenes if s['image'] not in {r['image'] for r in resolved}]
    if missing:
        sdxl_results = generate_sdxl_images(missing, output_dir)
        resolved.extend(sdxl_results)
        if len(resolved) == len(scenes):
            print("✅ All images completed via Free Tier (Gemini/Flux/SDXL)")
            return resolved
    
    # PAID TIER 1: DALL-E 3 (if free options exhausted)
    missing = [s for s in scenes if s['image'] not in {r['image'] for r in resolved}]
    if missing:
        print(f"⚠️ {len(missing)} images need PAID generation...")
        dalle_results = generate_dalle_assets(missing, output_dir)
        resolved.extend(dalle_results)
        if len(resolved) == len(scenes): return resolved
    
    # PAID TIER 2: Banana.dev
    missing = [s for s in scenes if s['image'] not in {r['image'] for r in resolved}]
    if missing: resolved.extend(generate_banana_assets(missing, output_dir))
        
    # FINAL FALLBACK: Pexels Cartoon
    missing = [s for s in scenes if s['image'] not in {r['image'] for r in resolved}]
    if missing: resolved.extend(generate_pexels_assets(missing, output_dir, style="cartoon"))
        
    return resolved

def translate_to_hebrew(text):
    try:
        res = get_client().chat.completions.create(model="gpt-4o", messages=[{"role": "system", "content": "Translate to HEBREW. Return ONLY text."}, {"role": "user", "content": text}])
        return res.choices[0].message.content
    except: return "העתיд כבר כאן."

def translate_to_english(text):
    try:
        res = get_client().chat.completions.create(model="gpt-4o", messages=[{"role": "system", "content": "Translate to ENGLISH. Return ONLY text."}, {"role": "user", "content": text}])
        return res.choices[0].message.content
    except: return "The future is here."

def main():
    """Execute Full Daily Viral Content Pipeline"""
    print("🚀 DAILY RESEARCHER PIPELINE INITIATED")
    
    # 1. Research & Scripting
    data = run_daily_research(style="impact")
    if not data:
        print("❌ Pipeline aborted: Research failed.")
        return

    # Check for Output Directory
    timestamp = time.strftime("%Y-%m-%d")
    output_base = ROOT_DIR.parent / "Production_Factory/output"
    daily_dir = output_base / timestamp
    daily_dir.mkdir(parents=True, exist_ok=True)
    
    # Save Script Data
    json_path = daily_dir / "script_data.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"📜 Script Data saved to: {json_path}")
    
    # 2. Image Generation (Visualization)
    print("🎨 Generating Visual Assets...")
    scenes = data.get("scenes", [])
    if not scenes:
        print("❌ No scenes found in script data.")
        return
        
    resolved_scenes = generate_vision_assets(scenes, daily_dir, style="impact")
    
    # Update JSON with local paths
    data["scenes"] = resolved_scenes
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    if len(resolved_scenes) < len(scenes):
        print(f"⚠️ Warning: Only {len(resolved_scenes)}/{len(scenes)} images generated.")
    
    # 3. Handover to Orchestrator (Audio + Video Assembly)
    print("🤝 Handing over to Orchestrator v3 (No-Face)...")
    try:
        # Add Production_Factory to path for internal imports
        factory_path = ROOT_DIR.parent / "Production_Factory"
        if str(factory_path) not in sys.path:
            sys.path.append(str(factory_path))
            
        import orchestrator_v3_no_face as orchestrator
        
        # Override Orchestrator Output Dirs to match Daily Dir
        orchestrator.OUTPUT_DIR = daily_dir
        orchestrator.INPUT_DIR = daily_dir
        orchestrator.BROLL_DIR = factory_path / "broll" # Shared B-roll library
        
        # Run RU Pipeline
        script_ru = data.get("script_ru", "")
        if script_ru:
            final_video_ru = orchestrator.run_no_face_pipeline(
                text=script_ru,
                lang="ru",
                output_name="daily_viral_ru",
                scenes=resolved_scenes,
                style="impact"
            )
            if final_video_ru:
                print(f"🎉 SUCCESS! Video Ready: {final_video_ru}")
            else:
                print("❌ RU Video Assembly failed.")
                
    except ImportError as e:
        print(f"❌ Failed to import orchestrator: {e}")
    except Exception as e:
        print(f"❌ Orchestration failed: {e}")

if __name__ == "__main__":
    main()
