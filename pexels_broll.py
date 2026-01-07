#!/usr/bin/env python3
"""
Pexels Semantic B-Roll Search
Uses Sentence Transformers for semantic search on Pexels videos
"""

import os
import json
import requests
from pathlib import Path
from typing import List, Optional

# Pexels API
def search_pexels_videos(query: str, per_page: int = 5) -> List[dict]:
    """Search Pexels for videos matching query"""
    api_key = os.getenv("PEXELS_API_KEY", "")
    if not api_key:
        print("⚠️ PEXELS_API_KEY not set. Using mock data.")
        return []
    
    url = "https://api.pexels.com/videos/search"
    headers = {"Authorization": api_key}
    params = {"query": query, "per_page": per_page, "orientation": "portrait"}
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("videos", [])
    except Exception as e:
        print(f"❌ Pexels search failed: {e}")
        return []

def download_video(url: str, output_path: Path) -> bool:
    """Download video from URL (skip if exists)"""
    if output_path.exists() and output_path.stat().st_size > 0:
        print(f"⏭ Skip download (exists): {output_path}")
        return True
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(output_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"✅ Downloaded: {output_path}")
        return True
    except Exception as e:
        print(f"❌ Download failed: {e}")
        return False

def get_best_video_file(video: dict, quality: str = "hd") -> Optional[str]:
    """Get best quality video file URL"""
    files = video.get("video_files", [])
    
    # Sort by quality preference
    for f in files:
        f_quality = f.get("quality") or ""
        if quality in str(f_quality).lower():
            return f.get("link")
    
    # Fallback to first file
    if files:
        return files[0].get("link")
    return None

def semantic_search_broll(text: str, output_dir: Path, num_clips: int = 3) -> List[Path]:
    """
    Extract keywords from text and search for relevant B-Roll
    Uses simple keyword extraction (for full semantic, add sentence-transformers)
    """
    print(f"🎬 Searching B-Roll for: {text[:50]}...")
    
    # Simple keyword extraction (можно заменить на NLP)
    keywords = extract_keywords(text)
    print(f"📝 Keywords: {keywords}")
    
    downloaded = []
    output_dir.mkdir(exist_ok=True)
    
    for i, keyword in enumerate(keywords[:num_clips]):
        videos = search_pexels_videos(keyword, per_page=1)
        if videos:
            video = videos[0]
            url = get_best_video_file(video, "hd")
            if url:
                output_path = output_dir / f"broll_{i}_{keyword}.mp4"
                if download_video(url, output_path):
                    downloaded.append(output_path)
    
    print(f"✅ Downloaded {len(downloaded)} B-Roll clips")
    return downloaded

def extract_keywords(text: str) -> List[str]:
    """Extract keywords from text (simple version)"""
    # Удаляем стоп-слова и выбираем существительные
    stop_words = {"я", "и", "с", "на", "в", "для", "это", "the", "a", "an", "is", "are", "was", "were", "i", "am", "we", "you"}
    
    words = text.lower().split()
    keywords = [w for w in words if len(w) > 3 and w not in stop_words]
    
    # Уникальные ключевые слова
    seen = set()
    unique = []
    for w in keywords:
        if w not in seen:
            seen.add(w)
            unique.append(w)
    
    return unique[:5]

if __name__ == "__main__":
    # Test search
    ROOT_DIR = Path(__file__).parent.resolve()
    BROLL_DIR = ROOT_DIR / "broll"
    
    test_text = "Artificial intelligence and neural networks are changing the world of technology"
    clips = semantic_search_broll(test_text, BROLL_DIR)
    print(f"Downloaded clips: {clips}")
