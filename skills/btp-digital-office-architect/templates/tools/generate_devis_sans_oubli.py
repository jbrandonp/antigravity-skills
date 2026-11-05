"""
Script to generate the professional Excel workbook 'DEVIS_SANS_OUBLI_MODELE_PRO.xlsx'.
This tool automates quote tracking and follow-ups for small construction businesses.
"""

import os
from datetime import date, timedelta
from typing import Final, List, Tuple
import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Protection, Side
from openpyxl.utils import get_column_letter

DEFAULT_WORKBOOK_PATH: Final[str] = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "DEVIS_SANS_OUBLI_MODELE_PRO.xlsx"
)

DevisRow = Tuple[str, date, str, str, str, float, str, date, str, str, str]

# --- Constantes de style professionnel ---
FONT_FAMILY: Final[str] = "Calibri"
COLOR_PRIMARY_NAVY: Final[str] = "1B365D"  # Bleu marine professionnel BTP
COLOR_HEADER_FILL: Final[str] = "244061"
COLOR_LIGHT_BG: Final[str] = "F2F5F9"
COLOR_ACCENT_ORANGE: Final[str] = "E26B00"  # Orange sécurité chantier
COLOR_SUCCESS_GREEN: Final[str] = "27AE60"
COLOR_DANGER_RED: Final[str] = "C0392B"
COLOR_BORDER: Final[str] = "D9D9D9"


