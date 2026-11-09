"""
Moteur stochastique : Chaîne de Markov pour le Churn, Modèle de Frank Bass et Indice HHI.
Permet d'estimer avec rigueur la vitesse de capture de parts de marché et la concentration sectorielle.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class BassDiffusionForecast:
    quarter: int
    new_adopters: int
    cumulative_market_share_pct: float


class StochasticMarketEngine:
    """Moteur de modélisation stochastique et de dynamique des marchés."""

    @staticmethod
    def calculate_hhi(market_shares_pct: list[float]) -> float:
        """
        Calcule l'indice de concentration de Herfindahl-Hirschman (HHI) :
        HHI = Somme des parts de marché (en %) au carré.
        - HHI < 1500 : Marché compétitif / fragmenté.
        - 1500 <= HHI <= 2500 : Concentration modérée.
        - HHI > 2500 : Marché oligopolistique / concentré.
        """
        return round(sum(s ** 2 for s in market_shares_pct), 1)

    @staticmethod
    def calculate_markov_churn_transition(
        price_delta_ratio: float,  # ex: 0.8 si nous sommes 20% moins chers
        pain_score: float,  # de 0.0 à 1.0 (mesure du mécontentement envers le concurrent)
        switching_friction: float,  # de 0.0 à 1.0 (difficulté de transfert de données)
    ) -> float:
        """
        Calcule la probabilité de transition stochastique d'un client rival vers notre offre :
        P(switch) = 1 / (1 + exp(-(beta0 + beta1*(1-price_delta) + beta2*pain - beta3*friction)))
        """
        # Poids calibrés d'après les benchmarks B2B
        beta_price = 2.5
        beta_pain = 3.2
        beta_friction = 4.0

        utility = (
            (beta_price * (1.0 - price_delta_ratio))
            + (beta_pain * pain_score)
            - (beta_friction * switching_friction)
        )

        # Protection contre l'OverflowError sur math.exp
        clamped_utility = max(-50.0, min(50.0, utility))
        p_switch = 1.0 / (1.0 + math.exp(-clamped_utility))
        return round(p_switch, 3)

    @staticmethod
    def forecast_bass_diffusion(
        market_size_total: int,
        p_innovation: float = 0.03,  # Coefficient d'innovation (marketing direct)
        q_imitation: float = 0.38,  # Coefficient d'imitation (bouche-à-oreille entre pairs)
        quarters: int = 8,
    ) -> list[BassDiffusionForecast]:
        """
        Résout l'équation de Frank Bass pour projeter la courbe d'adoption sur N trimestres :
        S(t) = [p + q * F(t-1)] * [1 - F(t-1)]
        """
        results: list[BassDiffusionForecast] = []
        cumulative_share = 0.0

        for t in range(1, quarters + 1):
            adoption_rate = (p_innovation + q_imitation * cumulative_share) * (1.0 - cumulative_share)
            new_adopters = round(adoption_rate * market_size_total)
            cumulative_share = min(1.0, cumulative_share + adoption_rate)

            results.append(
                BassDiffusionForecast(
                    quarter=t,
                    new_adopters=new_adopters,
                    cumulative_market_share_pct=round(cumulative_share * 100.0, 1),
                )
            )

        return results
