"""
Script to safely append new quotes into the protected Excel workbook 'DEVIS_SANS_OUBLI_MODELE_PRO.xlsx'.
Preserves cell protections, formatting, and live dynamic formulas.
Strictly typed, zero 'Any'.
"""

import argparse
import os
import sys
from datetime import date, datetime
from typing import Final, List, Optional, Tuple, Union
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


def append_devis_to_workbook(
    excel_path: str,
    nom_client: str,
    montant_htva: float,
    objet_travaux: str,
    telephone: str = "",
    date_emission: Optional[date] = None,
    statut_initial: str = "En attente",
    commentaires: str = "",
    password: str = "BTP2026",
) -> Tuple[int, str]:
    """
    Insère une nouvelle ligne de devis dans le classeur Excel en respectant
    le zonage des cellules protégées et les formules vivantes.

    Paramètres :
        excel_path (str) : Chemin du fichier Excel cible.
        nom_client (str) : Nom complet du client ou de l'entreprise donneuse d'ordre.
        montant_htva (float) : Montant chiffré hors TVA.
        objet_travaux (str) : Description des travaux ou du chantier.
        telephone (str) : Numéro de contact de l'artisan/client.
        date_emission (Optional[date]) : Date de remise de l'offre (défaut : aujourd'hui).
        statut_initial (str) : Statut de l'offre ('En attente', 'Envoyé', 'À préparer').
        commentaires (str) : Notes ou détails additionnels.
        password (str) : Mot de passe de protection de la feuille.

    Retour :
        Tuple[int, str] : Numéro de la ligne insérée et identifiant du devis généré.
    """
    if not os.path.isfile(excel_path):
        raise FileNotFoundError(f"Le fichier Excel cible est introuvable : {excel_path}")

    if montant_htva <= 0:
        raise ValueError("Le montant du devis doit être un nombre strictement positif.")

    if not nom_client.strip():
        raise ValueError("Le nom du client ne peut pas être vide.")

    emission = date_emission if date_emission is not None else date.today()

    wb = openpyxl.load_workbook(excel_path)
    ws = wb["Suivi des Devis"]

    # Trouver la première ligne libre (à partir de la ligne 5)
    target_row = 5
    dernier_numero_int = 0

    for r in range(5, ws.max_row + 2):
        val = ws.cell(row=r, column=1).value
        val_str = str(val or "").strip()
        # Si on atteint les disclaimers ou une ligne vide
        if not val or val_str.startswith("AVERTISSEMENT") or val_str.startswith("Avertissement"):
            target_row = r
            break
        # Analyse du numéro pour incrément automatique
        if "DEV-" in val_str:
            try:
                num_part = int(val_str.split("-")[-1])
                if num_part > dernier_numero_int:
                    dernier_numero_int = num_part
            except ValueError:
                pass
        target_row = r + 1

    annee_courante = emission.year
    nouveau_numero = f"DEV-{annee_courante}-{dernier_numero_int + 1:03d}"

    # Styles
    font_data = Font(name=FONT_FAMILY, size=10)
    font_bold = Font(name=FONT_FAMILY, size=10, bold=True)
    border_thin = Border(
        left=Side(style="thin", color=COLOR_BORDER),
        right=Side(style="thin", color=COLOR_BORDER),
        top=Side(style="thin", color=COLOR_BORDER),
        bottom=Side(style="thin", color=COLOR_BORDER),
    )

    # 1. N° Devis (Col 1)
    c1 = ws.cell(row=target_row, column=1, value=nouveau_numero)
    c1.font = font_bold
    c1.alignment = Alignment(horizontal="center", vertical="center")
    c1.protection = Protection(locked=False)
    c1.border = border_thin

    # 2. Date Émission (Col 2)
    c2 = ws.cell(row=target_row, column=2, value=emission)
    c2.font = font_data
    c2.number_format = "YYYY-MM-DD"
    c2.alignment = Alignment(horizontal="center", vertical="center")
    c2.protection = Protection(locked=False)
    c2.border = border_thin

    # 3. Nom du Client (Col 3)
    c3 = ws.cell(row=target_row, column=3, value=nom_client.strip())
    c3.font = font_bold
    c3.alignment = Alignment(horizontal="left", vertical="center")
    c3.protection = Protection(locked=False)
    c3.border = border_thin

    # 4. Téléphone (Col 4)
    c4 = ws.cell(row=target_row, column=4, value=telephone.strip())
    c4.font = font_data
    c4.alignment = Alignment(horizontal="center", vertical="center")
    c4.protection = Protection(locked=False)
    c4.border = border_thin

    # 5. Objet des Travaux (Col 5)
    c5 = ws.cell(row=target_row, column=5, value=objet_travaux.strip())
    c5.font = font_data
    c5.alignment = Alignment(horizontal="left", vertical="center")
    c5.protection = Protection(locked=False)
    c5.border = border_thin

    # 6. Montant HTVA (€) (Col 6)
    c6 = ws.cell(row=target_row, column=6, value=float(montant_htva))
    c6.font = font_data
    c6.number_format = "#,##0.00 €"
    c6.alignment = Alignment(horizontal="right", vertical="center")
    c6.protection = Protection(locked=False)
    c6.border = border_thin

    # 7. Statut Actuel (Col 7)
    c7 = ws.cell(row=target_row, column=7, value=statut_initial)
    c7.font = font_data
    c7.alignment = Alignment(horizontal="center", vertical="center")
    c7.protection = Protection(locked=False)
    c7.border = border_thin

    # 8. Date Relance Prévue (Col 8) — Formule vivante J+14
    c8 = ws.cell(row=target_row, column=8, value=f'=IF(B{target_row}="","",B{target_row}+14)')
    c8.font = font_data
    c8.number_format = "YYYY-MM-DD"
    c8.alignment = Alignment(horizontal="center", vertical="center")
    c8.protection = Protection(locked=False)
    c8.border = border_thin

    # 9. Statut Relance Calculé (Col 9) — FORMULE VERROUILLÉE
    formula_relance = (
        f'=IF(G{target_row}="","",IF(G{target_row}="Accepté","Gagné",'
        f'IF(G{target_row}="Refusé","Clôturé",'
        f'IF(OR(G{target_row}="En attente",G{target_row}="Envoyé"),'
        f'IF(AND(H{target_row}<>"",TODAY()>H{target_row}),"À RELANCER D\'URGENCE","Dans les temps"),'
        f'IF(G{target_row}="À préparer","En cours bureau","")))))'
    )
    c9 = ws.cell(row=target_row, column=9, value=formula_relance)
    c9.font = font_bold
    c9.alignment = Alignment(horizontal="center", vertical="center")
    c9.protection = Protection(locked=True)  # Verrouillé pour protéger la logique
    c9.border = border_thin

    # 10. Dernier Contact (Col 10)
    c10 = ws.cell(row=target_row, column=10, value="")
    c10.font = font_data
    c10.alignment = Alignment(horizontal="center", vertical="center")
    c10.protection = Protection(locked=False)
    c10.border = border_thin

    # 11. Commentaires (Col 11)
    c11 = ws.cell(row=target_row, column=11, value=commentaires.strip())
    c11.font = font_data
    c11.alignment = Alignment(horizontal="left", vertical="center")
    c11.protection = Protection(locked=False)
    c11.border = border_thin

    ws.row_dimensions[target_row].height = 20

    # Réactiver la protection avec le mot de passe
    ws.protection.set_password(password)

    wb.save(excel_path)
    return target_row, nouveau_numero


