import asyncio
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

import ccxt
from common.messaging import RedisStreamManager
from common.token_broker import TokenBroker

# Add project root to path for common imports
ROOT = Path(__file__).resolve().parent.parent.parent
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

# AI / ML imports
try:
    import numpy as np
    from sklearn.linear_model import LinearRegression
except ImportError:
    np = None
    LinearRegression = None

# Logging for DAC8
log_fmt = "%(asctime)s [%(levelname)s] %(message)s"
logging.basicConfig(level=logging.INFO, format=log_fmt)
logger = logging.getLogger("BybitArbAlpha")


class FundingArbStrategy:
    """
    Ведущий архитектор: Antigravity (Senior Quant)
    Стратегия: Delta Neutral Funding Arbitrage (Cash & Carry)
    Биржа: Bybit Unified Trading Account (UTA)
    """

    def __init__(self, symbol="BTC/USDT", target_apr=0.12, leverage=1.0):
        self.broker = TokenBroker()
        # Fallback to env if not in broker
        api_key = os.getenv("BYBIT_API_KEY")
        api_secret = os.getenv("BYBIT_API_SECRET")
        if not api_key or not api_secret:
            logger.error("Missing BYBIT_API_KEY/BYBIT_API_SECRET. Set env vars or mount k8s secret 'bybit-secrets'.")
            raise RuntimeError("Bybit API credentials are required")

        self.exchange = ccxt.bybit(
            {
                "apiKey": api_key,
                "secret": api_secret,
                "enableRateLimit": True,
            }
        )
        self.symbol = symbol
        self.target_apr = target_apr
        self.leverage = leverage
        self.is_active = False
        self.history = []  # For ML features
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        self.messenger = RedisStreamManager(redis_url)

        # Институциональные комиссии Bybit (Maker/ Taker)
        self.fees = {"spot_taker": 0.001, "perp_taker": 0.00055, "perp_maker": 0.0002}

    async def get_market_state(self):
        """Сбор данных L2 + Funding Rate с проверкой на устаревание"""
        try:
            perp_symbol = f"{self.symbol}:USDT"

            ticker_task = asyncio.create_task(self.exchange.fetch_ticker(self.symbol))
            perp_task = asyncio.create_task(self.exchange.fetch_ticker(perp_symbol))
            funding_task = asyncio.create_task(self.exchange.fetch_funding_rate(perp_symbol))
            # Parallel gathering
            res = await asyncio.gather(ticker_task, perp_task, funding_task)
            spot, perp, funding = res

            # Проверка на "грязные данные" (Data Staleness)
            latency = (datetime.now().timestamp() * 1000) - spot["timestamp"]
            if latency > 1000:  # Более 1 секунды задержки
                logger.warning(f"⚠️ Данные устарели! Latency: {latency:.2f}ms")
                return None

            return {
                "spot_ask": spot["ask"],
                "perp_bid": perp["bid"],
                "funding_rate": funding["fundingRate"],
                "latency_ms": latency,
                "timestamp": spot["timestamp"],
            }
        except Exception as e:
            logger.error(f"❌ Ошибка сбора данных: {e}")
            return None

    def _predict_funding_volatility(self):
        """AI-компонент: Прогноз изменения ставки финансирования"""
        if not LinearRegression or len(self.history) < 10:
            return 0  # Neutral

        # Подготовка данных для регрессии
        X = np.array(range(len(self.history))).reshape(-1, 1)
        y = np.array([h["funding_rate"] for h in self.history])

        model = LinearRegression().fit(X, y)
        prediction = model.predict([[len(self.history) + 1]])[0]
        return prediction

    def calculate_metrics(self, state):
        """Расчет экономической целесообразности сделки"""
        spot_price = state["spot_ask"]
        perp_price = state["perp_bid"]
        fr = state["funding_rate"]

        # 1. Стоимость входа (Entry Cost)
        entry_fees = (spot_price * self.fees["spot_taker"]) + (perp_price * self.fees["perp_taker"])

        # 2. Ожидаемая годовая доходность (APR)
        # Фандинг каждые 8 часов (3 раза в день)
        daily_yield = fr * 3
        annual_yield = daily_yield * 365

        # 3. Точка безубыточности (Break-even days)
        # Учитываем комиссию на вход и выход (2x)
        total_cycle_fees = entry_fees * 2
        denom = spot_price * daily_yield
        denom = denom if denom != 0 else 0.0001
        days_to_be = total_cycle_fees / denom if daily_yield > 0 else float("inf")

        # 4. ML Overlay: Оптимизация точки входа
        predicted_fr = self._predict_funding_volatility()
        ml_score = 1.1 if predicted_fr > fr else 0.9  # Усиление если фандинг растет

        is_profitable = (annual_yield * ml_score >= self.target_apr) and (days_to_be < 14)

        return {"apr": annual_yield, "days_to_be": days_to_be, "is_profitable": is_profitable, "ml_score": ml_score}

    async def run(self, amount):
        logger.info(f"Alpha Engine started: {self.symbol}. Listening...")
        stream = "market_data"
        group = "alpha-group"
        async for _msg_id, state in self.messenger.consume(stream, group, "alpha-1"):
            # Update history for ML
            self.history.append(state)
            if len(self.history) > 100:
                self.history.pop(0)

            # Log periodically to show heartbeat
            if not hasattr(self, '_msg_count'): self._msg_count = 0
            self._msg_count += 1
            if self._msg_count % 10 == 0:
                logger.info(
                    f"💹 {self.symbol} Update | FR: {state['funding_rate']:.4%} | "
                    f"APR: {metrics['apr']:.2%} | Healthy: {'✅' if metrics['is_profitable'] else '⏳'}"
                )

            if metrics["is_profitable"] and not self.is_active:
                logger.info("🚀 SIGNAL: Opening position.")
                signal = {
                    "symbol": self.symbol,
                    "side": "SELL",
                    "amount": amount,
                    "leverage": self.leverage,
                    "price": state["perp_bid"],
                    "action": "OPEN",
                }
                await self.messenger.produce("signals", signal)
                self.is_active = True
            elif not metrics["is_profitable"] and self.is_active:
                logger.info("📉 SIGNAL: Closing position.")
                signal = {
                    "symbol": self.symbol,
                    "side": "BUY",
                    "amount": amount,
                    "price": state["perp_bid"],
                    "action": "CLOSE",
                }
                await self.messenger.produce("signals", signal)
                self.is_active = False


if __name__ == "__main__":
    strategy = FundingArbStrategy(symbol="BTC/USDT")
    asyncio.run(strategy.run(amount=0.01))
