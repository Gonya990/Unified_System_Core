# ============================================================================
# Скрипт установки Windows ML с NVIDIA TensorRT для RTX
# ============================================================================
# Этот скрипт автоматизирует установку всех необходимых компонентов
# для работы с ИИ на Windows ПК с NVIDIA RTX GPU
# ============================================================================

# Требуется запуск от имени администратора
#Requires -RunAsAdministrator

# Установка кодировки UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

# Цвета для вывода
function Write-ColorOutput($ForegroundColor, $Message) {
    $fc = $host.UI.RawUI.ForegroundColor
    $host.UI.RawUI.ForegroundColor = $ForegroundColor
    Write-Output $Message
    $host.UI.RawUI.ForegroundColor = $fc
}

function Write-Step($Message) {
    Write-ColorOutput Green "`n==> $Message"
}

function Write-Info($Message) {
    Write-ColorOutput Cyan "    $Message"
}

function Write-Warning($Message) {
    Write-ColorOutput Yellow "    [ВНИМАНИЕ] $Message"
}

function Write-Error($Message) {
    Write-ColorOutput Red "    [ОШИБКА] $Message"
}

# Создание папки для логов
$LogDir = "logs"
if (!(Test-Path $LogDir)) {
    New-Item -ItemType Directory -Path $LogDir | Out-Null
}

$LogFile = "$LogDir\setup-$(Get-Date -Format 'yyyyMMdd-HHmmss').log"
Start-Transcript -Path $LogFile

Write-ColorOutput Magenta @"

╔════════════════════════════════════════════════════════════════╗
║  Установка Windows ML с NVIDIA TensorRT для RTX                ║
║  Настройка ИИ окружения для NVIDIA RTX GPU                     ║
╚════════════════════════════════════════════════════════════════╝

"@

# ============================================================================
# 1. Проверка системы
# ============================================================================

Write-Step "Шаг 1: Проверка системы"

# Проверка версии Windows
$OSInfo = Get-CimInstance Win32_OperatingSystem
Write-Info "ОС: $($OSInfo.Caption) $($OSInfo.Version)"

if ([Environment]::Is64BitOperatingSystem) {
    Write-Info "✓ 64-битная система"
} else {
    Write-Error "Требуется 64-битная версия Windows"
    exit 1
}

# Проверка NVIDIA GPU
Write-Info "Поиск NVIDIA GPU..."
$NvidiaGPU = Get-CimInstance Win32_VideoController | Where-Object { $_.Name -like "*NVIDIA*" }

if ($NvidiaGPU) {
    Write-Info "✓ Обнаружен GPU: $($NvidiaGPU.Name)"
    Write-Info "  Драйвер: $($NvidiaGPU.DriverVersion)"
    Write-Info "  Видеопамять: $([math]::Round($NvidiaGPU.AdapterRAM / 1GB, 2)) GB"
} else {
    Write-Warning "NVIDIA GPU не обнаружен. Установка может не работать корректно."
}

# ============================================================================
# 2. Установка Chocolatey (менеджер пакетов для Windows)
# ============================================================================

Write-Step "Шаг 2: Установка Chocolatey"

if (!(Get-Command choco -ErrorAction SilentlyContinue)) {
    Write-Info "Установка Chocolatey..."
    Set-ExecutionPolicy Bypass -Scope Process -Force
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
    Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
    
    # Обновляем PATH
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
    
    Write-Info "✓ Chocolatey установлен"
} else {
    Write-Info "✓ Chocolatey уже установлен"
    choco upgrade chocolatey -y
}

# ============================================================================
# 3. Установка Python
# ============================================================================

Write-Step "Шаг 3: Установка Python 3.11"

