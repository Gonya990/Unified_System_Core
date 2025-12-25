# Windows Archive Analyzer | Анализатор архивов Windows

## Overview | Обзор

**English:** Tool to analyze large ZIP archives on Windows PC drives (G/D/F/H), identify useful content, and safely delete unnecessary files.

**Russian:** Инструмент для анализа больших ZIP архивов на дисках Windows PC (G/D/F/H), определения полезного содержимого и безопасного удаления ненужных файлов.

## Features | Возможности

### 1. Archive Discovery | Обнаружение архивов

- **English:** Scan multiple drives for ZIP files
- **Russian:** Сканирование нескольких дисков на наличие ZIP файлов

### 2. Content Analysis | Анализ содержимого

- **English:** Analyze archive contents without full extraction
- **Russian:** Анализ содержимого архивов без полного извлечения

### 3. Intelligent Categorization | Интеллектуальная категоризация

- **English:** Categorize files by type, age, duplication
- **Russian:** Категоризация файлов по типу, возрасту, дублированию

### 4. Safe Cleanup | Безопасная очистка

- **English:** Preview before deletion, backup options
- **Russian:** Предварительный просмотр перед удалением, опции резервного копирования

## Directory Structure | Структура директории

```
windows_archive_analyzer/
├── README.md                      # This file | Этот файл
├── config.json                    # Configuration | Конфигурация
├── scan_archives.ps1              # PowerShell scanner | PowerShell сканер
├── analyze_content.py             # Content analyzer | Анализатор содержимого
├── generate_report.py             # Report generator | Генератор отчетов
├── cleanup_archives.ps1           # Cleanup script | Скрипт очистки
├── reports/                       # Analysis reports | Отчеты анализа
└── backups/                       # Backup metadata | Метаданные резервных копий
```

## Usage | Использование

### Remote Execution from Mac | Удаленное выполнение с Mac

**English:** Since the archives are on your Windows PC, you'll execute commands remotely:

**Russian:** Так как архивы находятся на вашем Windows PC, вы будете выполнять команды удаленно:

```bash
# From Mac - connect to Windows PC via SSH/Tailscale
ssh user@windows-pc

# Or copy scripts to Windows PC and run there
# Или скопируйте скрипты на Windows PC и запустите там
```

### Step 1: Configure Scan | Настройте сканирование

Edit `config.json` to set:

- Drives to scan (G, D, F, H)
- Minimum archive size
- File types to keep
- Exclusion patterns

### Step 2: Scan Archives | Сканируйте архивы

```powershell
.\scan_archives.ps1
```

This will create a catalog of all ZIP files with metadata.

Это создаст каталог всех ZIP файлов с метаданными.

### Step 3: Analyze Content | Анализируйте содержимое

```powershell
python analyze_content.py
```

Generates detailed analysis report with recommendations.

Генерирует подробный отчет анализа с рекомендациями.

### Step 4: Review Report | Проверьте отчет

Open `reports/analysis_YYYYMMDD_HHMMSS.html` in browser.

Откройте `reports/analysis_YYYYMMDD_HHMMSS.html` в браузере.

### Step 5: Execute Cleanup | Выполните очистку

```powershell
.\cleanup_archives.ps1 --mode preview
.\cleanup_archives.ps1 --mode execute
```

## Analysis Categories | Категории анализа

### Keep | Сохранить

- Unique files not found elsewhere
- Recent archives (< 6 months)
- Important file types (documents, code, photos)
- Small total size

### Review | Проверить

- Duplicate content
- Mixed content archives
- Medium age (6-12 months)

### Delete | Удалить

- Complete duplicates
- Old temporary files
- Known junk patterns
- Very old archives (> 2 years) with common content

## Safety Features | Функции безопасности

- ✅ Preview mode before deletion
- ✅ Metadata backup of all archives
- ✅ Dry-run option
- ✅ Whitelist important patterns
- ✅ Size limits per operation
- ✅ Confirmation prompts

## Configuration | Конфигурация

See `config.json` for all options:

```json
{
  "drives": ["G:", "D:", "F:", "H:"],
  "min_size_mb": 10,
  "file_types_keep": [".doc", ".pdf", ".jpg", ".png", ".zip"],
  "exclude_patterns": ["backup_*", "important_*"],
  "age_threshold_delete_days": 730,
  "duplicate_detection": true
}
```

## Requirements | Требования

### Windows PC

- PowerShell 5.1+
- Python 3.8+ (for analysis scripts)
- 7-Zip (for archive inspection)

### Mac (for remote management)

- SSH or Tailscale access to Windows PC
- Optional: rsync for script deployment

## Next Steps | Следующие шаги

1. **Configure access to Windows PC** | **Настройте доступ к Windows PC**
2. **Install requirements** | **Установите требования**
3. **Run initial scan** | **Запустите первоначальное сканирование**
4. **Review analysis** | **Проверьте анализ**
5. **Execute cleanup** | **Выполните очистку**

---

**Status:** Ready for implementation | Готов к реализации
**Priority:** Medium | Средний
**Estimated time:** 2-3 hours for full analysis | 2-3 часа для полного анализа
