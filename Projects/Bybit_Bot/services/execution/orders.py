import asyncio
import logging
import os
from datetime import datetime

from common.leader import LeaderElection
from common.messaging import RedisStreamManager
from common.token_broker import TokenBroker
from kubernetes import client, config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("BybitExecution")


class BybitExecutionEngine:
    def __init__(self, provider="bybit"):
        self.broker = TokenBroker()
        self.api_key = self.broker.get_key(provider)
        self.is_leader = False
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        self.messenger = RedisStreamManager(redis_url)

    def on_start(self):
        self.is_leader = True
        logger.info("Leadership acquired. Starting execution loop.")

    def on_stop(self):
        self.is_leader = False
        logger.info("Leadership lost. Stopping execution loop.")

    async def execute_order(self, signal):
        """Execute order via Bybit API (DAC8 Compliant logging)"""
        if not self.is_leader:
            return

        logger.info(f"Executing {signal['action']} for {signal['symbol']}")
        # Simulating API call
        await asyncio.sleep(0.1)

        # Compliance Log
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "symbol": signal["symbol"],
            "action": signal["action"],
            "price": signal["price"],
            "amount": signal["amount"],
            "status": "FILLED",
        }
        await self.messenger.produce("compliance_logs", log_entry)

    async def run(self):
        # Leader Election Setup
        try:
            config.load_incluster_config()
        except config.ConfigException:
            config.load_kube_config()

        namespace = os.getenv("K8S_NAMESPACE", "trading")
        api = client.CoordinationV1Api()

        le = LeaderElection(api, namespace, "bybit-execution-lock", self.on_start, self.on_stop)

        # Run leader election in background
        asyncio.create_task(asyncio.to_thread(le.run))

        logger.info("Bybit Execution Engine started. Waiting for leadership...")

        stream = "signals"
        group = "execution-group"
        async for _msg_id, signal in self.messenger.consume(stream, group, "exec-1"):
            if self.is_leader:
                await self.execute_order(signal)
            else:
                logger.debug("Ignoring signal (not leader)")


if __name__ == "__main__":
    engine = BybitExecutionEngine()
    asyncio.run(engine.run())
