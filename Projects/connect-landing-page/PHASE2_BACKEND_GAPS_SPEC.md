# Connect Landing Page — Phase 2 Spec

## Objective
Align the Connect landing page with the **current one-time travel package** backend model, while **fully capturing** the previously implied subscription/membership model as a future-ready specification.

This document is meant to be pasted (or linked) into Beads under the Simless epic and used as the Phase 2 umbrella spec.

---

## Current Behavior (Observed)
### Frontend order flow (Connect landing)
- Client calls `createOrder(plan, { name, email })`.
- Request: `POST ${NEXT_PUBLIC_API_URL}/api/b2c/orders/auto-create`
- Expected response:
  ```json
  {
    "payment_url": "https://...",
    "order_id": "ord_...",
    "expires_at": "2026-01-13T17:00:00Z",
    "status": "pending"
  }
  ```
- Browser redirects to `payment_url`.

### Frontend contact flow (Connect landing)
- Contact form uses a Next.js Server Action: `sendContactEmail(formData)`.
- Uses env: `CONTACT_EMAIL_TO`, `CONTACT_EMAIL_FROM`, `RESEND_API_KEY`.
- If `RESEND_API_KEY` is missing, it currently **logs and returns success** (dev fallback).

### Backend expectations (per existing integration notes)
- Backend described as FastAPI + Postgres.
- Public products: `GET /api/packages`.
- Order creation: `POST /api/b2c/orders/auto-create`.
- There is **no subscription logic** in backend currently.

---

## The Mismatch (Documented + Comparison)
### What the landing page implies
The landing page language and UX uses “membership / monthly / subscription” framing.

### What the backend actually sells today
The backend sells **one-time prepaid eSIM data bundles** (packages), not recurring subscriptions.

### Why this matters (practical)
- Payment confirmation + fulfillment semantics differ.
- “Monthly plan” implies renewal, proration, cancellation, customer portal.
- One-time packages imply expiration, one-off purchase receipt, and optional re-purchase.

---

## Decision: Phase 2 (Now)
### Product positioning to ship now
**Update landing page copy and wording to one-time travel packages**:
- Use “package”, “prepaid”, “one-time purchase”, “valid for X days”, “no auto-renewal”.
- Avoid “monthly”, “membership”, “subscription” wording in B2C personal purchase paths.

This does not require backend subscription infrastructure and matches the current checkout redirect behavior.

---

## Subscription / Membership Model (Future Spec — Fully Captured)
This section is a **complete forward-looking spec** so future development can implement subscriptions without re-deriving requirements.

### Goals
- Offer recurring plans (Explorer / Connector / Global Citizen) billed monthly.
- Provide predictable recurring data entitlement (e.g., monthly allocation, rollover rules).
- Customer lifecycle:
  - start subscription
  - renew automatically
  - upgrade/downgrade
  - cancel
  - view invoices / payment methods

### Key Concepts & Entities
- **Plan**: marketing-level subscription offering (Explorer/Connector/Global Citizen)
- **Subscription**: an active contract tied to a customer
- **Billing Period**: monthly cycle, with period_start/period_end
- **Entitlement**: what the user receives each period (eSIM data package issuance, voucher, etc.)
- **Payment Provider Customer**: provider-side customer + payment method

### Data Model (minimum)
1) `customers`
- `id`, `email`, `name`, `created_at`
- `payment_provider_customer_id`

2) `plans`
- `id`, `slug`, `title`, `monthly_price`, `currency`
- `entitlement_policy` (e.g., tiers, allocation)

3) `subscriptions`
- `id`, `customer_id`, `plan_id`
- `status`: `trialing|active|past_due|canceled|paused`
- `current_period_start`, `current_period_end`
- `cancel_at_period_end` (bool)
- `payment_provider_subscription_id`

4) `subscription_events`
- provider event log (idempotent)
- `event_id` unique
- `subscription_id`, `type`, `payload_hash`, `created_at`

### API Surface (future)
1) Start subscription
- `POST /api/subscriptions`
- Request:
  ```json
  { "plan": "explorer", "customer": { "name": "...", "email": "..." } }
  ```
- Response:
  ```json
  { "subscription_id": "sub_...", "checkout_url": "https://..." }
  ```

2) Subscription status
- `GET /api/subscriptions/{subscription_id}`
- Response includes status, plan, next renewal date.

3) Customer portal
- `POST /api/subscriptions/portal`
- Response includes `portal_url`.

4) Webhooks
- `POST /api/webhooks/subscriptions/{provider}`
- Verify signature + idempotency.
- Handle:
  - `invoice.paid` → keep `active`
  - `invoice.payment_failed` → `past_due`
  - `customer.subscription.deleted` → `canceled`

### Idempotency & Webhook Security (future)
- Must verify provider signatures using raw body bytes.
- Must enforce replay window if timestamped signatures are used.
- Must dedupe by provider event_id with a unique constraint.

### Acceptance Criteria (future)
- A subscription renews automatically without manual intervention.
- Cancelation takes effect at period end (or immediately, depending on selected behavior).
- Status is authoritative from verified webhooks, not client callbacks.

---

## Phase 2 Backend Gaps (Now) — Required Work
This is the concrete backend work needed to support the current one-time travel package flow robustly.

### A) Public Contact / Lead Intake API
**Endpoint**: `POST /api/public/contact`

- Validates and stores a durable lead record.
- Routes asynchronously (email/CRM/Slack).
- Rate limits and PII-safe logs.

Request:
```json
{
  "name": "Jane Doe",
  "email": "jane@example.com",
  "subject": "Enterprise inquiry",
  "message": "We need 500 lines across LATAM",
  "source": "connect-landing-page",
  "locale": "en",
  "utm": { "source": "google", "medium": "cpc", "campaign": "brand" }
}
```

Response:
```json
{ "lead_id": "ld_123", "status": "accepted" }
```

### B) Public Order Status API
**Endpoint**: `GET /api/public/orders/{order_id}` (or `{order_token}` if IDs are guessable)

Response:
```json
{
  "order_id": "ord_123",
  "status": "pending|paid|failed|expired",
  "expires_at": "2026-01-13T17:00:00Z",
  "payment": { "provider": "provider_name", "last_event_at": "2026-01-13T16:59:10Z" }
}
```

### C) Payment Webhooks + Idempotency
**Endpoint**: `POST /api/webhooks/payments/{provider}`

- Signature verification (raw body).
- Replay protection (timestamp window where applicable).
- Idempotency by provider `event_id`.

### D) Order Creation Idempotency (write path)
If `POST /api/b2c/orders/auto-create` is public-facing:
- Support `Idempotency-Key` header.
- Replay prior response for same key.

---

## Minimal Test Plan (Now)
1) Contact happy path → `201` lead stored, routing queued
2) Contact validation failure → `400`
3) Contact rate-limit → `429`
4) Create order → order status returns `pending`
5) Webhook invalid signature → `401`, order unchanged
6) Webhook success → order becomes `paid`
7) Webhook replay → idempotent `200`, no duplicate side effects
8) Order create idempotency (same `Idempotency-Key`) → stable response
