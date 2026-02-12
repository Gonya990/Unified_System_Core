import sys
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path('/home/gonya/Unified_System_Core')
SRC_DIR = Path('/home/gonya/Unified_System_Core/Projects/Content_Factory/src')
load_dotenv(ROOT_DIR / '.env')
load_dotenv(ROOT_DIR / 'Projects/AI_Core/.env', override=True)
sys.path.insert(0, str(SRC_DIR / 'researcher'))
from datetime import datetime

from daily_researcher import generate_dalle_assets

day_str = datetime.now().strftime('%Y-%m-%d')
assets_dir = ROOT_DIR / 'Local_Dev' / 'Media' / 'legacy_wealth_v3' / day_str

missing = [{'image': 'scene_6_cta', 'keyword': 'mountain peak sunrise triumph success vertical cinematic'}]
print('Generating scene_6_cta...')
generate_dalle_assets(missing, assets_dir, style='cinematic_impact')
print('Done.')
