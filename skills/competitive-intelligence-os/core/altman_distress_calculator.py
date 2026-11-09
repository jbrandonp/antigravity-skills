"""
Calculateur de détresse financière selon l'Altman Z'-Score pour PME privées.
Permet d'analyser les bilans déposés à la Banque Nationale de Belgique (BNB) ou aux greffes légaux.
Identifie les concurrents au bord de la rupture pour préparer des stratégies de reprise ou de M&A prédateur.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FinancialBalanceSheetInput:
    total_assets_eur: float  # Total de l'actif
    working_capital_eur: float  # Fonds de roulement net (Actif circulant - Dettes CT)
    retained_earnings_eur: float  # Bénéfices non distribués / Réserves
    ebit_eur: float  # Résultat d'exploitation avant intérêts et impôts
    book_value_equity_eur: float  # Capitaux propres comptables
    total_liabilities_eur: float  # Dettes totales
    total_sales_revenue_eur: float  # Chiffre d'affaires


@dataclass(frozen=True)
class AltmanDistressScoreReport:
    z_score: float
    distress_zone: str  # 'DISTRESS', 'GREY', 'SAFE'
    bankruptcy_risk_12m_pct: float
    predatory_action_recommendation: str
    detailed_ratios: str


class AltmanDistressCalculator:
    """Calculateur de l'Altman Z'-Score pour entreprises non cotées."""

    @classmethod
    def calculate_z_prime(cls, data: FinancialBalanceSheetInput) -> AltmanDistressScoreReport:
        """
        Calcule le Z'-score d'Altman pour sociétés privées (formule standard 1983) :
        Z' = 0.717*X1 + 0.847*X2 + 3.107*X3 + 0.420*X4 + 0.998*X5
        """
        if data.total_assets_eur <= 0 or data.total_liabilities_eur <= 0:
            return AltmanDistressScoreReport(
                z_score=0.0,
                distress_zone="DISTRESS",
                bankruptcy_risk_12m_pct=95.0,
                predatory_action_recommendation="Données comptables anormales ou insolvabilité immédiate.",
                detailed_ratios="Actif ou passif nul ou négatif.",
            )

        x1 = data.working_capital_eur / data.total_assets_eur
        x2 = data.retained_earnings_eur / data.total_assets_eur
        x3 = data.ebit_eur / data.total_assets_eur
        x4 = data.book_value_equity_eur / data.total_liabilities_eur
        x5 = data.total_sales_revenue_eur / data.total_assets_eur

        z_prime = round(
            (0.717 * x1) + (0.847 * x2) + (3.107 * x3) + (0.420 * x4) + (0.998 * x5),
            2,
        )

        ratios_str = (
            f"X1 (Liquidité)={x1:.2f}, X2 (Réserves)={x2:.2f}, X3 (EBIT/Actif)={x3:.2f}, "
            f"X4 (Solvabilité)={x4:.2f}, X5 (Rotation CA)={x5:.2f}"
        )

        if z_prime < 1.23:
            zone = "DISTRESS"
            risk = 85.0
            recomm = (
                "ZONE DE DÉTRESSE FINANCIÈRE CRITIQUE : Le concurrent est au bord du défaut de paiement. "
                "Action recommandée : Ne pas dépenser d'argent en guerre commerciale contre lui. "
                "Préparer un courrier de proposition de rachat des actifs et de la base clients pour 1 € symbolique auprès du curateur."
            )
        elif z_prime <= 2.90:
            zone = "GREY"
            risk = 35.0
            recomm = (
                "ZONE GRISE : Santé financière fragile. Le concurrent est sous tension de trésorerie. "
                "Action recommandée : Accentuer la pression sur le Time-to-Value et les offres sans engagement."
            )
        else:
            zone = "SAFE"
            risk = 5.0
            recomm = (
                "ZONE SAINE : Le concurrent dispose d'un bilan solide et de réserves. "
                "Action recommandée : Éviter une guerre des prix frontale. Privilégier une stratégie de niche (Wedge Strategy)."
            )

        return AltmanDistressScoreReport(
            z_score=z_prime,
            distress_zone=zone,
            bankruptcy_risk_12m_pct=risk,
            predatory_action_recommendation=recomm,
            detailed_ratios=ratios_str,
        )
