---
name: excel-architect
description: Design and generate production-grade Excel spreadsheets (.xlsx) using openpyxl. Enforces professional styling, native formulas (SUM, AVERAGE, XLOOKUP), auto-fit column widths, freeze panes, data filters, and zebra-striping without file corruption.
---

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