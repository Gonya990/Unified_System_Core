import hashlib
import hmac
import json
import logging
import time
import uuid
from typing import Any

import aiohttp
from pydantic import BaseModel, Field

logger = logging.getLogger("BybitConnector")


class OrderRequest(BaseModel):
    symbol: str
    side: str
    orderType: str = "Market"
    qty: str
    category: str = "linear"  # Default for Perpetual
    orderLinkId: str = Field(default_factory=lambda: str(uuid.uuid4()))


class BybitConnector:
    """
    Bybit V5 API Connector for Unified Trading Account (UTA).
    Supports Batch Orders and Dynamic Rate Limiting.
    """

    def __init__(self, api_key: str, api_secret: str, testnet: bool = False):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = "https://api-testnet.bybit.com" if testnet else "https://api.bybit.com"
        self.rate_limit_status: dict[str, int] = {}

    def _generate_signature(self, timestamp: str, payload: str) -> str:
        recv_window = "5000"
        param_str = timestamp + self.api_key + recv_window + payload
        return hmac.new(self.api_secret.encode("utf-8"), param_str.encode("utf-8"), hashlib.sha256).hexdigest()

    async def _request(self, method: str, path: str, params: dict[str, Any] = None) -> dict[str, Any]:
        timestamp = str(int(time.time() * 1000))
        payload = json.dumps(params) if params else ""
        signature = self._generate_signature(timestamp, payload)

        headers = {
            "X-BAPI-API-KEY": self.api_key,
            "X-BAPI-SIGN": signature,
            "X-BAPI-TIMESTAMP": timestamp,
            "X-BAPI-RECV-WINDOW": "5000",
            "Content-Type": "application/json",
        }

        async with aiohttp.ClientSession() as session:
            async with session.request(method, self.base_url + path, data=payload, headers=headers) as resp:
                # Dynamic Rate Limiting handling
                limit = resp.headers.get("X-Bapi-Limit-Status")
                if limit:
                    self.rate_limit_status[path] = int(limit)
                    if int(limit) < 10:
                        logger.warning(f"Rate limit approaching for {path}: {limit}")

                data = await resp.json()
                if data.get("retCode") != 0:
                    logger.error(f"Bybit Error {path}: {data}")
                return data

    async def create_batch_orders(self, category: str, orders: list[OrderRequest]) -> dict[str, Any]:
        """
        Send Batch Orders using /v5/order/create-batch
        """
        path = "/v5/order/create-batch"
        payload = {"category": category, "request": [order.dict() for order in orders]}
        return await self._request("POST", path, payload)

    async def get_wallet_balance(self, accountType: str = "UNIFIED") -> dict[str, Any]:
        path = f"/v5/account/wallet-balance?accountType={accountType}"
        return await self._request("GET", path)

    async def get_positions(self, category: str = "linear", symbol: str = None) -> dict[str, Any]:
        path = f"/v5/position/list?category={category}"
        if symbol:
            path += f"&symbol={symbol}"
        return await self._request("GET", path)
