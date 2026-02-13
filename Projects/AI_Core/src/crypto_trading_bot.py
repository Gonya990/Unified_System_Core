#!/usr/bin/env python3
"""
Telegram Crypto Trading Bot - CONSERVATIVE STRATEGY
Безопасная торговля с защитой от потерь
"""

import asyncio
import logging
import os
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TelegramCryptoBot:
    """
    Conservative crypto trading bot for Telegram Wallet.

    SAFETY FEATURES:
    - Max 5% of balance per trade
    - Stop-loss at -3%
    - Take-profit at +5%
    - Only stable pairs (TON/USDT)
    - Notifications for every action
    """

    def __init__(self, telegram_token: str, chat_id: str):
        self.telegram_token = telegram_token
        self.chat_id = chat_id
        self.max_trade_percent = 0.05  # Max 5% per trade
        self.stop_loss_percent = 0.03  # Stop at -3%
        self.take_profit_percent = 0.05  # Take profit at +5%
        self.min_balance = 10  # Minimum $10 to trade

        # Trading state
        self.positions = {}
        self.balance = 0
        self.is_active = False

    async def notify(self, message: str):
        """Send Telegram notification."""
        try:
            import aiohttp

            url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
            payload = {"chat_id": self.chat_id, "text": f"🤖 Crypto Bot:\n{message}", "parse_mode": "Markdown"}

            async with aiohttp.ClientSession() as session:
                await session.post(url, json=payload)

            logger.info(f"Notification sent: {message}")
        except Exception as e:
            logger.error(f"Failed to send notification: {e}")

    async def get_balance(self) -> float:
        """
        Get Telegram Wallet balance.
        Note: This is a placeholder - actual implementation needs Telegram Wallet API.
        """
        # TODO: Integrate with Telegram Wallet API when available
        # For now, return simulated balance
        return 50.0  # $50 example

    async def get_price(self, pair: str = "TON/USDT") -> float:
        """Get current price from exchange."""
        try:
            import aiohttp

            # Using Binance API for price
            url = "https://api.binance.com/api/v3/ticker/price?symbol=TONUSDT"

            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return float(data["price"])

            return 0.0
        except Exception as e:
            logger.error(f"Failed to get price: {e}")
            return 0.0

    async def check_signal(self) -> Optional[str]:
        """
        Simple moving average strategy.
        Returns: 'BUY', 'SELL', or None
        """
        try:
            # Get historical prices (last 10 data points)
            import aiohttp

            url = "https://api.binance.com/api/v3/klines?symbol=TONUSDT&interval=5m&limit=10"

            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        prices = [float(k[4]) for k in data]  # Close prices

                        # Simple strategy: buy if last price < average, sell if >
                        avg = sum(prices) / len(prices)
                        current = prices[-1]

                        if current < avg * 0.98:  # 2% below average
                            return "BUY"
                        elif current > avg * 1.02:  # 2% above average
                            return "SELL"

            return None
        except Exception as e:
            logger.error(f"Signal check failed: {e}")
            return None

    async def execute_trade(self, action: str, amount: float):
        """
        Execute trade (BUY/SELL).
        Note: Placeholder - needs actual Telegram Wallet integration.
        """
        price = await self.get_price()

        if action == "BUY":
            self.positions["TON"] = {
                "amount": amount,
                "entry_price": price,
                "stop_loss": price * (1 - self.stop_loss_percent),
                "take_profit": price * (1 + self.take_profit_percent),
            }

            await self.notify(
                f"✅ **BOUGHT TON**\n"
                f"Amount: ${amount:.2f}\n"
                f"Price: ${price:.4f}\n"
                f"Stop-Loss: ${self.positions['TON']['stop_loss']:.4f}\n"
                f"Take-Profit: ${self.positions['TON']['take_profit']:.4f}"
            )

        elif action == "SELL" and "TON" in self.positions:
            entry = self.positions["TON"]["entry_price"]
            profit = (price - entry) / entry * 100

            await self.notify(f"💰 **SOLD TON**\nEntry: ${entry:.4f}\nExit: ${price:.4f}\nProfit: {profit:+.2f}%")

            del self.positions["TON"]

    async def check_stop_loss(self):
        """Check if stop-loss or take-profit hit."""
        if "TON" not in self.positions:
            return

        price = await self.get_price()
        pos = self.positions["TON"]

        # Stop-loss hit
        if price <= pos["stop_loss"]:
            await self.notify(f"🛑 **STOP-LOSS HIT** at ${price:.4f}")
            await self.execute_trade("SELL", 0)

        # Take-profit hit
        elif price >= pos["take_profit"]:
            await self.notify(f"🎯 **TAKE-PROFIT HIT** at ${price:.4f}")
            await self.execute_trade("SELL", 0)

    async def run(self):
        """Main trading loop."""
        await self.notify(
            "🚀 **Crypto Bot Started**\n"
            f"Max trade: {self.max_trade_percent * 100}% of balance\n"
            f"Stop-loss: {self.stop_loss_percent * 100}%\n"
            f"Take-profit: {self.take_profit_percent * 100}%\n"
            "Strategy: Conservative Moving Average"
        )

        self.is_active = True

        while self.is_active:
            try:
                # Get current balance
                self.balance = await self.get_balance()

                if self.balance < self.min_balance:
                    await self.notify(f"⚠️ Balance too low: ${self.balance:.2f}")
                    await asyncio.sleep(3600)  # Wait 1 hour
                    continue

                # Check stop-loss/take-profit
                await self.check_stop_loss()

                # Check for trading signal
                signal = await self.check_signal()

                if signal == "BUY" and "TON" not in self.positions:
                    trade_amount = self.balance * self.max_trade_percent
                    await self.execute_trade("BUY", trade_amount)

                elif signal == "SELL" and "TON" in self.positions:
                    await self.execute_trade("SELL", 0)

                # Wait 5 minutes before next check
                await asyncio.sleep(300)

            except Exception as e:
                logger.error(f"Trading loop error: {e}")
                await self.notify(f"❌ Error: {e}")
                await asyncio.sleep(60)

    async def stop(self):
        """Stop trading."""
        self.is_active = False
        await self.notify("🛑 **Crypto Bot Stopped**")


async def main():
    """Run the bot."""
    # Get credentials from environment
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("ADMIN_CHAT_ID")

    if not token or not chat_id:
        print("❌ Set TELEGRAM_BOT_TOKEN and ADMIN_CHAT_ID env vars")
        return

    bot = TelegramCryptoBot(token, chat_id)

    try:
        await bot.run()
    except KeyboardInterrupt:
        await bot.stop()


if __name__ == "__main__":
    asyncio.run(main())
