
import html
import json
import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
INPUT_FILE = BASE_DIR / "Projects" / "AI_Core" / "src" / "emails_4_months.json"
OUTPUT_PDF = BASE_DIR / "Job_Vacancies_Jan_2026.pdf"

# Manual Web Search Results (Hardcoded for reliability)
WEB_RESULTS = [
    {
        "title": "General Recruitment - Construction & Infrastructure",
        "company": "Project Pro",
        "email": "info@projectpro.co.il",
        "description": "Leading recruitment company for infrastructure and construction in Israel. Send CV for potential Site Manager roles.",
        "relevance": "High"
    },
    {
        "title": "Construction Recruitment (North/Akko)",
        "company": "Cohen Employment Group",
        "email": "info@cohengroup.li",
        "description": "Licensed recruitment agency focused on construction, based in Akko (North).",
        "relevance": "High - Location & Field"
    },
    {
        "title": "Samsung Research Israel Careers",
        "company": "Samsung",
        "email": "sril.career@samsung.com",
        "description": "General recruitment email. Worth sending CV for any relevant technical operations/logistics roles.",
        "relevance": "Medium"
    },
    {
        "title": "Mobileye Recruitment",
        "company": "Mobileye",
        "email": "recruitment_mobileye@mobileye.com",
        "description": "General recruitment email. Look for Operations/Fleet management roles.",
        "relevance": "Medium"
    },
    {
        "title": "Nefesh B'Nefesh Employment",
        "company": "Nefesh B'Nefesh",
        "email": "employment@nbn.org.il",
        "description": "Contact for Olim-friendly job listings and guidance.",
        "relevance": "Medium"
    }
]




def clean_text(text):
    if not text:
        return ""
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    # Escape HTML characters for ReportLab
    return html.escape(text)

def clean_snippet(text):
    if not text:
        return ""
    # Remove HTML tags if present (simple regex)
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return html.escape(text)

def extract_email(text):
    match = re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', text)
    return match.group(0) if match else None

def extract_url(text):
    match = re.search(r'(https?://[^\s]+)', text)
    return match.group(0) if match else None

def create_pdf(jobs):
    doc = SimpleDocTemplate(str(OUTPUT_PDF), pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    styles = getSampleStyleSheet()

    # Custom Styles
    styles.add(ParagraphStyle(name='JobTitle', parent=styles['Heading2'], fontSize=12, spaceAfter=6, textColor=colors.darkblue))
    styles.add(ParagraphStyle(name='JobMeta', parent=styles['Normal'], fontSize=10, textColor=colors.gray))
    styles.add(ParagraphStyle(name='JobDesc', parent=styles['Normal'], fontSize=10, leading=14))
    styles.add(ParagraphStyle(name='Link', parent=styles['Normal'], fontSize=10, textColor=colors.blue))

    story = []

    # Title
    story.append(Paragraph("Job Vacancies & Contacts for Igor Goncharenko", styles['Heading1']))
    story.append(Paragraph("Generated on Jan 6, 2026", styles['Normal']))
    story.append(Spacer(1, 24))

    # SECTION 1: Direct Email Contacts (Web)
    story.append(Paragraph("SECTION 1: Direct Email Contacts (Recommended)", styles['Heading2']))
    story.append(Paragraph("These are direct contacts for recruitment agencies and companies in your field.", styles['Normal']))
    story.append(Spacer(1, 12))

    for item in WEB_RESULTS:
        story.append(Paragraph(f"<b>{item['title']}</b> at {item['company']}", styles['JobTitle']))
        story.append(Paragraph(f"<b>Email:</b> <a href='mailto:{item['email']}'>{item['email']}</a>", styles['Link']))
        story.append(Paragraph(f"<i>Why fits:</i> {item['description']}", styles['JobDesc']))
        story.append(Spacer(1, 12))

    # SECTION 2: From Your Email Inbox (Last 4 Months)
    story.append(Spacer(1, 12))
    story.append(Paragraph("SECTION 2: Leads from Your Inbox (Last 4 Months)", styles['Heading2']))
    story.append(Paragraph("Relevant job alerts found in your Gmail.", styles['Normal']))
    story.append(Spacer(1, 12))

    if not jobs:
        story.append(Paragraph("No direct hiring emails found in the scanned batch.", styles['Normal']))

    for job in jobs:
        title = clean_text(job.get('subject', 'Job Opportunity'))
        sender = clean_text(job.get('sender', 'Unknown'))

        # Use content for snippet but careful with length and escaping
        content_raw = job.get('content', '')
        snippet = clean_snippet(content_raw)[:300] + "..."

        # Try to find a link or email in the RAW content before escaping
        email_contact = extract_email(content_raw)
        link_contact = extract_url(content_raw)

        story.append(Paragraph(f"<b>{title}</b>", styles['JobTitle']))
        story.append(Paragraph(f"From: {sender} | Date: {job.get('date', '')}", styles['JobMeta']))
        story.append(Paragraph(snippet, styles['JobDesc']))

        if email_contact:
            # Re-escape specifically for the display link if needed, but simple strings are safer
            story.append(Paragraph(f"<b>Contact Email:</b> <a href='mailto:{email_contact}'>{email_contact}</a>", styles['Link']))
        elif link_contact:
            # Escape the link for display but keep href valid
            safe_link = html.escape(link_contact)
            story.append(Paragraph(f"<b>Apply Link:</b> <a href='{safe_link}'>{safe_link}</a>", styles['Link']))

        story.append(Spacer(1, 12))

    doc.build(story)
    print(f"PDF generated: {OUTPUT_PDF}")

def main():
    if not INPUT_FILE.exists():
        print("Input file not found. Running with web results only.")
        create_pdf([])
        return

    with open(INPUT_FILE, encoding='utf-8') as f:
        emails = json.load(f)

    # Filter emails
    relevant_jobs = []
    seen_ids = set()

    keywords = ["operations", "manager", "site", "supervisor", "project", "logistics", "warehouse", "מנהל", "תפעול"]

    for email in emails:
        if email['id'] in seen_ids:
            continue
        seen_ids.add(email['id'])

        content = (email['subject'] + " " + email['content']).lower()

        # Must have at least one keyword
        if any(k in content for k in keywords):
            # Prioritize if email address found in body (rare for automated alerts, but good for direct comms)
            score = 0
            if "@" in email['content']:
                score += 2
            if "north" in content or "haifa" in content or "צפון" in content or "חיפה" in content:
                score += 1

            # Simple struct
            email['score'] = score
            relevant_jobs.append(email)

    # Sort
    relevant_jobs.sort(key=lambda x: x.get('score', 0), reverse=True)

    # Take top 15 unique
    unique_jobs = []
    seen_subjects = set()
    for j in relevant_jobs:
        subj_clean = j['subject'].lower().strip()
        if subj_clean not in seen_subjects:
            unique_jobs.append(j)
            seen_subjects.add(subj_clean)
        if len(unique_jobs) >= 15:
            break

    create_pdf(unique_jobs)

if __name__ == "__main__":
    main()
