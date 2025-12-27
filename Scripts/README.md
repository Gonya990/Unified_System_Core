# 📁 Scripts Directory

Organized collection of automation scripts for the Unified System.

## 📂 Structure

```text
Scripts/
├── automation/         # Nodriver browser automation
├── bot/               # Telegram AI bot management
├── deployment/        # VM and cloud deployment
├── External/          # Third-party tools
├── gcp/               # Google Cloud Platform
├── ios/               # iOS/iCloud sync scripts
├── monitoring/        # System monitoring
├── network/           # Tailscale & tunneling
├── openai_data_integration/  # OpenAI export processing
├── openai_mcp_server/        # MCP server for OpenAI
├── remote/            # Remote machine management
├── tools/             # Utility scripts
└── windows_archive_analyzer/ # Archive analysis tools
```

## 🗂️ Categories

### 🤖 bot/

Telegram AI bot management scripts

- `debug_bot.exp` - Bot debugging
- `start_bot_*.exp` - Bot startup scripts
- `switch_bot_to_tailscale.sh` - Network migration

### 🚀 deployment/

Deployment automation

- `deploy_bot_to_vm.sh` - Bot VM deployment
- `deploy_cloud_vm.sh` - Cloud VM creation
- `deploy_windows.exp` - Windows deployment

### 📊 gcp/

Google Cloud Platform integration

- `gcp_metrics_collector.py` - System metrics → Cloud Monitoring

### 📱 ios/

iOS device synchronization

- `sync_ios_exports.sh` - iCloud data sync

### 📡 network/

Network and tunnel management

- `install_tailscale_vm.sh` - Tailscale installation
- `setup_tunnel.sh` - Tunnel configuration

### 🔧 remote/

Remote machine management via expect

- `configure_ollama_net.exp` - Ollama network setup
- `open_firewall.exp` - Firewall configuration

### 🛠️ tools/

General-purpose utilities

- `admin_check.sh` - Admin privilege check
- `brute_proxmox.exp` - Proxmox access
- `pull_model.exp` - LLM model download
- `send_config.exp` - Config deployment

## 🔧 Usage

Most `.exp` scripts require `expect`:

```bash
expect script.exp [args]
```

Shell scripts:

```bash
./script.sh [args]
```

Python scripts:

```bash
python3 script.py
```

## ⚠️ Security Notes

- Never commit credentials
- Use `.env` files for secrets
- Check `secrets/` directory exclusion in `.gitignore`
