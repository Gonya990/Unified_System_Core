# Скрипт для добавления чат-бота в автозагрузку Windows
# Запускать с правами администратора

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "Установка автозапуска чат-бота LLM" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

# Путь к папке автозагрузки
$startupFolder = [System.Environment]::GetFolderPath('Startup')
Write-Host "`nПапка автозагрузки: $startupFolder" -ForegroundColor Yellow

# Создаем ярлык
$WshShell = New-Object -ComObject WScript.Shell
$shortcutPath = "$startupFolder\ChatLLM.lnk"
$shortcut = $WshShell.CreateShortcut($shortcutPath)

# Настройки ярлыка
$shortcut.TargetPath = "C:\Users\gonya\my-ai-project\start_chat.bat"
$shortcut.WorkingDirectory = "C:\Users\gonya\my-ai-project"
$shortcut.Description = "LLM Chat Bot on RTX 3080"
$shortcut.IconLocation = "C:\Windows\System32\shell32.dll,165"

# Сохраняем ярлык
$shortcut.Save()

Write-Host "`n✅ Готово!" -ForegroundColor Green
Write-Host "Чат-бот будет автоматически запускаться при входе в Windows" -ForegroundColor Green
Write-Host "`nЯрлык создан: $shortcutPath" -ForegroundColor Yellow

# Опционально: создать ярлык на рабочем столе
$desktopPath = [Environment]::GetFolderPath("Desktop")
$desktopShortcut = "$desktopPath\ChatLLM.lnk"
$shortcut2 = $WshShell.CreateShortcut($desktopShortcut)
$shortcut2.TargetPath = "C:\Users\gonya\my-ai-project\start_chat.bat"
$shortcut2.WorkingDirectory = "C:\Users\gonya\my-ai-project"
$shortcut2.Description = "LLM Chat Bot on RTX 3080"
$shortcut2.IconLocation = "C:\Windows\System32\shell32.dll,165"
$shortcut2.Save()

Write-Host "Ярлык на рабочем столе: $desktopShortcut" -ForegroundColor Yellow
Write-Host "`nТеперь можно запускать чат двойным кликом!" -ForegroundColor Green
