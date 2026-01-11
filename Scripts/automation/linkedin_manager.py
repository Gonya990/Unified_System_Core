#!/usr/bin/env python3
"""
LinkedIn Profile Manager - Автоматизация работы с LinkedIn профилем
Использует Playwright для браузерной автоматизации
"""

import asyncio
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# --- Configuration ---
LINKEDIN_PROFILE_URL = "https://www.linkedin.com/in/igor-goncharenko"
SESSION_FILE = Path(__file__).parent / ".linkedin_session.json"
PROFILE_DATA_FILE = Path(__file__).parent / "linkedin_profile_data.json"

# Profile data from RESUME_VARIANTS.md (Variant C - LinkedIn Optimized)
PROFILE_DATA = {
    "name": "Igor Goncharenko",
    "headline": "Supervisor | Project Coordinator | Systems Implementation",
    "about": """Experienced Supervisor with 7+ years in infrastructure, telecom, and high-rise construction projects. Currently leading elevator installation at BEYOND Tower – one of Israel's tallest buildings.

My strengths: Coordinating complex operations, managing teams under pressure, and ensuring quality delivery on tight schedules.

🔧 Key Skills: Project Coordination, Team Management, Field Supervision, Quality Control, Logistics, Safety Compliance

📍 Based in Israel | Open to new opportunities""",
    "location": "Israel",
    "current_position": {
        "title": "Supervisor / PM Assistant",
        "company": "Schindler",
        "description": "BEYOND Tower Project - Leading elevator installation in one of Israel's tallest buildings (+370m)",
        "start_date": "August 2023",
        "current": True
    },
    "experience": [
        {
            "title": "Supervisor / PM Assistant",
            "company": "Schindler",
            "location": "Israel",
            "start_date": "Aug 2023",
            "end_date": "Present",
            "description": """BEYOND Tower Project
• Lead field operations for smart elevator installation
• Coordinate 10+ subcontractors and technical teams
• Client and management interface
• Quality, safety, and manufacturer specs compliance"""
        },
        {
            "title": "Team Lead – Fiber Optics",
            "company": "URICOMS (Partner Communications)",
            "location": "Israel",
            "start_date": "2019",
            "end_date": "2023",
            "description": """• Led fiber optic network deployment (FTTx) across Central Israel
• Managed regional teams, schedules, and quality targets
• Complex troubleshooting at central offices and field sites"""
        },
        {
            "title": "Installation Technician",
            "company": "Vira & Assemblies Ltd",
            "location": "Israel",
            "start_date": "2020",
            "end_date": "2022",
            "description": """• Elevator installation and testing
• Work per test documentation and safety procedures"""
        }
    ],
    "skills": [
        "Project Coordination",
        "Team Management", 
        "Field Supervision",
        "Quality Control",
        "Logistics",
        "Safety Compliance",
        "Fiber Optics",
        "Elevator Systems",
        "Technical Documentation",
        "Subcontractor Management",
        "Scheduling & Reporting"
    ],
    "languages": [
        {"name": "Hebrew", "proficiency": "Professional working"},
        {"name": "Russian", "proficiency": "Native"},
        {"name": "Ukrainian", "proficiency": "Native"},
        {"name": "English", "proficiency": "Elementary"}
    ],
    "certifications": [
        "Driver's License B",
        "Forklift License (20T)",
        "Height Work Certified"
    ]
}


async def check_login_status(page):
    """Проверить залогинен ли пользователь"""
    try:
        await page.goto("https://www.linkedin.com/feed/", timeout=15000)
        await page.wait_for_load_state("networkidle", timeout=10000)
        
        # Check if we're on the feed (logged in) or login page
        if "/login" in page.url or "/authwall" in page.url:
            return False
        
        # Look for profile menu
        profile_menu = await page.query_selector('[data-control-name="nav.settings_signout"]')
        if profile_menu:
            return True
            
        # Alternative check - look for messaging icon
        messaging = await page.query_selector('[data-test-icon="nav-messages-icon"]')
        if messaging:
            return True
            
        return "feed" in page.url
    except Exception as e:
        print(f"Login check error: {e}")
        return False


async def manual_login(page):
    """Открыть страницу логина для ручного входа"""
    print("\n" + "="*60)
    print("🔐 ТРЕБУЕТСЯ ВХОД В LINKEDIN")
    print("="*60)
    print("\nОткрываю страницу входа в LinkedIn...")
    print("Пожалуйста, войдите вручную в браузере.")
    print("\n⚠️  После входа нажмите Enter в терминале для продолжения...")
    
    await page.goto("https://www.linkedin.com/login")
    
    # Wait for user to login manually
    input("\nНажмите Enter после успешного входа в LinkedIn...")
    
    # Verify login
    if await check_login_status(page):
        print("✅ Вход выполнен успешно!")
        return True
    else:
        print("❌ Вход не удался. Попробуйте снова.")
        return False


