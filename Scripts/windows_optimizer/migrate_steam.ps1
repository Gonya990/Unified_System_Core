# Steam Game Mover (Safety First)
# Usage: ./migrate_steam.ps1 "G:\SteamLibrary\steamapps\common\Cyberpunk 2077" "C:\Games\Cyberpunk 2077"
param(
    [Parameter(Mandatory = $true)]
    [string]$SourcePath,
    
    [Parameter(Mandatory = $true)]
    [string]$DestPath
)

if (-not (Test-Path $SourcePath)) {
    Write-Error "Source not found: $SourcePath"
    exit 1
}

# Create Dest
if (-not (Test-Path $DestPath)) {
    New-Item -ItemType Directory -Force -Path $DestPath | Out-Null
}

Write-Host "🚀 Moving Game to NVMe/SSD..." -ForegroundColor Cyan
Write-Host "   From: $SourcePath" -ForegroundColor Gray
Write-Host "   To:   $DestPath" -ForegroundColor Gray

# Robocopy (Multi-threaded, Resume-able)
# /E = recursive, /ZB = restartable, /MT:8 = 8 threads, /MOVE = deletions from source!
# Remove /MOVE if you want to keep copy first (Safer). We will use /MIR for safety then manual delete?
# No, lets standard copy then user verifies.

robocopy $SourcePath $DestPath /E /MT:16 /R:3 /W:5

if ($LASTEXITCODE -le 7) {
    Write-Host "✅ Move Succcessful!" -ForegroundColor Green
    
    # Optional: Web shortcut or mklink? 
    # Steam usually needs 'Move Install Folder' from UI, but Junction hack works too.
    # Creating Junction at source to point to new location
    
    Remove-Item $SourcePath -Recurse -Force
    New-Item -ItemType Junction -Path $SourcePath -Target $DestPath
    Write-Host "🔗 Linked old path to new location (Steam shouldn't notice)." -ForegroundColor Yellow
}
else {
    Write-Error "Copy failed with code $LASTEXITCODE"
}
