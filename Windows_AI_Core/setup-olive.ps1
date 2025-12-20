# ============================================================================
# Скрипт установки Olive Toolkit
# ============================================================================
# Olive - это инструмент оптимизации моделей от Microsoft
# Поддерживает оптимизацию для CPU, NPU и GPU (NVIDIA RTX)
# ============================================================================

# Установка кодировки UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

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

Write-ColorOutput Magenta @"

╔════════════════════════════════════════════════════════════════╗
║  Установка Olive Toolkit                                      ║
║  Инструмент оптимизации моделей для Windows ML                ║
╚════════════════════════════════════════════════════════════════╝

"@

# ============================================================================
# 1. Проверка Python
# ============================================================================

Write-Step "Шаг 1: Проверка Python"

if (!(Get-Command python -ErrorAction SilentlyContinue)) {
    Write-ColorOutput Red "Python не найден! Сначала запустите setup-rtx-ai-environment.ps1"
    exit 1
}

$PythonVersion = python --version
Write-Info "✓ Python установлен: $PythonVersion"

# ============================================================================
# 2. Установка Olive
# ============================================================================

Write-Step "Шаг 2: Установка Olive Toolkit"

Write-Info "Установка olive-ai..."
python -m pip install olive-ai --upgrade

Write-Info "Установка дополнительных зависимостей для ONNX Runtime..."
python -m pip install olive-ai[onnxruntime] --upgrade

Write-Info "Установка зависимостей для оптимизации..."
python -m pip install olive-ai[optimize] --upgrade

Write-Info "✓ Olive Toolkit установлен"

# ============================================================================
# 3. Установка дополнительных инструментов
# ============================================================================

Write-Step "Шаг 3: Установка дополнительных инструментов"

Write-Info "Установка onnxruntime-extensions..."
python -m pip install onnxruntime-extensions

Write-Info "Установка onnx-simplifier..."
python -m pip install onnx-simplifier

Write-Info "✓ Дополнительные инструменты установлены"

# ============================================================================
# 4. Проверка установки
# ============================================================================

Write-Step "Шаг 4: Проверка установки"

$OliveCheck = python -c "import olive; print(f'Olive версия: {olive.__version__}')" 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Info "✓ $OliveCheck"
} else {
    Write-ColorOutput Red "✗ Ошибка при проверке Olive"
    Write-ColorOutput Red $OliveCheck
}

# ============================================================================
# 5. Создание примеров конфигурации
# ============================================================================

Write-Step "Шаг 5: Создание примеров конфигурации"

$ConfigsDir = ".\configs"
if (!(Test-Path $ConfigsDir)) {
    New-Item -ItemType Directory -Path $ConfigsDir | Out-Null
}

# Пример конфигурации для оптимизации модели
$OliveConfigExample = @"
{
    "input_model": {
        "type": "PyTorchModel",
        "model_path": "model.onnx"
    },
    "systems": {
        "local_system": {
            "type": "LocalSystem",
            "accelerators": [
                {
                    "device": "gpu",
                    "execution_providers": [
                        "TensorrtExecutionProvider",
                        "CUDAExecutionProvider"
                    ]
                }
            ]
        }
    },
    "evaluators": {
        "common_evaluator": {
            "metrics": [
                {
                    "name": "latency",
                    "type": "latency",
                    "sub_types": [
                        {"name": "avg", "priority": 1}
                    ]
                }
            ]
        }
    },
    "passes": {
        "onnx_quantization": {
            "type": "OnnxQuantization",
            "data_dir": "calibration_data"
        },
        "onnx_dynamic_quantization": {
            "type": "OnnxDynamicQuantization"
        },
        "convert": {
            "type": "OnnxConversion"
        },
        "optimize": {
            "type": "OrtTransformersOptimization",
            "model_type": "bert"
        }
    },
    "engine": {
        "search_strategy": {
            "execution_order": "joint",
            "search_algorithm": "tpe"
        },
        "evaluator": "common_evaluator",
        "target": "local_system",
        "cache_dir": "cache",
        "output_dir": "output"
    }
}
"@

$OliveConfigExample | Out-File -FilePath "$ConfigsDir\olive-config-gpu-optimization.json" -Encoding UTF8
Write-Info "✓ Создан пример конфигурации: configs\olive-config-gpu-optimization.json"

# Упрощённая конфигурация для быстрой оптимизации
$SimpleConfig = @"
{
    "input_model": {
        "type": "OnnxModel",
        "model_path": "model.onnx"
    },
    "systems": {
        "local_system": {
            "type": "LocalSystem",
            "accelerators": [
                {
                    "device": "gpu",
                    "execution_providers": ["CUDAExecutionProvider"]
                }
            ]
        }
    },
    "passes": {
        "optimize": {
            "type": "OrtTransformersOptimization"
        }
    },
    "engine": {
        "target": "local_system",
        "cache_dir": "cache",
        "output_dir": "optimized_model"
    }
}
"@

$SimpleConfig | Out-File -FilePath "$ConfigsDir\olive-config-simple.json" -Encoding UTF8
Write-Info "✓ Создан простой пример: configs\olive-config-simple.json"

# ============================================================================
# Завершение
# ============================================================================

Write-ColorOutput Magenta @"

╔════════════════════════════════════════════════════════════════╗
║  ✓ Olive Toolkit установлен успешно!                          ║
╚════════════════════════════════════════════════════════════════╝

"@

Write-Step "Использование Olive:"
Write-Info "1. Для оптимизации модели используйте:"
Write-Info "   python -m olive.workflows.run --config your_config.json"
Write-Info ""
Write-Info "2. Примеры конфигураций созданы в папке 'configs\'"
Write-Info ""
Write-Info "3. Документация Olive:"
Write-Info "   https://github.com/microsoft/Olive"

Write-ColorOutput Green "`nНажмите Enter для выхода..."
Read-Host
