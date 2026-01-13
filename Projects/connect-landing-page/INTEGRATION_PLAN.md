# Integration Plan: Connect Landing Page & Global1Sim

## Current State Analysis

### Frontend (Connect Landing Page)
- **Tech Stack**: Next.js 16.1, React 19, Tailwind v4.
- **Goal**: Sell "Memberships" (Explorer, Connector, Global Citizen).
- **Current State**: Hardcoded mock payment form. No API integration.
- **Data**: Hardcoded countries and plans in `app/data/`.

### Backend (Global1Sim)
- **Tech Stack**: Python/FastAPI, Postgres.
- **Capabilities**:
  - **Public Products**: `GET /api/packages` (Lists eSIM data packages).
  - **Order Creation**: `POST /api/b2c/orders/auto-create` (Creates order + payment link).
  - **No Subscription Logic**: Backend sells one-time data bundles, not recurring subscriptions.
  - **No Contact Form Endpoint**: Missing functionality for "Contact Us".

---

## 3 Integration Possibilities

### Option 1: Direct Mapping (MVP) - **RECOMMENDED**
**Treat "Memberships" as Marketing Wrappers for Data Packages.**
- **Concept**: User selects "Explorer Plan" -> System buys "1GB Global Package".
- **Backend**: No changes. Use existing `b2c_orders.py`.
- **Frontend**: 
  - Hardcode mapping: `Explorer -> Tier ID X`, `Connector -> Tier ID Y`.
  - Call `POST /api/b2c/orders/auto-create`.
  - Redirect to `payment_url` returned by API.
- **Inference Cost**: Low.
- **Pros**: Immediate launch, zero backend dev time.
- **Cons**: One-time purchase only (not auto-renewing).

### Option 2: Next.js BFF (Backend for Frontend)
**Orchestrate logic in Next.js API Routes.**
- **Concept**: Frontend calls `/api/subscribe`. Next.js handles user creation & order placement.
- **Backend**: No changes.
- **Frontend**: Create API routes to hide complexity and handle "Contact Us" (e.g., send email via Resend/SendGrid).
- **Inference Cost**: Medium.
- **Pros**: Cleaner client code, enables custom logic (like email notifications).
- **Cons**: Still one-time purchase on backend.

### Option 3: Full Subscription Model
**Refactor Backend for Recurring Billing.**
- **Concept**: True implementation of subscriptions.
- **Backend**: Add `subscriptions` table, recurring payment logic (Stripe/Cardcom tokenization), Cron jobs.
- **Frontend**: Full customer portal for managing subscriptions.
- **Inference Cost**: High (Significant engineering effort).
- **Pros**: True business model alignment.
- **Cons**: Weeks of delay.

---

## Selected Plan: Option 1 + Contact Form Shim

### 1. Data Mapping
| Frontend Plan | Backend Package Tier (Example) |
|---------------|--------------------------------|
| Explorer      | `global_1gb_30d`               |
| Connector     | `global_3gb_30d`               |
| Global Citizen| `global_5gb_30d`               |

### 2. Contact Form Solution
Since backend lacks a contact endpoint:
- **Solution**: Use **Resend** or **Nodemailer** in a Next.js Server Action.
- **Action**: `sendContactEmail(formData)` directly from Next.js.

### 3. Implementation Checklist
- [ ] **Env Vars**: Set `NEXT_PUBLIC_API_URL` to Global1Sim URL.
- [ ] **API Client**: Create `lib/api.ts` with `createOrder` function.
- [ ] **Checkout Flow**: Replace mock modal with API call + Redirect.
- [ ] **Contact Form**: Implement Server Action for email sending.
