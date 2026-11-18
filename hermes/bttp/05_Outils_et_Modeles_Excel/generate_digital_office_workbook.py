"""
Générateur professionnel de classeur Excel pour le Bureau Numérique Universel.
Crée le fichier 'SUIVI_AFFAIRES_MODELE_PRO.xlsx' (ou spécifique BTP 'DEVIS_SANS_OUBLI_MODELE_PRO.xlsx')
avec zonage ergonomique, formules dynamiques vivantes et protection par mot de passe.
Strictement typé, zéro 'Any'.
"""

import argparse
import os
import sys
from datetime import date, timedelta
from typing import Dict, Final, List, Optional, Tuple, TypedDict
import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Protection, Side
from openpyxl.utils import get_column_letter

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


class SectorConfig(TypedDict):
    title_banner: str
    subtitle_banner: str
    sheet_title: str
    ref_col_name: str
    object_col_name: str
    amount_col_name: str
    delay_days: int
    prefix_id: str
    password: str
    sample_deals: List[Tuple[str, str, str, str, float, str, int]]


SECTOR_CONFIGS: Final[Dict[str, SectorConfig]] = {
    "btp": {
        "title_banner": "BUREAU NUMÉRIQUE BTP — SYSTÈME « DEVIS SANS OUBLI »",
        "subtitle_banner": "Suivi centralisé des offres, alertes de relance et protection du chiffre d'affaires",
        "sheet_title": "Suivi des Devis",
        "ref_col_name": "N° Devis",
        "object_col_name": "Objet des Travaux / Chantier",
        "amount_col_name": "Montant HTVA (€)",
        "delay_days": 14,
        "prefix_id": "DEV",
        "password": "OFFICE2026",
        "sample_deals": [
            ("Martin Sprl", "0470 12 34 56", "Rénovation toiture & isolation 120m²", "Wavre", 12500.0, "Accepté", -20),
            ("Dupont Résidence", "0485 98 76 54", "Remplacement chaudière condensation gaz", "Liège", 4200.0, "En attente", -16),
            ("Lambert SA", "0477 11 22 33", "Installation pompe à chaleur air-eau", "Namur", 8900.0, "Envoyé", -5),
            ("Boulangerie Meuse", "0495 55 44 33", "Mise en conformité électrique triphasé", "Huy", 3400.0, "En attente", -22),
            ("Immo Fléron Sprl", "0471 88 99 00", "Rénovation sanitaire 3 appartements", "Fléron", 7800.0, "Accepté", -10),
            ("Vermeulen SPRL", "0488 44 55 66", "Chape et carrelage rez-de-chaussée", "Liège", 5100.0, "En attente", -1),
            ("Renard SPRL", "0499 66 77 88", "Aménagement combles & faux plafonds", "Herstal", 2900.0, "À préparer", 0),
        ],
    },
    "services": {
        "title_banner": "BUREAU NUMÉRIQUE SERVICES & CONSEIL — SYSTÈME « PROPOSITIONS SANS OUBLI »",
        "subtitle_banner": "Pilotage des offres commerciales, relances douces et optimisation du TJM",
        "sheet_title": "Suivi des Devis",
        "ref_col_name": "Réf Proposition",
        "object_col_name": "Objet de la Mission / Prestation",
        "amount_col_name": "Budget HTVA (€)",
        "delay_days": 7,
        "prefix_id": "PROP",
        "password": "OFFICE2026",
        "sample_deals": [
            ("NexTech SA", "0472 11 22 33", "Refonte application web React & FastAPI", "Bruxelles", 8500.0, "Accepté", -15),
            ("GreenPulse Sprl", "0484 33 44 55", "Audit SEO & Stratégie de contenu B2B", "Liège", 2400.0, "En attente", -9),
            ("Fiduciaire Mosane", "0479 66 77 88", "Automatisation pipelines comptables", "Namur", 4800.0, "Envoyé", -3),
            ("Atelier Bois & Co", "0491 22 33 44", "Création identité visuelle et packaging", "Verviers", 1800.0, "En attente", -12),
            ("ScaleUp Partners", "0475 99 88 77", "Accompagnement CTO as a Service 3 mois", "Liège", 6000.0, "Accepté", -8),
            ("ImmoConseil", "0489 12 34 56", "Campagne publicitaire Google Ads & Meta", "Liège", 1500.0, "À préparer", 0),
        ],
    },
    "maintenance": {
        "title_banner": "BUREAU NUMÉRIQUE MAINTENANCE & ATELIER — SYSTÈME « ORDRES DE RÉPARATION »",
        "subtitle_banner": "Suivi des devis de remise en état, libération des ponts et flux pièces",
        "sheet_title": "Suivi des Devis",
        "ref_col_name": "N° Fiche OR",
        "object_col_name": "Véhicule / Machine & Intervention",
        "amount_col_name": "Devis Pièces & MO HTVA (€)",
        "delay_days": 3,
        "prefix_id": "OR",
        "password": "OFFICE2026",
        "sample_deals": [
            ("Transport Ardennes", "0473 44 55 66", "Remplacement embrayage & volant moteur", "Camionnette Ford", 1850.0, "Accepté", -6),
            ("Dubois Jean", "0486 77 88 99", "Kit distribution + pompe à eau", "Peugeot 308", 780.0, "En attente", -4),
            ("Menuiserie Closset", "0478 22 33 44", "Révision compresseur industriel 500L", "Atelier", 1200.0, "Envoyé", -1),
            ("Lemaire Sprl", "0493 55 66 77", "Remplacement turbo & injecteurs", "VW Transporter", 2400.0, "En attente", -5),
            ("Agri-Meuse", "0474 11 99 88", "Réparation vérin hydraulique tracteur", "Matériel agricole", 950.0, "Accepté", -4),
            ("Garage Partner", "0482 33 11 00", "Diagnostic électronique & calculateurs", "Audi A4", 450.0, "À préparer", 0),
        ],
    },
    "healthcare": {
        "title_banner": "BUREAU NUMÉRIQUE SANTÉ & SOINS — SYSTÈME « PLANS DE SOINS & SUIVI »",
        "subtitle_banner": "Continuité des protocoles de soins, suivi des forfaits et respect déontologique",
        "sheet_title": "Suivi des Devis",
        "ref_col_name": "Réf Protocole",
        "object_col_name": "Protocole de Soins / Forfait Traitement",
        "amount_col_name": "Honoraires Forfait (€)",
        "delay_days": 5,
        "prefix_id": "SOIN",
        "password": "OFFICE2026",
        "sample_deals": [
            ("Patient B.M.", "0471 23 45 67", "Rééducation post-opératoire genou (12 s.)", "Cabinet", 480.0, "Accepté", -10),
            ("Patiente C.D.", "0487 65 43 21", "Bilan postural complet & semelles", "Cabinet", 250.0, "En attente", -7),
            ("Patient E.F.", "0476 11 22 33", "Programme réathlétisation épaule (8 s.)", "Centre", 360.0, "Envoyé", -2),
            ("Patiente G.H.", "0494 33 22 11", "Cure thermo-active bien-être (5 séances)", "Espace Santé", 450.0, "En attente", -8),
            ("Patient I.J.", "0478 99 00 11", "Protocole rachis cervical & ergonomie", "Cabinet", 320.0, "Accepté", -6),
            ("Patiente K.L.", "0485 12 98 76", "Bilan diététique & micronutrition 3 mois", "Cabinet", 280.0, "À préparer", 0),
        ],
    },
    "retail": {
        "title_banner": "BUREAU NUMÉRIQUE COMMERCE B2B — SYSTÈME « COMMANDES & RÉASSORTS »",
        "subtitle_banner": "Suivi des commandes récurrentes, relances réassort et sécurisation du volume",
        "sheet_title": "Suivi des Devis",
        "ref_col_name": "N° Bon Commande",
        "object_col_name": "Volume Produits / Réassort Prévu",
        "amount_col_name": "Montant Commande HTVA (€)",
        "delay_days": 5,
        "prefix_id": "CMD",
        "password": "OFFICE2026",
        "sample_deals": [
            ("Brasserie du Centre", "0470 99 88 77", "Lot 50 fûts bière artisanale 30L", "Horeca Liège", 3750.0, "Accepté", -8),
            ("Hôtel de la Paix", "0486 11 22 33", "Réassort café torréfié 60kg", "Horeca Namur", 1320.0, "En attente", -6),
            ("Restaurant L'Olivier", "0477 44 55 66", "Fourniture hebdomadaire pains spéciaux", "Horeca Huy", 850.0, "Envoyé", -2),
            ("Épicerie Bio Terre", "0492 88 77 66", "Farines meule de pierre 500kg", "Commerce bio", 950.0, "En attente", -9),
            ("Traiteur Événement", "0474 33 22 11", "Buffet entreprise 150 personnes", "Corporate", 4200.0, "Accepté", -7),
            ("Bistro Mosan", "0483 55 44 33", "Assortiment jus artisanaux 200 bouteilles", "Horeca Liège", 620.0, "À préparer", 0),
        ],
    },
    "general": {
        "title_banner": "BUREAU NUMÉRIQUE UNIVERSEL — SYSTÈME « SUIVI DES AFFAIRES & DEVIS »",
        "subtitle_banner": "Pilotage des offres, relances automatiques et protection du chiffre d'affaires",
        "sheet_title": "Suivi des Devis",
        "ref_col_name": "N° Affaire / Devis",
        "object_col_name": "Objet de la Prestation / Projet",
        "amount_col_name": "Montant HTVA (€)",
        "delay_days": 7,
        "prefix_id": "AFF",
        "password": "OFFICE2026",
        "sample_deals": [
            ("Client Partenaire Sprl", "0470 12 34 56", "Prestation d'organisation & conseil", "Liège", 3500.0, "Accepté", -12),
            ("Entreprise Alpha", "0485 98 76 54", "Déploiement solution technique", "Namur", 2800.0, "En attente", -9),
            ("Société Bêta SA", "0477 11 22 33", "Fourniture matériel et installation", "Bruxelles", 5400.0, "Envoyé", -3),
            ("Cabinet Gamma", "0495 55 44 33", "Mission d'assistance opérationnelle", "Huy", 1900.0, "En attente", -11),
            ("Compagnie Delta", "0471 88 99 00", "Contrat annuel de maintenance", "Liège", 4500.0, "Accepté", -8),
            ("Groupe Epsilon", "0488 44 55 66", "Étude préalable & diagnostic", "Verviers", 1200.0, "À préparer", 0),
        ],
    },
}

