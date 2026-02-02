#!/usr/bin/env python3
"""
AI Content Factory Integration Layer
Combines Music, Video, Voice, and Subtitles into production pipeline
"""
import logging
import sys
from pathlib import Path

# Setup paths
SRC_DIR = Path(__file__).parent.parent.resolve()
sys.path.append(str(SRC_DIR / "audio"))
sys.path.append(str(SRC_DIR / "video"))

from advanced_subtitles import AdvancedSubtitles, SubtitleSegment, SubtitleWord
from ai_video_generator import VideoGenerator
from music_generator import MusicGenerator
from voice_generator import VoiceGenerator

logger = logging.getLogger(__name__)


class AIContentFactory:
    """Unified AI content production pipeline."""

    def __init__(
        self,
        use_ai_music: bool = True,
        use_ai_video: bool = True,
        use_ai_voice: bool = True,
        video_provider: str = "runway"
    ):
        """
        Args:
            use_ai_music: Use Suno AI for music (fallback to local library)
            use_ai_video: Use AI video generation for B-roll
            use_ai_voice: Use ElevenLabs for voiceover
            video_provider: 'runway', 'luma', or 'kling'
        """
        self.music_gen = MusicGenerator(use_ai=use_ai_music)
        self.voice_gen = VoiceGenerator() if use_ai_voice else None
        self.video_gen = VideoGenerator(provider=video_provider) if use_ai_video else None
        self.subtitle_gen = AdvancedSubtitles(style="impact")

    def create_video_content(
        self,
        script: str,
        lang: str = "ru",
        style: str = "impact",
        duration: int = 60,
        output_dir: Path = Path("/tmp/content_factory")
    ) -> dict[str, Path]:
        """
        Generate complete video content with all AI enhancements.

        Args:
            script: Video script text
            lang: Language code (ru, en, he)
            style: Visual style (impact, cartoon, cinematic)
            duration: Target duration in seconds
            output_dir: Output directory

        Returns:
            Dictionary with paths to generated assets
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        assets = {}

        logger.info(f"🎬 Starting AI Content Factory pipeline ({style} style, {duration}s)")

        # 1. Generate voiceover (with emotion detection)
        emotion = self._detect_emotion(script)
        logger.info(f"🎭 Detected emotion: {emotion}")

        if self.voice_gen:
            voice_path = self.voice_gen.generate_speech(
                text=script,
                voice_name="Antoni",
                emotion=emotion,
                output_path=output_dir / "voiceover.mp3"
            )
            if voice_path:
                assets["voiceover"] = voice_path
                logger.info(f"✅ Voiceover: {voice_path}")

        # 2. Generate background music (matching mood)
        mood = self._emotion_to_mood(emotion)
        music_path = self.music_gen.generate_music(
            mood=mood,
            duration=duration,
            genre=self._style_to_genre(style),
            output_path=output_dir / "background_music.mp3"
        )
        assets["music"] = music_path
        logger.info(f"✅ Music: {music_path}")

        # 3. Generate AI B-roll clips (if enabled)
        if self.video_gen:
            scenes = self._extract_scenes(script)
            video_clips = []

            for i, scene in enumerate(scenes[:5]):  # Max 5 clips
                clip_path = self.video_gen.generate_video(
                    prompt=scene["description"],
                    duration=min(scene["duration"], 10),
                    style=style,
                    output_path=output_dir / f"broll_{i+1}.mp4"
                )
                if clip_path:
                    video_clips.append(clip_path)
                    logger.info(f"✅ B-roll {i+1}: {clip_path}")

            if video_clips:
                assets["broll_clips"] = video_clips

        # 4. Generate advanced subtitles
        segments = self._script_to_segments(script, duration)

        # SRT for simple players
        srt_path = output_dir / "subtitles.srt"
        self.subtitle_gen.generate_srt(segments, srt_path, add_emoji=True)
        assets["subtitles_srt"] = srt_path
        logger.info(f"✅ SRT subtitles: {srt_path}")

        # ASS for advanced styling
        ass_path = output_dir / "subtitles.ass"
        self.subtitle_gen.generate_ass(segments, ass_path)
        assets["subtitles_ass"] = ass_path
        logger.info(f"✅ ASS subtitles: {ass_path}")

        logger.info(f"🎉 AI Content Factory complete! Generated {len(assets)} assets.")
        return assets

    def _detect_emotion(self, text: str) -> str:
        """Detect emotion from script text."""
        text_lower = text.lower()

        if any(word in text_lower for word in ["breakthrough", "amazing", "incredible", "wow"]):
            return "excited"
        elif any(word in text_lower for word in ["danger", "crisis", "warning", "threat"]):
            return "dramatic"
        elif any(word in text_lower for word in ["mystery", "secret", "unknown", "hidden"]):
            return "mysterious"
        elif any(word in text_lower for word in ["sad", "tragedy", "loss", "death"]):
            return "sad"
        elif any(word in text_lower for word in ["calm", "peaceful", "meditation", "nature"]):
            return "calm"

        return "neutral"

    def _emotion_to_mood(self, emotion: str) -> str:
        """Map emotion to music mood."""
        mood_map = {
            "excited": "upbeat",
            "dramatic": "dramatic",
            "mysterious": "mysterious",
            "sad": "calm",
            "calm": "calm",
            "neutral": "upbeat"
        }
        return mood_map.get(emotion, "upbeat")

    def _style_to_genre(self, style: str) -> str:
        """Map visual style to music genre."""
        genre_map = {
            "impact": "electronic",
            "cartoon": "upbeat",
            "cinematic": "cinematic",
            "minimal": "ambient"
        }
        return genre_map.get(style, "electronic")

    def _extract_scenes(self, script: str) -> list[dict]:
        """Extract scene descriptions from script."""
        # Simple sentence-based scene extraction
        sentences = script.split(". ")
        scenes = []

        for sentence in sentences[:5]:  # Max 5 scenes
            if len(sentence.strip()) > 20:
                scenes.append({
                    "description": sentence.strip(),
                    "duration": 5  # Default 5s per scene
                })

        return scenes

    def _script_to_segments(self, script: str, total_duration: int) -> list[SubtitleSegment]:
        """Convert script to subtitle segments with timing."""
        sentences = [s.strip() + "." for s in script.split(".") if s.strip()]

        if not sentences:
            return []

        # Distribute duration evenly across sentences
        duration_per_sentence = total_duration / len(sentences)
        segments = []

        current_time = 0.0
        for sentence in sentences:
            # Estimate words for karaoke
            words_list = sentence.split()
            word_duration = duration_per_sentence / len(words_list) if words_list else 0

            words = []
            word_time = current_time
            for word in words_list:
                words.append(SubtitleWord(
                    text=word,
                    start=word_time,
                    end=word_time + word_duration
                ))
                word_time += word_duration

            segments.append(SubtitleSegment(
                text=sentence,
                start=current_time,
                end=current_time + duration_per_sentence,
                words=words
            ))

            current_time += duration_per_sentence

        return segments


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    factory = AIContentFactory(
        use_ai_music=True,
        use_ai_video=False,  # Disable for testing
        use_ai_voice=False    # Disable for testing
    )

    test_script = """
    Искусственный интеллект меняет мир прямо сейчас.
    Новые технологии появляются каждый день.
    Будущее уже здесь, и оно удивительно.
    """

    assets = factory.create_video_content(
        script=test_script,
        lang="ru",
        style="impact",
        duration=15
    )

    print("\n✅ Generated assets:")
    for key, path in assets.items():
        print(f"  - {key}: {path}")
