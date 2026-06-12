"""
YouTube Channel Configuration — UnifiedCore Content Factory
Two-channel strategy: Megaforma (main) + UnifiedSystem (tech/dev)

Megaforma:       https://www.youtube.com/@Megaforma
UnifiedSystem:   https://www.youtube.com/@UnifiedSystem-l6d
"""

from pathlib import Path

# ─────────────────────────────────────────────
#  CHANNEL DEFINITIONS
# ─────────────────────────────────────────────

CREDENTIALS_DIR = Path(__file__).parent.parent / "uploaders" / ".credentials"

YOUTUBE_CHANNELS = {

    # ════════════════════════════════════════
    #  MEGAFORMA — Main channel (RU/EN/HE content)
    #  Focus: AI trends, geopolitics, future tech
    #  Target: Russian-speaking global audience
    # ════════════════════════════════════════
    "megaforma": {
        "name": "Megaforma",
        "handle": "@megaforma_ai",
        "channel_id": "UCXiWjKYfCDsmEphcqn5rBzg",  # Verified 2026-06-12
        "url": "https://www.youtube.com/@megaforma_ai",
        "token_file": str(CREDENTIALS_DIR / "youtube_token_megaforma_full.json"),
        "languages": ["ru", "en", "he"],  # Publish in all 3
        "content_modes": ["daily", "english", "hebrew", "cartoon"],
        "default_privacy": "public",
        "made_for_kids": False,          # REQUIRED for YPP
        "category_id": "28",            # Science & Technology
        "license": "youtube",           # Standard YouTube license
        "embeddable": True,             # Allow embedding (wider reach)
        "notify_subscribers": True,     # Notify on each upload
        "stabilize": True,              # Stabilization for Shorts
        # YPP Readiness
        "ypp_ready": True,
        "monetization_enabled": False,  # Off now, flip when 1k subs/4k hours
        "target_subs_for_ypp": 1000,
        "strategy": {
            "primary": "Shorts (60s)",   # Primary content format
            "secondary": "Documentary (28min)",
            "posting_frequency": "3-4 per day",
            "peak_times_utc": ["07:00", "12:00", "18:00"],  # ISR +3
        },
        "seo": {
            "channel_keywords": ["AI", "искусственный интеллект", "будущее технологий",
                                 "нейросети", "геополитика", "стартапы", "Megaforma"],
            "description_template": "Megaforma — канал о будущем технологий и искусственного интеллекта.",
        }
    },

    # ════════════════════════════════════════
    #  UNIFIED SYSTEM — Dev/Tech channel (EN)
    #  Focus: AI coding, system architecture, dev tools
    #  Target: Developers & tech professionals
    # ════════════════════════════════════════
    "unifiedsystem": {
        "name": "UnifiedSystem",
        "handle": "@UnifiedSystem-l6d",
        "url": "https://www.youtube.com/@UnifiedSystem-l6d",
        "token_file": str(CREDENTIALS_DIR / "youtube_token_unifiedsystem.json"),
        "languages": ["en"],            # English only
        "content_modes": ["english", "tutorial"],
        "default_privacy": "public",
        "made_for_kids": False,
        "category_id": "28",            # Science & Technology
        "license": "youtube",
        "embeddable": True,
        "notify_subscribers": True,
        "stabilize": False,
        # YPP Readiness
        "ypp_ready": True,
        "monetization_enabled": False,
        "target_subs_for_ypp": 1000,
        "strategy": {
            "primary": "Long-form tutorial",
            "secondary": "Shorts (code tips)",
            "posting_frequency": "1-2 per day",
            "peak_times_utc": ["09:00", "17:00"],  # US morning + EU evening
        },
        "seo": {
            "channel_keywords": ["AI system", "unified AI", "autonomous agents",
                                 "AI architecture", "UnifiedSystem", "LLM development"],
            "description_template": "UnifiedSystem — Building the future with autonomous AI agents.",
        }
    },
}

# ─────────────────────────────────────────────
#  CONTENT ROUTING
# ─────────────────────────────────────────────

# Map production mode → which channels get the video
CONTENT_ROUTING = {
    "daily":     ["megaforma"],                    # RU shorts → Megaforma only
    "english":   ["megaforma", "unifiedsystem"],   # EN shorts → Both channels
    "hebrew":    ["megaforma"],                    # HE shorts → Megaforma only
    "cartoon":   ["megaforma"],                    # Cartoon → Megaforma only
    "tutorial":  ["unifiedsystem"],               # Dev tutorial → UnifiedSystem only
    "longform":  ["megaforma"],                    # Documentary → Megaforma only
}

# ─────────────────────────────────────────────
#  SHORTS OPTIMIZATION
# ─────────────────────────────────────────────

SHORTS_SETTINGS = {
    "max_duration_seconds": 59,    # Keep under 60s for Shorts algorithm
    "target_duration_seconds": 50, # Sweet spot for completion rate
    "aspect_ratio": "9:16",        # Vertical for Shorts
    "hashtag_shorts": True,        # Always add #Shorts to title
    "auto_chapters": False,         # No chapters for Shorts
}

LONGFORM_SETTINGS = {
    "min_duration_minutes": 15,
    "target_duration_minutes": 28,
    "aspect_ratio": "16:9",
    "hashtag_shorts": False,
    "auto_chapters": True,         # Auto-generate chapters
    "chapters_interval_minutes": 3,
}


def get_channel(channel_id: str) -> dict:
    """Get channel config by ID."""
    return YOUTUBE_CHANNELS.get(channel_id, {})


def get_channels_for_mode(mode: str) -> list:
    """Get list of channel configs for a given production mode."""
    channel_ids = CONTENT_ROUTING.get(mode, ["megaforma"])
    return [
        {"id": cid, **YOUTUBE_CHANNELS[cid]}
        for cid in channel_ids
        if cid in YOUTUBE_CHANNELS
    ]


def get_all_active_channels() -> list:
    """Get all channels that have valid token files."""
    active = []
    for cid, config in YOUTUBE_CHANNELS.items():
        token_file = Path(config["token_file"])
        if token_file.exists():
            active.append({"id": cid, **config})
        else:
            print(f"⚠️  Channel '{cid}' ({config['handle']}) — token missing: {token_file.name}")
    return active


def get_ypp_status() -> dict:
    """Get YPP readiness status for all channels."""
    return {
        cid: {
            "channel": cfg["name"],
            "handle": cfg["handle"],
            "ypp_ready": cfg["ypp_ready"],
            "monetization": cfg["monetization_enabled"],
            "target_subs": cfg["target_subs_for_ypp"],
            "note": "✅ Ready to enable monetization when threshold reached" if cfg["ypp_ready"] else "❌ Not configured"
        }
        for cid, cfg in YOUTUBE_CHANNELS.items()
    }
