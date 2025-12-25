# Windows Archive Scanner | Сканер архивов Windows
# English: Scans multiple drives for ZIP archives and catalogs them
# Russian: Сканирует несколько дисков на наличие ZIP архивов и каталогизирует их

param(
    [string]$ConfigFile = "config.json",
    [switch]$Verbose
)

# Load configuration
$config = Get-Content $ConfigFile | ConvertFrom-Json

Write-Host "╔══════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║   Windows Archive Scanner | Сканер архивов Windows           ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Initialize results
$results = @()
$totalSize = 0
$totalCount = 0

# Scan each drive
foreach ($drive in $config.scan_settings.drives) {
    if (-not (Test-Path $drive)) {
        Write-Host "⚠ Drive $drive not found, skipping..." -ForegroundColor Yellow
        Write-Host "⚠ Диск $drive не найден, пропускаем..." -ForegroundColor Yellow
        continue
    }
    
    Write-Host "🔍 Scanning drive: $drive" -ForegroundColor Green
    Write-Host "🔍 Сканирование диска: $drive" -ForegroundColor Green
    
    # Find all ZIP files
    $searchPath = Join-Path $drive "*"
    $zipFiles = Get-ChildItem -Path $searchPath -Include *.zip,*.7z,*.rar -Recurse -ErrorAction SilentlyContinue | 
        Where-Object { 
            $_.Length -gt ($config.scan_settings.min_size_mb * 1MB) -and
            $_.FullName -notmatch ($config.exclusion_patterns.folders -join '|')
        }
    
    foreach ($file in $zipFiles) {
        $sizeGB = [math]::Round($file.Length / 1GB, 2)
        $age = (Get-Date) - $file.LastWriteTime
        
        $archiveInfo = [PSCustomObject]@{
            Path = $file.FullName
            Name = $file.Name
            SizeGB = $sizeGB
            SizeMB = [math]::Round($file.Length / 1MB, 2)
            Created = $file.CreationTime
            Modified = $file.LastWriteTime
            AgeDays = $age.Days
            Drive = $drive
            Extension = $file.Extension
        }
        
        $results += $archiveInfo
        $totalSize += $file.Length
        $totalCount++
        
        if ($Verbose) {
            Write-Host "  Found: $($file.Name) - $sizeGB GB" -ForegroundColor Gray
        }
    }
    
    Write-Host "  ✓ Found $($zipFiles.Count) archives on $drive" -ForegroundColor Green
}

# Generate summary
Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host " Scan Summary | Сводка сканирования" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "Total Archives | Всего архивов: $totalCount" -ForegroundColor Green
Write-Host "Total Size | Общий размер: $([math]::Round($totalSize / 1GB, 2)) GB" -ForegroundColor Green
Write-Host ""

# Save results
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$outputFile = "reports\scan_$timestamp.json"

New-Item -ItemType Directory -Force -Path "reports" | Out-Null

$scanReport = [PSCustomObject]@{
    Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    TotalCount = $totalCount
    TotalSizeGB = [math]::Round($totalSize / 1GB, 2)
    Archives = $results
}

$scanReport | ConvertTo-Json -Depth 10 | Out-File $outputFile -Encoding UTF8

Write-Host "✓ Scan results saved to: $outputFile" -ForegroundColor Green
Write-Host "✓ Результаты сканирования сохранены в: $outputFile" -ForegroundColor Green
Write-Host ""
Write-Host "Next step | Следующий шаг: python analyze_content.py $outputFile" -ForegroundColor Yellow
Write-Host ""

# Display top 10 largest archives
Write-Host "Top 10 Largest Archives | 10 самых больших архивов:" -ForegroundColor Cyan
$results | Sort-Object -Property SizeGB -Descending | Select-Object -First 10 | 
    Format-Table Name, SizeGB, AgeDays, Drive -AutoSize

Write-Host ""
