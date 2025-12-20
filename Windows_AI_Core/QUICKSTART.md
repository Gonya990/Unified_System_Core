# Быстрый старт: Настройка Windows ПК с NVIDIA RTX для ИИ

## Шаг 1: Подключение к Windows ПК с вашего Mac

### Вариант A: Microsoft Remote Desktop (Рекомендуется для начальной настройки)

```bash
# На вашем Mac
brew install --cask microsoft-remote-desktop
```

Затем:
1. Запустите Microsoft Remote Desktop
2. Нажмите "+" → "Add PC"
3. Введите IP адрес вашего Windows ПК
4. Введите учётные данные Windows

### Вариант B: SSH (Для командной строки)

На Windows ПК (от администратора):
```powershell
# Установите OpenSSH Server
Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0
Start-Service sshd
Set-Service -Name sshd -StartupType 'Automatic'
```

На вашем Mac:
```bash
# Подключение
ssh username@windows-pc-ip

# Копирование файлов
scp -r windows-rtx-ai-setup username@windows-pc-ip:C:/Users/username/
```

## Шаг 2: Копирование файлов на Windows ПК

### Через RDP:
1. В настройках подключения RDP включите "Folder Redirection"
2. Выберите папку `windows-rtx-ai-setup`
3. На Windows эта папка появится как сетевой диск
4. Скопируйте на локальный диск Windows

### Через SCP:
```bash
# На вашем Mac
scp -r ~/Applications/VSCode/windows-rtx-ai-setup username@windows-ip:C:/Users/username/
```

## Шаг 3: Запуск установки на Windows ПК

1. Подключитесь к Windows через RDP
2. Откройте **PowerShell от имени администратора**
3. Перейдите в папку:
   ```powershell
   cd C:\Users\YourUsername\windows-rtx-ai-setup
   ```

4. Разрешите выполнение скриптов:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

5. Запустите основной скрипт установки:
   ```powershell
   .\setup-rtx-ai-environment.ps1
   ```

6. Дождитесь завершения (может занять 15-30 минут)

7. **Перезагрузите компьютер**

## Шаг 4: Проверка установки

После перезагрузки:

```powershell
cd C:\Users\YourUsername\windows-rtx-ai-setup
.\verify-installation.ps1
```

Скрипт проверит:
- ✓ NVIDIA GPU и драйверы
- ✓ Python и pip
- ✓ CUDA Toolkit
- ✓ ONNX Runtime с GPU поддержкой
- ✓ PyTorch с CUDA
- ✓ .NET SDK

## Шаг 5: Установка Olive Toolkit (оптимизация моделей)

```powershell
.\setup-olive.ps1
```

## Шаг 6: Тестирование с примерами

### Python примеры:

```powershell
# Базовый пример
python examples\python\onnx-runtime-basic.py

# С TensorRT оптимизацией
python examples\python\onnx-runtime-tensorrt.py
```

### C# пример:

```powershell
cd examples\csharp
dotnet run
```

## Шаг 7: Работа с вашими моделями

### Оптимизация существующей ONNX модели:

```powershell
python examples\python\optimize-model-example.py --model your_model.onnx --fp16
```

### Создание нового проекта:

**Python:**
```powershell
# Активируйте виртуальное окружение
.\venv\Scripts\Activate.ps1

# Создайте свой скрипт
notepad my_inference.py
```

**C#:**
```powershell
dotnet new console -n MyAIApp
cd MyAIApp
dotnet add package Microsoft.ML.OnnxRuntime.Gpu
```

## Решение проблем

### GPU не обнаружен

1. Проверьте драйверы NVIDIA:
   ```powershell
   nvidia-smi
   ```

2. Если команда не работает, установите последние драйверы:
   - https://www.nvidia.com/download/index.aspx

### Python показывает ошибку "No module named onnxruntime"

```powershell
python -m pip install onnxruntime-gpu --upgrade
```

### CUDA провайдер недоступен

Убедитесь что установлены:
1. Драйверы NVIDIA (последняя версия)
2. CUDA Toolkit
3. onnxruntime-gpu (не просто onnxruntime)

```powershell
# Переустановка
pip uninstall onnxruntime onnxruntime-gpu
pip install onnxruntime-gpu
```

## Полезные команды

### Проверка GPU:
```powershell
nvidia-smi
```

### Мониторинг GPU в реальном времени:
```powershell
nvidia-smi -l 1
```

### Проверка Python пакетов:
```powershell
python -c "import onnxruntime as ort; print(ort.get_available_providers())"
```

### Настройка переменных окружения для TensorRT:
```powershell
. .\set-environment.ps1
```

## Следующие шаги

1. **Изучите примеры** в папке `examples/`
2. **Прочитайте документацию** в `README.md`
3. **Оптимизируйте свои модели** с помощью Olive
4. **Настройте VS Code Remote SSH** для удобной разработки с Mac

## Дополнительные ресурсы

- 📖 [Полная документация](README.md)
- 🔌 [Руководство по удалённому подключению](remote-connection-guide.md)
- 💡 [Примеры кода](examples/README.md)
- 🌐 [Windows ML Documentation](https://learn.microsoft.com/windows/ai/windows-ml/)
- 🚀 [ONNX Runtime GitHub](https://github.com/microsoft/onnxruntime)

## Получение помощи

Если возникли проблемы:
1. Проверьте логи в папке `logs/`
2. Запустите `verify-installation.ps1` для диагностики
3. Обратитесь к разделу "Решение проблем" в документации
