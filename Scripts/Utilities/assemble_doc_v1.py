import json
import os
import subprocess


def assemble_video(lang="EN"):
    print(f"🎬 Assembling documentary video for {lang}...")

    media_dir = "/Users/igorgoncharenko/Documents/Unified_System_Core/Reports/media"
    audio_dir = os.path.join(media_dir, "audio", lang)
    scenes_dir = os.path.join(media_dir, "scenes")
    durations_path = os.path.join(media_dir, "audio_durations.json")

    with open(durations_path) as f:
        durations = json.load(f)[lang]

    # Asset mapping for each block
    # Logic: Divide block duration by number of assets to get segment length
    asset_map = {
        "block_0.mp3": [
            "scene_1.mp4",
            "scene_2_city_grid_1771322867993.png",
            "scene_3.mp4"
        ],
        "block_1.mp3": [
            "scene_4.mp4",
            "scene_5_kubernetes_clusters_1771322882669.png"
        ],
        "block_2.mp3": [
            "scene_6_proxmox_hologram_1771322899091.png",
            "scene_8.mp4"
        ],
        "block_3.mp3": [
            "scene_10_ai_council_v4_1771323829059.png",
            "scene_11_data_streams_1771324072979.png",
            "scene_12_judge_gavel_1771324129162.png"
        ],
        "block_4.mp3": [
            "scene_13_vibranium_shield_dome_v3_1771323867320.png",
            "scene_15.mp4",
            "scene_16_data_crystals_v2_1771325039295.png"
        ],
        "block_5.mp3": [
            "scene_17_bybit_app_1771324216936.png",
            "scene_18.mp4",
            "scene_19.mp4",
            "scene_20.mp4",
            "scene_21_unified_sunset_v2_1771325023119.png"
        ]
    }

    # 1. Create temporary video segments for each asset
    temp_segments = []

    # Global offset for audio concatenation
    audio_files = []

    for block_name, assets in asset_map.items():
        if block_name not in durations: continue
        total_dur = durations[block_name]
        segment_dur = total_dur / len(assets)

        audio_files.append(os.path.join(audio_dir, block_name))

        for i, asset_name in enumerate(assets):
            asset_path = os.path.join(scenes_dir, asset_name)
            if not os.path.exists(asset_path):
                print(f"⚠️ Warning: Asset {asset_name} missing, using Scene 1 as fallback.")
                asset_path = os.path.join(scenes_dir, "scene_1.mp4")

            temp_out = os.path.join(media_dir, f"temp_{lang}_{block_name}_{i}.mp4")

            # Use ffmpeg to generate a segment
            # If image: use zoom/pan effect or loop
            # If video: loop or trim
            if asset_name.endswith(".png"):
                # Image to video with slight zoom
                cmd = [
                    'ffmpeg', '-y', '-loop', '1', '-i', asset_path,
                    '-vf', f"scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,zoompan=z='min(zoom+0.001,1.5)':d={int(segment_dur*30)}:s=1920x1080",
                    '-t', str(segment_dur), '-c:v', 'libx264', '-pix_fmt', 'yuv420p', temp_out
                ]
            else:
                # Video to video
                cmd = [
                    'ffmpeg', '-y', '-stream_loop', '-1', '-i', asset_path,
                    '-vf', 'scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080',
                    '-t', str(segment_dur), '-c:v', 'libx264', '-pix_fmt', 'yuv420p', temp_out
                ]

            print(f"  → Generating segment for {asset_name} ({segment_dur:.2f}s)...")
            subprocess.run(cmd, capture_output=True)
            temp_segments.append(temp_out)

    # 2. Concatenate all segments
    list_path = os.path.join(media_dir, f"list_{lang}.txt")
    with open(list_path, "w") as f:
        for seg in temp_segments:
            f.write(f"file '{seg}'\n")

    final_video_no_audio = os.path.join(media_dir, f"video_only_{lang}.mp4")
    concat_cmd = [
        'ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', list_path,
        '-c', 'copy', final_video_no_audio
    ]
    print("🎬 Concatenating visual segments...")
    subprocess.run(concat_cmd, capture_output=True)

    # 3. Concatenate all audio blocks
    audio_list_path = os.path.join(media_dir, f"audio_list_{lang}.txt")
    with open(audio_list_path, "w") as f:
        for aud in audio_files:
            f.write(f"file '{aud}'\n")

    final_audio = os.path.join(media_dir, f"full_audio_{lang}.mp3")
    audio_cmd = [
        'ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', audio_list_path,
        '-c', 'copy', final_audio
    ]
    print("🎬 Concatenating audio blocks...")
    subprocess.run(audio_cmd, capture_output=True)

    # 4. Merge video and audio
    final_output = f"/Users/igorgoncharenko/Documents/Unified_System_Core/Reports/DOCUMENTARY_2026_{lang}.mp4"
    merge_cmd = [
        'ffmpeg', '-y', '-i', final_video_no_audio, '-i', final_audio,
        '-c:v', 'copy', '-c:a', 'aac', '-shortest', final_output
    ]
    print(f"🏁 Finalizing video: {final_output}")
    subprocess.run(merge_cmd, capture_output=True)

    # Cleanup
    for seg in temp_segments:
        if os.path.exists(seg): os.remove(seg)
    if os.path.exists(list_path): os.remove(list_path)
    if os.path.exists(audio_list_path): os.remove(audio_list_path)
    if os.path.exists(final_video_no_audio): os.remove(final_video_no_audio)
    if os.path.exists(final_audio): os.remove(final_audio)

    print(f"✅ Documentary {lang} ready!")

if __name__ == "__main__":
    assemble_video("EN")
    assemble_video("RU")
