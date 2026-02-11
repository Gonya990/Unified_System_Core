# 🐵 Two Chimps: Automated Podcast Pipeline

This pipeline turns your voice notes into a video podcast hosted by two AI chimpanzees (The Skeptic and The Enthusiast).

## 🚀 Quick Start

1. **Drop your audio note** (MP3/M4A/MOV) into:
    `/Users/igorgoncharenko/Documents/Unified_System_Core/Context`

2. **Run the Pipeline**:

    ```bash
    cd /Users/igorgoncharenko/Documents/Unified_System_Core/Projects/Content_Factory
    
    # 1. Sync & Transcribe
    python3 src/two_chimps/sync_context.py (Optional if files are local)
    python3 src/two_chimps/transcribe_context.py
    
    # 2. Generate Script
    python3 src/two_chimps/generate_dialogue.py
    
    # 3. Generate Avatars (One time setup)
    python3 src/two_chimps/generate_avatars.py
    
    # 4. Generate Audio & Video
    python3 src/two_chimps/generate_voiceover.py
    python3 src/two_chimps/assemble_video.py
    ```

3. **Result**:
    Find your video in: `.../Context/final_videos/`

## 🛠 Components

| Script | Purpose |
| :--- | :--- |
| `sync_context.py` | Syncs Google Drive <-> Local Context folder. |
| `transcribe_context.py` | Converts audio notes to text using Whisper. |
| `generate_dialogue.py` | Uses GPT-4o to write a funny script between two hosts. |
| `generate_avatars.py` | Generates the visual personas using DALL-E 3. |
| `generate_voiceover.py` | Converts script to audio using EdgeTTS (Free). |
| `assemble_video.py` | Combines audio and images into an MP4 video. |
