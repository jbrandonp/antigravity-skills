---
name: office-document-architect
description: "Master Enterprise Office Document Generation Suite for Microsoft Excel (.xlsx), Word (.docx), and PowerPoint (.pptx). Enforces professional formatting, native formulas, openpyxl architecture, docx-js / python-docx report compilation, pptxgenjs slide decks, headless LibreOffice validation, and zero file corruption."
category: productivity
risk: safe
tags: ["office", "excel", "docx", "pptx", "word", "powerpoint", "openpyxl", "pptxgenjs", "spreadsheets", "presentations"]
---

# Master Enterprise Office Document Generation Suite

The authoritative engineering playbook for creating, editing, and validating production-grade Microsoft Office documents:
- **Excel Workbooks (`.xlsx`, `.xlsm`)**: OpenPyXL, native formulas, auto-fit widths, frozen panes, zebra striping.
- **Word Documents (`.docx`, `.dotx`)**: Structured reports, styles, numbering, tables of contents, image runs.
- **PowerPoint Decks (`.pptx`, `.potx`)**: High-impact presentations, native charts, layout coordinate systems, master slides.

---

## 📊 1. Excel Architecture Standards (OpenPyXL)

# Excel Architect (OpenPyXL Production Standard)

The reference engineering playbook for generating flawless, business-grade Excel (`.xlsx`) workbooks using Python and `openpyxl`. Perfectly aligned with Brandon's ecosystem preferences (`openpyxl` by default).

---

## 📊 The 5 Excel Architecture Standards

```text
 ┌─────────────────────────────────────────────────────────────┐
 │ 1. Visual Hierarchy & Theme Colors (Dark headers, Zebra rows)│
 ├─────────────────────────────────────────────────────────────┤
 │ 2. Dynamic Auto-Fit Columns (No ### display truncation)     │
 ├─────────────────────────────────────────────────────────────┤
 │ 3. Frozen Panes & Auto-Filters (Professional UX)            │
 ├─────────────────────────────────────────────────────────────┤
 │ 4. Native Formula Engine (SUM, AVERAGE, UPPERCASE syntax)    │
 ├─────────────────────────────────────────────────────────────┤
 │ 5. Number Formatting ($#,##0.00, DD/MM/YYYY, 0.0%)          │
 └─────────────────────────────────────────────────────────────┘
```

### Standard 1: Styling & Typography
- Font: Use clean system fonts like `Segoe UI`, `Calibri`, or `Aptos`.
- Header Row: Dark background (`#1F4E79` or `#2E4053`) with white bold text.
- Alternating Rows: Subtle zebra striping (`#F8F9F9` or `#F2F4F4`) to enhance readability across hundreds of rows.

### Standard 2: Auto-Fitting Column Widths
- Never leave columns at default width (leading to truncated strings or `###` numeric overflow).
- Iterate through each column, calculate `max(len(str(val))) + 3`, and apply dynamically.

### Standard 3: Freeze Panes & Filters
- Header row must always be frozen: `ws.freeze_panes = "A2"`.
- Table filters must be explicitly declared on the data range: `ws.auto_filter.ref = ws.dimensions`.

### Standard 4: Native Excel Formulas
- Write native uppercase formulas: `=SUM(C2:C50)`, `=AVERAGE(D2:D50)`, `=XLOOKUP(...)`.
- Let Excel compute values natively; do not hardcode calculated totals into formula cells.

---

## 🛠️ Deterministic Tooling

```bash
# Validate an existing Excel workbook for professional criteria
python scripts/validate_excel_output.py --file supermarket_prices.xlsx

# Generate an example professional Excel workbook
python scripts/validate_excel_output.py --demo
```

---

## 📄 2. Word Document Standards (`.docx`, `.dotx`)

# DOCX creation, editing, and analysis

A `.docx` is a ZIP archive of XML files. Choose your approach by task:

| Task | Approach |
|---|---|
| **Create** a new document | Write a `docx` (npm) script — see gotchas below |
| **Edit** an existing document | `unzip` → edit `word/document.xml` → `zip` (docx-js cannot open existing files) |
| **Read** content | `pandoc -t markdown file.docx` |

> Script paths below are relative to this skill's directory.