FONT_FAMILY: Final[str] = "Calibri"
COLOR_PRIMARY_NAVY: Final[str] = "1B365D"
COLOR_HEADER_FILL: Final[str] = "244061"
COLOR_LIGHT_BG: Final[str] = "F2F5F9"
COLOR_SUCCESS_GREEN: Final[str] = "27AE60"
COLOR_DANGER_RED: Final[str] = "C0392B"
COLOR_BORDER: Final[str] = "D9D9D9"


def create_digital_office_workbook(
    output_path: str,
    sector: str = "general",
    company_name: str = "Bureau Numérique",
) -> None:
    """
    Génère le classeur Excel professionnel avec zonage protégé et formules vivantes.
    """
    sec = sector.lower().strip()
    if sec not in SECTOR_CONFIGS:
        sec = "general"
    cfg = SECTOR_CONFIGS[sec]

    wb = openpyxl.Workbook()

    font_title = Font(name=FONT_FAMILY, size=15, bold=True, color="FFFFFF")
    font_subtitle = Font(name=FONT_FAMILY, size=10, italic=True, color="FFFFFF")
    font_header = Font(name=FONT_FAMILY, size=10, bold=True, color="FFFFFF")
    font_card_title = Font(name=FONT_FAMILY, size=9, bold=True, color="555555")
    font_card_value = Font(name=FONT_FAMILY, size=16, bold=True, color="1B365D")
    font_data = Font(name=FONT_FAMILY, size=10)
    font_data_bold = Font(name=FONT_FAMILY, size=10, bold=True)

    fill_header = PatternFill(start_color=COLOR_HEADER_FILL, end_color=COLOR_HEADER_FILL, fill_type="solid")
    fill_banner = PatternFill(start_color=COLOR_PRIMARY_NAVY, end_color=COLOR_PRIMARY_NAVY, fill_type="solid")
    fill_card = PatternFill(start_color=COLOR_LIGHT_BG, end_color=COLOR_LIGHT_BG, fill_type="solid")
    fill_urgent = PatternFill(start_color="FDEDEC", end_color="FDEDEC", fill_type="solid")
    fill_ok = PatternFill(start_color="EAFAF1", end_color="EAFAF1", fill_type="solid")

    thin_side = Side(border_style="thin", color=COLOR_BORDER)
    border_all = Border(left=thin_side, right=thin_side, top=thin_side, bottom=thin_side)

    # -------------------------------------------------------------------------
    # FEUILLE 1 : SUIVI DES AFFAIRES / DEVIS
    # -------------------------------------------------------------------------
    ws_devis = wb.active
    ws_devis.title = cfg["sheet_title"]
    ws_devis.views.sheetView[0].showGridLines = True

    ws_devis.merge_cells("A1:K1")
    ws_devis.merge_cells("A2:K2")
    ws_devis["A1"] = cfg["title_banner"]
    ws_devis["A2"] = cfg["subtitle_banner"]

    ws_devis["A1"].font = font_title
    ws_devis["A2"].font = font_subtitle
    ws_devis["A1"].fill = fill_banner
    ws_devis["A2"].fill = fill_banner
    ws_devis["A1"].alignment = Alignment(horizontal="center", vertical="center")
    ws_devis["A2"].alignment = Alignment(horizontal="center", vertical="center")
    ws_devis.row_dimensions[1].height = 26
    ws_devis.row_dimensions[2].height = 18

    headers: List[str] = [
        cfg["ref_col_name"],
        "Date Émission",
        "Nom du Client",
        "Téléphone / Contact",
        cfg["object_col_name"],
        cfg["amount_col_name"],
        "Statut Actuel",
        f"Date Relance (J+{cfg['delay_days']})",
        "Statut Relance (Auto)",
        "Dernier Contact",
        "Commentaires / Action",
    ]

    ws_devis.row_dimensions[4].height = 24
    for col_idx, header_text in enumerate(headers, start=1):
        cell = ws_devis.cell(row=4, column=col_idx, value=header_text)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = border_all
        cell.protection = Protection(locked=True)

    today = date.today()
    current_row = 5
    counter = 1

    for sample in cfg["sample_deals"]:
        client_name, tel, objet, loc, montant, statut, delta_days = sample
        emission_date = today + timedelta(days=delta_days)
        target_date = emission_date + timedelta(days=cfg["delay_days"])
        deal_id = f"{cfg['prefix_id']}-2026-{counter:03d}"
        counter += 1

        ws_devis.row_dimensions[current_row].height = 20

        c_a = ws_devis.cell(row=current_row, column=1, value=deal_id)
        c_b = ws_devis.cell(row=current_row, column=2, value=emission_date)
        c_c = ws_devis.cell(row=current_row, column=3, value=client_name)
        c_d = ws_devis.cell(row=current_row, column=4, value=tel)
        c_e = ws_devis.cell(row=current_row, column=5, value=objet)
        c_f = ws_devis.cell(row=current_row, column=6, value=montant)
        c_g = ws_devis.cell(row=current_row, column=7, value=statut)
        c_h = ws_devis.cell(row=current_row, column=8, value=f"=IF(B{current_row}=\"\",\"\",B{current_row}+{cfg['delay_days']})")
        c_i = ws_devis.cell(row=current_row, column=9, value=f"=IF(G{current_row}=\"\",\"\",IF(G{current_row}=\"Accepté\",\"Gagné\",IF(G{current_row}=\"Refusé\",\"Clôturé\",IF(OR(G{current_row}=\"En attente\",G{current_row}=\"Envoyé\"),IF(AND(H{current_row}<>\"\",TODAY()>H{current_row}),\"À RELANCER D'URGENCE\",\"Dans les temps\"),IF(G{current_row}=\"À préparer\",\"En cours bureau\",\"\")))))")
        c_j = ws_devis.cell(row=current_row, column=10, value="Appel téléphonique" if delta_days < -10 else "Envoi de l'offre")
        c_k = ws_devis.cell(row=current_row, column=11, value="À relancer ce vendredi" if delta_days < -10 else "Dossier en cours")

        c_b.number_format = "yyyy-mm-dd"
        c_f.number_format = "#,##0.00 €"
        c_h.number_format = "yyyy-mm-dd"

        c_a.alignment = Alignment(horizontal="center")
        c_b.alignment = Alignment(horizontal="center")
        c_f.alignment = Alignment(horizontal="right")
        c_g.alignment = Alignment(horizontal="center")
        c_h.alignment = Alignment(horizontal="center")
        c_i.alignment = Alignment(horizontal="center")

        for col in range(1, 12):
            cell = ws_devis.cell(row=current_row, column=col)
            cell.font = font_data
            cell.border = border_all
            if col == 9:
                cell.protection = Protection(locked=True)
                if statut in ("En attente", "Envoyé") and target_date < today:
                    cell.fill = fill_urgent
                    cell.font = font_data_bold
                else:
                    cell.fill = fill_ok
            else:
                cell.protection = Protection(locked=False)

        current_row += 1

    # Injecter des formules vivantes dans les lignes vides (jusqu'à la ligne 100)
    for r in range(current_row, 101):
        ws_devis.row_dimensions[r].height = 19
        c_h = ws_devis.cell(row=r, column=8)
        c_h.value = f"=IF(B{r}=\"\",\"\",B{r}+{cfg['delay_days']})"
        c_h.number_format = "yyyy-mm-dd"
        c_h.alignment = Alignment(horizontal="center")

        c_i = ws_devis.cell(row=r, column=9)
        c_i.value = f"=IF(G{r}=\"\",\"\",IF(G{r}=\"Accepté\",\"Gagné\",IF(G{r}=\"Refusé\",\"Clôturé\",IF(OR(G{r}=\"En attente\",G{r}=\"Envoyé\"),IF(AND(H{r}<>\"\",TODAY()>H{r}),\"À RELANCER D'URGENCE\",\"Dans les temps\"),IF(G{r}=\"À préparer\",\"En cours bureau\",\"\")))))"
        c_i.alignment = Alignment(horizontal="center")

        ws_devis.cell(row=r, column=2).number_format = "yyyy-mm-dd"
        ws_devis.cell(row=r, column=6).number_format = "#,##0.00 €"

        for col in range(1, 12):
            cell = ws_devis.cell(row=r, column=col)
            cell.font = font_data
            cell.border = border_all
            if col == 9:
                cell.protection = Protection(locked=True)
            else:
                cell.protection = Protection(locked=False)

    # Disclaimer de pied de page
    disclaimer_row = 103
    ws_devis.merge_cells(f"A{disclaimer_row}:K{disclaimer_row}")
    disc_cell = ws_devis.cell(
        row=disclaimer_row,
        column=1,
        value="AVERTISSEMENT : Classeur protégé pour préserver l'intégrité des calculs. Saisie libre sur les colonnes 1 à 8, 10 et 11.",
    )
    disc_cell.font = Font(name=FONT_FAMILY, size=9, italic=True, color="7F8C8D")
    disc_cell.alignment = Alignment(horizontal="center")
    disc_cell.protection = Protection(locked=True)

    # Protection de la feuille
    ws_devis.protection.set_password(cfg["password"])
    ws_devis.protection.sheet = True
    ws_devis.protection.enable()

    # -------------------------------------------------------------------------
    # FEUILLE 2 : TABLEAU DE BORD EXÉCUTIF
    # -------------------------------------------------------------------------
    ws_dash = wb.create_sheet(title="Tableau de Bord")
    ws_dash.views.sheetView[0].showGridLines = True

    ws_dash.merge_cells("A1:G1")
    ws_dash.merge_cells("A2:G2")
    ws_dash["A1"] = f"TABLEAU DE BORD EXÉCUTIF — {company_name.upper()}"
    ws_dash["A2"] = "Vision temps réel du portefeuille d'affaires, taux de transformation et relances urgentes"
    ws_dash["A1"].font = font_title
    ws_dash["A2"].font = font_subtitle
    ws_dash["A1"].fill = fill_banner
    ws_dash["A2"].fill = fill_banner
    ws_dash["A1"].alignment = Alignment(horizontal="center", vertical="center")
    ws_dash["A2"].alignment = Alignment(horizontal="center", vertical="center")
    ws_dash.row_dimensions[1].height = 26
    ws_dash.row_dimensions[2].height = 18

    kpi_cards = [
        ("B4", "C4", "B5", "C5", "AFFAIRES EN COURS", f"=COUNTIF('{cfg['sheet_title']}'!G5:G100, \"En attente\") + COUNTIF('{cfg['sheet_title']}'!G5:G100, \"Envoyé\")", "0 dossiers"),
        ("E4", "F4", "E5", "F5", "MONTANT EN COURS", f"=SUMIF('{cfg['sheet_title']}'!G5:G100, \"En attente\", '{cfg['sheet_title']}'!F5:F100) + SUMIF('{cfg['sheet_title']}'!G5:G100, \"Envoyé\", '{cfg['sheet_title']}'!F5:F100)", "#,##0.00 €"),
        ("B7", "C7", "B8", "C8", "CHIFFRE SIGNÉ (GAGNÉ)", f"=SUMIF('{cfg['sheet_title']}'!G5:G100, \"Accepté\", '{cfg['sheet_title']}'!F5:F100)", "#,##0.00 €"),
        ("E7", "F7", "E8", "F8", "RELANCES URGENTES", f"=COUNTIF('{cfg['sheet_title']}'!I5:I100, \"À RELANCER D'URGENCE\")", "0 dossiers à relancer"),
    ]

    for t_c1, t_c2, v_c1, v_c2, title, formula, fmt in kpi_cards:
        ws_dash.merge_cells(f"{t_c1}:{t_c2}")
        ws_dash.merge_cells(f"{v_c1}:{v_c2}")
        cell_t = ws_dash[t_c1]
        cell_t.value = title
        cell_t.font = font_card_title
        cell_t.fill = fill_card
        cell_t.alignment = Alignment(horizontal="center", vertical="center")

        cell_v = ws_dash[v_c1]
        cell_v.value = formula
        cell_v.font = font_card_value
        cell_v.fill = fill_card
        cell_v.number_format = fmt
        cell_v.alignment = Alignment(horizontal="center", vertical="center")

        for r in (int(t_c1[1]), int(v_c1[1])):
            for col_l in (t_c1[0], t_c2[0]):
                ws_dash[f"{col_l}{r}"].border = border_all

    ws_dash.protection.set_password(cfg["password"])
    ws_dash.protection.sheet = True
    ws_dash.protection.enable()

    # -------------------------------------------------------------------------
    # FEUILLE 3 : RITUEL HEBDOMADAIRE (15 MINUTES LE VENDREDI)
    # -------------------------------------------------------------------------
    ws_rituel = wb.create_sheet(title="Rituel Hebdomadaire")
    ws_rituel.views.sheetView[0].showGridLines = True

    ws_rituel.merge_cells("A1:E1")
    ws_rituel.merge_cells("A2:E2")
    ws_rituel["A1"] = "LE RITUEL HEBDOMADAIRE DE 16H30 (15 MINUTES CHRONO)"
    ws_rituel["A2"] = "La méthode simple pour ne plus jamais perdre une affaire faute de temps"
    ws_rituel["A1"].font = font_title
    ws_rituel["A2"].font = font_subtitle
    ws_rituel["A1"].fill = fill_banner
    ws_rituel["A2"].fill = fill_banner
    ws_rituel["A1"].alignment = Alignment(horizontal="center", vertical="center")
    ws_rituel["A2"].alignment = Alignment(horizontal="center", vertical="center")

    steps: List[Tuple[str, str, str]] = [
        ("Étape 1 (2 min)", "Ouvrir le classeur et regarder le montant en attente", "Visualiser l'argent qui dort dans le pipeline pour se motiver."),
        ("Étape 2 (3 min)", "Mettre en vert les affaires acceptées cette semaine", "Passer le statut à 'Accepté' : le chiffre bascule automatiquement en 'Gagné'."),
        ("Étape 3 (5 min)", "Repérer les lignes rouges 'À RELANCER D'URGENCE'", "Filtrer ou parcourir les dossiers où le client n'a pas répondu dans le délai."),
        ("Étape 4 (5 min)", "Passer 3 appels ou envoyer les messages de relance types", "Appeler ou vocaliser les 3 prospects avec le script de courtoisie du week-end."),
    ]

    ws_rituel.row_dimensions[4].height = 24
    ws_rituel.cell(row=4, column=1, value="Étape").font = font_header
    ws_rituel.cell(row=4, column=1).fill = fill_header
    ws_rituel.cell(row=4, column=2, value="Action Clé").font = font_header
    ws_rituel.cell(row=4, column=2).fill = fill_header
    ws_rituel.merge_cells("C4:E4")
    ws_rituel.cell(row=4, column=3, value="Objectif & Bénéfice").font = font_header
    ws_rituel.cell(row=4, column=3).fill = fill_header

    for idx, (et, act, obj) in enumerate(steps, start=5):
        ws_rituel.row_dimensions[idx].height = 24
        c1 = ws_rituel.cell(row=idx, column=1, value=et)
        c2 = ws_rituel.cell(row=idx, column=2, value=act)
        ws_rituel.merge_cells(f"C{idx}:E{idx}")
        c3 = ws_rituel.cell(row=idx, column=3, value=obj)
        for col in range(1, 6):
            c = ws_rituel.cell(row=idx, column=col)
            c.font = font_data
            c.border = border_all
            c.protection = Protection(locked=True)

    ws_rituel.protection.set_password(cfg["password"])
    ws_rituel.protection.sheet = True
    ws_rituel.protection.enable()

    # Ajustement largeur des colonnes
    col_widths = [16, 14, 25, 18, 38, 16, 14, 18, 24, 20, 26]
    for idx, w in enumerate(col_widths, start=1):
        letter = get_column_letter(idx)
        ws_devis.column_dimensions[letter].width = w

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    wb.save(output_path)
    print(f"[OK] Classeur généré ({sec.upper()}) : {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Générateur de classeur Excel Bureau Numérique Universel.")
    parser.add_argument("--output", "-o", default="SUIVI_AFFAIRES_MODELE_PRO.xlsx", help="Chemin du fichier Excel")
    parser.add_argument("--sector", "-s", default="general", choices=["btp", "services", "maintenance", "healthcare", "retail", "general"], help="Secteur d'activité")
    parser.add_argument("--company", "-c", default="Bureau Numérique", help="Nom de l'entreprise")
    args = parser.parse_args()

    create_digital_office_workbook(args.output, sector=args.sector, company_name=args.company)


if __name__ == "__main__":
    main()
