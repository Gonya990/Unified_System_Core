# Chrome Remote Debugging Walkthrough

## Changes Implemented

I have successfully deployed a headless Chrome instance using Docker, configured to listen on port `9222` on all network interfaces (`0.0.0.0`), fulfilling the requirement for remote debugging access equivalent to the provided Windows instructions.

### 1. Docker Configuration Fix

- Detected a misconfigured `~/.docker/config.json` (leftover from a Windows/WSL environment).
- **Action**: Reset `config.json` to allow correct image pulling on Linux.

### 2. Chrome Deployment

- **Method**: Docker Container
- **Image**: `zenika/alpine-chrome:latest`
- **Command**:

  ```bash
  docker run -d --name chrome-headless --restart unless-stopped -p 9222:9222 --cap-add=SYS_ADMIN zenika/alpine-chrome:latest --no-sandbox --remote-debugging-address=0.0.0.0 --remote-debugging-port=9222
  ```

## Verification Results

### 1. Container Status

The container is up and running.

```bash
CONTAINER ID   IMAGE                          STATUS          PORTS                                         NAMES
e57fc1d262a2   zenika/alpine-chrome:latest    Up 2 minutes    0.0.0.0:9222->9222/tcp, [::]:9222->9222/tcp   chrome-headless
```

### 2. Network Listener

Port 9222 is listening on all interfaces.

```bash
tcp   LISTEN 0      4096      *:9222      *:*
```

### 3. Service Response

The `json/version` endpoint returns valid Chrome metadata:

```json
{
   "Browser": "HeadlessChrome/124.0.6367.78",
   "Protocol-Version": "1.3",
   "webSocketDebuggerUrl": "ws://127.0.0.1:9222/devtools/browser/..."
}
```

## How to Connect

You can now connect to this Chrome instance from your other machines using the server's IP address:

- **Local LAN**: `172.18.114.216:9222`
- **Tailscale**: `100.88.65.71:9222`
- **Loopback (on server)**: `127.0.0.1:9222`
