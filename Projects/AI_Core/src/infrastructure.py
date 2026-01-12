"""
Infrastructure Manager for AI Bot.
Reads infrastructure.yaml and provides information about the network.
"""
import asyncio
import logging
from pathlib import Path

import yaml

logger = logging.getLogger(__name__)

class InfrastructureManager:
    def __init__(self, config_path: str = "config/infrastructure.yaml"):
        # Resolve path relative to project root (assuming src/infrastructure.py)
        root_dir = Path(__file__).parent.parent
        self.config_path = root_dir / config_path
        self.data = {"nodes": [], "apps": []}
        self.load_config()

    def load_config(self):
        """Load infrastructure definition."""
        try:
            if self.config_path.exists():
                with open(self.config_path) as f:
                    self.data = yaml.safe_load(f)
                logger.info(f"Loaded infrastructure config from {self.config_path}")
            else:
                logger.warning(f"Infrastructure config not found at {self.config_path}")
        except Exception as e:
            logger.error(f"Failed to load user config: {e}")

    def get_node_info(self, node_id: str) -> str:
        """Get description of a node."""
        for node in self.data.get("nodes", []):
            if node["id"] == node_id or node["name"] == node_id:
                return f"🖥 **{node['name']}**\nIP: `{node.get('ip', 'N/A')}`\nType: {node.get('type')}\nServices: {', '.join([s['name'] for s in node.get('services', [])])}"
        return "Node not found."

    def get_summary(self) -> str:
        """Get summary of all nodes."""
        summary = "🏗 **Infrastructure Summary**\n\n"
        for node in self.data.get("nodes", []):
            # We could add ping check here later
            summary += f"🔹 `{node['id']}` ({node['name']})\n"
        return summary

    async def check_nodes(self) -> str:
        """Ping nodes to check availability using Tailscale ping."""
        import platform
        import socket

        report = "📡 **Network Status**\n\n"

        # Get local IPs and hostname to detect self
        local_ips = set()
        local_hostname = ""
        try:
            local_hostname = socket.gethostname().lower()
            # Get all local IPs
            for info in socket.getaddrinfo(local_hostname, None):
                local_ips.add(info[4][0])
            # Also try to get Tailscale IP (may fail in WSL2)
            try:
                proc = await asyncio.create_subprocess_exec(
                    "/snap/bin/tailscale", "ip", "-4",
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.DEVNULL
                )
                stdout, _ = await proc.communicate()
                if proc.returncode == 0:
                    local_ips.add(stdout.decode().strip())
            except FileNotFoundError:
                # Tailscale CLI not available (e.g., WSL2 uses Windows Tailscale)
                pass
        except Exception:
            pass

        for node in self.data.get("nodes", []):
            ip = node.get("ip")
            node_name = node.get("name", node["id"])

            if not ip or ip == "N/A" or "Placeholder" in str(ip):
                report += f"⚪️ {node_name} (No IP)\n"
                continue

            # Check if this is the local machine (self)
            # Match by IP or by hostname pattern (for WSL2 where Tailscale runs on Windows)
            node_id = node.get("id", "").lower()
            is_self = ip in local_ips
            # Also check if node id matches hostname pattern (e.g., igor-gaming-1 matches Igor-Gaming)
            if local_hostname and (
                local_hostname in node_id or
                node_id.replace("-1", "").replace("-", "") in local_hostname.replace("-", "")
            ):
                is_self = True

            if is_self:
                report += f"🟢 Online (self) {node_name} ({ip})\n"
                continue

            try:
                # Try Tailscale ping first (more reliable for mesh VPN)
                proc = await asyncio.wait_for(
                    asyncio.create_subprocess_exec(
                        "/snap/bin/tailscale", "ping", "-c", "1", str(ip),
                        stdout=asyncio.subprocess.PIPE,
                        stderr=asyncio.subprocess.DEVNULL
                    ),
                    timeout=5.0
                )
                stdout, _ = await proc.communicate()

                if proc.returncode == 0:
                    # Check if it's a direct connection
                    is_direct = b"direct" in stdout
                    status = "🟢 Online" + (" (direct)" if is_direct else " (relay)")
                    report += f"{status} {node_name} ({ip})\n"
                else:
                    # Fallback to regular ping
                    param = "-c" if platform.system().lower() != "windows" else "-n"
                    proc2 = await asyncio.wait_for(
                        asyncio.create_subprocess_exec(
                            "ping", param, "1", str(ip),
                            stdout=asyncio.subprocess.DEVNULL,
                            stderr=asyncio.subprocess.DEVNULL
                        ),
                        timeout=3.0
                    )
                    await proc2.wait()

                    if proc2.returncode == 0:
                        report += f"🟢 Online {node_name} ({ip})\n"
                    else:
                        report += f"🔴 Offline {node_name} ({ip})\n"

            except asyncio.TimeoutError:
                report += f"⏱ Timeout {node_name} ({ip})\n"
            except FileNotFoundError:
                # Tailscale not found, use regular ping
                try:
                    param = "-c" if platform.system().lower() != "windows" else "-n"
                    proc = await asyncio.wait_for(
                        asyncio.create_subprocess_exec(
                            "ping", param, "1", str(ip),
                            stdout=asyncio.subprocess.DEVNULL,
                            stderr=asyncio.subprocess.DEVNULL
                        ),
                        timeout=3.0
                    )
                    await proc.wait()
                    status = "🟢 Online" if proc.returncode == 0 else "🔴 Offline"
                    report += f"{status} {node_name} ({ip})\n"
                except Exception:
                    report += f"❌ Error {node_name} ({ip})\n"
            except Exception as e:
                report += f"❌ {node_name}: {str(e)[:30]}\n"

        return report
