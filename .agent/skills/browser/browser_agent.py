#!/usr/bin/env python3
import json
import socket
import sys
import os
from pathlib import Path

SOCKET_PATH = "/tmp/nodriver.sock"

def send_command(cmd):
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        sock.connect(SOCKET_PATH)
        sock.send(json.dumps(cmd).encode())
        response = b""
        while True:
            chunk = sock.recv(65536)
            if not chunk: break
            response += chunk
        return json.loads(response.decode())
    except Exception as e:
        return {"ok": False, "error": str(e)}
    finally:
        sock.close()

def analyze():
    status = send_command({"action": "status"})
    elements = send_command({"action": "elements"})
    
    print("-" * 50)
    print(f"URL: {status.get('current_url', 'unknown')}")
    print("-" * 50)
    print("INTERACTABLE ELEMENTS:")
    
    if elements.get("ok"):
        for i, el in enumerate(elements.get("elements", [])):
            text = el.get("text", "[no text]")
            tag = el.get("tag", "el")
            selector = el.get("selector", "none")
            print(f"{i:2d}. [{tag:6}] {text[:50]:50} | {selector}")
    else:
        print(f"Error: {elements.get('error')}")
    print("-" * 50)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "analyze":
        analyze()
    else:
        print("Usage: browser_agent.py analyze")
