# 02 — AST Reference-Aware Restructuring Protocol

## 🎯 Objective
Safely insert or delete rows and columns across multi-sheet workbooks without corrupting cell coordinates, formula ranges, or generating `#REF!` errors.

---

## 🧩 The Structural Editing Dilemma
In standard Excel scripting, inserting rows/columns via raw libraries often creates silent bugs:
- Formulas pointing below the inserted index must shift downwards (e.g. `SUM(B5:B15)` -> `SUM(B7:B17)` if 2 rows are added).
- Absolute references (`$A$1`, `B$5`, `$C10`) must preserve their lock semantics while shifting numerically along the modified axis.
- Multi-sheet references (`'Assumptions'!$B$5`) must only shift if their targeted worksheet matches the edited sheet.

---

## 🛠️ The AST Tokenizer Solution

Instead of relying on fragile regex substitutions, the engine parses every formula string into an **Abstract Syntax Tree (AST)** using `openpyxl.formula.tokenizer.Tokenizer`:

```python
from openpyxl.formula.tokenizer import Tokenizer

tok = Tokenizer("=SUM(Sheet2!A1:B10) + $C$5")
for token in tok.items:
    if token.type == "OPERAND" and token.subtype == "RANGE":
        # Dissect coordinates and apply vector translation
        pass
```

### Translation Mechanics:
1. **Row Insert at `idx` with count `k`:**
   - For all cells with `row >= idx`, new row is `row + k`.
2. **Row Delete at `idx` with count `k`:**
   - If `idx <= row < idx + k`, cell reference evaluates to `#REF!`.
   - If `row >= idx + k`, new row is `row - k`.
3. **Column Operations:**
   - Identical logic translated across alphabetical column indices (`A` -> 1, `Z` -> 26, `AA` -> 27).

---

## 🛡️ Metadata Shifting
The restructuring engine also updates non-cell structures:
- `ws.merged_cells.ranges` (avoids broken merged header boundaries)
- `ws.auto_filter.ref` (adjusts filter range)
- `ws.freeze_panes` (retains user scroll locks)
- Native Excel tables (`tbl`)
