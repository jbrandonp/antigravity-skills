# LinkedIn Visual & Image Engineering Specifications

Visual assets on LinkedIn are not decoration—they are **attention amplifiers and scroll-stoppers**. An ill-proportioned or low-contrast image ruins mobile dwell time.

---

## 1. The 5-Dimension Image Scoring Rubric (/25)

Before attaching an image to any LinkedIn publication, audit it across these 5 criteria:

| Dimension | Weight | Description | 5/5 Benchmark | 1/5 Disqualification |
| :--- | :---: | :--- | :--- | :--- |
| **1. Mobile Contrast & Legibility** | 5 pts | Text readability on 5-inch smartphone screens. | Minimum 24pt bold typography, dark text on pure white or light text on #0D1117. High luminance contrast ($> 4.5:1$). | Tiny 10pt text, muddy grey-on-black, illegible spreadsheet screenshots. |
| **2. Authority & Ground Truth** | 5 pts | Authenticity of the visual proof. | Real terminal output, verified architecture schema, handwritten whiteboard sketch, actual production metrics. | Generic Unsplash stock photos (handshakes, smiling business models in glass offices). |
| **3. Scroll-Stopping Velocity** | 5 pts | Visual hook stopping thumb scroll within 500ms. | Sharp geometric contrast, isolated visual focal point, unexpected diagram or bug trace. | Bland decorative gradient, centered corporate logo. |
| **4. Standalone Value Density** | 5 pts | Can a practitioner learn something from the image alone? | Complete standalone mental model, flow chart, or before/after code diff. | Decorative banner that adds zero new information. |
| **5. Mobile Aspect Ratio** | 5 pts | Screen real estate occupied on mobile devices. | **Vertical 4:5 ($1200 \times 1500$ px)** or **Square 1:1 ($1200 \times 1200$ px)**. | **Horizontal 16:9 ($1200 \times 627$ px)** — wastes 60% of vertical mobile viewport. |

*Passing Score: ≥ 20/25. Anything below 18/25 should either be improved or published as text-only.*

---

## 2. Technical Aspect Ratio & Resolution Specs

```
   Vertical (4:5)          Square (1:1)         Horizontal (16:9)
  1200 x 1500 px          1200 x 1200 px          1200 x 627 px
┌──────────────────┐    ┌──────────────────┐    ┌──────────────────────────┐
│                  │    │                  │    │   [PENALIZED ON MOBILE]  │
│  ⭐ RECOMMENDED  │    │  ⭐ BEST FOR     │    └──────────────────────────┘
│  Occupies 80% of │    │  SCHEMATICS &    │
│  mobile screen   │    │  CODE SNIPPETS   │
│                  │    │                  │
└──────────────────┘    └──────────────────┘
```

### Format Summary
- **Vertical 4:5 ($1200 \times 1500$ px):** Optimal for infographics, bulleted frameworks, and step-by-step guides.
- **Square 1:1 ($1200 \times 1200$ px):** Standard for system diagrams, UI component mockups, and terminal windows.
- **Carousel PDF ($1080 \times 1350$ px):** Strictly 4:5 ratio exported as a multi-page PDF document.
- **File Format:** Lossless PNG for text/diagrams; WebP/JPEG (quality 90+) for photos.

---

## 3. Blacklisted Visual Slop

Never generate or attach:
- ❌ Stereotypical corporate stock imagery (executives shaking hands, women with headsets, businessmen pointing at charts).
- ❌ Synthetic AI uncanny-valley humans with distorted fingers or plastic skin.
- ❌ Unformatted raw terminal dumps with dark grey text on black backgrounds that cannot be read in daylight.
- ❌ Dense Excel spreadsheets scaled down to fit an image card.
