# Windows Hardware Storage Audit
# Identifies Physical Disks, Media Type (SSD/HDD), Bus Type (NVMe/SATA), and maps them to Drive Letters.

$Results = @()

# Get all physical disks
$Disks = Get-PhysicalDisk | Sort-Object DeviceId

foreach ($Disk in $Disks) {
    $DiskInfo = [ordered]@{
        DeviceId     = $Disk.DeviceId
        MediaType    = $Disk.MediaType # SSD, HDD, Unspecified
        BusType      = $Disk.BusType # NVMe, SATA, USB, RAID
        Model        = $Disk.Model
        SizeGB       = [math]::Round($Disk.Size / 1GB, 2)
        HealthStatus = $Disk.HealthStatus
        Partitions   = @()
    }
    
    # Find partitions for this disk
    $Partitions = Get-Partition -DiskNumber $Disk.DeviceId -ErrorAction SilentlyContinue
    
    if ($Partitions) {
        foreach ($Part in $Partitions) {
            if ($Part.DriveLetter) {
                $Vol = Get-Volume -DriveLetter $Part.DriveLetter -ErrorAction SilentlyContinue
                $FreeGB = if ($Vol) { [math]::Round($Vol.SizeRemaining / 1GB, 2) } else { 0 }
                $TotalGB = if ($Vol) { [math]::Round($Vol.Size / 1GB, 2) } else { 0 }
                
                $PartitionInfo = [ordered]@{
                    DriveLetter = $Part.DriveLetter + ":"
                    Label       = if ($Vol) { $Vol.FileSystemLabel } else { "Unknown" }
                    FreeGB      = $FreeGB
                    TotalGB     = $TotalGB
                    PercentFree = if ($Vol) { [math]::Round(($FreeGB / $TotalGB) * 100, 1) } else { 0 }
                }
                $DiskInfo.Partitions += $PartitionInfo
            }
        }
    }
    
    # Determine performance class
    $Class = "Unknown"
    if ($Disk.MediaType -eq "SSD") {
        if ($Disk.BusType -eq "NVMe") { $Class = "⚡ TIER 1 (NVMe SSD)" }
        else { $Class = "🚀 TIER 2 (SATA SSD)" }
    }
    elseif ($Disk.MediaType -eq "HDD") {
        $Class = "🐢 TIER 3 (HDD)"
    }
    elseif ($Disk.BusType -eq "USB") {
        $Class = "💾 EXTERNAL (USB)"
    }
    
    $DiskInfo["PerformanceTier"] = $Class
    $Results += [PSCustomObject]$DiskInfo
}

# Export to JSON for Python analysis
$JsonPath = Join-Path $PSScriptRoot "hardware_report.json"
$Results | ConvertTo-Json -Depth 5 | Out-File $JsonPath -Encoding UTF8
Write-Output ($Results | ConvertTo-Json -Depth 5)
