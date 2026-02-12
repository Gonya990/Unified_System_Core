import asyncio
import logging
import os

import psycopg2
from common.messaging import RedisStreamManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ComplianceLogger")

class ComplianceLogger:
    def __init__(self):
        default_db = "postgresql://user:pass@localhost:5432/trading"
        self.db_url = os.getenv("DATABASE_URL", default_db)
        self.conn = None
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        self.messenger = RedisStreamManager(redis_url)

    async def connect(self):
        try:
            self.conn = psycopg2.connect(self.db_url)
            self.conn.autocommit = True
            logger.info("Connected to Compliance Database")
        except Exception as e:
            logger.error(f"DB Connection failed: {e}")

    async def run(self):
        await self.connect()
        logger.info("ComplianceLogger started. Listening for execution reports...")
        stream = "execution_reports"
        group = "compliance-group"
        async for msg_id, report in self.messenger.consume(stream, group, "comp-1"):
            try:
                with self.conn.cursor() as cur:
                    cur.execute("""
                        INSERT INTO compliance_trades (
                            order_id, asset_pair, trade_side, executed_qty, 
                            price_executed, fmv_fiat_value, fee_amount, fee_currency
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        report['order_id'],
                        report['asset_pair'],
                        report['trade_side'],
                        report['executed_qty'],
                        report['price_executed'],
                        report['fmv_fiat_value'],
                        report['fee_amount'],
                        report['fee_currency']
                    ))
                logger.info(f"✅ DAC8 Logged: {report['order_id']}")
            except Exception as e:
                logger.error(f"Failed to log trade: {e}")

if __name__ == "__main__":
    logger_service = ComplianceLogger()
    asyncio.run(logger_service.run())
