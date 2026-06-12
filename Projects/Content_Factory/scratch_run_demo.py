import os
from pathlib import Path
from src.pipeline import orchestrator_v4_advanced

script_ru = """
Внимание. Будущее уже наступило. Автономные роботы возводят экологичные города, а новые технологии навсегда меняют наше понимание энергии. 
Мы объединяем мир, создавая гармонию между природой и прогрессом. Каждый новый шаг человечества — это путь к процветанию и чистому миру. 
Энергия будущего — это не просто ресурс, это ключ к выживанию нашей планеты и всех её обитателей. 
Присоединяйтесь к нам в этом увлекательном путешествии в завтрашний день!
"""

# We have 15 images already generated (0 to 14) from the previous run.
# So we create 15 dummy scenes.
scenes = [{"keyword": "futuristic city"} for _ in range(15)]

print("🎬 Running advanced pipeline with fixed audio...")
orchestrator_v4_advanced.run_advanced_pipeline(
    text=script_ru,
    output_name="runway_animated_demo",
    scenes=scenes
)
print("✅ Done!")
