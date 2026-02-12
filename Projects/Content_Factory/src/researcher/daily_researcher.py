#!/usr/bin/env python3
import json
import os
import random
import re
import sys
import time
from datetime import datetime
from pathlib import Path

import feedparser
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from openai import OpenAI

# Setup paths
SRC_DIR = Path(__file__).parent.parent.resolve()  # Projects/Content_Factory/src
FACTORY_DIR = SRC_DIR.parent  # Projects/Content_Factory
PROJECTS_DIR = FACTORY_DIR.parent  # /Projects
ROOT_DIR = PROJECTS_DIR.parent  # Unified_System_Core

# Fixed paths for local development
load_dotenv(ROOT_DIR / ".env")
load_dotenv(PROJECTS_DIR / "AI_Core/.env", override=True)

# Import TokenBroker and KnowledgeBase
try:
    # Add AI_Core to path for common modules
    AI_CORE_SRC = PROJECTS_DIR / "AI_Core/src"
    if str(AI_CORE_SRC) not in sys.path:
        sys.path.insert(0, str(AI_CORE_SRC))
    
    from token_broker import TokenBroker
    from modules.knowledge_base import KnowledgeBase
    
    BROKER = TokenBroker()
    KB = KnowledgeBase()
    print("✅ TokenBroker and KnowledgeBase integrated")
except ImportError:
    print("⚠️ Core modules not fully integrated, falling back")
    BROKER = None
    KB = None


# Configuration
def get_key(provider, owner=None):
    if BROKER:
        k = BROKER.get_key(provider, owner)
        if k:
            return k

    # Fallback
    if provider == "openai":
        return os.getenv("OPENAI_API_KEY")
    if provider == "gemini":
        return os.getenv("GEMINI_API_KEY")
    if provider == "pexels":
        return os.getenv("PEXELS_API_KEY")
    return None


PEXELS_API_KEY = get_key("pexels") or "5KikfJFyT75Rlibf2u829q4qZOTm0FVfttKCb5znbJSYqb96qAKarEDY"


def get_client():
    """Lazy initialization of OpenAI client with TokenBroker"""
    api_key = get_key("openai")
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    org_id = os.getenv("OPENAI_ORG_ID")
    return OpenAI(api_key=api_key, base_url=base_url, organization=org_id)


def get_latest_geo_news():
    """Fetches high-stakes Geopolitics & Tech news (Positive Future Focus)"""
    # MEGAFORMA STRATEGY: Future Tech, Scientific Breakthroughs, Global Unity
    topics = [
        "ai curing diseases breakthrough",
        "fusion energy infinite power",
        "mars colonization progress 2026",
        "global reforestation projects ai",
        "quantum computing solving climate change",
        "flying cars commercial launch",
        "universal language translator ai",
        "ocean cleaning autonomous drones",
        "neuralink restoring sight",
        "vertical farming feeding the world",
    ]
    query = random.choice(topics)
    print(f"📡 Researching MEGAFORMA topic: {query}")
    import urllib.parse

    encoded_query = urllib.parse.quote(query)
    # Search Google News
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
        for s in soup(["script", "style"]):
            s.decompose()
        return " ".join(soup.get_text(separator=" ").split())[:3000]
    except Exception as e:
        print(f"⚠️ Failed to browse {url}: {e}")
        return ""


def get_evergreen_topics():
    """Fallback topics for autonomous operation"""
    return [
        {
            "title": "The Rise of Universal Translators and Global Unity",
            "link": "https://en.wikipedia.org/wiki/Universal_translator",
        },
        {
            "title": "Quantum Computing Solving the Climate Crisis",
            "link": "https://en.wikipedia.org/wiki/Quantum_computing",
        },
        {
            "title": "Mars Colonization: The Next Step for Humanity",
            "link": "https://en.wikipedia.org/wiki/Colonization_of_Mars",
        },
        {"title": "Biotechnology: Curing All Diseases by 2050", "link": "https://en.wikipedia.org/wiki/Biotechnology"},
        {"title": "The Energy Revolution: Fusion Power is Near", "link": "https://en.wikipedia.org/wiki/Fusion_power"},
    ]