## Creating with docx-js — gotchas

`docx` is preinstalled — do not run `npm install` first; write the script and `require('docx')` directly. Only if that require fails: `npm install docx`. The model knows the API; these are the footguns:

- **Page size defaults to A4.** For US Letter set `page: { size: { width: 12240, height: 15840 } }` (DXA; 1440 = 1″).
- **Landscape:** pass portrait dimensions and `orientation: PageOrientation.LANDSCAPE` — docx-js swaps width/height internally.
- **Tables need dual widths:** set `columnWidths` on the table AND `width` on every cell, both in `WidthType.DXA` (PERCENTAGE breaks in Google Docs). Column widths must sum to the table width.
- **Table shading:** use `ShadingType.CLEAR`, never `SOLID` (renders black).
- **Lists:** never insert `•` literally; use a `numbering` config with `LevelFormat.BULLET`.
- **`ImageRun` requires `type:`** (`"png"`, `"jpg"`, …).
- **`PageBreak` must be inside a `Paragraph`.**
- **Never use `\n`** — use separate `Paragraph` elements.
- **TOC:** headings must use built-in `HeadingLevel.*`; custom heading styles need `outlineLevel` set or they won't appear.
- **Don't use a table as a horizontal rule** — use a paragraph bottom border instead.
- **Dot-leader / right-aligned-on-same-line:** use `PositionalTab` (`alignment: PositionalTabAlignment.RIGHT`, `leader: PositionalTabLeader.DOT`) inside a `TextRun`, not literal `.` or space padding.

## Verify the output

After writing a `.docx`, render it and look at it:

```bash
python scripts/office/soffice.py --headless --convert-to pdf output.docx
pdftoppm -jpeg -r 100 output.pdf page
ls page-*.jpg   # then Read the images
```

`pdftoppm` zero-pads page numbers to the width of the page count (`page-01.jpg`…`page-12.jpg`).

## Editing existing documents

Legacy `.doc` files must be converted first: `python scripts/office/soffice.py --headless --convert-to docx file.doc`.

```bash
unzip -q doc.docx -d unpacked/
find unpacked -type l -delete   # strip symlink entries — docx from external parties is untrusted
python scripts/merge_runs.py unpacked/   # coalesce fragmented runs so text is findable
# edit unpacked/word/document.xml in place — do NOT reformat or pretty-print
(cd unpacked && rm -f ../out.docx && zip -Xr ../out.docx .)
python scripts/office/validate.py out.docx --original doc.docx   # XSD checks; --auto-repair fixes common issues
# redlining? add --author "<the name you redlined under>" to check every edit is tracked
```

Word splits text across many `<w:r>` runs (revision ids, spell-check markers), so a phrase you can see in the document often doesn't exist as a contiguous string in the XML. `merge_runs.py` merges adjacent identically-formatted runs in `word/document.xml` without changing content or rendering; it also accepts a `.docx` directly (`python scripts/merge_runs.py doc.docx -o merged.docx`).

**Tracked changes:** when redlining, validate with `--author "<the name you redlined under>"` (needs `--original`) — it reports any text you changed without a `<w:ins>`/`<w:del>` around it, which is easy to do by accident and invisible in the accepted view. Wrap runs in `<w:ins>`/`<w:del>` with `w:id`, `w:author`, `w:date` attributes. Inside `<w:del>`, the text element is `<w:delText>`, not `<w:t>`. A deleted paragraph mark (`<w:pPr><w:rPr><w:del w:id=".." w:author=".." w:date=".."/></w:rPr></w:pPr>`) means "merge this paragraph into the next" — so deleting a paragraph outright is that plus a `<w:del>` around every run. The `<w:del/>` must come before the rPr's other children; their order is schema-enforced.

To produce a clean copy with all tracked changes accepted: `python scripts/accept_changes.py in.docx out.docx`.

Accepting a deleted paragraph mark should join that paragraph to the one below it, so a paragraph whose runs are *all* deleted vanishes. Word does this; `accept_changes.py` and `pandoc --track-changes=accept` don't always. Both fail the same way — they strip the deleted text but leave the emptied paragraph behind, which reads as a stray empty bullet when it was auto-numbered:

