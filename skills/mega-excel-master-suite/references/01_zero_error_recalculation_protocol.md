# 01 — Zero-Error Recalculation & OpenXML Integrity Protocol

## 🎯 Objective
Guarantee that every `.xlsx` / `.xlsm` spreadsheet produced by an AI agent evaluates cleanly with **zero formula errors** (`#REF!`, `#DIV/0!`, `#VALUE!`, `#NAME?`, `#SPILL!`, `#NULL!`, `#NUM!`, `#N/A`), has its `<v>` cache tags properly populated, and retains external link integrity.

---

## ⚙️ The OpenXML Storage Trap: `<f>` vs `<v>`
In the OpenXML specification (`xl/worksheets/sheet1.xml`), a formula cell is stored with two distinct elements:
```xml
<c r="C10">
    <f>SUM(C2:C9)</f>
    <v>14500.50</v>
</c>
```
1. `<f>` contains the formula expression string.
2. `<v>` contains the **cached numerical evaluation**.

### The openpyxl Limitation
When Python's `openpyxl` writes a formula to a worksheet:
- It writes the `<f>` tag verbatim.
- It leaves the `<v>` tag completely empty.

If a file is opened in Google Sheets, mobile Excel apps, or previewers without a recalculation step, **formula cells will display empty strings or zero**.

---

## 🔄 Recalculation Execution Flow

```text
┌────────────────────────────────┐
│  openpyxl writes formula (<f>) │
└───────────────┬────────────────┘
                │
                ▼
┌────────────────────────────────┐
│   Headless LibreOffice Macro   │  --> Executes ThisComponent.calculateAll()
└───────────────┬────────────────┘  --> Populates <v> cache tags in place
                │
                ▼
┌────────────────────────────────┐
│ Double-Pass openpyxl Inspector │  --> Pass 1: data_only=True scans for #ERRORS
└───────────────┬────────────────┘  --> Pass 2: data_only=False counts formulas & checks _xlfn.
                │
        ┌───────┴───────┐
        ▼               ▼
   [0 Errors]     [Errors Found]
    PASS ✓         FAIL (Returns coordinates to agent for auto-fix)
```

---

## 🛑 Modern Function Namespaces (`_xlfn.`)
Functions introduced after Excel 2007 must be prefixed with `_xlfn.` in raw OpenXML:
- `_xlfn.XLOOKUP`
- `_xlfn.LET`
- `_xlfn.LAMBDA`
- `_xlfn.FILTER`
- `_xlfn.UNIQUE`
- `_xlfn.SORT`
- `_xlfn.SEQUENCE`
- `_xlfn.TEXTJOIN`
- `_xlfn.IFS`
- `_xlfn.SWITCH`
- `_xlfn.MAXIFS`
- `_xlfn.MINIFS`

Writing these functions bare in openpyxl without the prefix results in literal `#NAME?` errors upon opening.