def run_daily_research(style="impact", deep=False, manual_topic=None, manual_outline=None):
    """Deep research with Megaforma Style (Geopolitics/Mystery) or Manual Inspiration"""
    print(f"🧠 Starting MEGAFORMA {'DEEP ' if deep else ''}RESEARCH (Style: {style.upper()})")

    context = ""

    if manual_topic:
        print(f"💡 Using YouTube Inspiration Topic: {manual_topic}")
        context += f"TOPIC: {manual_topic}\n"
        if manual_outline:
            print("📝 Using Manual Outline...")
            context += f"PROVIDED OUTLINE:\n{manual_outline}\n\n"

        # We might still want *some* fresh news context if the outline is vague,
        # but usually the outline is enough. Let's assume outline acts as context.
    else:
        news = get_latest_geo_news()
        if not news:
            print("⚠️ No fresh news found. Using evergreen fallback topics...")
            news = get_evergreen_topics()

        # Deep research: Browse more articles (up to 10)
        max_articles = 10 if deep else 2
        for item in news[:max_articles]:
            print(f"🔍 Browsing: {item['title']}...")
            context += f"TOPIC: {item['title']}\nCONTENT: {get_page_content(item['link'])}\n\n"

    # Style definitions
    if style == "cartoon":
        tone = "Satirical, sharp, funny politics"
        visuals = "political cartoon style, caricature, vibrant 3d"
    elif style == "sketch":
        tone = "Thoughtful, abstract, intellectual"
        visuals = "black and white pencil sketch, charcoal drawing, rough lines"
    elif style == "painting":
        tone = "Artistic, expressive, emotional"
        visuals = "digital painting, oil painting style, brush strokes, vivid colors"
    else:
        # The "Megaforma" signature style (Peace & Tech Edition)
        tone = "Inspiring, Visionary, Optimistic, Deep Documentary, Unifying"
        visuals = (
            "cinematic documentary footage, solar punk, high tech city, bright future, digital connections, nebula"
        )

    prompt = f"""
    Context: {context}
    Task: Write a viral 'Megaforma-style' RUSSIAN script (15 scenes).
    Theme: Future Tech, Human Progress, Global Unity.

    Target Audience: People looking for inspiration and "The Future" of humanity.
    Tone: {tone} (But structured like a viral educational video - Maksim Nikolashin style).
    Visual Style: {visuals}

    STRUCTURE (The 'Listicle' Format):
    - Scene 1-2: THE HOOK. Use a "Negative/Warning" or "Secret" framing. (e.g., "You won't believe what AI can do...", "Stop ignoring this technology...").
    - Scene 3: The Intro. "Here are 5 technologies changing everything."
    - Scene 4-13: THE LIST. Rapid fire facts/technologies. (e.g. "Number 1...", "Number 2...").
    - Scene 14-15: THE CONCLUSION. Evaluation & Call for Unity.

    CRITICAL:
    - Text must be in RUSSIAN.
    - VISUAL KEYWORDS must be English descriptions for Pexels/AI.
    - Do NOT use "Once upon a time". START WITH IMPACT.
    - Narrator should sound like a wise visionary.
    3. If news/context is weak, invent a realistic near-future AI scenario.
    4. Tone must be grounded in sci-fi reality.
    5. No scene labels. No "Scene 1:". ONLY spoken words. Use "..." for pauses.

    Format: JSON {{
        "selected_topic": "Viral Title (e.g. 7 Insane AI Tools)",
        "description": "YouTube Description with hashtags",
        "script_ru": "Full spoken text...",
        "pinned_comment": "Question to audience? (e.g. Which tech do you want?)",
        "scenes": [{{"image": "scene_1", "keyword": ""}}]
    }}
    """

    data = None

    # Strategy: Gemini (Primary for DEEP RESEARCH due to context window)
    if deep:
        try:
            print(f"🌠 DEEP RESEARCH: Attempting via Gemini (Context size: {len(context)})")
            import google.generativeai as genai

            genai.configure(api_key=get_key("gemini"))
            model = genai.GenerativeModel("models/gemini-1.5-pro")  # Using Pro for deep research
            res = model.generate_content(prompt)
            content = res.text
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            data = json.loads(content)
        except Exception as e:
            print(f"⚠️ Gemini Deep Research failed: {e}. Falling back to OpenAI...")

    # Strategy 1: OpenAI Responses API
    if not data:
        try:
            print("🤖 Attempting Research via OpenAI Responses API (GPT-4o)...")
            client = get_client()
            # Try new Responses API first (or fallback to Chat Completions)
            try:
                res = client.responses.create(
                    model="gpt-4o", input=prompt, instructions="Return ONLY valid JSON. No markdown, no explanations."
                )
                content = res.output_text
            except Exception as e:
                print(f"⚠️ Responses API not available ({e}), trying standard Chat Completions...")
                res = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "Return ONLY valid JSON. No markdown, no explanations."},
                        {"role": "user", "content": prompt},
                    ],
                    response_format={"type": "json_object"},
                )
                content = res.choices[0].message.content

            if content and "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            data = json.loads(content)
        except Exception as e:
            print(f"⚠️ OpenAI Research failed: {e}. Checking legacy fallback...")

    # Strategy 2: Gemini Fallback
    if not data:
        try:
            print("🌠 Attempting Research via Gemini 2.0...")
            import google.generativeai as genai

            genai.configure(api_key=get_key("gemini"))
            model = genai.GenerativeModel("models/gemini-2.0-flash")
            res = model.generate_content(prompt)
            content = res.text
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            data = json.loads(content)
        except Exception as e:
            print(f"⚠️ Gemini Research failed: {e}. Falling back to Ollama (Rock Solid)...")

    # Strategy 3: Ollama (Rock Solid Local Fallback)
    if not data:
        try:
            print("🦙 Attempting Research via Ollama (Llama 3)...")
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "llama3",
                    "prompt": f"{prompt}\nReturn ONLY JSON. Do not include markdown or explanations.",
                    "stream": False,
                    "format": "json"
                },
                timeout=60,
            )
            resp_json = response.json()
            if resp_json and isinstance(resp_json, dict):
                data = resp_json.get("response")
                if isinstance(data, str):
                    data = json.loads(data)
                print("✅ Ollama Research successful!")
            else:
                print("⚠️ Ollama returned empty or invalid response")
        except Exception as e:
            print(f"❌ All Research models failed (including Ollama): {e}")
            return None

    # Strict Scene Label Cleanup
    script = data.get("script_ru", "")
    script = re.sub(r"(?i)(сцена|scene|кадр|shot|narrator|диктор|voiceover)\s*\d*[:.-]*\s*", "", script)
    data["script_ru"] = script.strip()
    return data


