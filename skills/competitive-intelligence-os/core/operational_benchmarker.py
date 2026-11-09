"""
Module de Benchmarking Opérationnel d'Élite.
Ne compare pas de simples cases à cocher, mais des résultats opérationnels mesurés :
Time-to-Value (TTV), CAC Payback ajusté de la marge brute, Churn et NRR.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class OperationalMetrics:
    entity_name: str
    time_to_value_days: int  # Délai moyen pour que l'utilisateur obtienne son premier ROI
    cac_eur: float  # Coût d'Acquisition Client
    monthly_arpu_eur: float  # Revenu Moyen par Utilisateur par mois
    gross_margin_pct: float  # Marge brute (ex: 80% = 0.80)
    annual_churn_pct: float  # Taux d'attrition annuel (ex: 12% = 0.12)
    nrr_pct: float  # Rétention Nette des Revenus (ex: 110% = 1.10)


@dataclass(frozen=True)
class OperationalGapAnalysis:
    ttv_gap_days: int
    ttv_retention_multiplier: float  # Un TTV < 30j retient x fois plus
    cac_payback_months_us: float
    cac_payback_months_them: float
    churn_gap_pct: float
    critical_priority_gap: str
    action_plan_summary: str


class OperationalBenchmarker:
    """Moteur d'évaluation et de comparaison des métriques d'exploitation réelles."""

    @classmethod
    def calculate_cac_payback(cls, cac_eur: float, arpu_eur: float, margin_pct: float) -> float:
        """
        Calcule le délai de récupération du CAC ajusté de la marge brute :
        Payback (mois) = CAC / (ARPU mensuel * Marge brute)
        """
        monthly_margin = arpu_eur * margin_pct
        if monthly_margin <= 0:
            return 999.0
        return round(cac_eur / monthly_margin, 1)

    @classmethod
    def compare(cls, us: OperationalMetrics, competitor: OperationalMetrics) -> OperationalGapAnalysis:
        """Compare nos performances opérationnelles à celles du meilleur concurrent."""
        ttv_gap = us.time_to_value_days - competitor.time_to_value_days

        # Ratio de rétention empirique documenté : atteindre le ROI en < 30j retient 2,1x plus
        retention_mult = 2.1 if competitor.time_to_value_days <= 30 and us.time_to_value_days > 30 else 1.0

        payback_us = cls.calculate_cac_payback(us.cac_eur, us.monthly_arpu_eur, us.gross_margin_pct)
        payback_them = cls.calculate_cac_payback(competitor.cac_eur, competitor.monthly_arpu_eur, competitor.gross_margin_pct)

        churn_gap = round((us.annual_churn_pct - competitor.annual_churn_pct) * 100.0, 1)

        # Détermination de l'écart critique à traiter d'urgence
        if ttv_gap > 10:
            critical_gap = f"Time-to-Value défavorable (+{ttv_gap} jours)"
            action = f"Urgente refonte de l'onboarding pour passer de {us.time_to_value_days} jours à moins de {competitor.time_to_value_days} jours."
        elif payback_us > payback_them + 6:
            critical_gap = f"Payback CAC trop lent ({payback_us} mois vs {payback_them} mois)"
            action = "Optimiser les canaux d'acquisition organique ou augmenter le panier initial avec des forfaits annuels."
        elif churn_gap > 3.0:
            critical_gap = f"Sur-attrition annuelle (+{churn_gap}%)"
            action = "Mettre en place des alertes proactives sur la baisse d'usage logiciel et renforcer le support."
        else:
            critical_gap = "Parité opérationnelle ou avantage global"
            action = "Maintenir l'avance opérationnelle et accentuer la pression sur l'acquisition."

        return OperationalGapAnalysis(
            ttv_gap_days=ttv_gap,
            ttv_retention_multiplier=retention_mult,
            cac_payback_months_us=payback_us,
            cac_payback_months_them=payback_them,
            churn_gap_pct=churn_gap,
            critical_priority_gap=critical_gap,
            action_plan_summary=action,
        )
