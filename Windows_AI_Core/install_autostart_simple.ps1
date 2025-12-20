# Script to add LLM chat bot to Windows startup
# Run with administrator privileges

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "Installing LLM Chat Bot Auto-Start" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

# Get startup folder path
$startupFolder = [System.Environment]::GetFolderPath('Startup')
Write-Host "`nStartup folder: $startupFolder" -ForegroundColor Yellow

# Create shortcut
$WshShell = New-Object -ComObject WScript.Shell
$shortcutPath = "$startupFolder\ChatLLM.lnk"
$shortcut = $WshShell.CreateShortcut($shortcutPath)

# Configure shortcut
$shortcut.TargetPath = "C:\Users\gonya\my-ai-project\start_chat.bat"
$shortcut.WorkingDirectory = "C:\Users\gonya\my-ai-project"
$shortcut.Description = "LLM Chat Bot on RTX 3080"
$shortcut.IconLocation = "C:\Windows\System32\shell32.dll,165"

# Save shortcut
$shortcut.Save()

Write-Host "`nDone!" -ForegroundColor Green
Write-Host "Chat bot will auto-start on Windows login" -ForegroundColor Green
Write-Host "`nShortcut created: $shortcutPath" -ForegroundColor Yellow

# Optional: create desktop shortcut
$desktopPath = [Environment]::GetFolderPath("Desktop")
$desktopShortcut = "$desktopPath\ChatLLM.lnk"
$shortcut2 = $WshShell.CreateShortcut($desktopShortcut)
$shortcut2.TargetPath = "C:\Users\gonya\my-ai-project\start_chat.bat"
$shortcut2.WorkingDirectory = "C:\Users\gonya\my-ai-project"
$shortcut2.Description = "LLM Chat Bot on RTX 3080"
$shortcut2.IconLocation = "C:\Windows\System32\shell32.dll,165"
$shortcut2.Save()

Write-Host "Desktop shortcut: $desktopShortcut" -ForegroundColor Yellow
Write-Host "`nYou can now launch chat with double-click!" -ForegroundColor Green
