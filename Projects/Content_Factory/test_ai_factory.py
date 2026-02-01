#!/usr/bin/env python3
"""
AI Content Factory - Quick Test
Tests all 4 phases without requiring API keys (uses fallbacks)
"""
import sys
import logging
from pathlib import Path

# Setup paths
SRC_DIR = Path(__file__).parent / "src"
sys.path.insert(0, str(SRC_DIR / "pipeline"))

from ai_content_factory import AIContentFactory

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def test_factory():
    """Test AI Content Factory with fallbacks."""
    print("🚀 AI CONTENT FACTORY - Quick Test")
    print("=" * 60)
    
    # Initialize (all AI disabled for testing)
    factory = AIContentFactory(
        use_ai_music=False,   # Will use local library
        use_ai_video=False,   # Not needed for test
        use_ai_voice=False    # Will skip voice generation
    )
    
    # Test script
    script = """
    Искусственный интеллект революционизирует создание контента.
    Новые технологии позволяют генерировать музыку, видео и голос автоматически.
    Будущее контент-производства уже здесь.
    """
    
    output_dir = Path("/tmp/ai_factory_test")
    
    print(f"\n📝 Script: {script[:100]}...")
    print(f"📂 Output: {output_dir}")
    print("\n🎬 Starting production pipeline...\n")
    
    assets = factory.create_video_content(
        script=script,
        lang="ru",
        style="impact",
        duration=20,
        output_dir=output_dir
    )
    
    print("\n" + "=" * 60)
    print("✅ PRODUCTION COMPLETE")
    print("=" * 60)
    print(f"\nGenerated {len(assets)} assets:\n")
    
    for asset_type, path in assets.items():
        exists = "✅" if (isinstance(path, Path) and path.exists()) else "❌"
        print(f"  {exists} {asset_type}: {path}")
    
    print("\n💡 To enable AI features:")
    print("  1. Get API keys (Suno, ElevenLabs, Runway)")
    print("  2. Add to .env file")
    print("  3. Set USE_AI_MUSIC=true, USE_AI_VOICE=true, etc.")
    print("\n📚 See: .env.ai_template for configuration\n")

if __name__ == "__main__":
    test_factory()
