#!/usr/bin/env python3
"""
Advanced Subtitle Styling - Impact/Karaoke effects like SeTka Project
"""

import logging
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class SubtitleWord:
    """Single word with timing."""

    text: str
    start: float
    end: float


@dataclass
class SubtitleSegment:
    """Subtitle segment with words."""

    text: str
    start: float
    end: float
    words: list[SubtitleWord]


class AdvancedSubtitles:
    """Generate subtitles with advanced styling (karaoke, impact, emoji)."""

    STYLES = {
        "impact": {
            "font": "Impact",
            "font_size": 80,
            "font_color": "#FFFFFF",
            "outline_color": "#000000",
            "outline_width": 4,
            "shadow": True,
            "bold": True,
            "uppercase": True,
            "position": "center",  # center, top, bottom
            "animation": "fade_in",  # fade_in, slide_up, scale_bounce
        },
        "karaoke": {
            "font": "Montserrat-Bold",
            "font_size": 60,
            "font_color": "#FFFFFF",
            "highlight_color": "#FFD700",  # Gold highlight
            "outline_color": "#000000",
            "outline_width": 3,
            "position": "bottom",
            "word_by_word": True,  # Highlight each word
            "animation": "karaoke",
        },
        "cartoon": {
            "font": "Comic Sans MS",
            "font_size": 70,
            "font_color": "#FFFF00",  # Yellow
            "outline_color": "#FF00FF",  # Magenta outline
            "outline_width": 5,
            "shadow": True,
            "bounce": True,
            "position": "bottom",
        },
        "minimal": {
            "font": "Helvetica-Bold",
            "font_size": 48,
            "font_color": "#FFFFFF",
            "outline_color": "#000000",
            "outline_width": 2,
            "position": "bottom",
            "animation": "fade",
        },
    }

    def __init__(self, style: str = "impact"):
        """
        Args:
            style: Subtitle style (impact, karaoke, cartoon, minimal)
        """
        self.style_name = style
        self.style = self.STYLES.get(style, self.STYLES["impact"])

    def generate_srt(self, segments: list[SubtitleSegment], output_path: Path, add_emoji: bool = True) -> Path:
        """
        Generate SRT subtitle file.

        Args:
            segments: List of subtitle segments with timing
            output_path: Where to save SRT file
            add_emoji: Auto-add emoji based on content

        Returns:
            Path to SRT file
        """
        srt_content = []

        for i, segment in enumerate(segments, start=1):
            # Format timestamps
            start_time = self._format_timestamp(segment.start)
            end_time = self._format_timestamp(segment.end)

            # Process text
            text = segment.text

            if self.style.get("uppercase"):
                text = text.upper()

            if add_emoji:
                text = self._add_emoji(text)

            # SRT block
            srt_content.append(f"{i}")
            srt_content.append(f"{start_time} --> {end_time}")
            srt_content.append(text)
            srt_content.append("")  # Blank line

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text("\n".join(srt_content), encoding="utf-8")

        logger.info(f"✅ SRT subtitle saved: {output_path}")
        return output_path

    def generate_ass(
        self,
        segments: list[SubtitleSegment],
        output_path: Path,
        video_width: int = 1920,
        video_height: int = 1080,
    ) -> Path:
        """
        Generate ASS subtitle file with advanced styling.

        Args:
            segments: List of subtitle segments
            output_path: Where to save ASS file
            video_width: Video width for positioning
            video_height: Video height for positioning

        Returns:
            Path to ASS file
        """
        # ASS header
        ass_content = self._generate_ass_header(video_width, video_height)

        # Events
        ass_content.append("[Events]")
        ass_content.append("Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text")

        for segment in segments:
            start_time = self._format_ass_timestamp(segment.start)
            end_time = self._format_ass_timestamp(segment.end)

            text = segment.text

            if self.style.get("uppercase"):
                text = text.upper()

            # Add effects
            effect = ""
            if self.style.get("animation") == "karaoke" and segment.words:
                # Word-by-word karaoke effect
                text = self._generate_karaoke_text(segment.words)
            elif self.style.get("animation") == "scale_bounce":
                effect = "Bounce"

            ass_content.append(f"Dialogue: 0,{start_time},{end_time},Default,,0,0,0,{effect},{text}")

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text("\n".join(ass_content), encoding="utf-8")

        logger.info(f"✅ ASS subtitle saved: {output_path}")
        return output_path

    def _generate_ass_header(self, width: int, height: int) -> list[str]:
        """Generate ASS file header with style definitions."""
        pos_y_map = {"top": 50, "center": height // 2, "bottom": height - 100}

        pos_y = pos_y_map.get(self.style.get("position", "bottom"), height - 100)

        return [
            "[Script Info]",
            "Title: Generated Subtitles",
            "ScriptType: v4.00+",
            f"PlayResX: {width}",
            f"PlayResY: {height}",
            "",
            "[V4+ Styles]",
            "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
            f"Style: Default,{self.style['font']},{self.style['font_size']},{self._color_to_ass(self.style['font_color'])},{self._color_to_ass(self.style.get('highlight_color', '#FFFFFF'))},{self._color_to_ass(self.style['outline_color'])},&H00000000,-1,0,0,0,100,100,0,0,1,{self.style['outline_width']},{3 if self.style.get('shadow') else 0},2,10,10,{pos_y},1",
            "",
        ]

    def _color_to_ass(self, hex_color: str) -> str:
        """Convert hex color to ASS format (&HAABBGGRR)."""
        hex_color = hex_color.lstrip("#")
        r, g, b = (
            int(hex_color[0:2], 16),
            int(hex_color[2:4], 16),
            int(hex_color[4:6], 16),
        )
        return f"&H00{b:02X}{g:02X}{r:02X}"

    def _format_timestamp(self, seconds: float) -> str:
        """Format seconds to SRT timestamp (00:00:00,000)."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

    def _format_ass_timestamp(self, seconds: float) -> str:
        """Format seconds to ASS timestamp (0:00:00.00)."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = seconds % 60
        return f"{hours}:{minutes:02d}:{secs:05.2f}"

    def _generate_karaoke_text(self, words: list[SubtitleWord]) -> str:
        """Generate ASS karaoke effect for word-by-word highlighting."""
        karaoke_tags = []

        for word in words:
            duration = int((word.end - word.start) * 100)  # Centiseconds
            karaoke_tags.append(f"{{\\k{duration}}}{word.text}")

        return " ".join(karaoke_tags)

    def _add_emoji(self, text: str) -> str:
        """Auto-add emoji based on keywords."""
        emoji_map = {
            "AI": "🤖",
            "future": "🚀",
            "breakthrough": "💡",
            "warning": "⚠️",
            "crisis": "🚨",
            "money": "💰",
            "technology": "⚡",
            "robot": "🤖",
            "brain": "🧠",
            "computer": "💻",
            "innovation": "✨",
            "question": "❓",
            "amazing": "🔥",
        }

        text_lower = text.lower()
        for keyword, emoji in emoji_map.items():
            if keyword in text_lower and emoji not in text:
                # Add emoji at end of sentence
                text = f"{text} {emoji}"
                break

        return text


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Test subtitle generation
    segments = [
        SubtitleSegment(
            text="Welcome to the future of AI",
            start=0.0,
            end=3.0,
            words=[
                SubtitleWord("Welcome", 0.0, 0.5),
                SubtitleWord("to", 0.5, 0.7),
                SubtitleWord("the", 0.7, 0.9),
                SubtitleWord("future", 0.9, 1.5),
                SubtitleWord("of", 1.5, 1.7),
                SubtitleWord("AI", 1.7, 2.0),
            ],
        )
    ]

    gen = AdvancedSubtitles(style="impact")

    srt_path = Path("/tmp/test_subs.srt")
    gen.generate_srt(segments, srt_path)

    ass_path = Path("/tmp/test_subs.ass")
    gen.generate_ass(segments, ass_path)

    print(f"Generated: {srt_path}, {ass_path}")
