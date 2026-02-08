import asyncio
import json
import logging
import websockets
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("BybitIngestion")

class BybitDataIngestion:
    """
    Service A: Data Ingestion
    Задача: Поддержание стабильного WebSocket-соединения с Bybit API v5.
    """
    def __init__(self, symbols=["BTCUSDT"]):
        self.uri = "wss://stream.bybit.com/v5/public/linear"
        self.symbols = symbols
        self.is_running = True

    async def connect(self):
        while self.is_running:
            try:
                async with websockets.connect(self.uri) as ws:
                    logger.info(f"Connected to Bybit WS: {self.uri}")
                    
                    # Подписка на Orderbook L1 (Ticker)
                    subs = [f"tickers.{s}" for s in self.symbols]
                    payload = {"op": "subscribe", "args": subs}
                    await ws.send(json.dumps(payload))
                    
                    async for message in ws:
                        data = json.loads(message)
                        if "data" in data:
                            self.handle_message(data)
            except Exception as e:
                logger.error(f"WS Error: {e}. Reconnecting in 5s...")
                await asyncio.sleep(5)

    def handle_message(self, data):
        # Здесь данные нормализуются и отправляются в Redis/gRPC
        # В 2026 году важна метка времени для DAC8
        ts = datetime.now().isoformat()
        logger.debug(f"[{ts}] Received: {data['topic']}")

if __name__ == "__main__":
    ingestion = BybitDataIngestion()
    asyncio.run(ingestion.connect())
