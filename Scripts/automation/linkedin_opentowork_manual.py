#!/usr/bin/env python3
"""
LinkedIn: Force Open to Work (Manual/Semi-Auto)
"""

import asyncio
import sys
from playwright.async_api import async_playwright

PROFILE_URL = "https://www.linkedin.com/in/igor-goncha/"

async def main():
    print("🚀 Opening LinkedIn...")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(viewport={'width': 1280, 'height': 800})
        page = await context.new_page()
        
        await page.goto(PROFILE_URL)
        
        print("\n" + "="*50)
        print("⚡️ ДЕЙСТВИЯ ПОЛЬЗОВАТЕЛЯ ⚡️")
        print("="*50)
        print("1. Войдите в LinkedIn (если нужно)")
        print("2. Нажмите кнопку 'Open to' (синяя, под именем)")
        print("3. Выберите 'Finding a new job'")
        print("4. Настройте желаемые позиции и нажмите Save")
        print("="*50)
        
        input("\n>>> Нажмите Enter когда закончите, чтобы закрыть браузер...")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
