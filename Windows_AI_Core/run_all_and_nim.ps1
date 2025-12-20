<#
run_all_and_nim.ps1

Wrapper script that runs `run_all_windows.ps1` on Windows and then (optionally)
launches WSL to run `run_nim_on_wsl.sh` (via the pre-existing scripts in the repo).

Features:
- Administrator check
- DryRun for safe verification
- Optional flags: SkipVerify, SkipOlive, NoReboot
- Optionally auto-run NIM install inside WSL with NGC key
- Checks WSL availability and runs the script inside specified distro
- Converts Windows path to WSL path to allow commands inside Linux

Usage:
  .\run_all_and_nim.ps1 [-SkipVerify] [-SkipOlive] [-RunNim] [-NgcKey <key>] [-WslDistro <name>] [-DryRun] [-NoReboot]

Example:
  .\run_all_and_nim.ps1 -RunNim -NgcKey "xxxx-xxxx-..." -DryRun
#>

[CmdletBinding()]
param(
    [switch]$SkipVerify,
    [switch]$SkipOlive,
    [switch]$RunNim = $true,
    [string]$NgcKey = "",
    [string]$NgcKeyFile = "",
    [string]$WslDistro = "Ubuntu-22.04",
    [switch]$DryRun,
    [switch]$AutoInstallWSL,
    [switch]$AutoInstallTools,
    [switch]$InstallWSLOnly,
    [switch]$UseSsh,
    [string]$RemoteHost = "",
    [string]$RemoteUser = "",
    [int]$RemotePort = 22,
    [string]$RemotePath = "",
    [switch]$NoReboot,
    [string]$LogPath = "$PSScriptRoot\logs"
)

function Write-Info { param($m) Write-Host $m -ForegroundColor Cyan }
function Write-Warn { param($m) Write-Host $m -ForegroundColor Yellow }
function Write-Err { param($m) Write-Host $m -ForegroundColor Red }

# Admin check: skip when DryRun or when not on Windows for testing
if (-not $DryRun) {
    if (-not $IsWindows) {
        Write-Err "This script should be run on Windows. To run a dry-run on non-Windows, pass -DryRun."; exit 1
    }
    if (-not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
        Write-Err "This script must be run as Administrator. Right click PowerShell and 'Run as Administrator'."; exit 1
    }
} else {
    Write-Warn "DryRun: admin checks skipped";
}

# build args for run_all_windows.ps1
$runAllArgs = @()
if ($SkipVerify) { $runAllArgs += '-SkipVerify' }
if ($SkipOlive)  { $runAllArgs += '-SkipOlive' }
if ($NoReboot)  { $runAllArgs += '-NoReboot' }
if ($DryRun)    { $runAllArgs += '-DryRun' }

# Prepare logging
if (!(Test-Path $LogPath)) { New-Item -ItemType Directory -Path $LogPath | Out-Null }
$LogFile = Join-Path $LogPath "run_all_and_nim-$(Get-Date -Format 'yyyyMMdd-HHmmss').log"
Write-Info "Log file: $LogFile"

$ScriptDir = Split-Path -Path $MyInvocation.MyCommand.Definition -Parent
$runAllScript = Join-Path $ScriptDir 'run_all_windows.ps1'

if (!(Test-Path $runAllScript)) {
    Write-Err "run_all_windows.ps1 not found at $runAllScript"; exit 1
}

# If InstallWSLOnly is set, skip the Windows install
if ($InstallWSLOnly) { Write-Info "InstallWSLOnly: skipping run_all_windows.ps1, proceeding to WSL/distro setup" }
else {
# Run main Windows install script (DryRun allowed)
Write-Info "Running Windows environment setup (run_all_windows.ps1)"
if ($DryRun) { Write-Warn "Dry run: would execute run_all_windows.ps1 $($runAllArgs -join ' ')" }
else {
    Write-Info "Executing: $runAllScript $($runAllArgs -join ' ')"
    & $runAllScript @runAllArgs 2>&1 | Tee-Object -FilePath $LogFile -Append
}
}

# After Windows install, optionally run NIM inside WSL
if ($InstallWSLOnly -and -not $RunNim) { $RunNim = $true }

