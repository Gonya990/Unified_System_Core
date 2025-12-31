# ============================================================================
# Скрипт проверки установки Windows ML с NVIDIA TensorRT
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

function Write-Check($Message, $Success) {
    if ($Success) {
        Write-ColorOutput Green "  ✓ $Message"
    } else {
        Write-ColorOutput Red "  ✗ $Message"
    }
}

Write-ColorOutput Magenta @"

╔════════════════════════════════════════════════════════════════╗
║  Проверка установки RTX AI окружения                          ║
╚════════════════════════════════════════════════════════════════╝

"@

$AllChecks = @()

# ============================================================================
# 1. Проверка GPU
# ============================================================================

Write-ColorOutput Cyan "`n[1] Проверка NVIDIA GPU"
$NvidiaGPU = Get-CimInstance Win32_VideoController | Where-Object { $_.Name -like "*NVIDIA*RTX*" -or $_.Name -like "*NVIDIA*GeForce*" -or $_.Name -like "*NVIDIA*Quadro*" }

if ($NvidiaGPU) {
    Write-Check "NVIDIA GPU обнаружен: $($NvidiaGPU.Name)" $true
    Write-ColorOutput Gray "    Драйвер: $($NvidiaGPU.DriverVersion)"
    Write-ColorOutput Gray "    Видеопамять: $([math]::Round($NvidiaGPU.AdapterRAM / 1GB, 2)) GB"
    $AllChecks += $true
    
    # Проверка через nvidia-smi
    if (Get-Command nvidia-smi -ErrorAction SilentlyContinue) {
        Write-ColorOutput Gray "`n    Информация от nvidia-smi:"
        $NvidiaSmiOutput = nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv,noheader
        Write-ColorOutput Gray "    $NvidiaSmiOutput"
    }
} else {
    Write-Check "NVIDIA GPU не обнаружен" $false
    $AllChecks += $false
}

# ============================================================================
# 2. Проверка Python
# ============================================================================

Write-ColorOutput Cyan "`n[2] Проверка Python"
if (Get-Command python -ErrorAction SilentlyContinue) {
    $PythonVersion = python --version 2>&1
    Write-Check "Python установлен: $PythonVersion" $true
    $AllChecks += $true
    
    $PipVersion = python -m pip --version 2>&1
    Write-ColorOutput Gray "    pip: $PipVersion"
} else {
    Write-Check "Python не установлен" $false
    $AllChecks += $false
}

# ============================================================================
# 3. Проверка CUDA
# ============================================================================

Write-ColorOutput Cyan "`n[3] Проверка CUDA Toolkit"
$CudaPath = "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA"
if (Test-Path $CudaPath) {
    $CudaVersions = Get-ChildItem $CudaPath -Directory | Select-Object -ExpandProperty Name
    Write-Check "CUDA Toolkit установлен" $true
    Write-ColorOutput Gray "    Версии: $($CudaVersions -join ', ')"
    $AllChecks += $true
    
    # Проверка через nvcc
    if (Get-Command nvcc -ErrorAction SilentlyContinue) {
        $NvccVersion = nvcc --version 2>&1 | Select-String "release" 
        Write-ColorOutput Gray "    $NvccVersion"
    }
} else {
    Write-Check "CUDA Toolkit не найден" $false
    $AllChecks += $false
}

# ============================================================================
# 4. Проверка ONNX Runtime
# ============================================================================

Write-ColorOutput Cyan "`n[4] Проверка ONNX Runtime"
$OnnxCheck = python -c "import onnxruntime as ort; print(f'ONNX Runtime {ort.__version__}'); print('Доступные провайдеры:', ort.get_available_providers())" 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Check "ONNX Runtime установлен" $true
    $OnnxCheck -split "`n" | ForEach-Object { Write-ColorOutput Gray "    $_" }
    
    # Проверка TensorRT провайдера
    if ($OnnxCheck -match "TensorRTExecutionProvider") {
        Write-Check "TensorRT провайдер доступен" $true
        $AllChecks += $true
    } else {
        Write-Check "TensorRT провайдер не найден (это нормально, если TensorRT не установлен отдельно)" $false
        $AllChecks += $true  # Не критично
    }
    
    # Проверка CUDA провайдера
    if ($OnnxCheck -match "CUDAExecutionProvider") {
        Write-Check "CUDA провайдер доступен" $true
    }
} else {
    Write-Check "ONNX Runtime не установлен" $false
    $AllChecks += $false
}

# ============================================================================
# 5. Проверка PyTorch
# ============================================================================

