# Build Dependencies using 'uv add'
# Run this to generate/update pyproject.toml via CLI commands

Write-Host "📦 Building Dependency File using 'uv add'..." -ForegroundColor Cyan

# 1. Initialize Project (if pyproject.toml doesn't exist)
if (-not (Test-Path "pyproject.toml")) {
    Write-Host "Initializing new uv project..."
    uv init --name windows-ai-core --app --no-workspace
}

# 2. Add PyTorch with CUDA 11.8 Index
# We use --index-url to tell uv where to look for this specific package
Write-Host "Adding PyTorch (CUDA 11.8)..."
uv add torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# 3. Add other libraries (Standard PyPI)
Write-Host "Adding Transformers and Accelerate..."
uv add transformers accelerate

Write-Host "`n✅ Dependecies added! Check 'pyproject.toml' to see changes." -ForegroundColor Green
Write-Host "To run the bot:"
Write-Host "   uv run python ai_telegram_bot.py"