- `pandoc --track-changes=accept` never joins the paragraphs.
- `accept_changes.py` (LibreOffice) joins them correctly, except when the deleted paragraph is followed by an empty spacer paragraph.

An empty bullet in either view is an artifact of that view, not a defect in the document. Check paragraph deletions in the XML.

## Comments

Comments require six cross-linked files. Use the helper — directory mode when you'll also be editing `document.xml` (saves an unzip/rezip cycle), `.docx`-direct mode otherwise:

```bash
# Against an already-unpacked directory (preferred when also placing markers)
python scripts/comment.py unpacked/ "Fees & expenses cap is too low"
python scripts/comment.py unpacked/ "Agreed" --parent 0

# Against a .docx directly
python scripts/comment.py contract.docx "This cap is too low" -o annotated.docx
```

The script writes `comments.xml`, `commentsExtended.xml`, `commentsIds.xml`, `commentsExtensible.xml`, the relationships, and the content-type overrides. Comment IDs are auto-assigned. It then prints the `<w:commentRangeStart>`/`<w:commentRangeEnd>`/`<w:commentReference>` snippet to add to `word/document.xml` so the comment anchors to specific text — until you place those markers, the comment exists but is not visible.

## Dependencies

`docx` (npm, preinstalled — install only if `require('docx')` fails) · `pandoc` · LibreOffice (`soffice`) · `pdftoppm` (Poppler)

---

## 📽️ 3. PowerPoint Presentation Standards (`.pptx`, `.potx`)

# PPTX creation, editing, and analysis

A `.pptx` is a ZIP archive of XML files. Choose your approach by task:

| Task | Approach |
|---|---|
| **Create** a new deck | Write a `pptxgenjs` script — see gotchas below |
| **Edit** an existing deck, or build from a template | unzip → edit `ppt/slides/slideN.xml` → zip |
| **Read** content | `markitdown deck.pptx` (one block per slide under `<!-- Slide number: N -->` markers); visual grid: `python scripts/thumbnail.py deck.pptx` |

## Scripts

Paths are relative to this skill's directory. Everything else is plain Python, `node`, or shell.

| Script | What it does |
|---|---|
| `scripts/thumbnail.py deck.pptx [prefix]` | Labeled grid of every slide, for picking template layouts. `.pptx` only. Pass `prefix` — it defaults to `thumbnails`, which overwrites the grids of any other deck done in the same directory |
| `scripts/add_slide.py unpacked/ slide2.xml [--after slideN.xml]` | Duplicate a slide (or a `slideLayoutN.xml`) with all the package bookkeeping. Also takes a `.pptx` directly with `-o out.pptx` |
| `scripts/clean.py unpacked/` | Delete slides, media, and rels no longer referenced. Run **after** `<p:sldIdLst>` is final |
| `scripts/office/validate.py deck.pptx [--original src.pptx]` | Schema, relationship, content-type, chart and slide checks; each failure names its fix. Pass `--original` for any template-derived deck — it baselines the schema checks against the template, so the template's own XSD errors don't read as yours |
| `scripts/office/soffice.py --headless --convert-to pdf deck.pptx` | LibreOffice wrapper — bare `soffice` hangs in this sandbox |

## Creating with pptxgenjs — gotchas

`pptxgenjs` is preinstalled — do not run `npm install` first; write the script and `require('pptxgenjs')` directly. Only if that require fails: `npm install pptxgenjs`. The model knows the API; these are the footguns:

