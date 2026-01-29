from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import textwrap
import os
from datetime import datetime

# Setup content for 3 languages
CONTENT = {
    "RU": {
        "title": "Стратегия 2026: Суверенитет и Масштабирование",
        "subtitle": "Гибридная модель запуска стартапа (Делавэр-Израиль)",
        "slides": [
            {
                "title": "Глобальный Контекст 2026",
                "points": [
                    "Израиль: Deep-Tech лидерство, реформы для инвесторов.",
                    "США: Главный рынок масштабирования.",
                    "Россия: Технологический суверенитет и гранты."
                ]
            },
            {
                "title": "Гибридная Структура",
                "points": [
                    "США (Делавэр): C-Corp для венчурных инвестиций.",
                    "Израиль: R&D дочерняя компания (100%)",
                    "Преимущества: Доступ к грантам (Tnufa, SBIR) и талантам."
                ]
            },
            {
                "title": "Технология: Проект 'Вибраниум'",
                "points": [
                    "Отказ от облачной зависимости (Google/Apple).",
                    "Локальные LLM на собственном железе.",
                    "Агентная архитектура: Биллинг, SMM, Код."
                ]
            },
            {
                "title": "Тактика 2025-2026",
                "points": [
                    "Умный дом: Matter protokol.",
                    "Автоматизация: n8n (self-hosted).",
                    "Финансы: Агрегаторы активов."
                ]
            }
        ]
    },
    "EN": {
        "title": "Strategy 2026: Sovereignty & Scale",
        "subtitle": "Hybrid Startup Model (Delaware-Israel)",
        "slides": [
            {
                "title": "Global Context 2026",
                "points": [
                    "Israel: Deep-Tech leadership, investor reforms.",
                    "USA: Primary market for scaling.",
                    "Russia: Tech sovereignty & grants."
                ]
            },
            {
                "title": "Hybrid Structure",
                "points": [
                    "USA (Delaware): C-Corp for VC funding.",
                    "Israel: R&D subsidiary (100%).",
                    "Benefits: Access to grants (Tnufa, SBIR) & talent."
                ]
            },
            {
                "title": "Technology: Project 'Vibranium'",
                "points": [
                    "Zero dependency on Big Tech clouds.",
                    "Local LLMs on private hardware.",
                    "Agent Architecture: Billing, SMM, Code."
                ]
            },
            {
                "title": "Tactics 2025-2026",
                "points": [
                    "Smart Home: Matter protocol.",
                    "Automation: n8n (self-hosted).",
                    "Finance: Asset aggregators."
                ]
            }
        ]
    },
    "HE": {
        "title": "אסטרטגיה 2026: ריבונות וצמיחה",
        "subtitle": "מודל סטארט-אפ היברידי (דלאוור-ישראל)",
        "slides": [
            {
                "title": "הקשר גלובלי 2026",
                "points": [
                    "ישראל: מנהיגות Deep-Tech, רפורמות למשקיעים.",
                    "ארה\"ב: שוק מרכזי להרחבה.",
                    "רוסיה: ריבונות טכנולוגית ומענקים."
                ]
            },
            {
                "title": "מבנה היברידי",
                "points": [
                    "ארה\"ב (דלאוור): C-Corp לגיוס הון סיכון.",
                    "ישראל: חברת בת למחקר ופיתוח (100%).",
                    "יתרונות: גישה למענקים (תנופה, SBIR) וכישרונות."
                ]
            },
            {
                "title": "טכנולוגיה: פרויקט 'ויברניום'",
                "points": [
                    "אפס תלות בענני ביג טק.",
                    "מודלים מקומיים (LLM) על חומרה פרטית.",
                    "ארכיטקטורת סוכנים: בילינג, SMM, קוד."
                ]
            },
            {
                "title": "טקטיקה 2025-2026",
                "points": [
                    "בית חכם: פרוטוקול Matter.",
                    "אוטומציה: n8n (אירוח עצמי).",
                    "פיננסים: אגרגטורים של נכסים."
                ]
            }
        ]
    }
}

# Special handling for Hebrew (RTL)
import arabic_reshaper
from bidi.algorithm import get_display

def create_pdf(lang, filename):
    doc = SimpleDocTemplate(filename, pagesize=landscape(A4))
    styles = getSampleStyleSheet()
    
    # Register a font that supports Cyrillic and Hebrew if possible
    # For standard Mac, we might need a specific font path.
    # Using Helvetica as fallback, but ideally needs Unicode font.
    # Trying to find Arial or similar.
    
    font_path = "/System/Library/Fonts/Supplemental/Arial.ttf"
    if not os.path.exists(font_path):
        font_path = "/System/Library/Fonts/Helvetica.ttc" 
        
    try:
        pdfmetrics.registerFont(TTFont('Arial', font_path))
        font_name = 'Arial'
    except:
        font_name = 'Helvetica' # Fallback, might break HE/RU chars if not standard
    
    # Define styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontName=font_name,
        fontSize=24,
        spaceAfter=30,
        alignment=1 # Center
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontName=font_name,
        fontSize=14,
        leading=20,
        spaceAfter=10
    )

    story = []
    data = CONTENT[lang]

    # Title Page
    t = data['title']
    s = data['subtitle']
    
    if lang == "HE":
        t = get_display(arabic_reshaper.reshape(t))
        s = get_display(arabic_reshaper.reshape(s))
        
    story.append(Spacer(1, 100))
    story.append(Paragraph(t, title_style))
    story.append(Paragraph(s, body_style))
    story.append(PageBreak())
    
    # Slides
    for slide in data['slides']:
        st = slide['title']
        if lang == "HE":
            st = get_display(arabic_reshaper.reshape(st))
            
        story.append(Paragraph(st, title_style))
        story.append(Spacer(1, 20))
        
        for point in slide['points']:
            pt = f"• {point}"
            if lang == "HE":
                pt = get_display(arabic_reshaper.reshape(pt))
            story.append(Paragraph(pt, body_style))
            
        story.append(PageBreak())

    doc.build(story)
    print(f"Created {filename}")

# Generate 3 PDFs
desktop = os.path.expanduser("~/Desktop")
create_pdf("RU", os.path.join(desktop, "Strategy_2026_RU.pdf"))
create_pdf("EN", os.path.join(desktop, "Strategy_2026_EN.pdf"))
create_pdf("HE", os.path.join(desktop, "Strategy_2026_HE.pdf"))
