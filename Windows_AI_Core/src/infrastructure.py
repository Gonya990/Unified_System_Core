"""
Infrastructure Manager for AI Bot.
Reads infrastructure.yaml and provides information about the network.
"""
import yaml
import logging
import asyncio
from pathlib import Path
from typing import Dict, Any

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
                with open(self.config_path, "r") as f:
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
            status = "⚪️" # Unknown
            # We could add ping check here later
            summary += f"🔹 `{node['id']}` ({node['name']})\n"
        return summary
    
    async def check_nodes(self) -> str:
        """Ping nodes to check availability."""
        import platform
        import subprocess
        
        report = "📡 **Network Status**\n\n"
        
        for node in self.data.get("nodes", []):
            ip = node.get("ip")
            if not ip or ip == "N/A" or "Placeholder" in str(ip):
                report += f"⚪️ `{node['id']}` (No IP)\n"
                continue
                
            # Ping
            param = "-n" if platform.system().lower() == "windows" else "-c"
            command = ["ping", param, "1", str(ip)]
            
            try:
                # Async ping check would be better, but subprocess is ok for quick check
                proc = await asyncio.create_subprocess_exec(
                    "ping", param, "1", str(ip),
                    stdout=asyncio.subprocess.DEVNULL,
                    stderr=asyncio.subprocess.DEVNULL
                )
                await proc.wait()
                
                status = "🟢 Online" if proc.returncode == 0 else "🔴 Offline"
                report += f"{status} `{node['id']}` ({ip})\n"
            except Exception as e:
                 report += f"❌ `{node['id']}` (Ping error)\n"
                 
        return report
