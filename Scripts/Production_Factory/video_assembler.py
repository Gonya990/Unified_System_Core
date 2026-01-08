#!/usr/bin/env python3
"""
Video Assembler
Combines Avatar video with B-Roll clips for dynamic content
"""

from pathlib import Path
from typing import List
import subprocess  # nosec B404
import tempfile
import shutil

# Resolve absolute paths for tools to avoid B607
FFMPEG_BIN = shutil.which("ffmpeg")
FFPROBE_BIN = shutil.which("ffprobe")

if not FFMPEG_BIN or not FFPROBE_BIN:
    raise FileNotFoundError("ffmpeg or ffprobe not found in PATH")

def create_video_with_broll(
    avatar_video: Path,
    broll_clips: List[Path],
    output_path: Path,
    broll_interval: float = 5.0,  # Insert B-Roll every X seconds
    broll_duration: float = 2.0   # Duration of each B-Roll clip
) -> bool:
    """
    Create video with B-Roll insertions
    
    Args:
        avatar_video: Main avatar video path
        broll_clips: List of B-Roll video paths
        output_path: Output video path
        broll_interval: Seconds between B-Roll insertions
        broll_duration: Duration of each B-Roll clip
    
    Returns:
        True if successful
    """
    print(f"🎬 Assembling video with {len(broll_clips)} B-Roll clips...")
    
    if not broll_clips:
        # Just copy avatar if no B-Roll
        shutil.copy(avatar_video, output_path)
        return True
    
    # Get avatar video duration
    duration = get_video_duration(avatar_video)
    if duration <= 0:
        print("❌ Could not get video duration")
        return False
    
    # Create filter complex for ffmpeg
    # This is a simplified version - full implementation would use proper timeline editing
    try:
        # For now, just overlay B-Roll at specific intervals using concat
        # First, trim B-Roll clips to desired duration
        trimmed_brolls = []
        for i, broll in enumerate(broll_clips):
            trimmed = Path(tempfile.gettempdir()) / f"broll_trimmed_{i}.mp4"
            trim_video(broll, trimmed, broll_duration)
            if trimmed.exists():
                trimmed_brolls.append(trimmed)
        
        if not trimmed_brolls:
            shutil.copy(avatar_video, output_path)
            return True
        
        # Simple concat: avatar -> broll1 -> avatar -> broll2 -> etc
        # Split avatar into segments
        segment_duration = broll_interval
        segments = []
        current_time = 0
        broll_index = 0
        
        while current_time < duration:
            # Avatar segment
            seg_path = Path(tempfile.gettempdir()) / f"seg_{len(segments)}.mp4"
            end_time = min(current_time + segment_duration, duration)
            extract_segment(avatar_video, seg_path, current_time, end_time)
            if seg_path.exists():
                segments.append(seg_path)
            
            # Add B-Roll if available
            if broll_index < len(trimmed_brolls):
                segments.append(trimmed_brolls[broll_index])
                broll_index += 1
            
            current_time = end_time
        
        # Concat all segments
        concat_videos(segments, output_path)
        
        # Cleanup temp files
        for seg in segments:
            if seg.exists() and "broll_trimmed" not in str(seg):
                seg.unlink()
        
        print(f"✅ Assembled video: {output_path}")
        return True
        
    except Exception as e:
        print(f"❌ Assembly failed: {e}")
        return False

def get_video_duration(video_path: Path) -> float:
    """Get video duration in seconds"""
    try:
        # nosec B603: Using absolute path and list args
        result = subprocess.run([
            FFPROBE_BIN, "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            str(video_path)
        ], capture_output=True, text=True, check=False)
        return float(result.stdout.strip())
    except Exception:
        return 0.0

def trim_video(input_path: Path, output_path: Path, duration: float) -> bool:
    """Trim video to specified duration"""
    try:
        # nosec B603: Using absolute path and list args
        subprocess.run([
            FFMPEG_BIN, "-y", "-i", str(input_path),
            "-t", str(duration),
            "-c:v", "libx264", "-c:a", "aac",
            str(output_path)
        ], check=True, capture_output=True)
        return True
    except Exception:
        return False

def extract_segment(input_path: Path, output_path: Path, start: float, end: float) -> bool:
    """Extract segment from video"""
    try:
        # nosec B603: Using absolute path and list args
        subprocess.run([
            FFMPEG_BIN, "-y", "-i", str(input_path),
            "-ss", str(start), "-to", str(end),
            "-c:v", "libx264", "-c:a", "aac",
            str(output_path)
        ], check=True, capture_output=True)
        return True
    except Exception:
        return False

def concat_videos(videos: List[Path], output_path: Path) -> bool:
    """Concatenate videos using ffmpeg"""
    try:
        # Create concat file
        concat_file = Path(tempfile.gettempdir()) / "concat.txt"
        with open(concat_file, "w") as f:
            for v in videos:
                f.write(f"file '{v}'\n")
        
        # nosec B603: Using absolute path and list args
        subprocess.run([
            FFMPEG_BIN, "-y", "-f", "concat", "-safe", "0",
            "-i", str(concat_file),
            "-c:v", "libx264", "-c:a", "aac",
            str(output_path)
        ], check=True, capture_output=True)
        
        concat_file.unlink()
        return True
    except Exception as e:
        print(f"Concat error: {e}")
        return False

if __name__ == "__main__":
    ROOT_DIR = Path(__file__).parent.resolve()
    OUTPUT_DIR = ROOT_DIR / "outputs"
    
    # Test with mock data
    avatar = OUTPUT_DIR / "igor_ru_final.mp4"
    broll = []  # Add B-Roll paths here
    output = OUTPUT_DIR / "igor_assembled.mp4"
    
    if avatar.exists():
        create_video_with_broll(avatar, broll, output)
