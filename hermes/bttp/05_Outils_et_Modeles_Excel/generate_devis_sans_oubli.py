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

    # =========================================================================
    # FEUILLE 4 : CALCULATEUR DE RENTABILITÉ & COEFFICIENT K (CP 124)
    # =========================================================================
    ws_marge = wb.create_sheet(title="Calculateur Marge & Coeff K")
    ws_marge.views.sheetView[0].showGridLines = True

    ws_marge.merge_cells("A1:G1")
    ws_marge.merge_cells("A2:G2")
    ws_marge["A1"] = "CALCULATEUR DE DÉBOURSÉ SEC & COEFFICIENT K (BTP BELGE CP 124)"
    ws_marge["A2"] = "Blindage des marges, calcul du coût réel ouvrier chargé et prix plancher non négociable"
    ws_marge["A1"].font = font_title
    ws_marge["A2"].font = font_subtitle
    ws_marge["A1"].fill = fill_banner
    ws_marge["A2"].fill = fill_banner
    ws_marge["A1"].alignment = Alignment(horizontal="center", vertical="center")
    ws_marge["A2"].alignment = Alignment(horizontal="center", vertical="center")
    ws_marge.row_dimensions[1].height = 28
    ws_marge.row_dimensions[2].height = 20

    # Section 1 : Déboursé Sec (DS)
    ws_marge.cell(row=4, column=2, value="1. DÉBOURSÉ SEC (DÉPENSES DIRECTES DU CHANTIER)").font = font_card_title
    ds_labels = [
        ("Fournitures & Matériaux bruts (€ HTVA)", 4500.0, "#,##0.00 €", True),
        ("Majoration pertes & chutes de découpe (%)", 0.10, "0.0%", True),
        ("Consommables d'atelier (silicone, chevilles, vis) (%)", 0.04, "0.0%", True),
        ("Heures ouvriers prévues sur chantier (h)", 75.0, "0.0", True),
        ("Salaire horaire brut ouvrier CP 124 (€/h)", 18.50, "#,##0.00 €", True),
        ("Coût horaire chargé réel (ONSS 32.5% + Assur 5% + FSE 13%)", "=C9*(1+0.325+0.05+0.13)", "#,##0.00 €", False),
        ("Évacuation gravats / déchetterie / benne (€)", 200.0, "#,##0.00 €", True),
        ("Sous-traitance éventuelle (€ HTVA)", 0.0, "#,##0.00 €", True),
        ("TOTAL DÉBOURSÉ SEC (DS) CHANTIER", "=C5*(1+C6+C7) + (C8*C10) + C11 + C12", "#,##0.00 €", False),
    ]

    for idx, (lbl, default_val, num_fmt, is_unlocked) in enumerate(ds_labels, start=5):
        cell_lbl = ws_marge.cell(row=idx, column=2, value=lbl)
        cell_lbl.font = font_data_bold if idx == 13 else font_data
        cell_lbl.border = border_all

        cell_val = ws_marge.cell(row=idx, column=3, value=default_val)
        cell_val.font = Font(name=FONT_FAMILY, size=11, bold=(idx == 13), color="1B365D" if idx == 13 else "000000")
        cell_val.number_format = num_fmt
        cell_val.alignment = Alignment(horizontal="right", vertical="center")
        cell_val.border = border_all

        if idx == 13:
            cell_lbl.fill = fill_card
            cell_val.fill = fill_card

        if is_unlocked:
            cell_val.protection = Protection(locked=False)
        else:
            cell_val.protection = Protection(locked=True)

    # Section 2 : Coefficient K et Prix de Vente
    ws_marge.cell(row=4, column=5, value="2. COEFFICIENT K & PRIX PLANCHER").font = font_card_title
    k_labels = [
        ("Frais généraux atelier/véhicule/outillage (%)", 0.18, "0.0%", True),
        ("Marge bénéficiaire nette cible (%)", 0.15, "0.0%", True),
        ("COEFFICIENT MULTIPLICATEUR K", "=(1+F5)/(1-F6)", "0.000", False),
        ("PRIX DE VENTE MINIMUM RECOMMANDÉ (HTVA)", "=C13*F7", "#,##0.00 €", False),
        ("VOTRE PRIX DU DEVIS AU CLIENT (€ HTVA)", 10500.0, "#,##0.00 €", True),
        ("VERDICT DU CHANTIER", '=IF(F9>=F8, "✅ PRIX RENTABLE", "🚨 FUITE DE MARGE (" & TEXT(F8-F9, "#,##0.00 €") & ")")', "@", False),
    ]

    for idx, (lbl, default_val, num_fmt, is_unlocked) in enumerate(k_labels, start=5):
        actual_row = 5 if idx == 5 else (6 if idx == 6 else (7 if idx == 7 else (9 if idx == 8 else (11 if idx == 9 else 13))))
        cell_lbl = ws_marge.cell(row=actual_row, column=5, value=lbl)
        cell_lbl.font = font_data_bold if actual_row in (9, 13) else font_data
        cell_lbl.border = border_all

        cell_val = ws_marge.cell(row=actual_row, column=6, value=default_val)
        cell_val.font = Font(name=FONT_FAMILY, size=11, bold=(actual_row in (9, 13)), color=COLOR_DANGER_RED if actual_row == 13 else "000000")
        cell_val.number_format = num_fmt
        cell_val.alignment = Alignment(horizontal="right", vertical="center")
        cell_val.border = border_all

        if actual_row in (9, 13):
            cell_lbl.fill = fill_card
            cell_val.fill = fill_card

        if is_unlocked:
            cell_val.protection = Protection(locked=False)
        else:
            cell_val.protection = Protection(locked=True)

    ws_marge.column_dimensions["A"].width = 4
    ws_marge.column_dimensions["B"].width = 44
    ws_marge.column_dimensions["C"].width = 18
    ws_marge.column_dimensions["D"].width = 5
    ws_marge.column_dimensions["E"].width = 40
    ws_marge.column_dimensions["F"].width = 25
    ws_marge.column_dimensions["G"].width = 4

    ws_marge.protection.sheet = True
    ws_marge.protection.password = "BTP2026"

    # =========================================================================
    # FEUILLE 5 : AVENANTS DE CHANTIER & ATTESTATION TVA 6%
    # =========================================================================
    ws_avenant = wb.create_sheet(title="Avenants & TVA 6%")
    ws_avenant.views.sheetView[0].showGridLines = True

    ws_avenant.merge_cells("A1:G1")
    ws_avenant.merge_cells("A2:G2")
    ws_avenant["A1"] = "AVENANTS MINUTE SMARTPHONE & ATTESTATION FISCALE TVA 6%"
    ws_avenant["A2"] = "Sécurisation des travaux supplémentaires imprévus et protection légale contre redressement fiscal"
    ws_avenant["A1"].font = font_title
    ws_avenant["A2"].font = font_subtitle
    ws_avenant["A1"].fill = fill_banner
    ws_avenant["A2"].fill = fill_banner
    ws_avenant["A1"].alignment = Alignment(horizontal="center", vertical="center")
    ws_avenant["A2"].alignment = Alignment(horizontal="center", vertical="center")
    ws_avenant.row_dimensions[1].height = 28
    ws_avenant.row_dimensions[2].height = 20

    # Section A : Avenant Minute WhatsApp
    ws_avenant.cell(row=4, column=2, value="GÉNÉRATEUR D'AVENANT TRAVAUX SMARTPHONE (ANTI-TRAVAIL GRATUIT)").font = font_card_title
    av_fields = [
        ("Réf Devis Initial", "DEV-2026-042", True),
        ("Nom du Client", "Monsieur Dupont", True),
        ("Adresse Chantier", "Chaudfontaine", True),
        ("Description Travaux Supplémentaires", "Ajout 3 vannes thermostatiques connectées + désembouage", True),
        ("Montant Supplémentaire HTVA (€)", 680.0, True),
        ("Taux TVA Applicable (%)", 0.06, True),
        ("Montant TVA (€)", "=C9*C10", False),
        ("TOTAL AVENANT TVAC (€)", "=C9+C11", False),
        ("Acompte Matériel Requis (€)", 200.0, True),
        ("Délai Ajouté au Chantier (jours)", 1, True),
    ]

    for idx, (lbl, d_val, is_unlocked) in enumerate(av_fields, start=5):
        c_lbl = ws_avenant.cell(row=idx, column=2, value=lbl)
        c_lbl.font = font_data_bold if idx in (9, 12) else font_data
        c_lbl.border = border_all

        c_val = ws_avenant.cell(row=idx, column=3, value=d_val)
        c_val.font = Font(name=FONT_FAMILY, size=10, bold=(idx == 12))
        c_val.border = border_all
        c_val.alignment = Alignment(vertical="center")

        if idx in (9, 11, 12, 13):
            c_val.number_format = "#,##0.00 €"
            c_val.alignment = Alignment(horizontal="right", vertical="center")
        elif idx == 10:
            c_val.number_format = "0.0%"
            c_val.alignment = Alignment(horizontal="right", vertical="center")

        if is_unlocked:
            c_val.protection = Protection(locked=False)
        else:
            c_val.protection = Protection(locked=True)

    # Texte WhatsApp généré
    ws_avenant.cell(row=16, column=2, value="MESSAGE WHATSAPP PRÊT À ENVOYER AU CLIENT :").font = font_card_title
    ws_avenant.merge_cells("B17:F19")
    txt_formula = '="Bonjour " & C6 & ", suite à votre demande sur chantier à " & C7 & " : Avenant pour " & C8 & " = " & TEXT(C9, "#,##0.00 €") & " HTVA (soit " & TEXT(C12, "#,##0.00 €") & " TVAC). Répondez simplement OUI à ce message pour validation des travaux."'
    cell_msg = ws_avenant.cell(row=17, column=2, value=txt_formula)
    cell_msg.font = Font(name=FONT_FAMILY, size=9, italic=True, color="1B365D")
    cell_msg.fill = fill_card
    cell_msg.alignment = Alignment(wrap_text=True, vertical="center")
    cell_msg.protection = Protection(locked=True)

    # Section B : Attestation TVA 6% légale
    ws_avenant.cell(row=21, column=2, value="MENTION LÉGALE OBLIGATOIRE TVA 6% (LOGEMENT > 10 ANS) — AR N° 20 ART. 17 § 1").font = font_card_title
    ws_avenant.merge_cells("B22:F25")
    legal_tva_text = (
        "« En l’absence de contestation écrite dans un délai d’un mois à compter de la réception de la facture, "
        "le client est présumé reconnaître que les travaux sont effectués à un bâtiment dont la première occupation date "
        "d'au moins 10 ans, affecté effectivement et à titre prépondérant à un logement privé. Si ces conditions ne sont pas "
        "remplies, la responsabilité relative au paiement de la taxe, des intérêts et des amendes sera reportée sur le client. »"
    )
    cell_legal = ws_avenant.cell(row=22, column=2, value=legal_tva_text)
    cell_legal.font = Font(name=FONT_FAMILY, size=8, italic=True, color="555555")
    cell_legal.fill = fill_ok
    cell_legal.alignment = Alignment(wrap_text=True, vertical="center")
    cell_legal.protection = Protection(locked=True)

    ws_avenant.column_dimensions["A"].width = 4
    ws_avenant.column_dimensions["B"].width = 38
    ws_avenant.column_dimensions["C"].width = 25
    ws_avenant.column_dimensions["D"].width = 15
    ws_avenant.column_dimensions["E"].width = 15
    ws_avenant.column_dimensions["F"].width = 20
    ws_avenant.column_dimensions["G"].width = 4

    ws_avenant.protection.sheet = True
    ws_avenant.protection.password = "BTP2026"

    # Sauvegarde du fichier
    wb.save(output_path)
    print(f"[OK] Fichier Excel généré avec succès : {output_path}")


if __name__ == "__main__":
    create_devis_sans_oubli_workbook(DEFAULT_WORKBOOK_PATH)
