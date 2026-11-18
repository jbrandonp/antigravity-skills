"""
Générateur d'Avenants de Chantier Express et d'Attestations Fiscales TVA 6% (Belgique).
Permet aux artisans BTP de faire signer les travaux supplémentaires en 30 secondes sur smartphone
et de sécuriser immédiatement l'application du taux réduit de TVA 6% (logement > 10 ans).
Strictement typé, zéro 'Any'.
"""

import sys
from datetime import date
from typing import Final, NamedTuple, Optional, TypedDict

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


class AmendmentSpec(TypedDict):
    quote_ref: str
    client_name: str
    client_phone: str
    site_address: str
    work_description: str
    amount_htva_eur: float
    vat_rate_pct: float
    deposit_requested_eur: float
    execution_delay_days: int


class BelgianVatCertificateSpec(TypedDict):
    contractor_name: str
    contractor_bce_tva: str
    client_name: str
    client_address: str
    property_address: str
    first_occupancy_year: int
    is_private_dwelling: bool


def generate_whatsapp_amendment_text(spec: AmendmentSpec) -> str:
    """
    Génère le texte légal condensé d'avenant pour validation express par WhatsApp ou SMS.
    La réponse écrite 'OUI' ou 'ACCORD' constitue un commencement de preuve par écrit
    valable selon le Code de droit économique belge.
    """
    vat_amount = spec["amount_htva_eur"] * (spec["vat_rate_pct"] / 100.0)
    total_ttc = spec["amount_htva_eur"] + vat_amount

    text = (
        f"🚧 *AVENANT TRAVAUX CHANTIER — {spec['quote_ref']}*\n"
        f"Bonjour {spec['client_name']},\n\n"
        f"Suite à votre demande sur chantier à {spec['site_address']}, voici l'avenant chiffré :\n"
        f"📝 *Détail travaux :* {spec['work_description']}\n"
        f"💰 *Montant :* {spec['amount_htva_eur']:,.2f} € HTVA (TVA {spec['vat_rate_pct']:.0f}% : {vat_amount:,.2f} €)\n"
        f"👉 *Total TTC :* {total_ttc:,.2f} € TVAC\n"
    )

    if spec["deposit_requested_eur"] > 0:
        text += f"💳 *Acompte matériel souhaité :* {spec['deposit_requested_eur']:,.2f} €\n"

    text += (
        f"⏱️ *Délai supplémentaire prévu :* +{spec['execution_delay_days']} jour(s)\n\n"
        f"⚠️ *Pour validation et démarrage immédiat des travaux, merci de répondre simplement 'ACCORD' ou 'OUI' à ce message.*\n"
        f"Ce message vaut bon de commande d'avenant contractuel."
    )
    return text


def generate_belgian_vat_6_percent_certificate(spec: BelgianVatCertificateSpec) -> str:
    """
    Génère la mention légale obligatoire déchargeant l'artisan de la responsabilité TVA 6%.
    Conforme à l'Arrêté Royal n° 20 du Code de la TVA belge (Article 17 § 1).
    """
    current_year = date.today().year
    age_of_building = current_year - spec["first_occupancy_year"]

    status_warning = ""
    if age_of_building < 10:
        status_warning = (
            f"\n🚨 ATTENTION : Ce bâtiment a {age_of_building} ans (< 10 ans) ! "
            "Le taux légal obligatoire est de 21% (sauf régime spécial démolition/reconstruction à 6%).\n"
        )

    clause = (
        f"==================================================================\n"
        f"  ATTESTATION LÉGALE TVA 6% — TRAVAUX IMMOBILIERS (BELGIQUE)\n"
        f"  (Article 17 § 1 de l'Arrêté Royal n° 20 du Code de la TVA)\n"
        f"==================================================================\n"
        f"{status_warning}"
        f"Entrepreneur : {spec['contractor_name']} (TVA: {spec['contractor_bce_tva']})\n"
        f"Maître d'ouvrage (Client) : {spec['client_name']}\n"
        f"Adresse du bien concerné : {spec['property_address']}\n"
        f"Année de première occupation : {spec['first_occupancy_year']} (Âge : {age_of_building} ans)\n\n"
        f"DÉCLARATION LÉGALE SUR L'HONNEUR DU CLIENT :\n"
        f"« Le client soussigné atteste expressément par la présente que :\n"
        f"1. L'immeuble précité est utilisé effectivement et principalement comme logement privé ;\n"
        f"2. L'immeuble a été occupé pour la première fois il y a plus de dix ans à la date de la facture ;\n"
        f"3. Les travaux de rénovation/transformation sont fournis et facturés directement au consommateur final.\n\n"
        f"En l'absence de contestation écrite dans un délai d'un mois à compter de la réception de la facture,\n"
        f"l'artisan est déchargé de toute responsabilité fiscale quant à l'application du taux réduit de 6%.\n"
        f"La responsabilité relative au paiement de la taxe, des intérêts et des amendes sera reportée sur le client. »\n"
        f"=================================================================="
    )
    return clause


if __name__ == "__main__":
    # Test 1 : Avenant express smartphone
    sample_amendment: AmendmentSpec = {
        "quote_ref": "DEV-2026-042",
        "client_name": "Monsieur Dupont",
        "client_phone": "0485 98 76 54",
        "site_address": "Chaudfontaine",
        "work_description": "Ajout de 3 vannes thermostatiques connectées + désembouage circuit radiateurs",
        "amount_htva_eur": 680.0,
        "vat_rate_pct": 6.0,
        "deposit_requested_eur": 200.0,
        "execution_delay_days": 1,
    }
    print("[TEST 1] MESSAGE D'AVENANT WHATSAPP SMARTPHONE :")
    print(generate_whatsapp_amendment_text(sample_amendment))
    print("\n" + "-" * 60 + "\n")

    # Test 2 : Attestation TVA 6% belge
    sample_cert: BelgianVatCertificateSpec = {
        "contractor_name": "Bureau Numérique BTP / Chauffage Meuse",
        "contractor_bce_tva": "BE 0459.180.573",
        "client_name": "Monsieur Dupont",
        "client_address": "Rue des Villas 14, 4050 Chaudfontaine",
        "property_address": "Rue des Villas 14, 4050 Chaudfontaine",
        "first_occupancy_year": 2008,
        "is_private_dwelling": True,
    }
    print("[TEST 2] ATTESTATION LÉGALE TVA 6% BELGE :")
    print(generate_belgian_vat_6_percent_certificate(sample_cert))
