import subprocess
import sys
import os

print("PATH:", os.environ.get("PATH"))
try:
    print("Attempting to run 'go version'...")
    result = subprocess.run(["go", "version"], capture_output=True, text=True)
    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)
    print("Return Code:", result.returncode)
except FileNotFoundError:
    print("Executable 'go' not found in PATH.")
except Exception as e:
    print(f"Error: {e}")
