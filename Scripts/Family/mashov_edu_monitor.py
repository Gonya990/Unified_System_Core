
import logging
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("MashovEduMonitor")

def get_mashov_session(user_id, password):
    """
    Login to Mashov via Ministry of Education using Selenium.
    Returns (cookies, csrf_token, user_uuid).
    """
    logger.info("Initializing Headless Browser...")
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # Mask automation
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = None
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        # 1. Go to Mashov Login
        logger.info("Navigating to Mashov Login...")
        driver.get("https://web.mashov.info/students/login")

        # 2. Click "Ministry of Education" (Yanshuf)
        # Selector might vary, searching by text or class
        # Usually looking for idp-login or similar
        wait = WebDriverWait(driver, 10)

        # Try finding the Edu button
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "mat-mdc-button-touch-target"))) # Generic?
        # Better: find by href or specific class for Edu login
        # Usually 'az.mashov.info' link or similar.
        # Let's search by partial text logic if possible or specific mashov selector
        # In Mashov Angular app: <a href="https://web.mashov.info/api/login/mni/students">...</a>

        # Direct navigation to Edu Login for Mashov to skip button parsing
        driver.get("https://web.mashov.info/api/login/mni/students")

        logger.info("Redirected to Edu Login. Entering credentials...")

        # 3. Fill Edu Form (Same as MyOfek)
        # Use explicit wait for inputs
        user_input = wait.until(EC.presence_of_element_located((By.ID, "userName")))
        pass_input = driver.find_element(By.ID, "password")

        user_input.clear()
        user_input.send_keys(user_id)
        pass_input.clear()
        pass_input.send_keys(password)

        # 4. Submit
        submit_btn = driver.find_element(By.CSS_SELECTOR, ".ui-button.ui-widget") # Standard Edu button
        submit_btn.click()

        logger.info("Submitted. Waiting for redirect back to Mashov...")

        # 5. Wait for mashov dashboard
        # URL should contain 'web.mashov.info/students/main'
        wait.until(EC.url_contains("web.mashov.info/students/main"))
        logger.info("Login Successful!")

        # 6. Extract Cookies and Validation
        cookies = {c['name']: c['value'] for c in driver.get_cookies()}

        # 7. Use Requests to get data (faster than scraping)
        # We need the X-Csrf-Token usually? Or checking API calls.
        # Mashov often puts user info in LocalStorage or Cookie.

        # Let's try to grab the user UUID from the URL or API
        # Or just return cookies to use with requests

        driver.quit()
        return cookies

    except Exception as e:
        logger.error(f"Login Failed: {e}")
        if driver:
            try:
                # Save debug screenshot
                driver.save_screenshot("mashov_login_fail.png")
            except: pass
            driver.quit()
        return None

def fetch_grades_api(cookies):
    """
    Fetch grades using the session cookies.
    Need to find the student UUID first.
    """
    import requests
    s = requests.Session()
    s.cookies.update(cookies)

    # 1. Get User Info / Config to find UUID
    # Mashov usually has an auth/user endpoint
    # Try listing students (if parent) or current user

    # For Student Login, there's usually one student.
    # We can inspect the 'mashov_auth_token' or similar in cookies?

    # Try generic endpoint
    r = s.get("https://web.mashov.info/api/user") # Hypothetical
    # Start with listing children if parent, or self if student

    # Harder part: Mashov API needs a CSRF token often in headers (X-Csrf-Token).
    # It is usually in the cookie 'csrf_token' -> header 'X-Csrf-Token'.
    csrf = cookies.get("csrf_token") or cookies.get("XSRF-TOKEN")
    if csrf:
        s.headers.update({"X-Csrf-Token": csrf})

    # Standard endpoint checks
    # /api/students -> returns list of students (for this user)
    try:
        r = s.get("https://web.mashov.info/api/students")
        if r.status_code == 200:
            students = r.json()
            if students:
                target = students[0]
                uuid = target['credential']['userId'] # e.g.
                logger.info(f"Found Student: {target['privateName']} {target['familyName']} ({uuid})")

                # Get Grades
                r_grades = s.get(f"https://web.mashov.info/api/students/{uuid}/grades")
                return r_grades.json()
    except Exception as e:
        logger.error(f"API Error: {e}")

    return []

if __name__ == "__main__":
    # Test
    # Load from .env if possible
    u = os.getenv("MASHOV_USER")
    p = os.getenv("MASHOV_PASS")

    if u and p:
        cookies = get_mashov_session(u, p)
        if cookies:
            grades = fetch_grades_api(cookies)
            print(f"Grades found: {len(grades)}")
            print(grades[:5]) # Show top 5
    else:
        print("Please set MASHOV_USER and PASS")

