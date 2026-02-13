import datetime
from enum import Enum


class ContentLanguage(Enum):
    RU = "ru"
    EN = "en"
    HE = "he"


def get_daily_production_plan():
    """
    Returns a list of content tasks for the current day/time based on Master Plan.
    """
    now = datetime.datetime.now()
    weekday = now.weekday()  # 0 = Mon, 6 = Sun

    tasks = []

    # RU Base Schedule (Daily)
    # Triggered at 08:30 for 09:00 post, and 17:30 for 18:00 post
    # But for simplicity, we return the plan for the *whole day* if run in morning.

    tasks.append({"lang": ContentLanguage.RU, "slot": "morning"})
    tasks.append({"lang": ContentLanguage.RU, "slot": "evening"})

    # Language Expansions (Mon=0, Thu=3)
    if weekday in [0, 3]:
        tasks.append({"lang": ContentLanguage.EN, "slot": "afternoon"})
        tasks.append({"lang": ContentLanguage.HE, "slot": "late_afternoon"})

    return tasks


if __name__ == "__main__":
    plan = get_daily_production_plan()
    print(f"📅 Plan for today ({datetime.datetime.now().strftime('%A')}):")
    for t in plan:
        print(f" - {t['lang'].value.upper()} ({t['slot']})")
