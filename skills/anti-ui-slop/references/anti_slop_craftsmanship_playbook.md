# Anti-UI Slop & Master Craftsmanship Playbook

> **Scope**: Elimination of AI-generated interface clichés, the 4-layer color architecture, perceptual elevation, micro-interaction physics, and tabular typography.

---

## 1. 🚨 The 5 Dead Tells of AI-Generated UI Slop

AI code generators repeatedly default to predictable visual patterns. Real software craft requires intentionality:

### 1.1 The `transition-all` Reflow Trap
- **The AI Tell**: Appending `transition-all duration-300` indiscriminately to buttons, cards, and nav items.
- **Why It's Harmful**: `transition-all` animates expensive layout geometry properties (`width`, `height`, `padding`, `margin`), forcing composite thread drops, layout re-evaluations, and jank.
- **The Craft Fix**: Always animate targeted, GPU-composited properties:
  ```css
  /* Good: GPU accelerated opacity and transform */
  transition: opacity 150ms cubic-bezier(0.16, 1, 0.3, 1), transform 150ms cubic-bezier(0.16, 1, 0.3, 1);
  ```
  In Tailwind: `transition-colors duration-150` or `transition-transform duration-150`.

---

### 1.2 The Monotonous Indigo/Violet Palette
- **The AI Tell**: Defaulting every SaaS product to `bg-indigo-600` or `text-violet-500` with raw `#000000` dark mode.
- **Why It's Harmful**: Erodes product distinctiveness and signals low-effort prototype generation.
- **The Craft Fix**: Choose authentic domain-grounded palettes (e.g. Zinc Craft, Warm Stone, Slate Enterprise, Obsidian Emerald) structured across 4 functional layers.

---

### 1.3 The SaaS Card Soup & Hairline Overload
- **The AI Tell**: Chopping every screen into identical `rounded-xl shadow-md p-6 border border-gray-200` boxes with hairline dividers (`border-b`) under every single row.
- **The Craft Fix**: Structure hierarchy through **whitespace and typography scale**, not boxes inside boxes. Let the primary user journey occupy a prominent canvas; secondary details remain flat or grouped under quiet labels.

---

### 1.4 Marketing Buzzword Copywriting
- **The AI Tell**: Filling hero sections with:
  - *"Streamline your workflow with our next-gen all-in-one AI platform."*
  - *"Supercharge your productivity effortlessly."*
- **The Craft Fix**: Write clear, active, human verbs:
  - *"Create, send, and track client invoices in 60 seconds."*
  - *"Filter 12,000 product SKUs across Belgian supermarkets."*

---

### 1.5 Template Chrome & Punctuation Clichés
- **The AI Tells**:
  - Tracked-out all-caps eyebrows: `FEATURE — OVERVIEW`.
  - Adding middle dots everywhere: `Doc · 12 min · Active`.
  - Arbitrary numbered badges: `01 / 02 / 03` on unordered lists.
  - Appending `→` or `->` to every single button label.
- **The Craft Fix**: Let typography weight and spatial proximity establish grouping. Reserve numbers strictly for chronological or dependency-ordered workflows.

---

## 2. 🏛️ The 4-Layer Color Architecture

Rather than arbitrary hex codes, maintain 4 distinct perceptual layers in both light and dark modes:

```
┌────────────────────────────────────────────────────────┐
│  Layer 1: Canvas Background (--bg-canvas)              │
│  Light: #fafafa  |  Dark: #09090b                      │
├────────────────────────────────────────────────────────┤
│  Layer 2: Surface Elevation (--bg-surface)             │
│  Light: #ffffff  |  Dark: #121215 (Z-index light climb)│
├────────────────────────────────────────────────────────┤
│  Layer 3: Stroke & Border (--border-subtle)            │
│  Light: #e4e4e7  |  Dark: #27272a                      │
├────────────────────────────────────────────────────────┤
│  Layer 4: Accent Action (--accent-primary)             │
│  Light: #18181b  |  Dark: #fafafa (High contrast)      │
└────────────────────────────────────────────────────────┘
```

> [!IMPORTANT]
> **Dark Mode Elevation**: In dark mode, higher elements climb in luminance (`#09090b` $\to$ `#121215` $\to$ `#18181b`). Never blindly invert light mode colors or use pure pitch black `#000000` as the canvas.

---

## 3. 🔢 Tabular Figures & Typography Discipline

- **Numeric Metrics**: Always add `tabular-nums` or `font-mono` when displaying prices, counters, timestamps, or percentages. Without tabular figures, numbers shift horizontally whenever a digit changes, causing noticeable visual jitter.
- **Line Lengths**: Restrict paragraph widths to a maximum of 65-75 characters (`max-w-prose` or `max-w-xl`).
- **Headlines**: Never bold a single random word in a headline. Maintain uniform font-weight across the phrase.

---

## 4. ⚡ Micro-Interactions & Accessible State Machines

Every interactive button, row, and input must satisfy a 4-state matrix:

| State | Visual Treatment | Implementation Requirement |
| :--- | :--- | :--- |
| **Normal** | Layer 4 / Subtle surface | Base styling with contrast $\ge 4.5:1$. |
| **Hover** | 5-10% luminance shift | `hover:bg-accent/90`, `hover:border-strong`. |
| **Active / Press** | Subtle scale compression | `active:scale-[0.98]` with `cubic-bezier(0.16, 1, 0.3, 1)`. |
| **Focus-Visible** | High-contrast double ring | **Mandatory**: `focus-visible:ring-2 focus-visible:ring-offset-2`. Never leave `focus:outline-none` bare! |
| **Disabled** | 40% opacity, `cursor-not-allowed` | `disabled:opacity-40 disabled:pointer-events-none`. |

---

## 5. 🛠️ Deterministic Tooling Guide (WAT Framework)

This skill provides 2 production CLI scripts:

```bash
# 1. Scan codebase for AI slop, transition-all, and accessibility violations
python scripts/scan_ui_slop.py ./src

# 2. Generate 4-layer design tokens in CSS, Tailwind, or JSON
python scripts/generate_ui_tokens.py --theme zinc-craft --format css
python scripts/generate_ui_tokens.py --theme slate-enterprise --format tailwind
```
