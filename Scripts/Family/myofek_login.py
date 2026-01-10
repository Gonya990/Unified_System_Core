
import os
import sys
import logging
import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup Paths
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(ROOT_DIR))

# Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("MyOfekLogin")

# MYOFEK CONFIG
LOGIN_URL = "https://productplayer.cet.ac.il" # Based on search results
# Alternative: https://myofek.cet.ac.il/

def login_myofek_selenium(username, password):
    """
    Login to MyOfek using Selenium (headless).
    Returns driver or cookies.
    """
    logger.info(f"Attempting login to MyOfek for user {username}...")
    
    options = Options()
    options.add_argument("--headless") # Run in background
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    try:
        driver = webdriver.Chrome(options=options)
        driver.get(LOGIN_URL)
        
        # Wait for Page Load (and potential redirect to Ministry of Ed login)
        time.sleep(3)
        logger.info(f"Page Title: {driver.title}")
        
        # NOTE: MyOfek often redirects to "Edu ID" (Misrad HaHinuch)
        # We need to detect which login form is present.
        # This is V1 logic - finding generic input fields.
        
        # Check for MoE Login owl/button
        # <button class="login-button">...
        
        # Assuming direct or MoE login:
        # User/Pass fields often change ID.
        # We try generic "username" / "password" selectors if standard failing.
        
        # TODO: Refine selectors based on ACTUAL page HTML observed during runtime or user feedback.
        
        logger.warning("Unsure of exact selectors without visual check. Saving screenshot...")
        driver.save_screenshot(str(ROOT_DIR / "logs/myofek_login_page.png"))
        
        # Placeholder for actual fill logic
        # 1. Click "Login" button if exists
        # 2. Fill User/Pass
        # 3. Submit
        
        # driver.find_element(By.ID, "user").send_keys(username)
        # driver.find_element(By.ID, "pass").send_keys(password)
        # driver.find_element(By.ID, "submit").click()
        
        logger.info("Login logic incomplete - waiting for Page Structure info.")
        driver.quit()
        return False

    except Exception as e:
        logger.error(f"Selenium Error: {e}")
        try:
            driver.quit()
        except: pass
        return False

if __name__ == "__main__":
    user = os.getenv("MYOFEK_USER", "PLACEHOLDER")
    pwd = os.getenv("MYOFEK_PASS", "PLACEHOLDER")
    
    if user == "PLACEHOLDER":
        print("❌ Set MYOFEK_USER and MYOFEK_PASS env vars.")
    else:
        login_myofek_selenium(user, pwd)
