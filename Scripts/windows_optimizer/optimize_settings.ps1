# Windows Performance Optimization Script
# Applies High Performance Power Plan, Game Mode, and GPU Scheduling

Write-Host "Starting Windows Performance Tuning..." -ForegroundColor Cyan

# 1. Power Plan: Ultimate Performance
$HighPerfGuid = "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c" # High Performance standard
$UltPerfGuid = "e9a42b02-d5df-448d-aa00-03f14749eb61" # Ultimate Performance

# Try to duplicate Ultimate Performance scheme if it doesn't exist
$Schemes = powercfg /list
if ($Schemes -notmatch "Ultim") {
    powercfg /duplicatescheme $UltPerfGuid
}

# Set to Ultimate (or High if Ultimate fails)
powercfg /setactive $UltPerfGuid
if ($LASTEXITCODE -ne 0) {
    powercfg /setactive $HighPerfGuid
    Write-Host "Set Power Plan: High Performance" -ForegroundColor Yellow
}
else {
    Write-Host "Set Power Plan: Ultimate Performance" -ForegroundColor Green
}

# 2. Game Mode (Registry)
$RegPath = "HKCU:\Software\Microsoft\GameBar"
if (-not (Test-Path $RegPath)) { New-Item -Path $RegPath -Force | Out-Null }
Set-ItemProperty -Path $RegPath -Name "AllowAutoGameMode" -Value 1
Set-ItemProperty -Path $RegPath -Name "AutoGameModeEnabled" -Value 1
Write-Host "Enabled Game Mode" -ForegroundColor Green

# 3. GPU Priority for Games (Registry - Hardware Accelerated GPU Scheduling)
$GpuRegPath = "HKLM:\SYSTEM\CurrentControlSet\Control\GraphicsDrivers"
Set-ItemProperty -Path $GpuRegPath -Name "HwSchMode" -Value 2 -ErrorAction SilentlyContinue
# Value 2 = On. Requires Reboot.
Write-Host "Enabled Hardware Accel. GPU Scheduling (Requires Reboot)" -ForegroundColor Green

# 4. Disable Hibernation (Clear C: space)
powercfg /hibernate off
Write-Host "Disabled Hibernation (Freed NVMe Space)" -ForegroundColor Green

# 5. Network Throttling Disable
$NetPath = "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile"
Set-ItemProperty -Path $NetPath -Name "NetworkThrottlingIndex" -Value 0xffffffff
Write-Host "Disabled Network Throttling" -ForegroundColor Green

Write-Host "`nOptimization Complete. Please REBOOT to apply all changes." -ForegroundColor Cyan
