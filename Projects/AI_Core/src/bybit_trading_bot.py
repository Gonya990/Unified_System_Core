#!/usr/bin/env python3
"""
ByBit + Telegram Crypto Trading Bot
Реальная торговля с ОЧЕНЬ консервативной стратегией
"""

import argparse
import asyncio
import logging
import os
from typing import Optional

import aiohttp
from dotenv import load_dotenv

try:
    from pybit.unified_trading import HTTP
except ImportError:
    HTTP = None

import pandas as pd  # Data structuring

# Handle arguments
parser = argparse.ArgumentParser(description="ByBit Trading Bot")
parser.add_argument("--env", help="Path to .env file", default=".env")
args, unknown = parser.parse_known_args()

if os.path.exists(args.env):
    load_dotenv(args.env)
else:
    load_dotenv()

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class ByBitTradingBot:
    """
    ELITE QUANTUM Strategy for ByBit.
    
    STRATEGY (Triple Confirmation):
    1. Trend Filter: EMA 200 (Long only if price > EMA 200)
    2. Momentum: MACD Cross + RSI Entry
    3. Volatility: ATR-based Dynamic Stop Loss / Take Profit
    4. Risk Management: 10% of balance with strict SL
    """

    def __init__(
        self,
        api_key: str,
        api_secret: str,
        telegram_token: str,
        admin_chat_id: str,
        testnet: bool = False,
        monitor_only: bool = False,
    ):
        self.api_key = api_key
        self.api_secret = api_secret
        self.telegram_token = telegram_token
        self.admin_chat_id = admin_chat_id
        self.testnet = testnet
        self.monitor_only = monitor_only

        # Trading parameters (ELITE QUANTUM)
        self.max_trade_percent = 0.10
        self.atr_multiplier_sl = 2.0   # ATR-based volatility SL
        self.atr_multiplier_tp = 4.0   # 1:2 Risk/Reward ratio
        self.min_balance_usdt = 5.0
        self.min_order_value = 5.2

        self.symbols = ["TONUSDT", "ETHUSDT", "BTCUSDT", "SOLUSDT"]

        # State
        self.balance = 0
        self.positions = {}
        self.is_active = False
        self.trades_today = 0
        self.max_trades_per_day = 15
        self.last_notified_low_balance = None

        # Stats
        self.total_trades = 0
        self.winning_trades = 0
        self.total_profit = 0

    async def notify(self, message: str, urgent: bool = False):
        """Send Telegram notification."""
        try:
            emoji = "🔥" if urgent else "📈"
            text = f"{emoji} **ByBit PREMIUM BOT**\n\n{message}"

            url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
            payload = {
                "chat_id": self.admin_chat_id,
                "text": text,
                "parse_mode": "Markdown",
            }

            async with aiohttp.ClientSession() as session:
                await session.post(url, json=payload)

            logger.info(f"Notification: {message}")

        except Exception as e:
            logger.error(f"Notification failed: {e}")

    async def get_balance(self) -> float:
        """Get USDT balance from ByBit."""
        if not HTTP:
            return 0.0
        try:
            session = HTTP(testnet=self.testnet, api_key=self.api_key, api_secret=self.api_secret)
            result = session.get_wallet_balance(accountType="UNIFIED", coin="USDT")
            if result["retCode"] == 0:
                balance = float(result["result"]["list"][0]["coin"][0]["walletBalance"])
                return balance
            return 0.0
        except Exception as e:
            logger.error(f"Balance check error: {e}")
            return 0.0

    async def get_price(self, symbol: str) -> float:
        """Get current market price."""
        if not HTTP: return 0.0
        try:
            session = HTTP(testnet=self.testnet)
            result = session.get_tickers(category="spot", symbol=symbol)
            if result["retCode"] == 0:
                return float(result["result"]["list"][0]["lastPrice"])
            return 0.0
        except Exception as e:
            logger.error(f"Price error for {symbol}: {e}")
            return 0.0

    def _calculate_indicators(self, data: list[float]):
        """Quantum indicator engine."""
        prices = pd.Series(data)

        # RSI
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))

        # EMA
        ema_20 = prices.ewm(span=20, adjust=False).mean()
        ema_200 = prices.ewm(span=200, adjust=False).mean()

        # MACD
        ema_12 = prices.ewm(span=12, adjust=False).mean()
        ema_26 = prices.ewm(span=26, adjust=False).mean()
        macd = ema_12 - ema_26
        signal_line = macd.ewm(span=9, adjust=False).mean()

        # ATR (Volatility)
        # Using a simplified high-low approximation if only closes are provided,
        # but here we'll use price fluctuations
        atr = prices.diff().abs().rolling(window=14).mean()

        return rsi.iloc[-1], ema_20.iloc[-1], ema_200.iloc[-1], macd.iloc[-1], signal_line.iloc[-1], atr.iloc[-1]

    async def analyze_market(self, symbol: str) -> Optional[dict]:
        """Elite multi-indicator analysis."""
        if not HTTP: return None
        try:
            session = HTTP(testnet=self.testnet)
            # 1h candles
            result = session.get_kline(category="spot", symbol=symbol, interval="60", limit=250)
            if result["retCode"] != 0: return None

            closes = [float(k[4]) for k in result["result"]["list"]]
            rsi, ema20, ema200, macd, macd_sig, atr = self._calculate_indicators(closes)
            current_price = closes[-1]

            logger.info(f"[{symbol}] P: {current_price:.2f} | RSI: {rsi:.1f} | EMA200: {ema200:.2f} | MACD: {macd:.2f} | ATR: {atr:.4f}")

            # BUY CONDITION:
            # 1. Price above EMA 200 (Long trend)
            # 2. RSI < 40 (Oversold in trend)
            # 3. MACD Golden Cross (Momentum)
            if current_price > ema200 and rsi < 45 and macd > macd_sig:
                return {"signal": "BUY", "atr": atr}

            # SELL CONDITION:
            if rsi > 70 or (macd < macd_sig and current_price < ema20):
                return {"signal": "SELL", "atr": atr}

            return None
        except Exception as e:
            logger.error(f"Analysis error: {e}")
            return None

    async def place_order(self, symbol: str, side: str, quantity: float) -> bool:
        """Place market order."""
        if self.monitor_only:
            logger.info(f"[MONITOR] {side} {quantity} {symbol}")
            return True
        try:
            session = HTTP(testnet=self.testnet, api_key=self.api_key, api_secret=self.api_secret)
            # Find decimal precision for symbol (general hack for most major coins)
            precision = 4 if "TON" in symbol else 5
            if "BTC" in symbol: precision = 5
            formatted_qty = f"{quantity:.{precision}f}".rstrip('0').rstrip('.')

            kwargs = {
                "category": "spot",
                "symbol": symbol,
                "side": side,
                "orderType": "Market",
                "qty": formatted_qty,
            }
            if side == "Buy": kwargs["marketUnit"] = "baseCoin"

            result = session.place_order(**kwargs)
            if result["retCode"] == 0:
                await self.notify(f"🚀 **{side} EXECUTED**\nSymbol: {symbol}\nQty: {formatted_qty}")
                return True
            else:
                logger.error(f"Order failed: {result['retMsg']}")
                return False
        except Exception as e:
            logger.error(f"Order error: {e}")
            return False

    async def execute_trade(self, signal_data: dict, symbol: str):
        """Execute elite trade logic."""
        price = await self.get_price(symbol)
        if not price: return

        signal = signal_data["signal"]
        atr = signal_data["atr"]

        if signal == "BUY" and symbol not in self.positions:
            amount = max(self.balance * self.max_trade_percent, self.min_order_value)
            if amount > self.balance: return

            qty = round(amount / price, 4)
            if await self.place_order(symbol, "Buy", qty):
                self.positions[symbol] = {
                    "entry_price": price,
                    "qty": qty,
                    "stop_loss": price - (atr * self.atr_multiplier_sl),
                    "take_profit": price + (atr * self.atr_multiplier_tp)
                }
                self.trades_today += 1
                self.total_trades += 1
                await self.notify(f"🟢 **ELITE LONG OPENED**\n{symbol} @ {price}\nSL (ATR): {self.positions[symbol]['stop_loss']:.4f}\nTP (ATR): {self.positions[symbol]['take_profit']:.4f}")

        elif signal == "SELL" and symbol in self.positions:
            qty = self.positions[symbol]["qty"]
            if await self.place_order(symbol, "Sell", qty):
                profit = (price - self.positions[symbol]["entry_price"]) / self.positions[symbol]["entry_price"] * 100
                self.total_profit += (price - self.positions[symbol]["entry_price"]) * qty
                if profit > 0: self.winning_trades += 1
                await self.notify(f"🔴 **ELITE POSITION CLOSED**\n{symbol} @ {price}\nProfit: {profit:+.2f}%")
                del self.positions[symbol]

    async def check_risk(self):
        """Emergency checks for SL/TP."""
        for sym, pos in list(self.positions.items()):
            price = await self.get_price(sym)
            if not price: continue
            if price <= pos["stop_loss"]:
                await self.notify(f"🛑 **STOP LOSS HIT** on {sym}")
                await self.execute_trade("SELL", sym)
            elif price >= pos["take_profit"]:
                await self.notify(f"🎯 **TAKE PROFIT HIT** on {sym}")
                await self.execute_trade("SELL", sym)

    async def run(self):
        """Elite Main Loop."""
        await self.notify(f"👑 **ELITE QUANTUM BOT STARTING**\nMode: {'LIVE 🚀' if not self.testnet else 'TEST 🛡️'}\nEquity: ${self.balance:.2f}")
        self.is_active = True
        while self.is_active:
            try:
                self.balance = await self.get_balance()
                await self.check_risk()
                for sym in self.symbols:
                    if sym not in self.positions and self.trades_today < self.max_trades_per_day:
                        signal_data = await self.analyze_market(sym)
                        if signal_data and signal_data["signal"] == "BUY":
                            await self.execute_trade(signal_data, sym)
                await asyncio.sleep(60)
            except Exception as e:
                logger.error(f"Loop error: {e}")
                await asyncio.sleep(60)

async def main():
    load_dotenv(args.env if os.path.exists(args.env) else "Projects/AI_Core/.env")
    bot = ByBitTradingBot(
        api_key=os.getenv("BYBIT_API_KEY"),
        api_secret=os.getenv("BYBIT_API_SECRET"),
        telegram_token=os.getenv("TELEGRAM_BOT_TOKEN"),
        admin_chat_id=os.getenv("ADMIN_CHAT_ID", "708531393"),
        testnet=os.getenv("BYBIT_TESTNET", "false").lower() == "true", # LIVE DEFAULT
        monitor_only=os.getenv("BYBIT_MONITOR_ONLY", "false").lower() == "true" # TRADING DEFAULT
    )
    await bot.run()

if __name__ == "__main__":
    asyncio.run(main())

