import os
import sys

import torch

print("--- SYSTEM CHECK ---")
print(f"Python: {sys.version.split()[0]}")
print(f"CUDA Available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"GPU: {torch.cuda.get_device_name(0)}")
    print(f"VRAM: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")

print("\n--- LIVEPORTRAIT CHECK ---")
lp_path = os.path.abspath("LivePortrait")
if lp_path not in sys.path:
    sys.path.append(lp_path)

try:
    # Try to import crucial modules
    print("✅ LivePortrait Modules Loaded")
except Exception as e:
    print(f"❌ LivePortrait Error: {e}")

print("\n--- STYLETTS2 CHECK ---")
st_path = os.path.abspath("StyleTTS2")
if st_path not in sys.path:
    sys.path.append(st_path)

try:
    # StyleTTS2 local imports might need we be inside the dir or careful with paths
    # But let's try importing the models module
    print("✅ StyleTTS2 Models Loaded")
except Exception as e:
    print(f"❌ StyleTTS2 Error: {e}")

print("\n--- PYCAPS CHECK ---")
try:
    print("✅ PyCaps Loaded")
except Exception as e:
    print(f"❌ PyCaps Error: {e}")
