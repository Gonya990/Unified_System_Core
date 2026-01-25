# 🌐 System Networking & Connectivity Guide

## ⚠️ Critical Conflicts

### Apple iCloud Private Relay

**Status: MUST BE DISABLED** (For Developers)

**Why?**
iCloud Private Relay acts as an encrypted proxy for your network traffic (specifically Safari and DNS). It hides your IP and encrypts DNS requests by routing them through Apple and Cloudflare/Akamai partners.

- **Conflict**: It directly interferes with **Tailscale** and local development servers (`localhost`, local LAN IPs).
- **Symptom**:
  - VS Code Remote connection drops or fails to resolve hostnames.
  - "Connection Error" in local web apps.
  - Unable to reach nodes like `smart` or `igor-gaming` via their Tailscale names.
  - Strange "Undefined" errors in VS Code extensions that rely on webviews (which use Safari's engine under the hood).

**Resolution**:

1. Go to **System Settings** > **[Your Name/Apple ID]** > **iCloud**.
2. Click on **Private Relay**.
3. Set it to **OFF**.

*Note: If you want to keep it on for general browsing, you must ensure 'Limit IP Address Tracking' is turned OFF for your specific Wi-Fi/Ethernet network in Network Settings, but completely disabling it is recommended for a stable Unified System environment.*

---

## 🛡 Security Architecture: "How am I protected?"

Disabling Private Relay does **NOT** leave your data vulnerable. Here is how your Unified System protects you:

### 1. Data Transfer Protection (Tailscale)

**Replaces:** The need for public internet exposure.

- **Your Protection**: Any data sent between your MacBook, PC, and Linux server is encrypted with **WireGuard®** protocol.
- **Security**: It creates a private, encrypted tunnel. Even if you are on public Wi-Fi in a cafe, no one can see what you are sending to your home server.

### 2. Physical Data Protection (At Rest)

**Replaces:** Nothing (Private Relay never did this).

- **Your Protection**:
  - **Mac**: Ensure **FileVault** is ON (System Settings > Privacy & Security).
  - **Windows**: Ensure **BitLocker** is ON.
- **Security**: If your laptop is stolen, the data is unreadable without your password.

### 3. Browsing Privacy (The Alternative)

**Replaces:** iCloud Private Relay.

- If you want to hide your DNS/IP from your ISP while browsing:
  - Use a reputable **VPN** (e.g., Mullvad, NordVPN) but **enable Split Tunneling** to allow Tailscale traffic to bypass it.
  - Or use **Secure DNS** (like Cloudflare `1.1.1.1` or Quad9 `9.9.9.9`).

---

## 🔒 Tailscale Mesh Network

### Expected Configuration

All nodes in the Unified System must be on the specific Tailscale network `unified-system-core.org.github`.

| Node | Hostname | IP Range | Role |
|------|----------|----------|------|
| **MacBook Air** | `macbook-air-igor` | `100.x.x.x` | Control Center |
| **Windows PC** | `igor-gaming` | `100.x.x.x` | GPU / Compute |
| **Linux Server** | `smart` | `100.x.x.x` | Services / Mail |

### Connectivity Check

To verify your mesh is healthy:

```bash
# Check status
tailscale status

# Test connection to GPU node
ping -c 3 igor-gaming

# Test connection to Server
ping -c 3 smart
```

## 🔧 DNS Settings

The system uses specific DNS settings to allow for internal name resolution.

- **Split DNS**: Tailscale handles `*.ts.net` and MagicDNS hostnames.
- **Public DNS**: Standard queries go to `1.1.1.1` or `8.8.8.8` (unless Private Relay interferes).

If you experience "Name Not Resolved" errors:

1. **Disable Private Relay** (see above).
2. Check `tailscale status`.
3. Flush DNS cache: `sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder`.
