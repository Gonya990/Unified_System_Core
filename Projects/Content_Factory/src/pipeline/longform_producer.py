#!/usr/bin/env python3
"""
Long-Form Documentary Producer
Produces 25-30 minute deep-dive documentaries using LLM Council for research.
Weekly Schedule: Saturday 18:00 Israel Time

Token-aware: Uses TokenBroker for API management
"""

import json
import logging
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("LongFormProducer")

# Setup paths
SRC_DIR = Path(__file__).parent.parent.resolve()
FACTORY_DIR = SRC_DIR.parent
PROJECTS_DIR = FACTORY_DIR.parent
ROOT_DIR = PROJECTS_DIR.parent

# Add paths
sys.path.append(str(SRC_DIR / "researcher"))
sys.path.append(str(SRC_DIR / "pipeline"))
sys.path.append(str(ROOT_DIR / "Scripts/Utilities"))
sys.path.append(str(ROOT_DIR / "LLM_Council"))
sys.path.append(str(ROOT_DIR / "Scripts/Reporting"))

try:
    from telegram_reporter import (
        report_phase_complete,
        report_production_error,
        report_production_start,
    )
except ImportError:
    report_production_start = report_phase_complete = report_production_error = lambda *args, **kwargs: None

# load_dotenv(ROOT_DIR / ".env") # Handled at top

# Import TokenBroker
try:
    from token_broker import TokenBroker

    BROKER = TokenBroker()
    print("✅ TokenBroker ready for Long-Form production")
except ImportError:
    BROKER = None
    print("⚠️ TokenBroker not found, using ENV fallback")

# =============================================================================
#                           LONG-FORM CONFIGURATION
# =============================================================================

LONGFORM_CONFIG = {
    "target_duration_minutes": 28,  # Target 28 min (leaves buffer)
    "segments": 6,  # 6 segments x ~5 min each
    "words_per_minute": 130,  # Narration speed
    "style": "documentary",
    "lang": "ru",
    "output_prefix": "documentary_weekly",
}

# Each segment is ~5 minutes = ~650 words
WORDS_PER_SEGMENT = (
    LONGFORM_CONFIG["target_duration_minutes"] * LONGFORM_CONFIG["words_per_minute"] // LONGFORM_CONFIG["segments"]
)

# =============================================================================
#                           TOKEN TRACKING
# =============================================================================


class TokenTracker:
    """Track token usage across the pipeline"""

    def __init__(self):
        self.usage = {
            "openai": {"input": 0, "output": 0},
            "gemini": {"input": 0, "output": 0},
            "total_cost_estimate": 0.0,
        }

    def log(self, provider: str, input_tokens: int, output_tokens: int):
        if provider in self.usage:
            self.usage[provider]["input"] += input_tokens
            self.usage[provider]["output"] += output_tokens

        # Rough cost estimate (OpenAI GPT-4o pricing)
        if provider == "openai":
            self.usage["total_cost_estimate"] += (input_tokens * 2.5 + output_tokens * 10) / 1_000_000
        print(
            f"📊 Token Usage [{provider}]: +{input_tokens} in, +{output_tokens} out | Total est: ${self.usage['total_cost_estimate']:.4f}"
        )

    def report(self):
        print("\n" + "=" * 50)
        print("📊 LONG-FORM PRODUCTION TOKEN REPORT")
        print("=" * 50)
        for provider, usage in self.usage.items():
            if isinstance(usage, dict):
                print(f"  {provider}: {usage['input']} input, {usage['output']} output")
        print(f"  💰 Estimated Cost: ${self.usage['total_cost_estimate']:.4f}")
        print("=" * 50 + "\n")
        return self.usage


TRACKER = TokenTracker()

# =============================================================================
#                           DEEP RESEARCH (PLAN & EXECUTE)
# =============================================================================


