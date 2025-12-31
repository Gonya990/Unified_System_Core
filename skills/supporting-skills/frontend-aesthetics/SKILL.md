---
name: frontend-aesthetics
description: Steers Claude to design and implement distinctive, youth-engaging frontend interfaces (HTML/CSS/React) with a fun but authoritative brand aesthetic, avoiding generic "AI slop" UIs.
---

# Frontend Aesthetics (Youth + Brand)

Activate this skill whenever you generate or refactor frontend code or designs (HTML/CSS/JS/React/Tailwind) and the product should feel **fresh, youth-friendly, and on-brand**, not like a generic template.

This skill is inspired by the "frontend design through skills" pattern: instead of one vague design sentence, treat **typography, color, motion, and background** as explicit design axes that map directly to code.

## Core Principles

1. **Avoid the generic center**  
   - Do *not* default to Inter/Roboto, purple gradients on white, and bland cards.  
   - Assume the default model output is too safe and boring.

2. **Youth ≠ childish**  
   - Aim for **confident, slightly playful, street-smart** — think modern design brands, not kid cartoons.  
   - Clear hierarchy, bold statements, real contrast.

3. **Brand-forward, code-ready**  
   - Every aesthetic choice should map to **implementable CSS/JS**, not just mood words.  
   - Prefer idioms that work well in modern stacks (CSS variables, Tailwind tokens, React component props).

4. **Motion with intent**  
   - Use micro-interactions to reward taps, hovers, and progress.  
   - No random spinning logos; motion should reinforce meaning.

---

## Quick Start (What You Do First)

When a user asks you to build or redesign a UI:

1. **State the aesthetic** in 1–2 lines, tuned for youth + authority. Example:
   > "Confident, slightly rebellious youth fintech dashboard: bold typography, neon accents on dark, smooth micro-interactions, no corporate stiffness."

2. **Choose fonts, color system, motion style, and backgrounds explicitly** (see sections below) and show how they appear in CSS/Tailwind.

3. **Generate structure first, styling second**:
   - Step 1: semantic layout (sections, grids, nav, content).  
   - Step 2: brand layer (fonts, colors, motion, backgrounds).

4. **Output both design rationale and code**:  
   - A short design spec (1–3 paragraphs or a bullet list).  
   - Then concrete code (HTML/React/Tailwind/CSS modules).

---

## Design Axes

### 1. Typography (Signal quality + attitude)

- **Avoid**: Inter, Roboto, Open Sans, Lato, default system fonts, generic sans.  
- **Prefer** 2-font systems:
  - Display / personality font for headings (distinct, slightly edgy).
  - Clean, legible sans or humanist sans for body.
- **Youthful but serious** examples:
  - Display: Bricolage Grotesque, Space Grotesk, Clash Display, Sora.  
  - Body: IBM Plex Sans, Source Sans 3, Manrope.
- **Hierarchy rules**:
  - Big jumps: `h1` 2.5–3.5rem, `h2` ~1.75–2.25rem, body 0.95–1rem.  
  - Use real weight contrast (300 vs 800), not tiny 400 vs 500 changes.
- **Implementation hint**: expose typography as tokens, not one-off values.

```css
:root {
  --font-display: "Space Grotesk", system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
  --font-body: "IBM Plex Sans", system-ui, sans-serif;
}

h1, .heading-xl {
  font-family: var(--font-display);
  letter-spacing: -0.04em;
}

body {
  font-family: var(--font-body);
}
```

If using Tailwind, define custom fonts in `tailwind.config.js` and use utility classes (`font-display`, `font-body`).

---

### 2. Color & Theme (Brand + vibe)

Design with **intentional themes** instead of random rainbow gradients.

- Pick **1 dominant base**, **1–2 accent colors**, and a **background system**:
  - Youth fintech: deep charcoal background, electric lime/cyan accents, muted neutrals for surfaces.  
  - Creator/social: off-black or deep purple, saturated accents (magenta, teal), soft warm neutrals.
- Use **CSS variables** or Tailwind theme extensions to keep color consistent.
- Prefer **high contrast**, but always check accessibility (WCAG AA or better).

```css
:root {
  --color-bg: #040711;
  --color-bg-elevated: #080d1f;
  --color-accent: #8b5cf6; /* vibrant violet */
  --color-accent-soft: rgba(139, 92, 246, 0.15);
  --color-text: #f9fafb;
  --color-text-muted: #9ca3af;
  --color-danger: #f97373;
}

.button-primary {
  background: radial-gradient(circle at top left, #a855f7, #4c1d95);
  color: var(--color-text);
}

.card {
  background-color: var(--color-bg-elevated);
  border: 1px solid rgba(148, 163, 184, 0.3);
}
```

**Rules for youth + authority**:
- Use **bold accents in small doses** (buttons, key stats, active states).  
- Keep surfaces mostly dark or neutral to let accents pop.  
- Let color communicate status: success, warning, danger are crisp and saturated.

