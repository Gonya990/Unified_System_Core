#!/usr/bin/env python3
"""
LinkedIn Video Uploader
Uses Selenium for automated video uploads
"""

import os
import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# LinkedIn credentials
LINKEDIN_EMAIL = os.getenv("LINKEDIN_EMAIL", "")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD", "")

def create_driver(headless: bool = True) -> webdriver.Chrome:
    """Create Chrome driver with options"""
    options = Options()
    if headless:
        options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    
    return webdriver.Chrome(options=options)

def login_linkedin(driver: webdriver.Chrome) -> bool:
    """Login to LinkedIn"""
    print("🔐 Logging into LinkedIn...")
    
    try:
        driver.get("https://www.linkedin.com/login")
        time.sleep(2)
        
        # Enter email
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        email_input.send_keys(LINKEDIN_EMAIL)
        
        # Enter password
        password_input = driver.find_element(By.ID, "password")
        password_input.send_keys(LINKEDIN_PASSWORD)
        
        # Click login
        login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        login_button.click()
        
        time.sleep(3)
        
        # Check if login successful
        if "feed" in driver.current_url:
            print("✅ LinkedIn login successful")
            return True
        else:
            print("❌ LinkedIn login may have failed")
            return False
            
    except Exception as e:
        print(f"❌ LinkedIn login error: {e}")
        return False

def upload_video_linkedin(
    video_path: Path,
    caption: str,
    headless: bool = True
) -> bool:
    """
    Upload video to LinkedIn
    
    Args:
        video_path: Path to video file
        caption: Post caption/text
        headless: Run browser in headless mode
    
    Returns:
        True if upload successful
    """
    if not LINKEDIN_EMAIL or not LINKEDIN_PASSWORD:
        print("⚠️ LinkedIn credentials not set")
        print("Set LINKEDIN_EMAIL and LINKEDIN_PASSWORD environment variables")
        return False
    
    if not video_path.exists():
        print(f"❌ Video not found: {video_path}")
        return False
    
    print(f"📤 Uploading to LinkedIn: {video_path}")
    
    driver = None
    try:
        driver = create_driver(headless)
        
        if not login_linkedin(driver):
            return False
        
        # Navigate to post creation
        driver.get("https://www.linkedin.com/feed/")
        time.sleep(2)
        
        # Click "Start a post"
        start_post = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.share-box-feed-entry__trigger'))
        )
        start_post.click()
        time.sleep(2)
        
        # Click media button
        media_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label*="Add media"]'))
        )
        media_button.click()
        time.sleep(2)
        
        # Upload video file
        file_input = driver.find_element(By.CSS_SELECTOR, 'input[type="file"]')
        file_input.send_keys(str(video_path.absolute()))
        
        # Wait for upload
        print("⏳ Waiting for video upload...")
        time.sleep(30)  # Videos take time to upload
        
        # Enter caption
        text_area = driver.find_element(By.CSS_SELECTOR, 'div[data-placeholder]')
        text_area.send_keys(caption)
        time.sleep(1)
        
        # Click Post button
        post_button = driver.find_element(By.CSS_SELECTOR, 'button.share-actions__primary-action')
        post_button.click()
        
        print("✅ LinkedIn video posted successfully!")
        time.sleep(3)
        return True
        
    except Exception as e:
        print(f"❌ LinkedIn upload error: {e}")
        return False
        
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    # Test upload (requires credentials)
    ROOT_DIR = Path(__file__).parent.resolve()
    test_video = ROOT_DIR / "outputs" / "igor_ru_final.mp4"
    test_caption = "Test post from Content Farm automation 🤖 #AI #ContentCreation"
    
    if test_video.exists():
        upload_video_linkedin(test_video, test_caption, headless=False)
    else:
        print(f"Test video not found: {test_video}")
