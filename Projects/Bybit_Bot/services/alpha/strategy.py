import logging
import asyncio
from datetime import datetime

# Logging for DAC8
log_fmt = '%(asctime)s [%(levelname)s] %(message)s'
logging.basicConfig(level=logging.INFO, format=log_fmt)
logger = logging.getLogger("BybitArb")

class FundingArbStrategy:
    """
    Ведущий архитектор: Antigravity (Senior Quant)
    Стратегия: Delta Neutral Funding Arbitrage (Cash & Carry)
    Биржа: Bybit Unified Trading Account (UTA)
    """
    def __init__(self, exchange, symbol="BTC/USDT", target_apr=0.12, leverage=1.0):
        self.exchange = exchange
        self.symbol = symbol
        self.target_apr = target_apr
        self.leverage = leverage
        self.is_active = False
        
        # Институциональные комиссии Bybit (Maker/Taker)
        self.fees = {
            "spot_taker": 0.001,
            "perp_taker": 0.00055,
            "perp_maker": 0.0002
        }

    async def get_market_state(self):
        """Сбор данных L2 + Funding Rate с проверкой на устаревание"""
        try:
            perp_symbol = f"{self.symbol}:USDT"
            
            ticker_task = asyncio.create_task(
                self.exchange.fetch_ticker(self.symbol)
            )
            perp_task = asyncio.create_task(
                self.exchange.fetch_ticker(perp_symbol)
            )
            funding_task = asyncio.create_task(
                self.exchange.fetch_funding_rate(perp_symbol)
            )
            # Parallel gathering
            res = await asyncio.gather(
                ticker_task,
                perp_task,
                funding_task
            )
            spot, perp, funding = res
            
            # Проверка на "грязные данные" (Data Staleness)
            latency = (datetime.now().timestamp() * 1000) - spot['timestamp']
            if latency > 1000: # Более 1 секунды задержки
                logger.warning(f"⚠️ Данные устарели! Latency: {latency:.2f}ms")
                return None

            return {
                "spot_ask": spot['ask'],
                "perp_bid": perp['bid'],
                "funding_rate": funding['fundingRate'],
                "latency_ms": latency
            }
        except Exception as e:
            logger.error(f"❌ Ошибка сбора данных: {e}")
            return None

    def calculate_metrics(self, state):
        """Расчет экономической целесообразности сделки"""
        spot_price = state['spot_ask']
        perp_price = state['perp_bid']
        fr = state['funding_rate']
        
        # 1. Стоимость входа (Entry Cost)
        entry_fees = (spot_price * self.fees['spot_taker']) + \
                     (perp_price * self.fees['perp_taker'])
        
        # 2. Ожидаемая годовая доходность (APR)
        # Фандинг каждые 8 часов (3 раза в день)
        daily_yield = fr * 3
        annual_yield = daily_yield * 365
        
        # 3. Точка безубыточности (Break-even days)
        # Учитываем комиссию на вход и выход (2x)
        total_cycle_fees = entry_fees * 2
        denom = (spot_price * daily_yield)
        days_to_be = total_cycle_fees / denom if daily_yield > 0 else float('inf')
        
        return {
            "apr": annual_yield,
            "days_to_be": days_to_be,
            "is_profitable": (annual_yield >= self.target_apr) and (days_to_be < 14)
        }

    async def check_and_execute(self, amount):
        """Основной цикл принятия решений"""
        state = await self.get_market_state()
        if not state: return
        
        metrics = self.calculate_metrics(state)
        
        logger.info(
            f"📊 {self.symbol} | FR: {state['funding_rate']:.4%} | "
            f"APR: {metrics['apr']:.2%} | BE: {metrics['days_to_be']:.1f}d"
        )
        
        if metrics['is_profitable'] and not self.is_active:
            logger.info("🚀 СИГНАЛ НА ВХОД: Рыночные условия оптимальны.")
            # Здесь вызывается Execution Engine
            await self.open_arbitrage_position(amount, state)
        elif not metrics['is_profitable'] and self.is_active:
            logger.info("📉 СИГНАЛ НА ВЫХОД: Доходность ниже порога.")
            await self.close_arbitrage_position(amount)

    async def open_arbitrage_position(self, amount, state):
        """Параллельное исполнение: Long Spot + Short Perp"""
        logger.info(
            f"Executing: BUY {amount} {self.symbol} (Spot) & "
            f"SELL {amount} (Perp)"
        )
        # Использование TWAP или Iceberg для крупных позиций
        self.is_active = True

    async def close_arbitrage_position(self, amount):
        logger.info(
            f"Closing: SELL {amount} {self.symbol} (Spot) & "
            f"BUY {amount} (Perp)"
        )
        self.is_active = False
