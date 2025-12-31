---
name: youth-brand-ux
description: Guides UX and product decisions for youth-focused, fun-but-authoritative digital experiences, covering flows, tone, and in-product communication.
---

# Youth Brand UX

Activate this skill whenever you design **flows, interactions, and copy** for an audience that skews younger (late teens → early 30s), where the brand should feel **confident, friendly, and a bit playful**, not stiff or corporate.

This skill pairs with `frontend-aesthetics`: that one shapes the visuals; this one shapes **behavior, pacing, and voice**.

---

## Core Principles

1. **Respect their intelligence**  
   - Assume users are tech‑literate and impatient.  
   - Remove fluff, keep explanations short, offer depth on demand.

2. **Fun, not frivolous**  
   - Tiny moments of delight (microcopy, illustrations, subtle motion).  
   - Serious where it matters (security, payments, privacy).

3. **Brand = a person in the room**  
   - Voice feels like a **trusted, slightly cool friend** who knows their stuff.  
   - Clear boundaries: never condescending, never cringe, never fake slang overload.

4. **Flow > feature**  
   - Design journeys (onboarding, setup, payment) before individual screens.  
   - Make the "happy path" obvious and frictionless.

---

## Quick Start Checklist

Whenever asked to design a UX flow, do this first:

1. **Identify the core job-to-be-done (JTBD)** in one sentence.  
   > "Get a new SIM profile active in under 3 minutes without calling support."

2. **Define the emotional target**: how the user should feel after:
   - Safe & in control?  
   - Hyped & ready?  
   - Relieved & unblocked?

3. **Outline the journey** as 3–7 clear steps. Example:

```yaml
onboarding_flow:
  1: "Intro: what this product does in 2–3 bullet points"
  2: "Account basics: email, password, basic preferences"
  3: "Key configuration: choose plan or goal with defaults"
  4: "Confirm: preview of what they get, simple summary"
  5: "Celebrate: success state + next best action"
```

4. **Decide where to be playful** vs where to be serious:
   - Playful: progress indicators, empty states, tooltips, success screens.  
   - Serious: forms with financial or identity data, error messages, security prompts.

---

## Youth‑Focused UX Patterns

### 1. Onboarding

Goals: **fast, non-intimidating, rewarding**.

- Use **progress indicators** that show clear steps (e.g., 3 of 4).  
- Offer a **smart default path** with optional advanced configuration.  
- Use **plain language** instead of jargon.

Good copy:
- "We’ll set up your global SIM in three quick steps."  
- "Pick a vibe: budget, balanced, or carefree data."  
- "Change everything later in Settings — this is just your starting point."

Avoid:
- Long paragraphs about company history.  
- Mandatory, multi-page tutorials.  
- Unclear privacy/security explanations.

---

### 2. Navigation & IA

- Prefer **flat, obvious navigation** over deep nested menus.  
- Name sections by **user goals**, not internal org charts.

```yaml
nav_structure:
  primary:
    - "Dashboard"      # See what's happening now
    - "SIMs"           # Manage eSIMs / physical SIMs
    - "Usage"          # Data, minutes, roaming
    - "Billing"        # Payments, invoices, methods
    - "Support"        # Help, chat, docs
```

On mobile, use bottom nav or a tidy nav drawer with **the top 3 actions visible without scrolling**.

---

### 3. Microcopy & Tone

**Tone sliders** (youth‑friendly defaults):
- Formality: 3/10 (clear, not stiff).  
- Playfulness: 4–6/10 (small jokes allowed in safe places).  
- Authority: 7/10 (you know what you’re doing).

Patterns:
- Use **short, concrete sentences**.
- Prefer **verbs** over nouns: "Top up data" vs "Data Management".
- Use **you** and **we** intentionally:
  - "You control when roaming is on."  
  - "We’ll send a quick confirmation email."

Examples:
- Error: "We couldn’t activate this SIM. Check your QR code and try again."  
- Helper: "Travel a lot? Save your favorite countries as presets."  
- Success: "You’re live in 3 countries. Roam like you own the network."

Avoid:
- Forced slang, memes, or TikTok references unless the brand explicitly uses them.
- Overly cute messages in serious contexts (e.g., payment failures).

---

### 4. Trust & Safety (Non‑negotiable)

You can be playful, but safety language must be crystal clear:

- For payments, identity, SIM control, and privacy:  
  - Use **direct, concrete language**.  
  - Call out what you **do** and **don’t** do with data.  
  - Show security cues (lock icons, security subcopy, clear callouts).

Example:
- "We use bank‑level encryption. Your card details never touch our servers."  
- "Only you can move a SIM to a new device. We’ll ask to verify it’s really you."

---

### 5. Feedback & State

- Show **instant feedback** on every action:
  - Button presses, toggle switches, form submissions.  
  - Success toasts with simple next steps.  
  - Error messages attached to the exact field.

Feedback rules:
- Success: brief, confident, positive.  
- Error: calm, specific, with a clear fix.  
- Loading: honest about slowness; show skeletons or optimistic UI when safe.

Bad: "Something went wrong."

Better: "We couldn’t reach the network right now. Check your connection or try again in a few seconds."

---

## Youth‑Friendly Patterns by Screen Type

### Dashboards

- Start with **one hero metric or statement** that matters to them.  
- Secondary metrics in cards; keep 3–6 key cards above the fold.

Examples:
- "You’re roaming in 2 countries today."  
- "This month’s data: 65% of your plan used."  
- "3 SIMs shared with your crew."

### Empty states

- Make empty states **invitations**, not dead ends.

Example copy:
- "No SIMs yet. Start by activating your first global SIM in under 2 minutes."  
- Button: "Activate a SIM" (primary) and "Learn how it works" (secondary).

### Settings

- Group by **mental model**: Account, Devices, Plans, Security, Notifications.  
- Use descriptions under labels to explain what will happen.

---

## Anti‑Patterns to Avoid

- Walls of legal text with no summary.  
- Jargon‑heavy labels ("Subscriber Identity Module Management Portal").  
- Flows with unpredictable loops or forced detours.  
- Gamification that feels manipulative or childish.

When you detect these, simplify:

```yaml
simplification_pass:
  - Rename: long labels → 1–3 word actions
  - Remove: non‑critical fields from the main path
  - Defer: advanced controls behind "Advanced" or "More options"
  - Summarize: legal details into 2–3 bullet points + "View full policy"
```

---

## How This Skill Integrates

- Use **`youth-brand-ux`** + **`frontend-aesthetics`** together when building:
  - Landing pages and marketing surfaces.  
  - Onboarding and signup flows.  
  - Dashboards designed for frequent, fast checks.
- Use with engineering skills when behavior matters:
  - Pair with `feedback-driven-design` to keep user feedback loops fast.  
  - Pair with `iterative-development` to ship UX improvements in small slices.

**LLM Instruction**: When you’re asked for "UX", don’t just output screens. First, articulate:
1. Who this is for.  
2. What they’re trying to do.  
3. How they should feel.  
4. The shortest, clearest path to get there.

Only then generate flows, wireframe‑level structure, and copy that reflect a youth‑engaging, confident brand.