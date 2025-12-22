# SSH Setup Implementation Plan

## Goal
Convert the provided PowerShell script into a Bash script (`setup_ssh_consortium.sh`) to establish SSH keys for the "AI Consortium" on the current Linux environment.

## User Review Required
- **Execution**: The script requires interactive password entry for `ssh`. I will generate the script first. The user needs to decide if they want me to run it (which might require handling prompts) or if they will run it themselves.

## Proposed Changes
### SSH Setup
#### [NEW] [setup_ssh_consortium.sh](file:///home/gonya/setup_ssh_consortium.sh)
- Bash equivalent of the PowerShell steps:
    1.  Define IPs (`NucIP`, `WslIP`) and User (`gonya`).
    2.  Check/Generate SSH Key (`~/.ssh/id_ai_consortium`).
    3.  Copy ID to NUC.
    4.  Copy ID to WSL (Localhost check?).

## Verification Plan
- **Manual**: Run the script and verify `ssh -i ~/.ssh/id_ai_consortium user@host` works without password.
