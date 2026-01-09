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
    return OpenAI(api_key=api_key, base_url="https://api.openai.com/v1")

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
        print("🤖 Attempting Research via OpenAI (GPT-4)...")
        res = get_client().chat.completions.create(
            model="gpt-4-turbo",
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
            print("🌠 Attempting Research via Gemini...")
            import google.generativeai as genai
            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
            model = genai.GenerativeModel("gemini-1.5-flash")
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

def generate_dalle_assets(scenes, output_dir: Path):
    """DALL-E 3 Image generation"""
    time.sleep(1.2) # Vibranium Pause
    print(f"🎨 Trying DALL-E 3 for {len(scenes)} scenes...")
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
    """💎 THE ORCHESTRATOR: Parries between all providers"""
    if style != "cartoon":
        return generate_pexels_assets(scenes, output_dir, style="impact")

    print("🚀 VIBRANIUM CARTOON PIPELINE: Multi-Model Parrying Active")
    # Step 1: DALL-E
    resolved = generate_dalle_assets(scenes, output_dir)
    if len(resolved) == len(scenes): return resolved
    
    # Step 2: Banana (if missing)
    missing = [s for s in scenes if s['image'] not in {r['image'] for r in resolved}]
    if missing: resolved.extend(generate_banana_assets(missing, output_dir))
        
    # Step 3: Pexels Cartoon (if still missing)
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
