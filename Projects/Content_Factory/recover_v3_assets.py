import sys
from pathlib import Path

from dotenv import load_dotenv

# Setup paths
ROOT_DIR = Path('/home/gonya/Unified_System_Core')
SRC_DIR = Path('/home/gonya/Unified_System_Core/Projects/Content_Factory/src')

load_dotenv(ROOT_DIR / '.env')
load_dotenv(ROOT_DIR / 'Projects/AI_Core/.env', override=True)

sys.path.insert(0, str(SRC_DIR / 'researcher'))
from daily_researcher import generate_dalle_assets


def recover():
    print("🚑 RECOVERY MODE: Checking for missing V3 assets...")

    day_str = datetime.now().strftime('%Y-%m-%d')
    assets_dir = ROOT_DIR / "Local_Dev" / "Media" / "legacy_wealth_v3" / day_str

    all_scenes = [
        {'image': 'scene_1_hook', 'keyword': 'business man laptop city office cinematic handheld'},
        {'image': 'scene_2_trump_kiyosaki', 'keyword': 'luxury wealth gold coins assets success'},
        {'image': 'scene_3_ai_core', 'keyword': 'tech server room blue light data abstract'},
        {'image': 'scene_4_orchestrator', 'keyword': 'epic orchestra conductor silhouette stage lighting'},
        {'image': 'scene_5_sovereign_living', 'keyword': 'modern luxury mansion pool aerial cinematic'},
        {'image': 'scene_6_cta', 'keyword': 'mountain peak sunrise triumph success'}
    ]

    missing = []
    for s in all_scenes:
        expected_path = assets_dir / f"{s['image']}.jpg"
        if not expected_path.exists():
            print(f"❌ Missing: {s['image']}")
            missing.append(s)
        else:
            print(f"✅ Exists: {s['image']}")

    if missing:
        print(f"🎨 Generating {len(missing)} missing assets via DALL-E...")
        try:
            generate_dalle_assets(missing, assets_dir, style="cinematic_impact")
            print("✅ Recovery Complete.")
        except Exception as e:
            print(f"❌ Recovery Failed: {e}")
    else:
        print("🎉 All assets present.")

if __name__ == '__main__':
    from datetime import datetime
    recover()
