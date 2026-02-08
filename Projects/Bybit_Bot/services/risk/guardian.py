import logging
import os
import asyncio
from common.messaging import RedisStreamManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("RiskGuard")

class RiskGuard:
    def __init__(self, max_leverage=3, max_pos_size=1000, daily_loss_limit=500):
        self.max_leverage = max_leverage
        self.max_pos_size = max_pos_size
        self.daily_loss_limit = daily_loss_limit
        self.current_daily_loss = 0
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        self.messenger = RedisStreamManager(redis_url)

    def validate_order(self, order_data):
        # 1. Проверка плеча
        lev = order_data.get('leverage', 1)
        if lev > self.max_leverage:
            logger.error(f"❌ Плечо {lev} > {self.max_leverage}")
            return False

        # 2. Проверка размера (Notional)
        nv = order_data['amount'] * order_data['price']
        if nv > self.max_pos_size:
            logger.error(f"❌ Позиция ${nv} > ${self.max_pos_size}")
            return False

        # 3. Kill Switch
        if self.current_daily_loss >= self.daily_loss_limit:
            logger.critical("🛑 KILL SWITCH ACTIVE")
            return False

        return True

    async def run(self):
        logger.info("RiskGuard started. Listening for signals...")
        stream = "signals"
        group = "risk-group"
        async for msg_id, signal in self.messenger.consume(stream, group, "risk-1"):
            if self.validate_order(signal):
                logger.info(f"✅ Signal {msg_id} validated. Sending to execution.")
                await self.messenger.produce("orders_validated", signal)
            else:
                logger.warning(f"⚠️ Signal {msg_id} rejected by risk.")

if __name__ == "__main__":
    guard = RiskGuard()
    asyncio.run(guard.run())
