import asyncio
import json
import logging
import os
from pathlib import Path

from dotenv import load_dotenv

# Browser Use & LangChain
try:
    from browser_use import Agent
    from langchain_google_genai import ChatGoogleGenerativeAI
except ImportError:
    # Fallback for local dev without libs
    Agent = None

from telegram_notify import send_telegram_message
from gmail_agent import get_gmail_service, get_unread_emails

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("job_hunter.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("JobHunter")

BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / "config" / "profiles.json"
ENV_PATH = BASE_DIR / ".env"

# Load Env
load_dotenv(ENV_PATH)
# Also try to load from Projects/AI_Core locations if on server
load_dotenv(BASE_DIR.parent.parent / "Projects" / "AI_Core" / ".env")


async def load_config():
    if not CONFIG_PATH.exists():
        logger.error(f"Config not found at {CONFIG_PATH}")
        return None
    with open(CONFIG_PATH) as f:
        return json.load(f)

def get_llm():
    """Configure LLM based on environment"""
    # api_key = os.getenv("OPENAI_API_KEY")
    # if api_key:
    #    pass # OpenAI Disabled due to permission errors

    gemini_key = os.getenv("GEMINI_API_KEY")
    if gemini_key:
        real_llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", google_api_key=gemini_key)

        class GeminiAdapter:
            def __init__(self, llm):
                self._llm = llm
                self.provider = "google"
                self.model_name = llm.model

            def __getattr__(self, name):
                return getattr(self._llm, name)

            async def ainvoke(self, *args, **kwargs):
                return await self._llm.ainvoke(*args, **kwargs)

            def invoke(self, *args, **kwargs):
                return self._llm.invoke(*args, **kwargs)

        return GeminiAdapter(real_llm)

    logger.error("No valid API Key found (OPENAI_API_KEY or GEMINI_API_KEY)")
    return None

# Job Hunter - Email Analysis Mode
# Analyzes incoming Gmail vacancies against User CV

# Analyzes incoming Gmail vacancies against User CV


async def process_profile(profile, llm):
    # 1. Load Real CV & Priority Skills
    cv_path = BASE_DIR.parent.parent / "REAL_CV.txt"
    skills_path = BASE_DIR.parent.parent / "NEW_SKILLS.txt"

    user_cv = ""
    priority_skills = ""

    if cv_path.exists():
        with open(cv_path, encoding="utf-8") as f:
            user_cv = f.read()

    if skills_path.exists():
        with open(skills_path, encoding="utf-8") as f:
            priority_skills = f.read()

    # 2. Fetch Emails
    logger.info("Fetching unread emails from Gmail...")
    try:
        service = get_gmail_service()
        emails = get_unread_emails(service, max_results=20)
    except Exception as e:
        logger.error(f"Gmail fetch failed: {e}")
        return

    # 3. Filter Job Emails
    job_emails = [e for e in emails if e['category'] in ['work', 'linkedin', 'urgent']]

    if not job_emails:
        logger.info("No new job-related emails found.")
        send_telegram_message("ℹ️ Job Analyzer: No new job emails found.")
        return

    logger.info(f"Analyzing {len(job_emails)} job emails...")
    send_telegram_message(f"🔎 Job Analyzer: Found {len(job_emails)} potential job emails. Analyzing with Priority Skills...")

    # 4. Analyze each
    for email in job_emails:
        description = f"Subject: {email['subject']}\nFrom: {email['sender']}\nBody: {email['body_preview']}..."

        prompt = (
            f"Ты - Карьерный Аналитик. \n"
            f"**Задача:** Проанализируй эту вакансию (из письма) на соответствие Резюме (CV) и Приоритетным Навыкам пользователя.\n"
            f"**Письмо:**\n{description}\n\n"
            f"**Резюме пользователя:**\n{user_cv[:2000]}\n\n"
            f"**ПРИОРИТЕТНЫЕ НАВЫКИ (Критически важны):**\n{priority_skills[:1000]}\n\n"
            f"**Формат ответа (НА РУССКОМ ЯЗЫКЕ):**\n"
            f"Совпадение: [0-100]%\n"
            f"Роль: [Название роли]\n"
            f"Компания: [Название компании]\n"
            f"Анализ: [1-2 предложения, почему подходит или нет. Обязательно упомяни, если есть Приоритетные Навыки]\n"
            f"Действие: [Откликнуться / Игнорировать / Срочно]"
        )

        try:
            # Use invoke directly since we are just doing text analysis, no browser needed
            response = llm.invoke(prompt)
            analysis = response.content

            # Send Report
            msg = (
                f"📧 **Анализ Вакансии**\n"
                f"От: {email['sender']}\n"
                f"{analysis}"
            )
            send_telegram_message(msg)

        except Exception as e:
            logger.error(f"Analysis failed for {email['id']}: {e}")

async def main():
    await load_config() # Keep config loading just for structure
    llm = get_llm()
    if not llm:
        return

    logger.info("Starting Job Analyzer (Email Mode)...")
    await process_profile({"name": "User"}, llm)
    logger.info("Analysis complete.")

if __name__ == "__main__":
    asyncio.run(main())
