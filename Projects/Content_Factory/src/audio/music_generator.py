#!/usr/bin/env python3
"""
Music Generator for Content Factory
Integrates Suno AI API + Royalty-free library fallback
"""
import os
import random
import logging
from pathlib import Path
from typing import Optional, List
import requests

logger = logging.getLogger(__name__)

# Royalty-free music library (local fallback)
ROYALTY_FREE_LIBRARY = Path(__file__).parent.parent.parent / "assets" / "music"

# Suno API configuration
SUNO_API_KEY = os.getenv("SUNO_API_KEY")
SUNO_BASE_URL = "https://api.suno.ai/v1"

class MusicGenerator:
    """Generate background music using Suno AI or local library."""
    
    def __init__(self, use_ai: bool = True):
        self.use_ai = use_ai and bool(SUNO_API_KEY)
        if not self.use_ai:
            logger.warning("Suno AI disabled or API key missing. Using local library.")
    
    def generate_music(
        self,
        mood: str = "upbeat",
        duration: int = 60,
        genre: str = "electronic",
        output_path: Optional[Path] = None
    ) -> Path:
        """
        Generate background music.
        
        Args:
            mood: Mood descriptor (upbeat, calm, dramatic, mysterious)
            duration: Target duration in seconds
            genre: Music genre (electronic, ambient, cinematic)
            output_path: Where to save generated music
        
        Returns:
            Path to music file
        """
        if self.use_ai:
            try:
                return self._generate_suno(mood, duration, genre, output_path)
            except Exception as e:
                logger.error(f"Suno generation failed: {e}. Falling back to local library.")
        
        return self._get_royalty_free(mood, duration, genre)
    
    def _generate_suno(
        self,
        mood: str,
        duration: int,
        genre: str,
        output_path: Optional[Path]
    ) -> Path:
        """Generate music using Suno AI API."""
        headers = {
            "Authorization": f"Bearer {SUNO_API_KEY}",
            "Content-Type": "application/json"
        }
        
        # Suno prompt engineering
        prompt = f"{mood} {genre} instrumental background music, no vocals, {duration} seconds"
        
        payload = {
            "prompt": prompt,
            "duration": duration,
            "instrumental": True,
            "genre": genre
        }
        
        logger.info(f"🎵 Generating Suno music: {prompt}")
        
        response = requests.post(
            f"{SUNO_BASE_URL}/generate",
            json=payload,
            headers=headers,
            timeout=60
        )
        response.raise_for_status()
        
        result = response.json()
        audio_url = result.get("audio_url")
        
        if not audio_url:
            raise ValueError("Suno API returned no audio URL")
        
        # Download generated audio
        audio_response = requests.get(audio_url, timeout=30)
        audio_response.raise_for_status()
        
        if not output_path:
            output_path = Path(f"/tmp/suno_{mood}_{genre}_{duration}s.mp3")
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(audio_response.content)
        
        logger.info(f"✅ Suno music saved: {output_path}")
        return output_path
    
    def _get_royalty_free(
        self,
        mood: str,
        duration: int,
        genre: str
    ) -> Path:
        """Get royalty-free music from local library."""
        ROYALTY_FREE_LIBRARY.mkdir(parents=True, exist_ok=True)
        
        # Create mood-based subdirectories
        mood_map = {
            "upbeat": "energetic",
            "calm": "ambient",
            "dramatic": "cinematic",
            "mysterious": "dark"
        }
        
        mood_dir = ROYALTY_FREE_LIBRARY / mood_map.get(mood, "ambient")
        mood_dir.mkdir(exist_ok=True)
        
        # Check for existing tracks
        tracks = list(mood_dir.glob("*.mp3"))
        
        if tracks:
            selected_track = random.choice(tracks)
            logger.info(f"📀 Using local track: {selected_track.name}")
            return selected_track
        
        # If no local tracks, create a placeholder
        logger.warning(f"No royalty-free tracks found in {mood_dir}. Using silence.")
        placeholder = mood_dir / f"{mood}_placeholder.mp3"
        
        # Generate silent MP3 using ffmpeg
        import subprocess
        subprocess.run([
            "ffmpeg", "-f", "lavfi", "-i", f"anullsrc=r=44100:cl=stereo",
            "-t", str(duration), "-y", str(placeholder)
        ], check=True, capture_output=True)
        
        return placeholder
    
    def get_recommended_mood(self, script_text: str) -> str:
        """Analyze script text to recommend music mood."""
        text_lower = script_text.lower()
        
        # Keyword-based mood detection
        if any(word in text_lower for word in ["breakthrough", "innovation", "future", "amazing"]):
            return "upbeat"
        elif any(word in text_lower for word in ["meditation", "calm", "peaceful", "nature"]):
            return "calm"
        elif any(word in text_lower for word in ["danger", "crisis", "war", "threat"]):
            return "dramatic"
        elif any(word in text_lower for word in ["mystery", "secret", "unknown", "hidden"]):
            return "mysterious"
        
        return "upbeat"  # Default


if __name__ == "__main__":
    # Test
    logging.basicConfig(level=logging.INFO)
    gen = MusicGenerator(use_ai=False)
    
    track = gen.generate_music(
        mood="upbeat",
        duration=30,
        genre="electronic"
    )
    print(f"Generated: {track}")
