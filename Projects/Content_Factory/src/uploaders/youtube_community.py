#!/usr/bin/env python3
"""
YouTube Community Tab Automator (Playwright)
Because API does not support Community Posts.
"""

import asyncio
import sys
from pathlib import Path

from playwright.async_api import async_playwright

# Store session in the same folder as other credentials
STATE_FILE = Path(__file__).parent / ".credentials" / "youtube_browser_state.json"
STATE_FILE.parent.mkdir(parents=True, exist_ok=True)

class YouTubeCommunity:
    def __init__(self, headless: bool = True):
        self.headless = headless
        self.browser = None
        self.context = None
        self.page = None

    async def start(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=self.headless)

        if STATE_FILE.exists():
            print("🔑 Loading YouTube session...")
            self.context = await self.browser.new_context(storage_state=str(STATE_FILE))
        else:
            print("⚠️ No session found. Need manual login.")
            self.context = await self.browser.new_context()

        self.page = await self.context.new_page()

    async def login_manual(self):
        """Interactive login to save session"""
        print("🔐 Opening YouTube Studio for manual login...")
        if self.browser: await self.browser.close()

        self.playwright = await async_playwright().start()
        # Headless=False so user can see
        self.browser = await self.playwright.chromium.launch(headless=False)
        self.context = await self.browser.new_context()
        self.page = await self.context.new_page()

        # Navigate to Studio directly
        await self.page.goto("https://studio.youtube.com/")

        print("⏳ Please login manually...")
        print("   Once you see the Studio Dashboard, press Enter here.")
        input()

        await self.context.storage_state(path=str(STATE_FILE))
        print(f"✅ Session saved to {STATE_FILE}")
        await self.close()

    async def post_community_update(self, text, image_path=None):
        if not self.page: await self.start()

        print("📝 Navigating to Community Tab...")
        # Direct link to create post usually tricky, better go to channel content or main studio
        # Actually, clicking 'Create' -> 'Create post' is standard in Studio
        await self.page.goto("https://studio.youtube.com/")

        try:
            # Wait for 'Create' button
            # This selector path might change, need robust finding
            create_btn = self.page.get_by_test_id("create-icon")
            # or try text
            if not await create_btn.count():
                create_btn = self.page.locator("#create-icon")

            await create_btn.click()

            # Click 'Create post'
            # Usually a menu item
            await self.page.get_by_text("Create post").click()

            # Now we are likely redirected to the community tab on the front-end or a dialog
            # YouTube usually redirects to https://www.youtube.com/channel/UC.../community?show_compose=1

            # Let's wait for the input box
            # It's an editable div usually
            print("⏳ Waiting for composer...")
            await self.page.wait_for_selector("#creation-box", timeout=15000)

            # Type text
            await self.page.click("#creation-box")
            await self.page.keyboard.type(text)

            if image_path:
                print("🖼 Attaching image...")
                # Find input type=file
                # This is tricky in Polymer/Shadow DOM
                pass

            # Click Post
            await self.page.get_by_text("Post").click()
            print("✅ Community Post Published!")

        except Exception as e:
            print(f"❌ Failed to post: {e}")
            # Save screenshot for debug
            await self.page.screenshot(path="community_fail.png")

    async def close(self):
        if self.context: await self.context.close()
        if self.browser: await self.browser.close()
        if hasattr(self, 'playwright'): await self.playwright.stop()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "login":
        import asyncio
        yt = YouTubeCommunity(headless=False)
        asyncio.run(yt.login_manual())
    else:
        print("Usage: python3 youtube_community.py login")
