from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import uvicorn
import asyncio
import threading
import os
from pathlib import Path
from .usage_tracker import UsageTracker
from .infrastructure import InfrastructureManager

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
    
    # Get Usage Data (Mock for now, or read from DB)
    usage_tracker = bot_context.get("usage")
    stats = usage_tracker.get_user_stats(0) if usage_tracker else "N/A" # 0 = all users if implemented
    
    return templates.TemplateResponse("index.html", {
        "request": request,
        "nodes": infra_data,
        "bot_status": "Online 🟢",
        "stats": stats
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
    
    # Mock data for now (would need to query DB by date)
    # TODO: Implement daily aggregation in UsageTracker
    return {
        "dates": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "tokens": [1200, 1500, 900, 2100, 1800, 1300, 1600]
    }

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
