"""
Script to generate the prospecting tracker workbook 'FICHIER_PROSPECTION_LIEGE_BTP.xlsx'.
Structured for qualifying and tracking prospects in the construction sector around Liège.
"""

import os
from typing import Final, List, Tuple
import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

DEFAULT_PROSPECT_PATH: Final[str] = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "FICHIER_PROSPECTION_LIEGE_BTP.xlsx"
)

ProspectRow = Tuple[str, str, str, str, str, str, str, str, str, str, str, str]

FONT_FAMILY: Final[str] = "Calibri"
COLOR_PRIMARY_NAVY: Final[str] = "1B365D"
COLOR_HEADER_FILL: Final[str] = "244061"
COLOR_LIGHT_BG: Final[str] = "F2F5F9"
COLOR_BORDER: Final[str] = "D9D9D9"


def create_prospection_workbook(output_path: str = DEFAULT_PROSPECT_PATH) -> None:
    """
    Génère la base de prospection commerciale BTP avec données de test réalistes.

    Paramètres :
        output_path (str) : Chemin du fichier Excel cible.

    Retour :
        None
    """
    wb: openpyxl.Workbook = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Pipeline Prospection Liège"
    ws.views.sheetView[0].showGridLines = True

    # Styles
    font_title = Font(name=FONT_FAMILY, size=15, bold=True, color="FFFFFF")
    font_subtitle = Font(name=FONT_FAMILY, size=10, italic=True, color="FFFFFF")
    font_header = Font(name=FONT_FAMILY, size=11, bold=True, color="FFFFFF")
    font_data = Font(name=FONT_FAMILY, size=10)

    fill_banner = PatternFill(start_color=COLOR_PRIMARY_NAVY, end_color=COLOR_PRIMARY_NAVY, fill_type="solid")
    fill_header = PatternFill(start_color=COLOR_HEADER_FILL, end_color=COLOR_HEADER_FILL, fill_type="solid")
    thin_border = Border(
        left=Side(style="thin", color=COLOR_BORDER),
        right=Side(style="thin", color=COLOR_BORDER),
        top=Side(style="thin", color=COLOR_BORDER),
        bottom=Side(style="thin", color=COLOR_BORDER),
    )

    # Bannière
    ws.merge_cells("A1:L1")
    ws.merge_cells("A2:L2")
    ws["A1"] = "BUREAU NUMÉRIQUE BTP — FICHIER DE PROSPECTION COMMERCIALE (WALLONIE / LIÈGE)"
    ws["A2"] = "Suivi des prises de contact, entretiens de découverte et taux de conversion"
    ws["A1"].font = font_title
    ws["A2"].font = font_subtitle
    ws["A1"].fill = fill_banner
    ws["A2"].fill = fill_banner
    ws["A1"].alignment = Alignment(horizontal="center", vertical="center")
    ws["A2"].alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 26
    ws.row_dimensions[2].height = 18

    # En-têtes
    headers: List[str] = [
        "ID",
        "Nom Entreprise",
        "Métier",
        "Commune",
        "Gérant / Décideur",
        "Téléphone Direct",
        "Email",
        "Canal Approche",
        "Statut Prospection",
        "Dernier Contact",
        "Date Prochaine Relance",
        "Notes & Irritants Détectés",
    ]

    header_row = 4
    ws.row_dimensions[header_row].height = 24
    for col_idx, h in enumerate(headers, start=1):
        cell = ws.cell(row=header_row, column=col_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = thin_border

    # Prospects types qualifiés pour la région liégeoise
    prospects: List[ProspectRow] = [
        ("PROSP-001", "Chauffage Meuse Confort", "HVAC / Chauffage", "Liège (Angleur)", "Alain Renard", "0475 33 44 55", "contact@meuse-confort.be", "Comptoir Facq", "À contacter", "2026-11-02", "2026-11-09", "5 ouvriers, patron au comptoir à 7h. Se plaint de devis sans retour."),
        ("PROSP-002", "Électricité Lambert & Fils", "Électricité", "Chaudfontaine", "Benoît Lambert", "0495 11 22 33", "info@lambert-elec.be", "Google Maps", "Vocal envoyé", "2026-11-04", "2026-11-07", "Très actif en domotique. Secrétaire à mi-temps."),
        ("PROSP-003", "Verviers Sanitaire Sprl", "Plomberie", "Verviers", "Fabrice Martin", "087 22 33 44", "f.martin@verviers-sanitaire.be", "LinkedIn", "Démo planifiée", "2026-11-03", "2026-11-10", "RDV démo mardi 14h via Google Meet. Intéressé par 'Devis sans oubli'."),
        ("PROSP-004", "Rénov Mosane", "Rénovation", "Seraing", "Thierry Dumont", "0478 99 88 77", "tdumont@renov-mosane.be", "Comptable", "Diagnostic offert", "2026-11-01", "2026-11-08", "Recommandé par fiduciaire locale. Dossiers chantiers éparpillés."),
        ("PROSP-005", "Clim & Chauffage Herstal", "HVAC / Froid", "Herstal", "Guy Collard", "04 264 55 66", "info@climherstal.be", "Google Maps", "À contacter", "", "2026-11-10", "Dépannages urgents fréquents."),
    ]

    for r_idx, p_data in enumerate(prospects, start=5):
        ws.row_dimensions[r_idx].height = 20
        for c_idx, val in enumerate(p_data, start=1):
            cell = ws.cell(row=r_idx, column=c_idx, value=val)
            cell.font = font_data
            cell.border = thin_border
            cell.alignment = Alignment(vertical="center")
            if c_idx in (1, 3, 4, 8, 9, 10, 11):
                cell.alignment = Alignment(horizontal="center", vertical="center")

    # Largeurs de colonnes
    col_widths = {
        "A": 12, "B": 26, "C": 20, "D": 18, "E": 20, "F": 16,
        "G": 28, "H": 18, "I": 20, "J": 14, "K": 18, "L": 42
    }
    for c_letter, w in col_widths.items():
        ws.column_dimensions[c_letter].width = w

    wb.save(output_path)
    print(f"[OK] Fichier de prospection généré avec succès : {output_path}")


if __name__ == "__main__":
    create_prospection_workbook(DEFAULT_PROSPECT_PATH)
