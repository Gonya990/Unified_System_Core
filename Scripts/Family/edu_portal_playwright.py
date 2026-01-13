import asyncio
import os
import sys
from pathlib import Path
from playwright.async_api import async_playwright
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(ROOT_DIR / ".env")

async def login_edu_portal():
    user = os.getenv("MASHOV_USER")
    pwd = os.getenv("MASHOV_PASS")
    
    if not user or not pwd:
        print("❌ Credentials missing in .env")
        return

    async with async_playwright() as p:
        print("🚀 Starting Playwright...")
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        # Direct link to Edu Login
        url = "https://web.mashov.info/api/login/mni/students"
        print(f"🔗 Navigating to {url}...")
        await page.goto(url)
        
        await page.wait_for_timeout(5000)
        
        print(f"📍 URL: {page.url}")
        
        if "idp.edu.gov.il" in page.url or "Hizdaot" in page.url:
            print("🔑 Login page detected. Entering credentials...")
            
            # Switch to password tab
            try:
                # Text usually contains "סיסמה"
                await page.click("text=/.*סיסמה.*/", timeout=5000)
                print("✅ Switched to password tab")
                await page.wait_for_timeout(1000)
            except:
                print("ℹ️ Already on password tab or switch failed")

            try:
                # Try multiple possible selectors for username/password
                await page.fill("input[name='HizdaotUser']", user, timeout=5000)
                await page.fill("input[name='password']", pwd, timeout=5000)
                await page.click("button[type='submit']")
                print("🚀 Credentials submitted")
            except Exception as e:
                # Fallback to general IDs
                try:
                    await page.fill("#HizdaotUser", user, timeout=2000)
                    await page.fill("#password", pwd, timeout=2000)
                    await page.click("#loginButton")
                    print("🚀 Credentials submitted (fallback)")
                except:
                    print(f"❌ Selection Error: {e}")
                    await page.screenshot(path="login_error.png")
                    await browser.close()
                    return
            
            print("⌛ Waiting for redirect...")
            await page.wait_for_timeout(15000)
            print(f"✅ Current URL: {page.url}")
            await page.screenshot(path="edu_portal_result.png")
            
            # If we are back at Mashov or Parents portal, it worked
            if "mashov" in page.url or "education" in page.url:
                print("🎉 SUCCESS: Logged in!")
                # Grab cookies for requests
                cookies = await context.cookies()
                print(f"🍪 Captured {len(cookies)} cookies")
            
        else:
            print(f"ℹ️ Redirected elsewhere: {page.url}")
            await page.screenshot(path="edu_portal_other.png")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(login_edu_portal())
