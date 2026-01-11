#!/usr/bin/env python3
"""
Long-Form Documentary Producer
Produces 25-30 minute deep-dive documentaries using LLM Council for research.
Weekly Schedule: Saturday 18:00 Israel Time

Token-aware: Uses TokenBroker for API management
"""

import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

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

from dotenv import load_dotenv
load_dotenv(ROOT_DIR / ".env")

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
    "segments": 6,                   # 6 segments x ~5 min each
    "words_per_minute": 130,         # Narration speed
    "style": "documentary",
    "lang": "ru",
    "output_prefix": "documentary_weekly"
}

# Each segment is ~5 minutes = ~650 words
WORDS_PER_SEGMENT = LONGFORM_CONFIG["target_duration_minutes"] * LONGFORM_CONFIG["words_per_minute"] // LONGFORM_CONFIG["segments"]

# =============================================================================
#                           TOKEN TRACKING
# =============================================================================

class TokenTracker:
    """Track token usage across the pipeline"""
    def __init__(self):
        self.usage = {
            "openai": {"input": 0, "output": 0},
            "gemini": {"input": 0, "output": 0},
            "total_cost_estimate": 0.0
        }
    
    def log(self, provider: str, input_tokens: int, output_tokens: int):
        if provider in self.usage:
            self.usage[provider]["input"] += input_tokens
            self.usage[provider]["output"] += output_tokens
        
        # Rough cost estimate (OpenAI GPT-4o pricing)
        if provider == "openai":
            self.usage["total_cost_estimate"] += (input_tokens * 2.5 + output_tokens * 10) / 1_000_000
        print(f"📊 Token Usage [{provider}]: +{input_tokens} in, +{output_tokens} out | Total est: ${self.usage['total_cost_estimate']:.4f}")
    
    def report(self):
        print("\n" + "="*50)
        print("📊 LONG-FORM PRODUCTION TOKEN REPORT")
        print("="*50)
        for provider, usage in self.usage.items():
            if isinstance(usage, dict):
                print(f"  {provider}: {usage['input']} input, {usage['output']} output")
        print(f"  💰 Estimated Cost: ${self.usage['total_cost_estimate']:.4f}")
        print("="*50 + "\n")
        return self.usage

TRACKER = TokenTracker()

# =============================================================================
#                           DEEP RESEARCH (LLM COUNCIL)
# =============================================================================