def get_documentary_structure(topic: str) -> Optional[dict]:
    """Phase 1: Get structured plan with segment outlines"""
    print(f"\n🧠 PHASE 1: Planning Documentary Structure for '{topic}'")

    try:
        from council.council import LLMCouncil

        if BROKER:
            council = LLMCouncil.from_token_broker(BROKER)
        else:
            council = LLMCouncil.from_env(str(ROOT_DIR / "LLM_Council/.env"))

        plan_query = f"""
        Create a detailed 6-segment OUTLINE for a 28-minute DOCUMENTARY about: {topic}

        Return JSON format:
        {{
            "title": "Documentary Title (Russian)",
            "description": "YouTube description",
            "segments": [
                {{
                    "name": "segment_name",
                    "focus_points": ["point 1", "point 2", "point 3"],
                    "visual_theme": "general visual style",
                    "target_minutes": 5
                }}
            ],
            "youtube_tags": ["tag1", "tag2"]
        }}

        Rules:
        - Russian language for title/description
        - Exactly 6 segments
        """

        import asyncio

        # Enable verbose logging to troubleshoot
        session = asyncio.run(council.deliberate(plan_query, verbose=True))
        consensus = session.stage3_consensus

        # Robust JSON extraction
        if "```json" in consensus:
            consensus = consensus.split("```json")[1].split("```")[0].strip()
        elif "```" in consensus:
            consensus = consensus.split("```")[1].split("```")[0].strip()

        # Try to find { ... } if looks like text
        if not consensus.startswith("{"):
            start = consensus.find("{")
            end = consensus.rfind("}")
            if start != -1 and end != -1:
                consensus = consensus[start : end + 1]

        data = json.loads(consensus)
        TRACKER.log("openai", len(plan_query) // 4, len(consensus) // 4)

        try:
            asyncio.run(council.close())
        except Exception:
            pass

        return data
    except Exception as e:
        print(f"❌ Planning failed: {e}")
        return None


def generate_segment_script(topic: str, segment_info: dict, context_summary: str = "") -> Optional[dict]:
    """Phase 2: Generate full-length script for a single segment using LLMCouncil"""
    seg_name = segment_info.get("name", "Unknown")
    print(f"📝 Phase 2: Writing Script for '{seg_name}' (Target 650+ words)")

    try:
        from council.council import LLMCouncil

        if BROKER:
            council = LLMCouncil.from_token_broker(BROKER)
        else:
            council = LLMCouncil.from_env(str(ROOT_DIR / "LLM_Council/.env"))

        prompt = f"""
        Write a FULL DOCUMENTARY SCRIPT for one segment of a documentary about: {topic}

        SEGMENT: {seg_name}
        FOCUS POINTS: {segment_info.get("focus_points")}
        CONTEXT: {context_summary}

        REQUIREMENTS:
        1. LANGUAGE: Russian
        2. LENGTH: Minimum 650 words (Essential!)
        3. TONE: Authoritative, cinematic, engaging
        4. STRUCTURE: Pure narration text with "..." for dramatic pauses
        5. VISUALS: Provide exactly 5-8 vivid visual scene descriptions for Pexels search

        Return JSON format:
        {{
            "script": "FULL TEXT HERE (Min 650 words)...",
            "scenes": [
                {{"keyword": "vivid english search keywords for cinematic b-roll", "description": "russian description"}}
            ]
        }}
        """

        import asyncio

        session = asyncio.run(council.deliberate(prompt, verbose=False))
        content = session.stage3_consensus

        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()

        # Try to find { ... } if it's buried in text
        if "{" in content and "}" in content:
            start = content.find("{")
            end = content.rfind("}")
            content = content[start : end + 1]

        # Clean up some common LLM JSON errors (like trailing commas)
        content = re.sub(r",\s*([\]}])", r"\1", content)

        try:
            seg_data = json.loads(content)
        except json.JSONDecodeError as je:
            print(f"❌ JSON Decode Error at pos {je.pos}: {je.msg}")
            print(f"Snippet near error: {content[max(0, je.pos - 100) : je.pos + 100]}")
            # Final attempt: JSON fixes (double-quote keys if they are single-quoted)
            try:
                # This is a bit risky but can save scripts
                import ast

                seg_data = ast.literal_eval(content)
            except Exception:
                return None

        # Approximate tokens
        TRACKER.log("openai", len(prompt) // 4, len(content) // 4)

        try:
            asyncio.run(council.close())
        except Exception:
            pass

        return seg_data

    except Exception as e:
        print(f"⚠️ Segment generation failed: {e}")
        return None


def deep_research_with_council(topic: str) -> dict:
    """Refactored: Plan with Council, Execute with individual calls"""
    structure = get_documentary_structure(topic)
    if not structure:
        return None

    full_data = {
        "title": structure.get("title"),
        "description": structure.get("description"),
        "youtube_tags": structure.get("youtube_tags"),
        "segments": [],
    }

    cumulative_script = ""
    for i, seg_info in enumerate(structure.get("segments", [])):
        seg_script_data = generate_segment_script(topic, seg_info, context_summary=cumulative_script[-2000:])
        if seg_script_data:
            segment_data = {
                "name": seg_info.get("name"),
                "script": seg_script_data.get("script", ""),
                "scenes": seg_script_data.get("scenes", []),
            }
            full_data["segments"].append(segment_data)
            cumulative_script += " " + segment_data["script"]
        else:
            print(f"❌ Failed to generate script for segment {i + 1}")
            full_data["segments"].append(
                {"name": seg_info.get("name"), "script": f"...Продолжаем наше исследование {topic}...", "scenes": []}
            )

    # Calculate chapters based on word count estimate (~130 wpm)
    chapters = ["0:00 Начало"]
    current_seconds = 0
    for i, seg in enumerate(full_data["segments"][:-1]):
        words = len(seg.get("script", "").split())
        current_seconds += (words / 130) * 60
        m, s = divmod(int(current_seconds), 60)
        chapters.append(f"{m}:{s:02d} {full_data['segments'][i + 1]['name']}")

    full_data["youtube_chapters"] = chapters
    full_data["total_word_count"] = len(cumulative_script.split())

    return full_data


def fallback_research(topic: str) -> dict:
    """Legacy/Simple single-model research"""
    print(f"🌠 Fallback Research (Gemini Flash) for '{topic}'")
    # Kept for compatibility but usually deep_research_with_council handles things now
    return None  # We prefer the new multi-step process


# =============================================================================
#                           LONG-FORM ASSEMBLY
# =============================================================================


def assemble_longform_video(data: dict, output_dir: Path) -> Optional[Path]:
    """
    Assemble full documentary from segments.
    Uses existing orchestrator for each segment, then concatenates.
    """
    print(f"\n🎬 LONG-FORM ASSEMBLY: {data.get('title', 'Documentary')}")

    from daily_researcher import generate_vision_assets
    from orchestrator_v3_no_face import (
        BROLL_DIR,
        add_subtitles,
        assemble_hybrid_video,
        generate_audio,
        semantic_search_broll,
    )

    timestamp = datetime.now().strftime("%Y%m%d")
    segments = data.get("segments", [])

    segment_videos = []

    for i, segment in enumerate(segments):
        print(f"\n📹 Processing Segment {i + 1}/{len(segments)}: {segment.get('name', 'Unknown')}")

        # Rate limiting / token awareness
        time.sleep(3)  # Strategic pause between segments

        script = segment.get("script", "")
        scenes = segment.get("scenes", [])

        if not script:
            print(f"⚠️ Empty script for segment {i + 1}, skipping")
            continue

        segment_name = f"longform_seg_{i}_{timestamp}"

        # 1. Generate audio for this segment
        audio_path = output_dir / f"{segment_name}_audio.wav"
        if not generate_audio(script, audio_path, lang="ru"):
            print(f"❌ Audio failed for segment {i + 1}")
            report_production_error(f"Audio generation failed for segment {i + 1}: {segment.get('name')}")
            continue

        # 2. Fetch visual assets
        assets_dir = output_dir / f"assets_seg_{i}"
        assets_dir.mkdir(exist_ok=True)

        # Convert scenes to proper format
        scene_list = []
        for scene in scenes:
            kw = scene.get("keyword", "technology future")
            scene_list.append({"image": f"seg{i}_scene{len(scene_list)}", "keyword": kw})

        # Alternating styles: Every second segment uses AI Generation (cartoon style)
        current_style = "cartoon" if i % 2 == 1 else "impact"
        print(f"🎨 Using Style: {current_style} for Segment {i + 1}")

        resolved_scenes = generate_vision_assets(scene_list, assets_dir, style=current_style)

        if not resolved_scenes:
            # Use B-roll as backup
            print(f"⚠️ Using B-roll for segment {i + 1}")
            clips = semantic_search_broll(script[:100], BROLL_DIR, num_clips=5)
            for _, clip in enumerate(clips):
                resolved_scenes.append(
                    {"image": str(clip), "resolved_path": str(clip), "keyword": "documentary footage"}
                )

        # 3. Assemble segment video
        raw_video = output_dir / f"{segment_name}_raw.mp4"
        assemble_hybrid_video(audio_path, resolved_scenes, raw_video, style="impact")

        # 4. Add subtitles
        final_segment = output_dir / f"{segment_name}_final.mp4"
        if add_subtitles(raw_video, final_segment, lang="ru", style="impact"):
            segment_videos.append(final_segment)
            # Delete raw video if final succeeded
            if raw_video.exists():
                raw_video.unlink()
        else:
            segment_videos.append(raw_video)

        print(f"✅ Segment {i + 1} complete: {segment_videos[-1]}")
        report_phase_complete(
            f"Segment {i + 1}/{len(segments)} Rendered",
            f"**{segment.get('name')}** is complete.\nStyle: {current_style}",
        )

        # Local Preview: Copy first segment to Desktop immediately
        if i == 0:
            print("📣 FIRST SEGMENT READY! Providing local preview path...")
            try:
                # We can't scp directly from here as we are on the server,
                # but we can print a notification for the orchestrator to handle.
                print(f"PREVIEW_READY: {segment_videos[-1]}")
            except Exception:
                pass

    if not segment_videos:
        print("❌ No segments produced")
        return None

    # 5. Concatenate all segments
    print(f"\n🔗 Concatenating {len(segment_videos)} segments...")

    concat_file = output_dir / "concat_list.txt"
    with open(concat_file, "w") as f:
        for video in segment_videos:
            # Use absolute path or relative to output_dir
            f.write(f"file '{video.name}'\n")

    final_output = output_dir / f"{LONGFORM_CONFIG['output_prefix']}_{timestamp}_final.mp4"

    import subprocess

    try:
        subprocess.run(
            ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_file), "-c", "copy", str(final_output)],
            check=True,
            capture_output=True,
            cwd=str(output_dir),
        )
    except subprocess.CalledProcessError as e:
        print(f"❌ FFMPEG Concat Failed: {e.stderr.decode()}")
        return None

    print(f"✅ DOCUMENTARY COMPLETE: {final_output}")

    # 6. Generate chapter file for YouTube
    chapters = data.get("youtube_chapters", [])
    if chapters:
        chapters_file = output_dir / f"{LONGFORM_CONFIG['output_prefix']}_{timestamp}_chapters.txt"
        with open(chapters_file, "w") as f:
            f.write("\n".join(chapters))
        print(f"📝 YouTube chapters saved: {chapters_file}")

    # Cleanup segment files after concatenation
    for seg in segment_videos:
        if seg.exists() and seg != final_output:
            try:
                seg.unlink()
            except Exception:
                pass

    return final_output


