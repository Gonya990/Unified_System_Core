from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn
import threading
import os
from pathlib import Path
from usage_tracker import UsageTracker
from infrastructure import InfrastructureManager

# Init FastAPI
app = FastAPI(title="Unified Bot Dashboard")

# Setup Templates
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Global Context (inserted by main.py)
bot_context = {}

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    # Get Infrastructure Data
    infra_mgr = bot_context.get("infra")
    infra_data = infra_mgr.data.get("nodes", []) if infra_mgr else []
    
    # Get Usage Data
    usage_tracker = bot_context.get("usage")
    stats = usage_tracker.get_user_stats(0) if usage_tracker else "N/A"
    
    # Get GPU/Proxmox Status (Live)
    proxmox = bot_context.get("proxmox")
    gpu_status = "N/A"
    if proxmox:
        ai_vm_status = proxmox.get_vm_status(106)
        gaming_vm_status = proxmox.get_vm_status(100)
        if ai_vm_status == "running":
            gpu_status = "🧠 AI Cluster (VM 106)"
        elif gaming_vm_status == "running":
            gpu_status = "🎮 Gaming (VM 100)"
        else:
            gpu_status = "💤 Off"

    # Get Swarm Health
    inference = bot_context.get("inference")
    swarm_count = 0
    if inference and inference.swarm:
        swarm_count = inference.swarm.get_stats().get("gemini_keys_active", 0)
    
    return templates.TemplateResponse("index.html", {
        "request": request,
        "nodes": infra_data,
        "bot_status": "Online 🟢",
        "stats": stats,
        "gpu_status": gpu_status,
        "swarm_count": swarm_count
    })

@app.get("/logs")
async def get_logs():
    """Read last 50 lines of log file if exists."""
    log_file = "bot.log" # Make sure check config where logs are
    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            lines = f.readlines()
            return {"logs": lines[-50:]}
    return {"logs": ["Log file not found"]}

@app.get("/stats/tokens")
async def get_token_stats():
    """Get token usage statistics for chart."""
    usage_tracker = bot_context.get("usage")
    if not usage_tracker:
        return {"dates": [], "tokens": []}
    
    return usage_tracker.get_daily_usage(days=7)

@app.get("/search/notes")
async def search_notes(q: str):
    """Search Notion notes."""
    notion = bot_context.get("notion")
    if not notion:
        return {"results": []}
    
    results = await notion.search_pages(q)
    return {"results": results}

@app.post("/action/{action}")
async def run_action(action: str):
    """Execute management actions."""
    if action == "backup":
        # Trigger backup (would need access to bot instance)
        return {"message": "Backup triggered (not implemented yet)"}
    
    elif action == "restart":
        import subprocess
        subprocess.Popen(["sudo", "systemctl", "restart", "ai-bot"])
        return {"message": "Bot restarting..."}
    
    return {"message": f"Unknown action: {action}"}

class DashboardService:
    def __init__(self, port=8096, context=None):
        self.port = port
        self.context = context or {}
        
    def start(self):
        # Inject context into app global
        global bot_context
        bot_context.update(self.context)
        
        # Run Uvicorn in a separate thread
        thread = threading.Thread(target=self._run_server, daemon=True)
        thread.start()
        
    def _run_server(self):
        uvicorn.run(app, host="0.0.0.0", port=self.port, log_level="warning")
