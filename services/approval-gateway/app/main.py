from __future__ import annotations

import sys
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# Policy engine on path
_STAGING = Path(__file__).resolve().parents[3]
_POLICY_ENGINE = _STAGING / "services" / "policy-engine"
if str(_POLICY_ENGINE) not in sys.path:
    sys.path.insert(0, str(_POLICY_ENGINE))
from policy_engine.engine import PolicyEngine  # noqa: E402

from .leases import LeaseStore, generate_challenge
from .webauthn import verify_assertion

app = FastAPI(title="Unified Core Approval Gateway", version="1.0.0")
engine = PolicyEngine(_STAGING / "config" / "policy.json")
leases = LeaseStore(ttl_seconds=120)
_challenges: dict[str, str] = {}


class ExecuteCheckRequest(BaseModel):
    command: str = ""
    path: str | None = None
    intent: str | None = None


class ExecuteCheckResponse(BaseModel):
    allowed: bool
    action: str
    risk_score: float
    lease_id: str | None = None
    challenge: str | None = None
    reasons: list[str] = Field(default_factory=list)


class ApproveRequest(BaseModel):
    lease_id: str
    assertion: dict | None = None


class RiskScoreRequest(BaseModel):
    command: str | None = None
    path: str | None = None
    intent: str | None = None


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "approval-gateway"}


@app.post("/v1/execute/check", response_model=ExecuteCheckResponse)
def execute_check(body: ExecuteCheckRequest) -> ExecuteCheckResponse:
    decision = engine.evaluate(command=body.command, path=body.path, intent=body.intent)
    if decision.allowed:
        return ExecuteCheckResponse(
            allowed=True,
            action="allow",
            risk_score=decision.risk_score,
            reasons=decision.reasons,
        )
    if decision.action == "require_yubikey":
        lease = leases.create(
            command=body.command,
            path=body.path,
            domain=decision.domain,
            risk_score=decision.risk_score,
        )
        challenge = generate_challenge()
        _challenges[lease.lease_id] = challenge
        return ExecuteCheckResponse(
            allowed=False,
            action="require_yubikey",
            risk_score=decision.risk_score,
            lease_id=lease.lease_id,
            challenge=challenge,
            reasons=decision.reasons,
        )
    return ExecuteCheckResponse(
        allowed=False,
        action="deny",
        risk_score=decision.risk_score,
        reasons=decision.reasons,
    )


@app.post("/v1/approve")
def approve(body: ApproveRequest) -> dict:
    lease = leases.get(body.lease_id)
    if not lease:
        raise HTTPException(404, "Lease not found")
    challenge = _challenges.get(body.lease_id, "")
    if not verify_assertion(body.assertion or {}, challenge):
        raise HTTPException(403, "Invalid or missing WebAuthn assertion")
    approved = leases.approve(body.lease_id, body.assertion)
    _challenges.pop(body.lease_id, None)
    return {"status": "approved", "lease": approved.to_dict() if approved else None}


@app.post("/v1/deny")
def deny(body: ApproveRequest) -> dict:
    lease = leases.deny(body.lease_id)
    if not lease:
        raise HTTPException(404, "Lease not found")
    _challenges.pop(body.lease_id, None)
    return {"status": "denied", "lease": lease.to_dict()}


@app.get("/v1/lease/{lease_id}")
def get_lease(lease_id: str) -> dict:
    lease = leases.get(lease_id)
    if not lease:
        raise HTTPException(404, "Lease not found")
    return lease.to_dict()


@app.post("/v1/risk-score")
def risk_score(body: RiskScoreRequest) -> dict:
    return engine.get_risk_score(command=body.command, path=body.path, intent=body.intent)