def deep_research_with_council(topic: str) -> Dict:
    """
    Use LLM Council for multi-model deep research.
    Returns structured documentary content.
    """
    print(f"\n🧠 LLM COUNCIL: Deep Research on '{topic}'")
    
    try:
        from council.council import LLMCouncil
        
        if BROKER:
            # Try research tier, fallback to any
            council = LLMCouncil.from_token_broker(BROKER, tier="research")
            if not council.primary_client: # Double check if it actually got a key
                 council = LLMCouncil.from_token_broker(BROKER, tier=None)
        else:
            council = LLMCouncil.from_env(str(ROOT_DIR / "LLM_Council/.env"))
        
        query = f"""
        Create a 28-minute DOCUMENTARY script about: {topic}
        
        Structure (6 segments, ~650 words each):
        
        SEGMENT 1: THE HOOK (5 min)
        - Shocking opening fact or question
        - Why this matters NOW
        - Brief preview of what's coming
        
        SEGMENT 2: HISTORICAL CONTEXT (5 min)
        - How did we get here?
        - Key milestones and turning points
        - The pivotal moment that changed everything
        
        SEGMENT 3: THE CURRENT STATE (5 min)
        - What's happening RIGHT NOW
        - Key players and innovations
        - Recent breakthroughs
        
        SEGMENT 4: DEEP DIVE - TECHNOLOGY (5 min)
        - How it actually works
        - Technical explanation made accessible
        - Demonstrations and examples
        
        SEGMENT 5: IMPLICATIONS & FUTURE (5 min)
        - What does this mean for society?
        - Expert predictions
        - Potential risks and opportunities
        
        SEGMENT 6: CONCLUSION & CALL TO ACTION (3 min)
        - Summary of key insights
        - What viewers should do/think
        - Inspiring final message
        
        CRITICAL RULES:
        - Write in RUSSIAN language
        - Natural speech patterns (use "..." for pauses)
        - NO scene labels or "Scene 1:" markers
        - Each segment should have 3-5 visual scene descriptions
        - Tone: Documentary style, authoritative but accessible
        
        Return JSON format:
        {{
            "title": "Documentary Title (Russian)",
            "description": "YouTube description with SEO",
            "segments": [
                {{
                    "name": "segment_name",
                    "script": "full spoken text for this segment...",
                    "scenes": [{{"keyword": "visual description for B-roll"}}]
                }}
            ],
            "total_word_count": 3900,
            "youtube_tags": ["tag1", "tag2"],
            "youtube_chapters": ["0:00 Intro", "5:00 History", ...]
        }}
        """
        
        import asyncio
        session = asyncio.run(council.deliberate(query, verbose=True))
        
        # Parse consensus
        consensus = session.stage3_consensus
        if "```json" in consensus:
            consensus = consensus.split("```json")[1].split("```")[0].strip()
        
        data = json.loads(consensus)
        print(f"✅ Council completed: '{data.get('title', 'Unknown')}'")
        
        # Track approximate tokens (estimate based on response length)
        TRACKER.log("openai", len(query) // 4, len(consensus) // 4)
        
        council.close()
        return data
        
    except Exception as e:
        print(f"❌ Council research failed: {e}")
        return None

def fallback_research(topic: str) -> Dict:
    """
    Fallback to single-model research if Council fails.
    Uses Gemini Pro for long context.
    """
    print(f"🌠 Fallback Research (Gemini Pro) for '{topic}'")
    
    try:
        import google.generativeai as genai
        
        # Try to find a key for gemini
        api_key = BROKER.get_key("gemini") if BROKER else os.getenv("GEMINI_API_KEY")
        if not api_key:
             api_key = BROKER.get_key("gemini", tier="free") if BROKER else None
        
        if not api_key:
             print("❌ No Gemini API key found for fallback")
             return None

        genai.configure(api_key=api_key)
        
        # Use Flash for higher reliability/speed as fallback
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        prompt = f"""
        Create a 28-minute DOCUMENTARY script about: {topic}
        
        Structure: 6 segments, ~650 words each, total ~3900 words.
        
        Segments: Hook, History, Current State, Technology Deep-Dive, Future Implications, Conclusion.
        
        Write in RUSSIAN. Include visual scene descriptions.
        
        Return JSON with: title, description, segments (each with name, script, scenes), youtube_chapters.
        """
        
        response = model.generate_content(prompt)
        content = response.text
        
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        
        data = json.loads(content)
        TRACKER.log("gemini", len(prompt) // 4, len(content) // 4)
        
        return data
        
    except Exception as e:
        print(f"❌ Fallback research failed: {e}")
        return None

# =============================================================================
#                           LONG-FORM ASSEMBLY
# =============================================================================

def assemble_longform_video(data: Dict, output_dir: Path) -> Optional[Path]:
    """
    Assemble full documentary from segments.
    Uses existing orchestrator for each segment, then concatenates.
    """
    print(f"\n🎬 LONG-FORM ASSEMBLY: {data.get('title', 'Documentary')}")
    
    from orchestrator_v3_no_face import (
        generate_audio, OUTPUT_DIR, INPUT_DIR, BROLL_DIR,
        assemble_hybrid_video, add_subtitles, semantic_search_broll
    )
    from pexels_broll import semantic_search_broll
    from daily_researcher import generate_pexels_assets
    
    timestamp = datetime.now().strftime('%Y%m%d')
    segments = data.get("segments", [])
    
    segment_videos = []
    
    for i, segment in enumerate(segments):
        print(f"\n📹 Processing Segment {i+1}/{len(segments)}: {segment.get('name', 'Unknown')}")
        
        # Rate limiting / token awareness
        time.sleep(3)  # Strategic pause between segments
        
        script = segment.get("script", "")
        scenes = segment.get("scenes", [])
        
        if not script:
            print(f"⚠️ Empty script for segment {i+1}, skipping")
            continue
        
        segment_name = f"longform_seg_{i}_{timestamp}"
        
        # 1. Generate audio for this segment
        audio_path = output_dir / f"{segment_name}_audio.wav"
        if not generate_audio(script, audio_path, lang="ru"):
            print(f"❌ Audio failed for segment {i+1}")
            continue
        
        # 2. Fetch visual assets
        assets_dir = output_dir / f"assets_seg_{i}"
        assets_dir.mkdir(exist_ok=True)
        
        # Convert scenes to proper format
        scene_list = []
        for j, scene in enumerate(scenes):
            kw = scene.get("keyword", "technology future")
            scene_list.append({
                "image": f"seg{i}_scene{j}",
                "keyword": kw
            })
        
        resolved_scenes = generate_pexels_assets(scene_list, assets_dir, style="impact")
        
        if not resolved_scenes:
            # Use B-roll as backup
            print(f"⚠️ Using B-roll for segment {i+1}")
            clips = semantic_search_broll(script[:100], BROLL_DIR, num_clips=5)
            for j, clip in enumerate(clips):
                resolved_scenes.append({
                    "image": str(clip),
                    "resolved_path": str(clip),
                    "keyword": "documentary footage"
                })
        
        # 3. Assemble segment video
        raw_video = output_dir / f"{segment_name}_raw.mp4"
        assemble_hybrid_video(audio_path, resolved_scenes, raw_video, style="impact")
        
        # 4. Add subtitles
        final_segment = output_dir / f"{segment_name}_final.mp4"
        if add_subtitles(raw_video, final_segment, lang="ru", style="impact"):
            segment_videos.append(final_segment)
        else:
            segment_videos.append(raw_video)
        
        print(f"✅ Segment {i+1} complete: {segment_videos[-1]}")
    
    if not segment_videos:
        print("❌ No segments produced")
        return None
    
    # 5. Concatenate all segments
    print(f"\n🔗 Concatenating {len(segment_videos)} segments...")
    
    concat_file = output_dir / "concat_list.txt"
    with open(concat_file, "w") as f:
        for video in segment_videos:
            f.write(f"file '{video.name}'\n")
    
    final_output = output_dir / f"{LONGFORM_CONFIG['output_prefix']}_{timestamp}_final.mp4"
    
    import subprocess
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_file),
        "-c", "copy", str(final_output)
    ], check=True, capture_output=True, cwd=str(output_dir))
    
    print(f"✅ DOCUMENTARY COMPLETE: {final_output}")
    
    # 6. Generate chapter file for YouTube
    chapters = data.get("youtube_chapters", [])
    if chapters:
        chapters_file = output_dir / f"{LONGFORM_CONFIG['output_prefix']}_{timestamp}_chapters.txt"
        with open(chapters_file, "w") as f:
            f.write("\n".join(chapters))
        print(f"📝 YouTube chapters saved: {chapters_file}")
    
    # Cleanup intermediate files
    for seg in segment_videos:
        if seg.exists() and seg != final_output:
            seg.unlink()
    
    return final_output

