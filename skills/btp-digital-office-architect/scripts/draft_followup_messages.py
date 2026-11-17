"""
Script universel pour générer automatiquement les messages de relance personnalisés
(vocaux WhatsApp, SMS/textes et e-mails doux) pour les affaires en retard.
S'adapte dynamiquement au ton du secteur métier (BTP, Conseil, Garage, Soins, Commerce).
Strictement typé, zéro 'Any'.
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


class OverdueDeal(TypedDict):
    ref_deal: str
    date_emission: str
    client: str
    tel: str
    objet: str
    montant_htva: float
    jours_retard: int


def scan_overdue_deals(excel_path: str) -> List[OverdueDeal]:
    """
    Parcourt le classeur Excel et extrait les affaires nécessitant une relance.
    """
    if not os.path.isfile(excel_path):
        raise FileNotFoundError(f"Classeur Excel introuvable : {excel_path}")

    wb = openpyxl.load_workbook(excel_path, data_only=True)
    sheet_name = "Suivi des Devis" if "Suivi des Devis" in wb.sheetnames else wb.sheetnames[0]
    ws = wb[sheet_name]

    today = date.today()
    overdue_list: List[OverdueDeal] = []

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

        is_overdue = False
        jours_retard = 0
        if target_date is not None and statut in ("En attente", "Envoyé"):
            if target_date < today:
                is_overdue = True
                jours_retard = (today - target_date).days

        if "URGENCE" in statut_relance or is_overdue:
            client = str(ws.cell(row=row, column=3).value or "Client")
            tel = str(ws.cell(row=row, column=4).value or "")
            objet = str(ws.cell(row=row, column=5).value or "Prestation")
            montant_val = ws.cell(row=row, column=6).value
            montant = float(montant_val) if isinstance(montant_val, (int, float)) else 0.0

            emission_str = ""
            if isinstance(date_emission_val, (date, datetime)):
                emission_str = date_emission_val.strftime("%d/%m/%Y")

            overdue_list.append({
                "ref_deal": num_str,
                "date_emission": emission_str,
                "client": client,
                "tel": tel,
                "objet": objet,
                "montant_htva": montant,
                "jours_retard": max(1, jours_retard),
            })

    return overdue_list


def generate_messages_for_deal(
    deal: OverdueDeal,
    sector: str = "general",
    sender_name: str = "Brandon",
) -> Dict[str, str]:
    """
    Rédige les 3 formats de messages personnalisés selon le secteur.
    """
    client = deal["client"]
    objet = deal["objet"]
    ref = deal["ref_deal"]
    montant = deal["montant_htva"]
    sec = sector.lower().strip()

    if sec == "btp":
        vocal = (
            f"« Bonjour {client}, {sender_name} à l'appareil. Je vous fais un petit vocal rapide pour prendre des nouvelles. "
            f"Je suis en train de caler le planning des chantiers pour les prochaines semaines avec l'équipe. "
            f"Est-ce que vous avez pu jeter un œil à notre devis pour {objet} ({montant:,.2f} € HTVA) ? "
            f"Faites-moi un petit signe si c'est bon pour vous, comme ça je vous réserve votre créneau d'intervention. "
            f"Passez un excellent week-end ! »"
        )
        texte = (
            f"Bonjour {client}, {sender_name} à l'appareil. On prépare le planning chantiers du mois prochain. "
            f"Avez-vous des questions sur notre devis pour {objet} ({montant:,.2f} €) ? "
            f"Dites-moi si vous souhaitez qu'on réserve la date. Bon week-end !"
        )
        email = (
            f"Objet : Suivi de votre devis {ref} — {objet}\n\n"
            f"Bonjour {client},\n\n"
            f"Je me permets de revenir vers vous concernant notre proposition du {deal['date_emission']} "
            f"relative aux travaux suivants : {objet} (montant de {montant:,.2f} € HTVA).\n\n"
            f"Nous finalisons actuellement notre planning d'intervention pour les prochaines semaines. "
            f"Avez-vous eu l'occasion d'examiner notre offre ou souhaitez-vous un ajustement technique particulier ?\n\n"
            f"Je reste à votre entière disposition pour tout renseignement complémentaire.\n\n"
            f"Bien cordialement,\n{sender_name}"
        )
    elif sec == "services":
        vocal = (
            f"« Bonjour {client}, c'est {sender_name}. J'espère que ta semaine s'est bien passée. "
            f"Je faisais le point sur nos lancements de projets pour le mois qui vient. "
            f"As-tu pu échanger en interne sur notre proposition pour {objet} ({montant:,.2f} € HTVA) ? "
            f"Dis-moi si tu as des questions ou si tu souhaites qu'on ajuste certains points avant de démarrer. Bon week-end ! »"
        )
        texte = (
            f"Hello {client}, as-tu pu regarder notre proposition pour {objet} ? "
            f"On bloque les créneaux de delivery de ce mois-ci. Dis-moi si tu veux un call rapide de 5 min. Bon vendredi !"
        )
        email = (
            f"Objet : Suivi de notre proposition {ref} — {objet}\n\n"
            f"Bonjour {client},\n\n"
            f"J'espère que vous passez une excellente semaine.\n\n"
            f"Je reviens vers vous concernant notre proposition d'accompagnement transmise le {deal['date_emission']} "
            f"pour le projet : {objet} (budget de {montant:,.2f} € HTVA).\n\n"
            f"Afin d'anticiper au mieux les disponibilités de notre équipe pour votre livraison, "
            f"pouvez-vous me dire où en est votre arbitrage en interne ?\n\n"
            f"À votre écoute pour en discuter,\n\n"
            f"Cordialement,\n{sender_name}"
        )
    elif sec == "maintenance":
        vocal = (
            f"« Bonjour {client}, l'atelier mécanique à l'appareil. "
            f"Je vous appelle concernant votre ordre de réparation pour {objet} ({montant:,.2f} € HTVA). "
            f"Les pièces sont réservées chez notre fournisseur, mais nous attendons votre accord pour lancer le montage "
            f"et libérer votre véhicule pour la fin de semaine. Merci de me faire signe dès que possible ! »"
        )
        texte = (
            f"Bonjour {client}, le devis de remise en état pour {objet} ({montant:,.2f} €) est prêt. "
            f"Pouvez-vous nous confirmer votre accord afin qu'on lance la commande des pièces ? Merci, l'Atelier."
        )
        email = (
            f"Objet : Accord devis atelier {ref} — {objet}\n\n"
            f"Bonjour {client},\n\n"
            f"Suite au diagnostic effectué, notre devis pour {objet} s'élève à {montant:,.2f} € HTVA.\n\n"
            f"Afin de commander les pièces et d'effectuer la remise en état dans les meilleurs délais, "
            f"merci de nous confirmer votre validation par retour de mail ou par téléphone.\n\n"
            f"Cordialement,\nL'Atelier"
        )
    elif sec == "healthcare":
        vocal = (
            f"« Bonjour {client}, ici le cabinet de soins. "
            f"Je vous contacte simplement pour faire le point sur la suite de votre protocole pour {objet}. "
            f"Afin de garantir la continuité de votre rééducation sans interruption, "
            f"pensez à planifier vos prochains créneaux en ligne ou par message. Prenez bien soin de vous ! »"
        )
        texte = (
            f"Bonjour {client}, nous planifions les séances de suivi pour votre protocole : {objet}. "
            f"N'hésitez pas à nous indiquer vos disponibilités de la semaine prochaine. Bon rétablissement !"
        )
        email = (
            f"Objet : Suivi de votre protocole de soins — {objet}\n\n"
            f"Bonjour {client},\n\n"
            f"Nous faisons le point sur le déroulement de votre prise en charge ({objet}).\n\n"
            f"Pour assurer les meilleurs résultats et la consolidation des progrès réalisés, "
            f"nous vous invitons à confirmer vos prochains créneaux de rendez-vous.\n\n"
            f"Restant à votre disposition,\n\n"
            f"Le Cabinet de Soins"
        )
    else:
        vocal = (
            f"« Bonjour {client}, {sender_name} à l'appareil. Je vous fais un petit message rapide en cette fin de semaine. "
            f"Je voulais m'assurer que vous aviez bien reçu notre offre concernant {objet} ({montant:,.2f} € HTVA). "
            f"Avez-vous eu l'opportunité d'y jeter un œil ? N'hésitez pas si vous avez la moindre question technique ou pratique. "
            f"Passez un très bon week-end ! »"
        )
        texte = (
            f"Bonjour {client}, {sender_name} à l'appareil. Avez-vous pu prendre connaissance de notre proposition pour {objet} ({montant:,.2f} €) ? "
            f"Restant à votre disposition si besoin d'un ajustement. Bon vendredi !"
        )
        email = (
            f"Objet : Suivi de votre offre {ref} — {objet}\n\n"
            f"Bonjour {client},\n\n"
            f"Je me permets de faire un point avec vous sur notre offre du {deal['date_emission']} "
            f"concernant : {objet} (montant de {montant:,.2f} € HTVA).\n\n"
            f"Avez-vous pu en prendre connaissance et avez-vous des questions sur notre proposition ?\n\n"
            f"Restant à votre entière écoute pour avancer ensemble,\n\n"
            f"Cordialement,\n{sender_name}"
        )

    return {"vocal": vocal, "texte": texte, "email": email}


def main() -> None:
    parser = argparse.ArgumentParser(description="Générateur de messages de relance personnalisés universels.")
    parser.add_argument("--excel-path", "-e", required=True, help="Chemin du classeur Excel")
    parser.add_argument("--sector", "-s", default="general", choices=["btp", "services", "maintenance", "healthcare", "retail", "general"], help="Secteur métier")
    parser.add_argument("--sender", default="Brandon", help="Nom de l'émetteur")
    args = parser.parse_args()

    overdue = scan_overdue_deals(args.excel_path)
    total_urgent_revenue = sum(d["montant_htva"] for d in overdue)

    print("=" * 70)
    print(f"📋 RITUEL DU VENDREDI 16H30 — RELANCES D'AFFAIRES ({args.sector.upper()})")
    print("=" * 70)
    print(f"Nombre d'affaires en souffrance : {len(overdue)}")
    print(f"Montant total en attente de relance : {total_urgent_revenue:,.2f} € HTVA\n")

    if not overdue:
        print("✅ Aucune affaire en retard ! Félicitations, votre pipeline est parfaitement à jour.")
        return

    for idx, deal in enumerate(overdue, start=1):
        msgs = generate_messages_for_deal(deal, sector=args.sector, sender_name=args.sender)
        print(f"[{idx}/{len(overdue)}] AFFAIRE : {deal['ref_deal']} | {deal['client']} | {deal['montant_htva']:,.2f} € HTVA")
        print(f"    Objet : {deal['objet']}")
        print(f"    Date émission : {deal['date_emission']} (Retard : {deal['jours_retard']} j)")
        print(f"    Téléphone : {deal['tel'] or 'Non renseigné'}\n")
        print("  🎙️ VOCAL WHATSAPP CONSEILLÉ (20-25 sec) :")
        print(f"     {msgs['vocal']}\n")
        print("  📱 TEXTE SMS / WHATSAPP RAPIDE :")
        print(f"     {msgs['texte']}\n")
        print("  ✉️ E-MAIL DOUX DE RELANCE :")
        for line in msgs["email"].split("\n"):
            print(f"     {line}")
        print("-" * 70)


if __name__ == "__main__":
    main()
