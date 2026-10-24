# The 5 Dead Tells of AI-Generated Design & Grounding Heuristics

Derived from Anthropic and SOTA design studio audits to eradicate generated clichés.

## 🚨 The 5 Commonest AI Tells

AI-generated interfaces repeatedly cluster around these predictable defaults:

1. **The Warm Cream / Terracotta Cliche**:
   - Background near `#F4F1EA` with high-contrast serif display and warm clay accent near `#D97757` (Claude's default interaction accent).
   - **Correction**: Choose an authentic palette drawn directly from the client's industry, materials, and domain.

2. **The Terminal Acid-Green / Vermilion Dark Mode**:
   - Near-black `#0B0B0B` background with a single neon acid-green or hot vermilion accent.
   - **Correction**: Calibrated OKLCH dark mode palettes with proper surface elevation and subtle cool/warm undertones.

3. **The Broadsheet / Newspaper Hairline Trap**:
   - Zero border-radius, dense columns, hairline 1px rules across every single item.
   - **Correction**: Hierarchy governed by whitespace, typography scale, and card elevation rather than continuous dividers.

4. **The Monotonous SaaS-Card Kit**:
   - Content chopped into identical rounded cards (`rounded-xl`), uniform border-radius on everything regardless of hierarchy, same soft grey shadow (`rgba(0,0,0,0.08)`), and random gradient washes as filler decoration.
   - **Correction**: Vary density by importance. Primary user journeys live in prominent canvases; secondary information is grouped or flat.

5. **Template Chrome & Punctuation Clichés**:
   - Tracked-out `ALL-CAPS` eyebrow label above every heading (`FEATURE — overview`).
   - Meta strings joined with middle dots (`A · B · C`).
   - Meaningless numbered badges (`01 / 02 / 03`) on items that are not sequential processes.
   - Appending `→` to every single button or link.

---

## 📐 Grounding Designs in Real Subject Matter

- **Identity First**: A design for a children's educational app must look aesthetically lightyears away from a quantitative hedge fund terminal.
- **Copywriting is Design**: Avoid marketing filler like "Streamline your workflow with next-gen AI". Write plain, human verbs: "Export invoice", "Review changes".
- **Typographic Discipline**: Keep body line lengths below 80 characters. Let serifs have slightly more line-height than sans-serifs. Never accent a random single word in a headline with bold or italic.
