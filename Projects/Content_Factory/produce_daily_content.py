import sys
import os
import time
from pathlib import Path
from dotenv import load_dotenv

# Setup paths
ROOT_DIR = Path('/home/gonya/Unified_System_Core')
SRC_DIR = Path('/home/gonya/Unified_System_Core/Projects/Content_Factory/src')
sys.path.insert(0, str(SRC_DIR))
sys.path.insert(0, str(SRC_DIR / 'researcher'))
sys.path.insert(0, str(SRC_DIR / 'pipeline'))

# Load Core Modules
import scheduler
from daily_researcher import generate_vision_assets
import orchestrator_v3_no_face as orchestrator

load_dotenv(ROOT_DIR / '.env')
load_dotenv(ROOT_DIR / 'Projects/AI_Core/.env', override=True)

def run_production_cycle():
    print("🏭 CONTENT FACTORY: STARTING PRODUCTION CYCLE...")
    
    # 1. Get Plan
    plan = scheduler.get_daily_production_plan()
    print(f"📅 Today's Plan: {len(plan)} slots")
    
    for task in plan:
        lang = task['lang'].value
        slot = task['slot']
        print(f"\n🚀 Processing: {lang.upper()} ({slot}) ...")
        
        # 2. Mine Topic (Simulated for safety, would be real research in prod)
        topic = "Future of Business 2026" # Default
        
        # 3. Generate Content
        # We need a function to generate script based on Lang + Topic
        # For now, we reuse the Legacy Wealth logic but adapted for dynamic lang
        
        output_name = f"content_{slot}_{lang}"
        
        # (Placeholder for real generation logic, mapped to Orchestrator)
        # implementation details would go here...
        print(f"✅ {output_name} produced successfully (Simulation).")
        
        # 4. Upload
        if os.getenv('AUTOMATION_MODE') == 'True':
            print(f"📤 Uploading {output_name} to Telegram...")
            # Call telegram uploader
            # Call youtube uploader
            # Call insta uploader
            
    print("\n💤 Cycle Complete. Sleeping until next trigger.")

if __name__ == '__main__':
    run_production_cycle()
