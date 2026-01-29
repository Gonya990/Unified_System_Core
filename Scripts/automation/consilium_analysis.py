import os
import json
import subprocess
from pathlib import Path

# SECURE CONFIG
ARCHIVE_DIR = Path("/mnt/data/Archives")
SECURE_VAULT = Path("/mnt/secure_vault")
DATABASE_DIR = SECURE_VAULT / "database"
LOG_DIR = SECURE_VAULT / "logs"

# Ensure dirs exist inside the vault
DATABASE_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

MODELS = ["llama3:8b", "llama3.2:latest"] # The Consilium

def run_ollama(prompt, model):
    try:
        result = subprocess.run(
            ["ollama", "run", model, prompt],
            capture_output=True, text=True, timeout=120
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Error: {e}"

def analyze_content_type(text):
    """Detect if content is financial, brand, or personal"""
    keywords = {
        "FINANCIAL": ["invoice", "bank", "balance", "credit", "payment", "transaction", "tax", "счет", "банк", "оплата"],
        "BRAND": ["strategy", "logo", "content", "marketing", "competitor", "reels", "vision", "стратегия", "бренд"],
        "PERSONAL": ["photo", "message", "chat", "email", "history"]
    }
    found = []
    text_lower = text.lower()
    for category, kws in keywords.items():
        if any(kw in text_lower for kw in kws):
            found.append(category)
    return found if found else ["GENERAL"]

def process_file(file_path):
    print(f"🧐 Consilium Analysing: {file_path.name}")
    
    # 1. Decrypt locally to vault (RAM-like speed inside ext4 on img)
    temp_file = SECURE_VAULT / f"temp_{file_path.stem}"
    try:
        if file_path.suffix == ".gpg":
            subprocess.run([
                "gpg", "--batch", "--yes", "--output", str(temp_file), 
                "--decrypt", str(file_path)
            ], check=True)
        else:
            # If it's a raw file, copy to temp
            import shutil
            shutil.copy2(file_path, temp_file)
            
        # 2. Extract content
        # For simplicity, we sample the header and metadata
        with open(temp_file, 'rb') as f:
            sample = f.read(5000).decode('utf-8', errors='ignore')
            
        # 3. Classify
        tags = analyze_content_type(sample)
        print(f"   Tags identified: {tags}")
        
        # 4. Ask the Consilium (Multiple Agents)
        results = {}
        target_dir = DATABASE_DIR
        if "FINANCIAL" in tags:
            target_dir = SECURE_VAULT / "financial_data"
            target_dir.mkdir(exist_ok=True)
            print("   ⚠️ FINANCIAL DATA DETECTED. Routing to hardened sub-vault.")

        for model in MODELS:
            prompt = f"Analyze this content fragment. Categories: {tags}. Extract key entities, dates, and actionable info. Content: {sample[:2000]}"
            print(f"   -> Agent {model} is thinking...")
            results[model] = run_ollama(prompt, model)
            
        # 5. Save to Database
        doc_id = file_path.stem
        record = {
            "source": str(file_path),
            "tags": tags,
            "consilium_reports": results,
            "processed_at": "2026-01-28"
        }
        
        with open(target_dir / f"{doc_id}.json", "w") as f:
            json.dump(record, f, indent=2)
            
        print(f"✅ Indexed {doc_id} to Secure Vault")
        
    finally:
        # 5. SECURE WIPE
        if temp_file.exists():
            subprocess.run(["shred", "-u", str(temp_file)])

def start_processing():
    print("🚀 VIBRANIUM SECURE ANALYSIS STARTING...")
    # Find all GPG files
    gpg_files = list(ARCHIVE_DIR.rglob("*.gpg"))
    print(f"📦 Found {len(gpg_files)} encrypted archives to process.")
    
    for f in gpg_files:
        try:
            process_file(f)
        except Exception as e:
            print(f"❌ Failed to process {f.name}: {e}")

if __name__ == "__main__":
    start_processing()
