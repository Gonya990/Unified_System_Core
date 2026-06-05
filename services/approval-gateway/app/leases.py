from __future__ import annotations

import secrets
import time
import uuid
from dataclasses import dataclass
from typing import Any


@dataclass
class Lease:
    lease_id: str
    command: str
    path: str | None
    domain: str | None
    risk_score: float
    created_at: float
    expires_at: float
    status: str = "pending"  # pending | approved | denied | expired
    assertion: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "lease_id": self.lease_id,
            "command": self.command,
            "path": self.path,
            "domain": self.domain,
            "risk_score": self.risk_score,
            "created_at": self.created_at,
            "expires_at": self.expires_at,
            "status": self.status,
        }


class LeaseStore:
    def __init__(self, ttl_seconds: int = 120) -> None:
        self.ttl_seconds = ttl_seconds
        self._leases: dict[str, Lease] = {}

    def create(
        self,
        *,
        command: str,
        path: str | None,
        domain: str | None,
        risk_score: float,
    ) -> Lease:
        now = time.time()
        lease = Lease(
            lease_id=str(uuid.uuid4()),
            command=command,
            path=path,
            domain=domain,
            risk_score=risk_score,
            created_at=now,
            expires_at=now + self.ttl_seconds,
        )
        self._leases[lease.lease_id] = lease
        return lease

    def get(self, lease_id: str) -> Lease | None:
        self._purge()
        return self._leases.get(lease_id)

    def approve(self, lease_id: str, assertion: dict[str, Any] | None = None) -> Lease | None:
        lease = self.get(lease_id)
        if not lease or lease.status != "pending":
            return None
        if time.time() > lease.expires_at:
            lease.status = "expired"
            return lease
        lease.status = "approved"
        lease.assertion = assertion
        return lease

    def deny(self, lease_id: str) -> Lease | None:
        lease = self.get(lease_id)
        if not lease:
            return None
        lease.status = "denied"
        return lease

    def _purge(self) -> None:
        now = time.time()
        for lid, lease in list(self._leases.items()):
            if lease.status == "pending" and now > lease.expires_at:
                lease.status = "expired"
            if lease.status in ("approved", "denied", "expired") and now - lease.created_at > 3600:
                del self._leases[lid]


def generate_challenge() -> str:
    return secrets.token_urlsafe(32)
