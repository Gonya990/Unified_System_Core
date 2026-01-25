import subprocess
import os
import sys

log_file = '/Users/igorgoncharenko/Documents/Unified_System_Core/python_debug.log'

def log(msg):
    with open(log_file, 'a') as f:
        f.write(msg + "\n")

try:
    # Clear log
    with open(log_file, 'w') as f:
        f.write("=== Python Debug Log ===\n")
    
    # 1. Check CWD
    cwd = os.getcwd()
    log(f"CWD: {cwd}")
    
    # 2. Check Node Path
    node_dir = os.path.join(cwd, "tools/node-v20.11.0-darwin-arm64/bin")
    node_exe = os.path.join(node_dir, "node")
    log(f"Looking for node at: {node_exe}")
    
    if os.path.exists(node_exe):
        log("Node executable matches.")
        # Try running it
        res = subprocess.run([node_exe, '--version'], capture_output=True, text=True)
        log(f"Node Output: {res.stdout.strip()}")
        log(f"Node Error: {res.stderr.strip()}")
    else:
        log("❌ Node executable NOT found.")
        
    # 3. Check n8n
    n8n_path = "/Users/igorgoncharenko/Documents/Unified_System_Core/tools/npm-global/bin/n8n"
    if os.path.exists(n8n_path):
         log(f"n8n found at {n8n_path}")
    else:
         log(f"n8n NOT found at {n8n_path}")
         
except Exception as e:
    log(f"🔥 Exception: {e}")
