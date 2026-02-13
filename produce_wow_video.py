import sys
from pathlib import Path

# Add src to path
SRC_DIR = Path(__file__).resolve().parent / "Projects/Content_Factory/src"
sys.path.append(str(SRC_DIR))

from pipeline.orchestrator_v4_advanced import run_advanced_pipeline

# 3 Scenes for a "wow" result
scenes = [
    {"keyword": "cyberpunk tokyo rainy night neon lights cinematic 8k"},
    {"keyword": "futuristic robotic hand typing on glass interface digital art"},
    {"keyword": "flying car over futuristic city sunset cinematic high detail"},
]

text = (
    "In the year 2077, Tokyo has transformed into a bioluminescent "
    "paradise. Technology and nature have finally merged, creating "
    "a world of infinite possibilities."
)

print("🚀 Starting PREMIUM Video Generation...")
run_advanced_pipeline(text=text, output_name="premium_tokyo_2077", scenes=scenes, style="impact")
