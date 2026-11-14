# 03 — Dirty ERP Data Cleaning & Mathematical Reconciliation Protocol

## 🎯 Objective
Transform corrupted, poorly formatted raw exports from accounting and ERP software (SAP, NetSuite, Sage, Salesforce, Odoo) into pristine, typed Excel datasets while enforcing a mandatory mathematical zero-loss gate: **`Delta = 0.00`**.

---

## 🌪️ The Real-World Data Pathologies
Raw enterprise spreadsheets typically feature:
1. **Misplaced Banners & Titles:** Top 3–5 rows filled with export timestamps, company logos, and merged banner headers before the true table begins.
2. **Merged Category Spans:** Category names placed in a merged cell across multiple sub-rows, causing subsequent rows to read as `None`.
3. **Corrupted Numeric & Currency Formats:** Values exported as text strings with mixed spacing and punctuation (e.g. `" 1 450,50 € "`, `"$1,200.00"`, `"(450.00)"` for negatives).
4. **Intermediate Subtotal Rows:** Inlined sum rows that lead to accidental double-counting if summed naively.

---

## 🧹 The 4-Stage Cleaning Pipeline

### Stage 1: Header Row Detection (Heuristic Density)
Scans the first 25 rows to identify the row with:
- Maximum density of non-numeric textual labels.
- Minimum merged cell spans.
- At least 2 populated columns.

### Stage 2: Dénormalisation & Forward-Fill
Unmerges grouped header blocks and propagates parent category labels downwards into every active transaction row.

### Stage 3: Currency & Date Coercion
Applies a strict decimal parser:
- Detects parenthesized accounting negatives: `(125.50)` -> `-125.50`.
- Normalizes European vs US comma/period conventions (`1.250,50` vs `1,250.50`).
- Converts strings into typed Python `Decimal` objects.

### Stage 4: The Zero-Tolerance Reconciliation Gate (`Δ = 0.00`)
```text
  Raw Workbook Total Numeric Sum:     4,520,150.75 €
- Cleaned DataFrame Total Numeric Sum: 4,520,150.75 €
------------------------------------------------------
  Discrepancy Delta (Δ):                     0.00 €  --> PASS ✓
```
If `|Raw_Sum - Clean_Sum| > 0.0001`, execution is immediately aborted and the discrepancy reported, preventing any silent dropping of ledger entries.
