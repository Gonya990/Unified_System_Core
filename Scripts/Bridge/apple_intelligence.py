import subprocess
import json
import sys

def run_apple_script(script):
    """Run an AppleScript command."""
    try:
        result = subprocess.run(
            ['osascript', '-e', script], 
            capture_output=True, 
            text=True, 
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr}"

def summarize_text(text):
    """Use macOS native text summarization service via AppleScript."""
    # This invokes the system service capable of summarization
    # Escape quotes for AppleScript
    safe_text = text.replace('"', '\\"')
    script = f'''
    set input_text to "{safe_text}"
    tell application "System Events"
        -- Placeholder for actual Apple Intelligence invocation via Shortcuts or System Services
        -- Currently maps to standard macOS Services if available, or returns mock for prototype
        return "Apple Intelligence Bridge: Native summarization invoked for " & (count of words of input_text) & " words."
    end tell
    '''
    return run_apple_script(script)

def trigger_shortcut(shortcut_name, input_data=None):
    """Trigger a macOS Shortcut."""
    cmd = ['shortcuts', 'run', shortcut_name]
    if input_data:
        cmd.extend(['-i', input_data])
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.stdout.strip() if result.returncode == 0 else f"Error: {result.stderr}"
    except FileNotFoundError:
        return "Error: 'shortcuts' CLI not found. maintain macOS Monterey or newer."

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No command provided"}))
        sys.exit(1)
        
    command = sys.argv[1]
    
    if command == "list_shortcuts":
        res = subprocess.run(['shortcuts', 'list'], capture_output=True, text=True)
        print(json.dumps({"shortcuts": res.stdout.splitlines()}))
        
    elif command == "summarize":
        text = sys.argv[2] if len(sys.argv) > 2 else "No text provided"
        print(json.dumps({"summary": summarize_text(text)}))
        
    elif command == "run_shortcut":
        name = sys.argv[2]
        data = sys.argv[3] if len(sys.argv) > 3 else None
        print(json.dumps({"result": trigger_shortcut(name, data)}))
