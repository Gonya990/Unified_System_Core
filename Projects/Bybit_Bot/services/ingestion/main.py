import asyncio
import json
import logging
import os
import websockets
from datetime import datetime
from common.messaging import RedisStreamManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("BybitIngestion")

class BybitDataIngestion:
    def __init__(self, symbols=["BTCUSDT"]):
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
                    payload = {"op": "subscribe", "args": subs}
                    await ws.send(json.dumps(payload))
                    
                    async for message in ws:
                        data = json.loads(message)
                        if "data" in data and "topic" in data:
                            await self.handle_message(data)
            except Exception as e:
                logger.error(f"WS Error: {e}. Reconnecting in 5s...")
                await asyncio.sleep(5)

    async def handle_message(self, data):
        """Нормализация и отправка в шину данных"""
        ticker_data = data['data']
        # Bybit V5 Ticker structure normalization
        msg = {
            "symbol": ticker_data.get('symbol'),
            "spot_ask": float(ticker_data.get('ask1Price', 0)),
            "perp_bid": float(ticker_data.get('bid1Price', 0)),
            "funding_rate": float(ticker_data.get('fundingRate', 0)),
            "timestamp": datetime.now().timestamp()
        }
        await self.messenger.produce("market_data", msg)
        logger.debug(f"Produced market data for {msg['symbol']}")

if __name__ == "__main__":
    ingestion = BybitDataIngestion()
    asyncio.run(ingestion.connect())
