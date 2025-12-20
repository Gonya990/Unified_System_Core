# Настройка Windows ПК с NVIDIA RTX для работы с ИИ

## Обзор

Этот набор скриптов поможет настроить Windows ПК с NVIDIA RTX для работы с ИИ приложениями через удалённое подключение с вашего Macbook Air M1.

## Архитектура решения

```
Windows ML Runtime (ONNX Runtime)
    ↓
NVIDIA TensorRT для RTX (GPU Provider)
    ↓
NVIDIA RTX GPU
```

## Компоненты для установки

1. **NVIDIA драйверы** - последние Game Ready или Studio Driver
2. **CUDA Toolkit** - для поддержки GPU вычислений
3. **cuDNN** - библиотека для глубокого обучения
4. **TensorRT** - оптимизация inference на NVIDIA GPU
5. **ONNX Runtime** - Windows ML Runtime с TensorRT провайдером
6. **Python 3.10+** - для работы с Olive и примерами
7. **Olive Toolkit** - оптимизация моделей для различного железа

## Быстрый старт

### 1. Подключение к Windows ПК с Mac

#### Вариант A: Remote Desktop (RDP)
```bash
# Установите Microsoft Remote Desktop на Mac
brew install --cask microsoft-remote-desktop

# Подключитесь через приложение Microsoft Remote Desktop
# Введите IP адрес вашего Windows ПК
```

#### Вариант B: SSH (если настроен OpenSSH на Windows)
```bash
# Подключение через SSH
ssh username@windows-pc-ip

# Копирование файлов на Windows ПК
scp -r windows-rtx-ai-setup username@windows-pc-ip:C:/Users/username/
```

### 2. Установка компонентов на Windows ПК

На Windows ПК запустите PowerShell **от имени администратора** и выполните:

```powershell
# Перейдите в папку со скриптами
cd C:\Users\YourUsername\windows-rtx-ai-setup

# Разрешите выполнение скриптов
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Запустите основной скрипт установки
.\setup-rtx-ai-environment.ps1
```

### 3. Проверка установки

```powershell
# Проверьте GPU
.\verify-installation.ps1
```

### 4. Оптимизация модели с Olive

```powershell
# Установите Olive
.\setup-olive.ps1

# Оптимизируйте вашу ONNX модель
python optimize-model-example.py --model path/to/your/model.onnx
```

## Структура проекта

```
windows-rtx-ai-setup/
├── README.md                           # Этот файл
├── setup-rtx-ai-environment.ps1       # Основной скрипт установки
├── verify-installation.ps1            # Проверка установки
├── setup-olive.ps1                    # Установка Olive Toolkit
├── remote-connection-guide.md         # Руководство по удалённому подключению
├── examples/
│   ├── python/
│   │   ├── onnx-runtime-basic.py     # Базовый пример ONNX Runtime
│   │   ├── onnx-runtime-tensorrt.py  # Пример с TensorRT
│   │   └── optimize-model-example.py  # Пример оптимизации с Olive
│   └── csharp/
│       ├── WindowsMLExample.csproj    # C# проект
│       └── Program.cs                 # Пример на C#
└── configs/
    └── olive-config-example.json      # Пример конфигурации Olive
```

## Требования

### На Windows ПК:
- Windows 10/11 (64-bit)
- NVIDIA RTX GPU (2000 серия или новее)
- Минимум 8 GB RAM (рекомендуется 16 GB)
- 20 GB свободного места на диске
- Подключение к интернету

### На Macbook Air M1:
- macOS с установленным RDP клиентом или SSH
- Сетевой доступ к Windows ПК

## Полезные ссылки

- [Windows ML Documentation](https://learn.microsoft.com/windows/ai/windows-ml/)
- [ONNX Runtime Documentation](https://onnxruntime.ai/docs/)
- [NVIDIA TensorRT](https://developer.nvidia.com/tensorrt)
- [Olive Toolkit](https://github.com/microsoft/Olive)
- [ONNX Model Zoo](https://github.com/onnx/models)

## Поддержка

При возникновении проблем:
1. Проверьте логи в папке `logs/`
2. Запустите `verify-installation.ps1` для диагностики
3. Убедитесь, что все драйверы NVIDIA обновлены

## Лицензия

Этот набор скриптов предоставляется "как есть" для образовательных целей.

<TargetFramework>net10.0</TargetFramework>

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Загрузка небольшой модели для теста
model_name = "microsoft/phi-2"  # 2.7B параметров - подходит для RTX 3080

print("Загрузка модели...")
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,  # FP16 для экономии памяти
    device_map="cuda"  # Использовать GPU
)

print("Модель загружена на GPU!")

# Генерация текста
prompt = "What is artificial intelligence?"
inputs = tokenizer(prompt, return_tensors="pt").to("cuda")

outputs = model.generate(
    **inputs,
    max_length=100,
    temperature=0.7
)

response = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(f"\nPrompt: {prompt}")
print(f"Response: {response}")

# Более мощные модели (требуют больше VRAM)
models = [
    "microsoft/phi-3-mini-4k-instruct",  # 3.8B
    "meta-llama/Llama-3.2-3B",          # 3B (нужен токен HF)
    "google/gemma-2b",                   # 2B
]

# Модели с лучшей поддержкой русского:
model_name = "bigscience/bloomz-560m"  # Меньше, но мультиязычная
model_name = "facebook/opt-1.3b"        # Хорошо для диалогов

# Интерактивный чат
while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    # ... генерация ответа
