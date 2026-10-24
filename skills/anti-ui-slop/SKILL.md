---
name: anti-ui-slop
description: 'Master Anti-UI Slop & UI Design Pro System. Eliminates generic AI-generated interfaces and builds production-grade software by combining UIZZE 800,000+ real web and iOS screens with 25+ foundational design laws across color theory (4-layer system, OKLCH, dark mode), layout, typography, cards, spacing, and micro-interactions. Use when designing, redesigning, polishing, critiquing, or pre-ship reviewing web or mobile apps. Trigger with "anti-ui-slop", "stop UI slop", "ui-design-pro", "ground this UI", "make it look professional", or "run the UI finish gate".'
license: MIT
metadata:
  version: "2.0.0"
  author: "UIZZE and Design Pro Master Suite"
  compatibility: "Universal coding agent skill (Antigravity, Claude Code, Cursor, Copilot)"
  tags: "ui-design, design-system, design-laws, anti-slop, frontend, web-ui, ios-ui"
---

> **Stop AI coding agents from shipping generic UI. Build intentional, trustworthy software that converts.**

# Anti-UI-Slop & UI Design Pro Master Suite

This skill transforms rough, AI-generated, or amateur UI into polished, production-grade software. It bridges two complementary paradigms:
1. **Evidence-Based Real Screens**: Grounding UI in real, working product patterns (800,000+ screens via UIZZE).
2. **Deterministic Design Laws**: 25+ mathematical and perceptual design rules encoded in `reference/design-laws.md` covering the 4-layer color system, OKLCH scales, typography hierarchies, card density, and micro-interactions.

---

## 1. The 25 Actionable Design Laws (`reference/design-laws.md`)

When designing, refining, or auditing any interface, enforce the foundational principles in `reference/design-laws.md`:

### Color Science & Contrast
- **4-Layer Color System**: Distinguish canvas background, card surface, border definition, and accent actions. Never use pure black (`#000000`) or flat grey on white.
- **Perceptual Uniformity (OKLCH)**: Maintain consistent perceived brightness across hues.
- **Dark Mode Elevation**: Increase surface lightness with z-index elevation; do not invert blindly.

### Layout, Spacing & Density
- **Consistent Spacing Scale**: Base layout on 4px/8px multiples (`gap-2`, `gap-4`, `gap-6`, `gap-8`).
- **Visual Hierarchy**: Headlines guide, labels orient, body informs. Ensure minimum contrast ratios (WCAG 2.2 AA).
- **Cards & Containers**: Avoid nested border soups; use subtle borders (`border-neutral-200 dark:border-neutral-800`) or elevation shadows, never harsh outlines.

### Micro-Interactions & Polish
- **Active State Feedback**: Every clickable element requires hover, active, focus-visible, and disabled states.
- **Predictable Transitions**: Keep durations between 150ms-250ms with `cubic-bezier(0.16, 1, 0.3, 1)`. Avoid generic `transition-all`.

---

## 2. Real-World Screen Playbooks (`reference/`)

Choose the specific playbook for your current task:

- **New Interface or Major Redesign**: `reference/new-work.md`
- **Product, SaaS & Dashboard Work**: `reference/operate.md`
- **Refinement, Elevation & Polish**: `reference/polish.md`
- **Simplification & Distillation**: `reference/distill.md`
- **Formal Interface Audit**: `reference/audit.md`
- **Native iOS / Mobile Screens**: `reference/ios.md`
- **Deep Design Laws & Tokens**: `reference/design-laws.md`

Do not load multiple playbooks at once. Apply focused architectural judgment rather than treating checklists as mindless busywork.

---

## 3. Work from the Product Context

Always read the user brief, existing UI tokens, components, and brand guidelines before writing code. Existing product conventions outrank generic defaults.
- Do not add novelty for its own sake.
- Make the product's primary user journey obvious within 3 seconds of viewing.
- Eliminate redundant badges, empty decorative cards, and generic stock illustrations.

---

## 4. The UI Finish Gate

Before completing any UI task:
1. **Visual QA**: Inspect layout in desktop and mobile viewport widths.
2. **Text Clipping**: Verify long strings and localized text do not overflow or truncate destructively.
3. **Contrast Verification**: Ensure text meets 4.5:1 ratio against its immediate container background.
4. **State Completeness**: Ensure loading skeleton, empty state, and error message states are defined.
