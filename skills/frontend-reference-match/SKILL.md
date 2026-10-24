---
name: frontend-reference-match
description: Exact reference-matching frontend reproduction pipeline. Enforces strict visual matching, local serving (http://localhost:3000), multi-round Puppeteer screenshot diffing, and anti-generic craft guardrails (banning default Tailwind palettes, flat shadows, and transition-all).
---

# Frontend Reference Match: Exact Visual Replication & Craft Guardrails

This skill enforces pixel-level visual fidelity when reproducing user interfaces from reference images, accompanied by strict anti-generic design guardrails.

## The First Imperative

- **Match Reference Images Exactly**: If a reference screenshot or mock is provided, replicate its layout, spacing, typography, hierarchy, and palette with zero deviation.
- **Do Not "Improve" or Re-invent**: Keep sections, component structures, and copy faithful to the source. Swap in placeholder content (`https://placehold.co/WIDTHxHEIGHT`) only where original assets are unavailable.

---

## The Screenshot Verification Loop

```
[Write/Edit index.html]
       │
       ▼
 1. Serve on Localhost (node serve.mjs -> http://localhost:3000)
    * Never screenshot file:/// URLs (breaks fonts, CORS, and SVG filters)
       │
       ▼
 2. Capture Viewport (node screenshot.mjs http://localhost:3000 [label])
    * Outputs to: ./temporary screenshots/screenshot-N.png
       │
       ▼
 3. Visual Diffing Round (Inspect image with Read tool)
    * Measure exact discrepancies: font weight, line-height, padding, gaps, hex codes
       │
       ▼
 4. Fix Code & Re-Screenshot (Execute at least 2 comparison rounds)
       │
       ▼
 [Stop only when visual matches reference or user approves]
```

---

## Anti-Generic Craft Guardrails

When creating or matching frontend components, strictly enforce these quality standards:

1. **Colors**:
   - **Banned**: Default Tailwind blues/indigos (`bg-blue-600`, `bg-indigo-500`, etc.).
   - **Required**: Derive a deliberate, brand-specific palette. Use calibrated neutrals (`#09090b`, `#18181b`, `#fafafa`) tinted with the primary hue.

2. **Shadows**:
   - **Banned**: Flat `shadow-md` or `shadow-lg`.
   - **Required**: Layered, multi-stop shadows with color tinting and low opacity (e.g. `0 2px 5px rgba(0,0,0,0.4), 0 8px 24px rgba(0,0,0,0.3)`).

3. **Typography**:
   - **Banned**: Single generic font across the entire document.
   - **Required**: Pair a high-character display font for headings with a legible sans for body. Apply tight negative tracking (`letter-spacing: -0.03em`) on titles and generous line-height (`1.6 - 1.7`) on paragraphs.

4. **Gradients & Surface Depth**:
   - Layer multiple radial gradients to simulate real light sources.
   - Add subtle SVG noise texture for analog richness.
   - Build a defined elevation hierarchy: Base surface -> Elevated card -> Floating popover/modal.

5. **Animations & Transitions**:
   - **Banned**: `transition-all` (causes layout thrashing and jitter).
   - **Required**: Animate strictly GPU-accelerated properties: `transform` and `opacity`. Use spring or bezier easing curves (`cubic-bezier(0.16, 1, 0.3, 1)`).

6. **Micro-Interactions**:
   - Every clickable element must declare distinct `:hover`, `:focus-visible`, and `:active` pseudo-states.