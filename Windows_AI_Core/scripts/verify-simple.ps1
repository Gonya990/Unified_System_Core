# ============================================================================
# Verification Script - Simple Version (English)
# ============================================================================

function Write-Section($Title) {
    Write-Host "`n========================================" -ForegroundColor Cyan
    Write-Host "  $Title" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
}

function Write-Check($Message, $Success) {
    if ($Success) {
        Write-Host "  OK: $Message" -ForegroundColor Green
    } else {
        Write-Host "  FAIL: $Message" -ForegroundColor Red
    }
}

Write-Host "`n========================================" -ForegroundColor Magenta
Write-Host "  RTX AI Environment Verification" -ForegroundColor Magenta
Write-Host "========================================`n" -ForegroundColor Magenta

$AllChecks = @()

# ============================================================================
# 1. Check GPU
# ============================================================================

Write-Section "1. Checking NVIDIA GPU"
$NvidiaGPU = Get-CimInstance Win32_VideoController | Where-Object { $_.Name -like "*NVIDIA*" }

if ($NvidiaGPU) {
    Write-Check "NVIDIA GPU found: $($NvidiaGPU.Name)" $true
    Write-Host "    Driver: $($NvidiaGPU.DriverVersion)" -ForegroundColor Gray
    $AllChecks += $true
    
    if (Get-Command nvidia-smi -ErrorAction SilentlyContinue) {
        Write-Host "`n    nvidia-smi output:" -ForegroundColor Gray
        nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv,noheader
    }
} else {
    Write-Check "NVIDIA GPU not found" $false
    $AllChecks += $false
}

# ============================================================================
# 2. Check Python
# ============================================================================

Write-Section "2. Checking Python"
if (Get-Command python -ErrorAction SilentlyContinue) {
    $PythonVersion = python --version 2>&1
    Write-Check "Python installed: $PythonVersion" $true
    $AllChecks += $true
} else {
    Write-Check "Python not installed" $false
    $AllChecks += $false
}

# ============================================================================
# 3. Check ONNX Runtime
# ============================================================================

Write-Section "3. Checking ONNX Runtime"
$OnnxCheck = python -c "import onnxruntime as ort; print(f'ONNX Runtime {ort.__version__}'); print('Providers:', ort.get_available_providers())" 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Check "ONNX Runtime installed" $true
    $OnnxCheck -split "`n" | ForEach-Object { Write-Host "    $_" -ForegroundColor Gray }
    
    if ($OnnxCheck -match "CUDAExecutionProvider") {
        Write-Check "CUDA provider available" $true
    }
    $AllChecks += $true
} else {
    Write-Check "ONNX Runtime not installed" $false
    $AllChecks += $false
}

# ============================================================================
# 4. Check PyTorch
# ============================================================================

Write-Section "4. Checking PyTorch"
$TorchCheck = python -c "import torch; print(f'PyTorch {torch.__version__}'); print(f'CUDA available: {torch.cuda.is_available()}'); print(f'GPU devices: {torch.cuda.device_count() if torch.cuda.is_available() else 0}')" 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Check "PyTorch installed" $true
    $TorchCheck -split "`n" | ForEach-Object { Write-Host "    $_" -ForegroundColor Gray }
    
    if ($TorchCheck -match "CUDA available: True") {
        Write-Check "PyTorch with CUDA support" $true
        $AllChecks += $true
    } else {
        Write-Check "PyTorch without CUDA" $false
        $AllChecks += $false
    }
} else {
    Write-Check "PyTorch not installed" $false
    $AllChecks += $false
}

# ============================================================================
# 5. Check .NET SDK
# ============================================================================

Write-Section "5. Checking .NET SDK"
if (Get-Command dotnet -ErrorAction SilentlyContinue) {
    $DotnetVersion = dotnet --version 2>&1
    Write-Check ".NET SDK installed: $DotnetVersion" $true
    $AllChecks += $true
} else {
    Write-Check ".NET SDK not installed" $false
    $AllChecks += $false
}

# ============================================================================
# Summary
# ============================================================================

Write-Host "`n========================================" -ForegroundColor Magenta
$SuccessCount = ($AllChecks | Where-Object { $_ -eq $true }).Count
$TotalCount = $AllChecks.Count

if ($SuccessCount -eq $TotalCount) {
    Write-Host "  SUCCESS: All checks passed ($SuccessCount/$TotalCount)" -ForegroundColor Green
    Write-Host "========================================`n" -ForegroundColor Magenta
    Write-Host "Your system is ready for AI on RTX!" -ForegroundColor Green
} else {
    Write-Host "  WARNING: Passed $SuccessCount/$TotalCount checks" -ForegroundColor Yellow
    Write-Host "========================================`n" -ForegroundColor Magenta
}

Write-Host "`nNext steps:" -ForegroundColor Cyan
Write-Host "  1. Install Olive: powershell -File setup-olive-simple.ps1" -ForegroundColor White
Write-Host "  2. Run examples: cd examples\python && python onnx-runtime-basic.py" -ForegroundColor White

Write-Host "`nPress Enter to exit..." -ForegroundColor Green
Read-Host
