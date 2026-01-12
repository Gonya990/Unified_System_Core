#!/usr/bin/env python3
"""
LinkedIn Job Search & Apply Script
Поиск вакансий и автоматические отклики
"""

import asyncio
import json
import sys
from datetime import datetime
from pathlib import Path

PROFILE_URL = "https://www.linkedin.com/in/igor-goncha/"
JOBS_SEARCH_URL = "https://www.linkedin.com/jobs/search/?keywords=supervisor%20project%20coordinator&location=Israel&f_AL=true"

# Resume files
RESUME_HE = "/Users/macbook/Documents/Unified_System/docs/resume/Resume_B_Hebrew_Tech.pdf"
RESUME_EN = "/Users/macbook/Documents/Unified_System/docs/resume/Resume_English_PM.pdf"

RESULTS_FILE = Path(__file__).parent / "linkedin_job_results.json"


async def main():
    print("\n" + "="*60)
    print("🔍 LINKEDIN JOB SEARCH & APPLY")
    print("="*60)
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    try:
        from playwright.async_api import async_playwright
    except ImportError:
        print("❌ Playwright не установлен!")
        sys.exit(1)

    results = {
        "timestamp": datetime.now().isoformat(),
        "profile": {},
        "jobs_found": [],
        "applications_sent": []
    }

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            slow_mo=500
        )

        context = await browser.new_context(
            viewport={'width': 1400, 'height': 900}
        )

        page = await context.new_page()

        # ========== STEP 1: Check Profile ==========
        print("\n" + "-"*40)
        print("📍 ШАГ 1: Проверка профиля")
        print("-"*40)

        await page.goto(PROFILE_URL, timeout=30000)
        await asyncio.sleep(3)

        if "/login" in page.url or "/authwall" in page.url:
            print("\n🔐 Требуется вход в LinkedIn!")
            print("   Войдите в браузере...")
            await page.goto("https://www.linkedin.com/login")
            input("\n>>> Нажмите Enter после входа: ")
            await page.goto(PROFILE_URL, timeout=30000)
            await asyncio.sleep(3)

        print("✅ Профиль загружен!")

        # Get profile info
        try:
            headline_el = await page.query_selector('div.text-body-medium')
            if headline_el:
                results["profile"]["headline"] = await headline_el.inner_text()
                print(f"   Headline: {results['profile']['headline'][:50]}...")

            # Check Open to Work
            otw = await page.query_selector('[class*="open-to-work"], [class*="openToWork"]')
            results["profile"]["open_to_work"] = otw is not None
            print(f"   Open to Work: {'✅ Да' if otw else '❌ Нет'}")

        except Exception as e:
            print(f"   ⚠️ Ошибка: {e}")

        # ========== STEP 2: Search Jobs ==========
        print("\n" + "-"*40)
        print("📍 ШАГ 2: Поиск вакансий")
        print("-"*40)

        await page.goto(JOBS_SEARCH_URL, timeout=30000)
        await asyncio.sleep(4)

        print("   Критерии: Supervisor, Project Coordinator, Israel, Easy Apply")

        # Get job listings
        job_cards = await page.query_selector_all('.jobs-search-results__list-item, .job-card-container')
        print(f"   Найдено карточек: {len(job_cards)}")

        jobs = []
        for i, card in enumerate(job_cards[:10]):  # First 10
            try:
                title_el = await card.query_selector('a.job-card-list__title, .job-card-container__link')
                company_el = await card.query_selector('.job-card-container__primary-description, .job-card-container__company-name')
                location_el = await card.query_selector('.job-card-container__metadata-item')
                easy_apply = await card.query_selector('[class*="easy-apply"], svg[data-test-icon="linkedin"]')

                job = {
                    "title": await title_el.inner_text() if title_el else "Unknown",
                    "company": await company_el.inner_text() if company_el else "Unknown",
                    "location": await location_el.inner_text() if location_el else "Unknown",
                    "easy_apply": easy_apply is not None
                }
                jobs.append(job)
                print(f"   {i+1}. {job['title'][:40]} @ {job['company'][:20]} {'[Easy Apply]' if job['easy_apply'] else ''}")
            except:
                continue

        results["jobs_found"] = jobs

        if not jobs:
            print("\n⚠️ Вакансии не найдены. Попробуйте расширить поиск.")

        # ========== STEP 3: Easy Apply ==========
        print("\n" + "-"*40)
        print("📍 ШАГ 3: Отклики на вакансии")
        print("-"*40)

        easy_apply_jobs = [j for j in jobs if j.get("easy_apply")]
        print(f"   Вакансий с Easy Apply: {len(easy_apply_jobs)}")

        if easy_apply_jobs and len(job_cards) > 0:
            print("\n   Открываю первую вакансию с Easy Apply...")

            # Click first job
            try:
                first_card = job_cards[0]
                await first_card.click()
                await asyncio.sleep(3)

                # Look for Easy Apply button
                apply_btn = await page.query_selector('button.jobs-apply-button, button:has-text("Easy Apply")')
                if apply_btn:
                    btn_text = await apply_btn.inner_text()
                    print(f"   Найдена кнопка: {btn_text}")

                    # Click to open form
                    await apply_btn.click()
                    await asyncio.sleep(2)

                    # Check what form fields appear
                    print("\n   📋 Форма заявки:")

                    resume_upload = await page.query_selector('input[type="file"], [class*="resume-upload"]')
                    if resume_upload:
                        print("   - ✅ Загрузка резюме")

                    phone_input = await page.query_selector('input[name*="phone"], input[id*="phone"]')
                    if phone_input:
                        print("   - ✅ Поле телефон")

                    # Don't submit - just report
                    print("\n   ⚠️ Форма готова. Ожидаю подтверждение для отправки...")

                    choice = input("\n>>> Отправить заявку? (y/n): ").strip().lower()
                    if choice == 'y':
                        submit_btn = await page.query_selector('button[aria-label*="Submit"], button:has-text("Submit")')
                        if submit_btn:
                            await submit_btn.click()
                            await asyncio.sleep(2)
                            print("   ✅ Заявка отправлена!")
                            results["applications_sent"].append(jobs[0])
                    else:
                        # Close modal
                        close_btn = await page.query_selector('button[aria-label="Dismiss"]')
                        if close_btn:
                            await close_btn.click()
                        print("   ❌ Отменено пользователем")

            except Exception as e:
                print(f"   ⚠️ Ошибка при отклике: {e}")

        # ========== STEP 4: Save Results ==========
        print("\n" + "-"*40)
        print("📍 ШАГ 4: Сохранение результатов")
        print("-"*40)

        with open(RESULTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        print(f"   💾 Результаты: {RESULTS_FILE}")

        # Summary
        print("\n" + "="*60)
        print("📊 ИТОГО")
        print("="*60)
        print(f"   Профиль: {PROFILE_URL}")
        print(f"   Open to Work: {'✅' if results['profile'].get('open_to_work') else '❌'}")
        print(f"   Найдено вакансий: {len(jobs)}")
        print(f"   С Easy Apply: {len(easy_apply_jobs)}")
        print(f"   Отправлено заявок: {len(results['applications_sent'])}")

        input("\n>>> Нажмите Enter для закрытия браузера...")
        await browser.close()

    return results


if __name__ == "__main__":
    asyncio.run(main())
