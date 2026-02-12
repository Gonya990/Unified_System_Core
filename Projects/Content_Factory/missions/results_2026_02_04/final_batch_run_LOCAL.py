
import os
import subprocess
import sys
import time
from pathlib import Path

from dotenv import load_dotenv

# Force load ENV
load_dotenv('/home/gonya/Unified_System_Core/Projects/Content_Factory/.env')
# Ensure API keys are present in env for subprocesses
os.environ['PEXELS_API_KEY'] = os.getenv('PEXELS_API_KEY', '')
os.environ['ELEVENLABS_API_KEY'] = os.getenv('ELEVENLABS_API_KEY', '')
os.environ['RUNWAY_API_KEY'] = os.getenv('RUNWAY_API_KEY', '')

# Setup paths
FACTORY_ROOT = '/home/gonya/Unified_System_Core/Projects/Content_Factory'
sys.path.append(os.path.join(FACTORY_ROOT, 'src'))
sys.path.append(os.path.join(FACTORY_ROOT, 'src/pipeline'))

from orchestrator_v3_no_face import run_no_face_pipeline

SCRIPTS = [
    {
        'title': 'AI_Revolution_Hardware',
        'text': 'Процессоры будущего уже здесь. Квантовые вычисления изменят все. Ваш смартфон скоро станет мощнее суперкомпьютера.',
        'scenes': [{'keyword': 'quantum computer chip'}, {'keyword': 'futuristic cityscape'}]
    },
    {
        'title': 'AI_Revolution_Medicine',
        'text': 'Искусственный интеллект победит болезни. Персонализированная медицина и нанороботы — это не фантастика, это 2026 год.',
        'scenes': [{'keyword': 'dna helix medical'}, {'keyword': 'doctor futuristic hospital'}]
    },
    {
        'title': 'AI_Revolution_Space',
        'text': 'Мы колонизируем Марс быстрее, чем вы думаете. ИИ проектирует корабли, которые доставят нас к звездам.',
        'scenes': [{'keyword': 'mars planet space'}, {'keyword': 'spaceship launch'}]
    },
     {
        'title': 'AI_Revolution_Energy',
        'text': 'Бесконечная энергия солнца и термояд. ИИ оптимизирует сети, делая электричество почти бесплатным.',
        'scenes': [{'keyword': 'solar panels future'}, {'keyword': 'nuclear fusion reactor'}]
    },
    {
        'title': 'AI_Revolution_Creativity',
        'text': 'Творчество без границ. Искусство, музыка, кино — ИИ становится соавтором шедевров новой эпохи.',
        'scenes': [{'keyword': 'digital art creation'}, {'keyword': 'virtual reality headset'}]
    }
]

def run_reels():
    print('🚀 Starting BATCH REELS (Premium)...')
    for i, item in enumerate(SCRIPTS):
        print(f'🎬 Reel {i+1}: {item["title"]}')
        try:
            name = f'REEL_BATCH_{int(time.time())}_{i}_{item["title"]}'
            run_no_face_pipeline(
                text=item['text'],
                lang='ru',
                output_name=name,
                scenes=item['scenes'],
                style='impact'
            )

            output_file = Path(FACTORY_ROOT) / f'outputs/{name}_final.mp4'
            if output_file.exists():
                print(f'📤 Sending {name} to Telegram...')
                caption = f'🎞️ <b>Reel {i+1}/5: {item["title"]}</b>\n\n✅ <b>Voice:</b> ElevenLabs\n✅ <b>Video:</b> Pexels API\n\n<a href="https://www.pexels.com">Photos provided by Pexels</a>'
                subprocess.run([
                    'curl',
                    '-F', f'video=@{output_file}',
                    '-F', 'chat_id=708531393',
                    '-F', f'caption={caption}',
                    '-F', 'parse_mode=HTML',
                    'https://api.telegram.org/bot8518131338:AAHtcEgI--E2Fktdo3nE3oynhzq1gvrVON4/sendVideo'
                ])
        except Exception as e:
            print(f'❌ Error Reel {i}: {e}')

def run_longform():
    print('📽️ Starting LONG-FORM DOCUMENTARY...')
    # Topic
    topic = "The Future of Humanity 2026"

    # Run Orchestrator command
    cmd = f'nohup uv run --with google-generativeai --with python-dotenv --with edge-tts --with openai --with pyyaml --with requests python3 {FACTORY_ROOT}/src/pipeline/longform_producer.py --topic "{topic}" > {FACTORY_ROOT}/missions/results_2026_02_04/longform_final.log 2>&1 &'
    os.system(cmd)
    print('✅ Longform Producer detached. Check Telegram for updates.')

    # Inform User via Telegram
    msg = f'📽️ <b>ЗАПУЩЕНА ГЕНЕРАЦИЯ ДОКУМЕНТАЛЬНОГО ФИЛЬМА</b>\n\n<b>Тема:</b> {topic}\n<b>Длительность:</b> 15-30 мин\n<b>Инструменты:</b> GCP Vertex AI, ElevenLabs, Pexels.\n\n⏳ Ожидайте уведомления по завершению.'
    subprocess.run([
        'curl',
        '-X', 'POST',
        'https://api.telegram.org/bot8518131338:AAHtcEgI--E2Fktdo3nE3oynhzq1gvrVON4/sendMessage',
        '-d', f'chat_id=708531393&text={msg}&parse_mode=HTML'
    ])

if __name__ == '__main__':
    run_reels()
    run_longform()
