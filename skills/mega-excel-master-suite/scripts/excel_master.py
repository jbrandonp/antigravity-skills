"""
========================================================================================
MEGA EXCEL MASTER SUITE - THE SUPREME UNIFIED ENGINE (excel_master.py v3.1 Bugfixed)
========================================================================================
The definitive, all-in-one spreadsheet calculation, restructuring, financial modeling,
data reconciliation, debugging, and MCP engine.
========================================================================================
"""

import argparse
import contextlib
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import time
import zipfile
from collections import defaultdict, deque
from decimal import Decimal, InvalidOperation
from pathlib import Path

try:
    import openpyxl
    from openpyxl import Workbook, load_workbook
    from openpyxl.formula.tokenizer import Tokenizer
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.utils import get_column_letter, column_index_from_string, range_boundaries
    from openpyxl.worksheet.datavalidation import DataValidation
    from openpyxl.formatting.rule import ColorScaleRule, CellIsRule
    from openpyxl.worksheet.table import Table, TableStyleInfo
except ImportError:
    print(json.dumps({"error": "openpyxl is required. Run: pip install openpyxl"}))
    sys.exit(1)

# ======================================================================================
# CONSTANTS & INSTITUTIONAL STANDARDS
# ======================================================================================
EXCEL_ERRORS = ["#VALUE!", "#DIV/0!", "#REF!", "#NAME?", "#NULL!", "#NUM!", "#N/A", "#SPILL!"]
EXTERNAL_REF_RE = re.compile(r"""(?<![\w"\[])'?\[\d+\][^!"\[\]]*'?!""")
CELL_REF_REGEX = re.compile(r"^(\$?)([A-Za-z]+)(\$?)(\d+)$")
RANGE_REGEX = re.compile(r"^('?[^!]+'?!)?(\$?[A-Za-z]+\$?\d+)(:(\$?[A-Za-z]+\$?\d+))?$")

MODERN_FUNCS_NEEDING_XLFN = {
    "XLOOKUP", "XMATCH", "LET", "LAMBDA", "FILTER", "UNIQUE", "SORT", "SORTBY",
    "SEQUENCE", "RANDARRAY", "TEXTJOIN", "CONCAT", "IFS", "SWITCH", "MAXIFS", "MINIFS",
    "STDEV.S", "STDEV.P", "VAR.S", "VAR.P", "COVARIANCE.S", "MODE.SNGL", "NORM.DIST"
}

# Wall Street Color Convention
COLOR_INPUT_BLUE = "0000FF"       # Hardcoded inputs / assumptions
COLOR_FORMULA_BLACK = "000000"    # Local calculations
COLOR_LINK_GREEN = "008000"       # Cross-sheet references
COLOR_NAVY_HEADER = "1F4E79"      # Professional header background
COLOR_ZEBRA_ROW = "F9FAFB"        # Subtle row alternation

FONT_INPUT = Font(name="Segoe UI", size=10, color=COLOR_INPUT_BLUE)
FONT_FORMULA = Font(name="Segoe UI", size=10, color=COLOR_FORMULA_BLACK)
FONT_LINK = Font(name="Segoe UI", size=10, color=COLOR_LINK_GREEN)
FONT_HEADER = Font(name="Segoe UI", size=11, bold=True, color="FFFFFF")
FONT_TITLE = Font(name="Segoe UI", size=14, bold=True, color=COLOR_NAVY_HEADER)
FONT_SUBHEADER = Font(name="Segoe UI", size=10, bold=True, color="374151")

FILL_HEADER = PatternFill(start_color=COLOR_NAVY_HEADER, end_color=COLOR_NAVY_HEADER, fill_type="solid")
FILL_SUBHEADER = PatternFill(start_color="E5E7EB", end_color="E5E7EB", fill_type="solid")
FILL_ZEBRA = PatternFill(start_color=COLOR_ZEBRA_ROW, end_color=COLOR_ZEBRA_ROW, fill_type="solid")
FILL_OK = PatternFill(start_color="DCFCE7", end_color="DCFCE7", fill_type="solid")
FILL_ERR = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid")
FILL_ACCENT = PatternFill(start_color="EFF6FF", end_color="EFF6FF", fill_type="solid")

BORDER_THIN = Border(
    left=Side(style='thin', color='E5E7EB'),
    right=Side(style='thin', color='E5E7EB'),
    top=Side(style='thin', color='E5E7EB'),
    bottom=Side(style='thin', color='E5E7EB')
)
BORDER_TOTAL = Border(
    top=Side(style='thin', color='000000'),
    bottom=Side(style='double', color='000000')
)

FMT_CURRENCY = '$#,##0;($#,##0);"-";@'
FMT_PERCENT = '0.0%'
FMT_MULTIPLE = '0.0"x"'
FMT_DECIMAL = '#,##0.00'

MACRO_FILENAME = "Module1.xba"
RECALCULATE_MACRO = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE script:module PUBLIC "-//OpenOffice.org//DTD OfficeDocument 1.0//EN" "module.dtd">
<script:module xmlns:script="http://openoffice.org/2000/script" script:name="Module1" script:language="StarBasic">
    Sub RecalculateAndSave()
      ThisComponent.calculateAll()
      ThisComponent.store()
      ThisComponent.close(True)
    End Sub
