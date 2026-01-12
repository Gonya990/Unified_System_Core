
import logging
import os
import time
from pathlib import Path

import undetected_chromedriver as uc
from dotenv import load_dotenv
from selenium.webdriver.common.by import By

# Load Env
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(ROOT_DIR / ".env")

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("EduPortalLogin")

def setup_driver(headless=True):
    options = uc.ChromeOptions()
    if headless:
        # options.add_argument("--headless=new") # UC sometimes unstable with headless
        pass

    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1280,800")

    # UC automatically handles the driver download and patching
    driver = uc.Chrome(options=options, headless=headless, use_subprocess=True)

    return driver

def login_edu_portal(username, password):
    driver = None
    try:
        logger.info("Initializing Browser...")
        driver = setup_driver(headless=True)

        # Try direct link to "grades" or "messages" which should force login
        url = "https://parents.education.gov.il/prhnet/parent/grades"
        logger.info(f"Navigating to {url}...")
        driver.get(url)

        time.sleep(10) # Wait for redirects

        logger.info(f"Current URL: {driver.current_url}")
        driver.save_screenshot("debug_edu_portal_step1.png")

        # Check if we are on the Edu Login page
        # Usually looking for specific inputs
        page_source = driver.page_source

        if "Hizdaot" in driver.current_url or "edu.gov.il" in driver.current_url:
            logger.info("Found Unified Login Page.")

            # Try to find username input
            # Common IDs: "user", "HizdaotUser", "TeudatZehut"
            try:
                # Based on standard Edu login
                user_input = None

                # Strategy 1: Look for ID by name or id
                possible_user_selectors = ["HizdaotUser", "user", "username", "TeudatZehut"]
                for selector in possible_user_selectors:
                    try:
                        user_input = driver.find_element(By.ID, selector)
                        logger.info(f"Found user input with ID: {selector}")
                        break
                    except:
                        continue

                if not user_input:
                    # Try by Name
                    user_input = driver.find_element(By.NAME, "username")

                if user_input:
                    user_input.clear()
                    user_input.send_keys(username)
                    logger.info("Entered Username.")

                    # Password
                    # Usually prompted after clicking Next or on same page
                    # Sometimes SMS code is default. need to switch to "User/Pass" tab

                    # Look for "Login with Password" tab/link
                    # Text: "כניסה עם סיסמה" or similar
                    try:
                        pwd_tab = driver.find_element(By.XPATH, "//*[contains(text(), 'סיסמה')]")
                        pwd_tab.click()
                        time.sleep(2)
                    except:
                        pass # Maybe already on password tab

                    pwd_input = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
                    pwd_input.clear()
                    pwd_input.send_keys(password)
                    logger.info("Entered Password.")

                    # Submit
                    submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
                    submit_btn.click()
                    logger.info("Clicked Submit.")

                    time.sleep(15) # Wait for login processing

                    logger.info(f"Post-Login URL: {driver.current_url}")
                    driver.save_screenshot("debug_edu_portal_success.png")

                    if "parents.education.gov.il" in driver.current_url and "login" not in driver.current_url:
                        return True

            except Exception as e:
                logger.error(f"Interaction Error: {e}")

        elif "parents.education.gov.il" in driver.current_url:
             logger.info("Seem to be on Portal page (already logged in or public?)")

        return False

    except Exception as e:
        logger.error(f"Login Error: {e}")
        if driver:
            driver.save_screenshot("debug_error.png")
        return False
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    user = os.getenv("MASHOV_USER")
    pwd = os.getenv("MASHOV_PASS")

    if not user or not pwd:
        print("❌ USER/PASS env vars missing.")
    else:
        login_edu_portal(user, pwd)
