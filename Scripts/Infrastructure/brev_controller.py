import os
import subprocess
import json
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger("BrevController")


class BrevController:
    """
    Manages Brev.dev GPU instances for the Unified System.
    Requires 'brev' CLI to be installed (brew install brevdev/brev/brev).
    """

    def __init__(self, instance_name: str = "adf-gpu-instance"):
        self.instance_name = instance_name
        self.api_key = os.getenv("BREV_API_KEY")

    def _run_cmd(self, cmd: list) -> Optional[str]:
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            logger.error(f"Brev Command Failed: {e.stderr}")
            return None
        except FileNotFoundError:
            logger.error("Brev CLI not found. Please install it: 'brew install brevdev/brev/brev'")
            return None

    def get_status(self) -> Optional[str]:
        """Check if instance is RUNNING, STOPPED, or NOT_FOUND."""
        output = self._run_cmd(["brev", "ls", "--json"])
        if not output:
            return "UNKNOWN"

        try:
            instances = json.loads(output)
            for inst in instances:
                if inst.get("name") == self.instance_name:
                    return inst.get("status", "UNKNOWN").upper()
            return "NOT_FOUND"
        except Exception as e:
            logger.error(f"Error parsing brev output: {e}")
            return "ERROR"

    def start_instance(self) -> bool:
        """Starts the instance if it's not already running."""
        status = self.get_status()
        if status == "RUNNING":
            logger.info(f"Instance {self.instance_name} is already running.")
            return True

        logger.info(f"Starting Brev instance: {self.instance_name}...")
        res = self._run_cmd(["brev", "start", self.instance_name])
        return res is not None

    def stop_instance(self) -> bool:
        """Stops the instance to save credits/usage."""
        logger.info(f"Stopping Brev instance: {self.instance_name}...")
        res = self._run_cmd(["brev", "stop", self.instance_name])
        return res is not None

    def get_ssh_url(self) -> Optional[str]:
        """Returns the SSH or internal URL for the NIM endpoint if applicable."""
        # Note: Brev usually provides SSH access. For NIM, we need the HTTP port.
        # This is a placeholder logic for the specific NIM tunnel/ip.
        output = self._run_cmd(["brev", "ls", "--json"])
        if not output:
            return None

        try:
            instances = json.loads(output)
            for inst in instances:
                if inst.get("name") == self.instance_name:
                    # Logic to extract IP or Hostname
                    return inst.get("hostname")
            return None
        except:
            return None


if __name__ == "__main__":
    # Test
    logging.basicConfig(level=logging.INFO)
    ctrl = BrevController()
    print(f"Status: {ctrl.get_status()}")
