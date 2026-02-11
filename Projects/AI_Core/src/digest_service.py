"""
Daily Digest Service
Generates and sends daily summary reports to users.
"""
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class DigestService:
    """Generates daily digest reports."""

    def __init__(
        self,
        usage_tracker,
        task_manager,
        linear_client,
        infra_manager,
        calendar_client=None,
        ha_controller=None,
    ):
        self.usage_tracker = usage_tracker
        self.task_manager = task_manager
        self.linear_client = linear_client
        self.infra_manager = infra_manager
        self.calendar_client = calendar_client
        self.ha_controller = ha_controller

    async def generate_digest(self, user_id: int, username: str) -> str:
        """Generate daily digest for a user."""
        if self.ha_controller:
            # We fetch shopping recommendations from finance_manager
            # if available via the orchestrator or directly
            pass

        today = datetime.now().strftime("%d.%m.%Y")
        day_name = datetime.now().strftime("%A")

        # Translate day name to Russian
        days_ru = {
            "Monday": "Понедельник",
            "Tuesday": "Вторник",
            "Wednesday": "Среда",
            "Thursday": "Четверг",
            "Friday": "Пятница",
            "Saturday": "Суббота",
            "Sunday": "Воскресенье"
        }
        day_ru = days_ru.get(day_name, day_name)

        digest = f"🌅 **Доброе утро, {username}!**\n\n"
        digest += f"📅 {day_ru}, {today}\n\n"
        digest += "━━━━━━━━━━━━━━━━━━━━\n\n"

        # 1. Yesterday's Stats
        stats = self.usage_tracker.get_user_stats(user_id, days=1)
        if stats and stats.get('total_tokens', 0) > 0:
            digest += "📊 **Вчера:**\n"
            digest += f"  • Токенов: {stats['total_tokens']:,}\n"
            digest += f"  • Запросов: {stats['requests']}\n\n"

        # 2. Tasks (Local)
        tasks = self.task_manager.list_tasks(user_id)
        if tasks:
            digest += f"📝 **Задачи ({len(tasks)}):**\n"
            for t in tasks[:3]:  # Top 3
                digest += f"  • {t['text']}\n"
            if len(tasks) > 3:
                digest += f"  ... и ещё {len(tasks) - 3}\n"
            digest += "\n"

        # 3. Linear Tasks
        if self.linear_client.api_key:
            try:
                issues = self.linear_client.get_my_issues(limit=5)
                if issues:
                    digest += f"📋 **Linear ({len(issues)}):**\n"
                    for issue in issues[:3]:
                        title_trunc = issue["title"][:40]
                        digest += (
                            f"  • {issue['identifier']}: {title_trunc}...\n"
                        )
                    if len(issues) > 3:
                        digest += f"  ... и ещё {len(issues) - 3}\n"
                    digest += "\n"
            except Exception as e:
                logger.error(f"Failed to fetch Linear issues for digest: {e}")

        # 4. Infrastructure Status
        try:
            health_summary = []
            for node in self.infra_manager.data.get("nodes", []):
                status = "🟢" if node.get("reachable") else "🔴"
                health_summary.append(f"{status} {node['name']}")

            if health_summary:
                digest += "🏗 **Инфраструктура:**\n"
                digest += "  " + " | ".join(health_summary) + "\n\n"
        except Exception as e:
            logger.error(f"Failed to get infra status for digest: {e}")

        # 5. Home Assistant Status
        if self.ha_controller:
            try:
                ha_report = await self.ha_controller.get_sensors_report()
                if ha_report and "не найдено" not in ha_report:
                    digest += ha_report + "\n"
            except Exception as e:
                logger.error(f"Failed to get HA report for digest: {e}")

        # 6. Shopping Strategy
        # Trying to find finance_manager in self? No, but maybe we can pass it
        # However, for now, we can check if it's available.
        # Let's assume finance_manager is passed in __init__
        if hasattr(self, "finance_manager") and self.finance_manager:
            try:
                shop_report = (
                    await self.finance_manager.get_shopping_recommendations(user_id)
                )
                if shop_report and "не найдено" not in shop_report:
                    digest += shop_report + "\n\n"
            except Exception as e:
                logger.error(f"Failed to get shopping report for digest: {e}")

        # 5. Calendar Events (Today)
        if self.calendar_client:
            try:
                events = self.calendar_client.get_today_events()
                if events:
                    digest += f"📅 **События сегодня ({len(events)}):**\n"
                    for event in events[:3]:
                        formatted = self.calendar_client.format_event(event)
                        digest += f"  • {formatted}\n"
                    if len(events) > 3:
                        digest += f"  ... и ещё {len(events) - 3}\n"
                    digest += "\n"
            except Exception as e:
                logger.error(f"Failed to fetch calendar events for digest: {e}")

        # 6. Motivational Quote
        quotes = [
            "💪 Сегодня отличный день для продуктивности!",
            "🚀 Начни день с главной задачи!",
            "⭐ Маленькие шаги ведут к большим целям!",
            "🎯 Фокус на важном, а не срочном!",
            "🌟 Ты можешь больше, чем думаешь!"
        ]
        import random
        digest += quotes[random.randint(0, len(quotes) - 1)] + "\n\n"

        digest += "━━━━━━━━━━━━━━━━━━━━\n"
        digest += "Хорошего дня! 😊"

        return digest
