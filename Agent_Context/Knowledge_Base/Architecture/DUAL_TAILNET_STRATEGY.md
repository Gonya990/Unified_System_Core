# Running Two Tailnets on Windows (Architecture Decision)

Date: 2026-01-22
Source: User provided guide
Decision: Use Option 1 (WSL2 + Windows Native) for Simultaneous Access.

## Setup

1. **Windows Host**: Connected to Tailnet A (Personal/Gonya990).
   - Functions as ingress point for Mac/iPhone.
2. **WSL2 (Ubuntu)**: Connected to Tailnet B (Unified Core/Work).
   - Functions as the "Factory" running Docker, Ollama, and heavy workloads.
   - Using userspace networking or independent tun.

## Benefits

- Simultaneous access to both networks.
- Isolation of work/core services in WSL.
- Mac can access Core services via SSH tunnel through Windows.

## Reference

Official Tailscale limitation: No simultaneous connections on one device.
Workaround: Run one tailnet in Windows native, another inside WSL2.
Execution:
`curl -fsSL https://tailscale.com/install.sh | sh`
`sudo tailscaled --tun=userspace-networking --socks5-server=localhost:1055 &`
`tailscale up`
