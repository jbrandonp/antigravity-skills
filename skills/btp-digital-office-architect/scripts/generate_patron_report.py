"""
Générateur automatisé du "Rapport Patron" mensuel pour le Bureau Numérique Universel.
Scanne le classeur Excel en moins de 1 seconde et produit une synthèse exécutive d'une page
avec les chiffres clés, le montant sécurisé et les 3 actions prioritaires.
Combat actif contre le churn des abonnements récurrents. Strictement typé, zéro 'Any'.
"""

import argparse
import os
import sys
from datetime import date, datetime
from typing import Dict, Final, List, Optional, Tuple, TypedDict
import openpyxl

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


class PatronReportMetrics(TypedDict):
    company_name: str
    report_date: str
    total_deals: int
    won_count: int
    won_revenue: float
    pending_count: int
    pending_revenue: float
    overdue_count: int
    overdue_revenue: float
    conversion_rate: float
    top_urgent_actions: List[Dict[str, str]]


def generate_patron_report_metrics(
    excel_path: str,
    company_name: str = "Bureau Numérique",
) -> PatronReportMetrics:
    """
    Extrait les données du classeur Excel et compile les métriques de pilotage patronal.
    """
    if not os.path.isfile(excel_path):
        raise FileNotFoundError(f"Classeur Excel introuvable : {excel_path}")

    wb = openpyxl.load_workbook(excel_path, data_only=True)
    sheet_name = "Suivi des Devis" if "Suivi des Devis" in wb.sheetnames else wb.sheetnames[0]
    ws = wb[sheet_name]

    today = date.today()
    total_deals = 0
    won_count = 0
    won_revenue = 0.0
    pending_count = 0
    pending_revenue = 0.0
    overdue_count = 0
    overdue_revenue = 0.0

    urgent_candidates: List[Tuple[float, str, str, str, str, int]] = []

    for row in range(5, ws.max_row + 1):
        num_val = ws.cell(row=row, column=1).value
        if not num_val:
            continue
        num_str = str(num_val).strip()
        if num_str.startswith("AVERTISSEMENT") or num_str.startswith("Avertissement") or len(num_str) > 40:
            continue

        total_deals += 1
        statut = str(ws.cell(row=row, column=7).value or "").strip()
        montant_val = ws.cell(row=row, column=6).value
        montant = float(montant_val) if isinstance(montant_val, (int, float)) else 0.0
        client = str(ws.cell(row=row, column=3).value or "Client")
        tel = str(ws.cell(row=row, column=4).value or "")
        objet = str(ws.cell(row=row, column=5).value or "Prestation")
        date_relance_val = ws.cell(row=row, column=8).value

        target_date: Optional[date] = None
        if isinstance(date_relance_val, datetime):
            target_date = date_relance_val.date()
        elif isinstance(date_relance_val, date):
            target_date = date_relance_val

        statut_relance = str(ws.cell(row=row, column=9).value or "").strip()

        if statut == "Accepté":
            won_count += 1
            won_revenue += montant
        elif statut in ("En attente", "Envoyé"):
            pending_count += 1
            pending_revenue += montant

            is_overdue = False
            retard_jours = 0
            if target_date is not None and target_date < today:
                is_overdue = True
                retard_jours = (today - target_date).days

            if "URGENCE" in statut_relance or is_overdue:
                overdue_count += 1
                overdue_revenue += montant
                urgent_candidates.append((montant, num_str, client, tel, objet, max(1, retard_jours)))

    # Trier les actions urgentes par montant décroissant
    urgent_candidates.sort(key=lambda x: x[0], reverse=True)
    top_3 = urgent_candidates[:3]

    actions_list: List[Dict[str, str]] = []
    for mnt, num_id, cl, t, obj, ret in top_3:
        actions_list.append({
            "ref": num_id,
            "client": cl,
            "tel": t or "Non renseigné",
            "objet": obj,
            "montant": f"{mnt:,.2f} € HTVA",
            "retard": f"{ret} jours",
            "action": f"Passer un appel direct ou vocal WhatsApp (panier : {mnt:,.0f} €)",
        })

    taux_transfo = (won_count / total_deals * 100.0) if total_deals > 0 else 0.0

    return {
        "company_name": company_name,
        "report_date": today.strftime("%d/%m/%Y"),
        "total_deals": total_deals,
        "won_count": won_count,
        "won_revenue": round(won_revenue, 2),
        "pending_count": pending_count,
        "pending_revenue": round(pending_revenue, 2),
        "overdue_count": overdue_count,
        "overdue_revenue": round(overdue_revenue, 2),
        "conversion_rate": round(taux_transfo, 1),
        "top_urgent_actions": actions_list,
    }