if ($RunNim) {
    # If remote SSH execution is requested and we have host details, run remotely
    if ($UseSsh) {
        if ($RemoteHost -eq "" -or $RemoteUser -eq "") { Write-Err "UseSsh requires RemoteHost and RemoteUser"; exit 1 }
        # ensure ssh & scp available on this machine
        if (-not (Get-Command ssh -ErrorAction SilentlyContinue)) { Write-Err "ssh is required on this machine to use UseSsh"; exit 1 }
        if (-not (Get-Command scp -ErrorAction SilentlyContinue)) { Write-Err "scp is required on this machine to use UseSsh"; exit 1 }

        $remotePath = $RemotePath
        if ($remotePath -eq "") { $remotePath = "C:\\Users\\$RemoteUser\\windows-rtx-ai-setup" }

        Write-Info "Copying repository to remote host $($RemoteUser)@$($RemoteHost):$remotePath"
        if ($DryRun) { Write-Warn "DRY-RUN: would copy $ScriptDir to $($RemoteHost):$remotePath" }
        else {
            # Ensure remote path exists
            ssh -p $RemotePort $RemoteUser@$RemoteHost "powershell -NoProfile -Command `"New-Item -ItemType Directory -Force -Path '$remotePath'`""
            $dest = "$($RemoteUser)@$($RemoteHost):$remotePath/"
            & scp -P $RemotePort -r "$ScriptDir/*" $dest
        }

        # Copy ngc key file if provided (either key string or keyfile local path)
        $remoteNgcFile = ""
        if ($NgcKeyFile -ne "") {
            if ($DryRun) { Write-Warn "DRY-RUN: would copy NgcKeyFile $NgcKeyFile to remote host" }
            else {
                $remoteNgcFile = "$remotePath\ngc_key.txt"
                $dest = "$($RemoteUser)@$($RemoteHost):$remoteNgcFile"
                & scp -P $RemotePort $NgcKeyFile $dest
            }
        } elseif ($NgcKey -ne "") {
            if ($DryRun) { Write-Warn "DRY-RUN: would copy provided NgcKey to remote host via temporary file" }
            else {
                # create a temporary file locally
                $tmpPath = [System.IO.Path]::GetTempFileName()
                set-content -Path $tmpPath -Value $NgcKey -NoNewline
                $remoteNgcFile = "$remotePath\ngc_key.txt"
                $dest = "$($RemoteUser)@$($RemoteHost):$remoteNgcFile"
                & scp -P $RemotePort $tmpPath $dest
                Remove-Item $tmpPath -Force
            }
        }

        # Build the remote command
        $remoteArgs = @()
        if ($SkipVerify) { $remoteArgs += '-SkipVerify' }
        if ($SkipOlive)  { $remoteArgs += '-SkipOlive' }
        if ($NoReboot)   { $remoteArgs += '-NoReboot' }
        if ($DryRun)     { $remoteArgs += '-DryRun' }
        if ($AutoInstallWSL) { $remoteArgs += '-AutoInstallWSL' }
        if ($InstallWSLOnly) { $remoteArgs += '-InstallWSLOnly' }
        if ($AutoInstallTools) { $remoteArgs += '-AutoInstallTools' }
        if ($remoteNgcFile -ne "") { $remoteArgs += "-NgcKeyFile '$remoteNgcFile'" }

        $remoteCmd = "powershell -NoProfile -ExecutionPolicy Bypass -File '$remotePath\run_all_and_nim.ps1' $($remoteArgs -join ' ')"
        if ($DryRun) { Write-Warn "DRY-RUN: would run on remote: ssh -p $RemotePort $RemoteUser@$RemoteHost \"$remoteCmd\"" }
        else {
            Write-Info "Running remote installation on $RemoteHost"
            ssh -p $RemotePort $RemoteUser@$RemoteHost "$remoteCmd" 2>&1 | Tee-Object -FilePath $LogFile -Append
            # cleanup remote ngc file afterwards
            if ($remoteNgcFile -ne "") { ssh -p $RemotePort $RemoteUser@$RemoteHost "powershell -NoProfile -Command \"Remove-Item -Force -Path '$remoteNgcFile'\"" }
        }

        Write-Info "Remote run completed. See logs on remote machine and $LogFile"; return
    }

    # Check WSL availability
    $wslPresent = (Get-Command wsl.exe -ErrorAction SilentlyContinue) -ne $null
    if (-not $wslPresent) {
        if ($AutoInstallWSL) {
            Write-Info "WSL is not installed. AutoInstallWSL requested — attempting to enable WSL and install distro: $WslDistro"
            if ($DryRun) {
                Write-Warn "DRY-RUN: would run 'wsl --install -d $WslDistro' to install WSL and the distro"
            } else {
                Write-Info "Running: wsl --install -d $WslDistro"
                # install WSL (may require reboot). This command requires admin rights.
                wsl.exe --install -d $WslDistro
            }
        } else {
            Write-Err "WSL (wsl.exe) not found. Please enable WSL and install a distro (e.g., Ubuntu-22.04) and Docker Desktop WSL2 backend.";
            exit 1
        }
    }

    # ensure distro exists
    try {
        $dists = wsl.exe -l -v 2>&1 | Out-String
        if ($dists -notmatch [regex]::Escape($WslDistro)) {
            Write-Warn "WSL distro '$WslDistro' not found. Available distros:";
            wsl.exe -l -v
            if ($AutoInstallWSL) {
                if ($DryRun) { Write-Warn "DRY-RUN: would run 'wsl --install -d $WslDistro' to create the distro" }
                else {
                    Write-Info "AutoInstallWSL: Installing distro $WslDistro"
                    wsl.exe --install -d $WslDistro
                }
            } else {
                if (-not $DryRun) { Write-Err "Please create or import the distro: wsl --install -d $WslDistro"; exit 1 }
                else { Write-Warn "DryRun: skipping distro creation" }
            }
        }
    }
    catch {
        Write-Err "Unable to list WSL distros: $_"; exit 1
    }

    # Convert Windows path to WSL path
    function Convert-WindowsToWslPath {
        param([string]$path)
        $p = $path -replace '\\','/'
        if ($p -match '^([A-Za-z]):/(.*)') {
            $drive = $matches[1].ToLower()
            $rest = $matches[2]
            return "/mnt/$drive/$rest"
        } else { return $p }
    }

    $wsldir = Convert-WindowsToWslPath $ScriptDir
    $k8sDir = Join-Path $ScriptDir 'quick_install' -Resolve

    # The repo path for WSL should be available under /mnt/<drive>/path
    $wsl_k8s_dir = Convert-WindowsToWslPath (Join-Path $ScriptDir '..\quick_install\run-on-rtx\k8s' | Resolve-Path | Select-Object -ExpandProperty Path)

    # If remote SSH execution is requested and we have host details, run remotely
    if ($UseSsh) {
        if ($RemoteHost -eq "" -or $RemoteUser -eq "") { Write-Err "UseSsh requires RemoteHost and RemoteUser"; exit 1 }
        # ensure ssh & scp available on this machine
        if (-not (Get-Command ssh -ErrorAction SilentlyContinue)) { Write-Err "ssh is required on this machine to use UseSsh"; exit 1 }
        if (-not (Get-Command scp -ErrorAction SilentlyContinue)) { Write-Err "scp is required on this machine to use UseSsh"; exit 1 }

        $remotePath = $RemotePath
        if ($remotePath -eq "") { $remotePath = "C:\\Users\\$RemoteUser\\windows-rtx-ai-setup" }

        Write-Info "Copying repository to remote host $($RemoteUser)@$($RemoteHost):$remotePath"
            if ($DryRun) { Write-Warn "DRY-RUN: would copy $ScriptDir to $($RemoteHost):$remotePath" }
        else {
            # Ensure remote path exists
            ssh -p $RemotePort $RemoteUser@$RemoteHost "powershell -NoProfile -Command `"New-Item -ItemType Directory -Force -Path '$remotePath'`""
                $dest = "$($RemoteUser)@$($RemoteHost):$remotePath/"
                & scp -P $RemotePort -r "$ScriptDir/*" $dest
        }

        # Copy ngc key file if provided (either key string or keyfile local path)
        $remoteNgcFile = ""
        if ($NgcKeyFile -ne "") {
            if ($DryRun) { Write-Warn "DRY-RUN: would copy NgcKeyFile $NgcKeyFile to remote host" }
            else {
                $remoteNgcFile = "$remotePath\ngc_key.txt"
                    $dest = "$($RemoteUser)@$($RemoteHost):$remoteNgcFile"
                    & scp -P $RemotePort $NgcKeyFile $dest
            }
        } elseif ($NgcKey -ne "") {
            if ($DryRun) { Write-Warn "DRY-RUN: would copy provided NgcKey to remote host via temporary file" }
            else {
                # create a temporary file locally
                $tmpPath = [System.IO.Path]::GetTempFileName()
                set-content -Path $tmpPath -Value $NgcKey -NoNewline
                $remoteNgcFile = "$remotePath\ngc_key.txt"
                    $dest = "$($RemoteUser)@$($RemoteHost):$remoteNgcFile"
                    & scp -P $RemotePort $tmpPath $dest
                Remove-Item $tmpPath -Force
            }
        }

        # Build the remote command
        $remoteArgs = @()
        if ($SkipVerify) { $remoteArgs += '-SkipVerify' }
        if ($SkipOlive)  { $remoteArgs += '-SkipOlive' }
        if ($NoReboot)   { $remoteArgs += '-NoReboot' }
        if ($DryRun)     { $remoteArgs += '-DryRun' }
        if ($AutoInstallWSL) { $remoteArgs += '-AutoInstallWSL' }
        if ($InstallWSLOnly) { $remoteArgs += '-InstallWSLOnly' }
        if ($AutoInstallTools) { $remoteArgs += '-AutoInstallTools' }
        if ($remoteNgcFile -ne "") { $remoteArgs += "-NgcKeyFile '$remoteNgcFile'" }

        $remoteCmd = "powershell -NoProfile -ExecutionPolicy Bypass -File '$remotePath\run_all_and_nim.ps1' $($remoteArgs -join ' ')"
        if ($DryRun) { Write-Warn "DRY-RUN: would run on remote: ssh -p $RemotePort $RemoteUser@$RemoteHost \"$remoteCmd\"" }
        else {
            Write-Info "Running remote installation on $RemoteHost"
            ssh -p $RemotePort $RemoteUser@$RemoteHost "$remoteCmd" 2>&1 | Tee-Object -FilePath $LogFile -Append
            # cleanup remote ngc file afterwards
            if ($remoteNgcFile -ne "") { ssh -p $RemotePort $RemoteUser@$RemoteHost "powershell -NoProfile -Command \"Remove-Item -Force -Path '$remoteNgcFile'\"" }
        }

        Write-Info "Remote run completed. See logs on remote machine and $LogFile"; return
    }
    
    # Compose wsl command (dry-run allowed)
    $wslCmd = @()
    $wslCmd += "cd '$wsl_k8s_dir'"
    $wslCmd += "./run_nim_on_wsl.sh --only-step1"
    if ($DryRun) { Write-Warn "Dry run: would execute in WSL: $($wslCmd -join ' && ')" }
    else {
        Write-Info "Running NIM install inside WSL distro: $WslDistro"
        # run step1
        wsl.exe -d $WslDistro -- bash -lc "$($wslCmd -join ' && ')" 2>&1 | Tee-Object -FilePath $LogFile -Append

        # If an NgcKey is provided, run full install with key
            if ($NgcKey -ne '') {
                $escapedKey = $NgcKey -replace "'","'""'"
                # Build a safe WSL command that sets the env var and invokes the installer
                $cmdInner = "cd '$wsl_k8s_dir' && NGC_KEY='$escapedKey' ./run_nim_on_wsl.sh"
            } elseif ($NgcKeyFile -ne '') {
                # convert local file path to WSL path and pass via --ngc-key-file
                $wslKeyFile = Convert-WindowsToWslPath (Resolve-Path $NgcKeyFile | Select-Object -ExpandProperty Path)
                $cmdInner = "cd '$wsl_k8s_dir' && ./run_nim_on_wsl.sh --ngc-key-file '$wslKeyFile'"
                Write-Info "Running NIM full install in WSL (NGC key provided). Note: sensitive values are not printed in the logs by default."
                wsl.exe -d $WslDistro -- bash -lc "$cmdInner" 2>&1 | Tee-Object -FilePath $LogFile -Append
            } else {
            Write-Info "No NGC key provided, running interactive install. You will be prompted inside WSL."
            wsl.exe -d $WslDistro -- bash -lc "cd '$wsl_k8s_dir' && ./run_nim_on_wsl.sh" 2>&1 | Tee-Object -FilePath $LogFile -Append
        }

        # Post-install: check pods and events
        Write-Info "Checking NIM pods (kubectl) inside WSL"
        wsl.exe -d $WslDistro -- bash -lc "kubectl -n nim-service get pods -o wide || true; kubectl -n nim-service get events --sort-by='.lastTimestamp' | tail -n 20 || true" 2>&1 | Tee-Object -FilePath $LogFile -Append
    }
    # Ensure required tools exist in WSL if AutoInstallTools is requested
    if ($AutoInstallTools) {
        $toolsToCheck = @('curl','kubectl','helm')
        foreach ($tool in $toolsToCheck) {
            Write-Info "Checking for $tool in WSL distro: $WslDistro"
            $checkCmd = "if command -v $tool >/dev/null 2>&1; then echo 'present'; else echo 'missing'; fi"
            $present = wsl.exe -d $WslDistro -- bash -lc $checkCmd 2>&1 | Out-String
            if ($present -match 'missing') {
                Write-Warn "$tool is missing in WSL. AutoInstallWSL will attempt to install $tool in the distro."
                if ($DryRun) { Write-Warn "DRY-RUN: would install $tool in WSL" }
                else {
                    switch ($tool) {
                        'curl' { wsl.exe -d $WslDistro -- bash -lc "sudo apt-get update && sudo apt-get install -y curl apt-transport-https ca-certificates gnupg lsb-release" 2>&1 | Tee-Object -FilePath $LogFile -Append }
                        'kubectl' { wsl.exe -d $WslDistro -- bash -lc "curl -LO \"https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl\" && sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl" 2>&1 | Tee-Object -FilePath $LogFile -Append }
                        'helm' { wsl.exe -d $WslDistro -- bash -lc "curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash" 2>&1 | Tee-Object -FilePath $LogFile -Append }
                        default { Write-Warn "No install action for $tool" }
                    }
                }
            } else { Write-Info "$tool already present in WSL" }
        }
    }
} else {
    Write-Warn "RunNim not set: skipping WSL-based NIM installation"
}

Write-Info "Run completed. Logs written to: $LogFile"

# End of script
