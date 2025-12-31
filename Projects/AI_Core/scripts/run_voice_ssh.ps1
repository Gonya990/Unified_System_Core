# PowerShell script to run voice_assistant_local.py in test-file mode via SSH
# Usage: powershell -ExecutionPolicy Bypass -File run_voice_ssh.ps1 -file C:\path\to\test.wav
param(
    [string]$file = "C:\Users\gonya\my-ai-project\test_input.wav",
    [switch]$noTTS
)

$project = "C:\Users\gonya\my-ai-project"
Push-Location $project

# If virtual env exists, activate it
$venvActivate = Join-Path $project ".venv\Scripts\Activate.ps1"
if (Test-Path $venvActivate) {
    Write-Host "Activating venv"
    . $venvActivate
}

# Build argument list and call python safely (avoids quoting/parsing problems)
$argsList = @('voice_assistant_local.py', '--file', $file)
if ($noTTS) { $argsList += '--no-tts' }

Write-Host "Running: python $($argsList -join ' ')"
& python @argsList

Pop-Location