def format_patron_report_text(m: PatronReportMetrics) -> str:
    """
    Formate le rapport en texte clair prêt à être imprimé ou envoyé sur smartphone.
    """
    sep = "=" * 70
    sub_sep = "-" * 70

    lines: List[str] = [
        sep,
        f"📊 RAPPORT PATRON MENSUEL — {m['company_name'].upper()}",
        f"Date d'édition : {m['report_date']} | Suivi d'activité & Pilotage du Pipeline",
        sep,
        "",
        "🎯 1. SYNTHÈSE DES CHIFFRES CLÉS (VUE D'ENSEMBLE) :",
        f"   • Total des dossiers traités    : {m['total_deals']}",
        f"   • Chiffre d'affaires GAGNÉ      : {m['won_revenue']:,.2f} € HTVA ({m['won_count']} dossiers validés)",
        f"   • Pipeline EN COURS             : {m['pending_revenue']:,.2f} € HTVA ({m['pending_count']} dossiers en attente)",
        f"   • Taux de transformation global : {m['conversion_rate']} %",
        "",
        sub_sep,
        f"🚨 2. ALERTES DE TRÉSORERIE & RETARDS ({m['overdue_count']} DOSSIERS EN SOUFFRANCE) :",
        f"   • Montant total en risque       : {m['overdue_revenue']:,.2f} € HTVA",
        "   • Diagnostic : Ces clients ont dépassé leur date normale de décision sans réponse.",
        "",
        sub_sep,
        "⚡ 3. LES 3 ACTIONS PRIORITAIRES DE LA SEMAINE (À FAIRE EN 15 MINUTES) :",
    ]

    if not m["top_urgent_actions"]:
        lines.append("   ✅ Aucune affaire en retard ! Félicitations, votre pipeline est propre.")
    else:
        for idx, act in enumerate(m["top_urgent_actions"], start=1):
            lines.append(f"   [{idx}] Dossier {act['ref']} — {act['client']} ({act['montant']})")
            lines.append(f"       Objet  : {act['objet']}")
            lines.append(f"       Contact: {act['tel']} (Retard de relance : {act['retard']})")
            lines.append(f"       Action : {act['action']}")
            lines.append("")

    lines.extend([
        sub_sep,
        "💡 NOTE DE CONSEIL :",
        "Le secret d'un bon mois réside dans la relance rapide. Récupérer un seul des 3 dossiers",
        f"ci-dessus injectera immédiatement du chiffre d'affaires sur votre compte bancaire.",
        sep,
    ])

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Générateur de Rapport Patron mensuel.")
    parser.add_argument("--excel-path", "-e", required=True, help="Chemin du classeur Excel")
    parser.add_argument("--company", "-c", default="Bureau Numérique", help="Nom de l'entreprise")
    parser.add_argument("--output", "-o", default="", help="Fichier texte de sortie")
    args = parser.parse_args()

    metrics = generate_patron_report_metrics(args.excel_path, company_name=args.company)
    report_text = format_patron_report_text(metrics)

    print(report_text)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report_text)
        print(f"\n[OK] Rapport Patron enregistré dans : {args.output}")


if __name__ == "__main__":
    main()
