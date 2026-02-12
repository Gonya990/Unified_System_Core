
import json
import os
import sqlite3
from collections import Counter

import requests

# Configuration
INDEX_FILE = "/home/gonya/Unified_System_Core/Projects/Content_Factory/config/knowledge_base_index.json"
DB_PATH = "/home/gonya/storage.sqlite3" # The one we imported Facebook messages into
OLLAMA_URL = "http://host.docker.internal:11434/api/generate"
MODEL = "llama3.2" # Or gemini if configured

def get_recent_topics(db_path, limit=50):
    """Extract potential topics from recent messages."""
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        # Get recent messages from the user (assuming sender_id 0 or 1 is user, or just generic analysis)
        # We'll just grab recent messages for now as a sample.
        cur.execute("SELECT body_md, created_ts FROM messages ORDER BY created_ts DESC LIMIT ?", (limit,))
        rows = cur.fetchall()
        conn.close()
        return [r[0] for r in rows if r[0]]
    except Exception as e:
        print(f"⚠️ Could not read DB: {e}")
        return []

def analyze_index(index_path):
    """Analyze file structure to guess content themes."""
    with open(index_path) as f:
        data = json.load(f)

    docs = data.get('documents', [])
    media = data.get('media_assets', [])

    # Extract keywords from filenames
    keywords = []
    for item in docs + media:
        name = item['filename'].lower()
        # Simple cleanup
        name = os.path.splitext(name)[0].replace('_', ' ').replace('-', ' ')
        keywords.extend(name.split())

    # Filter common stop words (very basic)
    stop_words = {'video', 'image', 'photo', 'chat', 'message', 'copy', 'of', 'the', 'and', 'json', 'html', 'txt', 'jpg', 'mp4'}
    keywords = [w for w in keywords if w not in stop_words and len(w) > 3]

    common = Counter(keywords).most_common(20)
    return common, len(docs), len(media)

def generate_prompt(topics, file_stats, message_samples):
    prompt = f"""
    You are 'Consilium', the AI Creative Director of the 'Unified System'.
    
    **Objective:** Create a content plan for a video series (YouTube/Instagram/TikTok) based on the user's digital footprint.
    
    **Data Analysis:**
    - **Total Documents:** {file_stats[1]}
    - **Total Media Assets:** {file_stats[2]} (Footage available for B-roll)
    - **Top File Keywords:** {', '.join([t[0] for t in file_stats[0]])}
    
    **Recent Context (User Messages):**
    "{' ... '.join(message_samples[:10]).replace('\n', ' ')}"
    
    **Task:**
    1. Identify 3 main "Content Pillars" based on this data (e.g., Tech/Coding, Personal Archive/Memories, Gaming/Lifestyle).
    2. Suggest **5 specific video episode ideas** for the coming week.
    3. For each episode, write a catchy title and a 1-sentence hook.
    
    **Format:** Markdown. Be creative, bold, and energetic.
    """
    return prompt

def query_llm(prompt):
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }
    try:
        # Try local Ollama (via host.docker.internal if inside docker, or localhost if undefined)
        # Since we run this script on the HOST (igor-gaming-1), use localhost
        url = "http://localhost:11434/api/generate"
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return response.json().get('response', '')
        else:
            return f"Error from LLM: {response.text}"
    except Exception as e:
        return f"LLM Connection Failed: {e}"

def main():
    print("🧠 Consilium: Analyzing data footprint...")

    # 1. Analyze Files
    if not os.path.exists(INDEX_FILE):
        print("❌ Index not found. Run archive_indexer.py first.")
        return

    file_stats = analyze_index(INDEX_FILE)
    print(f"📊 Analyzed {file_stats[1]} docs and {file_stats[2]} media files.")

    # 2. Analyze Messages
    messages = get_recent_topics(DB_PATH)
    print(f"💬 Read {len(messages)} recent messages.")

    # 3. Generate
    print("💡 Designing content strategy...")
    prompt = generate_prompt(None, file_stats, messages)

    plan = query_llm(prompt)

    print("\n" + "="*40)
    print("🎬 CONSILIUM: CONTENT SERIES PLAN")
    print("="*40 + "\n")
    print(plan)

    # Save plan
    report_path = "/home/gonya/Unified_System_Core/Projects/Content_Factory/reports/series_plan_v1.md"
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, "w") as f:
        f.write(plan)
    print(f"\n✅ Plan saved to: {report_path}")

if __name__ == "__main__":
    main()
