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
ROOT_DIR = Path(__file__).parent.resolve()
load_dotenv(ROOT_DIR / ".env")
load_dotenv(ROOT_DIR.parent.parent / "Projects/AI_Core/.env", override=True)

# Configuration
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "5KikfJFyT75Rlibf2u829q4qZOTm0FVfttKCb5znbJSYqb96qAKarEDY")

def get_client():
    """Lazy initialization of OpenAI client"""
    api_key = os.getenv("OPENAI_API_KEY")
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
    {style_prompt}
    CRITICAL: No scene labels. No "Scene 1:". ONLY spoken words. Use "..." for pauses.
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
    """💎 Gemini 2.0 Flash Image - FREE Tier 1 (Highest Quality)"""
    print(f"🌠 Trying Gemini 2.0 Flash Image for {len(scenes)} scenes...")
    resolved = []
    try:
        import google.generativeai as genai
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        model = genai.GenerativeModel("models/gemini-2.0-flash-exp-image-generation")
        
        for s in scenes:
            time.sleep(1.5)
            try:
                prompt = f"Create a vibrant 9:16 vertical cartoon-style illustration: {s['keyword']}. Pixar quality, colorful, fun, high detail."
                response = model.generate_content([prompt])
                
                # Gemini returns image data
                if hasattr(response, 'candidates') and response.candidates:
                    for part in response.candidates[0].content.parts:
                        if hasattr(part, 'inline_data'):
                            img_data = part.inline_data.data
                            path = output_dir / f"{s['image']}.jpg"
                            with open(path, "wb") as f:
                                f.write(img_data)
                            s["resolved_path"] = str(path)
                            resolved.append(s)
                            print(f"   ✅ Gemini: {s['image']}")
                            break
            except Exception as e:
                print(f"   ⚠️ Gemini failed for {s['image']}: {e}")
    except Exception as e:
        print(f"❌ Gemini Image setup failed: {e}")
    return resolved

def generate_flux_images(scenes, output_dir: Path):
    """⚡ Flux.1 Schnell - FREE Local (Fast & Quality)"""
    print(f"⚡ Trying Flux.1 Schnell (local) for {len(scenes)} scenes...")
    resolved = []
    try:
        import requests
        # Check if local Flux server is running
        flux_url = "http://localhost:8080/generate"
        
        for s in scenes:
            time.sleep(0.5)  # Flux is fast!
            try:
                prompt = f"cartoon style, 3d animation, pixar quality, vibrant colors, vertical 9:16 format, {s['keyword']}"
                response = requests.post(flux_url, json={
                    "prompt": prompt,
                    "width": 1080,
                    "height": 1920,
                    "num_steps": 4,  # Schnell optimized for 1-4 steps
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
    except Exception as e:
        print(f"❌ Flux server not available: {e}")
    return resolved

def generate_sdxl_images(scenes, output_dir: Path):
    """🎨 Stable Diffusion XL - FREE Local (Backup)"""
    print(f"🎨 Trying SDXL (local) for {len(scenes)} scenes...")
    resolved = []
    try:
        import requests
        sdxl_url = "http://localhost:8188/generate"
        
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
    except Exception as e:
        print(f"❌ SDXL server not available: {e}")
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
