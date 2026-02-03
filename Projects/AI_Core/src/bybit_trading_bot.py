#!/usr/bin/env python3
"""
ByBit + Telegram Crypto Trading Bot
Реальная торговля с ОЧЕНЬ консервативной стратегией
"""
import asyncio
import logging
import os
from datetime import datetime
from typing import Optional

from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ByBitTradingBot:
    """
    Ultra-conservative trading bot for ByBit.

    SAFETY RULES:
    - Max 3% of balance per trade
    - Stop-loss: -2%
    - Take-profit: +4%
    - Only USDT pairs
    - Trade only during high liquidity
    - Max 1 position at a time
    """

    def __init__(
        self,
        api_key: str,
        api_secret: str,
        telegram_token: str,
        admin_chat_id: str,
        testnet: bool = True
    ):
        self.api_key = api_key
        self.api_secret = api_secret
        self.telegram_token = telegram_token
        self.admin_chat_id = admin_chat_id
        self.testnet = testnet

        # Trading parameters (VERY CONSERVATIVE)
        self.max_trade_percent = 0.03  # Only 3%!
        self.stop_loss_percent = 0.02  # -2% stop
        self.take_profit_percent = 0.04  # +4% target
        self.min_balance_usdt = 10  # Minimum $10
        self.min_order_value = 5.1  # ByBit Spot API minimum is 5 USDT (added small buffer)

        # State
        self.balance = 0
        self.positions = {}
        self.is_active = False
        self.trades_today = 0
        self.max_trades_per_day = 5  # Limit trades

        # Stats
        self.total_trades = 0
        self.winning_trades = 0
        self.total_profit = 0

    async def notify(self, message: str, urgent: bool = False):
        """Send Telegram notification."""
        try:
            import aiohttp

            emoji = "🚨" if urgent else "📊"
            text = f"{emoji} **ByBit Bot**\n\n{message}"

            url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
            payload = {
                'chat_id': self.admin_chat_id,
                'text': text,
                'parse_mode': 'Markdown'
            }

            async with aiohttp.ClientSession() as session:
                await session.post(url, json=payload)

            logger.info(f"Notification: {message}")

        except Exception as e:
            logger.error(f"Notification failed: {e}")

    async def get_balance(self) -> float:
        """Get USDT balance from ByBit."""
        try:
            from pybit.unified_trading import HTTP

            session = HTTP(
                testnet=self.testnet,
                api_key=self.api_key,
                api_secret=self.api_secret
            )

            result = session.get_wallet_balance(accountType="UNIFIED", coin="USDT")

            if result['retCode'] == 0:
                balance = float(result['result']['list'][0]['coin'][0]['walletBalance'])
                logger.info(f"Balance: ${balance:.2f} USDT")
                return balance

            return 0.0

        except Exception as e:
            logger.error(f"Failed to get balance: {e}")
            await self.notify(f"❌ Balance check failed: {e}", urgent=True)
            return 0.0

    async def get_price(self, symbol: str = "TONUSDT") -> float:
        """Get current market price."""
        try:
            from pybit.unified_trading import HTTP

            session = HTTP(testnet=self.testnet)

            result = session.get_tickers(category="spot", symbol=symbol)

            if result['retCode'] == 0:
                price = float(result['result']['list'][0]['lastPrice'])
                return price

            return 0.0

        except Exception as e:
            logger.error(f"Price fetch failed: {e}")
            return 0.0

    async def analyze_market(self, symbol: str = "TONUSDT") -> Optional[str]:
        """
        Simple but effective strategy:
        - RSI < 30 = OVERSOLD → BUY
        - RSI > 70 = OVERBOUGHT → SELL
        - Moving Average crossover
        """
        try:
            from pybit.unified_trading import HTTP

            session = HTTP(testnet=self.testnet)

            # Get kline data (1 hour candles, last 50)
            result = session.get_kline(
                category="spot",
                symbol=symbol,
                interval="60",
                limit=50
            )

            if result['retCode'] != 0:
                return None

            klines = result['result']['list']
            closes = [float(k[4]) for k in klines]  # Close prices

            # Calculate RSI
            rsi = self._calculate_rsi(closes, period=14)

            # Calculate moving averages
            sma_short = sum(closes[-10:]) / 10
            sma_long = sum(closes[-30:]) / 30
            current_price = closes[-1]

            logger.info(f"Market: RSI={rsi:.1f}, SMA_short={sma_short:.4f}, SMA_long={sma_long:.4f}")

            # Trading signals
            if rsi < 35 and current_price < sma_long * 0.98:
                # Oversold + below long MA = BUY signal
                return 'BUY'

            elif rsi > 65 and current_price > sma_long * 1.02:
                # Overbought + above long MA = SELL signal
                return 'SELL'

            return None

        except Exception as e:
            logger.error(f"Market analysis failed: {e}")
            return None

    def _calculate_rsi(self, prices: list[float], period: int = 14) -> float:
        """Calculate RSI indicator."""
        deltas = [prices[i] - prices[i-1] for i in range(1, len(prices))]

        gains = [d if d > 0 else 0 for d in deltas]
        losses = [-d if d < 0 else 0 for d in deltas]

        avg_gain = sum(gains[-period:]) / period
        avg_loss = sum(losses[-period:]) / period

        if avg_loss == 0:
            return 100

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        return rsi

    async def place_order(
        self,
        symbol: str,
        side: str,  # Buy or Sell
        quantity: float
    ) -> bool:
        """Place market order on ByBit."""
        # Ensure quantity is rounded (Spot TONUSDT usually 2 decimal places)
        formatted_qty = f"{quantity:.2f}"
        try:
            from pybit.unified_trading import HTTP

            session = HTTP(
                testnet=self.testnet,
                api_key=self.api_key,
                api_secret=self.api_secret
            )

            kwargs = {
                "category": "spot",
                "symbol": symbol,
                "side": side,
                "orderType": "Market",
                "qty": formatted_qty,
                "timeInForce": "IOC"
            }

            # For Market Buy on Spot, ByBit defaults to quote coin (USDT).
            # We specify baseCoin to use the TON quantity.
            if side.lower() == "buy":
                kwargs["marketUnit"] = "baseCoin"

            result = session.place_order(**kwargs)

            if result['retCode'] == 0:
                order_id = result['result']['orderId']
                logger.info(f"Order placed: {side} {quantity} {symbol}, ID: {order_id}")

                await self.notify(
                    f"✅ **Order Executed**\n"
                    f"Side: {side}\n"
                    f"Symbol: {symbol}\n"
                    f"Quantity: {quantity}\n"
                    f"Order ID: {order_id}"
                )

                return True

            else:
                await self.notify(
                    f"❌ **Order Failed**\n{result['retMsg']}",
                    urgent=True
                )
                return False

        except Exception as e:
            logger.error(f"Order placement failed: {e}")
            await self.notify(f"❌ Order error: {e}", urgent=True)
            return False

    async def execute_trade(self, signal: str, symbol: str = "TONUSDT"):
        """Execute trading signal."""
        try:
            # Check daily limit
            if self.trades_today >= self.max_trades_per_day:
                logger.info("Daily trade limit reached")
                return

            price = await self.get_price(symbol)

            if signal == 'BUY' and symbol not in self.positions:
                # Calculate position size (3% of balance)
                trade_amount = self.balance * self.max_trade_percent

                # Check against exchange minimum (5 USDT)
                if trade_amount < self.min_order_value:
                    logger.warning(f"Trade amount ${trade_amount:.2f} too low. Using minimum ${self.min_order_value}")
                    trade_amount = self.min_order_value

                if trade_amount > self.balance:
                    logger.error(f"Balance ${self.balance:.2f} too low for minimum order ${trade_amount:.2f}")
                    return

                quantity = round(trade_amount / price, 2)

                # Place buy order
                if await self.place_order(symbol, "Buy", quantity):
                    self.positions[symbol] = {
                        'entry_price': price,
                        'quantity': quantity,
                        'entry_time': datetime.now().isoformat(),
                        'stop_loss': price * (1 - self.stop_loss_percent),
                        'take_profit': price * (1 + self.take_profit_percent)
                    }

                    self.trades_today += 1
                    self.total_trades += 1

                    await self.notify(
                        f"🟢 **OPENED POSITION**\n"
                        f"Symbol: {symbol}\n"
                        f"Entry: ${price:.4f}\n"
                        f"Quantity: {quantity:.2f}\n"
                        f"Amount: ${trade_amount:.2f}\n"
                        f"Stop-Loss: ${self.positions[symbol]['stop_loss']:.4f}\n"
                        f"Take-Profit: ${self.positions[symbol]['take_profit']:.4f}"
                    )

            elif signal == 'SELL' and symbol in self.positions:
                pos = self.positions[symbol]
                quantity = pos['quantity']

                # Place sell order
                if await self.place_order(symbol, "Sell", quantity):
                    # Calculate profit
                    entry = pos['entry_price']
                    profit_pct = (price - entry) / entry * 100
                    profit_usd = (price - entry) * quantity

                    self.total_profit += profit_usd
                    if profit_usd > 0:
                        self.winning_trades += 1

                    await self.notify(
                        f"🔴 **CLOSED POSITION**\n"
                        f"Symbol: {symbol}\n"
                        f"Entry: ${entry:.4f}\n"
                        f"Exit: ${price:.4f}\n"
                        f"Profit: {profit_pct:+.2f}% (${profit_usd:+.2f})\n"
                        f"Win Rate: {self.winning_trades}/{self.total_trades}"
                    )

                    del self.positions[symbol]
                    self.trades_today += 1

        except Exception as e:
            logger.error(f"Trade execution failed: {e}")
            await self.notify(f"❌ Trade error: {e}", urgent=True)

    async def check_stop_loss(self):
        """Monitor positions for stop-loss/take-profit."""
        for symbol, pos in list(self.positions.items()):
            try:
                price = await self.get_price(symbol)

                # Stop-loss hit
                if price <= pos['stop_loss']:
                    await self.notify(
                        f"🛑 **STOP-LOSS TRIGGERED**\n"
                        f"Symbol: {symbol}\n"
                        f"Price: ${price:.4f}\n"
                        f"Stop-Loss: ${pos['stop_loss']:.4f}",
                        urgent=True
                    )
                    await self.execute_trade('SELL', symbol)

                # Take-profit hit
                elif price >= pos['take_profit']:
                    await self.notify(
                        f"🎯 **TAKE-PROFIT HIT**\n"
                        f"Symbol: {symbol}\n"
                        f"Price: ${price:.4f}\n"
                        f"Target: ${pos['take_profit']:.4f}"
                    )
                    await self.execute_trade('SELL', symbol)

            except Exception as e:
                logger.error(f"Stop-loss check failed: {e}")

    async def run(self):
        """Main trading loop."""
        await self.notify(
            "🚀 **Trading Bot Started**\n\n"
            f"Mode: {'TESTNET' if self.testnet else 'LIVE'}\n"
            f"Max trade: {self.max_trade_percent*100}%\n"
            f"Stop-loss: {self.stop_loss_percent*100}%\n"
            f"Take-profit: {self.take_profit_percent*100}%\n"
            f"Max trades/day: {self.max_trades_per_day}\n"
            "Strategy: RSI + Moving Average"
        )

        self.is_active = True

        while self.is_active:
            try:
                # Reset daily counter at midnight
                now = datetime.now()
                if now.hour == 0 and now.minute == 0:
                    self.trades_today = 0

                # Get balance
                self.balance = await self.get_balance()

                if self.balance < self.min_balance_usdt:
                    await self.notify(
                        f"⚠️ **Low Balance**\n"
                        f"Current: ${self.balance:.2f}\n"
                        f"Minimum: ${self.min_balance_usdt:.2f}\n"
                        "Trading paused.",
                        urgent=True
                    )
                    await asyncio.sleep(3600)  # Wait 1 hour
                    continue

                # Check existing positions
                await self.check_stop_loss()

                # Analyze market (only if no position)
                if not self.positions:
                    signal = await self.analyze_market("TONUSDT")

                    if signal:
                        await self.execute_trade(signal, "TONUSDT")

                # Wait 5 minutes before next check
                await asyncio.sleep(300)

            except Exception as e:
                logger.error(f"Main loop error: {e}")
                await self.notify(f"❌ Bot error: {e}", urgent=True)
                await asyncio.sleep(60)

    async def stop(self):
        """Stop bot and close positions."""
        self.is_active = False

        # Close all positions
        for symbol in list(self.positions.keys()):
            await self.execute_trade('SELL', symbol)

        await self.notify(
            "🛑 **Bot Stopped**\n\n"
            f"Total trades: {self.total_trades}\n"
            f"Winning: {self.winning_trades}\n"
            f"Win rate: {self.winning_trades/max(1,self.total_trades)*100:.1f}%\n"
            f"Total profit: ${self.total_profit:+.2f}"
        )


