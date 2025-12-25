---
description: Analyze and cleanup large ZIP archives on Windows PC
---

# Windows Archive Cleanup Workflow

# Рабочий процесс очистки архивов Windows

**English:** This workflow helps you analyze large ZIP archives on your Windows PC drives (G/D/F/H), identify useful content, and safely delete unnecessary files.

**Russian:** Этот рабочий процесс помогает анализировать большие ZIP архивы на дисках вашего Windows PC (G/D/F/H), определять полезное содержимое и безопасно удалять ненужные файлы.

## Prerequisites | Предварительные требования

1. **Windows PC Access** | **Доступ к Windows PC**
   - SSH or Remote Desktop access
   - Tailscale connection (recommended)
   - Or physical access to the machine

2. **Software Requirements** | **Требования к ПО**
   - PowerShell 5.1+
   - Python 3.8+ (optional, for advanced analysis)
   - 7-Zip or WinRAR

3. **Permissions** | **Разрешения**
   - Read access to drives G, D, F, H
   - Write access for creating reports
   - Delete permissions (for cleanup phase)

## Steps | Шаги

### 1. Deploy Scripts to Windows PC | Развертывание скриптов на Windows PC

**English:** Copy the analyzer scripts to your Windows PC:

**Russian:** Скопируйте скрипты анализатора на ваш Windows PC:

**Option A: Using Tailscale/SSH**

```bash
# From Mac
scp -r Scripts/windows_archive_analyzer user@windows-pc:C:/Users/user/
```

**Option B: Manual Copy**

- Download the Scripts/windows_archive_analyzer folder
- Copy to Windows PC via USB/network share
- Place in C:\Users\user\archive_analyzer

### 2. Configure Scan Settings | Настройте параметры сканирования

**English:** Edit `config.json` on Windows PC:

**Russian:** Отредактируйте `config.json` на Windows PC:

```powershell
# On Windows PC
cd C:\Users\user\archive_analyzer
notepad config.json
```

Verify:

- Drives to scan (G:, D:, F:, H:)
- Minimum file size
- Exclusion patterns
- File types to preserve

### 3. Run Initial Scan | Запустите первоначальное сканирование

**English:** Execute the scan script:

**Russian:** Выполните скрипт сканирования:

```powershell
.\scan_archives.ps1 -Verbose
```

This will:

- Scan all specified drives
- Find ZIP/7Z/RAR files above size threshold
- Create catalog with metadata
- Save results to `reports/scan_YYYYMMDD_HHMMSS.json`

Expected time: 10-30 minutes depending on drive size

Ожидаемое время: 10-30 минут в зависимости от размера дисков

### 4. Review Scan Results | Проверьте результаты сканирования

**English:** Open the generated report:

**Russian:** Откройте сгенерированный отчет:

```powershell
# View report summary
Get-Content reports\scan_*.json | ConvertFrom-Json | 
    Select-Object TotalCount, TotalSizeGB, Timestamp
```

**Questions to answer:**

- How many archives were found?
- What's the total size?
- Which drives have the most archives?
- Any immediate patterns (old files, duplicates)?

### 5. Analyze Content (Optional) | Анализ содержимого (опционально)

**English:** For deeper analysis, run the Python analyzer:

**Russian:** Для более глубокого анализа запустите Python анализатор:

```powershell
python analyze_content.py reports\scan_LATEST.json
```

This provides:

- Duplicate detection
- Content categorization
- Age-based recommendations
- Size optimization suggestions

### 6. Review Analysis Report | Проверьте отчет анализа

**English:** Open the HTML report in browser:

**Russian:** Откройте HTML отчет в браузере:

```powershell
start reports\analysis_*.html
```

Review each category:

- **Keep** - Unique, recent, important
- **Review** - Needs manual decision
- **Delete** - Safe to remove

### 7. Preview Cleanup | Предварительный просмотр очистки

**English:** Run cleanup in preview mode first:

