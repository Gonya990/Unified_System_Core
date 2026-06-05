from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class FinanceProvider(ABC):
    @abstractmethod
    def fetch_transactions(self, since_days: int = 30) -> list[dict[str, Any]]:
        ...

    @abstractmethod
    def fetch_balances(self) -> list[dict[str, Any]]:
        ...
