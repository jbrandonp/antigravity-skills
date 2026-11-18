import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def build_workbook():
    wb = openpyxl.Workbook()
    
    # Color palette
    NAVY_DARK = "1A365D"
    NAVY_MED = "2B6CB0"
    NAVY_LIGHT = "EBF8FF"
    SLATE_GRAY = "4A5568"
    LIGHT_GRAY = "F7FAFC"
    BORDER_GRAY = "CBD5E0"
    WHITE = "FFFFFF"
    GOLD_ACCENT = "D69E2E"
    GREEN_ACCENT = "2F855A"
    RED_ACCENT = "C53030"
    
    # Styles
    font_title = Font(name="Calibri", size=16, bold=True, color=WHITE)
    font_subtitle = Font(name="Calibri", size=11, italic=True, color=NAVY_LIGHT)
    font_section = Font(name="Calibri", size=13, bold=True, color=NAVY_DARK)
    font_header = Font(name="Calibri", size=11, bold=True, color=WHITE)
    font_sub_header = Font(name="Calibri", size=11, bold=True, color=NAVY_DARK)
    font_data = Font(name="Calibri", size=10, color="000000")
    font_bold = Font(name="Calibri", size=10, bold=True, color="000000")
    font_total = Font(name="Calibri", size=11, bold=True, color=NAVY_DARK)
    
    fill_title = PatternFill(start_color=NAVY_DARK, end_color=NAVY_DARK, fill_type="solid")
    fill_header = PatternFill(start_color=NAVY_MED, end_color=NAVY_MED, fill_type="solid")
    fill_sub_header = PatternFill(start_color=NAVY_LIGHT, end_color=NAVY_LIGHT, fill_type="solid")
    fill_zebra = PatternFill(start_color=LIGHT_GRAY, end_color=LIGHT_GRAY, fill_type="solid")
    fill_total = PatternFill(start_color="EDF2F7", end_color="EDF2F7", fill_type="solid")
    fill_accent_green = PatternFill(start_color="C6F6D5", end_color="C6F6D5", fill_type="solid")
    fill_accent_gold = PatternFill(start_color="FEFCBF", end_color="FEFCBF", fill_type="solid")
    
    thin_border = Border(
        left=Side(style='thin', color=BORDER_GRAY),
        right=Side(style='thin', color=BORDER_GRAY),
        top=Side(style='thin', color=BORDER_GRAY),
        bottom=Side(style='thin', color=BORDER_GRAY)
    )
    total_border = Border(
        top=Side(style='thin', color=NAVY_DARK),
        bottom=Side(style='double', color=NAVY_DARK)
    )
    
    align_left = Alignment(horizontal='left', vertical='center')
    align_right = Alignment(horizontal='right', vertical='center')
    align_center = Alignment(horizontal='center', vertical='center')
    align_wrap = Alignment(horizontal='left', vertical='center', wrap_text=True)

    # =========================================================================
    # SHEET 1: SYNTHÈSE OPÉRATION
    # =========================================================================
    ws1 = wb.active
    ws1.title = "01_Synthèse_Opération"
    ws1.views.sheetView[0].showGridLines = True
    
    # Title Block
    ws1.merge_cells("A1:G1")
    ws1["A1"] = "TOP CONSTRUCT — DOSSIER D'EXPERTISE TECHNIQUE & AUDIT AVP 01"
    ws1["A1"].font = font_title
    ws1["A1"].fill = fill_title
    ws1["A1"].alignment = align_center
    ws1.row_dimensions[1].height = 35
    
    ws1.merge_cells("A2:G2")
    ws1["A2"] = "Construction de 2 Habitations Unifamiliales Jumelées (3 Façades) — Rue Fays, 4420 Saint-Nicolas"
    ws1["A2"].font = font_subtitle
    ws1["A2"].fill = fill_title
    ws1["A2"].alignment = align_center
    ws1.row_dimensions[2].height = 20

    # Project Information Card
    ws1["A4"] = "1. FICHE D'IDENTITÉ DU DOSSIER"
    ws1["A4"].font = font_section
    
    headers_info = ["Paramètre", "Valeur Officielle du Projet", "", "Paramètre Cadastral", "Valeur Cadastrale", "", ""]
    ws1.append([]) # row 5
    
    info_data = [
        ("Maître de l'Ouvrage", "Top Construct SRL", "Parcelles Mères", "Division 3, Section B, n° 1066D5 et 1066C5"),
        ("Auteur de Projet", "Bureau AOS SRL (Rue de Gozée 427, 6110)", "Superficie Totale", "1 012,0 m² (10 ares 12 ca)"),
        ("Localisation", "Rue Fays, 4420 Saint-Nicolas (Liège)", "Front de Rue", "28,77 mètres linéaires"),
        ("Phase Documentaire", "Avant-Projet AVP 01 (Planches 1 à 6)", "Emprise Communale", "39,0 m² à céder à titre gratuit"),
        ("Date d'Émission", "19/08/2026", "Recul Latéral Ouest", "3,12 m (le long parcelle 1066B4)"),
        ("Typologie Bâtie", "2 Maisons jumelées 3 façades", "Recul Latéral Est", "11,65 m (à rue) / 3,56 m (arrière)")
    ]
    
    ws1["A5"] = "Paramètre Général"
    ws1["B5"] = "Valeur Officielle"
    ws1["D5"] = "Paramètre Foncier"
    ws1["E5"] = "Valeur Cadastrale"
    for col in ["A5", "B5", "D5", "E5"]:
        ws1[col].font = font_header
        ws1[col].fill = fill_header
        ws1[col].alignment = align_left
    
    current_row = 6
    for g_lbl, g_val, f_lbl, f_val in info_data:
        ws1.cell(row=current_row, column=1, value=g_lbl).font = font_bold
        ws1.cell(row=current_row, column=2, value=g_val).font = font_data
        ws1.cell(row=current_row, column=4, value=f_lbl).font = font_bold
        ws1.cell(row=current_row, column=5, value=f_val).font = font_data
        ws1.cell(row=current_row, column=1).border = thin_border
        ws1.cell(row=current_row, column=2).border = thin_border
        ws1.cell(row=current_row, column=4).border = thin_border
        ws1.cell(row=current_row, column=5).border = thin_border
        current_row += 1

    # Surface Metrics Card
    current_row += 2
    ws1.cell(row=current_row, column=1, value="2. TABLEAU COMPARATIF DES SURFACES ET RENDEMENT").font = font_section
    current_row += 1
    
    headers_surf = ["Espace / Localisation", "Maison Gauche (m²)", "Maison Droite (m²)", "Moyenne / Total", "Observations Ergonomiques"]
    for c_idx, h in enumerate(headers_surf, start=1):
        cell = ws1.cell(row=current_row, column=c_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = align_center if c_idx in [2, 3, 4] else align_left
        cell.border = thin_border
    
    current_row += 1
    surf_rows = [
        ("Séjour + Cuisine ouverte (RDC)", 31.22, 30.68, "=AVERAGE(B16:C16)", "Gauche: cuisine avant / Droite: îlot 3,70m"),
        ("Buanderie technique (RDC)", 6.00, 6.57, "=AVERAGE(B17:C17)", "Emplacement PAC intérieure, VMC et machines"),
        ("Hall d'entrée & WC invité (RDC)", 5.58, 5.55, "=AVERAGE(B18:C18)", "WC sous escalier marches 7-9 (conflit échappée)"),
        ("Chambre 1 Parentale (Étage)", 13.49, 13.49, "=AVERAGE(B19:C19)", "Lit double + niche dressing (déficit vitré 13,3%)"),
        ("Chambre 2 Enfant/Bureau (Étage)", 9.27, 9.12, "=AVERAGE(B20:C20)", "Écart de 5cm causé par trémie escalier droite"),
        ("Chambre 3 Enfant/Amis (Étage)", 10.42, 10.42, "=AVERAGE(B21:C21)", "Chambre double confortable avec penderie"),
        ("Salle de Douche - SDD (Étage)", 7.20, 7.05, "=AVERAGE(B22:C22)", "Douche italienne + double vasque (écart 5cm)"),
        ("WC Étage & Hall de nuit (Étage)", 4.12, 4.42, "=AVERAGE(B23:C23)", "Porte WC extérieure accidentogène sur marche 14")
    ]
    
    for label, g_val, d_val, f_val, obs in surf_rows:
        ws1.cell(row=current_row, column=1, value=label).font = font_data
        ws1.cell(row=current_row, column=2, value=g_val).font = font_data
        ws1.cell(row=current_row, column=3, value=d_val).font = font_data
        ws1.cell(row=current_row, column=4, value=f_val).font = font_data
        ws1.cell(row=current_row, column=5, value=obs).font = font_data
        
        for c in range(1, 6):
            ws1.cell(row=current_row, column=c).border = thin_border
            if c in [2, 3, 4]:
                ws1.cell(row=current_row, column=c).number_format = '0.00 "m²"'
                ws1.cell(row=current_row, column=c).alignment = align_right
        current_row += 1
        
    # Totals
    ws1.cell(row=current_row, column=1, value="TOTAL SURFACE HABITABLE NETTE (Par Maison)").font = font_total
    ws1.cell(row=current_row, column=2, value="=SUM(B16:B23)").font = font_total
    ws1.cell(row=current_row, column=3, value="=SUM(C16:C23)").font = font_total
    ws1.cell(row=current_row, column=4, value="=AVERAGE(B24:C24)").font = font_total
    ws1.cell(row=current_row, column=5, value="Rendement spatial net/brut exceptionnel de 78,0%").font = font_bold
    for c in range(1, 6):
        ws1.cell(row=current_row, column=c).border = total_border
        ws1.cell(row=current_row, column=c).fill = fill_accent_green
        if c in [2, 3, 4]:
            ws1.cell(row=current_row, column=c).number_format = '0.00 "m²"'
            ws1.cell(row=current_row, column=c).alignment = align_right
            
    current_row += 1
    ws1.cell(row=current_row, column=1, value="Surface Brute Hors-Tout (Dalle 7,00 x 8,00m x 2)").font = font_bold
    ws1.cell(row=current_row, column=2, value=112.0).font = font_bold
    ws1.cell(row=current_row, column=3, value=112.0).font = font_bold
    ws1.cell(row=current_row, column=4, value=224.0).font = font_bold
    ws1.cell(row=current_row, column=5, value="Emprise structure murs/cloisons: 24,7 m² (22,0%)").font = font_data
    for c in range(1, 6):
        ws1.cell(row=current_row, column=c).border = thin_border
        if c in [2, 3, 4]:
            ws1.cell(row=current_row, column=c).number_format = '0.00 "m²"'
            ws1.cell(row=current_row, column=c).alignment = align_right

    current_row += 1
    ws1.cell(row=current_row, column=1, value="Potentiel Combles Aménageables (H ≥ 1,80 m)").font = font_bold
    ws1.cell(row=current_row, column=2, value=21.0).font = font_bold
    ws1.cell(row=current_row, column=3, value=21.0).font = font_bold
    ws1.cell(row=current_row, column=4, value=42.0).font = font_bold
    ws1.cell(row=current_row, column=5, value="Toiture 35° : gain +42 m² (4e/5e chambres)").font = font_bold
    for c in range(1, 6):
        ws1.cell(row=current_row, column=c).border = thin_border
        ws1.cell(row=current_row, column=c).fill = fill_accent_gold
        if c in [2, 3, 4]:
            ws1.cell(row=current_row, column=c).number_format = '0.00 "m²"'
            ws1.cell(row=current_row, column=c).alignment = align_right

    # =========================================================================
    # SHEET 2: MÉTRÉ QUANTITATIF & DÉBOURSÉ SEC (28 LIGNES EXACTES)
    # =========================================================================
    ws2 = wb.create_sheet("02_Métré_Déboursé_Sec")
    ws2.views.sheetView[0].showGridLines = True
    
    ws2.merge_cells("A1:G1")
    ws2["A1"] = "BORDEREAU QUANTITATIF ET ESTIMATIF DÉTAILLÉ (NBN B 06-001)"
    ws2["A1"].font = font_title
    ws2["A1"].fill = fill_title
    ws2["A1"].alignment = align_center
    ws2.row_dimensions[1].height = 30
    
    ws2.merge_cells("A2:G2")
    ws2["A2"] = "Sous-détail du Déboursé Sec Entreprise Générale pour les 2 Maisons Jumelées (224 m² bruts)"
    ws2["A2"].font = font_subtitle
    ws2["A2"].fill = fill_title
    ws2["A2"].alignment = align_center
    ws2.row_dimensions[2].height = 20
    
    headers_boq = ["Code Poste", "Désignation des Travaux BTP", "Quantité", "Unité", "Prix Unit. HTVA (€)", "Montant Total HTVA (€)", "Remarques & Ratios"]
    ws2.append([]) # row 3
    for c_idx, h in enumerate(headers_boq, start=1):
        cell = ws2.cell(row=4, column=c_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = align_center if c_idx in [1, 3, 4] else (align_right if c_idx in [5, 6] else align_left)
        cell.border = thin_border
    ws2.row_dimensions[4].height = 25
    
    boq_items = [
        # Lot 00
        ("LOT 00", "TERRASSEMENTS & FONDATIONS SPÉCIALES", "", "", "", "", "SOUS-TOTAL LOT 00"),
        ("00.01", "Installation de chantier, balisage sécuritaire & clôtures", 1.0, "fft", 3500.0, "=C6*E6", "Balisage voirie Rue Fays"),
        ("00.02", "Décapage de la terre végétale sur ép. 30 cm en dépôt", 48.0, "m³", 12.0, "=C7*E7", "Stockage fond de parcelle pour régalage"),
        ("00.03", "Terrassement en déblai de masse & évacuation décharge", 136.0, "m³", 28.0, "=C8*E8", "~175 m³ foisonnés (11 camions)"),
        ("00.04", "Empierrement drainant compacté sous radier type 0/32", 60.0, "t", 32.0, "=C9*E9", "Epaisseur 20 cm compactée"),
        ("00.05", "Béton armé C30/37 coulé pompé pour radier ép. 25 cm", 28.0, "m³", 185.0, "=C10*E10", "4 toupies + pompe à béton"),
        ("00.06", "Aciers FeB 500 treillis soudés double nappe (80 kg/m³)", 2240.0, "kg", 1.85, "=C11*E11", "Armature anti-tassement différentiel"),
        
        # Lot 01
        ("LOT 01", "ÉLÉVATION, MAÇONNERIES & STRUCTURE", "", "", "", "", "SOUS-TOTAL LOT 01"),
        ("01.01", "Blocs d'assise thermique isolante Foamglas / Kimblok", 44.0, "m", 42.0, "=C13*E13", "Rupture thermique en pied de mur"),
        ("01.02", "Maçonnerie de blocs béton lourds 14 cm porteurs", 145.0, "m²", 65.0, "=C14*E14", "Murs intérieurs et mitoyen"),
        ("01.03", "Hourdis précontraints béton armé 13+4 cm de chape", 112.0, "m²", 78.0, "=C15*E15", "Portée libre séjour 4,30 m"),
        ("01.04", "Briques de parement ton clair pose à joints fins", 204.0, "m²", 125.0, "=C16*E16", "Déduction faite des 35 m² de baies"),
        ("01.05", "Isolant mural polyuréthane PIR rainuré 14 cm (λ=0,022)", 204.0, "m²", 45.0, "=C17*E17", "R = 6,36 m²·K/W"),

        # Lot 02
        ("LOT 02", "CHARPENTE, COUVERTURE & TOITURE 35°", "", "", "", "", "SOUS-TOTAL LOT 02"),
        ("02.01", "Charpente traditionnelle en sapin du nord traitée 35°", 145.0, "m²", 85.0, "=C19*E19", "Préservation volume combles (exclure fermettes)"),
        ("02.02", "Sous-toiture étanche HPV, contre-lattes & pare-vapeur", 145.0, "m²", 18.0, "=C20*E20", "Étanchéité à l'air continue"),
        ("02.03", "Tuiles plates en terre cuite anthracite & faîtières", 145.0, "m²", 68.0, "=C21*E21", "Esthétique contemporaine"),
        ("02.04", "Solin zinc/plomb engravé mécanique sur décrochement 20cm", 8.0, "m", 95.0, "=C22*E22", "Étanchéité critique décrochement toiture"),
        ("02.05", "Gouttières zinc 1/2 rondes & descentes d'eaux pluviales", 36.0, "m", 45.0, "=C23*E23", "Raccordement citerne EP"),

        # Lot 03
        ("LOT 03", "MENUISERIES EXTÉRIEURES & SEUILS", "", "", "", "", "SOUS-TOTAL LOT 03"),
        ("03.01", "Châssis PVC/Alu RAL 7016 DV HR 1.0 (Ensemble 2 maisons)", 1.0, "fft", 38000.0, "=C25*E25", "Baies coulissantes, OB-F, OB-O"),
        ("03.02", "Seuils pierre bleue belge avec rupture thermique EPDM", 22.0, "m", 110.0, "=C26*E26", "Talon isolant pour seuils baies"),

        # Lot 04
        ("LOT 04", "ISOLATIONS DU BÂTIMENT", "", "", "", "", "SOUS-TOTAL LOT 04"),
        ("04.01", "Polyuréthane PUR projeté sol ép. 12 cm poncé", 112.0, "m²", 32.0, "=C28*E28", "U = 0,206 W/m²·K"),
        ("04.02", "Isolation toiture laine minérale 22 cm + membrane PV", 145.0, "m²", 38.0, "=C29*E29", "U = 0,154 W/m²·K"),

        # Lot 05
        ("LOT 05", "TECHNIQUES SPÉCIALES (HVAC, ÉLEC, PV)", "", "", "", "", "SOUS-TOTAL LOT 05"),
        ("05.01", "Pompe à Chaleur air/eau 6 kW avec ECS intégrée (x2)", 2.0, "fft", 14500.0, "=C31*E31", "Label A+++ écologique"),
        ("05.02", "Chauffage par le sol basse température RDC + Étage", 224.0, "m²", 55.0, "=C32*E32", "Confort radiant optimal"),
        ("05.03", "VMC Double Flux Système D avec récupérateur >85% (x2)", 2.0, "fft", 7800.0, "=C33*E33", "230 m³/h pulsion / 225 m³/h extraction"),
        ("05.04", "Sanitaires complets (4 WC suspendus, 2 SDD, meubles)", 1.0, "fft", 19500.0, "=C34*E34", "Tubes insonorisés Silent-PP"),
        ("05.05", "Électricité conforme RGIE + pré-équipement borne EV (x2)", 1.0, "fft", 22000.0, "=C35*E35", "Triphasé 400V+N 40A"),
        ("05.06", "Photovoltaïque 2 x 6,02 kWc (28 panneaux 430 Wc)", 1.0, "fft", 16000.0, "=C36*E36", "Production ~5 720 kWh/an/lot"),

        # Lot 06
        ("LOT 06", "PARACHÈVEMENTS INTÉRIEURS", "", "", "", "", "SOUS-TOTAL LOT 06"),
        ("06.01", "Plafonnage plâtre projeté lissé sur murs et plafonds", 420.0, "m²", 22.0, "=C38*E38", "Finition prêt à peindre"),
        ("06.02", "Chapes ciment lissées traditionnelles ép. 8 cm", 224.0, "m²", 24.0, "=C39*E39", "Enrobage plancher chauffant"),
        ("06.03", "Carrelage grès cérame 60x60 cm collé + plinthes", 224.0, "m²", 65.0, "=C40*E40", "RDC et pièces d'eau"),
        ("06.04", "Blocs-portes intérieurs prépeints réversibles (12 pcs)", 12.0, "pce", 320.0, "=C41*E41", "Recommandation: 83cm au RDC"),
        ("06.05", "Escaliers béton habillage bois massif + garde-corps (x2)", 2.0, "pce", 4200.0, "=C42*E42", "14 marches Blondel conforme"),

        # Lot 07
        ("LOT 07", "ASSAINISSEMENT, VRD & RACCORDEMENTS", "", "", "", "", "SOUS-TOTAL LOT 07"),
        ("07.01", "Citernes eau de pluie béton 7 500 L + filtre à panier (x2)", 2.0, "pce", 3200.0, "=C44*E44", "Capacité totale 15 000 L"),
        ("07.02", "Groupe hydrophore automatique à vitesse variable (x2)", 2.0, "pce", 1400.0, "=C45*E45", "Alimentation 4 WC + LL"),
        ("07.03", "Massif d'infiltration alvéolaire eaux pluviales (8,5 m³)", 1.0, "fft", 4200.0, "=C46*E46", "Rétention d'orage Code de l'Eau"),
        ("07.04", "Raccordements impétrants voirie (CILE, ORES, AIDE, VOO)", 1.0, "fft", 18000.0, "=C47*E47", "Raccordement réseau public Rue Fays")
    ]
    
    current_row = 5
    lot_header_rows = []
    
    for item in boq_items:
        code, desig, qty, unit, pu, total_formula, rem = item
        is_lot_header = code.startswith("LOT")
        
        ws2.cell(row=current_row, column=1, value=code)
        ws2.cell(row=current_row, column=2, value=desig)
        ws2.cell(row=current_row, column=3, value=qty if qty != "" else None)
        ws2.cell(row=current_row, column=4, value=unit if unit != "" else None)
        ws2.cell(row=current_row, column=5, value=pu if pu != "" else None)
        ws2.cell(row=current_row, column=6, value=total_formula if total_formula != "" else None)
        ws2.cell(row=current_row, column=7, value=rem)
        
        if is_lot_header:
            lot_header_rows.append(current_row)
            for c in range(1, 8):
                cell = ws2.cell(row=current_row, column=c)
                cell.font = font_sub_header
                cell.fill = fill_sub_header
                cell.border = thin_border
            ws2.row_dimensions[current_row].height = 22
        else:
            for c in range(1, 8):
                cell = ws2.cell(row=current_row, column=c)
                cell.font = font_data
                cell.border = thin_border
                if c in [1, 4]:
                    cell.alignment = align_center
                elif c == 3:
                    cell.alignment = align_right
                    cell.number_format = '#,##0.00'
                elif c in [5, 6]:
                    cell.alignment = align_right
                    cell.number_format = '#,##0.00 €'
            ws2.row_dimensions[current_row].height = 19
            
        current_row += 1
        
    # Grand Total BOQ
    current_row += 1
    ws2.cell(row=current_row, column=1, value="TOTAL DÉBOURSÉ SEC TRAVAUX (2 HABITATIONS)").font = font_total
    ws2.cell(row=current_row, column=6, value="=SUM(F6:F11)+SUM(F13:F17)+SUM(F19:F23)+SUM(F25:F26)+SUM(F28:F29)+SUM(F31:F36)+SUM(F38:F42)+SUM(F44:F47)").font = font_total
    ws2.cell(row=current_row, column=7, value="Somme arithmétique exacte des 28 postes").font = font_bold
    for c in range(1, 8):
        ws2.cell(row=current_row, column=c).border = total_border
        ws2.cell(row=current_row, column=c).fill = fill_accent_green
    ws2.cell(row=current_row, column=6).number_format = '#,##0.00 €'
    ws2.cell(row=current_row, column=6).alignment = align_right
    ws2.row_dimensions[current_row].height = 24
    
    current_row += 1
    ws2.cell(row=current_row, column=1, value="Frais Généraux Entreprise (10%)").font = font_bold
    ws2.cell(row=current_row, column=6, value=f"=F{current_row-1}*0.1").font = font_bold
    ws2.cell(row=current_row, column=6).number_format = '#,##0.00 €'
    ws2.cell(row=current_row, column=6).alignment = align_right
    
    current_row += 1
    ws2.cell(row=current_row, column=1, value="Marge Bénéficiaire Entreprise & Aléas Chantier (10%)").font = font_bold
    ws2.cell(row=current_row, column=6, value=f"=(F{current_row-2}+F{current_row-1})*0.1").font = font_bold
    ws2.cell(row=current_row, column=6).number_format = '#,##0.00 €'
    ws2.cell(row=current_row, column=6).alignment = align_right

    current_row += 1
    ws2.cell(row=current_row, column=1, value="PRIX DE CONSTRUCTION SOUMISSION ENTREPRISE GÉNÉRALE").font = font_title
    ws2.cell(row=current_row, column=6, value=f"=F{current_row-3}+F{current_row-2}+F{current_row-1}").font = font_title
    ws2.cell(row=current_row, column=7, value="Soit ~1 824 € HTVA / m² brut bâti").font = font_bold
    for c in range(1, 8):
        ws2.cell(row=current_row, column=c).fill = fill_title
        ws2.cell(row=current_row, column=c).font = font_title
    ws2.cell(row=current_row, column=6).number_format = '#,##0.00 €'
    ws2.cell(row=current_row, column=6).alignment = align_right
    ws2.row_dimensions[current_row].height = 28

    # =========================================================================
    # SHEET 3: BILAN FINANCIER PROMOTEUR & SCÉNARIOS ROI
    # =========================================================================
    ws3 = wb.create_sheet("03_Bilan_Promoteur_ROI")
    ws3.views.sheetView[0].showGridLines = True
    
    ws3.merge_cells("A1:F1")
    ws3["A1"] = "BILAN FINANCIER OPÉRATIONNEL & RENTABILITÉ PROMOTEUR"
    ws3["A1"].font = font_title
    ws3["A1"].fill = fill_title
    ws3["A1"].alignment = align_center
    ws3.row_dimensions[1].height = 30
    
    ws3.merge_cells("A2:F2")
    ws3["A2"] = "Compte de résultat prévisionnel d'opération immobilière pour Top Construct (2 Maisons neuves)"
    ws3["A2"].font = font_subtitle
    ws3["A2"].fill = fill_title
    ws3["A2"].alignment = align_center
    ws3.row_dimensions[2].height = 20
    
    headers_fin = ["Poste Budgétaire", "Détail du Calcul / Base", "Montant Lot 1 (€)", "Montant Lot 2 (€)", "Total Projet HTVA (€)", "% du Coût Total"]
    ws3.append([]) # row 3
    for c_idx, h in enumerate(headers_fin, start=1):
        cell = ws3.cell(row=4, column=c_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = align_center if c_idx in [3, 4, 5, 6] else align_left
        cell.border = thin_border
    ws3.row_dimensions[4].height = 25
    
    fin_items = [
        ("Acquisition Foncier (Terrain 1 012 m²)", "Achat parcelles 1066D5 & 1066C5", 55000.0, 55000.0, 110000.0, "=E5/$E$11"),
        ("Droits d'Enregistrement (12,5% Wallonie)", "12,5% appliqué sur le foncier", 6875.0, 6875.0, 13750.0, "=E6/$E$11"),
        ("Frais d'Acte, Notaire & Division AGDP", "Plan de division et PV de bornage", 3125.0, 3125.0, 6250.0, "=E7/$E$11"),
        ("Travaux de Construction Entreprise Générale", "Devis complet (gros-œuvre + techniques)", "=E8/2", "=E8/2", "=Métré_Déboursé_Sec!F52", "=E8/$E$11"),
        ("Honoraires Conception & Contrôles", "Architecte AOS, Stabilité, PEB, CSS", 13000.0, 13000.0, 26000.0, "=E9/$E$11"),
        ("Frais Financiers, Assurances & Imprévus", "Intercalaires, assurance décennale", 12666.5, 12666.5, 25333.0, "=E10/$E$11")
    ]
    
    current_row = 5
    for poste, base, lot1, lot2, total, pct in fin_items:
        ws3.cell(row=current_row, column=1, value=poste).font = font_bold
        ws3.cell(row=current_row, column=2, value=base).font = font_data
        ws3.cell(row=current_row, column=3, value=lot1).font = font_data
        ws3.cell(row=current_row, column=4, value=lot2).font = font_data
        ws3.cell(row=current_row, column=5, value=total).font = font_bold
        ws3.cell(row=current_row, column=6, value=pct).font = font_data
        
        for c in range(1, 7):
            cell = ws3.cell(row=current_row, column=c)
            cell.border = thin_border
            if c in [3, 4, 5]:
                cell.number_format = '#,##0.00 €'
                cell.alignment = align_right
            elif c == 6:
                cell.number_format = '0.0 %'
                cell.alignment = align_right
        current_row += 1
        
    # Total Cost
    ws3.cell(row=current_row, column=1, value="COÛT DE REVIENT TOTAL DE L'OPÉRATION").font = font_total
    ws3.cell(row=current_row, column=2, value="Somme tous frais confondus").font = font_total
    ws3.cell(row=current_row, column=3, value="=SUM(C5:C10)").font = font_total
    ws3.cell(row=current_row, column=4, value="=SUM(D5:D10)").font = font_total
    ws3.cell(row=current_row, column=5, value="=SUM(E5:E10)").font = font_total
    ws3.cell(row=current_row, column=6, value="=SUM(F5:F10)").font = font_total
    for c in range(1, 7):
        ws3.cell(row=current_row, column=c).border = total_border
        ws3.cell(row=current_row, column=c).fill = fill_total
        if c in [3, 4, 5]:
            ws3.cell(row=current_row, column=c).number_format = '#,##0.00 €'
            ws3.cell(row=current_row, column=c).alignment = align_right
        elif c == 6:
            ws3.cell(row=current_row, column=c).number_format = '0.0 %'
            ws3.cell(row=current_row, column=c).alignment = align_right
    ws3.row_dimensions[current_row].height = 24
    
    current_row += 2
    ws3.cell(row=current_row, column=1, value="CHIFFRE D'AFFAIRES & MARGE OPÉRATIONNELLE (SCÉNARIO 1 : AS-IS)").font = font_section
    current_row += 1
    
    ws3.cell(row=current_row, column=1, value="Prix de Revente Prévisionnel (2 Maisons neuves)").font = font_bold
    ws3.cell(row=current_row, column=2, value="365 000 € HTVA par maison neuve 3 façades").font = font_data
    ws3.cell(row=current_row, column=3, value=365000.0).font = font_bold
    ws3.cell(row=current_row, column=4, value=365000.0).font = font_bold
    ws3.cell(row=current_row, column=5, value="=C14+D14").font = font_bold
    for c in range(1, 6):
        ws3.cell(row=current_row, column=c).border = thin_border
        if c in [3, 4, 5]:
            ws3.cell(row=current_row, column=c).number_format = '#,##0.00 €'
            ws3.cell(row=current_row, column=c).alignment = align_right
            
    current_row += 1
    ws3.cell(row=current_row, column=1, value="MARGE BRUTE OPÉRATIONNELLE PROMOTEUR").font = font_title
    ws3.cell(row=current_row, column=2, value="Chiffre d'Affaires - Coût de Revient Total").font = font_title
    ws3.cell(row=current_row, column=3, value="=C14-C11").font = font_title
    ws3.cell(row=current_row, column=4, value="=D14-D11").font = font_title
    ws3.cell(row=current_row, column=5, value="=E14-E11").font = font_title
    ws3.cell(row=current_row, column=6, value="=E15/E14").font = font_title
    for c in range(1, 7):
        ws3.cell(row=current_row, column=c).fill = fill_accent_green
        ws3.cell(row=current_row, column=c).font = font_title
        ws3.cell(row=current_row, column=c).border = total_border
        if c in [3, 4, 5]:
            ws3.cell(row=current_row, column=c).number_format = '#,##0.00 €'
            ws3.cell(row=current_row, column=c).alignment = align_right
        elif c == 6:
            ws3.cell(row=current_row, column=c).number_format = '0.0 % (Marge)'
            ws3.cell(row=current_row, column=c).alignment = align_right
    ws3.row_dimensions[current_row].height = 28
    
    # Scenarios Table
    current_row += 3
    ws3.cell(row=current_row, column=1, value="TABLEAU COMPARATIF DES 3 SCÉNARIOS DE VALORISATION").font = font_section
    current_row += 1
    
    headers_scen = ["Scénario Stratégique", "Description du Produit Commercialisé", "Surcoût Travaux (€)", "CA Total HTVA (€)", "Marge Brute (€)", "Marge Nette (%)"]
    for c_idx, h in enumerate(headers_scen, start=1):
        cell = ws3.cell(row=current_row, column=c_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = align_center if c_idx >= 3 else align_left
        cell.border = thin_border
    current_row += 1
    
    scenarios = [
        ("Scénario 1 : Économique Standard", "Maison 3 façades 3 chambres (112 m² bruts) As-Is", 0.0, 730000.0, 140000.0, 0.1918),
        ("Scénario 2 : Premium Évolutif (+42 m²)", "Maison 4-5 ch avec combles aménagés (133 m² habitables)", 17000.0, 810000.0, 203000.0, 0.2506),
        ("Scénario 3 : Optimisation Foncière Est", "Valorisation dent creuse 11,65 m (garage double ou 3e lot)", 35000.0, 960000.0, 265000.0, 0.2760)
    ]
    for s_nom, s_desc, s_cout, s_ca, s_marge, s_pct in scenarios:
        ws3.cell(row=current_row, column=1, value=s_nom).font = font_bold
        ws3.cell(row=current_row, column=2, value=s_desc).font = font_data
        ws3.cell(row=current_row, column=3, value=s_cout).font = font_data
        ws3.cell(row=current_row, column=4, value=s_ca).font = font_bold
        ws3.cell(row=current_row, column=5, value=s_marge).font = font_bold
        ws3.cell(row=current_row, column=6, value=s_pct).font = font_bold
        
        for c in range(1, 7):
            cell = ws3.cell(row=current_row, column=c)
            cell.border = thin_border
            if c in [3, 4, 5]:
                cell.number_format = '#,##0.00 €'
                cell.alignment = align_right
            elif c == 6:
                cell.number_format = '0.0 %'
                cell.alignment = align_right
        current_row += 1

    # =========================================================================
    # SHEET 4: THERMIQUE PEB & VENTILATION
    # =========================================================================
    ws4 = wb.create_sheet("04_Thermique_&_Ventilation")
    ws4.views.sheetView[0].showGridLines = True
    
    ws4.merge_cells("A1:F1")
    ws4["A1"] = "BILAN THERMIQUE PEB (LABEL Q-ZEN) & DIMENSIONNEMENT AÉRAULIQUE"
    ws4["A1"].font = font_title
    ws4["A1"].fill = fill_title
    ws4["A1"].alignment = align_center
    ws4.row_dimensions[1].height = 30
    
    ws4["A3"] = "1. COEFFICIENTS DE TRANSMISSION THERMIQUE (VALEURS U) COUCHE PAR COUCHE"
    ws4["A3"].font = font_section
    
    headers_u = ["Paroi de Déperdition", "Composition Analytique des Couches", "Épaisseur (m)", "Lambda λ (W/m·K)", "Résistance R (m²·K/W)", "Coefficient U (W/m²·K)"]
    ws4.append([]) # row 4
    for c_idx, h in enumerate(headers_u, start=1):
        cell = ws4.cell(row=5, column=c_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = align_center if c_idx in [3, 4, 5, 6] else align_left
        cell.border = thin_border
        
    u_items = [
        ("Mur Extérieur (38 cm)", "Brique de parement terre cuite", 0.09, 1.15, 0.078, ""),
        ("", "Lame d'air fortement ventilée", 0.03, 0.00, 0.160, ""),
        ("", "Isolant polyuréthane PIR rainuré", 0.14, 0.022, 6.364, ""),
        ("", "Blocs de béton lourds porteurs", 0.14, 1.30, 0.108, ""),
        ("", "Plafonnage intérieur plâtre", 0.015, 0.52, 0.029, ""),
        ("TOTAL MUR EXTÉRIEUR", "Avec résistances Rsi (0,13) + Rse (0,04)", 0.38, "-", 6.909, 0.143),
        
        ("Toiture Inclinée 35°", "Laine minérale semi-rigide sous chevrons", 0.22, 0.035, 6.286, ""),
        ("", "Pare-vapeur étanche à l'air + Gyproc", 0.0125, 0.25, 0.050, ""),
        ("TOTAL TOITURE 35°", "Avec résistances Rsi (0,10) + Rse (0,04)", 0.25, "-", 6.476, 0.154),
        
        ("Plancher sur Sol (Radier)", "Polyuréthane PUR projeté sous chape", 0.12, 0.026, 4.615, ""),
        ("", "Chape ciment lissée traditionnelle", 0.08, 1.30, 0.062, ""),
        ("TOTAL PLANCHER SOL", "Avec résistance superficielle Rsi (0,17)", 0.20, "-", 4.847, 0.206),
        
        ("Châssis & Vitrages HR", "Profilés PVC 6 chambres + DV HR 1.0", "-", "-", "-", 1.200)
    ]
    
    current_row = 6
    for paroi, comp, ep, lam, r_val, u_val in u_items:
        is_total = paroi.startswith("TOTAL") or paroi.startswith("Châssis")
        ws4.cell(row=current_row, column=1, value=paroi).font = font_bold if paroi != "" else font_data
        ws4.cell(row=current_row, column=2, value=comp).font = font_bold if is_total else font_data
        ws4.cell(row=current_row, column=3, value=ep if ep != "-" else "-").font = font_data
        ws4.cell(row=current_row, column=4, value=lam if lam != "-" and lam != 0.0 else "-").font = font_data
        ws4.cell(row=current_row, column=5, value=r_val if r_val != "-" else "-").font = font_bold if is_total else font_data
        ws4.cell(row=current_row, column=6, value=u_val if u_val != "" else "").font = font_title if is_total else font_data
        
        for c in range(1, 7):
            cell = ws4.cell(row=current_row, column=c)
            cell.border = thin_border
            if is_total:
                cell.fill = fill_sub_header
            if c in [3, 4, 5]:
                if isinstance(cell.value, (int, float)):
                    cell.number_format = '0.000'
                cell.alignment = align_right
            elif c == 6:
                if isinstance(cell.value, (int, float)):
                    cell.number_format = '0.000 "W/m²·K"'
                    cell.alignment = align_right
        current_row += 1
        
    # Ventilation Table
    current_row += 2
    ws4.cell(row=current_row, column=1, value="2. DIMENSIONNEMENT DU SYSTÈME DE VENTILATION DOUBLE FLUX (SYSTÈME D)").font = font_section
    current_row += 1
    
    headers_vent = ["Local / Pièce", "Type de Flux Aéraulique", "Règle Réglementaire AGW", "Débit Requis Maison 1 (m³/h)", "Débit Requis Maison 2 (m³/h)", "Statut PEB"]
    for c_idx, h in enumerate(headers_vent, start=1):
        cell = ws4.cell(row=current_row, column=c_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = align_center if c_idx in [2, 4, 5, 6] else align_left
        cell.border = thin_border
    current_row += 1
    
    vent_items = [
        ("Séjour + Cuisine ouverte", "Pulsion d'air neuf", "3,6 m³/h par m² (max 150)", 112.0, 112.0, "Conforme"),
        ("Chambre 1 Parentale", "Pulsion d'air neuf", "3,6 m³/h par m² (min 25)", 48.0, 48.0, "Conforme"),
        ("Chambre 2 Enfant", "Pulsion d'air neuf", "3,6 m³/h par m²", 33.0, 33.0, "Conforme"),
        ("Chambre 3 Enfant", "Pulsion d'air neuf", "3,6 m³/h par m²", 37.0, 37.0, "Conforme"),
        ("TOTAL PULSION D'AIR NEUF", "ENTRÉE D'AIR GLOBAL", "Total requis par groupe", 230.0, 230.0, "ÉQUILIBRÉ"),
        ("Cuisine (Zone cuisson)", "Extraction d'air vicié", "Débit fixe obligatoire", 75.0, 75.0, "Conforme"),
        ("Salle de Douche (S.D.D.)", "Extraction d'air vicié", "Débit fixe obligatoire", 50.0, 50.0, "Conforme"),
        ("Buanderie technique", "Extraction d'air vicié", "Débit fixe obligatoire", 50.0, 50.0, "Conforme"),
        ("WC Rez-de-chaussée", "Extraction d'air vicié", "25 m³/h par local", 25.0, 25.0, "Conforme"),
        ("WC Étage", "Extraction d'air vicié", "25 m³/h par local", 25.0, 25.0, "Conforme"),
        ("TOTAL EXTRACTION D'AIR VICIÉ", "SORTIE D'AIR GLOBAL", "Total extrait par groupe", 225.0, 225.0, "ÉQUILIBRÉ")
    ]
    
    for local, flux, regle, deb1, deb2, statut in vent_items:
        is_tot = local.startswith("TOTAL")
        ws4.cell(row=current_row, column=1, value=local).font = font_bold if is_tot else font_data
        ws4.cell(row=current_row, column=2, value=flux).font = font_data
        ws4.cell(row=current_row, column=3, value=regle).font = font_data
        ws4.cell(row=current_row, column=4, value=deb1).font = font_bold if is_tot else font_data
        ws4.cell(row=current_row, column=5, value=deb2).font = font_bold if is_tot else font_data
        ws4.cell(row=current_row, column=6, value=statut).font = font_bold
        
        for c in range(1, 7):
            cell = ws4.cell(row=current_row, column=c)
            cell.border = thin_border
            if is_tot:
                cell.fill = fill_accent_green if "PULSION" in local else fill_accent_gold
            if c in [4, 5]:
                cell.number_format = '#,##0 "m³/h"'
                cell.alignment = align_right
            elif c in [2, 6]:
                cell.alignment = align_center
        current_row += 1

    # =========================================================================
    # SHEET 5: CHECKLIST DE PERMIS CODT
    # =========================================================================
    ws5 = wb.create_sheet("05_Checklist_Permis_CoDT")
    ws5.views.sheetView[0].showGridLines = True
    
    ws5.merge_cells("A1:F1")
    ws5["A1"] = "MATRICE D'ARBITRAGE TECHNIQUE & CHECKLIST DE DÉPÔT CODT"
    ws5["A1"].font = font_title
    ws5["A1"].fill = fill_title
    ws5["A1"].alignment = align_center
    ws5.row_dimensions[1].height = 30
    
    headers_check = ["Priorité", "Objet de la Non-Conformité", "Risque Chantier / Permis", "Action Corrective Immédiate", "Responsable", "Statut Audit"]
    ws5.append([]) # row 2
    for c_idx, h in enumerate(headers_check, start=1):
        cell = ws5.cell(row=3, column=c_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = align_center if c_idx in [1, 5, 6] else align_left
        cell.border = thin_border
        
    check_items = [
        ("P1", "Absence de Flèche Nord", "Irrecevabilité administrative immédiate du CoDT", "Dessiner la rose des vents sur le plan d'implantation", "Bureau AOS SRL", "Bloquant"),
        ("P1", "Annexe Droite Fantôme", "Contradiction entre façades (+161.95m) et plan RDC", "Dessiner et coter l'annexe au RDC ou la supprimer des façades", "Bureau AOS SRL", "Bloquant"),
        ("P1", "Division Cadastrale AGDP", "Mitoyenneté non alignée sur frontière 1066D5/1066C5", "Faire dresser le plan de division par géomètre-expert", "Géomètre-Expert", "Bloquant"),
        ("P1", "Évacuation Îlot Central (3,70 m)", "Tuyau Ø75 mm inlogeable dans chape de 8 cm", "Intégrer les attentes d'égouttage directement dans le radier", "Ingénieur Stabilité", "Bloquant"),
        ("P2", "Solin Décrochement Toiture 20 cm", "Infiltration d'eau pluviale sur 8 m de rampant", "Prescrire solin zinc/plomb engravé avec membrane EPDM soudée", "Couvreur", "À intégrer"),
        ("P2", "Pignon Droit Encaissé (-60 cm)", "Humidité latérale issue du terrain mitoyen (+159.60m)", "Cimentage hydrofuge d'assise + nappe Delta-MS + drain agricole", "Terrassier", "À intégrer"),
        ("P2", "Bande Coupe-Feu Toiture EI 60", "Non-conformité aux normes pompiers Zone IILE", "Reporter sur le plan la bande sous-toiture incombustible 1,00 m", "Bureau AOS SRL", "À intégrer"),
        ("P3", "Échappée de Tête WC RDC", "Hauteur < 1,60 m sous paillasse escalier marches 7-9", "Permuter cuvette et lave-mains pour dégager hauteur ≥ 2,00 m", "Bureau AOS SRL", "Recommandé"),
        ("P3", "Conflit Porte WC Étage", "Porte battante percute les usagers sur la marche 14", "Remplacer par une porte à galandage escamotable dans cloison", "Bureau AOS SRL", "Recommandé"),
        ("P3", "Salubrité Chambre 1 (13,3%)", "Déficit par rapport au ratio légal du 1/6e (16,7%)", "Rehausser la baie pignon à 1,80 x 1,20 m pour atteindre 16,0%", "Bureau AOS SRL", "Recommandé")
    ]
    
    current_row = 4
    for prio, objet, risque, action, resp, statut in check_items:
        ws5.cell(row=current_row, column=1, value=prio).font = font_bold
        ws5.cell(row=current_row, column=2, value=objet).font = font_bold
        ws5.cell(row=current_row, column=3, value=risque).font = font_data
        ws5.cell(row=current_row, column=4, value=action).font = font_data
        ws5.cell(row=current_row, column=5, value=resp).font = font_data
        ws5.cell(row=current_row, column=6, value=statut).font = font_bold
        
        for c in range(1, 7):
            cell = ws5.cell(row=current_row, column=c)
            cell.border = thin_border
            if c == 1:
                cell.alignment = align_center
                if prio == "P1":
                    cell.fill = fill_accent_gold
                elif prio == "P2":
                    cell.fill = fill_sub_header
            elif c in [5, 6]:
                cell.alignment = align_center
                if statut == "Bloquant":
                    cell.fill = PatternFill(start_color="FED7D7", end_color="FED7D7", fill_type="solid")
                    cell.font = Font(name="Calibri", size=10, bold=True, color=RED_ACCENT)
        current_row += 1

    # Auto-adjust column widths across all sheets
    for ws in wb.worksheets:
        for col in ws.columns:
            max_len = 0
            col_letter = get_column_letter(col[0].column)
            for cell in col:
                # skip merged title rows
                if cell.row in [1, 2]:
                    continue
                val_str = str(cell.value or "")
                if len(val_str) > max_len:
                    max_len = len(val_str)
            ws.column_dimensions[col_letter].width = max(max_len + 3, 12)
            
    # Specific targeted manual column widths for aesthetics
    ws1.column_dimensions["A"].width = 38
    ws1.column_dimensions["B"].width = 24
    ws1.column_dimensions["C"].width = 22
    ws1.column_dimensions["D"].width = 24
    ws1.column_dimensions["E"].width = 45
    
    ws2.column_dimensions["A"].width = 14
    ws2.column_dimensions["B"].width = 52
    ws2.column_dimensions["C"].width = 14
    ws2.column_dimensions["D"].width = 10
    ws2.column_dimensions["E"].width = 20
    ws2.column_dimensions["F"].width = 24
    ws2.column_dimensions["G"].width = 42

    ws3.column_dimensions["A"].width = 42
    ws3.column_dimensions["B"].width = 45
    ws3.column_dimensions["C"].width = 20
    ws3.column_dimensions["D"].width = 20
    ws3.column_dimensions["E"].width = 24
    ws3.column_dimensions["F"].width = 18

    ws4.column_dimensions["A"].width = 30
    ws4.column_dimensions["B"].width = 45
    ws4.column_dimensions["C"].width = 15
    ws4.column_dimensions["D"].width = 18
    ws4.column_dimensions["E"].width = 22
    ws4.column_dimensions["F"].width = 22

    ws5.column_dimensions["A"].width = 12
    ws5.column_dimensions["B"].width = 32
    ws5.column_dimensions["C"].width = 45
    ws5.column_dimensions["D"].width = 55
    ws5.column_dimensions["E"].width = 20
    ws5.column_dimensions["F"].width = 16

    output_path = str(Path(__file__).resolve().parent / "DEVIS_ET_METRE_TOP_CONSTRUCT_ST_NICOLAS_AVP01.xlsx")
    wb.save(output_path)
    print(f"Workbook successfully saved at: {output_path}")

if __name__ == "__main__":
    build_workbook()
