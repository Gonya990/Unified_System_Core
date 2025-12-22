# 🔐 Final Access Pack

Your hardware and network connection (via Openterface and Tailscale) is now ready. Below are the specific credentials and URLs discovered for your environment.

## 🌐 Web Service Access

Access these URLs directly from your **MacBook Air** browser:

| Service | Tailscale URL | Local/Docker Port |
| :--- | :--- | :--- |
| **Home Assistant** | [http://100.88.65.71:8123](http://100.88.65.71:8123) | `8123` |
| **n8n Automation** | [http://100.88.65.71:8080](http://100.88.65.71:8080) | `8080` (Editor) |
| **OpenCode (Web)** | [http://100.88.65.71:4096](http://100.88.65.71:4096) | `4096` |
| **Ollama AI API** | [http://100.88.65.71:11434](http://100.88.65.71:11434) | `11434` |
| **Chrome Debug** | [http://100.88.65.71:9222](http://100.88.65.71:9222) | `9222` |

## 🔑 Credentials & Tokens

### 💻 System Login (SSH)

Used for accessing `igor-gaming-1` from your Mac:

- **User**: `gonya`
- **Password**: `GarYk6550`
- **Command**: `ssh gonya@100.88.65.71`

### 🛠️ OpenCode Connection Token

If the web interface prompts for a token:

- **Token**: `261667942920`

## 📡 Network Configuration Reminder

To use your preferred domain name instead of the IP, ensure your Mac's `/etc/hosts` file contains:

```bash
100.88.65.71 mydomain.com
```

> [!IMPORTANT]
> Since you are using **Openterface**, if you lose network access, you can always use the hardware KVM to verify the status directly on the console.

## ✅ Verification Checklist

- [ ] SSH into the Linux machine from Mac.
- [ ] Open Home Assistant at port 8123.
- [ ] Verify `mydomain.com` resolves correctly.
