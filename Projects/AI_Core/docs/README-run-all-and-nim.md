# run_all_and_nim.ps1

This wrapper runs `run_all_windows.ps1` and optionally launches WSL to run the NIM installer (`run_nim_on_wsl.sh`), automating the full stack setup.

Usage:
```powershell
cd C:\Path\to\windows-rtx-ai-setup
 .\run_all_and_nim.ps1 [-SkipVerify] [-SkipOlive] [-RunNim] [-NgcKey <key>] [-NgcKeyFile <file>] [-WslDistro <distro>] [-AutoInstallWSL] [-AutoInstallTools] [-InstallWSLOnly] [-UseSsh] [-RemoteHost <host>] [-RemoteUser <user>] [-RemotePort <port>] [-RemotePath <path>] [-NoReboot] [-DryRun] [-LogPath <path>]
```

Notes:
- `RunNim` is true by default: it will attempt to find WSL and run the NIM installer inside the given distro (`Ubuntu-22.04` by default).
- If NGC API key is provided via `-NgcKey`, the script will pass it to the WSL script using an environment variable (safer than CLI args).
- `DryRun` is ideal to verify what will execute without making changes.
- Script requires Administrator privileges and Docker Desktop with WSL integration enabled.
 - `AutoInstallWSL` will enable WSL and install the specified distro if WSL/distro are not present (requires Admin privileges and may prompt for reboot).
 - `AutoInstallTools` will ensure `curl`, `kubectl`, and `helm` are installed in the WSL distro (via apt-get / install scripts).
 - `InstallWSLOnly` will only install/prepare WSL and tools (skipping `run_all_windows.ps1` Windows installation).
 - `UseSsh` with `-RemoteHost` and `-RemoteUser` will copy the repository to the remote Windows host via `scp` and run `run_all_and_nim.ps1` on that host via `ssh`.
	Use `-NgcKeyFile` to securely pass the NGC key file to the remote host (it will be cleaned up after the run).

Troubleshooting:
- If WSL is missing, enable WSL and install a distro, then re-run.
- If Docker Desktop doesn't show WSL integration, enable it in Docker Desktop settings.
- If the NIM operator fails to install pods, check `kubectl -n nim-service get pods -o wide` and `kubectl -n nim-service describe pod <pod>`.

Security:
- Avoid copying and sharing the logs if they may contain sensitive tokens. Use `-DryRun` to check before running.
- If you need to share logs for support, sanitize them to remove sensitive headers or keys.

This script is meant for convenience and automation; review it before running in production environments.
