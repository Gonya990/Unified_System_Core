
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import html
import re

# Paths
OUTPUT_PDF = "/Users/macbook/Desktop/Resumes_Igor/Прямые_Контакты_Работодателей_Расширенный.pdf"
FONT_PATH = "/System/Library/Fonts/Supplemental/Arial.ttf"

# Job Data (Verified & Expanded)
JOBS = [
    # --- DIRECT EMPLOYERS (Technology / Operations) ---
    {
        "company": "Schindler Israel",
        "vacancy": "Operations / Project Manager / Technical Supervisor",
        "contact_type": "Direct Email",
        "location": "North / Center",
        "contact": "jobs.il@schindler.com", # High confidence
        "note": "Прямой HR. Идеально по профилю (лифты/эскалаторы). Укажите опыт управления."
    },
    {
        "company": "INSIGHTEC",
        "vacancy": "Warehouse Manager / Logistics",
        "contact_type": "Careers Page",
        "location": "Haifa (Tirat Carmel)",
        "contact": "https://www.insightec.com/careers/",
        "note": "Медицинские технологии. Офис в Тират Кармель. Нужен опыт склада."
    },
    {
        "company": "Utron",
        "vacancy": "Site Manager / Installation Manager",
        "contact_type": "HR Form / LinkedIn",
        "location": "Israel (Projects based)",
        "contact": "https://www.utron.com/contact-us/",
        "note": "Автоматические парковки. Очень релевантно опыту монтажа/механики. Писать через 'Contact Us'."
    },
    {
        "company": "Fives Intralogistics",
        "vacancy": "Deployment Manager / Site Supervisor",
        "contact_type": "LinkedIn / Corporate",
        "location": "North (Binyamina/Caesarea)",
        "contact": "https://www.fivesgroup.com/careers", 
        "note": "Логистическая автоматизация. Искать через карьеру или LinkedIn рекрутеров."
    },
    {
        "company": "Airwayz",
        "vacancy": "Operations Director / Manager",
        "contact_type": "Direct Email",
        "location": "Tel Aviv / Hybrid",
        "contact": "contact@airwayz.co", # Verified
        "note": "Дроны/Управление трафиком. Высокая позиция, но можно пробовать."
    },
    {
        "company": "Galilee Culinary Institute (GCI)",
        "vacancy": "Manager of Operations",
        "contact_type": "Direct Apply",
        "location": "North (Kibbutz Gonen)",
        "contact": "https://www.jpro.org/jobs/manager-of-operations-at-galilee-culinary-institute-2/", # Found in search
        "note": "Управление объектом в Кибуц Гонен (Север). Логистика, обслуживание, закупки."
    },

    # --- RECRUITMENT AGENCIES (Construction / Infrastructure) ---
    {
        "company": "Project Pro",
        "vacancy": "Construction / Project Managers",
        "contact_type": "Recruiter Email",
        "location": "Nationwide",
        "contact": "info@projectpro.co.il", # Verified
        "note": "Агентство №1 по стройке/инфраструктуре. Отправлять смело."
    },
    {
        "company": "Cohen Employment Group",
        "vacancy": "Construction Management",
        "contact_type": "Recruiter Email",
        "location": "North (Akko)",
        "contact": "info@cohengroup.li", # Verified
        "note": "Базируются в Акко. Специализация на стройке."
    },
    {
        "company": "Nisha Group (Cleantech/Bio)",
        "vacancy": "Operations & Logistics Roles",
        "contact_type": "Recruiter Email",
        "location": "North / Center",
        "contact": "cv@nisha.co.il", # General CV inbox
        "note": "Крупное агентство. У них много клиентов на Севере (промзоны Хайфа/Йокнеам)."
    },
    
    # --- JOB BOARDS (Actionable Links) ---
    {
        "company": "AllJobs (North Operations)",
        "vacancy": "מנהל תפעול צפון (Список вакансий)",
        "contact_type": "Job Board Search",
        "location": "North",
        "contact": "https://www.alljobs.co.il/SearchResultsGuest.aspx?page=1&position=1086&region=3&type=&freetxt=",
        "note": "Прямая ссылка на поиск 'Менеджер по операциям' на Севере. Обновляется ежедневно."
    },
    {
        "company": "Drushim (Work Manager)",
        "vacancy": "מנהל עבודה דרושים צפון (Список вакансий)",
        "contact_type": "Job Board Search",
        "location": "North",
        "contact": "https://www.drushim.co.il/jobs/search/%D7%9E%D7%A0%D7%94%D7%9C-%D7%A2%D7%91%D7%95%D7%93%D7%94/?area=3",
        "note": "Прямая ссылка на вакансии 'Прораб/Менеджер работ' на Севере."
    },
    {
        "company": "Nefesh B'Nefesh Job Board",
        "vacancy": "Jobs in the North",
        "contact_type": "Job Board",
        "location": "North",
        "contact": "https://www.nbn.org.il/life-in-israel/employment/job-board/?_job_region=north",
        "note": "Доска вакансий для репатриантов. Фильтр 'North' уже включен."
    }
]

def create_pdf():
    try:
        pdfmetrics.registerFont(TTFont('Arial', FONT_PATH))
        font_name = 'Arial'
    except:
        font_name = 'Helvetica'

    doc = SimpleDocTemplate(OUTPUT_PDF, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    styles = getSampleStyleSheet()
    
    # Custom Styles
    style_title = ParagraphStyle(name='Title', parent=styles['Heading1'], fontName=font_name, fontSize=18, spaceAfter=20, textColor=colors.darkblue)
    style_h2 = ParagraphStyle(name='H2', parent=styles['Heading2'], fontName=font_name, fontSize=14, spaceBefore=10, textColor=colors.black)
    style_normal = ParagraphStyle(name='Normal', parent=styles['Normal'], fontName=font_name, fontSize=11, leading=14)
    style_link = ParagraphStyle(name='Link', parent=styles['Normal'], fontName=font_name, fontSize=11, textColor=colors.blue)

    story = []

    # Header
    story.append(Paragraph("Варианты Трудоустройства: Прямые Контакты и Вакансии", style_title))
    story.append(Paragraph("Специально для Игоря Гончаренко (Operations / Site Manager / Technical)", style_normal))
    story.append(Spacer(1, 24))

    # Iterate categories (Implicitly by order in JOBS list for now, or grouped)
    # Let's just list them nicely
    
    for job in JOBS:
        # Title: Company - Vacancy
        header_text = f"<b>{job['company']}</b> - {job['vacancy']}"
        story.append(Paragraph(header_text, style_h2))
        
        # Details
        story.append(Paragraph(f"📍 <b>Локация:</b> {job['location']}", style_normal))
        
        # Contact Link
        contact = job['contact']
        if "@" in contact and "http" not in contact:
            link_html = f"<a href='mailto:{contact}'>{contact}</a>"
            story.append(Paragraph(f"📧 <b>Отправить резюме:</b> {link_html}", style_link))
        else:
            link_html = f"<a href='{contact}'>Перейти к вакансии / контактам</a>"
            story.append(Paragraph(f"🔗 <b>Ссылка:</b> {link_html}", style_link))
            # Also show text URL for copy-paste if needed, or keep clean
            story.append(Paragraph(f"<font size=9 color=grey>{contact}</font>", style_normal))

        # Note
        story.append(Paragraph(f"💡 <i>{job['note']}</i>", style_normal))
        
        story.append(Spacer(1, 12))
        story.append(Paragraph("<hr/>", style_normal))

    doc.build(story)
    print(f"PDF generated: {OUTPUT_PDF}")

if __name__ == "__main__":
    create_pdf()
