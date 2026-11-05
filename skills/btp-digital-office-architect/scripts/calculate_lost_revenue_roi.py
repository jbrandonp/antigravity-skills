"""
Calculateur CLI du manque à gagner financier et du retour sur investissement (ROI).
Démontre mathématiquement à n'importe quel prospect le coût de l'inaction et la rentabilité
immédiate de l'installation du Bureau Numérique (< 15 jours de payback).
Strictement typé, zéro 'Any'.
"""

import argparse
import os
import sys
from typing import Final, TypedDict

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


class ROICalculationResult(TypedDict):
    client_name: str
    quotes_per_month: int
    avg_amount: float
    loss_rate: float
    win_rate: float
    pack_price: float
    forgotten_quotes_month: float
    recoverable_quotes_year: float
    monthly_loss_revenue: float
    annual_loss_revenue: float
    amortization_days: float
    payback_single_quote_ratio: float
    three_year_gain: float
    pitch_vocal: str


def calculate_business_roi(
    quotes_per_month: int = 10,
    avg_amount: float = 3200.0,
    loss_rate: float = 0.30,
    win_rate: float = 0.40,
    pack_price: float = 350.0,
    client_name: str = "Entreprise",
) -> ROICalculationResult:
    """
    Calcule les métriques de fuite de chiffre d'affaires et le retour sur investissement.
    """
    if quotes_per_month <= 0 or avg_amount <= 0 or pack_price <= 0:
        raise ValueError("Les valeurs d'entrée doivent être strictement positives.")

    # 1. Fuite mensuelle et annuelle
    forgotten_per_month = quotes_per_month * loss_rate
    recoverable_per_month = forgotten_per_month * win_rate
    recoverable_per_year = recoverable_per_month * 12.0

    monthly_lost_revenue = recoverable_per_month * avg_amount
    annual_lost_revenue = recoverable_per_year * avg_amount

    # 2. Amortissement et Payback
    # Combien de jours pour rentabiliser le pack ?
    daily_gain = (annual_lost_revenue / 365.0) if annual_lost_revenue > 0 else 1.0
    amortization_days = round(pack_price / daily_gain, 1)

    # Ratio de rentabilisation dès la première affaire sauvée
    single_quote_ratio = round(avg_amount / pack_price, 1)

    # Gain cumulé sur 3 ans (après coût du pack et abonnement de 60 €/m)
    cost_3_years = pack_price + (60.0 * 36.0)  # 350 + 2160 = 2510 €
    gross_gain_3_years = annual_lost_revenue * 3.0
    net_gain_3_years = gross_gain_3_years - cost_3_years

    # 3. Synthèse commerciale verbatim
    pitch = (
        f"« Monsieur {client_name}, faisons un calcul très simple ensemble : vous envoyez environ {quotes_per_month} offres "
        f"par mois avec un panier moyen de {avg_amount:,.0f} €. Faute de temps pour rappeler les clients le soir, "
        f"environ {int(loss_rate * 100)} % restent sans suite. Si mon système vous permet de ne récupérer ne serait-ce que "
        f"40 % de ces devis oubliés, cela représente {recoverable_per_year:,.1f} chantiers signés en plus par an, soit "
        f"{annual_lost_revenue:,.0f} € de chiffre d'affaires récupéré. Face à cela, mon installation à {pack_price:,.0f} € "
        f"est rentabilisée dès le premier devis sauvé en moins de {int(amortization_days)} jours. "
        f"On installe le système cette semaine ? »"
    )

    return {
        "client_name": client_name,
        "quotes_per_month": quotes_per_month,
        "avg_amount": avg_amount,
        "loss_rate": loss_rate,
        "win_rate": win_rate,
        "pack_price": pack_price,
        "forgotten_quotes_month": forgotten_per_month,
        "recoverable_quotes_year": recoverable_per_year,
        "monthly_loss_revenue": round(monthly_lost_revenue, 2),
        "annual_loss_revenue": round(annual_lost_revenue, 2),
        "amortization_days": amortization_days,
        "payback_single_quote_ratio": single_quote_ratio,
        "three_year_gain": round(net_gain_3_years, 2),
        "pitch_vocal": pitch,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Calculateur CLI de manque à gagner et ROI Bureau Numérique.")
    parser.add_argument("--client", "-c", default="Entreprise", help="Nom du client prospect")
    parser.add_argument("--quotes", "-q", type=int, default=10, help="Nombre de devis/offres envoyés par mois")
    parser.add_argument("--amount", "-a", type=float, default=3200.0, help="Panier moyen hors TVA d'une offre")
    parser.add_argument("--loss-rate", type=float, default=0.30, help="Taux estimé d'offres sans suite (défaut: 30%%)")
    parser.add_argument("--win-rate", type=float, default=0.40, help="Taux de signature des offres relancées (défaut: 40%%)")
    parser.add_argument("--pack", "-p", type=float, default=350.0, help="Prix du pack d'installation")

    args = parser.parse_args()

    res = calculate_business_roi(
        quotes_per_month=args.quotes,
        avg_amount=args.amount,
        loss_rate=args.loss_rate,
        win_rate=args.win_rate,
        pack_price=args.pack,
        client_name=args.client,
    )

    print("=" * 70)
    print(f"📊 DÉMONSTRATION FINANCIÈRE DE ROI — {res['client_name'].upper()}")
    print("=" * 70)
    print(f"Volume mensuel analysé       : {res['quotes_per_month']} offres/mois @ {res['avg_amount']:,.2f} € HTVA")
    print(f"Taux d'abandon constaté      : {int(res['loss_rate'] * 100)} % des offres oubliées faute de relance")
    print(f"Taux de conversion relance   : {int(res['win_rate'] * 100)} % de signature sur relance active\n")

    print("💸 COÛT DE L'INACTION (L'HÉMORRAGIE FINANCIÈRE) :")
    print(f"  • Offres récupérables par an : {res['recoverable_quotes_year']:,.1f} dossiers signés en plus")
    print(f"  • Perte de CA mensuelle      : {res['monthly_loss_revenue']:,.2f} € HTVA / mois")
    print(f"  • PERTE DE CA ANNUELLE BRUTE : {res['annual_loss_revenue']:,.2f} € HTVA / an\n")

    print(f"⚡ RENTABILITÉ DE L'INTERVENTION BUREAU NUMÉRIQUE ({res['pack_price']:,.2f} € HTVA) :")
    print(f"  • Délai d'amortissement net  : {res['amortization_days']} jours de travail")
    print(f"  • Multiplicateur 1er devis   : x{res['payback_single_quote_ratio']} (1 seul devis paye l'intervention {res['payback_single_quote_ratio']} fois)")
    print(f"  • Gain net cumulé sur 3 ans  : +{res['three_year_gain']:,.2f} € HTVA\n")

    print("-" * 70)
    print("🎙️ PITCH COMMERCIAL VERBATIM (À DIRE AU PROSPECT EN RENDEZ-VOUS) :")
    print(f"{res['pitch_vocal']}")
    print("=" * 70)


if __name__ == "__main__":
    main()
