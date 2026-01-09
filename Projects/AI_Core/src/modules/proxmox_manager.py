import subprocess
import logging
import os
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class ProxmoxManager:
    """Orchestrates Proxmox VMs via direct SSH and qm commands."""
    
    def __init__(self):
        self.pve_host = os.environ.get("PVE_HOST", "100.78.145.67")
        self.pve_user = os.environ.get("PVE_USER", "root")

    def _run_ssh_cmd(self, cmd):
        ssh_cmd = f"ssh -o StrictHostKeyChecking=no {self.pve_user}@{self.pve_host} \"{cmd}\""
        try:
            result = subprocess.check_output(ssh_cmd, shell=True, stderr=subprocess.STDOUT)
            return result.decode().strip()
        except subprocess.CalledProcessError as e:
            logger.error(f"SSH Command failed: {e.output.decode()}")
            return None

    def get_vm_status(self, vmid):
        logger.info(f"Checking status of VM {vmid}...")
        res = self._run_ssh_cmd(f"qm status {vmid}")
        if res and "status: running" in res:
            return "running"
        return "stopped"

    def stop_vm(self, vmid, timeout=60):
        logger.info(f"Gracefully stopping VM {vmid}...")
        self._run_ssh_cmd(f"qm shutdown {vmid}")
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            status = self.get_vm_status(vmid)
            if status == "stopped":
                logger.info(f"VM {vmid} stopped.")
                return True
            time.sleep(3)
        
        logger.warning(f"VM {vmid} did not stop gracefully. Forcing stop...")
        self._run_ssh_cmd(f"qm stop {vmid}")
        return True

    def start_vm(self, vmid):
        logger.info(f"Starting VM {vmid}...")
        self._run_ssh_cmd(f"qm start {vmid}")
        logger.info(f"VM {vmid} start command sent.")

    def switch_to_gaming(self, ai_vmid=106, gaming_vmid=100):
        """AI (with GPU) -> Gaming (with GPU)"""
        logger.info("🎮 TRANSITION: AI -> GAMING")
        self.stop_vm(ai_vmid)
        self.start_vm(gaming_vmid)
        logger.info("✅ Mode: GAMING")

    def switch_to_ai(self, ai_vmid=106, gaming_vmid=100):
        """Gaming (with GPU) -> AI (with GPU)"""
        logger.info("🧠 TRANSITION: GAMING -> AI")
        self.stop_vm(gaming_vmid)
        self.start_vm(ai_vmid)
        logger.info("✅ Mode: AI")

if __name__ == "__main__":
    # Test script: check status of AI and Gaming VMs
    manager = ProxmoxManager()
    print(f"AI VM (106) Status: {manager.get_vm_status(106)}")
    print(f"Gaming VM (100) Status: {manager.get_vm_status(100)}")