---

### 3. Motion & Micro‑interactions

Motion should feel **smooth, purposeful, and slightly playful**.

- Use motion to:
  - Guide attention (entering content, notifications, toasts).  
  - Confirm actions (button presses, success states).  
  - Communicate system status (loading, transitions).
- Avoid:
  - Constant bouncing, spinning, or flashing.  
  - Motion that blocks interaction.

**Patterns**:
- Buttons: scale 0.97 on press, 1.03 on hover, with easing and short duration.  
- Cards: subtle lift + shadow shift on hover.  
- Page transitions: quick fade + slide, ≤ 250ms.

```css
.button-primary {
  transition: transform 150ms cubic-bezier(0.16, 1, 0.3, 1),
              box-shadow 150ms ease;
}

.button-primary:hover {
  transform: translateY(-1px) scale(1.02);
}

.button-primary:active {
  transform: translateY(0) scale(0.97);
}

.card-hover {
  transition: transform 200ms ease, box-shadow 200ms ease;
}

.card-hover:hover {
  transform: translateY(-2px);
  box-shadow: 0 18px 40px rgba(15, 23, 42, 0.7);
}
```

For React, prefer CSS transitions or simple libraries (Framer Motion) instead of custom JS animation loops.

---

### 4. Backgrounds & Depth

Backgrounds are where you break out of the generic mold.

- Replace flat white with:
  - Soft gradients anchored to the corners.  
  - Noise/texture layers at very low opacity.  
  - Subtle radial glows behind important content.
- Keep contrast: foreground content must stay crystal clear.

```css
.app-shell {
  min-height: 100vh;
  background:
    radial-gradient(circle at top left, rgba(139, 92, 246, 0.25), transparent 55%),
    radial-gradient(circle at bottom right, rgba(56, 189, 248, 0.18), transparent 55%),
    #020617;
}

.bg-noise {
  position: fixed;
  inset: 0;
  pointer-events: none;
  opacity: 0.12;
  mix-blend-mode: soft-light;
  background-image: url("/textures/noise.png");
}
```

**Guideline**: 1–2 strong background ideas max. Don’t stack five gradients and SVG blobs.

---

### 5. Layout & Components

- Use **clear, opinionated layouts**:
  - Sticky top nav for primary navigation.  
  - Left rail (or compact bottom nav on mobile) for key actions.  
  - Responsive grid for cards and content.
- Make primary actions visually obvious (color, size, placement).
- Group content into **digestible sections** with clear headings.

Example React + Tailwind layout sketch:

```jsx
export function AppShell({ children }) {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-50">
      <header className="sticky top-0 z-40 border-b border-slate-800 bg-slate-950/80 backdrop-blur">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-3">
          <span className="font-display text-xl tracking-tight">global<span className="text-violet-400">1</span>sim</span>
          <nav className="flex gap-6 text-sm text-slate-300">
            <button className="hover:text-white">Dashboard</button>
            <button className="hover:text-white">SIMs</button>
            <button className="hover:text-white">Usage</button>
          </nav>
        </div>
      </header>
      <main className="mx-auto flex max-w-6xl gap-6 px-4 py-6">
        {children}
      </main>
    </div>
  );
}
```

---

### 6. Responsiveness & Accessibility

Youthful design still honors **accessibility and performance**:

- Design **mobile-first**, then scale up.  
- Tap targets ≥ 44×44px; avoid tiny icons as only targets.  
- Respect prefers-reduced-motion and prefers-color-scheme.  
- Maintain color contrast; don’t rely only on color for status.

On every screen you generate, quickly check:
- Is the primary action obvious on mobile?  
- Can users read this in low-light, low-brightness contexts?  
- Does motion feel smooth on mid-range devices?

---

## Anti‑Patterns (What to Avoid)

Avoid these defaults unless the user explicitly asks for them:

- "AI slop" layout: centered hero + three cards + bland CTA with purple gradient.
- Overused fonts: Inter, Roboto, generic system fonts as the *only* typefaces.
- Unstyled HTML form controls with random spacing and misaligned labels.
- Walls of text with no hierarchy, line-height, or whitespace.
- Animations that feel like a loading screen from 2010.

When you catch yourself drifting into these, stop and re-apply this skill:
- Re-pick fonts.  
- Re-define the theme.  
- Re-think motion with intent.

---

## How This Skill Integrates

- Combine with **`youth-brand-ux`** (separate skill) when decisions involve flows, onboarding, or product copy.
- When asked to "make it cleaner" or "more modern", interpret that as:
  - Increase typographic hierarchy.  
  - Simplify color usage.  
  - Clarify layout and spacing.  
  - Introduce subtle, meaningful motion.

**LLM Instruction**: When generating frontend code, load this skill and explicitly walk through: **Typography → Theme → Motion → Backgrounds → Layout → Accessibility** before finalizing your answer.