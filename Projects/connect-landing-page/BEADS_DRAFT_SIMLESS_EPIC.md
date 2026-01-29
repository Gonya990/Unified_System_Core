# Beads Draft — Connect Landing Page Integration (under Simless epic)

## Purpose
This document consolidates the relevant Beads issues for integrating `Projects/connect-landing-page/` with backend systems, and provides a review-ready draft of what each issue should contain.

Primary goals:
1) Ensure these issues are correctly organized under the **Simless epic** (once epic id is confirmed).
2) Ensure the product model is consistent **now** (one-time travel packages) while fully capturing the future **subscription/membership** model as a spec.

Related spec (Phase 2):
- `Projects/connect-landing-page/PHASE2_BACKEND_GAPS_SPEC.md`

---

## Current Beads Topology (observed)
### MVP
- `US-z3v` — Connect Landing Page Integration (MVP)
  - Blocks/children (all closed):
    - `US-6lz` Configure Env & API Client (closed)
    - `US-xqt` Implement Payment Flow (closed)
    - `US-xn1` Implement Contact Form (closed)
    - `US-df2` Verify & Deploy (closed)

### Phase 2 Umbrella
- `US-pkr` — Connect Landing Page — Phase 2 (Backend Gaps & Localization)
  - Discovered-from dependents (open):
    - `US-byw` [Backend] Order Webhook Handler & Idempotency (open, P1)
    - `US-cy0` [Backend] Order Status & Confirmation Endpoint (open, P1)
    - `US-y1e` [Backend] Public Contact API & Lead Routing (open, P2)
    - (plus localization/UI tasks: `US-hz1`, `US-09z`, `US-ai0`)

---

## Required Epic Organization (Simless)
**User requirement**: These Beads should be under the **Simless epic**.

### Pending input
- Simless epic id: `US-____` (NEEDED)

### Proposed linking
Once epic id is known:
- Attach `US-pkr` under Simless epic using `parent-child`.
- Optional: also attach `US-z3v` under Simless epic (if you want the whole integration lineage grouped).

Command template:
- `bd dep add US-pkr US-____ --type parent-child`
- (optional) `bd dep add US-z3v US-____ --type parent-child`

---

## Product Model: One-time vs Subscription (required documentation)
### Decision for now
- Landing page should be updated to **one-time travel package purchase** framing.

### Subscription model (future)
- The full subscription/membership model must be extracted and preserved for future development.
- This is captured in: `Projects/connect-landing-page/PHASE2_BACKEND_GAPS_SPEC.md` under:
  - “Subscription / Membership Model (Future Spec — Fully Captured)”

---

## Draft Issue Content (review-ready)
Use the following as the intended descriptions/acceptance criteria for each issue.

### `US-pkr` — Phase 2 Umbrella (Backend Gaps & Localization)
**Description (paste-ready)**
- Source of truth spec: `Projects/connect-landing-page/PHASE2_BACKEND_GAPS_SPEC.md`
- Phase 2 scope (backend):
  1) Public contact/lead intake API
  2) Payment webhooks + signature verification + idempotency
  3) Public order status/confirmation endpoint
  4) Order create idempotency if endpoint is public-facing
- Phase 2 scope (frontend copy): migrate B2C flows to one-time package wording (monthly/subscription copy removal), while preserving future subscription spec.

**Acceptance criteria**
- All child issues (`US-y1e`, `US-byw`, `US-cy0`) have explicit API contracts + DoD.
- Product mismatch is explicitly resolved for the shipped landing page.

---

### `US-y1e` — [Backend] Public Contact API & Lead Routing
**Goal**
Provide a durable backend endpoint for lead capture and routing (instead of email-only shim).

**Endpoint**
- `POST /api/public/contact`

**Minimum requirements**
- Strict validation + size limits + unknown-field rejection.
- Rate limiting and abuse controls.
- Store lead durably; route asynchronously (email/CRM/Slack) with retries.
- PII-safe structured logs.

**DoD**
- Endpoint returns `201` with `{lead_id,status}`.
- Downstream routing failures do not lose the lead.

---

### `US-byw` — [Backend] Order Webhook Handler & Idempotency
**Goal**
Create a verified webhook intake that transitions orders to `paid/failed/expired` authoritatively.

**Endpoint**
- `POST /api/webhooks/payments/{provider}`

**Minimum requirements**
- Signature verification using raw request body.
- Replay window enforcement when provider supports timestamps.
- Idempotency by provider `event_id` with unique constraint.
- Structured logs + metrics for verification failures.

**DoD**
- Duplicate webhook deliveries do not cause duplicate side effects.
- Invalid signature never mutates state.

---

### `US-cy0` — [Backend] Order Status & Confirmation Endpoint
**Goal**
Support post-checkout redirect UX with a stable, public “what happened” endpoint.

**Endpoint**
- `GET /api/public/orders/{order_id}` (or tokenized variant)

**Minimum requirements**
- No PII exposure.
- Status reflects webhook-confirmed truth.
- Supports pending→paid transition reliably.

**DoD**
- Returns `pending` after creation; flips to `paid` after verified webhook.

---

## Notes
- Frontend currently maps marketing plans to backend `package_tier_id` and expects one-time checkout redirect via `payment_url`.
- Any remaining “monthly” terminology in B2C paths should be removed/renamed to one-time semantics, while preserving the subscription spec for future implementation.