# =============================================================================
#                           MAIN PIPELINE
# =============================================================================

def run_longform_production(topic: str = None) -> Optional[Path]:
    """
    Full long-form documentary production pipeline.
    Call from scheduler or manually.
    """
    print("\n" + "="*60)
    print("🎬 LONG-FORM DOCUMENTARY PRODUCTION")
    print("="*60)
    
    timestamp = datetime.now().strftime('%Y-%m-%d')
    
    # Auto-generate topic if not provided
    if not topic:
        topics = [
            "Искусственный интеллект в 2026: Полная картина",
            "Квантовые компьютеры: Технология будущего уже здесь",
            "Космическая гонка 2026: Марс, Луна и дальше",
            "Биотехнологии: Как мы победим болезни",
            "Энергетическая революция: Термоядерный синтез",
            "Автономные системы: Роботы среди нас"
        ]
        import random
        topic = random.choice(topics)
    
    print(f"📌 Topic: {topic}")
    
    # 1. Deep Research
    data = deep_research_with_council(topic)
    if not data:
        data = fallback_research(topic)
    
    if not data:
        print("❌ Research failed, aborting production")
        return None
    
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
        
        # Notify via MCP Agent Mail
        try:
            from agent_mail_client import AgentMailClient
            client = AgentMailClient()
            client.send(
                to="PinkLake",
                subject="🎬 Documentary Ready",
                body=f"New 30-min documentary produced:\n\nTopic: {topic}\nPath: {final_video}\n\nToken usage: {TRACKER.usage}"
            )
        except:
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
