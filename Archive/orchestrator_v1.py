
import subprocess
import sys
from pathlib import Path

# Paths
ROOT_DIR = Path(__file__).parent.resolve()
LIVE_PORTRAIT_DIR = ROOT_DIR / "LivePortrait"
STYLETTS_DIR = ROOT_DIR / "StyleTTS2"
OUTPUT_DIR = ROOT_DIR / "outputs"
INPUT_DIR = ROOT_DIR / "inputs"

OUTPUT_DIR.mkdir(exist_ok=True)
INPUT_DIR.mkdir(exist_ok=True)

# Add paths to sys.path
sys.path.append(str(LIVE_PORTRAIT_DIR))
sys.path.append(str(STYLETTS_DIR))

def generate_audio(text, output_audio_path):
    print(f"🎤 Generating Audio for: '{text}'...")
    # --- Generate Audio (using Edge-TTS) ---
    print("🎤 Generating Audio via Edge-TTS...")

    # We will generate mp3 first, then convert to wav for compatibility if needed (LivePortrait calls ffmpeg anyway)
    mp3_path = output_audio_path.with_suffix(".mp3")

    voice = "en-US-ChristopherNeural"

    cmd_audio = [
        "edge-tts",
        "--text", text,
        "--write-media", str(mp3_path),
        "--voice", voice
    ]

    try:
        subprocess.run(cmd_audio, check=True, cwd=str(ROOT_DIR))
        print(f"✅ Edge-TTS audio generated: {mp3_path}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Edge-TTS audio generation failed: {e}")
        return False
    except FileNotFoundError:
        print("❌ Error: 'edge-tts' command not found. Please install it: pip install edge-tts")
        return False

    # Convert to WAV just in case (and ensure correct sample rate/channels for LivePortrait consistency)
    cmd_convert = [
        "ffmpeg", "-y",
        "-i", str(mp3_path),
        "-ar", "44100", # Standard sample rate
        "-ac", "1",     # Mono channel
        str(output_audio_path)
    ]
    try:
        subprocess.run(cmd_convert, check=True, capture_output=True)
        print(f"✅ Converted MP3 to WAV: {output_audio_path}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Audio conversion failed: {e.stderr.decode()}")
        return False
    except FileNotFoundError:
        print("❌ Error: 'ffmpeg' command not found. Please install FFmpeg.")
        return False

    if not output_audio_path.exists():
         print("❌ Final WAV audio file not found after generation/conversion!")
         return False

    return True

def animate_face(image_path, audio_path, output_video_path):
    print(f"🎬 Animating Face: {image_path} with {audio_path}...")

    # LivePortrait Inference
    # python inference.py --source ... --driving ...
    # BUT LivePortrait needs a driving VIDEO, not Audio directly (unless we use Audio2Video driving mode which is internal)
    # The standard LivePortrait uses a 'driving video' (motion template).
    # To animate from AUDIO, we usually need SadTalker OR LivePortrait's 'Audio-Driven' mode (if supported) or a driving video template.

    # Wait, initially I proposed LivePortrait. LivePortrait is Video-to-Video (Expression Transfer).
    # Did I promise Audio-to-Video?
    # Valid Point: LivePortrait needs a driving video (expression video) to drive the source image.
    # To make it "Audio Driven", we typically use a set of "driving templates" (pre-recorded videos of someone talking)
    # OR we use SadTalker (Image+Audio -> Video).

    # Let's check user request: "Human-like", "LivePortrait".
    # LivePortrait is BEST for quality but needs a driver.
    # Strategy: Use a generic "talking driver video" (d0.mp4) and re-time it? No, that won't match lips.
    # CORRECTION: For strict Audio-Sync (Lip Sync), SadTalker/Wav2Lip is standard.
    # HOWEVER, newer "EchoMimic" or "LivePortrait with generic driver" are options.

    # LET'S USE LIVEPORTRAIT WITH A GENERIC DRIVER FOR NOW (Lips won't sync perfectly to new text, just animation).
    # OR: Use a pre-existing "speech driver" that matches the audio length?

    # CRITICAL PIVOT: To get LIP SYNC with LivePortrait, we need a driving video that HAS the lips moving correctly.
    # Usually we generate the lip motion using SadTalker/Wav2Lip, then pass that as 'driving' to LivePortrait for high quality.
    # OR we use `EchoMimic` (which I found in research but didn't install).

    # FOR THIS TEST: I will use the standard `d0.mp4` driver just to show AN ANIMATION of YOUR face.
    # Later we will add Wav2Lip/SadTalker to generate the driver.

    cmd = [
        sys.executable,
        str(LIVE_PORTRAIT_DIR / "inference.py"),
        "--source", str(image_path),
        "--driving", str(LIVE_PORTRAIT_DIR / "assets/examples/driving/d0.mp4"),
        "--output-dir", str(OUTPUT_DIR)
    ]

    try:
        subprocess.run(cmd, check=True)
        print(f"✅ Animation Complete. Result in {OUTPUT_DIR}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Animation Failed: {e}")

    return str(OUTPUT_DIR / f"{image_path.stem}--{Path(LIVE_PORTRAIT_DIR / 'assets/examples/driving/d0.mp4').stem}.mp4")

