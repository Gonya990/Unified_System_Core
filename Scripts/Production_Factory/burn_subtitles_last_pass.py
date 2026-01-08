#!/usr/bin/env python3
import os
import sys
from pathlib import Path
from orchestrator_v3_no_face import add_subtitles

ROOT_DIR = Path(__file__).parent.resolve()
OUTPUT_DIR = ROOT_DIR / "outputs"

def burn_all():
    # 1. Russian
    ru_video = OUTPUT_DIR / "ai_council_ru_final.mp4"
    ru_final = OUTPUT_DIR / "ai_council_ru_motivaider.mp4"
    if ru_video.exists():
        print(f"🔥 Burning Subtitles for Russian Video: {ru_video}")
        add_subtitles(ru_video, ru_final, lang="ru")
    
    # 2. English
    en_video = OUTPUT_DIR / "ai_council_en_final.mp4"
    en_final = OUTPUT_DIR / "ai_council_en_motivaider.mp4"
    if en_video.exists():
        print(f"🔥 Burning Subtitles for English Video: {en_video}")
        add_subtitles(en_video, en_final, lang="en")

if __name__ == "__main__":
    burn_all()
