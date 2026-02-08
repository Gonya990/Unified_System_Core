import logging
import asyncio
import psycopg2
from datetime import datetime, timezone
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ComplianceLogger")

class ComplianceLogger:
    """
    Service E: Compliance Logger
    Задача: Асинхронная запись всех транзакций в PostgreSQL/TimescaleDB (DAC8).
    """
    def __init__(self):
        self.db_url = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost:5432/trading")
        self.conn = None
        self.queue = asyncio.Queue()

    async def connect(self):
        try:
            self.conn = psycopg2.connect(self.db_url)
            self.conn.autocommit = True
            logger.info("Connected to Compliance Database")
        except Exception as e:
            logger.error(f"DB Connection failed: {e}")

    async def log_trade(self, trade_data):
        """Добавление сделки в очередь на запись"""
        await self.queue.put(trade_data)

    async def worker(self):
        """Фоновый процесс записи из очереди"""
        while True:
            trade = await self.queue.get()
            try:
                with self.conn.cursor() as cur:
                    cur.execute("""
                        INSERT INTO compliance_trades (
                            order_id, asset_pair, trade_side, executed_qty, 
                            price_executed, fmv_fiat_value, fee_amount, fee_currency
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        trade['order_id'], trade['asset_pair'], trade['trade_side'],
                        trade['executed_qty'], trade['price_executed'],
                        trade['fmv_fiat_value'], trade['fee_amount'], trade['fee_currency']
                    ))
                logger.info(f"Logged trade: {trade['order_id']}")
            except Exception as e:
                logger.error(f"Failed to log trade {trade.get('order_id')}: {e}")
            finally:
                self.queue.task_done()

    async def run(self):
        await self.connect()
        asyncio.create_task(self.worker())
