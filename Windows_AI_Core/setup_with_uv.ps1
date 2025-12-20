# Setup Environment with UV (Project Sync)
# Run this on your Windows Machine in PowerShell

Write-Host "🚀 Setting up Windows AI Core with 'uv' Package Manager..." -ForegroundColor Cyan

# 1. Install 'uv' if missing
if (-not (Get-Command "uv" -ErrorAction SilentlyContinue)) {
    Write-Host "Installing uv..." -ForegroundColor Yellow
    powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path", "User") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "Machine")
}

# 2. Sync Dependencies from pyproject.toml
Write-Host "Syncing Project Dependencies (including PyTorch CUDA)..." -ForegroundColor Yellow
uv sync

Write-Host "`n✅ Environment Ready!" -ForegroundColor Green
Write-Host "To Start the Bot:" -ForegroundColor White
Write-Host "   uv run python ai_telegram_bot.py" -ForegroundColor Cyan
