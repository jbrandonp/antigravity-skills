"""
Script to export quotes or deals from the Excel workbook to a clean UTF-8 CSV file.
Ensures zero vendor lock-in and seamless data portability to any ERP (Vertuoza, Odoo, Bouwsoft, HubSpot).
Strictly typed, zero 'Any'.
"""

import argparse
import csv
import os
import sys
from typing import Final, List, Union
import openpyxl

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

CellValue = Union[str, int, float, bool, None]
DIR_PATH: Final[str] = os.path.dirname(os.path.abspath(__file__))


def export_devis_to_csv(
    excel_path: str = "",
    csv_path: str = "",
) -> int:
    """
    Exporte l'intégralité des devis ou affaires vers un fichier CSV standardisé UTF-8.
    """
    if not excel_path:
        candidates = [
            os.path.join(DIR_PATH, "SUIVI_AFFAIRES_MODELE_PRO.xlsx"),
            os.path.join(DIR_PATH, "DEVIS_SANS_OUBLI_MODELE_PRO.xlsx"),
        ]
        excel_path = next((p for p in candidates if os.path.isfile(p)), candidates[0])

    if not csv_path:
        csv_name = "EXPORTS_AFFAIRES_ERP_COMPATIBLE.csv" if "AFFAIRES" in os.path.basename(excel_path) else "EXPORTS_DEVIS_ERP_COMPATIBLE.csv"
        csv_path = os.path.join(DIR_PATH, csv_name)

    if not os.path.isfile(excel_path):
        raise FileNotFoundError(f"Classeur Excel introuvable : {excel_path}")

    wb = openpyxl.load_workbook(excel_path, data_only=True)
    sheet_name = "Suivi des Devis" if "Suivi des Devis" in wb.sheetnames else wb.sheetnames[0]
    ws = wb[sheet_name]

    exported_rows: List[List[CellValue]] = []

    # En-têtes standards (ligne 4)
    headers = [str(ws.cell(row=4, column=c).value or f"Col_{c}").strip() for c in range(1, 12)]
    exported_rows.append(headers)

    # Extraction des données réelles (lignes 5 à max_row)
    count = 0
    for r in range(5, ws.max_row + 1):
        num_devis = ws.cell(row=r, column=1).value
        if not num_devis:
            continue
        num_str = str(num_devis).strip()
        # Filtre les mentions légales ou textes de bas de page
        if num_str.startswith("AVERTISSEMENT") or num_str.startswith("Avertissement") or len(num_str) > 40:
            continue
        row_data = [ws.cell(row=r, column=c).value for c in range(1, 12)]
        exported_rows.append(row_data)
        count += 1

    # Écriture du CSV avec encodage UTF-8 et séparateur point-virgule (standard Excel européen)
    os.makedirs(os.path.dirname(os.path.abspath(csv_path)), exist_ok=True)
    with open(csv_path, mode="w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerows(exported_rows)

    print(f"[OK] Exportation réussie : {count} lignes exportées vers {csv_path}")
    return count


def main() -> None:
    parser = argparse.ArgumentParser(description="Exportateur CSV pour Bureau Numérique.")
    parser.add_argument("--excel-path", "-e", default="", help="Chemin du classeur Excel")
    parser.add_argument("--output-csv", "-o", default="", help="Chemin du fichier CSV cible")
    args = parser.parse_args()

    export_devis_to_csv(excel_path=args.excel_path, csv_path=args.output_csv)


if __name__ == "__main__":
    main()
