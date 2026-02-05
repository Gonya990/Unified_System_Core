
import os
import sys

BASE_DIR = "/home/gonya/Unified_System_Core/Projects/AI_Core/src"

def patch_bot_v2():
    path = os.path.join(BASE_DIR, "ai_telegram_bot_v2.py")
    with open(path, "r") as f:
        content = f.read()
    
    # Fix paths
    old_path = '/home/gonya/Documents/Unified_System'
    new_path = '/home/gonya/Unified_System_Core/Projects/AI_Core'
    
    if old_path in content:
        content = content.replace(old_path, new_path)
        print(f"✅ Patched path in ai_telegram_bot_v2.py")
    else:
        print(f"⚠️ Path string not found in ai_telegram_bot_v2.py")

    with open(path, "w") as f:
        f.write(content)

def patch_inference():
    path = os.path.join(BASE_DIR, "inference_client.py")
    with open(path, "r") as f:
        content = f.read()
    
    # Fix default URL
    old_url = 'http://localhost:11434'
    new_url = 'http://host.docker.internal:11434'
    
    if old_url in content:
        content = content.replace(old_url, new_url)
        print(f"✅ Patched URL in inference_client.py")
    else:
         print(f"⚠️ URL string not found in inference_client.py")
         
    with open(path, "w") as f:
        f.write(content)

def patch_ha_controller():
    path = os.path.join(BASE_DIR, "ha_controller.py")
    with open(path, "r") as f:
        content = f.read()
    
    # Fix import
    # Current: from ha_client import HAConfig, HomeAssistantClient
    # New: 
    # try:
    #     from .ha_client import HAConfig, HomeAssistantClient
    # except ImportError:
    #     from ha_client import HAConfig, HomeAssistantClient

    target_import = "from ha_client import HAConfig, HomeAssistantClient"
    replacement = """try:
    from .ha_client import HAConfig, HomeAssistantClient
except ImportError:
    from ha_client import HAConfig, HomeAssistantClient"""
    
    if target_import in content and "try:" not in content.split(target_import)[0][-20:]: 
        # Only replace if not already inside a try block (simple check)
        content = content.replace(target_import, replacement)
        print(f"✅ Patched import in ha_controller.py")
    else:
        print(f"⚠️ Import string mismatch or already patched in ha_controller.py")

    with open(path, "w") as f:
        f.write(content)

if __name__ == "__main__":
    patch_bot_v2()
    patch_inference()
    patch_ha_controller()