def get_style_prompt_prefix(style):
    if style == "cartoon":
        return "cartoon style, 3d animation, pixar quality, vibrant colors, vertical 9:16 format"
    elif style == "sketch":
        return (
            "black and white pencil sketch, charcoal drawing, rough lines, artistic, minimalist, vertical 9:16 format"
        )
    elif style == "painting":
        return "digital painting, oil painting style, brush strokes, artistic, vivid colors, vertical 9:16 format"
    else:  # impact/default
        return "cinematic documentary footage, hyper-realistic, 8k, detailed, dramatic lighting, vertical 9:16 format"


def generate_gemini_images(scenes, output_dir: Path, style="impact"):
    """💎 Gemini 2.0 Flash Image - DISABLED (API not available yet)"""
    print("⚠️ Gemini Image Generation not available (experimental API)")
    return []  # Skip for now, will be enabled when API is stable


def generate_flux_images(scenes, output_dir: Path, style="impact"):
    """⚡ Flux.1 Schnell - FREE Local (Fast & Quality)"""
    print(f"⚡ Checking Flux.1 Schnell server (Style: {style})...")
    resolved = []
    prefix = get_style_prompt_prefix(style)
    try:
        import requests

        flux_url = "http://localhost:8080/generate"

        # Quick health check (1 second timeout)
        try:
            requests.get("http://localhost:8080/", timeout=1)
        except Exception:
            print("❌ Flux server not running (install in progress)")
            return []

        print(f"✅ Flux server online! Generating {len(scenes)} scenes...")
        for s in scenes:
            time.sleep(0.5)
            try:
                # Use style-aware prefix
                prompt = f"{prefix}, {s['keyword']}"
                response = requests.post(
                    flux_url,
                    json={"prompt": prompt, "width": 1080, "height": 1920, "num_steps": 4, "guidance": 3.5},
                    timeout=30,
                )

                if response.status_code == 200:
                    path = output_dir / f"{s['image']}.jpg"
                    with open(path, "wb") as f:
                        f.write(response.content)
                    s["resolved_path"] = str(path)
                    resolved.append(s)
                    print(f"   ✅ Flux ({style}): {s['image']}")
            except Exception as e:
                print(f"   ⚠️ Flux failed for {s['image']}: {e}")
                break  # Stop trying if one fails
    except Exception as e:
        print(f"❌ Flux error: {e}")
    return resolved


