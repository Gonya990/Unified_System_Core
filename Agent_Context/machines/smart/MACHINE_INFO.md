# Machine: smart

**Collected:** Sun Dec 22 21:40:00 IST 2025
**Platform:** Fedora Linux 41 (6.15.6-100.fc41.x86_64)
**Hostname:** smart
**Tailscale IP:** 100.81.133.25
**LAN IP:** 192.168.1.176
**User:** igor

## Role: Gateway & Streaming Client

This device is tagged as `gateway`, `gonya-client`, `gonya-server` in Tailscale.

### Installed Software

- **Moonlight** 6.1.0 (Flatpak) — Game streaming client
- **Tailscale** 1.84.0

### Connectivity

- Sunshine on Windows (`100.127.194.111`): ✅ Reachable
- Latency: Amsterdam 61ms, Paris 64ms

## Setup for Moonlight

To pair with Windows Sunshine:

```bash
flatpak run com.moonlight_stream.Moonlight
# Add host: 100.127.194.111
# Enter PIN shown on Windows
```

## SSH Access

```bash
ssh igor@100.81.133.25  # Password: 6550
# SSH key from Mac added
```
