# ============================================================================
# Windows ML with NVIDIA TensorRT for RTX - Setup Script (English version)
# ============================================================================

#Requires -RunAsAdministrator

Write-Host "`n========================================" -ForegroundColor Magenta
Write-Host "Windows ML + TensorRT Setup for RTX GPU" -ForegroundColor Magenta
Write-Host "========================================`n" -ForegroundColor Magenta

# ============================================================================
# 1. Install Chocolatey
# ============================================================================

Write-Host "`n==> Installing Chocolatey..." -ForegroundColor Green

if (!(Get-Command choco -ErrorAction SilentlyContinue)) {
    Write-Host "    Installing Chocolatey package manager..." -ForegroundColor Cyan
    Set-ExecutionPolicy Bypass -Scope Process -Force
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
    Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
    
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
    
    Write-Host "    OK: Chocolatey installed" -ForegroundColor Green
} else {
    Write-Host "    OK: Chocolatey already installed" -ForegroundColor Green
    choco upgrade chocolatey -y
}

# ============================================================================
# 2. Install Python
# ============================================================================

Write-Host "`n==> Installing Python 3.11..." -ForegroundColor Green

if (!(Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "    Installing Python..." -ForegroundColor Cyan
    choco install python311 -y
    
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
    
    Write-Host "    OK: Python installed" -ForegroundColor Green
} else {
    $PythonVersion = python --version
    Write-Host "    OK: Python already installed: $PythonVersion" -ForegroundColor Green
}

Write-Host "    Upgrading pip..." -ForegroundColor Cyan
python -m pip install --upgrade pip

# ============================================================================
# 3. Install Visual C++ Redistributables
# ============================================================================

Write-Host "`n==> Installing Visual C++ Redistributables..." -ForegroundColor Green
choco install vcredist-all -y

# ============================================================================
# 4. Install .NET SDK
# ============================================================================

Write-Host "`n==> Installing .NET SDK..." -ForegroundColor Green

if (!(Get-Command dotnet -ErrorAction SilentlyContinue)) {
    Write-Host "    Installing .NET SDK..." -ForegroundColor Cyan
    choco install dotnet-sdk -y
    
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
    
    Write-Host "    OK: .NET SDK installed" -ForegroundColor Green
} else {
    $DotnetVersion = dotnet --version
    Write-Host "    OK: .NET SDK already installed: $DotnetVersion" -ForegroundColor Green
}

# ============================================================================
# 5. Install ONNX Runtime with GPU support
# ============================================================================

Write-Host "`n==> Installing ONNX Runtime GPU..." -ForegroundColor Green
python -m pip install onnxruntime-gpu --upgrade

Write-Host "    Installing ONNX tools..." -ForegroundColor Cyan
python -m pip install onnx numpy pillow

# ============================================================================
# 6. Install PyTorch with CUDA
# ============================================================================

Write-Host "`n==> Installing PyTorch with CUDA..." -ForegroundColor Green
python -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# ============================================================================
# 7. Install AI libraries
# ============================================================================

Write-Host "`n==> Installing AI libraries..." -ForegroundColor Green
python -m pip install transformers accelerate optimum

# ============================================================================
# 8. Create virtual environment
# ============================================================================

Write-Host "`n==> Creating virtual environment..." -ForegroundColor Green

$VenvPath = ".\venv"
if (!(Test-Path $VenvPath)) {
    Write-Host "    Creating venv..." -ForegroundColor Cyan
    python -m venv $VenvPath
    Write-Host "    OK: Virtual environment created: $VenvPath" -ForegroundColor Green
} else {
    Write-Host "    OK: Virtual environment already exists" -ForegroundColor Green
}

# ============================================================================
# 9. Create environment setup script
# ============================================================================

Write-Host "`n==> Creating environment setup script..." -ForegroundColor Green

$EnvFile = ".\set-environment.ps1"
@"
# Environment setup for Windows ML with TensorRT

# CUDA
if (Test-Path "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA") {
    `$CudaPath = Get-ChildItem "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA" -Directory | Sort-Object Name -Descending | Select-Object -First 1
    `$env:CUDA_PATH = `$CudaPath.FullName
    Write-Host "CUDA_PATH set: `$env:CUDA_PATH" -ForegroundColor Green
}

# TensorRT
if (Test-Path "C:\Program Files\NVIDIA Corporation\TensorRT") {
    `$TensorRTPath = Get-ChildItem "C:\Program Files\NVIDIA Corporation\TensorRT" -Directory | Sort-Object Name -Descending | Select-Object -First 1
    `$env:TENSORRT_PATH = `$TensorRTPath.FullName
    Write-Host "TENSORRT_PATH set: `$env:TENSORRT_PATH" -ForegroundColor Green
}

# ONNX Runtime TensorRT settings
`$env:ORT_TENSORRT_FP16_ENABLE = "1"
`$env:ORT_TENSORRT_ENGINE_CACHE_ENABLE = "1"
`$env:ORT_TENSORRT_CACHE_PATH = "`$PWD\tensorrt_cache"

Write-Host "Environment configured" -ForegroundColor Green
"@ | Out-File -FilePath $EnvFile -Encoding UTF8

Write-Host "    OK: Environment script created: $EnvFile" -ForegroundColor Green

# ============================================================================
# Completion
# ============================================================================

Write-Host "`n========================================" -ForegroundColor Magenta
Write-Host "Installation Complete!" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Magenta

Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Restart your computer" -ForegroundColor White
Write-Host "  2. Run: .\verify-installation.ps1" -ForegroundColor White
Write-Host "  3. Run: .\setup-olive.ps1" -ForegroundColor White
Write-Host "  4. Check examples in 'examples\' folder" -ForegroundColor White
Write-Host ""

Write-Host "Press Enter to exit..." -ForegroundColor Green
Read-Host