def generate_sdxl_images(scenes, output_dir: Path, style="impact"):
    """🎨 Stable Diffusion XL - FREE Local (Backup)"""
    print(f"🎨 Checking SDXL server (Style: {style})...")
    resolved = []
    prefix = get_style_prompt_prefix(style)
    try:
        import requests

        sdxl_url = "http://localhost:8188/generate"

        # Quick health check (1 second timeout)
        try:
            requests.get("http://localhost:8188/", timeout=1)
        except Exception:
            print("❌ SDXL server not running (install in progress)")
            return []

        print(f"✅ SDXL server online! Generating {len(scenes)} scenes...")
        for s in scenes:
            time.sleep(1.0)
            try:
                prompt = f"{prefix}, {s['keyword']}"
                response = requests.post(
                    sdxl_url,
                    json={
                        "prompt": prompt,
                        "negative_prompt": "ugly, blurry, low quality, distorted, text, watermark",
                        "width": 1080,
                        "height": 1920,
                        "steps": 25,
                    },
                    timeout=60,
                )

                if response.status_code == 200:
                    path = output_dir / f"{s['image']}.jpg"
                    with open(path, "wb") as f:
                        f.write(response.content)
                    s["resolved_path"] = str(path)
                    resolved.append(s)
                    print(f"   ✅ SDXL ({style}): {s['image']}")
            except Exception as e:
                print(f"   ⚠️ SDXL failed for {s['image']}: {e}")
                break  # Stop trying if one fails
    except Exception as e:
        print(f"❌ SDXL error: {e}")
    return resolved


def generate_dalle_assets(scenes, output_dir: Path, style="impact"):
    """DALL-E 3 Image generation (PAID FALLBACK)"""
    time.sleep(1.2)  # Vibranium Pause
    print(f"💰 Trying DALL-E 3 for {len(scenes)} scenes (PAID, Style: {style})...")
    resolved = []
    client = get_client()
    prefix = get_style_prompt_prefix(style)
    for s in scenes:
        time.sleep(2.0)  # User requested tactical pause
        try:
            prompt = f"{prefix}, VERTICAL 9:16, {s['keyword']}"
            res = client.images.generate(model="dall-e-3", prompt=prompt, size="1024x1792", n=1)
            img_data = requests.get(res.data[0].url).content
            path = output_dir / f"{s['image']}.jpg"
            with open(path, "wb") as f:
                f.write(img_data)
            s["resolved_path"] = str(path)
            resolved.append(s)
            print(f"   ✅ DALL-E: {s['image']}")
        except Exception as e:
            print(f"   ⚠️ DALL-E failed: {e}")
    return resolved


