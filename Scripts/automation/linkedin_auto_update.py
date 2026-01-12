#!/usr/bin/env python3
"""
LinkedIn Auto-Updater - Автоматическое обновление профиля LinkedIn
"""

import asyncio
import sys
from datetime import datetime

# Data to update
NEW_HEADLINE = "Supervisor | Project Coordinator | Systems Implementation"
NEW_ABOUT = """Experienced Supervisor with 7+ years in infrastructure, telecom, and high-rise construction projects. Currently leading elevator installation at BEYOND Tower – one of Israel's tallest buildings.

My strengths: Coordinating complex operations, managing teams under pressure, and ensuring quality delivery on tight schedules.

🔧 Key Skills: Project Coordination, Team Management, Field Supervision, Quality Control, Logistics, Safety Compliance

📍 Based in Israel | Open to new opportunities"""

PROFILE_URL = "https://www.linkedin.com/in/igor-goncharenko"


async def main():
    print("\n" + "="*60)
    print("🔗 LINKEDIN AUTO-UPDATER")
    print("="*60)
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    try:
        from playwright.async_api import async_playwright
    except ImportError:
        print("❌ Playwright не установлен!")
        sys.exit(1)

    async with async_playwright() as p:
        # Launch visible browser
        browser = await p.chromium.launch(
            headless=False,
            slow_mo=500  # Slow down for visibility
        )

        context = await browser.new_context(
            viewport={'width': 1400, 'height': 900}
        )

        page = await context.new_page()

        # Step 1: Go to LinkedIn
        print("\n📍 Шаг 1: Открываю LinkedIn...")
        await page.goto("https://www.linkedin.com/feed/", timeout=30000)
        await asyncio.sleep(2)

        # Check if logged in
        if "/login" in page.url or "/authwall" in page.url:
            print("\n🔐 Требуется вход в LinkedIn!")
            print("   Войдите в браузере и нажмите Enter...")
            await page.goto("https://www.linkedin.com/login")
            input("\n>>> Нажмите Enter после входа: ")

        print("✅ Вход выполнен!")

        # Step 2: Go to profile edit
        print("\n📍 Шаг 2: Открываю редактирование профиля...")
        await page.goto(f"{PROFILE_URL}/edit/intro/", timeout=30000)
        await asyncio.sleep(3)

        # Step 3: Update headline
        print("\n📍 Шаг 3: Обновляю Headline...")
        try:
            # Look for headline input
            headline_input = await page.wait_for_selector(
                'input[id*="headline"], input[name*="headline"], input[aria-label*="Headline"]',
                timeout=10000
            )
            if headline_input:
                await headline_input.click()
                await page.keyboard.press("Control+A")
                await page.keyboard.type(NEW_HEADLINE)
                print(f"   ✅ Headline: {NEW_HEADLINE}")
        except Exception as e:
            print(f"   ⚠️ Не удалось найти поле Headline: {e}")
            print("   Попробуйте обновить вручную")

        # Step 4: Save
        print("\n📍 Шаг 4: Сохраняю изменения...")
        try:
            save_btn = await page.wait_for_selector(
                'button[type="submit"], button:has-text("Save"), button:has-text("Сохранить")',
                timeout=5000
            )
            if save_btn:
                await save_btn.click()
                await asyncio.sleep(2)
                print("   ✅ Сохранено!")
        except Exception:
            print("   ⚠️ Кнопка сохранения не найдена")

        # Step 5: Update About section
        print("\n📍 Шаг 5: Обновляю раздел 'О себе'...")
        await page.goto(f"{PROFILE_URL}/edit/about/", timeout=30000)
        await asyncio.sleep(2)

        try:
            about_textarea = await page.wait_for_selector(
                'textarea, [contenteditable="true"]',
                timeout=10000
            )
            if about_textarea:
                await about_textarea.click()
                await page.keyboard.press("Control+A")
                await page.keyboard.type(NEW_ABOUT)
                print("   ✅ About section обновлен!")

                # Save
                save_btn = await page.query_selector('button[type="submit"], button:has-text("Save")')
                if save_btn:
                    await save_btn.click()
                    await asyncio.sleep(2)
        except Exception as e:
            print(f"   ⚠️ Ошибка при обновлении About: {e}")

        # Step 6: Verify
        print("\n📍 Шаг 6: Проверяю результат...")
        await page.goto(PROFILE_URL, timeout=30000)
        await asyncio.sleep(2)

        # Get current headline
        try:
            headline_el = await page.query_selector('div.text-body-medium')
            if headline_el:
                current = await headline_el.inner_text()
                print(f"   Текущий headline: {current[:50]}...")
        except Exception:
            pass

        print("\n" + "="*60)
        print("✅ ГОТОВО!")
        print("="*60)
        print("\nПроверьте профиль в браузере.")
        print("Нажмите Enter для закрытия...")

        input()
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
