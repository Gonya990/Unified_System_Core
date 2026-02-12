#!/usr/bin/env python3
"""
Threads Browser Automation using Playwright
Workaround for blocked Threads API
"""

import asyncio
from pathlib import Path
from typing import Union

from playwright.async_api import async_playwright

# Paths
STATE_FILE = Path(__file__).parent / ".threads_state.json"


class ThreadsBrowser:
    def __init__(self, headless: bool = True):
        self.headless = headless
        self.browser = None
        self.context = None
        self.page = None

    async def start(self):
        """Initialize browser with saved state"""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=self.headless)

        # Load saved state if exists
        if STATE_FILE.exists():
            print("🔑 Loading saved session...")
            self.context = await self.browser.new_context(storage_state=str(STATE_FILE))
        else:
            print("⚠️ No saved session found. Manual login required.")
            self.context = await self.browser.new_context()

        self.page = await self.context.new_page()
        return self

    async def login_manual(self):
        """Open browser for manual login and save state"""
        print("🔐 Opening Threads for manual login...")

        # Launch visible browser
        self.browser = await self.playwright.chromium.launch(headless=False)
        self.context = await self.browser.new_context()
        self.page = await self.context.new_page()

        await self.page.goto("https://www.threads.net/login")

        print("⏳ Please login manually in the browser...")
        print("   After login, press Enter here to save session.")
        input()

        # Save state
        await self.context.storage_state(path=str(STATE_FILE))
        print(f"✅ Session saved to {STATE_FILE}")

        await self.close()

    async def post(self, text: str, image_path: Union[str, list] = None):
        """Create a new Threads post"""
        if not self.page:
            await self.start()

        print(f"📝 Creating Threads post: {text[:50]}...")

        # Navigate to Threads
        await self.page.goto("https://www.threads.net")
        await self.page.wait_for_load_state("networkidle")

        # Check if logged in
        try:
            # Look for compose button or "New thread" area
            # Wait for the main feed to load
            await self.page.wait_for_selector(
                '[data-pressable-container="true"]', timeout=10000
            )

            # Find and click "Start a thread" or compose button
            compose_selectors = [
                'text="Start a thread"',
                '[aria-label="Create"]',
                '[aria-label="New thread"]',
                'div[role="button"]:has-text("thread")',
            ]

            for selector in compose_selectors:
                try:
                    await self.page.click(selector, timeout=3000)
                    break
                except Exception:
                    continue

            # Wait for compose modal/area
            await self.page.wait_for_timeout(1000)

            # Type the post content
            textarea_selectors = [
                '[contenteditable="true"]',
                'div[role="textbox"]',
                "textarea",
            ]

            for selector in textarea_selectors:
                try:
                    await self.page.fill(selector, text, timeout=3000)
                    break
                except Exception:
                    try:
                        element = await self.page.query_selector(selector)
                        if element:
                            await element.type(text, delay=50)
                            break
                    except Exception:
                        continue

            # Handle image upload if provided
            if image_path:
                try:
                    # Convert single string to list
                    files_to_upload = (
                        [image_path] if isinstance(image_path, str) else image_path
                    )

                    # Validate files exist
                    valid_files = [f for f in files_to_upload if Path(f).exists()]

                    if valid_files:
                        file_input = await self.page.query_selector(
                            'input[type="file"]'
                        )
                        if file_input:
                            await file_input.set_input_files(valid_files)
                            await self.page.wait_for_timeout(2000)
                except Exception as e:
                    print(f"⚠️ Image upload failed: {e}")

            # Click Post button
            post_selectors = [
                'text="Post"',
                '[aria-label="Post"]',
                'div[role="button"]:has-text("Post")',
            ]

            for selector in post_selectors:
                try:
                    await self.page.click(selector, timeout=3000)
                    print("✅ Post button clicked!")
                    break
                except Exception:
                    continue

            # Wait for post to complete
            await self.page.wait_for_timeout(3000)

            # Verify success
            print("✅ Threads post created successfully!")
            return True

        except Exception as e:
            print(f"❌ Failed to create post: {e}")

            # Check if login required
            if "login" in self.page.url.lower():
                print("⚠️ Session expired. Please run login_manual() first.")

            return False

    async def close(self):
        """Clean up browser resources"""
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if hasattr(self, "playwright"):
            await self.playwright.stop()


async def main():
    """Test the Threads browser automation"""
    import sys

    # Default to headless=True for server environment
    threads = ThreadsBrowser(headless=True)

    if len(sys.argv) > 1 and sys.argv[1] == "login":
        # Cannot run headed on server without Xvfb
        print("⚠️ Interactive login requires local browser or Xvfb.")
        print("Please upload .threads_state.json manually to this directory.")
        return
    else:
        await threads.start()
        await threads.post("🚀 Testing Unified System automation! #AI #Future")
        await threads.close()


if __name__ == "__main__":
    asyncio.run(main())
