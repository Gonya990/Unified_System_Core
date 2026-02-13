#!/usr/bin/env python3
"""
LinkedIn Profile Updater v2 - Работает с современной версткой LinkedIn
Использует session cookie для авторизации
"""

import asyncio
import sys
from datetime import datetime

# LinkedIn session cookie (li_at)
LI_AT_COOKIE = "AQJpi9etRrX6vgAAAZusywM_gicM8MmWPBMrKPdOXKJh6FzfrGlXPbRiausF6opnzPYUwjPyouFVyGX1I52uVxEHjiH3hajF541GV7uaYPrgZSdG4VmpWtBG4W0TuGnmeBktwtmKzPn-sgi7dXeh0E7w6pqHq90qH5KFaYJHxLZRMCiSV0QhgbsgCzUx34BqpdELABUOMyhJ-grMoNTX9BQvFAsTxGEXWSf-F6EeD8HVIwwSBSJFuM2O9B0bbMW-i3oHDgTUczI-FHw_VJJ20dQgR_7doZJ2wdhACv8s8_d19seCFR58UY0RVXzCksFbou2fhholx9YEAjdz0cxG8N3LbM86ExdjEPY9_8x6EMQKJWFPYQ"

# Profile data
NEW_HEADLINE = "Supervisor | Project Coordinator | Systems Implementation"
NEW_ABOUT = """Experienced Supervisor with 7+ years in infrastructure, telecom, and high-rise construction projects. Currently leading elevator installation at BEYOND Tower – one of Israel's tallest buildings.

My strengths: Coordinating complex operations, managing teams under pressure, and ensuring quality delivery on tight schedules.

🔧 Key Skills: Project Coordination, Team Management, Field Supervision, Quality Control, Logistics, Safety Compliance

📍 Based in Israel | Open to new opportunities"""

PROFILE_URL = "https://www.linkedin.com/in/igor-goncharenko"


async def main():
    print("\n" + "=" * 60)
    print("🔗 LINKEDIN PROFILE UPDATER v2")
    print("=" * 60)
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    try:
        from playwright.async_api import async_playwright
    except ImportError:
        print("❌ Playwright не установлен!")
        sys.exit(1)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=300)

        context = await browser.new_context(viewport={"width": 1400, "height": 900})

        # Set LinkedIn session cookie
        print("\n🍪 Устанавливаю session cookie...")
        await context.add_cookies(
            [
                {
                    "name": "li_at",
                    "value": LI_AT_COOKIE,
                    "domain": ".linkedin.com",
                    "path": "/",
                    "httpOnly": True,
                    "secure": True,
                }
            ]
        )

        page = await context.new_page()

        # Go to profile
        print("\n📍 Открываю профиль...")
        await page.goto(PROFILE_URL, timeout=30000)
        await asyncio.sleep(3)

        # Check if logged in
        if "/login" in page.url or "/authwall" in page.url:
            print("❌ Cookie недействительный или истёк")
            print("   Нужен свежий li_at cookie")
            await browser.close()
            return

        print("✅ Авторизация успешна!")

        # Find and click edit button on intro section
        print("\n📍 Ищу кнопку редактирования...")

        # LinkedIn uses pencil icon for edit
        edit_buttons = await page.query_selector_all('button[aria-label*="Edit"], button svg[data-icon="pencil"]')
        print(f"   Найдено кнопок редактирования: {len(edit_buttons)}")

        # Try to find the intro edit button (usually first one)
        try:
            # Look for edit intro section specifically
            intro_edit = await page.wait_for_selector(
                '[data-view-name="profile-card"] button[aria-label*="Edit intro"]', timeout=5000
            )
            if intro_edit:
                await intro_edit.click()
                print("   ✅ Нажата кнопка редактирования intro")
                await asyncio.sleep(2)
        except Exception:
            # Alternative: look for first pencil button
            try:
                first_edit = await page.query_selector(
                    'button[class*="profile-topcard"] svg, section button[aria-label*="Edit"]'
                )
                if first_edit:
                    await first_edit.click()
                    await asyncio.sleep(2)
            except Exception:
                print("   ⚠️ Не могу найти кнопку редактирования")

        # Now try to find headline field in modal
        print("\n📍 Ищу поле Headline в модальном окне...")

        # Wait for modal
        await asyncio.sleep(2)

        # Try different selectors for headline
        headline_selectors = [
            'input[id*="headline"]',
            'input[name*="headline"]',
            '[aria-label*="Headline"] input',
            'input[placeholder*="headline"]',
            'form input[type="text"]',
        ]

        headline_found = False
        for selector in headline_selectors:
            try:
                el = await page.wait_for_selector(selector, timeout=3000)
                if el:
                    # Found it!
                    current_value = await el.input_value()
                    print(f"   Текущий headline: {current_value[:50] if current_value else '(пусто)'}...")

                    # Clear and type new
                    await el.click()
                    await el.fill("")
                    await el.type(NEW_HEADLINE, delay=50)
                    print(f"   ✅ Новый headline: {NEW_HEADLINE}")
                    headline_found = True
                    break
            except Exception:
                continue

        if not headline_found:
            print("   ⚠️ Поле headline не найдено")
            print("   LinkedIn мог изменить структуру страницы")

        # Take screenshot for debugging
        screenshot_path = "/Users/macbook/Documents/Unified_System/Scripts/automation/linkedin_screenshot.png"
        await page.screenshot(path=screenshot_path)
        print(f"\n📸 Скриншот сохранён: {screenshot_path}")

        # Save if possible
        try:
            save_btn = await page.query_selector('button:has-text("Save"), button[type="submit"]')
            if save_btn:
                await save_btn.click()
                print("✅ Изменения сохранены!")
                await asyncio.sleep(2)
        except Exception:
            pass

        print("\n" + "=" * 60)
        print("📋 РЕЗУЛЬТАТ")
        print("=" * 60)
        print(f"\nПрофиль: {PROFILE_URL}")
        print(f"Скриншот: {screenshot_path}")
        print("\n🔍 Проверьте браузер и скриншот")
        print("   Если изменения не применились - обновите вручную")
        print("\n   Данные для обновления:")
        print(f"   Headline: {NEW_HEADLINE}")

        input("\nНажмите Enter для закрытия браузера...")
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