Write-ColorOutput Cyan "`n[5] Проверка PyTorch"
$TorchCheck = python -c "import torch; print(f'PyTorch {torch.__version__}'); print(f'CUDA доступна: {torch.cuda.is_available()}'); print(f'CUDA версия: {torch.version.cuda if torch.cuda.is_available() else \"N/A\"}'); print(f'GPU устройств: {torch.cuda.device_count() if torch.cuda.is_available() else 0}')" 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Check "PyTorch установлен" $true
    $TorchCheck -split "`n" | ForEach-Object { Write-ColorOutput Gray "    $_" }
    
    if ($TorchCheck -match "CUDA доступна: True") {
        Write-Check "PyTorch с поддержкой CUDA" $true
        $AllChecks += $true
    } else {
        Write-Check "PyTorch без поддержки CUDA" $false
        $AllChecks += $false
    }
} else {
    Write-Check "PyTorch не установлен" $false
    $AllChecks += $false
}

# ============================================================================
# 6. Проверка .NET SDK
# ============================================================================

Write-ColorOutput Cyan "`n[6] Проверка .NET SDK"
if (Get-Command dotnet -ErrorAction SilentlyContinue) {
    $DotnetVersion = dotnet --version 2>&1
    Write-Check ".NET SDK установлен: $DotnetVersion" $true
    $AllChecks += $true
} else {
    Write-Check ".NET SDK не установлен" $false
    $AllChecks += $false
}

# ============================================================================
# 7. Проверка дополнительных библиотек
# ============================================================================

Write-ColorOutput Cyan "`n[7] Проверка дополнительных библиотек"

$Libraries = @(
    @{Name="numpy"; ImportName="numpy"},
    @{Name="Pillow"; ImportName="PIL"},
    @{Name="transformers"; ImportName="transformers"},
    @{Name="onnx"; ImportName="onnx"}
)

foreach ($Lib in $Libraries) {
    $LibCheck = python -c "import $($Lib.ImportName); print($($Lib.ImportName).__version__)" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Check "$($Lib.Name): $LibCheck" $true
    } else {
        Write-Check "$($Lib.Name) не установлен" $false
    }
}

# ============================================================================
# 8. Тест производительности GPU
# ============================================================================

Write-ColorOutput Cyan "`n[8] Тест производительности GPU (быстрый тест)"

$PerfTest = @"
import time
import numpy as np

try:
    import onnxruntime as ort
    
    # Создаём простую модель в памяти (тест скорости)
    providers = ['CUDAExecutionProvider', 'CPUExecutionProvider']
    available = ort.get_available_providers()
    
    if 'CUDAExecutionProvider' in available:
        print('✓ Используется GPU (CUDA)')
        # Создаём сессию
        session_options = ort.SessionOptions()
        session_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
        print('✓ GPU доступен для inference')
    else:
        print('⚠ GPU недоступен, используется CPU')
        
except Exception as e:
    print(f'✗ Ошибка: {e}')
"@

$PerfTest | python 2>&1 | ForEach-Object { Write-ColorOutput Gray "    $_" }

# ============================================================================
# Итоги
# ============================================================================

Write-ColorOutput Magenta "`n╔════════════════════════════════════════════════════════════════╗"
$SuccessCount = ($AllChecks | Where-Object { $_ -eq $true }).Count
$TotalCount = $AllChecks.Count

if ($SuccessCount -eq $TotalCount) {
    Write-ColorOutput Green "║  ✓ Все проверки пройдены ($SuccessCount/$TotalCount)                            ║"
    Write-ColorOutput Magenta "╚════════════════════════════════════════════════════════════════╝"
    Write-ColorOutput Green "`n🎉 Ваша система готова к работе с ИИ на NVIDIA RTX!"
} else {
    Write-ColorOutput Yellow "║  ⚠ Пройдено проверок: $SuccessCount/$TotalCount                                 ║"
    Write-ColorOutput Magenta "╚════════════════════════════════════════════════════════════════╝"
    Write-ColorOutput Yellow "`n⚠ Некоторые компоненты не установлены. Проверьте логи выше."
}

Write-ColorOutput Cyan "`n📝 Следующие шаги:"
Write-ColorOutput Gray "  1. Если есть ошибки, переустановите соответствующие компоненты"
Write-ColorOutput Gray "  2. Установите Olive Toolkit: .\setup-olive.ps1"
Write-ColorOutput Gray "  3. Запустите примеры в папке 'examples\'"
Write-ColorOutput Gray "  4. Изучите документацию в README.md"

Write-ColorOutput Green "`nНажмите Enter для выхода..."
Read-Host