def create_devis_sans_oubli_workbook(output_path: str = DEFAULT_WORKBOOK_PATH) -> None:
    """
    Crée le classeur Excel 'Devis sans oubli' avec dashboard et suivi automatisé.

    Paramètres :
        output_path (str) : Chemin absolu ou relatif du fichier .xlsx à générer.

    Retour :
        None
    """
    # Création du classeur
    wb: openpyxl.Workbook = openpyxl.Workbook()

    # Définition des polices et bordures standards
    font_title = Font(name=FONT_FAMILY, size=16, bold=True, color="FFFFFF")
    font_subtitle = Font(name=FONT_FAMILY, size=11, italic=True, color="FFFFFF")
    font_header = Font(name=FONT_FAMILY, size=11, bold=True, color="FFFFFF")
    font_card_title = Font(name=FONT_FAMILY, size=10, bold=True, color="555555")
    font_card_value = Font(name=FONT_FAMILY, size=18, bold=True, color="1B365D")
    font_data = Font(name=FONT_FAMILY, size=10)
    font_data_bold = Font(name=FONT_FAMILY, size=10, bold=True)

    fill_header = PatternFill(start_color=COLOR_HEADER_FILL, end_color=COLOR_HEADER_FILL, fill_type="solid")
    fill_banner = PatternFill(start_color=COLOR_PRIMARY_NAVY, end_color=COLOR_PRIMARY_NAVY, fill_type="solid")
    fill_card = PatternFill(start_color=COLOR_LIGHT_BG, end_color=COLOR_LIGHT_BG, fill_type="solid")
    fill_urgent = PatternFill(start_color="FDEDEC", end_color="FDEDEC", fill_type="solid")
    fill_ok = PatternFill(start_color="EAFAF1", end_color="EAFAF1", fill_type="solid")

    thin_border_side = Side(border_style="thin", color=COLOR_BORDER)
    border_all = Border(
        left=thin_border_side,
        right=thin_border_side,
        top=thin_border_side,
        bottom=thin_border_side,
    )

    # =========================================================================
    # FEUILLE 1 : SUIVI DES DEVIS
    # =========================================================================
    ws_devis = wb.active
    ws_devis.title = "Suivi des Devis"
    ws_devis.views.sheetView[0].showGridLines = True

    # Bannière supérieure
    ws_devis.merge_cells("A1:K1")
    ws_devis.merge_cells("A2:K2")
    ws_devis["A1"] = "BUREAU NUMÉRIQUE BTP — SYSTÈME « DEVIS SANS OUBLI »"
    ws_devis["A2"] = "Suivi centralisé des offres, alertes de relance et protection du chiffre d'affaires"

    ws_devis["A1"].font = font_title
    ws_devis["A2"].font = font_subtitle
    ws_devis["A1"].fill = fill_banner
    ws_devis["A2"].fill = fill_banner
    ws_devis["A1"].alignment = Alignment(horizontal="center", vertical="center")
    ws_devis["A2"].alignment = Alignment(horizontal="center", vertical="center")
    ws_devis.row_dimensions[1].height = 28
    ws_devis.row_dimensions[2].height = 20

    # Ligne d'en-tête du tableau
    headers: List[str] = [
        "N° Devis",
        "Date Émission",
        "Nom du Client",
        "Téléphone",
        "Objet des Travaux / Chantier",
        "Montant HTVA (€)",
        "Statut Actuel",
        "Date Relance Prévue",
        "Statut Relance",
        "Dernier Contact",
        "Commentaires & Décisions",
    ]

    header_row = 4
    ws_devis.row_dimensions[header_row].height = 26

    for col_idx, header_text in enumerate(headers, start=1):
        cell = ws_devis.cell(row=header_row, column=col_idx, value=header_text)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = border_all

    # Données d'exemple réalistes pour un artisan en région liégeoise
    today = date.today()
    sample_data: List[DevisRow] = [
        ("DEV-2026-081", today - timedelta(days=18), "Jean-Marc Dupont", "0475 12 34 56", "Remplacement chaudière condensation gaz", 4850.00, "En attente", today - timedelta(days=4), "À RELANCER D'URGENCE", "Email devis envoyé", "Client hésitait sur la prime Wallonie"),
        ("DEV-2026-082", today - timedelta(days=12), "Sophie Lambert", "0498 22 44 66", "Rénovation électrique cuisine + tableau", 3200.00, "En attente", today - timedelta(days=1), "À RELANCER D'URGENCE", "Appel du 28/10", "Attente accord de sa banque"),
        ("DEV-2026-083", today - timedelta(days=7), "Garage Sprl Simonis", "04 223 45 67", "Installation 3 pompes à chaleur atelier", 12400.00, "Envoyé", today + timedelta(days=2), "Dans les temps", "Remis en main propre", "Décision en CA vendredi"),
        ("DEV-2026-084", today - timedelta(days=5), "Marc Vandamme", "0477 98 76 54", "Mise en conformité schéma unifilaire", 950.00, "Accepté", today + timedelta(days=10), "Gagné", "Signature reçue", "Acompte 30% versé"),
        ("DEV-2026-085", today - timedelta(days=2), "Boulangerie Le Pain d'Or", "04 252 11 22", "Dépannage chambre froide + contrat", 1680.00, "Envoyé", today + timedelta(days=5), "Dans les temps", "Envoi par mail", "Relance prévue mardi prochain"),
        ("DEV-2026-086", today - timedelta(days=25), "Patrick Henrotte", "0486 33 22 11", "Chauffage sol rez-de-chaussée 80m²", 7500.00, "Refusé", today - timedelta(days=10), "Clôturé", "Appel du client", "Trop cher, a choisi concurrent"),
        ("DEV-2026-087", today - timedelta(days=1), "Immobilière Meuse Sa", "04 221 00 00", "Remplacement 4 chauffe-eau appartements", 5200.00, "À préparer", today + timedelta(days=3), "En cours bureau", "Visite effectuée hier", "Métré en cours de calcul"),
    ]

    for row_offset, row_values in enumerate(sample_data, start=5):
        ws_devis.row_dimensions[row_offset].height = 20
        for col_idx, val in enumerate(row_values, start=1):
            cell = ws_devis.cell(row=row_offset, column=col_idx, value=val)
            cell.font = font_data
            cell.border = border_all
            cell.alignment = Alignment(vertical="center")

            # Formatage spécifique des dates et des montants
            if col_idx == 2 or col_idx == 8:
                cell.number_format = "YYYY-MM-DD"
                cell.alignment = Alignment(horizontal="center", vertical="center")
            elif col_idx == 6:
                cell.number_format = "#,##0.00 €"
                cell.alignment = Alignment(horizontal="right", vertical="center")
            elif col_idx in (1, 4, 7, 9):
                cell.alignment = Alignment(horizontal="center", vertical="center")

            # Déverrouillage des colonnes de saisie autorisées pour l'artisan
            if col_idx in (1, 2, 3, 4, 5, 6, 7, 8, 10, 11):
                cell.protection = Protection(locked=False)
            else:
                cell.protection = Protection(locked=True)

            # Coloration conditionnelle du statut de relance
            if col_idx == 9:
                if val == "À RELANCER D'URGENCE":
                    cell.fill = fill_urgent
                    cell.font = Font(name=FONT_FAMILY, size=10, bold=True, color=COLOR_DANGER_RED)
                elif val == "Gagné":
                    cell.fill = fill_ok
                    cell.font = Font(name=FONT_FAMILY, size=10, bold=True, color=COLOR_SUCCESS_GREEN)

    # Déverrouillage préventif des lignes vides 12 à 100 et injection des formules automatiques
    for empty_row in range(len(sample_data) + 5, 101):
        for col_idx in range(1, len(headers) + 1):
            empty_cell = ws_devis.cell(row=empty_row, column=col_idx)
            empty_cell.border = border_all
            empty_cell.font = font_data
            if col_idx in (1, 2, 3, 4, 5, 6, 7, 8, 10, 11):
                empty_cell.protection = Protection(locked=False)
            else:
                empty_cell.protection = Protection(locked=True)
            if col_idx in (2, 8):
                empty_cell.number_format = "YYYY-MM-DD"
                empty_cell.alignment = Alignment(horizontal="center", vertical="center")
            elif col_idx == 6:
                empty_cell.number_format = "#,##0.00 €"
                empty_cell.alignment = Alignment(horizontal="right", vertical="center")
            elif col_idx in (1, 4, 7, 9):
                empty_cell.alignment = Alignment(horizontal="center", vertical="center")

        # Formule automatique de date de relance prévue (J+14 par défaut)
        ws_devis.cell(row=empty_row, column=8, value=f'=IF(B{empty_row}="","",B{empty_row}+14)')
        # Formule automatique du statut de relance
        ws_devis.cell(
            row=empty_row,
            column=9,
            value=(
                f'=IF(G{empty_row}="","",IF(G{empty_row}="Accepté","Gagné",'
                f'IF(G{empty_row}="Refusé","Clôturé",'
                f'IF(OR(G{empty_row}="En attente",G{empty_row}="Envoyé"),'
                f'IF(AND(H{empty_row}<>"",TODAY()>H{empty_row}),"À RELANCER D\'URGENCE","Dans les temps"),'
                f'IF(G{empty_row}="À préparer","En cours bureau","")))))'
            )
        )

    # Mention légale de décharge en bas de la feuille Suivi des Devis
    disclaimer_text = (
        "AVERTISSEMENT LÉGAL : Cet outil est une aide organisationnelle interne. "
        "La validation définitive des prix, métrés, conditions contractuelles et délais légaux "
        "relève de la responsabilité exclusive du dirigeant d'entreprise."
    )
    ws_devis.cell(row=103, column=1, value=disclaimer_text).font = Font(name=FONT_FAMILY, size=8, italic=True, color="888888")

    # Activation de la protection par mot de passe contre les fausses manipulations
    ws_devis.protection.sheet = True
    ws_devis.protection.password = "BTP2026"

    # Ajustement automatique des largeurs de colonnes
    col_widths = {
        "A": 16,  # N° Devis
        "B": 14,  # Date
        "C": 24,  # Client
        "D": 16,  # Téléphone
        "E": 40,  # Objet chantier
        "F": 18,  # Montant HTVA
        "G": 16,  # Statut actuel
        "H": 18,  # Date relance
        "I": 24,  # Statut relance
        "J": 22,  # Dernier contact
        "K": 35,  # Commentaires
    }
    for col_letter, width in col_widths.items():
        ws_devis.column_dimensions[col_letter].width = width

    # =========================================================================
    # FEUILLE 2 : TABLEAU DE BORD (DASHBOARD PATRON)
    # =========================================================================
    ws_dash = wb.create_sheet(title="Tableau de Bord")
    ws_dash.views.sheetView[0].showGridLines = True

    # Bannière Dashboard
    ws_dash.merge_cells("A1:G1")
    ws_dash.merge_cells("A2:G2")
    ws_dash["A1"] = "TABLEAU DE BORD DU DIRIGEANT — SYNTHÈSE COMMERCIALE"
    ws_dash["A2"] = "Vision instantanée de la trésorerie en attente et des devis à sauver"
    ws_dash["A1"].font = font_title
    ws_dash["A2"].font = font_subtitle
    ws_dash["A1"].fill = fill_banner
    ws_dash["A2"].fill = fill_banner
    ws_dash["A1"].alignment = Alignment(horizontal="center", vertical="center")
    ws_dash["A2"].alignment = Alignment(horizontal="center", vertical="center")
    ws_dash.row_dimensions[1].height = 28
    ws_dash.row_dimensions[2].height = 20

    # KPI 1 : Devis en cours de décision
    ws_dash.merge_cells("B4:C4")
    ws_dash.merge_cells("B5:C5")
    ws_dash["B4"] = "DEVIS EN ATTENTE (VOLUME)"
    ws_dash["B5"] = '=COUNTIF(\'Suivi des Devis\'!G5:G100, "En attente") + COUNTIF(\'Suivi des Devis\'!G5:G100, "Envoyé")'
    ws_dash["B4"].font = font_card_title
    ws_dash["B5"].font = font_card_value
    ws_dash["B4"].fill = fill_card
    ws_dash["B5"].fill = fill_card
    ws_dash["B4"].alignment = Alignment(horizontal="center", vertical="center")
    ws_dash["B5"].alignment = Alignment(horizontal="center", vertical="center")

    # KPI 2 : Chiffre d'Affaires en attente de signature
    ws_dash.merge_cells("E4:F4")
    ws_dash.merge_cells("E5:F5")
    ws_dash["E4"] = "CA EN ATTENTE DE SIGNATURE"
    ws_dash["E5"] = '=SUMIF(\'Suivi des Devis\'!G5:G100, "En attente", \'Suivi des Devis\'!F5:F100) + SUMIF(\'Suivi des Devis\'!G5:G100, "Envoyé", \'Suivi des Devis\'!F5:F100)'
    ws_dash["E4"].font = font_card_title
    ws_dash["E5"].font = Font(name=FONT_FAMILY, size=18, bold=True, color=COLOR_ACCENT_ORANGE)
    ws_dash["E4"].fill = fill_card
    ws_dash["E5"].fill = fill_card
    ws_dash["E5"].number_format = "#,##0.00 €"
    ws_dash["E4"].alignment = Alignment(horizontal="center", vertical="center")
    ws_dash["E5"].alignment = Alignment(horizontal="center", vertical="center")

    # KPI 3 : Chiffre d'affaires gagné
    ws_dash.merge_cells("B7:C7")
    ws_dash.merge_cells("B8:C8")
    ws_dash["B7"] = "CA SIGNÉ / ACCEPTÉ"
    ws_dash["B8"] = '=SUMIF(\'Suivi des Devis\'!G5:G100, "Accepté", \'Suivi des Devis\'!F5:F100)'
    ws_dash["B7"].font = font_card_title
    ws_dash["B8"].font = Font(name=FONT_FAMILY, size=18, bold=True, color=COLOR_SUCCESS_GREEN)
    ws_dash["B7"].fill = fill_card
    ws_dash["B8"].fill = fill_card
    ws_dash["B8"].number_format = "#,##0.00 €"
    ws_dash["B7"].alignment = Alignment(horizontal="center", vertical="center")
    ws_dash["B8"].alignment = Alignment(horizontal="center", vertical="center")

    # KPI 4 : Devis en retard critique de relance
    ws_dash.merge_cells("E7:F7")
    ws_dash.merge_cells("E8:F8")
    ws_dash["E7"] = "ALERTES DEVIS À RELANCER"
    ws_dash["E8"] = '=COUNTIF(\'Suivi des Devis\'!I5:I100, "À RELANCER D\'URGENCE")'
    ws_dash["E7"].font = font_card_title
    ws_dash["E8"].font = Font(name=FONT_FAMILY, size=18, bold=True, color=COLOR_DANGER_RED)
    ws_dash["E7"].fill = fill_urgent
    ws_dash["E8"].fill = fill_urgent
    ws_dash["E7"].alignment = Alignment(horizontal="center", vertical="center")
    ws_dash["E8"].alignment = Alignment(horizontal="center", vertical="center")

    # Bordures des cartes KPI
    for card_range in ["B4:C5", "E4:F5", "B7:C8", "E7:F8"]:
        coords = card_range.split(":")
        top_left_col = coords[0][0]
        top_left_row = int(coords[0][1:])
        bottom_right_col = coords[1][0]
        bottom_right_row = int(coords[1][1:])
        
        for r in range(top_left_row, bottom_right_row + 1):
            for c_letter in [top_left_col, bottom_right_col]:
                col_number = openpyxl.utils.column_index_from_string(c_letter)
                ws_dash.cell(row=r, column=col_number).border = border_all

    # Tableau récapitulatif par statut
    recap_start_row = 11
    ws_dash.cell(row=recap_start_row, column=2, value="Répartition Commerciale").font = font_card_title
    ws_dash.cell(row=recap_start_row, column=3, value="Nombre").font = font_card_title
    ws_dash.cell(row=recap_start_row, column=4, value="Montant Total HTVA").font = font_card_title
    
    statuts_recap = ["À préparer", "Envoyé", "En attente", "Accepté", "Refusé"]
    for idx, stat in enumerate(statuts_recap, start=recap_start_row + 1):
        ws_dash.cell(row=idx, column=2, value=stat).font = font_data_bold
        ws_dash.cell(row=idx, column=3, value=f'=COUNTIF(\'Suivi des Devis\'!G5:G100, "{stat}")').font = font_data
        ws_dash.cell(row=idx, column=4, value=f'=SUMIF(\'Suivi des Devis\'!G5:G100, "{stat}", \'Suivi des Devis\'!F5:F100)').font = font_data
        ws_dash.cell(row=idx, column=4).number_format = "#,##0.00 €"
        
        for c in range(2, 5):
            ws_dash.cell(row=idx, column=c).border = border_all

    # Largeurs de colonnes Dashboard
    dash_widths = {"A": 5, "B": 22, "C": 18, "D": 22, "E": 22, "F": 18, "G": 5}
    for c_letter, w in dash_widths.items():
        ws_dash.column_dimensions[c_letter].width = w

    # Mention légale Dashboard
    ws_dash.cell(row=18, column=2, value=disclaimer_text).font = Font(name=FONT_FAMILY, size=8, italic=True, color="888888")

    # Protection du tableau de bord contre l'écrasement des formules
    ws_dash.protection.sheet = True
    ws_dash.protection.password = "BTP2026"

    # =========================================================================
    # FEUILLE 3 : LE RITUEL HEBDOMADAIRE (15 MINUTES CHRONO)
    # =========================================================================
    ws_rituel = wb.create_sheet(title="Rituel Hebdomadaire")
    ws_rituel.views.sheetView[0].showGridLines = True

    ws_rituel.merge_cells("A1:F1")
    ws_rituel.merge_cells("A2:F2")
    ws_rituel["A1"] = "LE RITUEL DU VENDREDI 16H30 — 15 MINUTES CHRONO"
    ws_rituel["A2"] = "La routine simple pour ne plus jamais perdre d'argent par oubli"
    ws_rituel["A1"].font = font_title
    ws_rituel["A2"].font = font_subtitle
    ws_rituel["A1"].fill = fill_banner
    ws_rituel["A2"].fill = fill_banner
    ws_rituel["A1"].alignment = Alignment(horizontal="center", vertical="center")
    ws_rituel["A2"].alignment = Alignment(horizontal="center", vertical="center")
    ws_rituel.row_dimensions[1].height = 28
    ws_rituel.row_dimensions[2].height = 20

    checklist = [
        ("Étape 1 (2 min)", "Ouvrir le classeur Excel 'Devis sans oubli' sur le PC du bureau."),
        ("Étape 2 (3 min)", "Passer en revue les chantiers signés cette semaine : changer leur statut en 'Accepté' (vert)."),
        ("Étape 3 (5 min)", "Regarder la feuille 'Tableau de Bord' : repérer les lignes rouges 'À RELANCER D'URGENCE'."),
        ("Étape 4 (5 min)", "Passer les 2 ou 3 coups de téléphone aux clients hésitants ou envoyer le modèle de relance."),
        ("Étape 5 (Bonus)", "Partir en week-end l'esprit 100 % libéré sans stress administratif !")
    ]

    for idx, (step, desc) in enumerate(checklist, start=5):
        ws_rituel.cell(row=idx, column=2, value=step).font = font_data_bold
        ws_rituel.cell(row=idx, column=2).alignment = Alignment(horizontal="center", vertical="center")
        ws_rituel.cell(row=idx, column=2).fill = fill_card
        ws_rituel.cell(row=idx, column=2).border = border_all
        
        ws_rituel.merge_cells(start_row=idx, start_column=3, end_row=idx, end_column=5)
        cell_desc = ws_rituel.cell(row=idx, column=3, value=desc)
        cell_desc.font = font_data
        cell_desc.alignment = Alignment(vertical="center")
        
        for c in range(3, 6):
            ws_rituel.cell(row=idx, column=c).border = border_all
        ws_rituel.row_dimensions[idx].height = 26

    ws_rituel.column_dimensions["A"].width = 5
    ws_rituel.column_dimensions["B"].width = 20
    ws_rituel.column_dimensions["C"].width = 30
    ws_rituel.column_dimensions["D"].width = 30
    ws_rituel.column_dimensions["E"].width = 25
    ws_rituel.column_dimensions["F"].width = 5

    ws_rituel.protection.sheet = True
    ws_rituel.protection.password = "BTP2026"

    # Sauvegarde du fichier
    wb.save(output_path)
    print(f"[OK] Fichier Excel généré avec succès : {output_path}")


if __name__ == "__main__":
    create_devis_sans_oubli_workbook(DEFAULT_WORKBOOK_PATH)
