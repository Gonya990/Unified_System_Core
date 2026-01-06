
import json
import re
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
INPUT_FILE = BASE_DIR / "Projects" / "AI_Core" / "src" / "latest_emails.json"

# Resume Keywords (from My_Resume.md)
KEYWORDS = [
    "Operations", "Manager", "Project", "Site", "Warehouse", "Logistics", "Technical", "Supervisor", "Integrator",
    "תפעול", "פרויקטים", "מנהל", "מחסן", "לוגיסטיקה", "טכני", "אחזקה", "בינוי", "תשתיות", "שטח", "מפקח"
]

# Negative Keywords (Higher Education strict requirements usually mentioned in snippets might be hard to detect, 
# but we can look for "Degree required" if confident. For now, rely on positive matching).
# However, user said "so I don't need higher education".
# We will prioritize roles that look like "Operations", "Site Manager", "Technical" over "R&D Manager" or "Software Engineer".

def clean_text(text):
    return text.replace("\r", " ").replace("\n", " ").strip()

def extract_url(text):
    # Regex to find links
    url_pattern = r'https?://[^\s<>"]+|www\.[^\s<>"]+'
    matches = re.findall(url_pattern, text)
    if matches:
        return matches[0]
    return None

def analyze_emails():
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        emails = json.load(f)

    job_emails = []

    for email in emails:
        sender = email.get('sender', '').lower()
        subject = email.get('subject', '').lower()
        snippet = email.get('content_preview', '')
        
        # 1. Identify Job Emails
        is_job_email = False
        if any(s in sender for s in ['linkedin', 'alljobs', 'taasuka', 'job', 'career', 'drushim', 'glassdoor']):
            is_job_email = True
        elif any(k in subject for k in ['vacancy', 'job', 'hiring', 'opportunity', 'משרה', 'דרוש', 'גיוס']):
            is_job_email = True
            
        if not is_job_email:
            continue

        # 2. Score Relevance based on Resume Keywords
        score = 0
        combined_text = (subject + " " + snippet).lower()
        
        for kw in KEYWORDS:
            if kw.lower() in combined_text:
                score += 1
        
        # Boost for location "North" or "Haifa" or "Krayot"
        if any(loc in combined_text for loc in ['haifa', 'north', 'krayot', 'akko', 'nahariya', 'carmiel', 'חיפה', 'צפון', 'קריות', 'עכו', 'נהריה', 'כרמיאל']):
            score += 2
            
        # 3. Filter Low Relevance
        if score > 0:
            link = extract_url(snippet)
            job_emails.append({
                'id': email['id'],
                'date': email['date'],
                'sender': email['sender'],
                'subject': email['subject'],
                'score': score,
                'snippet': snippet[:300], # Short preview
                'link': link
            })

    # Sort by score descending
    job_emails.sort(key=lambda x: x['score'], reverse=True)
    
    # Print candidates
    print(f"Found {len(job_emails)} potentially relevant job emails.")
    print("-" * 60)
    for i, job in enumerate(job_emails[:20]): # Top 20
        print(f"{i+1}. [{job['score']} pts] {job['subject']}")
        print(f"   From: {job['sender']}")
        print(f"   Date: {job['date']}")
        print(f"   Link: {job['link']}")
        print(f"   Snippet: {clean_text(job['snippet'])}...")
        print("-" * 60)

if __name__ == "__main__":
    analyze_emails()
