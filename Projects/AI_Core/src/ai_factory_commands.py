#!/usr/bin/env python3
"""
AI Factory Bot Commands - Telegram integration
Add these commands to ai_telegram_bot_v2.py
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from telegram import Update
    from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)


async def ai_music_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Generate background music using Suno AI."""
    user_id = update.effective_user.id
    if not db.is_approved(user_id):  # noqa: F821
        return

    if not context.args:
        await update.message.reply_text(
            "🎵 **Suno AI Music Generator**\n\n"
            "Usage: `/aimusic <mood> [genre] [duration]`\n\n"
            "**Moods:** upbeat, calm, dramatic, mysterious\n"
            "**Genres:** electronic, ambient, cinematic\n"
            "**Duration:** 30-180 seconds (default: 60)\n\n"
            "Example: `/aimusic upbeat electronic 45`",
            parse_mode="Markdown",
        )
        return

    mood = context.args[0]
    genre = context.args[1] if len(context.args) > 1 else "electronic"
    duration = int(context.args[2]) if len(context.args) > 2 else 60

    await update.message.reply_text(f"🎵 Generating {mood} {genre} music ({duration}s)...")

    try:
        import sys
        from pathlib import Path

        # Detect Unified_System_Core root
        CURRENT_FILE = Path(__file__).resolve()
        # ai_factory_commands.py is in Projects/AI_Core/src/
        UNIFIED_ROOT = CURRENT_FILE.parent.parent.parent.parent
        FACTORY_SRC = UNIFIED_ROOT / "Projects/Content_Factory/src"

        sys.path.append(str(FACTORY_SRC / "audio"))
        from music_generator import MusicGenerator

        gen = MusicGenerator(use_ai=True)
        music_path = gen.generate_music(mood=mood, duration=duration, genre=genre)

        if music_path and music_path.exists():
            with open(music_path, "rb") as audio_file:
                await update.message.reply_audio(
                    audio=audio_file, title=f"{mood.capitalize()} {genre}", performer="Suno AI"
                )
            await update.message.reply_text(f"✅ Music generated: {music_path.name}")
        else:
            await update.message.reply_text("❌ Failed to generate music")

    except Exception as e:
        logger.error(f"Music generation error: {e}")
        await update.message.reply_text(f"❌ Error: {e}")


async def ai_voice_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Generate voice using ElevenLabs."""
    user_id = update.effective_user.id
    if not db.is_approved(user_id):  # noqa: F821
        return

    if not context.args:
        await update.message.reply_text(
            "🎤 **ElevenLabs Voice Generator**\n\n"
            "Usage: `/aivoice <emotion> <text>`\n\n"
            "**Emotions:** excited, dramatic, mysterious, sad, calm, neutral\n\n"
            "Example: `/aivoice excited Welcome to the future of AI!`",
            parse_mode="Markdown",
        )
        return

    emotion = context.args[0]
    text = " ".join(context.args[1:])

    if not text:
        await update.message.reply_text("❌ Please provide text to speak")
        return

    await update.message.reply_text(f"🎤 Generating voice ({emotion})...")

    try:
        import sys
        from pathlib import Path

        # Detect Unified_System_Core root
        CURRENT_FILE = Path(__file__).resolve()
        UNIFIED_ROOT = CURRENT_FILE.parent.parent.parent.parent
        FACTORY_SRC = UNIFIED_ROOT / "Projects/Content_Factory/src"

        sys.path.append(str(FACTORY_SRC / "audio"))
        from voice_generator import VoiceGenerator

        gen = VoiceGenerator()
        voice_path = gen.generate_speech(text=text, voice_name="Antoni", emotion=emotion)

        if voice_path and voice_path.exists():
            with open(voice_path, "rb") as audio_file:
                await update.message.reply_voice(audio=audio_file)
            await update.message.reply_text(f"✅ Voice generated ({len(text)} chars)")
        else:
            await update.message.reply_text("❌ ElevenLabs API not configured")

    except Exception as e:
        logger.error(f"Voice generation error: {e}")
        await update.message.reply_text(f"❌ Error: {e}")


async def ai_subtitle_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Generate advanced subtitles."""
    user_id = update.effective_user.id
    if not db.is_approved(user_id):  # noqa: F821
        return

    if not context.args:
        await update.message.reply_text(
            "📝 **Advanced Subtitle Generator**\n\n"
            "Usage: `/aisub <style> <text>`\n\n"
            "**Styles:** impact, karaoke, cartoon, minimal\n\n"
            "Example: `/aisub impact AI is changing the world`",
            parse_mode="Markdown",
        )
        return

    style = context.args[0]
    text = " ".join(context.args[1:])

    if not text:
        await update.message.reply_text("❌ Please provide subtitle text")
        return

    await update.message.reply_text(f"📝 Generating {style} subtitles...")

    try:
        import sys
        from pathlib import Path

        # Detect Unified_System_Core root
        CURRENT_FILE = Path(__file__).resolve()
        UNIFIED_ROOT = CURRENT_FILE.parent.parent.parent.parent
        FACTORY_SRC = UNIFIED_ROOT / "Projects/Content_Factory/src"

        sys.path.append(str(FACTORY_SRC / "video"))
        from advanced_subtitles import AdvancedSubtitles, SubtitleSegment

        gen = AdvancedSubtitles(style=style)

        # Create simple segment
        segment = SubtitleSegment(text=text, start=0.0, end=5.0, words=[])

        output_dir = Path("/tmp/subs")
        output_dir.mkdir(exist_ok=True)

        srt_path = output_dir / "subtitle.srt"
        ass_path = output_dir / "subtitle.ass"

        gen.generate_srt([segment], srt_path, add_emoji=True)
        gen.generate_ass([segment], ass_path)

        # Send both files
        with open(srt_path, "rb") as srt_file:
            await update.message.reply_document(document=srt_file, filename=f"{style}_subtitle.srt")

        with open(ass_path, "rb") as ass_file:
            await update.message.reply_document(document=ass_file, filename=f"{style}_subtitle.ass")

        await update.message.reply_text(f"✅ Generated subtitles in {style} style\nFiles: SRT (simple) + ASS (styled)")

    except Exception as e:
        logger.error(f"Subtitle generation error: {e}")
        await update.message.reply_text(f"❌ Error: {e}")


# Add these to the commands_to_register dictionary:
# "aimusic": ai_music_command,
# "aivoice": ai_voice_command,
# "aisub": ai_subtitle_command,
