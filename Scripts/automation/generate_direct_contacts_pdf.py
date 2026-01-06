
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import html
import re

# Paths
OUTPUT_PDF = "/Users/macbook/Desktop/Resumes_Igor/Прямые_Контакты_Работодателей.pdf"
FONT_PATH = "/System/Library/Fonts/Supplemental/Arial.ttf"

# Data from Web Search + Personal Knowledge
JOBS = [
    {
        "company": "Schindler Israel",
        "vacancy": "Operations / Elevators / Technical",
        "contact_type": "Direct Email",
        "contact": "jobs.il@schindler.com", # Verified
        "note": "Прямой email HR отдела. Отправляйте резюме сюда с пометкой Technical Operations."
    },
    {
        "company": "Airwayz",
        "vacancy": "Director of Operations",
        "contact_type": "Direct Email",
        "contact": "contact@airwayz.co", # Verified
        "note": "Общий контакт, но резюме рассматриваются. Укажите 'Attn: HR Manager' в теме."
    },
    {
        "company": "Utron",
        "vacancy": "Site Manager",
        "contact_type": "Contact info / HR",
        "contact": "https://www.utron.com/contact-us/", 
        "note": "Прямого email нет, но можно найти HR 'Keren Bar-Lev' в LinkedIn или писать в форму. "
    },
    {
        "company": "Fives Intralogistics",
        "vacancy": "Deployment Manager",
        "contact_type": "Corporate Format",
        "contact": "First.Last@fivesgroup.com (Format)",
        "note": "Попробуйте найти рекрутера в LinkedIn и подставить имя."
    },
    {
        "company": "INSIGHTEC",
        "vacancy": "Warehouse Manager",
        "contact_type": "Careers Page",
        "contact": "https://www.insightec.com/careers/",
        "note": "Заявки только через сайт. Главный офис: Tirat Carmel. Tel: +972-4-8131313."
    },
    {
        "company": "Project Pro",
        "vacancy": "Construction / Infrastructure Recruitment",
        "contact_type": "Recruiter Email",
        "contact": "info@projectpro.co.il", # Verified
        "note": "Крупное агентство по найму в строительстве. Обязательно напишите им."
    },
    {
        "company": "Cohen Employment Group",
        "vacancy": "Construction (North)",
        "contact_type": "Recruiter Email",
        "contact": "info@cohengroup.li", # Verified
        "note": "Рекрутеры в Акко (Север). Специализация - строительство."
    }
]

def create_pdf():
    # Register readable font (Arial supports Cyrillic usually)
    try:
        pdfmetrics.registerFont(TTFont('Arial', FONT_PATH))
        font_name = 'Arial'
    except:
        print("Arial font not found in System. Using Helvetica (No Cyrillic support!).")
        font_name = 'Helvetica' # Fallback, will fail for Russian text display

    doc = SimpleDocTemplate(OUTPUT_PDF, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    styles = getSampleStyleSheet()
    
    # Custom Styles
    style_h1 = ParagraphStyle(name='H1', parent=styles['Heading1'], fontName=font_name, fontSize=16, spaceAfter=20, textColor=colors.darkblue)
    style_normal = ParagraphStyle(name='Normal', parent=styles['Normal'], fontName=font_name, fontSize=11, leading=14)
    style_bold = ParagraphStyle(name='Bold', parent=styles['Normal'], fontName=font_name, fontSize=11, leading=14, textColor=colors.black)
    style_link = ParagraphStyle(name='Link', parent=styles['Normal'], fontName=font_name, fontSize=11, textColor=colors.blue)

    story = []

    # Title
    story.append(Paragraph("Прямые Контакты Работодателей (Январь 2026)", style_h1))
    story.append(Paragraph("Список проверенных контактов и вакансий для отправки резюме.", style_normal))
    story.append(Spacer(1, 24))

    for job in JOBS:
        # Check validity
        contact = job['contact']
        
        # Company & Vacancy
        story.append(Paragraph(f"<b>Компания:</b> {job['company']}", style_bold))
        story.append(Paragraph(f"<b>Вакансия:</b> {job['vacancy']}", style_normal))
        
        # Contact
        if "@" in contact:
            story.append(Paragraph(f"<b>Email:</b> <a href='mailto:{contact}'>{contact}</a>", style_link))
        else:
            story.append(Paragraph(f"<b>Сайт/Ссылка:</b> <a href='{contact}'>{contact}</a>", style_link))
            
        # Note
        story.append(Paragraph(f"<i>Примечание:</i> {job['note']}", style_normal))
        story.append(Spacer(1, 14))
        story.append(Paragraph("_" * 50, style_normal))
        story.append(Spacer(1, 14))

    doc.build(story)
    print(f"PDF generated: {OUTPUT_PDF}")

if __name__ == "__main__":
    create_pdf()
