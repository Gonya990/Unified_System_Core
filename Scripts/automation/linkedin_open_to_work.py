#!/usr/bin/env python3
"""
LinkedIn: Enable Open to Work + Easy Apply Job Search
"""

import asyncio
import json
import sys
from datetime import datetime
from pathlib import Path

PROFILE_URL = "https://www.linkedin.com/in/igor-goncha/"
# URL с фильтром Easy Apply (f_AL=true)
JOBS_EASY_APPLY_URL = "https://www.linkedin.com/jobs/search/?keywords=supervisor%20OR%20operations%20manager%20OR%20field%20manager%20OR%20site%20manager&location=Israel&f_AL=true&f_TPR=r604800"

RESUME_HE = "/Users/macbook/Documents/Unified_System/docs/resume/Resume_B_Hebrew_Tech.pdf"
RESULTS_FILE = Path(__file__).parent / "linkedin_easy_apply_results.json"


async def main():
    print("\n" + "="*60)
    print("🚀 LINKEDIN: OPEN TO WORK + EASY APPLY")
    print("="*60)
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    try:
        from playwright.async_api import async_playwright
    except ImportError:
        print("❌ Playwright не установлен!")
        sys.exit(1)

    results = {
        "timestamp": datetime.now().isoformat(),
        "open_to_work_enabled": False,
        "jobs_found": [],
        "applications_sent": []
    }

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            slow_mo=400
        )

        context = await browser.new_context(viewport={'width': 1400, 'height': 900})
        page = await context.new_page()

        # === LOGIN CHECK ===
        print("\n📍 Проверка авторизации...")
        await page.goto("https://www.linkedin.com/feed/", timeout=30000)
        await asyncio.sleep(2)

        if "/login" in page.url or "/authwall" in page.url:
            print("🔐 Требуется вход!")
            await page.goto("https://www.linkedin.com/login")
            input("\n>>> Войдите и нажмите Enter: ")

        print("✅ Авторизация OK")

        # === STEP 1: ENABLE OPEN TO WORK ===
        print("\n" + "-"*40)
        print("📍 ШАГ 1: Включение Open to Work")
        print("-"*40)

        await page.goto(PROFILE_URL, timeout=30000)
        await asyncio.sleep(3)

        # Look for "Open to" button
        try:
            # Click on "Open to" button in profile header
            open_to_btn = await page.wait_for_selector(
                'button:has-text("Open to"), a:has-text("Open to")',
                timeout=5000
            )
            if open_to_btn:
                await open_to_btn.click()
                await asyncio.sleep(2)

                # Look for "Finding a new job" option
                finding_job = await page.query_selector(
                    'button:has-text("Finding a new job"), div:has-text("Finding a new job")'
                )
                if finding_job:
                    await finding_job.click()
                    await asyncio.sleep(2)
                    print("   ✅ Открыта форма Open to Work!")

                    # Try to save/enable
                    save_btn = await page.query_selector('button:has-text("Add to profile"), button:has-text("Save")')
                    if save_btn:
                        await save_btn.click()
                        await asyncio.sleep(2)
                        results["open_to_work_enabled"] = True
                        print("   ✅ Open to Work ВКЛЮЧЕН!")
                else:
                    print("   ⚠️ Не нашёл опцию 'Finding a new job'")
        except Exception as e:
            print(f"   ⚠️ Ошибка при включении Open to Work: {e}")
            print("   Попробуйте вручную: Профиль → Open to → Finding a new job")

        # === STEP 2: SEARCH EASY APPLY JOBS ===
        print("\n" + "-"*40)
        print("📍 ШАГ 2: Поиск вакансий с Easy Apply")
        print("-"*40)

        print(f"   URL: {JOBS_EASY_APPLY_URL[:60]}...")
        await page.goto(JOBS_EASY_APPLY_URL, timeout=30000)
        await asyncio.sleep(4)

        # Get job cards
        job_cards = await page.query_selector_all('.jobs-search-results__list-item, .job-card-container, [data-job-id]')
        print(f"   Найдено карточек: {len(job_cards)}")

        jobs = []
        for i, card in enumerate(job_cards[:15]):
            try:
                title_el = await card.query_selector('a strong, .job-card-list__title strong, [class*="job-card"] strong')
                company_el = await card.query_selector('[class*="company"], [class*="primary-description"]')

                title = await title_el.inner_text() if title_el else "Unknown"
                company = await company_el.inner_text() if company_el else "Unknown"

                job = {"title": title.strip(), "company": company.strip()[:30]}
                jobs.append(job)
                print(f"   {i+1}. {job['title'][:45]} @ {job['company']}")
            except Exception:
                continue

        results["jobs_found"] = jobs

        # === STEP 3: APPLY TO JOBS ===
        if jobs:
            print("\n" + "-"*40)
            print("📍 ШАГ 3: Отклики на вакансии")
            print("-"*40)

            for i, card in enumerate(job_cards[:5]):  # First 5 jobs
                try:
                    # Click job card
                    await card.click()
                    await asyncio.sleep(2)

                    # Find Easy Apply button
                    easy_apply_btn = await page.query_selector('button.jobs-apply-button')
                    if easy_apply_btn:
                        btn_text = await easy_apply_btn.inner_text()
                        if "Easy Apply" in btn_text:
                            print(f"\n   📝 Вакансия {i+1}: Найдена кнопка Easy Apply")

                            await easy_apply_btn.click()
                            await asyncio.sleep(2)

                            # Check for resume upload
                            file_input = await page.query_selector('input[type="file"]')
                            if file_input:
                                # Upload resume
                                await file_input.set_input_files(RESUME_HE)
                                print("      ✅ Резюме загружено")
                                await asyncio.sleep(1)

                            # Look for Submit or Next button
                            submit_btn = await page.query_selector('button[aria-label*="Submit"], button:has-text("Submit application")')
                            next_btn = await page.query_selector('button[aria-label*="Continue"], button:has-text("Next")')

                            if submit_btn:
                                # Direct submit available
                                choice = input(f"      >>> Отправить заявку на '{jobs[i]['title'][:30]}'? (y/n): ").strip().lower()
                                if choice == 'y':
                                    await submit_btn.click()
                                    await asyncio.sleep(2)
                                    print("      ✅ Заявка отправлена!")
                                    results["applications_sent"].append(jobs[i])
                                else:
                                    # Close modal
                                    close = await page.query_selector('button[aria-label="Dismiss"]')
                                    if close:
                                        await close.click()
                            elif next_btn:
                                print("      ⚠️ Требуется многошаговая форма")
                                close = await page.query_selector('button[aria-label="Dismiss"]')
                                if close:
                                    await close.click()

                            await asyncio.sleep(1)
                except Exception as e:
                    print(f"   ⚠️ Ошибка: {e}")
                    continue

        # === SAVE RESULTS ===
        print("\n" + "-"*40)
        print("📍 Сохранение результатов")
        print("-"*40)

        with open(RESULTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"   💾 {RESULTS_FILE}")

        # Summary
        print("\n" + "="*60)
        print("📊 ИТОГО")
        print("="*60)
        print(f"   Open to Work: {'✅ Включён' if results['open_to_work_enabled'] else '⚠️ Проверьте вручную'}")
        print(f"   Вакансий найдено: {len(jobs)}")
        print(f"   Заявок отправлено: {len(results['applications_sent'])}")

        input("\n>>> Enter для закрытия браузера...")
        await browser.close()

    return results


if __name__ == "__main__":
    asyncio.run(main())
