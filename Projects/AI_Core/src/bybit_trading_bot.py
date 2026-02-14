#!/usr/bin/env python3
"""
ByBit + Telegram Crypto Trading Bot
Реальная торговля с ОЧЕНЬ консервативной стратегией
"""

import argparse
import asyncio
import logging
import os
from datetime import datetime
from typing import Optional

import aiohttp
from dotenv import load_dotenv

try:
    from pybit.unified_trading import HTTP
except ImportError:
    HTTP = None

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
    PREMIUM PROFIT Strategy for ByBit.
    
    STRATEGY:
    - Multi-indicator: RSI + Bollinger Bands + SMA Trend Filter
    - Confirmations: Entry on Lower BB touch + RSI oversold (<35)
    - Trend Protection: Only trade in the direction of the 1h SMA(50)
    - Risk Management: 10% of balance (optimized for small accounts)
    - Coins: TON, ETH, BTC, SOL
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

        # Trading parameters (PREMIUM AGGRESSIVE)
        self.max_trade_percent = 0.10  # 10% to make real gains on small balance
        self.stop_loss_percent = 0.025  # -2.5% stop
        self.take_profit_percent = 0.05  # +5% target
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
        """Calculate RSI, SMA and Bollinger Bands."""
        import numpy as np
        prices = np.array(data)
        
        # RSI
        deltas = np.diff(prices)
        seed = deltas[:14]
        up = seed[seed >= 0].sum() / 14
        down = -seed[seed < 0].sum() / 14
        rs = up / (down if down != 0 else 0.001)
        rsi = 100. - (100. / (1. + rs))
        
        # SMA
        sma_20 = np.mean(prices[-20:])
        sma_50 = np.mean(prices[-50:])
        
        # BB
        std = np.std(prices[-20:])
        upper_bb = sma_20 + (2 * std)
        lower_bb = sma_20 - (2 * std)
        
        return rsi, sma_20, sma_50, upper_bb, lower_bb

    async def analyze_market(self, symbol: str) -> Optional[str]:
        """Premium multi-indicator analysis."""
        if not HTTP: return None
        try:
            session = HTTP(testnet=self.testnet)
            # 1h candles
            result = session.get_kline(category="spot", symbol=symbol, interval="60", limit=100)
            if result["retCode"] != 0: return None
            
            closes = [float(k[4]) for k in result["result"]["list"]]
            rsi, sma20, sma50, upper, lower = self._calculate_indicators(closes)
            current_price = closes[-1]

            logger.info(f"[{symbol}] Price: {current_price:.4f} | RSI: {rsi:.1f} | BB: L={lower:.4f} U={upper:.4f} | Trend: {sma50:.4f}")

            # BUY CONDITION: RSI Oversold AND Touching Lower BB AND Trend is generally UP (Price > SMA50)
            if rsi < 35 and current_price <= lower * 1.005 and current_price > sma50 * 0.95:
                # Strong buy zone
                return "BUY"

            # SELL CONDITION: RSI Overbought OR Touching Upper BB
            if rsi > 65 or current_price >= upper * 0.995:
                return "SELL"

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

    async def execute_trade(self, signal: str, symbol: str):
        """Execute trade logic."""
        price = await self.get_price(symbol)
        if not price: return

        if signal == "BUY" and symbol not in self.positions:
            amount = max(self.balance * self.max_trade_percent, self.min_order_value)
            if amount > self.balance: return
            
            qty = round(amount / price, 4)
            if await self.place_order(symbol, "Buy", qty):
                self.positions[symbol] = {
                    "entry_price": price,
                    "qty": qty,
                    "stop_loss": price * (1 - self.stop_loss_percent),
                    "take_profit": price * (1 + self.take_profit_percent)
                }
                self.trades_today += 1
                self.total_trades += 1
                await self.notify(f"🟢 **LONG OPENED**\n{symbol} @ {price}\nSL: {self.positions[symbol]['stop_loss']:.4f}\nTP: {self.positions[symbol]['take_profit']:.4f}")

        elif signal == "SELL" and symbol in self.positions:
            qty = self.positions[symbol]["qty"]
            if await self.place_order(symbol, "Sell", qty):
                profit = (price - self.positions[symbol]["entry_price"]) / self.positions[symbol]["entry_price"] * 100
                self.total_profit += (price - self.positions[symbol]["entry_price"]) * qty
                if profit > 0: self.winning_trades += 1
                await self.notify(f"🔴 **POSITION CLOSED**\n{symbol} @ {price}\nProfit: {profit:+.2f}%")
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
        """Main Loop."""
        await self.notify(f"👑 **PREMIUM CRYPTO BOT STARTING**\nMode: {'LIVE 🚀' if not self.testnet else 'TEST 🛡️'}\nEquity: ${self.balance:.2f}\nPairs: {', '.join(self.symbols)}")
        self.is_active = True
        while self.is_active:
            try:
                self.balance = await self.get_balance()
                await self.check_risk()
                for sym in self.symbols:
                    if sym not in self.positions and self.trades_today < self.max_trades_per_day:
                        signal = await self.analyze_market(sym)
                        if signal == "BUY": await self.execute_trade(signal, sym)
                await asyncio.sleep(60) # High frequency scanning
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

