import os
import time
import threading
import subprocess
from pathlib import Path

import firebase_admin
from firebase_admin import credentials, firestore

SRC_DIR = Path(__file__).parent.parent.resolve()

def init_firebase():
    if not firebase_admin._apps:
        # Search for credentials
        possible_paths = [
            SRC_DIR.parent.parent / "unified-core-service-account.json",
            SRC_DIR.parent.parent / "Projects" / "AI_Core" / "unified-core-service-account.json",
            Path.home() / "unified-core-service-account.json"
        ]
        
        cred_path = None
        for p in possible_paths:
            if p.exists():
                cred_path = p
                break
                
        if cred_path:
            cred = credentials.Certificate(str(cred_path))
            firebase_admin.initialize_app(cred)
        else:
            print("❌ Firebase credentials not found. Ensure unified-core-service-account.json is present.")
            exit(1)
    return firestore.client()

db = init_firebase()

def process_job(doc_id, job):
    def _run():
        try:
            print(f"🚀 Starting Factory Job {doc_id}...")
            db.collection("factory_jobs").document(doc_id).update({"status": "processing", "progress": 10})
            
            # Run orchestrator
            text = job.get("text", "")
            script_path = SRC_DIR / "pipeline" / "orchestrator_v4_advanced.py"
            
            # Run orchestrator
            cmd = ["python", str(script_path), text]
            print(f"Running: {' '.join(cmd)}")
            subprocess.run(cmd, check=True)
            
            # Update status
            db.collection("factory_jobs").document(doc_id).update({"status": "ready", "progress": 100})
            print(f"✅ Factory Job {doc_id} complete.")
            
        except Exception as e:
            print(f"❌ Error in job {doc_id}: {e}")
            db.collection("factory_jobs").document(doc_id).update({"status": "error"})
            
    threading.Thread(target=_run).start()

def process_upload(doc_id, job):
    def _run():
        try:
            print(f"🚀 Publishing Job {doc_id} to YouTube...")
            db.collection("factory_jobs").document(doc_id).update({"status": "publishing"})
            
            script_path = SRC_DIR / "uploaders" / "youtube_uploader.py"
            cmd = ["python", str(script_path)]
            subprocess.run(cmd, check=True)
            
            db.collection("factory_jobs").document(doc_id).update({"status": "published"})
            print(f"✅ Job {doc_id} published successfully.")
        except Exception as e:
            print(f"❌ Error publishing job {doc_id}: {e}")
            db.collection("factory_jobs").document(doc_id).update({"status": "error"})

    threading.Thread(target=_run).start()

def on_snapshot(col_snapshot, changes, read_time):
    for change in changes:
        if change.type.name == 'ADDED' or change.type.name == 'MODIFIED':
            doc = change.document
            data = doc.to_dict()
            status = data.get('status')
            
            if status == 'pending':
                process_job(doc.id, data)
            elif status == 'approved':
                process_upload(doc.id, data)

def main():
    print("🏭 Starting Content Factory Firebase Listener...")
    col_query = db.collection('factory_jobs')
    col_watch = col_query.on_snapshot(on_snapshot)
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down.")

if __name__ == "__main__":
    main()
