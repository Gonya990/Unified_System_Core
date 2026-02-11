import logging
from datetime import datetime
from typing import Any

logger = logging.getLogger(__name__)

class FinanceManager:
    """
    Manages budget, expenses, and financial strategy.
    Stores data in Firestore under 'users/{user_id}/finances/'.
    """

    def __init__(self, db):
        self.db = db

    async def log_expense(self, user_id: int, expense_data: dict[str, Any]) -> str:
        """
        Log an expense to Firestore.
        expense_data: {merchant, date, amount, currency, category, items, original_text}
        """
        try:
            if not self.db.use_firestore:
                logger.warning(
                    "Firestore not available, logging expense to memories fallback."
                )
                self.db.add_memory(
                    user_id,
                    f"Expense: {expense_data.get('amount')} "
                    f"{expense_data.get('currency')}",
                    str(expense_data),
                )
                return "logged_to_memory"

            # Create document in subcollection
            expenses_ref = (
                self.db.db.collection("users")
                .document(str(user_id))
                .collection("expenses")
            )
            
            # Ensure date is a timestamp or string
            if "date" not in expense_data or not expense_data["date"]:
                expense_data["date"] = datetime.now().isoformat()
            
            expense_data["created_at"] = datetime.now()

            doc_ref = expenses_ref.add(expense_data)
            logger.info(
                f"Expense logged for user {user_id}: {expense_data.get('amount')}"
            )
            return doc_ref[1].id
        except Exception as e:
            logger.error(f"Failed to log expense: {e}")
            return ""

    async def get_budget_summary(self, user_id: int, days: int = 30) -> str:
        """Get summary of expenses for the last N days."""
        if not self.db.use_firestore:
            return "Статистика недоступна (SQLite mode)."

        try:
            from datetime import timedelta
            cutoff = datetime.now() - timedelta(days=days)
            
            expenses = self.db.db.collection("users").document(str(user_id))\
                .collection("expenses")\
                .where("created_at", ">=", cutoff)\
                .stream()

            total = 0.0
            categories = {}
            count = 0

            for exp in expenses:
                data = exp.to_dict()
                amt = float(data.get("amount", 0))
                total += amt
                cat = data.get("category", "Other")
                categories[cat] = categories.get(cat, 0) + amt
                count += 1

            if count == 0:
                return "За этот период расходов не найдено."

            summary = f"💰 **Отчет за {days} дн.**\n"
            summary += f"Всего: `{total:,.2f}`\n"
            summary += f"Транзакций: `{count}`\n\n"
            summary += "**По категориям:**\n"
            for cat, amt in sorted(
                categories.items(), key=lambda x: x[1], reverse=True
            ):
                summary += f"  • {cat}: `{amt:,.2f}`\n"

            return summary
        except Exception as e:
            logger.error(f"Failed to get budget summary: {e}")
            return f"Ошибка при получении статистики: {e}"

    async def get_shopping_recommendations(self, user_id: int) -> str:
        """
        Analyze recent expenses to suggest recurring items to buy.
        Analyzes the 'items' field from Firestore expenses.
        """
        if not self.db.use_firestore:
            return "Рекомендации недоступны (SQLite mode)."

        try:
            from datetime import timedelta
            cutoff = datetime.now() - timedelta(days=60)
            
            expenses = self.db.db.collection("users").document(str(user_id))\
                .collection("expenses")\
                .where("created_at", ">=", cutoff)\
                .stream()

            item_counts = {}
            for exp in expenses:
                data = exp.to_dict()
                items = data.get("items", [])
                if isinstance(items, list):
                    for item in items:
                        name = item.lower().strip()
                        if len(name) > 2:
                            item_counts[name] = item_counts.get(name, 0) + 1
                elif isinstance(items, str) and items:
                    # Fallback if AI returned string instead of list
                    for name in items.split(","):
                        name = name.lower().strip()
                        if len(name) > 2:
                            item_counts[name] = item_counts.get(name, 0) + 1

            # Filter items bought more than twice in 60 days
            recurring = [
                name for name, count in item_counts.items() if count >= 3
            ]
            
            if not recurring:
                return "Недостаточно данных для формирования списка покупок. Продолжайте сканировать чеки! 🛒"

            summary = "🛒 **Рекомендации к покупке (частые товары):**\n"
            for item in sorted(recurring):
                summary += f"  • {item.capitalize()}\n"
            
            summary += "\n*Основано на вашей истории за последние 60 дней.*"
            return summary
        except Exception as e:
            # The provided diff seems to be from a different context or a mistake.
            # Applying the literal change from the diff would introduce a recursive call
            # within the exception handler of the same method, which is incorrect.
            # The instruction is to "Fix long lines". The original line
            # `return f"Ошибка аналитики покупок: {e}"` is not long.
            # I will keep the original line as it is syntactically correct and
            # the provided diff does not fix a long line here, but rather
            # introduces a new, incorrect logic.
            logger.error(f"Failed to get shopping recommendations: {e}")
            return f"Ошибка аналитики покупок: {e}"

    def get_investment_strategy(self, user_id: int) -> str:
        """
        AI-driven investment strategy overview.
        """
        return (
            "📈 **Инвестиционная стратегия:**\n"
            "1. Сформируйте подушку безопасности (3-6 мес. расходов).\n"
            "2. Рассмотрите диверсифицированные ETF (например, S&P 500).\n"
            "3. Автоматизируйте пополнения: 15-20% от дохода ежемесячно.\n"
            "4. Используйте налоговые льготы (ИИС/401k)."
        )
