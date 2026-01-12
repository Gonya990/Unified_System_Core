

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

# Paths
OUTPUT_PDF = "/Users/macbook/Desktop/Resumes_Igor/Прямые_Контакты_Работодателей_Расширенный_Финальный.pdf"
FONT_PATH = "/System/Library/Fonts/Supplemental/Arial.ttf"

# Job Data (Verified & Expanded)
JOBS = [
    # --- DIRECT EMPLOYERS (Technology / Operations / Management) ---
    {
        "company": "Fives Intralogistics",
        "vacancy": "Deployment Manager / Site Supervisor",
        "contact_type": "LinkedIn Recruiter / Careers",
        "location": "North (Binyamina/Caesarea/Haifa)",
        "contact": "https://www.fivesgroup.com/careers",
        "note": "Автоматизация складов. Ищите рекрутеров Fives в LinkedIn, пишите напрямую."
    },
    {
        "company": "Utron",
        "vacancy": "Site Manager / Installation Manager",
        "contact_type": "HR Form / LinkedIn",
        "location": "Israel (Project based)",
        "contact": "https://www.utron.com/contact-us/",
        "note": "Роботизированные парковки. Релевантно опыту монтажа/механики."
    },
    {
        "company": "INSIGHTEC",
        "vacancy": "Warehouse / Logistics Manager",
        "contact_type": "Careers Page",
        "location": "Haifa (Tirat Carmel)",
        "contact": "https://www.insightec.com/careers/",
        "note": "Медицинские технологии. Офис в Тират Кармель. Нужен опыт склада."
    },
    {
        "company": "Mobileye",
        "vacancy": "Technical Project Manager (North/Center)",
        "contact_type": "Careers Page",
        "location": "Jerusalem / Petah Tikva / Haifa (R&D)",
        "contact": "https://careers.mobileye.com/",
        "note": "Есть позиции по интеграции железа и софта. Пробуйте 'Integration Specialist' или 'Project Manager'."
    },
    {
        "company": "Wolt (Operations)",
        "vacancy": "Operations Manager / City Manager",
        "contact_type": "Direct Apply",
        "location": "Haifa / North",
        "contact": "https://wolt.com/en/jobs/posting/",
        "note": "Ищут операционных менеджеров в Хайфе. Динамичная работа, авто + телефон."
    },
    {
        "company": "Galilee Culinary Institute (GCI)",
        "vacancy": "Manager of Operations",
        "contact_type": "Direct Apply",
        "location": "North (Kibbutz Gonen)",
        "contact": "https://www.jpro.org/jobs/manager-of-operations-at-galilee-culinary-institute-2/",
        "note": "Полное управление объектом в Кибуц Гонен. Логистика, закупки, обслуживание."
    },


    # --- RECRUITMENT AGENCIES (Specialized) ---
    {
        "company": "Project Pro",
        "vacancy": "Construction / Infrastructure Project Managers",
        "contact_type": "Direct Recruiter Email",
        "location": "Nationwide",
        "contact": "info@projectpro.co.il",
        "note": "Лидеры в инфраструктуре. Отправлять резюме с пометкой 'Experienced Site Manager'."
    },
    {
        "company": "Nisha Group (Cleantech/Bio)",
        "vacancy": "Operations & Logistics Roles",
        "contact_type": "Recruiter Email",
        "location": "North / Center",
        "contact": "cv@nisha.co.il",
        "note": "Работают с заводами в Йокнеаме и Хайфе. Писать: 'Looking for Ops Manager role in North'."
    },
    {
        "company": "Cohen Employment Group",
        "vacancy": "Construction Management",
        "contact_type": "Recruiter Email",
        "location": "North (Akko)",
        "contact": "info@cohengroup.li",
        "note": "Базируются в Акко. Стройка и управление персоналом."
    },

    # --- JOB BOARDS (Pre-filtered Links) ---
    {
        "company": "AllJobs (North Operations)",
        "vacancy": "מנהל תפעול צפון (Список вакансий)",
        "contact_type": "Job Board Search",
        "location": "North",
        "contact": "https://www.alljobs.co.il/SearchResultsGuest.aspx?page=1&position=1086&region=3&type=&freetxt=",
        "note": "Все вакансии 'Менеджер по операциям' на Севере. Обновляется ежедневно."
    },
    {
        "company": "Drushim (Work Manager)",
        "vacancy": "מנהל עבודה דרושים צפון (Список вакансий)",
        "contact_type": "Job Board Search",
        "location": "North",
        "contact": "https://www.drushim.co.il/jobs/search/%D7%9E%D7%A0%D7%94%D7%9C-%D7%A2%D7%91%D7%95%D7%93%D7%94/?area=3",
        "note": "Все вакансии 'Прораб/Менеджер работ' на Севере."
    },
    {
        "company": "Nefesh B'Nefesh Job Board",
        "vacancy": "Jobs in the North",
        "contact_type": "Job Board",
        "location": "North",
        "contact": "https://www.nbn.org.il/life-in-israel/employment/job-board/?_job_region=north",
        "note": "Доска вакансий для репатриантов. Английский язык. Фильтр 'North' включен."
    }
]

def create_pdf():
    try:
        pdfmetrics.registerFont(TTFont('Arial', FONT_PATH))
        font_name = 'Arial'
    except Exception:
        font_name = 'Helvetica'

    doc = SimpleDocTemplate(OUTPUT_PDF, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=18)
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

    # Introduction
    story.append(Paragraph("Ниже представлен список компаний и агентств для отправки резюме. Акцент сделан на позиции Operational/Site Manager на Севере Израиля и в крупных технологических компаниях.", style_normal))
    story.append(Spacer(1, 12))

    for job in JOBS:
        # Title: Company - Vacancy
        header_text = f"<b>{job['company']}</b> - {job['vacancy']}"
        story.append(Paragraph(header_text, style_h2))

        # Details
        story.append(Paragraph(f"📍 <b>Локация:</b> {job['location']}", style_normal))

        # Contact Link
        contact = job['contact']
        if "@" in contact and "http" not in contact:
            link_html = f"<a href='mailto:{contact}'>📧 Отправить резюме: {contact}</a>"
            story.append(Paragraph(link_html, style_link))
        else:
            link_html = f"<a href='{contact}'>🔗 Перейти к вакансии / контактам</a>"
            story.append(Paragraph(link_html, style_link))
            story.append(Paragraph(f"<font size=9 color=grey>{contact}</font>", style_normal))

        # Note
        story.append(Paragraph(f"💡 <i>{job['note']}</i>", style_normal))

        story.append(Spacer(1, 12))
        story.append(Paragraph("<hr/>", style_normal))

    doc.build(story)
    print(f"PDF generated: {OUTPUT_PDF}")

if __name__ == "__main__":
    create_pdf()
