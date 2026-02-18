import json
import os
import subprocess


def get_duration(file_path):
    cmd = [
        'ffprobe', '-v', 'error', '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1', file_path
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    return float(res.stdout.strip())

def collect_durations():
    base_dir = "/Users/igorgoncharenko/Documents/Unified_System_Core/Reports/media/audio"
    report = {}
    for lang in ["EN", "RU"]:
        report[lang] = {}
        lang_dir = os.path.join(base_dir, lang)
        if not os.path.exists(lang_dir): continue
        for f in sorted(os.listdir(lang_dir)):
            if f.endswith(".mp3") and f.startswith("block_"):
                d = get_duration(os.path.join(lang_dir, f))
                report[lang][f] = d

    with open("/Users/igorgoncharenko/Documents/Unified_System_Core/Reports/media/audio_durations.json", "w") as f:
        json.dump(report, f, indent=2)
    print("✅ Durations collected.")

if __name__ == "__main__":
    collect_durations()