- **Set `pres.layout` before adding slides.** The default canvas is `LAYOUT_16x9` = **10" × 5.625"**, not 13.3" wide. Coordinates past the edge are written, not clamped — the shape just isn't on the slide. (`LAYOUT_WIDE` is 13.3" × 7.5".)
- **Hex colors: never `#`, never 8 digits.** `color: "FF0000"`. Both `"#FF0000"` and alpha baked into the hex (`"00000020"`) **corrupt the file**. For translucency: `transparency: 0-100` on fills and images, `opacity: 0.0-1.0` on shadows — each is silently ignored on the other.
- **pptxgenjs mutates option objects in place** (converts values to EMU on first use). Never share one `shadow`/options object across two `add*` calls — build a fresh object each time.
- **Shadow `offset` must be ≥ 0** — a negative offset corrupts the file. To cast a shadow upward, use `angle: 270` with a positive offset.
- **`letterSpacing` is silently ignored** — the real option is `charSpacing`.
- **Lists:** `bullet: true` on each item, never a literal `•` (renders double bullets). Set `breakLine: true` on every array item except the last. Space bulleted paragraphs with `paraSpaceAfter`, not `lineSpacing` (huge gaps).
- **One `new pptxgen()` per output file** — never reuse an instance.
- **`rectRadius` only works on `ROUNDED_RECTANGLE`**, not `RECTANGLE`.
- **Gradient fills aren't supported** — use a gradient image as the background instead.
- **Text boxes have built-in internal padding** — set `margin: 0` whenever text must align with a shape, line, or icon at the same x.
- **Speaker notes go in `slide.addNotes("...")`** (plain text, once per slide), never in a text box on the slide.
- **Keep charts native.** Use `addChart()` for everything PowerPoint can chart (pass an array of `{type, data, options}` for combos). For PowerPoint-native features the library doesn't expose (trendlines, error bars), compute the extra series yourself or post-process the generated OOXML — do not fall back to a rendered image. Only chart types PowerPoint has no native form for (Sankey, network, chord) go in as images.
- **Default charts render bare** — no title, no data labels, dated palette. Set `showTitle` + `title`, `showValue: true` + `dataLabelPosition`, `chartColors: [...]` from your palette, and quiet the frame (`catAxisLabelColor`/`valAxisLabelColor`, `valGridLine: { color, size }`, `catGridLine: { style: "none" }`, `showLegend: false` for a single series).
- **On a stacked bar or column chart, `dataLabelPosition` must be `ctr`, `inEnd`, or `inBase`.** `outEnd` **corrupts the file**.
- **A combo series using `secondaryValAxis`/`secondaryCatAxis` needs both `valAxes` and `catAxes` on the chart options, two entries each.** Without them pptxgenjs writes axis *ids* it never declares, and PowerPoint **discards that chart** and reports the file as corrupt. Supplying only `valAxes` is not enough.
- **After `writeFile()`, run `python scripts/office/validate.py deck.pptx`.** It reports the two chart faults above and the slide-XML defects PowerPoint refuses, and names the fix for each. Fix them in your generator, not by hand-editing the packed XML.
- **Never reorder the children of `<p:presentation>`.** pptxgenjs writes `<p:notesMasterIdLst>` right after `<p:sldIdLst>` and points both masters at one theme part. PowerPoint reads that happily — move the element and the same deck becomes unopenable.
- **Icons:** render `react-icons` to SVG (`ReactDOMServer.renderToStaticMarkup`), rasterize with `sharp` at ≥256px, and insert via `addImage({ data: "image/png;base64," + buf.toString("base64") })` — the `image/png;base64,` prefix is required (`react-icons`, `react`, `react-dom`, and `sharp` are preinstalled — `npm install react-icons react react-dom sharp` only if a require fails).

## Editing existing decks and templates

