import os
from pathlib import Path
from typing import Iterable
from urllib.parse import quote

import requests


def _get_pexels_key() -> str | None:
    key = os.getenv("PEXELS_API_KEY")
    if key:
        return key
    try:
        from token_broker import TokenBroker

        broker = TokenBroker()
        return broker.get_key("pexels")
    except Exception:
        return None


def _pick_best_file(video_files: Iterable[dict]) -> dict | None:
    best = None
    for vf in video_files or []:
        if vf.get("file_type") != "video/mp4":
            continue
        # Prefer highest resolution
        if not best:
            best = vf
            continue
        if (vf.get("height") or 0) > (best.get("height") or 0):
            best = vf
        elif (vf.get("height") or 0) == (best.get("height") or 0) and (
            vf.get("width") or 0
        ) > (best.get("width") or 0):
            best = vf
    return best


def semantic_search_broll(
    query: str, output_dir: Path, num_clips: int = 5, orientation: str = "portrait"
) -> list[Path]:
    """Fetch Pexels B-roll clips for a query. Returns list of local mp4 paths."""
    key = _get_pexels_key()
    if not key:
        print("⚠️ PEXELS_API_KEY not configured. Skipping B-roll.")
        return []

    output_dir.mkdir(parents=True, exist_ok=True)

    url = (
        "https://api.pexels.com/videos/search?"
        f"query={quote(query)}&per_page={num_clips}&orientation={orientation}"
    )

    try:
        res = requests.get(url, headers={"Authorization": key}, timeout=15)
        if res.status_code != 200:
            print(f"⚠️ Pexels API error: {res.status_code}")
            return []
        data = res.json() or {}
    except Exception as e:
        print(f"⚠️ Pexels request failed: {e}")
        return []

    clips: list[Path] = []
    for video in data.get("videos", [])[:num_clips]:
        vf = _pick_best_file(video.get("video_files"))
        if not vf:
            continue
        link = vf.get("link")
        if not link:
            continue
        vid_id = video.get("id", "unknown")
        out_path = output_dir / f"pexels_{vid_id}.mp4"
        if out_path.exists():
            clips.append(out_path)
            continue
        try:
            r = requests.get(link, stream=True, timeout=30)
            if r.status_code != 200:
                continue
            with open(out_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        f.write(chunk)
            clips.append(out_path)
        except Exception:
            # If download fails, skip this clip
            if out_path.exists():
                try:
                    out_path.unlink()
                except Exception:
                    pass
    return clips
