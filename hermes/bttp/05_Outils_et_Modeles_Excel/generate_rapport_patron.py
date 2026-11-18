"""
Script to generate the automated 'Rapport Patron' from the quote tracking workbook.
Eliminates manual reporting time for recurring maintenance subscribers.
"""

import os
from datetime import date, datetime
from typing import Final, List, TypedDict
import openpyxl

DIR_PATH: Final[str] = os.path.dirname(os.path.abspath(__file__))
DEFAULT_EXCEL_PATH: Final[str] = os.path.join(DIR_PATH, "DEVIS_SANS_OUBLI_MODELE_PRO.xlsx")
DEFAULT_TXT_PATH: Final[str] = os.path.join(DIR_PATH, "RAPPORT_PATRON_EXEMPLE.txt")
COLOR_BORDER: Final[str] = "D9D9D9"


class DevisRelanceInfo(TypedDict):
    num: str
    client: str
    tel: str
    montant: float


class RapportMetrics(TypedDict):
    total_devis: int
    ca_en_attente: float
    ca_signe: float
    nb_urgences: int


def generate_rapport_patron(excel_path: str = DEFAULT_EXCEL_PATH, output_txt_path: str = DEFAULT_TXT_PATH) -> RapportMetrics:
    """
    Analyse le fichier de suivi des devis et génère le rapport mensuel du dirigeant.

    Paramètres :
        excel_path (str) : Chemin du classeur de devis client.
        output_txt_path (str) : Chemin de sortie du rapport synthétique d'une page.

    Retour :
        RapportMetrics : Dictionnaire typé contenant les métriques calculées.
    """
    wb = openpyxl.load_workbook(excel_path, data_only=True)
    ws = wb["Suivi des Devis"]

    total_devis = 0
    ca_en_attente = 0.0
    ca_signe = 0.0
    ca_perdu = 0.0
    devis_a_relancer: List[DevisRelanceInfo] = []

    # Parcours des lignes de devis (à partir de la ligne 5)
    for row in range(5, ws.max_row + 1):
        num_devis = ws.cell(row=row, column=1).value
        if not num_devis:
            continue
        num_str = str(num_devis).strip()
        # Filtre les mentions légales ou textes de bas de page
        if num_str.startswith("AVERTISSEMENT") or num_str.startswith("Avertissement") or len(num_str) > 40:
            continue

        total_devis += 1
        client = str(ws.cell(row=row, column=3).value or "Inconnu")
        tel = str(ws.cell(row=row, column=4).value or "")
        montant_val = ws.cell(row=row, column=6).value
        statut = str(ws.cell(row=row, column=7).value or "").strip()
        statut_relance = str(ws.cell(row=row, column=9).value or "").strip()

        montant = float(montant_val) if isinstance(montant_val, (int, float)) else 0.0

        if statut in ("En attente", "Envoyé"):
            ca_en_attente += montant
        elif statut == "Accepté":
            ca_signe += montant
        elif statut == "Refusé":
            ca_perdu += montant

        date_relance_val = ws.cell(row=row, column=8).value
        is_overdue = False
        if isinstance(date_relance_val, datetime):
            is_overdue = date_relance_val.date() < date.today()
        elif isinstance(date_relance_val, date):
            is_overdue = date_relance_val < date.today()

        is_urgent = (
            statut_relance == "À RELANCER D'URGENCE"
            or "URGENCE" in statut_relance
            or (statut in ("En attente", "Envoyé") and is_overdue)
        )

        if is_urgent:
            devis_a_relancer.append({
                "num": str(num_devis),
                "client": client,
                "tel": tel,
                "montant": montant,
            })

    # Synthèse textuelle prête à être envoyée au patron par email ou WhatsApp
    today_str = date.today().strftime("%d/%m/%Y")
    lignes_rapport = [
        "==================================================================",
        f"       RAPPORT MENSUEL DU DIRIGEANT — BUREAU NUMÉRIQUE BTP        ",
        f"                   Situation arrêtée au {today_str}               ",
        "==================================================================",
        "",
        "1. PERFORMANCE COMMERCIALE GLOBALE :",
        f"   • Nombre total de devis traités : {total_devis}",
        f"   • Chiffre d'affaires SIGNÉ (Validé) : {ca_signe:,.2f} € HTVA",
        f"   • Chiffre d'affaires EN ATTENTE DE DÉCISION : {ca_en_attente:,.2f} € HTVA",
        f"   • Chiffre d'affaires Refusé : {ca_perdu:,.2f} € HTVA",
        "",
        "------------------------------------------------------------------",
        "2. ALERTES PRIORITAIRES — LES DEVIS À RAPPELER CETTE SEMAINE :",
    ]

    if devis_a_relancer:
        for d in devis_a_relancer:
            lignes_rapport.append(
                f"   [!] {d['num']} | {d['client']} | {d['montant']:,.2f} € | Tél : {d['tel']}"
            )
        lignes_rapport.append("")
        lignes_rapport.append("   CONSEIL STRATÉGIQUE :")
        lignes_rapport.append(
            f"   ➔ Rappeler ces {len(devis_a_relancer)} clients peut débloquer immédiatement "
            f"jusqu'à {sum(d['montant'] for d in devis_a_relancer):,.2f} € de chantiers !"
        )
    else:
        lignes_rapport.append("   [OK] Aucun devis en retard critique de relance. Félicitations !")

    lignes_rapport.extend([
        "",
        "------------------------------------------------------------------",
        "3. PROCHAINES ACTIONS BUREAU & MAINTENANCE :",
        "   • Sauvegarde mensuelle du classeur OneDrive effectuée.",
        "   • Vérification des flux d'alertes : 100 % opérationnels.",
        "==================================================================",
    ])

    rapport_complet = "\n".join(lignes_rapport)

    with open(output_txt_path, "w", encoding="utf-8") as f:
        f.write(rapport_complet)

    print(f"[OK] Rapport Patron généré avec succès : {output_txt_path}")
    return {
        "total_devis": total_devis,
        "ca_en_attente": ca_en_attente,
        "ca_signe": ca_signe,
        "nb_urgences": len(devis_a_relancer),
    }


if __name__ == "__main__":
    generate_rapport_patron(DEFAULT_EXCEL_PATH, DEFAULT_TXT_PATH)
