from pathlib import Path

import PIL.Image

if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = PIL.Image.LANCZOS

from moviepy.editor import CompositeVideoClip, ImageClip

# Пути
CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent.parent.parent.parent
CONTEXT_DIR = Path("/Users/igorgoncharenko/Documents/Unified_System_Core/Context")
AVATARS_DIR = CURRENT_DIR / "assets"
VIDEO_DIR = CONTEXT_DIR / "video_clips"

if not VIDEO_DIR.exists():
    VIDEO_DIR.mkdir(parents=True, exist_ok=True)

def create_ken_burns_clip(image_path, output_path, duration=5.0, zoom_factor=1.1):
    """
    Создает видеоклип из изображения с медленным зумом (эффект Кена Бернса).
    """
    print(f"🎬 Генерация клипа движения для: {image_path.name}")

    # Загрузка изображения
    clip = ImageClip(str(image_path)).set_duration(duration)

    # Эффект Зума
    # Простое решение: Медленное увеличение масштаба
    w, h = clip.size

    # Zoom In: Начало 1.0, Увеличение со временем
    clip = clip.resize(lambda t: 1 + 0.02 * t) # Медленный зум

    # Центрирование (CompositeVideoClip автоматически центрирует)
    final = CompositeVideoClip([clip], size=(w, h))

    final.write_videofile(
        str(output_path),
        fps=24,
        codec="libx264",
        audio=False,
        preset="medium",
        ffmpeg_params=["-pix_fmt", "yuv420p"] # Важно для совместимости
    )
    print(f"✅ Видеоклип сохранен: {output_path.name}")

def generate_dynamic_avatars():
    avatars = {
        "Rex": AVATARS_DIR / "dino_skeptic.png",
        "Trike": AVATARS_DIR / "dino_enthusiast.png",
        "Studio": AVATARS_DIR / "dino_studio_background.png"
    }

    for name, path in avatars.items():
        if not path.exists():
            print(f"⚠️ Аватар не найден: {path}")
            continue

        output = VIDEO_DIR / f"{name.lower()}_motion.mp4"
        create_ken_burns_clip(path, output, duration=10.0)

if __name__ == "__main__":
    generate_dynamic_avatars()
