import os
import threading
from pathlib import Path
from typing import Optional

import uvicorn
from fastapi import Cookie, Depends, FastAPI, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

# Init FastAPI
app = FastAPI(title="Unified Bot Dashboard")

# Setup Templates
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Global Context (inserted by main.py)
bot_context = {}

async def get_current_user(request: Request, session_token: Optional[str] = Cookie(None)):
    """Dependency to get the current authenticated user."""
    usage_tracker = bot_context.get("usage")
    if not session_token or not usage_tracker:
        raise HTTPException(
            status_code=status.HTTP_307_TEMPORARY_REDIRECT,
            headers={"Location": "/login-required"}
        )

    user_id = usage_tracker.verify_session(session_token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_307_TEMPORARY_REDIRECT,
            headers={"Location": "/login-required"}
        )

    # Get user data from bot's DB
    bot_db = bot_context.get("db") # Assumes db is passed in context
    user_data = bot_db.get_user(user_id) if bot_db else None

    if not user_data:
        raise HTTPException(status_code=403, detail="User data not found")

    return user_data

@app.get("/auth")
async def auth(token: str):
    """Verify Telegram token and set session cookie."""
    usage_tracker = bot_context.get("usage")
    if not usage_tracker:
        return {"error": "Usage tracker not available"}

    user_id = usage_tracker.verify_session(token)
    if user_id:
        response = RedirectResponse(url="/")
        response.set_cookie(key="session_token", value=token, httponly=True, max_age=86400)
        return response

    return HTMLResponse("❌ Invalid or expired token. Please generate a new one via /login in the bot.")

@app.get("/login-required", response_class=HTMLResponse)
async def login_required(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, user: dict = Depends(get_current_user)):
    user_id = user.get('user_id')
    branch_id = user.get('branch_id', 'HOME_HQ')
    role = user.get('role', 'MEMBER')

    # Get Infrastructure Data - Filtered by branch
    infra_mgr = bot_context.get("infra")
    all_nodes = infra_mgr.data.get("nodes", []) if infra_mgr else []

    # RBAC: Only HOME_HQ or Admins see full infra. Others see only their status.
    if branch_id == 'HOME_HQ' or role == 'ADMIN':
        infra_data = all_nodes
    else:
        # Simple members only see their own usage/stats (placeholder filter)
        infra_data = [n for n in all_nodes if n.get('branch_id') == branch_id]

    # Get Usage Data
    usage_tracker = bot_context.get("usage")
    stats = usage_tracker.get_user_stats(user_id) if usage_tracker else "N/A"

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

    # Get Kostik's Agent Status (MCP Mail)
    kosta_status = "Working ⚡" # Default to active as it's part of the mesh
    try:
        # Quick check if MCP server is reachable locally
        import requests
        r = requests.get("http://localhost:8765", timeout=0.1)
        if r.status_code < 500:
            kosta_status = "Working ⚡"
        else:
            kosta_status = "Resting 💤"
    except Exception:
        kosta_status = "Busy ⚙️"

    return templates.TemplateResponse("index.html", {
        "request": request,
        "nodes": infra_data,
        "bot_status": "Online 🟢",
        "stats": stats,
        "gpu_status": gpu_status,
        "swarm_count": swarm_count,
        "kosta_status": kosta_status
    })

@app.get("/logs")
async def get_logs():
    """Read last 50 lines of log file if exists."""
    log_file = "bot.log" # Make sure check config where logs are
    if os.path.exists(log_file):
        with open(log_file) as f:
            lines = f.readlines()
            return {"logs": lines[-50:]}
    return {"logs": ["Log file not found"]}

@app.get("/stats")
async def get_stats_redirect():
    """Redirect /stats to /api/stats/system for backward compatibility or ease."""
    return await get_system_stats()

@app.get("/stats/tokens")
async def get_token_stats():
    """Get token usage statistics for chart."""
    usage_tracker = bot_context.get("usage")
    if not usage_tracker:
        return {"dates": [], "tokens": []}

    return usage_tracker.get_daily_usage(days=7)

@app.get("/api/stats/system")
async def get_system_stats():
    """Get real-time system statistics for frontend widgets."""
    import time

    import psutil

    # System Metrics
    cpu_percent = psutil.cpu_percent()
    ram_obj = psutil.virtual_memory()
    ram_percent = ram_obj.percent

    # Swarm Status
    inference = bot_context.get("inference")
    active_keys = 0
    if inference and inference.swarm:
        active_keys = inference.swarm.get_stats().get("gemini_keys_active", 0)

    # Kosta Status
    kosta_ok = False
    try:
        import requests
        # Try local first, then remote
        try:
            r = requests.get("http://localhost:8765", timeout=0.2)
            if r.status_code < 500: kosta_ok = True
        except Exception:
            r = requests.get("http://100.110.209.49:8765", timeout=0.5)
            if r.status_code < 500: kosta_ok = True
    except: pass

    return {
        "cpu": cpu_percent,
        "ram": ram_percent,
        "swarm_keys": active_keys,
        "kosta_status": "Online" if kosta_ok else "Offline",
        "timestamp": time.time()
    }

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
