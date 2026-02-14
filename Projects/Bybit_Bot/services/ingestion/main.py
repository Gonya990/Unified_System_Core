import asyncio
import json
import logging
import os
from datetime import datetime

import websockets
from common.messaging import RedisStreamManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("BybitIngestion")


class BybitDataIngestion:
    def __init__(self, symbols=None):
        if symbols is None:
            symbols = ["BTCUSDT"]
        self.uri = "wss://stream.bybit.com/v5/public/linear"
        self.symbols = symbols
        self.is_running = True
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        self.messenger = RedisStreamManager(redis_url)

    async def connect(self):
        while self.is_running:
            try:
                async with websockets.connect(self.uri) as ws:
                    logger.info(f"Connected to Bybit WS: {self.uri}")
                    subs = [f"tickers.{s}" for s in self.symbols]
                    payload = {"op": "subscribe", "args": subs, "req_id": "sub_001"}
                    await ws.send(json.dumps(payload))

                    async for message in ws:
                        data = json.loads(message)
                        if "op" in data and data.get("op") == "subscribe":
                            logger.info(f"Subscription result: {data}")
                            continue
                        
                        if "data" in data and "topic" in data:
                            await self.handle_message(data)
                        elif "ret_msg" in data:
                            logger.warning(f"Response: {data}")
            except Exception as e:
                logger.error(f"WS Error: {e}. Reconnecting in 5s...")
                await asyncio.sleep(5)

    async def handle_message(self, data):
        """Нормализация и отправка в шину данных"""
        ticker_data = data["data"]
        # Bybit V5 Ticker structure normalization
        msg = {
            "symbol": ticker_data.get("symbol"),
            "spot_ask": float(ticker_data.get("ask1Price", ticker_data.get("lastPrice", 0))),
            "perp_bid": float(ticker_data.get("bid1Price", ticker_data.get("lastPrice", 0))),
            "funding_rate": float(ticker_data.get("fundingRate", 0)),
            "timestamp": datetime.now().timestamp(),
        }
        await self.messenger.produce("market_data", msg)
        # Log once every 10 messages to avoid spam but show activity
        if not hasattr(self, '_msg_count'): self._msg_count = 0
        self._msg_count += 1
        if self._msg_count % 10 == 0:
            logger.info(f"📈 Produced market stats for {msg['symbol']} (total: {self._msg_count})")


if __name__ == "__main__":
    ingestion = BybitDataIngestion()
    asyncio.run(ingestion.connect())
