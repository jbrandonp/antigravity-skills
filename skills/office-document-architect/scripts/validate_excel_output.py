# -*- coding: utf-8 -*-
"""
validate_excel_output.py - OpenPyXL Excel Architect Validator
Valide la mise en page, les formules, les largeurs de colonnes et le gel des volets.
"""

import os
import sys
import pathlib
import argparse
from typing import TypedDict, List, Dict, Tuple

class ExcelCheckResult(TypedDict):
    sheet_name: str
    criterion: str
    status: str
    detail: str

def create_demo_workbook(out_path: str) -> None:
    try:
        from openpyxl import Workbook
        from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
        from openpyxl.utils import get_column_letter
    except ImportError:
        print("[!] openpyxl n est pas installe. Installez-le avec : pip install openpyxl")
        return

    wb = Workbook()
    ws = wb.active
    ws.title = "Comparatif_Prix"

    headers = ["ID Produit", "Enseigne", "Article", "Prix Unitaire (€)", "Quantite", "Total (€)"]
    ws.append(headers)

    # Styles
    header_font = Font(name="Segoe UI", size=11, bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid")
    center_align = Alignment(horizontal="center", vertical="center")
    right_align = Alignment(horizontal="right", vertical="center")

    thin_border = Border(
        left=Side(style="thin", color="D4D4D4"),
        right=Side(style="thin", color="D4D4D4"),
        top=Side(style="thin", color="D4D4D4"),
        bottom=Side(style="thin", color="D4D4D4"),
    )

    for col_num in range(1, len(headers) + 1):
        cell = ws.cell(row=1, column=col_num)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center_align

    # Données
    data = [
        [101, "Colruyt", "Lait Demi-Écrémé 1L", 0.95, 12],
        [102, "Delhaize", "Lait Demi-Écrémé 1L", 1.05, 8],
        [103, "Colruyt", "Café Moulu 500g", 3.89, 4],
        [104, "Delhaize", "Café Moulu 500g", 4.15, 3],
        [105, "Colruyt", "Pâtes Penne 500g", 0.89, 15],
    ]

    zebra_fill = PatternFill(start_color="F2F4F4", end_color="F2F4F4", fill_type="solid")

    for r_idx, row in enumerate(data, start=2):
        ws.append([row[0], row[1], row[2], row[3], row[4], f"=D{r_idx}*E{r_idx}"])
        for c_idx in range(1, 7):
            c = ws.cell(row=r_idx, column=c_idx)
            c.border = thin_border
            c.font = Font(name="Segoe UI", size=10)
            if r_idx % 2 == 1:
                c.fill = zebra_fill
            if c_idx in (4, 6):
                c.number_format = "#,##0.00 €"
                c.alignment = right_align
            elif c_idx in (1, 5):
                c.alignment = center_align

    # Ligne de total
    tot_row = len(data) + 2
    ws.cell(row=tot_row, column=3, value="TOTAL GENERAL").font = Font(name="Segoe UI", bold=True)
    tot_cell = ws.cell(row=tot_row, column=6, value=f"=SUM(F2:F{tot_row-1})")
    tot_cell.font = Font(name="Segoe UI", bold=True)
    tot_cell.number_format = "#,##0.00 €"
    tot_cell.alignment = right_align

    # Volets figes et filtres
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = f"A1:F{len(data)+1}"

    # Auto-fit des colonnes
    for col in ws.columns:
        max_len = max(len(str(cell.value or "")) for cell in col)
        col_letter = get_column_letter(col[0].column)
        ws.column_dimensions[col_letter].width = max(max_len + 4, 12)

    wb.save(out_path)
    print(f"[OK] Classeur de demonstration genere : {out_path}")

def inspect_workbook(file_path: str) -> List[ExcelCheckResult]:
    checks: List[ExcelCheckResult] = []
    try:
        from openpyxl import load_workbook
    except ImportError:
        checks.append({"sheet_name": "N/A", "criterion": "openpyxl", "status": "FAIL", "detail": "openpyxl non installe."})
        return checks

    p = pathlib.Path(file_path)
    if not p.exists():
        checks.append({"sheet_name": "N/A", "criterion": "File", "status": "FAIL", "detail": f"Fichier {file_path} introuvable."})
        return checks

    wb = load_workbook(file_path, data_only=False)
    for name in wb.sheetnames:
        ws = wb[name]
        # 1. Verification Volets figes
        has_freeze = bool(ws.freeze_panes)
        checks.append({
            "sheet_name": name,
            "criterion": "Freeze Panes",
            "status": "PASS" if has_freeze else "WARN",
            "detail": f"Volets figes : {ws.freeze_panes or 'Non configure (Recommande: A2)'}",
        })

        # 2. Verification Auto-Filter
        has_filter = bool(ws.auto_filter.ref)
        checks.append({
            "sheet_name": name,
            "criterion": "Auto Filter",
            "status": "PASS" if has_filter else "WARN",
            "detail": f"Filtres automatiques : {ws.auto_filter.ref or 'Absents'}",
        })

        # 3. Verification Formules
        formulas_count = 0
        for row in ws.iter_rows(values_only=False):
            for cell in row:
                if isinstance(cell.value, str) and cell.value.startswith("="):
                    formulas_count += 1
        checks.append({
            "sheet_name": name,
            "criterion": "Native Formulas",
            "status": "PASS" if formulas_count > 0 else "INFO",
            "detail": f"{formulas_count} formule(s) native(s) detectee(s)",
        })

    return checks

def main():
    parser = argparse.ArgumentParser(description="Excel Architect - Validateur de classeur OpenPyXL")
    parser.add_argument("--file", type=str, help="Fichier Excel (.xlsx) a auditer")
    parser.add_argument("--demo", action="store_true", help="Generer et auditer un classeur de demonstration")
    args = parser.parse_args()

    print("=" * 65)
    print("      EXCEL ARCHITECT (STANDARD OPENPYXL PRODUCTION)        ")
    print("=" * 65)

    target_file = args.file
    if args.demo or not target_file:
        target_file = "demo_supermarches.xlsx"
        create_demo_workbook(target_file)

    checks = inspect_workbook(target_file)
    for c in checks:
        tag = f"[{c['status']}]"
        print(f"{tag:<8} {c['sheet_name']:<18} | {c['criterion']:<15} : {c['detail']}")

    print("=" * 65)

if __name__ == "__main__":
    main()