#!/usr/bin/env python3
"""
Financial Tracker - Gmail Payment Parser
Парсит квитанции из Gmail и создаёт финансовый отчёт
"""

import re
from datetime import datetime


class PaymentParser:
    """Парсер платежей из email."""

    SERVICES = {
        "suno": {"name": "Suno AI", "category": "AI Services"},
        "elevenlabs": {"name": "ElevenLabs", "category": "AI Services"},
        "runway": {"name": "Runway ML", "category": "AI Services"},
        "luma": {"name": "Luma Labs", "category": "AI Services"},
        "openai": {"name": "OpenAI", "category": "AI Services"},
        "anthropic": {"name": "Anthropic Claude", "category": "AI Services"},
        "google": {"name": "Google Cloud", "category": "Cloud"},
        "stripe": {"name": "Stripe", "category": "Payment"},
        "paypal": {"name": "PayPal", "category": "Payment"},
    }

    def parse_amount(self, text: str) -> float:
        """Extract amount from text."""
        # Try different patterns
        patterns = [
            r"\$(\d+\.?\d*)",
            r"(\d+\.?\d*)\s*USD",
            r"Total:\s*\$?(\d+\.?\d*)",
            r"Amount:\s*\$?(\d+\.?\d*)",
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return float(match.group(1))

        return 0.0

    def detect_service(self, subject: str, sender: str) -> dict:
        """Detect service from email."""
        text = f"{subject} {sender}".lower()

        for key, service in self.SERVICES.items():
            if key in text:
                return service

        return {"name": "Unknown", "category": "Other"}

    def parse_emails(self, emails: list[dict]) -> list[dict]:
        """Parse payment emails into structured data."""
        payments = []

        for email in emails:
            service = self.detect_service(email.get("subject", ""), email.get("sender", ""))

            amount = self.parse_amount(email.get("body", "") + email.get("subject", ""))

            payment = {
                "date": email.get("date"),
                "service": service["name"],
                "category": service["category"],
                "amount": amount,
                "subject": email.get("subject"),
                "sender": email.get("sender"),
            }

            payments.append(payment)

        return payments

    def generate_report(self, payments: list[dict]) -> str:
        """Generate financial report."""
        total = sum(p["amount"] for p in payments)

        by_category = {}
        for p in payments:
            cat = p["category"]
            if cat not in by_category:
                by_category[cat] = {"total": 0, "count": 0, "items": []}

            by_category[cat]["total"] += p["amount"]
            by_category[cat]["count"] += 1
            by_category[cat]["items"].append(p)

        report = "# 💰 FINANCIAL REPORT\\n\\n"
        report += f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\\n"
        report += f"**Total Payments:** ${total:.2f}\\n\\n"
        report += "---\\n\\n"

        report += "## По категориям:\\n\\n"
        for cat, data in sorted(by_category.items()):
            report += f"### {cat}: ${data['total']:.2f} ({data['count']} платежей)\\n\\n"

            for item in data["items"]:
                report += f"- **{item['service']}**: ${item['amount']:.2f}\\n"
                report += f"  - {item['date']}\\n"
                report += f"  - {item['subject'][:60]}...\\n\\n"

        return report


if __name__ == "__main__":
    # Test
    parser = PaymentParser()

    test_emails = [
        {
            "subject": "Suno Pro Subscription - Invoice #12345",
            "sender": "billing@suno.ai",
            "body": "Thank you for your subscription. Total: $10.00",
            "date": "2026-02-01",
        },
        {
            "subject": "ElevenLabs Payment Confirmation",
            "sender": "no-reply@elevenlabs.io",
            "body": "Payment of $5.00 received",
            "date": "2026-02-01",
        },
    ]

    payments = parser.parse_emails(test_emails)
    report = parser.generate_report(payments)

    print(report)