**Russian:** Сначала запустите очистку в режиме предварительного просмотра:

```powershell
.\cleanup_archives.ps1 -Mode Preview
```

This shows what WOULD be deleted without actually deleting.

Это покажет, что БУДЕТ удалено, не удаляя на самом деле.

### 8. Backup Important Data | Резервное копирование важных данных

**English:** Before deletion, ensure backups:

**Russian:** Перед удалением убедитесь в наличии резервных копий:

```powershell
# Create backup metadata (file list, hashes)
.\cleanup_archives.ps1 -Mode CreateBackupMetadata
```

### 9. Execute Cleanup | Выполните очистку

**English:** After reviewing, execute the actual cleanup:

**Russian:** После проверки выполните фактическую очистку:

```powershell
# This will prompt for confirmation
.\cleanup_archives.ps1 -Mode Execute

# Or for auto-deletion of safe categories only
.\cleanup_archives.ps1 -Mode Execute -Category SafeDelete
```

### 10. Verify Results | Проверьте результаты

**English:** After cleanup, run a new scan to verify:

**Russian:** После очистки запустите новое сканирование для проверки:

```powershell
.\scan_archives.ps1
```

Compare before/after results:

- Space freed
- Archives remaining
- Cleanup effectiveness

## Safety Features | Функции безопасности

✅ **Dry Run Mode** | **Режим пробного запуска**

- Always preview before deleting
- Shows exactly what will be removed

✅ **Metadata Backup** | **Резервное копирование метаданных**

- Saves file lists and hashes
- Enables recovery if needed

✅ **Confirmation Prompts** | **Запросы подтверждения**

- Requires explicit approval
- Shows size being deleted

✅ **Incremental Cleanup** | **Инкрементальная очистка**

- Can delete in batches
- Set GB limits per run

✅ **Whitelist Protection** | **Защита белого списка**

- Never deletes whitelisted patterns
- Preserves important folders

## Troubleshooting | Устранение неполадок

### Can't access drive

**Problem:** Drive G/D/F/H not accessible

**Solution:**

```powershell
# Check drive status
Get-PSDrive -PSProvider FileSystem

# Check permissions
Test-Path G:\ -ErrorAction SilentlyContinue
```

### Script execution blocked

**Problem:** PowerShell execution policy

**Solution:**

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

### Scan too slow

**Problem:** Scanning takes too long

**Solution:**

- Reduce max_depth in config.json
- Increase min_size_mb to focus on large files
- Exclude known large folders (node_modules, etc.)

### Archives corrupted

**Problem:** Can't read archive contents

**Solution:**

- Install 7-Zip: `winget install 7zip.7zip`
- Use -SkipCorrupted flag in scan

## Notes | Примечания

**English:**

- Archive analysis doesn't extract files (fast)
- Backups are metadata only (file lists, not actual files)
- Recommended to start with preview mode
- Can be run multiple times iteratively

**Russian:**

- Анализ архивов не извлекает файлы (быстро)
- Резервные копии только метаданные (списки файлов, не сами файлы)
- Рекомендуется начать с режима предварительного просмотра
- Можно запускать несколько раз итеративно

## Expected Results | Ожидаемые результаты

Based on typical usage:

- **Initial scan:** Identify 50-200GB of archives
- **Analysis:** 30-50% marked for review, 20-30% safe delete
- **Cleanup:** Free up 10-50GB on first pass
- **Time:** 1-2 hours total for full workflow

На основе типичного использования:

- **Первоначальное сканирование:** Определение 50-200 GB архивов
- **Анализ:** 30-50% отмечено для проверки, 20-30% безопасно удалить
- **Очистка:** Освобождение 10-50 GB на первом проходе
- **Время:** 1-2 часа всего для полного рабочего процесса

---

**Status:** Ready for deployment | Готов к развертыванию
**Location:** Scripts/windows_archive_analyzer/
**Next:** Deploy to Windows PC and run scan
