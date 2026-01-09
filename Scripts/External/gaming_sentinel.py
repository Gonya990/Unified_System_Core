import os
import time
import requests
import psutil
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# CONFIGURATION
CORE_URL = "http://100.110.209.49:8080/webhook/reclaim" # Example endpoint
IDLE_THRESHOLD_MINS = 30
CHECK_INTERVAL_SECS = 60

def is_gaming_active():
    """
    Check for active streaming or high GPU load.
    Adjust process names based on setup (Sunshine, Moonlight, Steam, etc.)
    """
    active_processes = ["Sunshine.exe", "Moonlight.exe", "Steam.exe"]
    
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] in active_processes:
            # You could add further checks here, like network connection count for Sunshine
            return True
    return False

def get_idle_time():
    """Returns the time in seconds since the last user input (keyboard/mouse)."""
    # Note: On Windows this requires ctypes and GetLastInputInfo
    try:
        import ctypes
        class LASTINPUTINFO(ctypes.Structure):
            _fields_ = [
                ("cbSize", ctypes.c_uint),
                ("dwTime", ctypes.c_uint),
            ]
        
        lii = LASTINPUTINFO()
        lii.cbSize = ctypes.sizeof(LASTINPUTINFO)
        ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lii))
        millis = ctypes.windll.kernel32.GetTickCount() - lii.dwTime
        return millis / 1000.0
    except Exception:
        return 0 # Fallback if not on Windows or error

def main():
    logger.info("Sentinel started. Monitoring for idle gaming session...")
    idle_start = None
    
    while True:
        gaming = is_gaming_active()
        idle_time = get_idle_time()
        
        if not gaming or idle_time > (IDLE_THRESHOLD_MINS * 60):
            if idle_start is None:
                idle_start = time.time()
                logger.info(f"System detected as idle. Starting reclaim timer ({IDLE_THRESHOLD_MINS}m)...")
            
            elapsed = (time.time() - idle_start) / 60
            if elapsed >= IDLE_THRESHOLD_MINS:
                logger.warning("IDLE THRESHOLD REACHED. Sending reclaim request to Core.")
                try:
                    requests.post(CORE_URL, json={"status": "idle", "vmid": 100})
                    # Optional: Shutdown itself if core doesn't do it via Proxmox
                    # os.system("shutdown /s /t 60")
                except Exception as e:
                    logger.error(f"Failed to notify core: {e}")
        else:
            if idle_start is not None:
                logger.info("Activity detected. Resetting idle timer.")
            idle_start = None
            
        time.sleep(CHECK_INTERVAL_SECS)

if __name__ == "__main__":
    main()