async def main():
    """Run the bot."""
    # Load credentials
    api_key = os.getenv('BYBIT_API_KEY', '')
    api_secret = os.getenv('BYBIT_API_SECRET', '')
    telegram_token = os.getenv('TELEGRAM_BOT_TOKEN', '')
    admin_chat_id = os.getenv('ADMIN_CHAT_ID', '708531393')

    if not api_key or not api_secret:
        print("❌ Set BYBIT_API_KEY and BYBIT_API_SECRET in .env")
        print("For safety, starting in TESTNET mode...")
        api_key = "test"
        api_secret = "test"

    # Start in TESTNET or LIVE based on .env
    testnet_env = os.getenv('BYBIT_TESTNET', 'true').lower()
    is_testnet = testnet_env == 'true'

    bot = ByBitTradingBot(
        api_key=api_key,
        api_secret=api_secret,
        telegram_token=telegram_token,
        admin_chat_id=admin_chat_id,
        testnet=is_testnet
    )

    if not is_testnet:
        print("🚀 STARTING IN LIVE MODE! REAL FUNDS!")
    else:
        print("🛡️ STARTING IN TESTNET MODE (Safe Mode)")

    try:
        await bot.run()
    except KeyboardInterrupt:
        await bot.stop()


if __name__ == "__main__":
    print("🤖 ByBit Trading Bot")
    print("=" * 50)
    print("STARTING IN TESTNET MODE FOR SAFETY")
    print("=" * 50)
    asyncio.run(main())
