
"""
Style Presets for Video Factory 2026
Defines visual prompts and aesthetic settings for different content modes.
"""

STYLES = {
    "cartoon": {
        "name": "Pixar/Disney 3D Animation",
        "prompt_suffix": "3d render, pixar style, disney animation, vibrant colors, cute, expressive, high detailed, octane render, 8k, soft studio lighting",
        "negative_prompt": "photorealistic, real photo, grainy, blurry, low quality, dark, horror, text, watermark",
        "model_preference": "dalle-3-standard" # Can be flux in future
    },
    "impact": {
        "name": "Cinematic Documentary",
        "prompt_suffix": "cinematic shot, 35mm, realistic, dramatic lighting, high contrast, 8k, detailed texture, depth of field, national geographic style",
        "negative_prompt": "cartoon, drawing, anime, low res, blurry, jpeg artifacts, text, watermark",
        "model_preference": "flux-schnell" # Preference if available
    },
    "news": {
        "name": "Broadcast News",
        "prompt_suffix": "photorealistic, news studio, professional, clear focus, 4k, broadcast quality, bbc style",
        "negative_prompt": "cartoon, surreal, fantasy, distorted, low quality",
        "model_preference": "dalle-3-hd"
    },
    "tech": {
        "name": "Futuristic Tech",
        "prompt_suffix": "cyberpunk, neon lights, futuristic interface, holograms, high tech, dark background, glowing blue and orange, 8k",
        "negative_prompt": "vintage, rustic, natural, low quality",
        "model_preference": "dalle-3-hd"
    }
}

def get_style_prompt(style_key, subject):
    """
    Returns the full prompt for a given style and subject.
    """
    preset = STYLES.get(style_key, STYLES["impact"])
    return f"{subject}, {preset['prompt_suffix']}"