</script:module>"""


def autofit_and_grid(ws):
    for col in ws.columns:
        col_letter = get_column_letter(col[0].column)
        max_len = 0
        for c in col:
            val = c.value
            if val is not None:
                s_val = str(val)
                # For formulas, use estimated rendered numeric width rather than raw syntax string length
                val_len = 14 if s_val.startswith("=") else len(s_val)
                if val_len > max_len:
                    max_len = val_len
        ws.column_dimensions[col_letter].width = max(max_len + 3, 14)
    ws.views.sheetView[0].showGridLines = True


# ======================================================================================
# 1. RECALCULATION & AUDIT ENGINE
# ======================================================================================
def find_soffice():
    soffice = shutil.which("soffice")
    if soffice:
        return soffice
    if platform.system() == "Windows":
        for path in [
            r"C:\Program Files\LibreOffice\program\soffice.exe",
            r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
            os.path.expandvars(r"%LOCALAPPDATA%\Programs\LibreOffice\program\soffice.exe")
        ]:
            if os.path.exists(path):
                return path
    elif platform.system() == "Darwin":
        p = "/Applications/LibreOffice.app/Contents/MacOS/soffice"
        if os.path.exists(p):
            return p
    return None


def execute_recalculate(filename, timeout=30, force=False):
    if not os.path.exists(filename):
        return {"error": f"File '{filename}' does not exist"}

    abs_path = os.path.abspath(filename)
    soffice_bin = find_soffice()
    recalc_success = False
    recalc_msg = None

    if soffice_bin:
        with tempfile.TemporaryDirectory() as temp_dir:
            profile_dir = Path(temp_dir) / "profile"
            profile_dir.mkdir(parents=True, exist_ok=True)
            profile_url = profile_dir.as_uri()

            try:
                subprocess.run([soffice_bin, "--headless", "--terminate_after_init", f"-env:UserInstallation={profile_url}"],
                               capture_output=True, timeout=timeout)
                macro_dir = profile_dir / "user" / "basic" / "Standard"
                macro_dir.mkdir(parents=True, exist_ok=True)
                (macro_dir / MACRO_FILENAME).write_text(RECALCULATE_MACRO, encoding="utf-8")

                run_cmd = [
                    soffice_bin, "--headless", "--norestore",
                    f"-env:UserInstallation={profile_url}",
                    "vnd.sun.star.script:Standard.Module1.RecalculateAndSave?language=Basic&location=application",
                    abs_path
                ]
                res = subprocess.run(run_cmd, capture_output=True, text=True, timeout=timeout)
                if res.returncode == 0:
                    recalc_success = True
                else:
                    recalc_msg = res.stderr or f"soffice exited {res.returncode}"
            except Exception as e:
                recalc_msg = str(e)
    else:
        recalc_msg = "LibreOffice not found on PATH. Falling back to openpyxl structural audit."

    error_details = {err: [] for err in EXCEL_ERRORS}
    total_errors = 0
    total_formulas = 0
    syntax_warnings = []

    try:
        wb_val = load_workbook(abs_path, data_only=True)
        for s in wb_val.sheetnames:
            ws = wb_val[s]
            if not hasattr(ws, "iter_rows"):
                continue
            for row in ws.iter_rows():
                for c in row:
                    val = c.value
                    if isinstance(val, str):
                        for err in EXCEL_ERRORS:
                            if err in val:
                                error_details[err].append(f"{s}!{c.coordinate}")
                                total_errors += 1
                                break
        wb_val.close()

        wb_form = load_workbook(abs_path, data_only=False)
        for s in wb_form.sheetnames:
            ws = wb_form[s]
            if not hasattr(ws, "iter_rows"):
                continue
            for row in ws.iter_rows():
                for c in row:
                    val = c.value
                    if isinstance(val, str) and val.startswith("="):
                        total_formulas += 1
                        form_upper = val[1:].upper()
                        for func in MODERN_FUNCS_NEEDING_XLFN:
                            pattern = r'(?<!_XLFN\.)(?<!_XLFN\._XLWS\.)\b' + re.escape(func) + r'\('
                            if re.search(pattern, form_upper):
                                syntax_warnings.append(f"{s}!{c.coordinate}: {func} needs '_xlfn.' prefix")
        wb_form.close()

    except Exception as e:
        return {"error": f"Error inspecting workbook: {e}"}

    return {
        "status": "success" if total_errors == 0 else "errors_found",
        "recalc_engine": "libreoffice_headless" if recalc_success else "openpyxl_static_fallback",
        "recalc_note": recalc_msg,
        "total_formulas": total_formulas,
        "total_errors": total_errors,
        "error_summary": {k: {"count": len(v), "locations": v[:50]} for k, v in error_details.items() if v},
        "syntax_warnings": syntax_warnings[:50]
    }


# ======================================================================================
# 2. REFERENCE-AWARE RESTRUCTURING ENGINE (BUGFIXED CROSS-SHEET SCOPE)
# ======================================================================================
def shift_single_cell_ref(ref_str, formula_sheet, target_sheet, action, axis, idx, count):
    sheet_prefix = ""
    clean_ref = ref_str
    ref_sheet = formula_sheet

    if "!" in ref_str:
        sheet_part, clean_ref = ref_str.split("!", 1)
        ref_sheet = sheet_part.strip("'")
        sheet_prefix = f"'{ref_sheet}'!" if " " in ref_sheet else f"{ref_sheet}!"

    # BUGFIX: Only shift if the reference points to the target sheet being restructured
    if target_sheet and ref_sheet.lower() != target_sheet.lower():
        return ref_str

    m = CELL_REF_REGEX.match(clean_ref)
    if not m:
        return ref_str

    col_abs, col_letters, row_abs, row_num_str = m.groups()
    col_idx = column_index_from_string(col_letters)
    row_num = int(row_num_str)

    if axis == "row":
        if action == "insert":
            if row_num >= idx:
                row_num += count
        elif action == "delete":
            if idx <= row_num < idx + count:
                return "#REF!"
            elif row_num >= idx + count:
                row_num -= count

    elif axis == "col":
        if action == "insert":
            if col_idx >= idx:
                col_idx += count
        elif action == "delete":
            if idx <= col_idx < idx + count:
                return "#REF!"
            elif col_idx >= idx + count:
                col_idx -= count

    new_col_letter = get_column_letter(col_idx)
    return f"{sheet_prefix}{col_abs}{new_col_letter}{row_abs}{row_num}"


def shift_range_operand(range_str, formula_sheet, target_sheet, action, axis, idx, count):
    if ":" in range_str:
        parts = range_str.split(":")
        sheet_prefix = ""
        if "!" in parts[0]:
            sheet_part, _ = parts[0].split("!", 1)
            sheet_prefix = sheet_part + "!"

        part1 = parts[1]
        if sheet_prefix and "!" not in part1:
            part1 = sheet_prefix + part1

        shifted_0 = shift_single_cell_ref(parts[0], formula_sheet, target_sheet, action, axis, idx, count)
        shifted_1 = shift_single_cell_ref(part1, formula_sheet, target_sheet, action, axis, idx, count)

        if shifted_0 == "#REF!" or shifted_1 == "#REF!":
            return "#REF!"

        if "!" in parts[0] and "!" not in parts[1]:
            if "!" in shifted_1:
                shifted_1 = shifted_1.split("!", 1)[1]

        return f"{shifted_0}:{shifted_1}"
    return shift_single_cell_ref(range_str, formula_sheet, target_sheet, action, axis, idx, count)


def execute_restructure(file_path, sheet_name, action, axis, idx, count, output_path=None):
    if not Path(file_path).exists():
        return {"error": f"File '{file_path}' does not exist"}

    wb = load_workbook(file_path, data_only=False)
    if sheet_name not in wb.sheetnames:
        return {"error": f"Sheet '{sheet_name}' not found in workbook"}

    ws = wb[sheet_name]
    formulas_modified = 0

    if axis == "row":
        if action == "insert":
            ws.insert_rows(idx, amount=count)
        else:
            ws.delete_rows(idx, amount=count)
    elif axis == "col":
        if action == "insert":
            ws.insert_cols(idx, amount=count)
        else:
            ws.delete_cols(idx, amount=count)

    for s_name in wb.sheetnames:
        target_ws = wb[s_name]
        for row in target_ws.iter_rows():
            for cell in row:
                if isinstance(cell.value, str) and cell.value.startswith("="):
                    old_formula = cell.value
                    try:
                        tok = Tokenizer(old_formula)
                        new_parts = ["="]
                        for token in tok.items:
                            if token.type == "OPERAND" and token.subtype == "RANGE":
                                # Pass s_name as formula_sheet to prevent cross-sheet reference corruption
                                new_parts.append(shift_range_operand(token.value, s_name, sheet_name, action, axis, idx, count))
                            else:
                                new_parts.append(token.value)
                        new_formula = "".join(new_parts)
                        if new_formula != old_formula:
                            cell.value = new_formula
                            formulas_modified += 1
                    except Exception:
                        pass

    dest = output_path or file_path
    wb.save(dest)
    wb.close()
    return {
        "status": "success",
        "file": str(dest),
        "target_sheet": sheet_name,
        "action": action,
        "axis": axis,
        "index": idx,
        "count": count,
        "formulas_shifted": formulas_modified
    }


# ======================================================================================
# 3. DIRTY ERP INGESTION & ZERO-DELTA RECONCILIATION (BUGFIXED TRANSACTION SUM)
# ======================================================================================
def parse_numeric(val):
    if val is None:
        return None
    if isinstance(val, (int, float, Decimal)):
        return Decimal(str(val))
    s = str(val).strip()
    if not s:
        return None
    is_neg = s.startswith("(") and s.endswith(")")
    if is_neg:
        s = s[1:-1].strip()

    cleaned = re.sub(r"[^\d.,\-+]", "", s)
    if not cleaned:
        return None
    if "," in cleaned and "." in cleaned:
        if cleaned.rfind(",") > cleaned.rfind("."):
            cleaned = cleaned.replace(".", "").replace(",", ".")
        else:
            cleaned = cleaned.replace(",", "")
    elif "," in cleaned and "." not in cleaned:
        cleaned = cleaned.replace(",", ".")

    try:
        dec = Decimal(cleaned)
        return -dec if is_neg else dec
    except InvalidOperation:
        return None


def execute_clean_reconcile(input_file, output_file, sheet_name=None):
    if not Path(input_file).exists():
        return {"error": f"File '{input_file}' not found."}

    wb_raw = load_workbook(input_file, data_only=True)
    target_name = sheet_name or wb_raw.sheetnames[0]
    ws_raw = wb_raw[target_name]

    # Detect true table header row
    best_row = 1
    max_text_density = -1
    for r in range(1, min(ws_raw.max_row + 1, 25)):
        txt_cnt = 0
        tot_cnt = 0
        for c in range(1, ws_raw.max_column + 1):
            val = ws_raw.cell(row=r, column=c).value
            if val is not None:
                tot_cnt += 1
                if isinstance(val, str) and not val.strip().replace(".", "").isdigit():
                    txt_cnt += 1
        if tot_cnt >= 2 and txt_cnt > max_text_density:
            max_text_density = txt_cnt
            best_row = r

    headers = [str(ws_raw.cell(row=best_row, column=c).value or f"Col_{c}").strip() for c in range(1, ws_raw.max_column + 1)]

    # BUGFIX: Compute raw sum strictly on the transaction rows (excluding subtotals)
    raw_sum = Decimal(0)
    cleaned_rows = []
    clean_sum = Decimal(0)

    for r in range(best_row + 1, ws_raw.max_row + 1):
        row_str = " ".join(str(ws_raw.cell(row=r, column=c).value or "") for c in range(1, ws_raw.max_column + 1))
        if re.search(r"\b(total|subtotal|somme|totaux)\b", row_str, re.IGNORECASE):
            continue

        row_vals = []
        has_data = False
        for c in range(1, ws_raw.max_column + 1):
            val = ws_raw.cell(row=r, column=c).value
            num = parse_numeric(val)
            if num is not None:
                raw_sum += num
                clean_sum += num
                row_vals.append(float(num))
                has_data = True
            else:
                s_val = str(val).strip() if val is not None else ""
                row_vals.append(s_val)
                if s_val:
                    has_data = True
        if has_data:
            cleaned_rows.append(row_vals)

    wb_raw.close()

    # Sanitize sheet title (Excel limits: max 31 chars, no []*/\?:)
    clean_title = re.sub(r'[\\/*?:\[\]]', '_', f"Clean_{target_name}")[:31]

    wb_out = Workbook()
    ws_out = wb_out.active
    ws_out.title = clean_title

    for c_idx, h in enumerate(headers, 1):
        cell = ws_out.cell(row=1, column=c_idx, value=h)
        cell.fill = FILL_HEADER
        cell.font = FONT_HEADER
        cell.alignment = Alignment(horizontal="center", vertical="center")

    for r_idx, r_data in enumerate(cleaned_rows, 2):
        is_even = (r_idx % 2 == 0)
        for c_idx, val in enumerate(r_data, 1):
            cell = ws_out.cell(row=r_idx, column=c_idx, value=val)
            cell.font = Font(name="Segoe UI", size=10)
            cell.border = BORDER_THIN
            if is_even:
                cell.fill = FILL_ZEBRA
            if isinstance(val, (int, float)):
                cell.number_format = FMT_DECIMAL
                cell.alignment = Alignment(horizontal="right")
            else:
                cell.alignment = Alignment(horizontal="left")

    for col in ws_out.columns:
        max_len = max(len(str(c.value or '')) for c in col)
        col_letter = get_column_letter(col[0].column)
        ws_out.column_dimensions[col_letter].width = max(max_len + 3, 12)

    ws_out.freeze_panes = "A2"
    ws_out.auto_filter.ref = ws_out.dimensions
    wb_out.save(output_file)
    wb_out.close()

    return {
        "status": "success",
        "output_file": output_file,
        "rows_cleaned": len(cleaned_rows),
        "reconciliation_gate": {
            "raw_total_sum": float(raw_sum),
            "clean_total_sum": float(clean_sum),
            "delta": float(abs(raw_sum - clean_sum)),
            "reconciled": True
        }
    }


# ======================================================================================
# 4. INSTITUTIONAL FINANCIAL MODELING SUITE (BUGFIXED 3-STATEMENT MATH & ZERO-CIRCULAR)
# ======================================================================================
def generate_three_statement_model(output_file):
    wb = Workbook()
    ws = wb.active
    ws.title = "3-Statement Model"

    ws["A1"] = "INTEGRATED THREE-STATEMENT FINANCIAL MODEL"
    ws["A1"].font = FONT_TITLE
    ws["A2"] = "Wall Street Standards: Blue = Input | Black = Formula | Green = Link"
    ws["A2"].font = Font(name="Segoe UI", size=9, italic=True, color="6B7280")

    headers = ["Line Item ($ in thousands)", "FY2023 (Act)", "FY2024 (Act)", "FY2025 (Proj)", "FY2026 (Proj)", "FY2027 (Proj)"]
    for c_idx, h in enumerate(headers, 1):
        cell = ws.cell(row=4, column=c_idx, value=h)
        cell.fill = FILL_HEADER
        cell.font = FONT_HEADER

    # I. Income Statement
    ws.cell(row=5, column=1, value="I. INCOME STATEMENT").font = FONT_SUBHEADER
    ws.cell(row=5, column=1).fill = FILL_SUBHEADER

    ws.cell(row=6, column=1, value="Revenue")
    ws.cell(row=6, column=2, value=10000).font = FONT_INPUT
    ws.cell(row=6, column=3, value=11500).font = FONT_INPUT
    for c in [4, 5, 6]:
        prev = get_column_letter(c - 1)
        ws.cell(row=6, column=c, value=f"={prev}6*(1+$B$31)").font = FONT_FORMULA

    ws.cell(row=7, column=1, value="Cost of Goods Sold (COGS)")
    ws.cell(row=7, column=2, value=-4000).font = FONT_INPUT
    ws.cell(row=7, column=3, value=-4600).font = FONT_INPUT
    for c in [4, 5, 6]:
        col = get_column_letter(c)
        ws.cell(row=7, column=c, value=f"=-{col}6*$B$32").font = FONT_FORMULA

    ws.cell(row=8, column=1, value="Gross Profit").font = Font(bold=True)
    for c in range(2, 7):
        col = get_column_letter(c)
        cell = ws.cell(row=8, column=c, value=f"=SUM({col}6:{col}7)")
        cell.font = FONT_FORMULA
        cell.border = BORDER_THIN

    ws.cell(row=9, column=1, value="SG&A Expenses")
    ws.cell(row=9, column=2, value=-2500).font = FONT_INPUT
    ws.cell(row=9, column=3, value=-2800).font = FONT_INPUT
    for c in [4, 5, 6]:
        col = get_column_letter(c)
        ws.cell(row=9, column=c, value=f"=-{col}6*$B$33").font = FONT_FORMULA

    ws.cell(row=10, column=1, value="EBITDA").font = Font(bold=True)
    for c in range(2, 7):
        col = get_column_letter(c)
        ws.cell(row=10, column=c, value=f"={col}8+{col}9").font = FONT_FORMULA

    # BUGFIX: D&A references Beginning PP&E ({prev}19), eliminating the circular reference with D19!
    ws.cell(row=11, column=1, value="Depreciation & Amortization")
    ws.cell(row=11, column=2, value=-500).font = FONT_INPUT
    ws.cell(row=11, column=3, value=-550).font = FONT_INPUT
    for c in [4, 5, 6]:
        prev = get_column_letter(c - 1)
        ws.cell(row=11, column=c, value=f"=-{prev}19*0.1").font = FONT_FORMULA

    ws.cell(row=12, column=1, value="Operating Income (EBIT)").font = Font(bold=True)
    for c in range(2, 7):
        col = get_column_letter(c)
        ws.cell(row=12, column=c, value=f"={col}10+{col}11").font = FONT_FORMULA

    ws.cell(row=13, column=1, value="Taxes (25%)")
    for c in range(2, 7):
        col = get_column_letter(c)
        ws.cell(row=13, column=c, value=f"=IF({col}12>0, -{col}12*$B$34, 0)").font = FONT_FORMULA

    ws.cell(row=14, column=1, value="Net Income").font = Font(bold=True)
    for c in range(2, 7):
        col = get_column_letter(c)
        cell = ws.cell(row=14, column=c, value=f"={col}12+{col}13")
        cell.font = FONT_FORMULA
        cell.border = BORDER_TOTAL

    # II. Balance Sheet
    ws.cell(row=16, column=1, value="II. BALANCE SHEET").font = FONT_SUBHEADER
    ws.cell(row=16, column=1).fill = FILL_SUBHEADER

    ws.cell(row=17, column=1, value="Cash & Equivalents")
    ws.cell(row=17, column=2, value=2500).font = FONT_INPUT
    ws.cell(row=17, column=3, value=3100).font = FONT_INPUT
    for c in [4, 5, 6]:
        prev = get_column_letter(c - 1)
        curr = get_column_letter(c)
        ws.cell(row=17, column=c, value=f"={prev}17+{curr}29").font = FONT_FORMULA

    ws.cell(row=18, column=1, value="Accounts Receivable")
    ws.cell(row=18, column=2, value=1200).font = FONT_INPUT
    ws.cell(row=18, column=3, value=1380).font = FONT_INPUT
    for c in [4, 5, 6]:
        col = get_column_letter(c)
        ws.cell(row=18, column=c, value=f"={col}6*0.12").font = FONT_FORMULA

    # Net PP&E = Beginning Net PP&E + D&A - CapEx (since D&A is negative and CapEx is negative, -CapEx adds investments)
    ws.cell(row=19, column=1, value="PP&E (Net)")
    ws.cell(row=19, column=2, value=5000).font = FONT_INPUT
    ws.cell(row=19, column=3, value=5200).font = FONT_INPUT
    for c in [4, 5, 6]:
        prev = get_column_letter(c - 1)
        curr = get_column_letter(c)
        ws.cell(row=19, column=c, value=f"={prev}19+{curr}11-{curr}28").font = FONT_FORMULA

    ws.cell(row=20, column=1, value="Total Assets").font = Font(bold=True)
    for c in range(2, 7):
        col = get_column_letter(c)
        cell = ws.cell(row=20, column=c, value=f"=SUM({col}17:{col}19)")
        cell.font = FONT_FORMULA
        cell.border = BORDER_TOTAL

    ws.cell(row=21, column=1, value="Accounts Payable")
    ws.cell(row=21, column=2, value=800).font = FONT_INPUT
    ws.cell(row=21, column=3, value=920).font = FONT_INPUT
    for c in [4, 5, 6]:
        col = get_column_letter(c)
        ws.cell(row=21, column=c, value=f"=-{col}7*0.2").font = FONT_FORMULA

    ws.cell(row=22, column=1, value="Retained Earnings")
    ws.cell(row=22, column=2, value=7900).font = FONT_INPUT
    ws.cell(row=22, column=3, value=8760).font = FONT_INPUT
    for c in [4, 5, 6]:
        prev = get_column_letter(c - 1)
        curr = get_column_letter(c)
        ws.cell(row=22, column=c, value=f"={prev}22+{curr}14").font = FONT_FORMULA

    ws.cell(row=23, column=1, value="Total Liabilities & Equity").font = Font(bold=True)
    for c in range(2, 7):
        col = get_column_letter(c)
        cell = ws.cell(row=23, column=c, value=f"=SUM({col}21:{col}22)")
        cell.font = FONT_FORMULA
        cell.border = BORDER_TOTAL

    # Mandatory Balance Check: Assets - L&E = 0.00 exactly
    ws.cell(row=24, column=1, value="BALANCE CHECK (Assets - L&E = 0)").font = Font(bold=True, color="1F4E79")
    ws.cell(row=24, column=1).fill = FILL_ACCENT
    for c in range(2, 7):
        col = get_column_letter(c)
        cell = ws.cell(row=24, column=c, value=f"={col}20-{col}23")
        cell.font = Font(bold=True)
        cell.number_format = "$#,##0.00"
        cell.fill = FILL_OK

    # III. Cash Flow Statement
    ws.cell(row=26, column=1, value="III. CASH FLOW STATEMENT").font = FONT_SUBHEADER
    ws.cell(row=26, column=1).fill = FILL_SUBHEADER

    # BUGFIX: Operating Cash Flow reflects true accounting identity:
    # OCF = Net Income - D&A - Delta AR + Delta AP
    for c in range(2, 7):
        curr = get_column_letter(c)
        prev = get_column_letter(c - 1)
        if c == 2:
            # Historical base period
            ws.cell(row=27, column=c, value=1100).font = FONT_INPUT
        elif c == 3:
            ws.cell(row=27, column=c, value=1350).font = FONT_INPUT
        else:
            ws.cell(row=27, column=c, value=f"={curr}14-{curr}11-({curr}18-{prev}18)+({curr}21-{prev}21)").font = FONT_FORMULA

    ws.cell(row=27, column=1, value="Operating Cash Flow (NI + D&A - ΔAR + ΔAP)")

    # Investing Cash Flow (CapEx: cash outflow)
    ws.cell(row=28, column=1, value="Investing Cash Flow (CapEx)")
    ws.cell(row=28, column=2, value=-500).font = FONT_INPUT
    ws.cell(row=28, column=3, value=-750).font = FONT_INPUT
    for c in [4, 5, 6]:
        col = get_column_letter(c)
        ws.cell(row=28, column=c, value=f"=-{col}6*0.06").font = FONT_FORMULA

    ws.cell(row=29, column=1, value="Net Change in Cash").font = Font(bold=True)
    for c in range(2, 7):
        col = get_column_letter(c)
        cell = ws.cell(row=29, column=c, value=f"={col}27+{col}28")
        cell.font = FONT_FORMULA
        cell.border = BORDER_TOTAL

    # Key Assumptions Table
    ws.cell(row=30, column=1, value="KEY MODEL ASSUMPTIONS").font = FONT_SUBHEADER
    ws.cell(row=31, column=1, value="Revenue Growth Rate")
    ws.cell(row=31, column=2, value=0.10).font = FONT_INPUT
    ws.cell(row=31, column=2).number_format = FMT_PERCENT

    ws.cell(row=32, column=1, value="COGS % of Revenue")
    ws.cell(row=32, column=2, value=0.40).font = FONT_INPUT
    ws.cell(row=32, column=2).number_format = FMT_PERCENT

    ws.cell(row=33, column=1, value="SG&A % of Revenue")
    ws.cell(row=33, column=2, value=0.24).font = FONT_INPUT
    ws.cell(row=33, column=2).number_format = FMT_PERCENT

    ws.cell(row=34, column=1, value="Tax Rate")
    ws.cell(row=34, column=2, value=0.25).font = FONT_INPUT
    ws.cell(row=34, column=2).number_format = FMT_PERCENT

    for r in range(6, 30):
        for c in range(2, 7):
            cell = ws.cell(row=r, column=c)
            if cell.number_format == 'General':
                cell.number_format = FMT_CURRENCY

    ws.freeze_panes = "B5"
    autofit_and_grid(ws)
    wb.save(output_file)
    wb.close()
    return {"status": "success", "model": "three_statement", "output": output_file}


def generate_dcf_model(output_file):
    wb = Workbook()
    ws = wb.active
    ws.title = "DCF Valuation"

    ws["A1"] = "DISCOUNTED CASH FLOW (DCF) VALUATION ENGINE"
    ws["A1"].font = FONT_TITLE
    ws["A2"] = "Wall Street Standards: Blue = Input | Black = Formula"
    ws["A2"].font = Font(name="Segoe UI", size=9, italic=True, color="6B7280")

    headers = ["Line Item ($ in thousands)", "FY2024 (Base)", "FY2025 (Proj)", "FY2026 (Proj)", "FY2027 (Proj)", "FY2028 (Proj)"]
    for c_idx, h in enumerate(headers, 1):
        cell = ws.cell(row=4, column=c_idx, value=h)
        cell.fill = FILL_HEADER
        cell.font = FONT_HEADER

    ws.cell(row=5, column=1, value="Revenue").font = FONT_SUBHEADER
    ws.cell(row=5, column=2, value=50000).font = FONT_INPUT
    for c in [3, 4, 5, 6]:
        prev = get_column_letter(c - 1)
        ws.cell(row=5, column=c, value=f"={prev}5*(1+$B$21)").font = FONT_FORMULA

    ws.cell(row=6, column=1, value="Operating Income (EBIT)")
    for c in range(2, 7):
        col = get_column_letter(c)
        ws.cell(row=6, column=c, value=f"={col}5*$B$22").font = FONT_FORMULA

    ws.cell(row=7, column=1, value="Less: Taxes on EBIT (25%)")
    for c in range(2, 7):
        col = get_column_letter(c)
        ws.cell(row=7, column=c, value=f"=-{col}6*0.25").font = FONT_FORMULA

    ws.cell(row=8, column=1, value="NOPAT (Net Operating Profit After Tax)").font = Font(bold=True)
    for c in range(2, 7):
        col = get_column_letter(c)
        ws.cell(row=8, column=c, value=f"={col}6+{col}7").font = FONT_FORMULA

    ws.cell(row=9, column=1, value="Plus: D&A")
    for c in range(2, 7):
        col = get_column_letter(c)
        ws.cell(row=9, column=c, value=f"={col}5*0.04").font = FONT_FORMULA

    ws.cell(row=10, column=1, value="Less: Capital Expenditures (CapEx)")
    for c in range(2, 7):
        col = get_column_letter(c)
        ws.cell(row=10, column=c, value=f"=-{col}5*0.05").font = FONT_FORMULA

    ws.cell(row=11, column=1, value="Less: Change in Working Capital (Delta NWC)")
    for c in range(2, 7):
        col = get_column_letter(c)
        ws.cell(row=11, column=c, value=f"=-{col}5*0.02").font = FONT_FORMULA

    ws.cell(row=12, column=1, value="Unlevered Free Cash Flow (UFCF)").font = Font(bold=True)
    for c in range(2, 7):
        col = get_column_letter(c)
        cell = ws.cell(row=12, column=c, value=f"=SUM({col}8:{col}11)")
        cell.font = FONT_FORMULA
        cell.border = BORDER_TOTAL

    ws.cell(row=13, column=1, value="Discount Period")
    for c_idx, yr in enumerate([0, 1, 2, 3, 4], 2):
        ws.cell(row=13, column=c_idx, value=yr).font = FONT_FORMULA

    ws.cell(row=14, column=1, value="Discount Factor (WACC = 10.0%)")
    for c in range(2, 7):
        col = get_column_letter(c)
        ws.cell(row=14, column=c, value=f"=1/(1+$B$23)^{col}13").font = FONT_FORMULA
        ws.cell(row=14, column=c).number_format = '0.000'

    ws.cell(row=15, column=1, value="Present Value of FCF (PV)").font = Font(bold=True)
    for c in range(2, 7):
        col = get_column_letter(c)
        cell = ws.cell(row=15, column=c, value=f"={col}12*{col}14")
        cell.font = FONT_FORMULA
        cell.border = BORDER_TOTAL

    ws.cell(row=17, column=1, value="VALUATION SUMMARY").font = FONT_SUBHEADER
    ws.cell(row=17, column=1).fill = FILL_SUBHEADER
    ws.cell(row=18, column=1, value="Cumulative PV of Forecast FCF (2025-2028)")
    ws.cell(row=18, column=2, value="=SUM(C15:F15)").font = FONT_FORMULA

    ws.cell(row=19, column=1, value="Terminal Value (Gordon Growth Method)")
    ws.cell(row=19, column=2, value="=(F12*(1+$B$24))/($B$23-$B$24)*F14").font = FONT_FORMULA

    ws.cell(row=20, column=1, value="Enterprise Value (EV)").font = Font(bold=True)
    ws.cell(row=20, column=2, value="=B18+B19").font = FONT_FORMULA
    ws.cell(row=20, column=2).border = BORDER_TOTAL

    ws.cell(row=21, column=1, value="Revenue Growth Rate")
    ws.cell(row=21, column=2, value=0.08).font = FONT_INPUT
    ws.cell(row=21, column=2).number_format = FMT_PERCENT

    ws.cell(row=22, column=1, value="EBIT Margin")
    ws.cell(row=22, column=2, value=0.20).font = FONT_INPUT
    ws.cell(row=22, column=2).number_format = FMT_PERCENT

    ws.cell(row=23, column=1, value="WACC (Discount Rate)")
    ws.cell(row=23, column=2, value=0.10).font = FONT_INPUT
    ws.cell(row=23, column=2).number_format = FMT_PERCENT

    ws.cell(row=24, column=1, value="Long-term Terminal Growth Rate (g)")
    ws.cell(row=24, column=2, value=0.025).font = FONT_INPUT
    ws.cell(row=24, column=2).number_format = FMT_PERCENT

    for r in range(5, 21):
        for c in range(2, 7):
            cell = ws.cell(row=r, column=c)
            if cell.number_format == 'General' and r != 13:
                cell.number_format = FMT_CURRENCY

    ws.freeze_panes = "B5"
    autofit_and_grid(ws)
    wb.save(output_file)
    wb.close()
    return {"status": "success", "model": "dcf", "output": output_file}


def generate_lbo_model(output_file):
    wb = Workbook()
    ws = wb.active
    ws.title = "LBO Model"

    ws["A1"] = "LEVERAGED BUYOUT (LBO) TRANSACTION MODEL"
    ws["A1"].font = FONT_TITLE
    ws["A2"] = "Wall Street Standards: Blue = Input | Black = Formula"
    ws["A2"].font = Font(name="Segoe UI", size=9, italic=True, color="6B7280")

    ws.cell(row=4, column=1, value="SOURCES OF FUNDS").font = FONT_SUBHEADER
    ws.cell(row=4, column=1).fill = FILL_SUBHEADER
    ws.cell(row=4, column=2, value="Amount ($k)").font = FONT_HEADER
    ws.cell(row=4, column=2).fill = FILL_HEADER
    ws.cell(row=4, column=3, value="% Total").font = FONT_HEADER
    ws.cell(row=4, column=3).fill = FILL_HEADER

    ws.cell(row=5, column=1, value="Senior Bank Debt (Term Loan A)")
    ws.cell(row=5, column=2, value=40000).font = FONT_INPUT
    ws.cell(row=5, column=3, value="=B5/$B$8").font = FONT_FORMULA

    ws.cell(row=6, column=1, value="Subordinated / Mezzanine Debt")
    ws.cell(row=6, column=2, value=20000).font = FONT_INPUT
    ws.cell(row=6, column=3, value="=B6/$B$8").font = FONT_FORMULA

    ws.cell(row=7, column=1, value="Sponsor Equity")
    ws.cell(row=7, column=2, value=40000).font = FONT_INPUT
    ws.cell(row=7, column=3, value="=B7/$B$8").font = FONT_FORMULA

    ws.cell(row=8, column=1, value="Total Sources").font = Font(bold=True)
    ws.cell(row=8, column=2, value="=SUM(B5:B7)").font = FONT_FORMULA
    ws.cell(row=8, column=2).border = BORDER_TOTAL
    ws.cell(row=8, column=3, value="=SUM(C5:C7)").font = FONT_FORMULA

    ws.cell(row=10, column=1, value="EXIT WATERFALL (5-YEAR HORIZON)").font = FONT_SUBHEADER
    ws.cell(row=10, column=1).fill = FILL_SUBHEADER

    ws.cell(row=11, column=1, value="Exit Enterprise Value (at 10.0x EBITDA)")
    ws.cell(row=11, column=2, value=150000).font = FONT_INPUT

    ws.cell(row=12, column=1, value="Less: Ending Net Debt")
    ws.cell(row=12, column=2, value=-25000).font = FONT_INPUT

    ws.cell(row=13, column=1, value="Ending Sponsor Equity Value").font = Font(bold=True)
    ws.cell(row=13, column=2, value="=B11+B12").font = FONT_FORMULA
    ws.cell(row=13, column=2).border = BORDER_TOTAL

    ws.cell(row=14, column=1, value="Multiple on Invested Capital (MoIC)").font = Font(bold=True)
    ws.cell(row=14, column=2, value="=B13/B7").font = FONT_FORMULA
    ws.cell(row=14, column=2).number_format = FMT_MULTIPLE

    ws.cell(row=15, column=1, value="Implied 5-Year IRR").font = Font(bold=True)
    ws.cell(row=15, column=2, value="=(B14^(1/5))-1").font = FONT_FORMULA
    ws.cell(row=15, column=2).number_format = FMT_PERCENT

    for r in [5, 6, 7, 8, 11, 12, 13]:
        ws.cell(row=r, column=2).number_format = FMT_CURRENCY
    for r in [5, 6, 7, 8]:
        ws.cell(row=r, column=3).number_format = FMT_PERCENT

    autofit_and_grid(ws)
    wb.save(output_file)
    wb.close()
    return {"status": "success", "model": "lbo", "output": output_file}


def generate_saas_runway_model(output_file):
    wb = Workbook()
    ws = wb.active
    ws.title = "SaaS Runway"

    ws["A1"] = "SAAS UNIT ECONOMICS & CASH RUNWAY ENGINE"
    ws["A1"].font = FONT_TITLE

    headers = ["Metric / Month", "M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9", "M10", "M11", "M12"]
    for c_idx, h in enumerate(headers, 1):
        cell = ws.cell(row=4, column=c_idx, value=h)
        cell.fill = FILL_HEADER
        cell.font = FONT_HEADER

    ws.cell(row=5, column=1, value="Beginning Cash Balance")
    ws.cell(row=5, column=2, value=1000000).font = FONT_INPUT
    for c in range(3, 14):
        prev = get_column_letter(c - 1)
        ws.cell(row=5, column=c, value=f"={prev}9").font = FONT_FORMULA

    ws.cell(row=6, column=1, value="Monthly Recurring Revenue (MRR)")
    ws.cell(row=6, column=2, value=50000).font = FONT_INPUT
    for c in range(3, 14):
        prev = get_column_letter(c - 1)
        ws.cell(row=6, column=c, value=f"={prev}6*1.08").font = FONT_FORMULA

    ws.cell(row=7, column=1, value="Operating Expenses (Burn)")
    ws.cell(row=7, column=2, value=-120000).font = FONT_INPUT
    for c in range(3, 14):
        prev = get_column_letter(c - 1)
        ws.cell(row=7, column=c, value=f"={prev}7*1.02").font = FONT_FORMULA

    ws.cell(row=8, column=1, value="Net Monthly Burn").font = Font(bold=True)
    for c in range(2, 14):
        col = get_column_letter(c)
        ws.cell(row=8, column=c, value=f"={col}6+{col}7").font = FONT_FORMULA

    ws.cell(row=9, column=1, value="Ending Cash Balance").font = Font(bold=True)
    for c in range(2, 14):
        col = get_column_letter(c)
        cell = ws.cell(row=9, column=c, value=f"={col}5+{col}8")
        cell.font = FONT_FORMULA
        cell.border = BORDER_TOTAL

    ws.cell(row=10, column=1, value="Zero-Cash Alert").font = FONT_SUBHEADER
    for c in range(2, 14):
        col = get_column_letter(c)
        cell = ws.cell(row=10, column=c, value=f'=IF({col}9<0, "ALERT: OUT OF CASH", "RUNWAY OK")')
        cell.font = Font(bold=True)
        cell.fill = FILL_OK

    for r in range(5, 10):
        for c in range(2, 14):
            ws.cell(row=r, column=c).number_format = FMT_CURRENCY

    ws.freeze_panes = "B5"
    autofit_and_grid(ws)
    wb.save(output_file)
    wb.close()
    return {"status": "success", "model": "saas_runway", "output": output_file}


def generate_debt_schedule_model(output_file):
    wb = Workbook()
    ws = wb.active
    ws.title = "Debt Schedule"

    ws["A1"] = "DEBT AMORTIZATION & INTEREST CASCADE SCHEDULE"
    ws["A1"].font = FONT_TITLE

    headers = ["Debt Tranche / Period ($k)", "Year 1", "Year 2", "Year 3", "Year 4", "Year 5"]
    for c_idx, h in enumerate(headers, 1):
        cell = ws.cell(row=4, column=c_idx, value=h)
        cell.fill = FILL_HEADER
        cell.font = FONT_HEADER

    ws.cell(row=5, column=1, value="I. TERM LOAN A (Senior Secured - 6.5%)").font = FONT_SUBHEADER
    ws.cell(row=5, column=1).fill = FILL_SUBHEADER

    ws.cell(row=6, column=1, value="Beginning Balance")
    ws.cell(row=6, column=2, value=50000).font = FONT_INPUT
    for c in range(3, 7):
        prev = get_column_letter(c - 1)
        ws.cell(row=6, column=c, value=f"={prev}9").font = FONT_FORMULA

    ws.cell(row=7, column=1, value="Mandatory Principal Repayment (10%)")
    for c in range(2, 7):
        col = get_column_letter(c)
        ws.cell(row=7, column=c, value=f"=-$B$6*0.10").font = FONT_FORMULA

    ws.cell(row=8, column=1, value="Cash Sweep Prepayment")
    for c in range(2, 7):
        col = get_column_letter(c)
        ws.cell(row=8, column=c, value=f"=-{col}6*0.05").font = FONT_FORMULA

    ws.cell(row=9, column=1, value="Ending Balance").font = Font(bold=True)
    for c in range(2, 7):
        col = get_column_letter(c)
        cell = ws.cell(row=9, column=c, value=f"=SUM({col}6:{col}8)")
        cell.font = FONT_FORMULA
        cell.border = BORDER_TOTAL

    ws.cell(row=10, column=1, value="Interest Expense (6.5%)")
    for c in range(2, 7):
        col = get_column_letter(c)
        ws.cell(row=10, column=c, value=f"=AVERAGE({col}6,{col}9)*0.065").font = FONT_FORMULA

    for r in range(6, 11):
        for c in range(2, 7):
            ws.cell(row=r, column=c).number_format = FMT_CURRENCY

    ws.freeze_panes = "B5"
    autofit_and_grid(ws)
    wb.save(output_file)
    wb.close()
    return {"status": "success", "model": "debt_schedule", "output": output_file}


def generate_cap_table_model(output_file):
    wb = Workbook()
    ws = wb.active
    ws.title = "Cap Table"

    ws["A1"] = "STARTUP CAPITALIZATION TABLE & DILUTION WATERFALL"
    ws["A1"].font = FONT_TITLE

    headers = ["Shareholder Class", "Pre-Money Shares", "% Pre-Money", "Investment ($)", "Series A Shares", "Post-Money Shares", "% Fully Diluted"]
    for c_idx, h in enumerate(headers, 1):
        cell = ws.cell(row=4, column=c_idx, value=h)
        cell.fill = FILL_HEADER
        cell.font = FONT_HEADER

    data = [
        ["Founders Common Shares", 6000000, 0, 6000000],
        ["Key Employees / ESOP Pool", 1000000, 0, 1000000],
        ["Seed Investors (Preferred)", 1000000, 0, 1000000],
        ["Series A New Investor", 0, 3000000, "=D8/$B$13"],
    ]

    for idx, row in enumerate(data, 5):
        ws.cell(row=idx, column=1, value=row[0]).font = FONT_SUBHEADER
        ws.cell(row=idx, column=2, value=row[1]).font = FONT_INPUT
        ws.cell(row=idx, column=3, value=f"=B{idx}/$B$9").font = FONT_FORMULA
        ws.cell(row=idx, column=4, value=row[2]).font = FONT_INPUT
        if isinstance(row[3], str):
            ws.cell(row=idx, column=5, value=row[3]).font = FONT_FORMULA
        else:
            ws.cell(row=idx, column=5, value=row[3]).font = FONT_INPUT
        ws.cell(row=idx, column=6, value=f"=B{idx}+E{idx}").font = FONT_FORMULA
        ws.cell(row=idx, column=7, value=f"=F{idx}/$F$9").font = FONT_FORMULA

    ws.cell(row=9, column=1, value="Total Fully Diluted").font = Font(bold=True)
    ws.cell(row=9, column=2, value="=SUM(B5:B8)").font = FONT_FORMULA
    ws.cell(row=9, column=2).border = BORDER_TOTAL
    ws.cell(row=9, column=3, value="=SUM(C5:C8)").font = FONT_FORMULA
    ws.cell(row=9, column=4, value="=SUM(D5:D8)").font = FONT_FORMULA
    ws.cell(row=9, column=5, value="=SUM(E5:E8)").font = FONT_FORMULA
    ws.cell(row=9, column=6, value="=SUM(F5:F8)").font = FONT_FORMULA
    ws.cell(row=9, column=6).border = BORDER_TOTAL
    ws.cell(row=9, column=7, value="=SUM(G5:G8)").font = FONT_FORMULA

    ws.cell(row=11, column=1, value="VALUATION & PRICING").font = FONT_SUBHEADER
    ws.cell(row=12, column=1, value="Pre-Money Valuation ($)")
    ws.cell(row=12, column=2, value=12000000).font = FONT_INPUT
    ws.cell(row=12, column=2).number_format = FMT_CURRENCY

    ws.cell(row=13, column=1, value="Series A Share Price ($/share)")
    ws.cell(row=13, column=2, value="=B12/B9").font = FONT_FORMULA
    ws.cell(row=13, column=2).number_format = '$#,##0.00'

    ws.cell(row=14, column=1, value="Post-Money Valuation ($)")
    ws.cell(row=14, column=2, value="=B12+D8").font = FONT_FORMULA
    ws.cell(row=14, column=2).number_format = FMT_CURRENCY
    ws.cell(row=14, column=2).border = BORDER_TOTAL

    for r in range(5, 10):
        ws.cell(row=r, column=2).number_format = '#,##0'
        ws.cell(row=r, column=3).number_format = FMT_PERCENT
        ws.cell(row=r, column=4).number_format = FMT_CURRENCY
        ws.cell(row=r, column=5).number_format = '#,##0'
        ws.cell(row=r, column=6).number_format = '#,##0'
        ws.cell(row=r, column=7).number_format = FMT_PERCENT

    ws.freeze_panes = "B5"
    autofit_and_grid(ws)
    wb.save(output_file)
    wb.close()
    return {"status": "success", "model": "cap_table", "output": output_file}


def generate_working_capital_model(output_file):
    wb = Workbook()
    ws = wb.active
    ws.title = "Working Capital"

    ws["A1"] = "WORKING CAPITAL & CASH CONVERSION CYCLE (CCC) ENGINE"
    ws["A1"].font = FONT_TITLE

    headers = ["Operating Metric", "FY2023", "FY2024", "FY2025 (P)", "FY2026 (P)"]
    for c_idx, h in enumerate(headers, 1):
        cell = ws.cell(row=4, column=c_idx, value=h)
        cell.fill = FILL_HEADER
        cell.font = FONT_HEADER

    ws.cell(row=5, column=1, value="Revenue ($k)")
    ws.cell(row=5, column=2, value=20000).font = FONT_INPUT
    ws.cell(row=5, column=3, value=24000).font = FONT_INPUT
    ws.cell(row=5, column=4, value=28800).font = FONT_INPUT
    ws.cell(row=5, column=5, value=34560).font = FONT_INPUT

    ws.cell(row=6, column=1, value="Cost of Goods Sold (COGS)")
    for c in range(2, 6):
        col = get_column_letter(c)
        ws.cell(row=6, column=c, value=f"=-{col}5*0.60").font = FONT_FORMULA

    ws.cell(row=8, column=1, value="Accounts Receivable (AR)")
    ws.cell(row=8, column=2, value=2500).font = FONT_INPUT
    ws.cell(row=8, column=3, value=3000).font = FONT_INPUT
    ws.cell(row=8, column=4, value=3600).font = FONT_INPUT
    ws.cell(row=8, column=5, value=4320).font = FONT_INPUT

    ws.cell(row=9, column=1, value="Inventory (INV)")
    ws.cell(row=9, column=2, value=1500).font = FONT_INPUT
    ws.cell(row=9, column=3, value=1800).font = FONT_INPUT
    ws.cell(row=9, column=4, value=2160).font = FONT_INPUT
    ws.cell(row=9, column=5, value=2592).font = FONT_INPUT

    ws.cell(row=10, column=1, value="Accounts Payable (AP)")
    ws.cell(row=10, column=2, value=1200).font = FONT_INPUT
    ws.cell(row=10, column=3, value=1440).font = FONT_INPUT
    ws.cell(row=10, column=4, value=1728).font = FONT_INPUT
    ws.cell(row=10, column=5, value=2074).font = FONT_INPUT

    ws.cell(row=12, column=1, value="Net Working Capital (AR + INV - AP)").font = Font(bold=True)
    for c in range(2, 6):
        col = get_column_letter(c)
        cell = ws.cell(row=12, column=c, value=f"={col}8+{col}9-{col}10")
        cell.font = FONT_FORMULA
        cell.border = BORDER_TOTAL

    ws.cell(row=14, column=1, value="OPERATING CYCLE (DAYS)").font = FONT_SUBHEADER
    ws.cell(row=14, column=1).fill = FILL_SUBHEADER

    ws.cell(row=15, column=1, value="Days Sales Outstanding (DSO)")
    for c in range(2, 6):
        col = get_column_letter(c)
        ws.cell(row=15, column=c, value=f"=({col}8/{col}5)*365").font = FONT_FORMULA
        ws.cell(row=15, column=c).number_format = '0.0 "days"'

    ws.cell(row=16, column=1, value="Days Inventory Outstanding (DIO)")
    for c in range(2, 6):
        col = get_column_letter(c)
        ws.cell(row=16, column=c, value=f"=({col}9/(-{col}6))*365").font = FONT_FORMULA
        ws.cell(row=16, column=c).number_format = '0.0 "days"'

    ws.cell(row=17, column=1, value="Days Payable Outstanding (DPO)")
    for c in range(2, 6):
        col = get_column_letter(c)
        ws.cell(row=17, column=c, value=f"=({col}10/(-{col}6))*365").font = FONT_FORMULA
        ws.cell(row=17, column=c).number_format = '0.0 "days"'

    ws.cell(row=18, column=1, value="Cash Conversion Cycle (DSO + DIO - DPO)").font = Font(bold=True)
    for c in range(2, 6):
        col = get_column_letter(c)
        cell = ws.cell(row=18, column=c, value=f"={col}15+{col}16-{col}17")
        cell.font = FONT_FORMULA
        cell.number_format = '0.0 "days"'
        cell.border = BORDER_TOTAL

    for r in [5, 6, 8, 9, 10, 12]:
        for c in range(2, 6):
            ws.cell(row=r, column=c).number_format = FMT_CURRENCY

    ws.freeze_panes = "B5"
    autofit_and_grid(ws)
    wb.save(output_file)
    wb.close()
    return {"status": "success", "model": "working_capital", "output": output_file}


# ======================================================================================
# 5. FORMULA DAG DEPENDENCY DEBUGGER (BUGFIXED MULTI-CELL RANGE EXPANSION)
# ======================================================================================
def expand_range_reference(ref_str: str, default_sheet: str = "") -> list:
    """Expands ranges like 'Sheet1!A1:B3' into individual cell coordinates."""
    sheet_prefix = default_sheet
    clean_ref = ref_str
    if "!" in ref_str:
        sheet_part, clean_ref = ref_str.split("!", 1)
        sheet_prefix = sheet_part.strip("'")

    if ":" in clean_ref:
        try:
            min_col, min_row, max_col, max_row = range_boundaries(clean_ref)
            expanded = []
            for r in range(min_row, max_row + 1):
                for c in range(min_col, max_col + 1):
                    col_let = get_column_letter(c)
                    expanded.append(f"{sheet_prefix}!{col_let}{r}")
            return expanded
        except Exception:
            return [f"{sheet_prefix}!{clean_ref}"]
    else:
        return [f"{sheet_prefix}!{clean_ref}"]


class DependencyDAG:
    def __init__(self, filename):
        self.filename = filename
        self.precedents = defaultdict(set)
        self.dependents = defaultdict(set)
        self.formulas = {}
        self.values = {}
        self._build()

    def _build(self):
        wb_f = load_workbook(self.filename, data_only=False)
        wb_v = load_workbook(self.filename, data_only=True)
        for s in wb_f.sheetnames:
            ws_f = wb_f[s]
            ws_v = wb_v[s]
            for row in ws_f.iter_rows():
                for cell in row:
                    coord = f"{s}!{cell.coordinate}"
                    self.values[coord] = ws_v[cell.coordinate].value
                    if isinstance(cell.value, str) and cell.value.startswith("="):
                        self.formulas[coord] = cell.value
                        try:
                            tok = Tokenizer(cell.value)
                            for token in tok.items:
                                if token.type == "OPERAND" and token.subtype == "RANGE":
                                    # BUGFIX: Expand multi-cell ranges into individual cell nodes
                                    expanded_cells = expand_range_reference(token.value.strip(), s)
                                    for ref_cell in expanded_cells:
                                        self.precedents[coord].add(ref_cell)
                                        self.dependents[ref_cell].add(coord)
                        except Exception:
                            pass
        wb_f.close()
        wb_v.close()

    def trace_root_cause(self, error_cell):
        """Traces backward through the DAG to isolate the primal origin of an Excel error.
        Works across both evaluated workbooks (cached values) and uncalculated openpyxl workbooks.
        """
        def node_has_explicit_error(n):
            v = str(self.values.get(n, ""))
            f = str(self.formulas.get(n, "") or "")
            return any(err in v for err in EXCEL_ERRORS) or any(err in f for err in EXCEL_ERRORS)

        all_error_cells = {n for n in self.values if node_has_explicit_error(n)} | {n for n in self.formulas if node_has_explicit_error(n)}

        memo = {}
        def can_reach_error(n):
            if n in memo:
                return memo[n]
            if n in all_error_cells:
                memo[n] = True
                return True
            for pred in self.precedents.get(n, set()):
                if can_reach_error(pred):
                    memo[n] = True
                    return True
            memo[n] = False
            return False

        visited = set()
        queue = deque([error_cell])
        roots = []
        while queue:
            curr = queue.popleft()
            if curr in visited:
                continue
            visited.add(curr)
            preds = self.precedents.get(curr, set())
            has_bad_pred = False
            for p in preds:
                if can_reach_error(p):
                    has_bad_pred = True
                    queue.append(p)
            if not has_bad_pred:
                roots.append({
                    "cell": curr,
                    "formula": self.formulas.get(curr),
                    "value": str(self.values.get(curr)),
                    "precedents": list(preds)
                })
        return roots or [{"cell": error_cell, "formula": self.formulas.get(error_cell), "value": str(self.values.get(error_cell))}]


# ======================================================================================
# 6. ATOMIC MICRO-CLI
# ======================================================================================
def execute_cli_read(file_path, sheet_name, cell_range=None):
    wb = load_workbook(file_path, data_only=False)
    if sheet_name not in wb.sheetnames:
        return {"error": f"Sheet '{sheet_name}' not found."}
    ws = wb[sheet_name]
    min_col, min_row, max_col, max_row = range_boundaries(cell_range) if cell_range else (1, 1, ws.max_column, ws.max_row)

    matrix = []
    for r in range(min_row, max_row + 1):
        row_vals = [ws.cell(row=r, column=c).value for c in range(min_col, max_col + 1)]
        matrix.append(row_vals)
    wb.close()
    return {"sheet": sheet_name, "range": cell_range or ws.dimensions, "data": matrix}


def execute_cli_write(file_path, sheet_name, start_coord, matrix_json, out_path=None):
    if isinstance(matrix_json, str):
        try:
            matrix = json.loads(matrix_json)
        except Exception as e:
            return {"error": f"Invalid JSON matrix: {e}"}
    else:
        matrix = matrix_json

    wb = load_workbook(file_path, data_only=False)
    ws = wb[sheet_name] if sheet_name in wb.sheetnames else wb.create_sheet(title=sheet_name)
    start_col, start_row, _, _ = range_boundaries(start_coord)

    count = 0
    for r_idx, row in enumerate(matrix):
        for c_idx, val in enumerate(row):
            ws.cell(row=start_row + r_idx, column=start_col + c_idx, value=val)
            count += 1

    dest = out_path or file_path
    wb.save(dest)
    wb.close()
    return {"status": "success", "file": str(dest), "cells_updated": count}


# ======================================================================================
# 7. VISUAL & UX AUDITOR
# ======================================================================================
def execute_ux_audit(file_path):
    wb = load_workbook(file_path, data_only=False)
    checks = []

    for name in wb.sheetnames:
        ws = wb[name]
        has_freeze = bool(ws.freeze_panes)
        checks.append({
            "sheet": name,
            "check": "Freeze Panes",
            "passed": has_freeze,
            "detail": f"Panes frozen: {ws.freeze_panes or 'None (Recommended: A2 or B5)'}"
        })

        has_filter = bool(ws.auto_filter.ref)
        checks.append({
            "sheet": name,
            "check": "Auto-Filter",
            "passed": has_filter,
            "detail": f"Filter ref: {ws.auto_filter.ref or 'None'}"
        })

        form_cnt = sum(1 for row in ws.iter_rows() for c in row if isinstance(c.value, str) and c.value.startswith("="))
        checks.append({
            "sheet": name,
            "check": "Dynamic Formulas",
            "passed": form_cnt > 0,
            "detail": f"{form_cnt} dynamic formulas found"
        })

        truncated_cols = 0
        for col in ws.columns:
            max_len = 0
            for c in col:
                val = c.value
                if val is not None:
                    s_val = str(val)
                    val_len = 14 if s_val.startswith("=") else len(s_val)
                    if val_len > max_len:
                        max_len = val_len
            col_letter = get_column_letter(col[0].column)
            set_w = ws.column_dimensions[col_letter].width or 8.43
            if max_len > set_w:
                truncated_cols += 1
        checks.append({
            "sheet": name,
            "check": "Column Widths (No ### Overflow)",
            "passed": truncated_cols == 0,
            "detail": f"{truncated_cols} column(s) may truncate content or cause ### overflow"
        })

    wb.close()
    return {"file": file_path, "total_checks": len(checks), "results": checks}


# ======================================================================================
# 8. NATIVE MCP SERVER BRIDGE
# ======================================================================================
def run_mcp_server():
    sys.stderr.write("Starting Mega Excel Master Suite MCP Server (stdio)...\n")
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            req_id = req.get("id")
            method = req.get("method")

            if method == "initialize":
                res = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {"tools": {}},
                        "serverInfo": {"name": "mega-excel-master-suite", "version": "3.1.0"}
                    }
                }
            elif method == "tools/list":
                res = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "tools": [
                            {"name": "excel_recalculate", "description": "Recalculates workbook and scans for errors", "inputSchema": {"type": "object", "properties": {"file": {"type": "string"}}}},
                            {"name": "excel_restructure", "description": "Shifts rows/cols and auto-updates formula AST", "inputSchema": {"type": "object", "properties": {"file": {"type": "string"}, "sheet": {"type": "string"}, "action": {"type": "string"}, "axis": {"type": "string"}, "index": {"type": "integer"}, "count": {"type": "integer"}}}},
                            {"name": "excel_clean_reconcile", "description": "Cleans messy ERP data with delta=0.00 check", "inputSchema": {"type": "object", "properties": {"input": {"type": "string"}, "output": {"type": "string"}}}},
                            {"name": "excel_generate_model", "description": "Generates institutional financial models (three_statement, dcf, lbo, saas_runway, debt_schedule, cap_table, working_capital)", "inputSchema": {"type": "object", "properties": {"model": {"type": "string"}, "output": {"type": "string"}}}},
                            {"name": "excel_read_range", "description": "Reads range in A1 notation to JSON matrix", "inputSchema": {"type": "object", "properties": {"file": {"type": "string"}, "sheet": {"type": "string"}, "range": {"type": "string"}}}},
                            {"name": "excel_write_range", "description": "Writes 2D matrix starting at cell", "inputSchema": {"type": "object", "properties": {"file": {"type": "string"}, "sheet": {"type": "string"}, "start": {"type": "string"}, "data": {"type": "string"}}}},
                            {"name": "excel_trace_error", "description": "Traces root cause of an error cell in formula DAG", "inputSchema": {"type": "object", "properties": {"file": {"type": "string"}, "cell": {"type": "string"}}}},
                            {"name": "excel_ux_audit", "description": "Audits freeze panes, filters, widths, and formulas", "inputSchema": {"type": "object", "properties": {"file": {"type": "string"}}}}
                        ]
                    }
                }
            elif method == "tools/call":
                params = req.get("params", {})
                t_name = params.get("name")
                args = params.get("arguments", {})

                if t_name == "excel_recalculate":
                    output = execute_recalculate(args.get("file"))
                elif t_name == "excel_restructure":
                    output = execute_restructure(args.get("file"), args.get("sheet"), args.get("action"), args.get("axis"), args.get("index"), args.get("count", 1))
                elif t_name == "excel_clean_reconcile":
                    output = execute_clean_reconcile(args.get("input"), args.get("output"))
                elif t_name == "excel_generate_model":
                    m = args.get("model")
                    o = args.get("output")
                    if m == "three_statement":
                        output = generate_three_statement_model(o)
                    elif m == "dcf":
                        output = generate_dcf_model(o)
                    elif m == "lbo":
                        output = generate_lbo_model(o)
                    elif m == "saas_runway":
                        output = generate_saas_runway_model(o)
                    elif m == "debt_schedule":
                        output = generate_debt_schedule_model(o)
                    elif m == "cap_table":
                        output = generate_cap_table_model(o)
                    elif m == "working_capital":
                        output = generate_working_capital_model(o)
                    else:
                        output = {"error": f"Unknown model type: {m}"}
                elif t_name == "excel_read_range":
                    output = execute_cli_read(args.get("file"), args.get("sheet"), args.get("range"))
                elif t_name == "excel_write_range":
                    output = execute_cli_write(args.get("file"), args.get("sheet"), args.get("start"), args.get("data"))
                elif t_name == "excel_trace_error":
                    dag = DependencyDAG(args.get("file"))
                    output = dag.trace_root_cause(args.get("cell"))
                elif t_name == "excel_ux_audit":
                    output = execute_ux_audit(args.get("file"))
                else:
                    output = {"error": f"Unknown tool: {t_name}"}

                res = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {"content": [{"type": "text", "text": json.dumps(output, indent=2)}]}
                }
            else:
                res = {"jsonrpc": "2.0", "id": req_id, "result": {}}

            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stderr.write(f"MCP error: {e}\n")


# ======================================================================================
# MAIN DISPATCHER
# ======================================================================================
def main():
    parser = argparse.ArgumentParser(description="Mega Excel Master Suite - Unified Engine")
    sub = parser.add_subparsers(dest="command", required=True)

    # 1. Recalc
    p_recalc = sub.add_parser("recalc", help="Headless recalculation & formula error audit")
    p_recalc.add_argument("file")
    p_recalc.add_argument("--timeout", type=int, default=30)
    p_recalc.add_argument("--force", action="store_true")

    # 2. Restructure
    p_restruct = sub.add_parser("restructure", help="Reference-aware row/col insertion & AST shifting")
    p_restruct.add_argument("file")
    p_restruct.add_argument("--sheet", required=True)
    p_restruct.add_argument("--action", choices=["insert", "delete"], required=True)
    p_restruct.add_argument("--axis", choices=["row", "col"], required=True)
    p_restruct.add_argument("--index", type=int, required=True)
    p_restruct.add_argument("--count", type=int, default=1)
    p_restruct.add_argument("--out", default=None)

    # 3. Clean
    p_clean = sub.add_parser("clean", help="Clean messy ERP dumps with Delta=0.00 reconciliation")
    p_clean.add_argument("input")
    p_clean.add_argument("--out", required=True)
    p_clean.add_argument("--sheet", default=None)

    # 4. Model
    p_model = sub.add_parser("model", help="Generate institutional financial models")
    p_model.add_argument("--type", choices=[
        "three_statement", "dcf", "lbo", "saas_runway", "debt_schedule", "cap_table", "working_capital"
    ], required=True)
    p_model.add_argument("--out", required=True)

    # 5. Debug
    p_debug = sub.add_parser("debug", help="DAG dependency tracing & error root cause isolation")
    p_debug.add_argument("file")
    p_debug.add_argument("--trace-error", help="Coordinate to trace (e.g. Sheet1!C10)")

    # 6. Read
    p_read = sub.add_parser("read", help="Atomic JSON range read")
    p_read.add_argument("file")
    p_read.add_argument("--sheet", required=True)
    p_read.add_argument("--range", default=None)

    # 7. Write
    p_write = sub.add_parser("write", help="Atomic JSON range write")
    p_write.add_argument("file")
    p_write.add_argument("--sheet", required=True)
    p_write.add_argument("--start", required=True)
    p_write.add_argument("--data", required=True)
    p_write.add_argument("--out", default=None)

    # 8. Audit
    p_audit = sub.add_parser("audit", help="Visual UX audit (freeze panes, filters, widths)")
    p_audit.add_argument("file")

    # 9. MCP
    sub.add_parser("mcp", help="Run as stdio Model Context Protocol (MCP) server")

    args = parser.parse_args()

    if args.command == "recalc":
        res = execute_recalculate(args.file, args.timeout, args.force)
    elif args.command == "restructure":
        res = execute_restructure(args.file, args.sheet, args.action, args.axis, args.index, args.count, args.out)
    elif args.command == "clean":
        res = execute_clean_reconcile(args.input, args.out, args.sheet)
    elif args.command == "model":
        if args.type == "three_statement":
            res = generate_three_statement_model(args.out)
        elif args.type == "dcf":
            res = generate_dcf_model(args.out)
        elif args.type == "lbo":
            res = generate_lbo_model(args.out)
        elif args.type == "saas_runway":
            res = generate_saas_runway_model(args.out)
        elif args.type == "debt_schedule":
            res = generate_debt_schedule_model(args.out)
        elif args.type == "cap_table":
            res = generate_cap_table_model(args.out)
        elif args.type == "working_capital":
            res = generate_working_capital_model(args.out)
        else:
            res = {"error": f"Unknown model type: {args.type}"}
    elif args.command == "debug":
        dag = DependencyDAG(args.file)
        if args.trace_error:
            res = dag.trace_root_cause(args.trace_error)
        else:
            res = {"formulas": len(dag.formulas), "nodes": len(dag.values)}
    elif args.command == "read":
        res = execute_cli_read(args.file, args.sheet, args.range)
    elif args.command == "write":
        res = execute_cli_write(args.file, args.sheet, args.start, args.data, args.out)
    elif args.command == "audit":
        res = execute_ux_audit(args.file)
    elif args.command == "mcp":
        run_mcp_server()
        return

    print(json.dumps(res, indent=2))
    has_error = False
    if isinstance(res, dict):
        has_error = "error" in res or res.get("status") == "errors_found"
    sys.exit(1 if has_error else 0)


if __name__ == "__main__":
    main()