def generate_banana_assets(scenes, output_dir: Path, style="impact"):
    """Banana.dev Image generation"""
    api_key = os.getenv("BANANA_API_KEY")
    if not api_key:
        return []
    print(f"🍌 Trying Banana.dev for {len(scenes)} scenes (Style: {style})...")
    import banana_dev as banana

    resolved = []
    model_key = os.getenv("BANANA_MODEL_KEY", "stable-diffusion-xl")
    prefix = get_style_prompt_prefix(style)
    for s in scenes:
        time.sleep(2.0)  # Tactical pause
        try:
            inputs = {"prompt": f"{prefix}, vertical, {s['keyword']}"}
            res = banana.run(api_key, model_key, inputs)
            img_b64 = res["modelOutputs"][0]["image_base64"]
            path = output_dir / f"{s['image']}.jpg"
            import base64

            with open(path, "wb") as f:
                f.write(base64.b64decode(img_b64))
            s["resolved_path"] = str(path)
            resolved.append(s)
            print(f"   ✅ Banana: {s['image']}")
        except Exception as e:
            print(f"   ⚠️ Banana failed: {e}")
    return resolved


def generate_pexels_assets(scenes, output_dir: Path, style="impact"):
    """Pexels search with style-augmented keywords"""
    print(f"🎬 Trying Pexels ({style}) for {len(scenes)} scenes...")
    resolved = []
    for s in scenes:
        time.sleep(1.0)  # Tactical pause
        try:
            kw = s["keyword"]
            if style == "cartoon":
                kw = f"cartoon illustration animation {kw}"
            elif style == "sketch":
                kw = f"sketch drawing {kw}"
            elif style == "painting":
                kw = f"painting art {kw}"

            url = f"https://api.pexels.com/v1/search?query={kw}&per_page=1&orientation=portrait"
            res = requests.get(url, headers={"Authorization": PEXELS_API_KEY}).json()
            if res.get("photos"):
                img_data = requests.get(res["photos"][0]["src"]["large2x"]).content
                path = output_dir / f"{s['image']}.jpg"
                with open(path, "wb") as f:
                    f.write(img_data)
                s["resolved_path"] = str(path)
                resolved.append(s)
                print(f"   ✅ Pexels: {s['image']}")
        except Exception as e:
            print(f"   ⚠️ Pexels failed: {e}")
    return resolved


def check_local_context_files(scenes, output_dir: Path):
    """Search for matching keywords in local Context/ folder"""
    context_dir = ROOT_DIR / "Context"
    if not context_dir.exists():
        return []

    resolved = []
    import shutil

    # Simple keyword matching from filenames
    # Get all image/video files
    candidates = list(context_dir.rglob("*.jpg")) + list(context_dir.rglob("*.png")) + list(context_dir.rglob("*.mp4"))

    print(f"📂 Checking {len(candidates)} local context files for matches...")

    for s in scenes:
        kw = s['keyword'].lower().split()
        best_match = None

        for cand in candidates:
            # Check if any keyword matches filename
            cand_name = cand.stem.lower()
            if any(k in cand_name for k in kw):
                best_match = cand
                break

        if best_match:
            # Copy to assets folder to ensure availability
            dest = output_dir / best_match.name
            shutil.copy2(best_match, dest)
            s["resolved_path"] = str(dest)
            resolved.append(s)
            print(f"   ✅ Local Context Match: {s['image']} <- {best_match.name}")

    return resolved


