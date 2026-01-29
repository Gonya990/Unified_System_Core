# Wrapper to run full Windows install and checks.
# Run as administrator in PowerShell
[CmdletBinding()]
param(
    [switch]$SkipVerify,
    [switch]$SkipOlive,
    [switch]$DryRun,
    [switch]$NoReboot,
    [string]$LogPath = "$PSScriptRoot\logs"
)

# Check for administrator rights (only enforce on Windows)
if ($IsWindows) {
    if (-not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
        Write-Host "This script must be run as Administrator. Right click PowerShell and 'Run as Administrator'." -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "Not running on Windows host: admin checks are skipped. DryRun recommended." -ForegroundColor Yellow
    if (-not $DryRun) {
        Write-Host "Non-Windows host detected — only DryRun is safe. Use -DryRun to test this script." -ForegroundColor Red
        exit 1
    }
}

Set-StrictMode -Version Latest
Set-PSDebug -Strict
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force

$ScriptDir = Split-Path -Path $MyInvocation.MyCommand.Definition -Parent
Write-Host "Running Windows install wrapper from: $ScriptDir" -ForegroundColor Green

$LogDir = $LogPath
if (!(Test-Path $LogDir)) { New-Item -ItemType Directory -Path $LogDir | Out-Null }
$LogFile = "$LogDir\run_all_windows-$(Get-Date -Format 'yyyyMMdd-HHmmss').log"
Write-Host "Logging to: $LogFile" -ForegroundColor Cyan

if ($DryRun) { Write-Host "DRY RUN: No changes will be made" -ForegroundColor Yellow }

function Run-Or-Describe($ScriptPath, $Description) {
    if (!(Test-Path $ScriptPath)) {
        Write-Host "${Description} not found: $ScriptPath" -ForegroundColor Red
        return $false
    }
    Write-Host "Executing: $ScriptPath - $Description" -ForegroundColor Cyan
    if ($DryRun) { Write-Host "DRY-RUN: would execute $ScriptPath" -ForegroundColor Yellow; return $true }
    & $ScriptPath
    return $true
}

# Run the main installer
if (!(Run-Or-Describe "$ScriptDir\setup-rtx-ai-environment.ps1" "Main setup script")) { exit 1 }

# Offer a reboot prompt after install
Write-Host "Installation finished - consider rebooting if prompted by installer." -ForegroundColor Yellow
if (-not $NoReboot -and -not $DryRun) {
    $choice = Read-Host "Reboot now? (yes/no)"
    if ($choice -match '^(y|yes)$') { Restart-Computer }
} else {
    if ($DryRun) { Write-Host "DRY-RUN: Would prompt for reboot after install" -ForegroundColor Yellow }
    if ($NoReboot) { Write-Host "NoReboot flag set, skipping reboot prompt" -ForegroundColor Yellow }
}

# Optionally run verification script
if (-not $SkipVerify) {
    if (!(Run-Or-Describe "$ScriptDir\verify-installation.ps1" "Verification script")) {
        Write-Host "verify-installation.ps1 not found or failed - skipping verification." -ForegroundColor Yellow
    }
} else { Write-Host "Skipping verification as requested." -ForegroundColor Yellow }

# Optionally setup Olive
if (-not $SkipOlive) {
    if (!(Run-Or-Describe "$ScriptDir\setup-olive.ps1" "Olive setup script")) {
        Write-Host "setup-olive.ps1 not found - skipping Olive installation." -ForegroundColor Yellow
    }
} else { Write-Host "Skipping Olive installation as requested." -ForegroundColor Yellow }

# Activate venv and run a quick Python smoke test
$VenvPath = "$ScriptDir\venv"
if (Test-Path $VenvPath) {
    Write-Host "Activating venv: $VenvPath" -ForegroundColor Cyan
    if ($DryRun) { Write-Host "DRY-RUN: would activate venv and run smoke tests" -ForegroundColor Yellow }
    else {
        & "$VenvPath\Scripts\Activate.ps1"
        Write-Host "Running Python quick GPU check..." -ForegroundColor Cyan
        python -c "import torch; print('torch.cuda.is_available():', torch.cuda.is_available())"
        python -c "import onnxruntime as ort; print('ONNX providers:', ort.get_available_providers())"
    }
} else {
    Write-Host "Virtual environment not found - skip Python smoke tests." -ForegroundColor Yellow
}

Write-Host "=== RUN ALL COMPLETE ===" -ForegroundColor Green
Read-Host -Prompt "Press Enter to exit"