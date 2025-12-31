# ============================================================================
# Olive Toolkit Setup - Simple Version (English)
# ============================================================================

Write-Host "`n========================================" -ForegroundColor Magenta
Write-Host "  Installing Olive Toolkit" -ForegroundColor Magenta
Write-Host "========================================`n" -ForegroundColor Magenta

# Check Python
if (!(Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "ERROR: Python not found!" -ForegroundColor Red
    Write-Host "Run setup-simple.ps1 first" -ForegroundColor Yellow
    exit 1
}

$PythonVersion = python --version
Write-Host "Python: $PythonVersion" -ForegroundColor Green

# Install Olive
Write-Host "`nInstalling olive-ai..." -ForegroundColor Cyan
python -m pip install olive-ai --upgrade

Write-Host "Installing olive extensions..." -ForegroundColor Cyan
python -m pip install "olive-ai[onnxruntime]" --upgrade

Write-Host "Installing optimization tools..." -ForegroundColor Cyan
python -m pip install onnxruntime-extensions onnx-simplifier

# Verify installation
Write-Host "`nVerifying installation..." -ForegroundColor Cyan
$OliveCheck = python -c "import olive; print(f'Olive version: {olive.__version__}')" 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host "SUCCESS: $OliveCheck" -ForegroundColor Green
} else {
    Write-Host "ERROR: Olive installation failed" -ForegroundColor Red
}

Write-Host "`n========================================" -ForegroundColor Magenta
Write-Host "  Installation Complete!" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Magenta

Write-Host "Usage:" -ForegroundColor Cyan
Write-Host "  python examples\python\optimize-model-example.py --model your_model.onnx" -ForegroundColor White

Write-Host "`nPress Enter to exit..." -ForegroundColor Green
Read-Host
