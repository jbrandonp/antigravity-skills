"""
Script universel pour insérer de nouvelles affaires ou devis dans le classeur Excel protégé.
Préserve l'intégrité des formules, le zonage des protections et le formatage par secteur.
Strictement typé, zéro 'Any'.
"""

import argparse
import os
import sys
from datetime import date, datetime
from typing import Dict, Final, List, Optional, Tuple
import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Protection, Side

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

FONT_FAMILY: Final[str] = "Calibri"
COLOR_BORDER: Final[str] = "D9D9D9"

SECTOR_DELAYS: Final[Dict[str, Tuple[str, int]]] = {
    "btp": ("DEV", 14),
    "services": ("PROP", 7),
    "maintenance": ("OR", 3),
    "healthcare": ("SOIN", 5),
    "retail": ("CMD", 5),
    "general": ("AFF", 7),
}


def append_deal_to_workbook(
    excel_path: str,
    nom_client: str,
    montant_htva: float,
    objet_prestation: str,
    telephone: str = "",
    date_emission: Optional[date] = None,
    statut_initial: str = "En attente",
    commentaires: str = "",
    sector: str = "general",
    delay_days: Optional[int] = None,
    password: str = "OFFICE2026",
) -> Tuple[int, str]:
    """
    Insère une nouvelle affaire ou devis dans la feuille Excel tout en respectant
    les cellules déverrouillées et la formule d'alerte verrouillée.
    """
    if not os.path.isfile(excel_path):
        raise FileNotFoundError(f"Le fichier Excel cible est introuvable : {excel_path}")

    if montant_htva <= 0:
        raise ValueError("Le montant doit être un nombre strictement positif.")

    if not nom_client.strip():
        raise ValueError("Le nom du client ne peut pas être vide.")

    sec = sector.lower().strip()
    prefix_id, default_delay = SECTOR_DELAYS.get(sec, ("AFF", 7))
    actual_delay = delay_days if delay_days is not None else default_delay
    emission = date_emission if date_emission is not None else date.today()

    wb = openpyxl.load_workbook(excel_path)
    # Chercher la feuille principale de suivi
    sheet_name = "Suivi des Devis" if "Suivi des Devis" in wb.sheetnames else wb.sheetnames[0]
    ws = wb[sheet_name]

    # Trouver la première ligne libre et analyser le dernier ID
    target_row = 5
    dernier_numero_int = 0

    for r in range(5, ws.max_row + 2):
        val = ws.cell(row=r, column=1).value
        val_str = str(val or "").strip()
        if not val or val_str.startswith("AVERTISSEMENT") or val_str.startswith("Avertissement"):
            target_row = r
            break

        # Extraction du numéro incrémental
        if "-" in val_str:
            parts = val_str.split("-")
            last_part = parts[-1]
            if last_part.isdigit():
                num = int(last_part)
                if num > dernier_numero_int:
                    dernier_numero_int = num
        elif val_str.isdigit():
            num = int(val_str)
            if num > dernier_numero_int:
                dernier_numero_int = num

    nouveau_numero_int = dernier_numero_int + 1
    deal_id = f"{prefix_id}-2026-{nouveau_numero_int:03d}"

    font_data = Font(name=FONT_FAMILY, size=10)
    font_bold = Font(name=FONT_FAMILY, size=10, bold=True)
    thin_side = Side(border_style="thin", color=COLOR_BORDER)
    border_all = Border(left=thin_side, right=thin_side, top=thin_side, bottom=thin_side)
    fill_ok = PatternFill(start_color="EAFAF1", end_color="EAFAF1", fill_type="solid")

    ws.row_dimensions[target_row].height = 20

    c_a = ws.cell(row=target_row, column=1, value=deal_id)
    c_b = ws.cell(row=target_row, column=2, value=emission)
    c_c = ws.cell(row=target_row, column=3, value=nom_client.strip())
    c_d = ws.cell(row=target_row, column=4, value=telephone.strip())
    c_e = ws.cell(row=target_row, column=5, value=objet_prestation.strip())
    c_f = ws.cell(row=target_row, column=6, value=float(montant_htva))
    c_g = ws.cell(row=target_row, column=7, value=statut_initial.strip())
    c_h = ws.cell(row=target_row, column=8, value=f"=IF(B{target_row}=\"\",\"\",B{target_row}+{actual_delay})")
    c_i = ws.cell(row=target_row, column=9, value=f"=IF(G{target_row}=\"\",\"\",IF(G{target_row}=\"Accepté\",\"Gagné\",IF(G{target_row}=\"Refusé\",\"Clôturé\",IF(OR(G{target_row}=\"En attente\",G{target_row}=\"Envoyé\"),IF(AND(H{target_row}<>\"\",TODAY()>H{target_row}),\"À RELANCER D'URGENCE\",\"Dans les temps\"),IF(G{target_row}=\"À préparer\",\"En cours bureau\",\"\")))))")
    c_j = ws.cell(row=target_row, column=10, value="Envoi initial")
    c_k = ws.cell(row=target_row, column=11, value=commentaires.strip() if commentaires else "Nouveau dossier")

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
        cell = ws.cell(row=target_row, column=col)
        cell.font = font_data
        cell.border = border_all
        if col == 9:
            cell.protection = Protection(locked=True)
            cell.fill = fill_ok
        else:
            cell.protection = Protection(locked=False)

    try:
        ws.protection.set_password(password)
        ws.protection.sheet = True
        ws.protection.enable()
    except Exception:
        pass

    wb.save(excel_path)
    return target_row, deal_id


def main() -> None:
    parser = argparse.ArgumentParser(description="Insère une nouvelle affaire dans le classeur Excel protégé.")
    parser.add_argument("--excel-path", "-e", required=True, help="Chemin du classeur Excel")
    parser.add_argument("--client", "-c", required=True, help="Nom du client")
    parser.add_argument("--montant", "-m", type=float, required=True, help="Montant HTVA")
    parser.add_argument("--objet", "-o", required=True, help="Objet de la prestation")
    parser.add_argument("--tel", "-t", default="", help="Numéro de contact")
    parser.add_argument("--statut", "-s", default="En attente", help="Statut initial")
    parser.add_argument("--commentaires", default="", help="Notes")
    parser.add_argument("--sector", default="general", choices=["btp", "services", "maintenance", "healthcare", "retail", "general"], help="Secteur métier")
    parser.add_argument("--delay", type=int, default=None, help="Délai de relance personnalisé en jours")
    parser.add_argument("--password", "-p", default="OFFICE2026", help="Mot de passe feuille")

    args = parser.parse_args()

    row, deal_id = append_deal_to_workbook(
        excel_path=args.excel_path,
        nom_client=args.client,
        montant_htva=args.montant,
        objet_prestation=args.objet,
        telephone=args.tel,
        statut_initial=args.statut,
        commentaires=args.commentaires,
        sector=args.sector,
        delay_days=args.delay,
        password=args.password,
    )
    print(f"[OK] Affaire insérée avec succès : {deal_id} (Ligne {row}) dans {args.excel_path}")


if __name__ == "__main__":
    main()
