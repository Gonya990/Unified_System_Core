"""
Простой локальный голосовой ассистент (ASR -> LLM -> TTS).
Подходит для вашего RTX 3080 и уже установленного стека (PyTorch, transformers).

Рабочие режимы:
- Интерактивный режим: запись с микрофона и обработка (требует доступа к аудио-устройствам).
- Тестовый режим: обработка существующего WAV-файла (--file).

Примечание: при запуске по SSH используйте тестовый режим (--file),
иначе процесс не сможет получить доступ к локальному микрофону.
"""

import os
import sys
import argparse
import tempfile
from pathlib import Path
# Отложенный импорт для библиотек, которые нужны только в интерактивном режиме
from faster_whisper import WhisperModel
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# Настройки — можете менять
ASR_MODEL_SIZE = "small"        # small / medium / large (small быстрее)
RECORD_SECONDS_DEFAULT = 5
LLM_MODEL = "microsoft/Phi-3-mini-4k-instruct"  # замените при необходимости
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


def record_audio(filename: str, duration: float):
    print(f"Запись аудио: {duration} сек...")
    samplerate = 16000
    try:
        try:
            import sounddevice as sd
            import soundfile as sf
        except ImportError as ie:
            print("Для записи аудио в интерактивном режиме нужны пакеты 'sounddevice' и 'soundfile'.")
            print("Установите их в окружение: python -m pip install sounddevice soundfile")
            raise

        recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
        sd.wait()
        sf.write(filename, recording, samplerate)
        print(f"Сохранено в {filename}")
    except Exception as e:
        print(f"Ошибка записи аудио: {e}")
        raise


def transcribe_audio_whisper(model, path, language='ru'):
    # faster-whisper: returns segments and info
    print("ASR: распознавание (faster-whisper)...")
    segments, info = model.transcribe(path, language=language)
    text = "".join([seg.text for seg in segments])
    print("ASR -> текст:", text)
    return text


def load_llm(model_name: str):
    print(f"Загрузка LLM: {model_name} (это может занять время)")
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16 if DEVICE == "cuda" else torch.float32,
        device_map="auto" if DEVICE == "cuda" else None,
        trust_remote_code=True
    )
    model.eval()
    return tokenizer, model


def generate_llm_response(tokenizer, model, prompt: str):
    print("LLM: генерирую ответ...")
    inputs = tokenizer(prompt, return_tensors='pt', truncation=True, max_length=1024)
    if DEVICE == "cuda":
        inputs = {k: v.cuda() for k, v in inputs.items()}
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=200,
            temperature=0.7,
            top_p=0.9,
            do_sample=True,
            pad_token_id=tokenizer.pad_token_id,
            repetition_penalty=1.1,
            use_cache=False
        )
    text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    # Обрезаем промпт если модель повторила
    if "Assistant:" in text:
        text = text.split("Assistant:")[-1].strip()
    return text


def speak_text_pyttsx3(text: str):
    try:
        try:
            import pyttsx3
        except ImportError:
            print("pyttsx3 не установлен в окружении — пропускаю воспроизведение.")
            return

        engine = pyttsx3.init()
        rate = engine.getProperty('rate')
        engine.setProperty('rate', max(100, rate - 10))
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Ошибка TTS (pyttsx3): {e}")


def main():
    parser = argparse.ArgumentParser(description='Local voice assistant (ASR->LLM->TTS)')
    parser.add_argument('--file', '-f', type=str, help='Path to WAV file to process (test mode)')
    parser.add_argument('--record', '-r', type=float, default=RECORD_SECONDS_DEFAULT, help='Seconds to record in interactive mode')
    parser.add_argument('--no-tts', action='store_true', help='Do not run TTS, only print the LLM response')
    parser.add_argument('--model', type=str, default=LLM_MODEL, help='LLM model name override')
    args = parser.parse_args()

    print("Local voice assistant starting...")
    print(f"Device: {DEVICE}")

    # Загрузка ASR
    print(f"Loading ASR model: {ASR_MODEL_SIZE} on {DEVICE}...")
    asr_model = WhisperModel(ASR_MODEL_SIZE, device=DEVICE, compute_type="float16" if DEVICE == "cuda" else "float32")

    # Загрузка LLM
    tokenizer, llm_model = load_llm(args.model)

    # If file mode requested, process single file and exit
    if args.file:
        wav_path = Path(args.file)
        if not wav_path.exists():
            print(f"File not found: {wav_path}")
            sys.exit(2)
        text = transcribe_audio_whisper(asr_model, str(wav_path), language='ru')
        if not text.strip():
            print("Ничего не распознано в файле.")
            sys.exit(0)
        prompt = f"User: {text}\nAssistant:"
        response = generate_llm_response(tokenizer, llm_model, prompt)
        print(f"Assistant: {response}\n")
        if not args.no_tts:
            speak_text_pyttsx3(response)
        sys.exit(0)

    # Interactive loop (only if running with audio access)
    print("Готов к приёму голосовых команд.")
    print("Нажмите Enter чтобы записать (или введите длительность в секундах). Введите /exit для выхода.")

    while True:
        user_cmd = input("\n> ").strip()
        if not user_cmd:
            duration = args.record
        elif user_cmd.lower() in ['/exit', 'exit', 'quit']:
            print("Выход...")
            break
        else:
            try:
                duration = float(user_cmd)
            except Exception:
                duration = args.record

        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmpf:
            tmp_path = tmpf.name

        try:
            record_audio(tmp_path, duration)

            # ASR
            text = transcribe_audio_whisper(asr_model, tmp_path, language='ru')
            if not text.strip():
                print("Ничего не распознано, попробуйте еще раз.")
                continue

            # Build prompt for LLM
            prompt = f"User: {text}\nAssistant:"
            response = generate_llm_response(tokenizer, llm_model, prompt)
            print(f"Assistant: {response}\n")

            # TTS
            if not args.no_tts:
                speak_text_pyttsx3(response)

        finally:
            try:
                os.remove(tmp_path)
            except Exception:
                pass


if __name__ == '__main__':
    main()