async def get_profile_info(page):
    """Получить текущую информацию профиля"""
    print("\n📊 Получение информации профиля...")
    
    await page.goto(LINKEDIN_PROFILE_URL, timeout=30000)
    await page.wait_for_load_state("networkidle", timeout=15000)
    
    profile_info = {}
    
    try:
        # Get name
        name_el = await page.query_selector('h1.text-heading-xlarge')
        if name_el:
            profile_info['name'] = await name_el.inner_text()
        
        # Get headline
        headline_el = await page.query_selector('div.text-body-medium')
        if headline_el:
            profile_info['headline'] = await headline_el.inner_text()
        
        # Get location
        location_el = await page.query_selector('span.text-body-small.inline')
        if location_el:
            profile_info['location'] = await location_el.inner_text()
        
        # Get connections count
        connections_el = await page.query_selector('[href*="/connections/"]')
        if connections_el:
            profile_info['connections'] = await connections_el.inner_text()
        
        # Get about section
        about_section = await page.query_selector('#about ~ div.display-flex span[aria-hidden="true"]')
        if about_section:
            profile_info['about'] = await about_section.inner_text()
            
    except Exception as e:
        print(f"Ошибка при получении данных: {e}")
    
    return profile_info


async def compare_profiles(current, target):
    """Сравнить текущий профиль с целевым"""
    print("\n" + "="*60)
    print("📋 СРАВНЕНИЕ ПРОФИЛЕЙ")
    print("="*60)
    
    differences = []
    
    if current.get('name') != target.get('name'):
        differences.append(('name', current.get('name'), target.get('name')))
    
    if current.get('headline') != target.get('headline'):
        differences.append(('headline', current.get('headline'), target.get('headline')))
    
    # About section comparison (partial match)
    current_about = current.get('about', '')
    target_about = target.get('about', '')
    if target_about and target_about[:50] not in current_about:
        differences.append(('about', current_about[:100] + '...', target_about[:100] + '...'))
    
    if differences:
        print("\n⚠️  Найдены различия:\n")
        for field, current_val, target_val in differences:
            print(f"  📌 {field.upper()}:")
            print(f"     Текущее:  {current_val}")
            print(f"     Целевое:  {target_val}")
            print()
    else:
        print("\n✅ Профиль соответствует целевым данным!")
    
    return differences


async def main():
    """Основная функция"""
    print("\n" + "="*60)
    print("🔗 LINKEDIN PROFILE MANAGER")
    print("="*60)
    print(f"\n📅 Дата: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"🔗 Профиль: {LINKEDIN_PROFILE_URL}")
    
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        print("\n❌ Playwright не установлен!")
        print("   Установите: pip install playwright && playwright install chromium")
        sys.exit(1)
    
    async with async_playwright() as p:
        # Launch browser (visible for manual login)
        browser = await p.chromium.launch(
            headless=False,
            args=['--start-maximized']
        )
        
        context = await browser.new_context(
            viewport={'width': 1280, 'height': 800},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        
        page = await context.new_page()
        
        # Check login status
        logged_in = await check_login_status(page)
        
        if not logged_in:
            success = await manual_login(page)
            if not success:
                await browser.close()
                return
        else:
            print("✅ Уже залогинены в LinkedIn")
        
        # Get current profile info
        current_profile = await get_profile_info(page)
        
        print("\n📊 Текущий профиль:")
        for key, value in current_profile.items():
            print(f"   {key}: {value[:50] if len(str(value)) > 50 else value}...")
        
        # Compare with target
        differences = await compare_profiles(current_profile, PROFILE_DATA)
        
        # Save profile data
        export_data = {
            "fetched_at": datetime.now().isoformat(),
            "url": LINKEDIN_PROFILE_URL,
            "current_profile": current_profile,
            "target_profile": {
                "name": PROFILE_DATA["name"],
                "headline": PROFILE_DATA["headline"],
                "about": PROFILE_DATA["about"][:200] + "..."
            },
            "differences_found": len(differences)
        }
        
        with open(PROFILE_DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Данные сохранены в: {PROFILE_DATA_FILE}")
        
        # Ask about next steps
        if differences:
            print("\n" + "="*60)
            print("📝 ДОСТУПНЫЕ ДЕЙСТВИЯ:")
            print("="*60)
            print("1. Обновить профиль вручную (откроется редактирование)")
            print("2. Экспортировать целевые данные в текстовый файл")
            print("3. Завершить")
            
            choice = input("\nВыберите действие (1/2/3): ").strip()
            
            if choice == "1":
                await page.goto(f"{LINKEDIN_PROFILE_URL}/edit/intro/")
                print("\n🔧 Открыта страница редактирования профиля")
                print("   Внесите изменения и сохраните в браузере")
                input("\nНажмите Enter после завершения редактирования...")
                
            elif choice == "2":
                export_file = Path(__file__).parent / "linkedin_update_text.txt"
                with open(export_file, 'w', encoding='utf-8') as f:
                    f.write("="*60 + "\n")
                    f.write("LINKEDIN PROFILE UPDATE DATA\n")
                    f.write("="*60 + "\n\n")
                    f.write(f"Name: {PROFILE_DATA['name']}\n\n")
                    f.write(f"Headline:\n{PROFILE_DATA['headline']}\n\n")
                    f.write(f"About:\n{PROFILE_DATA['about']}\n\n")
                    f.write("Skills:\n")
                    for skill in PROFILE_DATA['skills']:
                        f.write(f"  • {skill}\n")
                print(f"\n💾 Данные экспортированы в: {export_file}")
        
        print("\n✅ Готово!")
        
        # Keep browser open for review
        input("\nНажмите Enter для закрытия браузера...")
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
