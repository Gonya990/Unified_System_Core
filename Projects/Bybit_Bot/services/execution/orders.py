import logging
import asyncio
from kubernetes import client, config
from k8s_leaderelection import LeaderElection

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("BybitExecution")

class BybitExecutionEngine:
    """
    Задача 2: Исполнение ордеров Bybit V5.
    - Паттерн: Leader Election (Single Writer).
    - API: Batch Creation.
    - Rate Control: X-Bapi-Limit-Status.
    """
import os
from common.messaging import RedisStreamManager

class BybitExecutionEngine:
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.is_leader = False
        self.rate_limit_remaining = 100
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        self.messenger = RedisStreamManager(redis_url)
        
        # Настройка Leader Election
        try:
            config.load_incluster_config()
        except Exception:
            try:
                config.load_kube_config()
            except:
                logger.warning("Kube config not found. Running without real LE.")
            
        self.le = LeaderElection(
            client.CoordinationV1Api(),
            namespace="trading",
            name="bybit-executor-lock",
            on_started_leading=self._on_start_leading,
            on_stopped_leading=self._on_stop_leading
        )

    def _on_start_leading(self):
        logger.info("👑 I am the LEADER. API writing ENABLED.")
        self.is_leader = True

    def _on_stop_leading(self):
        logger.warning("📉 Loss of leadership. API writing DISABLED.")
        self.is_leader = False

    async def execute_order(self, order):
        if not self.is_leader:
            return None
        
        # Эмуляция исполнения ордера на Bybit
        order_id = f"bit-{int(datetime.now().timestamp())}"
        report = {
            "order_id": order_id,
            "asset_pair": order['symbol'],
            "trade_side": order['side'],
            "executed_qty": order['amount'],
            "price_executed": order['price'],
            "fmv_fiat_value": order['amount'] * order['price'],
            "fee_amount": order['amount'] * order['price'] * 0.0006,
            "fee_currency": "USDT"
        }
        return report

    async def run(self):
        # Start leader election in background
        asyncio.create_task(asyncio.to_thread(self.le.run))
        
        logger.info("ExecutionEngine started. Listening for validated orders...")
        stream = "orders_validated"
        group = "execution-group"
        async for msg_id, order in self.messenger.consume(stream, group, "exec-1"):
            if self.is_leader:
                report = await self.execute_order(order)
                if report:
                    await self.messenger.produce("execution_reports", report)
                    logger.info(f"🚀 Executed and reported: {report['order_id']}")
            else:
                logger.debug(f"Passive mode: skipping order {msg_id}")

if __name__ == "__main__":
    engine = BybitExecutionEngine(os.getenv("BYBIT_API_KEY"), os.getenv("BYBIT_API_SECRET"))
    asyncio.run(engine.run())
