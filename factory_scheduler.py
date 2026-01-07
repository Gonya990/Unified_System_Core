#!/usr/bin/env python3
import sys
from pathlib import Path
from datetime import datetime

# Setup paths
ROOT_DIR = Path(__file__).parent.resolve()
sys.path.append(str(ROOT_DIR))

# Import logic
from orchestrator_v3_no_face import run_no_face_pipeline
from insta_uploader import upload_reel
from daily_researcher import run_daily_research, generate_vision_assets

# Configuration
REELS_AUTO_UPLOAD = True 

def run_factory_production():
    """
    Main Daily Production Loop
    1. Research Trends (Live Google News)
    2. Write Viral Script (LLM)
    3. Generate Visual Assets (DALL-E 3)
    4. Produce Video (Orchestrator)
    5. Publish to Instagram
    """
    day_str = datetime.now().strftime('%Y-%m-%d')
    print(f"🏭 --- Factory Run: {day_str} ---")
    
    # 1. Research & Scripting
    print("🧠 Starting Daily Research Phase...")
    content_data = run_daily_research()
    
    if not content_data:
        print("❌ Research failed. Aborting production.")
        return

    print(f"✅ Topic Selected: {content_data['selected_topic']}")
    
    # 2. Asset Generation
    print("🎨 Starting Asset Generation Phase...")
    assets_dir = ROOT_DIR / "assets" / day_str
    
    # Generate images and get updated scenes with paths
    scenes_with_assets = generate_vision_assets(content_data['scenes'], assets_dir)
    
    # Prepare scenes for orchestrator (map resolved_path to image)
    final_scenes = []
    for scene in scenes_with_assets:
        if scene.get("resolved_path"):
            final_scenes.append({
                "image": scene["resolved_path"], # Absolute path to generated image
                "keyword": scene["keyword"]
            })
            
    if len(final_scenes) < 5:
        print(f"❌ Critical Asset Failure. Only {len(final_scenes)} assets generated. Aborting.")
        return

    # 3. Production Pipeline
    output_name = f"factory_daily_{day_str.replace('-', '')}"
    print(f"🎬 Starting Production Phase: {output_name}")
    
    final_video_path = run_no_face_pipeline(
        text=content_data['script_ru'], 
        lang="ru", 
        output_name=output_name, 
        scenes=final_scenes
    )
    
    # 4. Verification & Upload
    if final_video_path and final_video_path.exists():
        print(f"✅ FINAL VIDEO READY: {final_video_path}")
        
        if REELS_AUTO_UPLOAD:
            print("📤 Initializing Default Upload...")
            caption = (
                f"{content_data['selected_topic']}\n\n"
                f"{content_data.get('description', '')}\n\n"
                "#AI #Future #2026 #TechNews #Innovation"
            )
            success = upload_reel(str(final_video_path), caption)
            if success:
                print("🏆 Reel published successfully!")
            else:
                print("⚠️ Upload failed. Check logs.")
    else:
        print("❌ Video generation failed.")

if __name__ == "__main__":
    run_factory_production()
