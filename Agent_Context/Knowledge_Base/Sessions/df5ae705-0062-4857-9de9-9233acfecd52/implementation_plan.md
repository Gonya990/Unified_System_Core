# Enable Virtualization in BIOS

## Goal Description

Enable virtualization support (SVM/VT-x) and potentially Re-Size BAR in the BIOS of the target server to support Docker and VM workloads. The server is managed via a serial console and PiKVM.

## User Review Required
>
> [!IMPORTANT]
> Need to confirm the PiKVM URL/IP and credentials if they are not hardcoded in the scripts.
> Need to confirm if "BIOS fix" implies the machine connected via `/dev/cu.usbserial-1120`.

## Proposed Changes

### Preparation

- Identify the correct PiKVM address (check `auto_pikvm.py` or `browser_agent.py` or ask user).
- Use `auto_pikvm.py` or `magic_sysrq.py` to manage the reboot process.

### BIOS Modification

- Reboot the server.
- spam `DEL` or `F2` key during boot (via PiKVM or Serial if supported).
- Navigate menus to:
  - `Advanced` / `CPU Configuration` -> Enable `SVM Mode` (AMD) or `Intel Virtualization Technology`.
  - `PCI Subsystem Settings` -> Enable `Above 4G Decoding` and `Re-Size BAR Support`.
- Save & Reset.

## Verification Plan

### Automated Tests

- Run `lscpu` on the Linux host after boot to check for `svm` or `vmx` flags.
- Check `sudo dmesg | grep BAR` to verify Re-Size BAR.

### Manual Verification

- User checks if Docker containers strictly requiring virtualization start correctly.