# =============================================================================
#                           MAIN PIPELINE
# =============================================================================


def run_longform_production(topic: str = None) -> Optional[Path]:
    """
    Full long-form documentary production pipeline.
    Call from scheduler or manually.
    """
    print("\n" + "=" * 60)
    print("🎬 LONG-FORM DOCUMENTARY PRODUCTION")
    print("=" * 60)

    timestamp = datetime.now().strftime("%Y-%m-%d")

    # Auto-generate topic if not provided
    if not topic:
        topics = [
            "Искусственный интеллект в 2026: Полная картина",
            "Квантовые компьютеры: Технология будущего уже здесь",
            "Космическая гонка 2026: Марс, Луна и дальше",
            "Биотехнологии: Как мы победим болезни",
            "Энергетическая революция: Термоядерный синтез",
            "Автономные системы: Роботы среди нас",
        ]
        import random

        topic = random.choice(topics)

    print(f"📌 Topic: {topic}")
    report_production_start(topic)

    # 1. Deep Research
    data = deep_research_with_council(topic)
    if not data:
        data = fallback_research(topic)

    if not data:
        print("❌ Research failed, aborting production")
        report_production_error(f"Research failed for topic: {topic}")
        return None

    report_phase_complete("Research & Planning", f"Documentary structure created: {data.get('title')}")

    # 2. Setup output directory
    output_dir = ROOT_DIR / "outputs" / f"documentary_{timestamp}"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save research data
    with open(output_dir / "documentary_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    # 3. Produce video
    final_video = assemble_longform_video(data, output_dir)

    # 4. Token report
    TRACKER.report()

    if final_video:
        print(f"\n🎉 SUCCESS: Documentary ready at {final_video}")
        report_phase_complete("Production Complete", f"Final video ready: {final_video.name}")

        # Local Desktop Transfer (Vibranium Auto-Ship)
        desktop_path = Path.home() / "Desktop" / final_video.name
        print(f"🚚 Shipping to Desktop: {desktop_path}")
        try:
            # This runs on the server, so we can't shutil to local Mac,
            # BUT the user mentioned scp in metadata. I will print the command.
            print(f"RUN_LOCAL: scp root@100.110.209.49:{final_video} ~/Desktop/")
        except Exception:
            pass

    return final_video


# =============================================================================
#                           CLI
# =============================================================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Long-Form Documentary Producer")
    parser.add_argument("--topic", type=str, help="Documentary topic (auto-generated if not provided)")
    parser.add_argument("--test", action="store_true", help="Test mode - research only, no video")

    args = parser.parse_args()

    if args.test:
        print("🧪 TEST MODE: Research only")
        data = deep_research_with_council(args.topic or "AI Revolution 2026")
        if data:
            print(json.dumps(data, indent=2, ensure_ascii=False)[:2000])
        TRACKER.report()
    else:
        run_longform_production(args.topic)