def animate_lip_sync(video_path, audio_path, output_video_path):
    print(f"👄 Running Lip Sync (Wav2Lip) on {video_path}...")

    # Wav2Lip Inference
    # python inference.py --checkpoint_path checkpoints/wav2lip_gan.pth --face <video> --audio <audio>

    wav2lip_dir = ROOT_DIR / "Wav2Lip"
    venv_python = ROOT_DIR / "venv_wav2lip/bin/python3"
    inference_script = wav2lip_dir / "inference.py"
    checkpoint = wav2lip_dir / "checkpoints/wav2lip_gan.pth"

    # Wav2Lip writes to 'results/result_voice.mp4' by default usually, but let's check args.
    # The default inference.py takes --outfile.

    cmd = [
        str(venv_python),
        str(inference_script),
        "--checkpoint_path", str(checkpoint),
        "--face", str(video_path),
        "--audio", str(audio_path),
        "--outfile", str(output_video_path),
        "--resize_factor", "1", # full res if possible
        "--pads", "0", "10", "0", "0" # Padding for face crop if needed
    ]

    try:
        # Run inside Wav2Lip dir to avoid path issues? No, paths are absolute.
        # But import paths might be relative in Wav2Lip code. Safe to cwd.
        subprocess.run(cmd, check=True, cwd=str(wav2lip_dir))
        print(f"✅ Lip Sync Complete: {output_video_path}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Lip Sync Failed: {e}")

if __name__ == "__main__":
    text = "Hello! I am a new AI blogger. I speak with a voice cloned from Gemini video, and I use your face with wings."
    image = LIVE_PORTRAIT_DIR / "assets/examples/source/igor_wings.png"
    audio_out = INPUT_DIR / "speech.wav"

    # 1. Generate Audio
    if generate_audio(text, audio_out):
        # 2. Animate Head (LivePortrait)
        # This returns the path to the concatenated video
        head_video = animate_face(image, audio_out, OUTPUT_DIR / "igor_test.mp4")

        # 3. Lip Sync (Wav2Lip)
        # Verify head_video exists
        # Note: LivePortrait result name logic is complex ("igor_wings--d0.mp4").
        # I need to verify what animate_face actually returns or produces.

        # It seems animate_face in my code voidly printed path.
        # Check logs: "/home/gonya/ContentFarm/outputs/igor_wings--d0.mp4"

        # Let's hardcode the expected LivePortrait output for now or update animate_face to return it.
        # I updated animate_face to return the path above.

        # Correct path from logs:
        lp_output = OUTPUT_DIR / "igor_wings--d0.mp4"

        if lp_output.exists():
            final_output = OUTPUT_DIR / "igor_final_lipsync.mp4"
            animate_lip_sync(lp_output, audio_out, final_output)
        else:
            print(f"❌ Could not find LivePortrait output: {lp_output}")