def main() -> None:
    parser = argparse.ArgumentParser(description="Ajoute un nouveau devis dans le classeur Excel sécurisé")
    parser.add_argument("--excel-path", type=str, required=True, help="Chemin du classeur Excel")
    parser.add_argument("--client", type=str, required=True, help="Nom du client")
    parser.add_argument("--montant", type=float, required=True, help="Montant HTVA en euros")
    parser.add_argument("--objet", type=str, required=True, help="Description des travaux")
    parser.add_argument("--tel", type=str, default="", help="Numéro de téléphone")
    parser.add_argument("--statut", type=str, default="En attente", help="Statut initial")
    parser.add_argument("--notes", type=str, default="", help="Commentaires / Notes")
    parser.add_argument("--password", type=str, default="BTP2026", help="Mot de passe de la feuille")

    args = parser.parse_args()

    try:
        row_idx, num_devis = append_devis_to_workbook(
            excel_path=args.excel_path,
            nom_client=args.client,
            montant_htva=args.montant,
            objet_travaux=args.objet,
            telephone=args.tel,
            statut_initial=args.statut,
            commentaires=args.notes,
            password=args.password,
        )
        print("======================================================================")
        print("[SUCCÈS] Nouveau devis inséré avec succès dans le classeur Excel !")
        print("======================================================================")
        print(f"Numéro généré : {num_devis}")
        print(f"Ligne Excel   : {row_idx}")
        print(f"Client        : {args.client}")
        print(f"Montant HTVA  : {args.montant:,.2f} €")
        print(f"Statut        : {args.statut}")
        print(f"Formule Col 9 : Injectée et verrouillée sous mot de passe.")
        print("======================================================================\n")
    except Exception as exc:
        print(f"[ERREUR] Échec de l'insertion du devis : {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
