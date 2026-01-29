# Design Specification: "We Got This" Landing Page

This document finalizes the layout, information architecture, and user stories for the "Acme Inc" Israeli landing page.

## 1. Information Architecture (The "Scan" Flow)
Since we are using an **RTL (Right-to-Left)** layout, the user's eye will follow a "Z-pattern" starting from the top-right.

### Layout Map:
| Section | Location | Content / Element | Purpose |
| :--- | :--- | :--- | :--- |
| **Header** | Top-Right | **Logo** | Brand recognition. |
| **Header** | Top-Left | **Sign In / CTA** | Immediate action for returning users. |
| **Hero** | Right Side | **Headline & Subtext** | The "Fixer" promise (Hebrew). |
| **Hero** | Left Side | **Animated Card Fan** | Visual "Wow" factor and engagement. |
| **Hero** | Below Text | **Primary CTA Button** | Conversion (e.g., "בואו נתחיל"). |
| **Trust Bar** | Full Width | **Local Logos** | "Trusted by 500+ Israeli companies." |
| **Features** | Grid (RTL) | **3-Column Grid** | Benefits: Speed, Reliability, Local Support. |
| **Social Proof** | Center | **Hebrew Testimonials** | Validating the "We Got This" claim. |
| **Footer** | Bottom-Right | **Contact / Links** | Standard navigation. |
| **Floating** | Bottom-Left | **WhatsApp Icon** | Immediate human connection. |

## 2. User Stories
These stories define *why* someone is on the site and what they expect to achieve.

### Story A: The "In-a-Hurry" Startup Founder (Itay)
- **Persona**: Tech-savvy, values efficiency, hates "fluff."
- **Goal**: Find a reliable connection service for his team *now*.
- **User Journey**: Enters site -> Scans Hero headline -> Sees "Trusted by [Local Startup]" -> Clicks Primary CTA within 10 seconds.
- **"We Got This" Moment**: The snappy 300ms animation and direct copy convince him we won't waste his time.

### Story B: The "Skeptical" Operations Manager (Noa)
- **Persona**: Detail-oriented, looking for reliability and support.
- **Goal**: Ensure the service has local support and won't fail during peak hours.
- **User Journey**: Enters site -> Scrolls to Features -> Reads about "24/7 Hebrew Support" -> Sees WhatsApp button -> Clicks WhatsApp to ask a quick question.
- **"We Got This" Moment**: Seeing the WhatsApp icon and the "Israeli-based team" badge.

### Story C: The "New User" Explorer (Yossi)
- **Persona**: Not sure what he needs yet, browsing options.
- **Goal**: Understand the value proposition without feeling pressured.
- **User Journey**: Enters site -> Watches the Hero animation -> Scrolls through Popular Destinations -> Reads a testimonial -> Clicks "How it Works" (Secondary CTA).
- **"We Got This" Moment**: The "Card Fanning" animation reveals information in a clean, non-overwhelming way.

## 3. Design Principles for Minimalism
- **One Goal per Section**: Each scroll depth should have a single focus (e.g., Hero = Action, Features = Value).
- **Visual Breathing Room**: Use at least `64px` of vertical padding between sections to maintain the premium feel.
- **Color as a Guide**: Use the primary brand color *only* for CTAs and key highlights to guide the eye.

---
*Design Specification by Antigravity.*