def generate_vision_assets(scenes, output_dir: Path, style="impact"):
    """💎 VIBRANIUM TRIPLE-THREAT: Local Context → Free → Paid Failover"""
    print(f"🚀 VIBRANIUM TRIPLE-THREAT PIPELINE: Local → Free → Paid Failover (Style: {style})")
    print("   Priority: Context → Gemini 2.0 → Flux.1 → SDXL → DALL-E → Banana → Pexels")

    # LEVEL 0: LOCAL CONTEXT (Highest Priority - Brand Assets)
    resolved = check_local_context_files(scenes, output_dir)
    if len(resolved) == len(scenes):
        print("✅ All assets found in Local Context")
        return resolved

    # FREE TIER 1: Gemini 2.0 Flash Image (Best Quality, Free)
    missing = [s for s in scenes if s["image"] not in {r["image"] for r in resolved}]
    if missing:
        gemini_results = generate_gemini_images(missing, output_dir, style=style)
        resolved.extend(gemini_results)
        if len(resolved) == len(scenes):
            print("✅ All images generated via Gemini 2.0 (FREE)")
            return resolved

    # FREE TIER 2: Flux.1 Schnell (Fast, Local)
    missing = [s for s in scenes if s["image"] not in {r["image"] for r in resolved}]
    if missing:
        flux_results = generate_flux_images(missing, output_dir, style=style)
        resolved.extend(flux_results)
        if len(resolved) == len(scenes):
            print("✅ All images completed via Gemini + Flux (FREE)")
            return resolved

    # FREE TIER 3: SDXL (Backup, Local)
    missing = [s for s in scenes if s["image"] not in {r["image"] for r in resolved}]
    if missing:
        sdxl_results = generate_sdxl_images(missing, output_dir, style=style)
        resolved.extend(sdxl_results)
        if len(resolved) == len(scenes):
            print("✅ All images completed via Free Tier (Gemini/Flux/SDXL)")
            return resolved

    # PAID TIER 1: DALL-E 3 (if free options exhausted)
    missing = [s for s in scenes if s["image"] not in {r["image"] for r in resolved}]
    if missing:
        print(f"⚠️ {len(missing)} images need PAID generation...")
        dalle_results = generate_dalle_assets(missing, output_dir, style=style)
        resolved.extend(dalle_results)
        if len(resolved) == len(scenes):
            return resolved

    # PAID TIER 2: Banana.dev
    missing = [s for s in scenes if s["image"] not in {r["image"] for r in resolved}]
    if missing:
        resolved.extend(generate_banana_assets(missing, output_dir, style=style))

    # FINAL FALLBACK: Pexels
    missing = [s for s in scenes if s["image"] not in {r["image"] for r in resolved}]
    if missing:
        try:
            resolved.extend(generate_pexels_assets(missing, output_dir, style=style))
        except Exception:
            # Pexels failure shouldn't crash the pipeline, just log it
            print("⚠️ Pexels fallback failed")

    return resolved


def translate_to_hebrew(text):
    try:
        res = get_client().chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Translate to HEBREW. Return ONLY text."},
                {"role": "user", "content": text},
            ],
        )
        return res.choices[0].message.content
    except Exception:
        return "העתיд כבר כאן."


def translate_to_english(text):
    try:
        res = get_client().chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Translate to ENGLISH. Return ONLY text."},
                {"role": "user", "content": text},
            ],
        )
        return res.choices[0].message.content
    except Exception:
        return "The future is here."


def main():
    """Execute Full Daily Viral Content Pipeline"""
    print("🚀 DAILY RESEARCHER PIPELINE INITIATED")
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # 1. Research & Scripting
    data = run_daily_research(style="impact")
    if not data:
        print("❌ Pipeline aborted: Research failed.")
        return

    # Check for Output Directory
    daily_dir = FACTORY_DIR / "outputs" / timestamp
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
        # Add pipeline path for internal imports
        pipeline_path = SRC_DIR / "pipeline"
        if str(pipeline_path) not in sys.path:
            sys.path.append(str(pipeline_path))

        import orchestrator_v3_no_face as orchestrator

        # Override Orchestrator Output Dirs to match Daily Dir
        orchestrator.OUTPUT_DIR = daily_dir
        orchestrator.INPUT_DIR = daily_dir
        orchestrator.BROLL_DIR = ROOT_DIR / "broll"  # Shared B-roll library

        # Run RU Pipeline
        script_ru = data.get("script_ru", "")
        if script_ru:
            final_video_ru = orchestrator.run_no_face_pipeline(
                text=script_ru, lang="ru", output_name="daily_viral_ru", scenes=resolved_scenes, style="impact"
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