if (!(Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Info "Установка Python 3.11..."
    choco install python311 -y
    
    # Обновляем PATH
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
    
    Write-Info "✓ Python установлен"
} else {
    $PythonVersion = python --version
    Write-Info "✓ Python уже установлен: $PythonVersion"
}

# Обновление pip
Write-Info "Обновление pip..."
python -m pip install --upgrade pip

# ============================================================================
# 4. Установка NVIDIA CUDA Toolkit (опционально, если не установлен)
# ============================================================================

Write-Step "Шаг 4: Проверка CUDA Toolkit"

$CudaPath = "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA"
if (Test-Path $CudaPath) {
    Write-Info "✓ CUDA Toolkit обнаружен"
    $CudaVersions = Get-ChildItem $CudaPath -Directory | Select-Object -ExpandProperty Name
    Write-Info "  Установленные версии: $($CudaVersions -join ', ')"
} else {
    Write-Warning "CUDA Toolkit не найден"
    Write-Info "Для установки CUDA Toolkit:"
    Write-Info "1. Перейдите на https://developer.nvidia.com/cuda-downloads"
    Write-Info "2. Скачайте CUDA Toolkit для Windows"
    Write-Info "3. Запустите установщик"
    Write-Info ""
    Write-Info "Нажмите Enter, чтобы продолжить установку остальных компонентов..."
    Read-Host
}

# ============================================================================
# 5. Установка Visual C++ Redistributables
# ============================================================================

Write-Step "Шаг 5: Установка Visual C++ Redistributables"

Write-Info "Установка Visual C++ Redistributable..."
choco install vcredist-all -y

# ============================================================================
# 6. Установка .NET SDK (для C# примеров)
# ============================================================================

Write-Step "Шаг 6: Установка .NET SDK"

if (!(Get-Command dotnet -ErrorAction SilentlyContinue)) {
    Write-Info "Установка .NET SDK..."
    choco install dotnet-sdk -y
    
    # Обновляем PATH
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
    
    Write-Info "✓ .NET SDK установлен"
} else {
    $DotnetVersion = dotnet --version
    Write-Info "✓ .NET SDK уже установлен: $DotnetVersion"
}

# ============================================================================
# 7. Установка ONNX Runtime с TensorRT
# ============================================================================

Write-Step "Шаг 7: Установка ONNX Runtime с TensorRT"

Write-Info "Установка ONNX Runtime GPU..."
python -m pip install onnxruntime-gpu --upgrade

Write-Info "Установка ONNX Runtime для работы с моделями..."
python -m pip install onnx numpy pillow

Write-Info "✓ ONNX Runtime установлен"

# ============================================================================
# 8. Установка дополнительных библиотек для работы с ИИ
# ============================================================================

Write-Step "Шаг 8: Установка дополнительных библиотек"

Write-Info "Установка PyTorch с CUDA поддержкой..."
python -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

Write-Info "Установка Transformers и других библиотек..."
python -m pip install transformers accelerate optimum

Write-Info "✓ Дополнительные библиотеки установлены"

# ============================================================================
# 9. Создание виртуального окружения для проектов
# ============================================================================

Write-Step "Шаг 9: Создание виртуального окружения"

$VenvPath = ".\venv"
if (!(Test-Path $VenvPath)) {
    Write-Info "Создание виртуального окружения..."
    python -m venv $VenvPath
    Write-Info "✓ Виртуальное окружение создано: $VenvPath"
    Write-Info ""
    Write-Info "Для активации виртуального окружения используйте:"
    Write-Info "  .\venv\Scripts\Activate.ps1"
} else {
    Write-Info "✓ Виртуальное окружение уже существует"
}

# ============================================================================
# 10. Создание примеров конфигурации
# ============================================================================

Write-Step "Шаг 10: Создание примеров конфигурации"

$ExamplesDir = ".\examples"
if (!(Test-Path $ExamplesDir)) {
    New-Item -ItemType Directory -Path $ExamplesDir | Out-Null
}

# Создание файла с переменными окружения
$EnvFile = ".\set-environment.ps1"
@"
# Скрипт для настройки переменных окружения

# CUDA
if (Test-Path "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA") {
    `$CudaPath = Get-ChildItem "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA" -Directory | Sort-Object Name -Descending | Select-Object -First 1
    `$env:CUDA_PATH = `$CudaPath.FullName
    `$env:CUDA_PATH_V12_1 = `$CudaPath.FullName
    Write-Host "CUDA_PATH установлен: `$env:CUDA_PATH" -ForegroundColor Green
}

# TensorRT (если установлен)
if (Test-Path "C:\Program Files\NVIDIA Corporation\TensorRT") {
    `$TensorRTPath = Get-ChildItem "C:\Program Files\NVIDIA Corporation\TensorRT" -Directory | Sort-Object Name -Descending | Select-Object -First 1
    `$env:TENSORRT_PATH = `$TensorRTPath.FullName
    Write-Host "TENSORRT_PATH установлен: `$env:TENSORRT_PATH" -ForegroundColor Green
}

# ONNX Runtime
`$env:ORT_TENSORRT_FP16_ENABLE = "1"
`$env:ORT_TENSORRT_ENGINE_CACHE_ENABLE = "1"
`$env:ORT_TENSORRT_CACHE_PATH = "`$PWD\tensorrt_cache"

Write-Host "Переменные окружения настроены" -ForegroundColor Green
"@ | Out-File -FilePath $EnvFile -Encoding UTF8

Write-Info "✓ Создан скрипт настройки окружения: $EnvFile"

# ============================================================================
# Завершение
# ============================================================================

Write-ColorOutput Magenta @"

╔════════════════════════════════════════════════════════════════╗
║  ✓ Установка завершена успешно!                               ║
╚════════════════════════════════════════════════════════════════╝

"@

Write-Step "Следующие шаги:"
Write-Info "1. Перезагрузите компьютер для применения всех изменений"
Write-Info "2. Запустите .\verify-installation.ps1 для проверки установки"
Write-Info "3. Установите Olive Toolkit: .\setup-olive.ps1"
Write-Info "4. Изучите примеры в папке 'examples\'"
Write-Info ""
Write-Info "Для настройки переменных окружения:"
Write-Info "  . .\set-environment.ps1"
Write-Info ""
Write-Info "Лог установки сохранён в: $LogFile"

Stop-Transcript

Write-ColorOutput Green "`nНажмите Enter для выхода..."
Read-Host
