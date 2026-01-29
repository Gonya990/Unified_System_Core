# Running full Windows setup (wrapper)

This wrapper (`run_all_windows.ps1`) invokes the installer (`setup-rtx-ai-environment.ps1`), then runs verification and Olive installation (optional), and finally runs some smoke tests.

The script supports the following switches:
- `-SkipVerify` — skip running `verify-installation.ps1` after install
- `-SkipOlive` — skip installing Olive Toolkit
- `-DryRun` — show actions without making any change
- `-NoReboot` — do not prompt or perform reboot
- `-LogPath <path>` — set custom log folder

Example usages:
```powershell
# Interactive default run
.\run_all_windows.ps1

# Dry run to see what would be executed
.\run_all_windows.ps1 -DryRun

# Full install without verification or olive
.\run_all_windows.ps1 -SkipVerify -SkipOlive

# Log to a custom path
.\run_all_windows.ps1 -LogPath C:\temp\ai-logs
```

Usage in PowerShell (Administrator):

```powershell
# Open PowerShell as Administrator
cd C:\Path\to\windows-rtx-ai-setup
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force
.\run_all_windows.ps1
```

Notes:
- The wrapper runs the same scripts as in the repository and performs quick checks.
- A reboot may be required after drivers / CUDA installation.
- Verify `nvidia-smi` after reboot and run `verify-installation.ps1` for detailed checks.

Troubleshooting:
- If Python or other dependencies fail, see the logs in `logs/`.
- If using Docker or WSL, ensure `Docker Desktop` WSL integration is enabled and the NVIDIA WSL driver is installed.

If you prefer full automation (no prompts): adapt `setup-rtx-ai-environment.ps1` to accept flags (non-interactive mode).