Pick layouts first: `python scripts/thumbnail.py template.pptx template-thumbs` writes a labeled grid of every slide and prints the file(s) it created — `template-thumbs.jpg`, split into `template-thumbs-N.jpg` past 12 slides. **Always pass that second argument, named after the deck.** It defaults to `thumbnails`, so two decks thumbnailed in one directory silently overwrite each other's grids — the first deck's are simply gone (template analysis only — visual QA needs the full-resolution renders from [Converting to Images](#converting-to-images); it only accepts `.pptx`, so copy a `.potx` to a `.pptx` name first). Use it with `markitdown` to map each content section onto a template slide, and vary the layouts — don't put every section on the same title-and-bullets slide.

```bash
python3 -c "import sys,zipfile; zipfile.ZipFile(sys.argv[1]).extractall('unpacked')" deck.pptx
python scripts/add_slide.py unpacked/ slide2.xml --after slide2.xml   # duplicate a slide (or slideLayoutN.xml); prints the new slide's path
# reorder / delete slides = edit <p:sldIdLst> in ppt/presentation.xml
python scripts/clean.py unpacked/                                     # after deletions: removes orphaned slides, media, rels
# edit slide content in ppt/slides/slideN.xml
(cd unpacked && rm -f ../out.pptx && zip -Xr ../out.pptx .)           # zip from INSIDE the dir; rm first or deleted parts survive
python scripts/office/validate.py out.pptx --original deck.pptx
```

- **Do all structural work — add, delete, reorder — before editing any slide's content.** `add_slide.py` copies a slide file verbatim, so duplicating after you edit clones the edited content; and `clean.py` deletes any slide missing from `<p:sldIdLst>`, including one you just wrote.
- **Never copy a slide file by hand** — `add_slide.py` does every registration a new slide needs and reports what it made (`Created ppt/slides/slide17.xml from slide2.xml`). It also works directly on a file: `add_slide.py deck.pptx slide2.xml -o out.pptx` — **pass `-o`, or it rewrites the input deck in place.** A duplicated slide still *references* its source's chart/SmartArt/embedded-object parts rather than cloning them, so editing one slide's chart changes the other's.
- **If you use `python-pptx`**, three things it won't do: duplicate a slide (its only entry point is `add_slide(layout)`), preserve formatting through `text_frame.text = "..."` (that collapses the paragraph to a single unstyled run — assign `run.text` instead), or read the SVG/EMF most template art uses (`add_picture` raises `UnidentifiedImageError`).
- Legacy `.ppt` must be converted first: `python scripts/office/soffice.py --headless --convert-to pptx file.ppt`. `.potx` templates unpack and pack identically — keep the `.potx` extension on the output.
- To reuse a template icon or image, duplicate a slide or layout that already contains it.

When filling in a template:

- If you script an XML transform, parse with `defusedxml.minidom` — round-tripping OOXML through `xml.etree.ElementTree` rewrites namespace prefixes and corrupts the deck.
- **Template slots ≠ source items.** If the template shows 4 team members and you have 3, delete the 4th member's entire group (image + text boxes), not just its text — then check for orphaned visuals in QA.
- One `<a:p>` per list item — never concatenate items into a single paragraph. Copy the sibling `<a:pPr>` to preserve spacing, and put `b="1"` on the `<a:rPr>` of titles, section headers, and inline labels (`Status:`, `Owner:`).
- Let bullets inherit from the layout; only add `<a:buChar>`, `<a:buAutoNum>` (numbered), or `<a:buNone>` to override — never a literal `•` in the text.
- Text with leading or trailing spaces needs `xml:space="preserve"` on its `<a:t>`.

## Design Ideas

**Don't create boring slides.** Plain bullets on a white background won't impress anyone. Consider ideas from this list for each slide.

### Before Starting

- **Pick a bold, content-informed color palette**: The palette should feel designed for THIS topic. If swapping your colors into a completely different presentation would still "work," you haven't made specific enough choices.
- **Dominance over equality**: One color should dominate (60-70% visual weight), with 1-2 supporting tones and one sharp accent. Never give all colors equal weight.
- **Dark/light contrast**: Dark backgrounds for title + conclusion slides, light for content ("sandwich" structure). Or commit to dark throughout for a premium feel.
- **Commit to a visual motif**: Pick ONE distinctive element and repeat it — rounded image frames, icons in colored circles. Carry it across every slide. **Do not use a color bar or accent stripe as your motif** (see Avoid list).

### Color Palettes

Choose colors that match your topic — don't default to generic blue. Use these palettes as inspiration:

| Theme | Primary | Secondary | Accent |
|-------|---------|-----------|--------|
| **Midnight Executive** | `1E2761` (navy) | `CADCFC` (ice blue) | `FFFFFF` (white) |
| **Forest & Moss** | `2C5F2D` (forest) | `97BC62` (moss) | `F5F5F5` (cream) |
| **Coral Energy** | `F96167` (coral) | `F9E795` (gold) | `2F3C7E` (navy) |
| **Warm Terracotta** | `B85042` (terracotta) | `E7E8D1` (sand) | `A7BEAE` (sage) |
| **Ocean Gradient** | `065A82` (deep blue) | `1C7293` (teal) | `21295C` (midnight) |
| **Charcoal Minimal** | `36454F` (charcoal) | `F2F2F2` (off-white) | `212121` (black) |
| **Teal Trust** | `028090` (teal) | `00A896` (seafoam) | `02C39A` (mint) |
| **Berry & Cream** | `6D2E46` (berry) | `A26769` (dusty rose) | `ECE2D0` (cream) |
| **Sage Calm** | `84B59F` (sage) | `69A297` (eucalyptus) | `50808E` (slate) |
| **Cherry Bold** | `990011` (cherry) | `FCF6F5` (off-white) | `2F3C7E` (navy) |

### For Each Slide

**Every slide needs a visual element** — image, chart, icon, or shape. Text-only slides are forgettable.

**Layout options:**
- Two-column (text left, illustration on right)
- Icon + text rows (icon in colored circle, bold header, description below)
- 2x2 or 2x3 grid (image on one side, grid of content blocks on other)
- Half-bleed image (full left or right side) with content overlay

**Data display:**
- Large stat callouts (big numbers 60-72pt with small labels below)
- Comparison columns (before/after, pros/cons, side-by-side options)
- Timeline or process flow (numbered steps, arrows)

**Visual polish:**
- Icons in small colored circles next to section headers
- Italic accent text for key stats or taglines

### Typography

**Font names you write into the .pptx are rendered by the user's PowerPoint, not by this environment.** Your visual QA renders via LibreOffice, which substitutes fonts it doesn't have — and for some fonts the substitute has different widths, so your QA preview can show text overflow (or fit) that the real deck won't have. To keep your QA trustworthy:

- **Safe fonts** (render true-to-width in QA *and* ship with Office): **Arial, Calibri, Cambria, Times New Roman, Courier New, Bookman Old Style, Century Schoolbook**. Use these for body text and anything where fit matters.
- **Headers with personality at zero QA risk**: pair a safe-list serif header (Cambria, Bookman Old Style, Century Schoolbook) with a safe-list sans body (Calibri or Arial). You get visual contrast without giving up reliable overflow checks.
- **If the user asks for a font outside the safe list** (e.g. Georgia or Trebuchet MS): use it where the user asked, but size those containers with extra slack (~10%) and don't trust QA text-fit on those elements — the preview of that font is approximate. If the user hasn't specified, prefer safe-list fonts for body text.
- **QA-unreliable fonts** (substitute has different widths — overflow checks can be wrong): Georgia, Trebuchet MS, Impact, Arial Black, Garamond, Consolas, Palatino Linotype. Calibri Light substitution varies by environment; treat as QA-unreliable. Fine for titles/accents with slack; don't trust QA text-fit on these.
- **Never default to Aptos** — Office's post-2023 default has no metric-compatible substitute here *and* is missing from older Office installs, so it's unreliable on both ends.

| Element | Size |
|---------|------|
| Slide title | 36-44pt bold |
| Section header | 20-24pt bold |
| Body text | 14-16pt |
| Captions | 10-12pt muted |

### Spacing

- 0.5" minimum margins
- 0.3-0.5" between content blocks
- Leave breathing room—don't fill every inch

### Avoid (Common Mistakes)

- **Don't repeat the same layout** — vary columns, cards, and callouts across slides
- **Don't center body text** — left-align paragraphs and lists; center only titles
- **Don't skimp on size contrast** — titles need 36pt+ to stand out from 14-16pt body
- **Don't default to blue** — pick colors that reflect the specific topic
- **Don't mix spacing randomly** — choose 0.3" or 0.5" gaps and use consistently
- **Don't style one slide and leave the rest plain** — commit fully or keep it simple throughout
- **Don't create text-only slides** — add images, icons, charts, or visual elements; avoid plain title + bullets
- **Don't forget text box padding** — when aligning lines or shapes with text edges, set `margin: 0` on the text box or offset the shape to account for padding
- **Don't use low-contrast elements** — icons AND text need strong contrast against the background; avoid light text on light backgrounds or dark text on dark backgrounds
- **NEVER use accent lines under titles** — these are a hallmark of AI-generated slides; use whitespace or background color instead
- **NEVER add decorative color bars or accent stripes** — this includes: header/footer bars spanning the slide width, vertical sidebar stripes down one edge of the slide, thin accent stripes along one edge of a card or content block, and "single-side borders" on rectangles. These read as AI-generated filler. If you want to set a card apart, use a subtle background tint, a drop shadow, or an icon — not an edge stripe.
- **Don't default to cream/beige backgrounds** — when no background is specified, use white (`FFFFFF`) or the user's brand palette; avoid warm-neutral defaults like `F5F5DC`, `FAF0E6`, `FAEBD7`, `FFF8E1`
- **Don't ship text that overflows its shape** — if text doesn't fit, reduce font size, split across slides, or enlarge the container; never leave content cut off or spilling past bounds

## QA (Required)

Your first render usually has a few real issues — overlaps, overflow, misalignment. Find and fix those, re-render only the slides you changed, and stop.

### Content QA

```bash
markitdown output.pptx
```

Check for missing content, typos, wrong order.

**When using templates, check for leftover placeholder text:**

```bash
markitdown output.pptx | grep -iE "\bx{3,}\b|lorem|ipsum|\bTODO|\[insert|this.*(page|slide).*layout"
```

If grep returns results, fix them before declaring success.

### File QA (required)

```bash
python scripts/office/validate.py output.pptx                      # built from scratch
python scripts/office/validate.py output.pptx --original src.pptx  # built from a template
```

**If the deck came from a template, always pass `--original`.** A template may itself
contain parts the XSD rejects, so a bare run can report failures you never caused — and
a genuine regression can hide among them. `--original` baselines
the schema and slide checks against the template, suppressing errors it already had.
The structural checks — relationships, content types, charts — ignore `--original` and
report template-inherited problems either way, so read those on their own merits.

pptxgenjs emits chart XML PowerPoint refuses to open, and every other tool
accepts: python-pptx opens those decks, LibreOffice renders them, the XSD
passes them. Every failure names its fix. Fix it in the generator and rebuild.

### Visual QA

Convert the slides to images (see [Converting to Images](#converting-to-images)) and inspect every one. After staring at the generating code you tend to see what you expect rather than what rendered, so look at the images fresh (a subagent works well for this if you have one). User-visible defects to look for:

- **Text overflow or text cut off at a box or slide boundary — check this first.** It is the most common defect and always user-visible. (For a font the previewer renders unreliably per Typography, the preview is approximate: trust the ~10% slack you left, not its apparent fit.)
- Overlapping elements (text through shapes, lines through words, stacked elements)
- Source citations or footers colliding with content above
- Elements too close (< 0.3" gaps) or cards/sections nearly touching
- Uneven gaps (large empty area in one place, cramped in another)
- Insufficient margin from slide edges (< 0.5")
- Columns or similar elements not aligned consistently
- Low-contrast text (e.g., light gray text on cream-colored background)
- Template decoration mispositioned after text replacement — e.g., a title underline positioned for one line, but the replaced title wrapped to two
- Low-contrast icons (e.g., dark icons on dark backgrounds without a contrasting circle)
- Text boxes too narrow causing excessive wrapping
- Leftover placeholder content

## Converting to Images

Convert presentations to individual slide images for visual inspection:

```bash
python scripts/office/soffice.py --headless --convert-to pdf output.pptx
rm -f slide-*.jpg
pdftoppm -jpeg -r 150 output.pdf slide
ls -1 "$PWD"/slide-*.jpg
```

**Pass the absolute paths printed above directly to the view tool.** The `rm` clears stale images from prior runs. `pdftoppm` zero-pads based on page count: `slide-1.jpg` for decks under 10 pages, `slide-01.jpg` for 10-99, `slide-001.jpg` for 100+.

**After fixes, rerun all four commands above** — the PDF must be regenerated from the edited `.pptx` before `pdftoppm` can reflect your changes.

## Dependencies

`pptxgenjs` (npm, preinstalled — install only if `require('pptxgenjs')` fails) · `markitdown[pptx]`, `Pillow`, `defusedxml`, `lxml` (pip — text dump, thumbnail, clean, validate) · LibreOffice (`soffice`, auto-configured for sandboxed environments via `scripts/office/soffice.py`) · `pdftoppm` (Poppler)
