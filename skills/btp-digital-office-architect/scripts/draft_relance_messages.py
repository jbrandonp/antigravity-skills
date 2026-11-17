"""
Script to automatically generate personalized WhatsApp and email follow-up messages
for overdue quotes found in 'DEVIS_SANS_OUBLI_MODELE_PRO.xlsx'.
Streamlines the Friday 16h30 ritual from 15 minutes down to 2 minutes.
Strictly typed, zero 'Any'.
"""

import argparse
import os
import sys
from datetime import date, datetime
from typing import Final, List, Optional, Tuple, TypedDict
import openpyxl

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


class OverdueQuote(TypedDict):
    num_devis: str
    date_emission: str
    client: str
    tel: str
    objet: str
    montant_htva: float
    jours_retard: int


def scan_overdue_quotes(excel_path: str) -> List[OverdueQuote]:
    """
    Parcourt le classeur Excel et extrait la liste de tous les devis en retard de relance.

    Paramètres :
        excel_path (str) : Chemin du classeur de devis client.

    Retour :
        List[OverdueQuote] : Liste des fiches de devis en souffrance.
    """
    if not os.path.isfile(excel_path):
        raise FileNotFoundError(f"Classeur Excel introuvable : {excel_path}")

    wb = openpyxl.load_workbook(excel_path, data_only=True)
    ws = wb["Suivi des Devis"]

    today = date.today()
    overdue_list: List[OverdueQuote] = []

    for row in range(5, ws.max_row + 1):
        num_val = ws.cell(row=row, column=1).value
        if not num_val:
            continue
        num_str = str(num_val).strip()
        if num_str.startswith("AVERTISSEMENT") or num_str.startswith("Avertissement") or len(num_str) > 40:
            continue

        statut = str(ws.cell(row=row, column=7).value or "").strip()
        statut_relance = str(ws.cell(row=row, column=9).value or "").strip()
        date_relance_val = ws.cell(row=row, column=8).value
        date_emission_val = ws.cell(row=row, column=2).value

        target_date: Optional[date] = None
        if isinstance(date_relance_val, datetime):
            target_date = date_relance_val.date()
        elif isinstance(date_relance_val, date):
            target_date = date_relance_val

        # Détection d'urgence : soit la formule indique l'urgence, soit la date est dépassée
        is_overdue = False
        jours_retard = 0
        if target_date is not None and statut in ("En attente", "Envoyé"):
            if target_date < today:
                is_overdue = True
                jours_retard = (today - target_date).days

        if "URGENCE" in statut_relance or is_overdue:
            client = str(ws.cell(row=row, column=3).value or "Client")
            tel = str(ws.cell(row=row, column=4).value or "")
            objet = str(ws.cell(row=row, column=5).value or "Travaux")
            montant_val = ws.cell(row=row, column=6).value
            montant = float(montant_val) if isinstance(montant_val, (int, float)) else 0.0

            emission_str = ""
            if isinstance(date_emission_val, (date, datetime)):
                emission_str = date_emission_val.strftime("%d/%m/%Y")

            overdue_list.append({
                "num_devis": num_str,
                "date_emission": emission_str,
                "client": client,
                "tel": tel,
                "objet": objet,
                "montant_htva": montant,
                "jours_retard": max(1, jours_retard),
            })

    return overdue_list


def generate_messages_markdown(quotes: List[OverdueQuote], company_name: str, artisan_name: str) -> str:
    """
    Génère un document markdown avec des scripts de relance personnalisés WhatsApp et Email.
    """
    lines: List[str] = [
        f"# 📲 MESSAGES DE RELANCE PERSONNALISÉS — RITUEL DU VENDREDI",
        f"## Entreprise : {company_name} | Date : {date.today().strftime('%d/%m/%Y')}",
        "",
        f"**Nombre de devis chauds à relancer :** {len(quotes)}",
        f"**Chiffre d'affaires total en attente :** {sum(q['montant_htva'] for q in quotes):,.2f} € HTVA",
        "",
        "---",
        "",
    ]

    for idx, q in enumerate(quotes, start=1):
        lines.extend([
            f"### {idx}. {q['client'].upper()} — {q['montant_htva']:,.2f} € HTVA ({q['num_devis']})",
            f"- **Objet du chantier :** {q['objet']}",
            f"- **Téléphone :** `{q['tel']}`",
            f"- **Retard de relance :** ~{q['jours_retard']} jours",
            "",
            "#### 💬 Option A : Message Texte WhatsApp (Rapide & Direct)",
            "> « Bonjour " + q['client'] + ", c'est " + artisan_name + " de " + company_name + ". ",
            "> Je finalise actuellement notre planning de chantiers pour les prochaines semaines et je voulais savoir où vous en étiez par rapport à notre devis pour " + q['objet'] + " (" + f"{q['montant_htva']:,.2f}" + " € HTVA) ? ",
            "> Avez-vous besoin de précisions ou souhaitez-vous qu'on bloque une date d'intervention ? Bonne fin de semaine ! »",
            "",
            "#### 🎙️ Option B : Script Vocal WhatsApp (20 secondes)",
            "> *(Ton chaleureux et détendu)*",
            "> « Bonjour " + q['client'] + ", c'est " + artisan_name + " au téléphone. Petit message rapide entre deux chantiers. ",
            "> Je regardais mes dossiers et je voyais qu'on n'avait pas refait le point sur votre devis de " + q['objet'] + ". ",
            "> Comme je commande le matériel lundi matin, faites-moi signe par ici si c'est toujours bon pour vous pour qu'on garde le créneau. Très bon week-end ! »",
            "",
            "#### ✉️ Option C : Email de Relance Doux",
            "> **Objet :** Suivi de votre devis " + q['num_devis'] + " — " + q['objet'],
            ">",
            "> Bonjour " + q['client'] + ",",
            ">",
            "> J'espère que vous allez bien.",
            "> Je me permets de revenir vers vous concernant le devis " + q['num_devis'] + " transmis récemment pour vos travaux de " + q['objet'] + ".",
            ">",
            "> Le projet est-il toujours d'actualité ? Avez-vous des questions techniques sur le matériel prévu ou sur les délais d'exécution ?",
            ">",
            "> Restant à votre entière disposition,",
            "> Bien cordialement,",
            ">",
            "> **" + artisan_name + "** — " + company_name,
            "",
            "---",
            "",
        ])

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Générateur de messages de relance personnalisés WhatsApp et Email")
    parser.add_argument("--excel-path", type=str, required=True, help="Chemin du classeur Excel de devis")
    parser.add_argument("--company-name", type=str, default="Bureau Numérique BTP", help="Nom commercial de l'entreprise")
    parser.add_argument("--artisan-name", type=str, default="Brandon", help="Prénom ou nom du gérant")
    parser.add_argument("--output-md", type=str, default="", help="Chemin du fichier Markdown de sortie (optionnel)")

    args = parser.parse_args()

    quotes = scan_overdue_quotes(args.excel_path)

    if not quotes:
        print("[INFO] Aucun devis urgent en retard de relance détecté dans le classeur. Félicitations !")
        sys.exit(0)

    md_content = generate_messages_markdown(quotes, args.company_name, args.artisan_name)

    if args.output_md:
        with open(args.output_md, "w", encoding="utf-8") as f:
            f.write(md_content)
        print(f"[SUCCÈS] {len(quotes)} messages de relance générés dans : {args.output_md}")
    else:
        print(md_content)


if __name__ == "__main__":
    main()
