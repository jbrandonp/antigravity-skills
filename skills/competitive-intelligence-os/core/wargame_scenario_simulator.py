"""
Simulateur de War Gaming Multi-Tours.
Inspiré des méthodologies d'exercices de simulation appliquées chez Shell, IBM et Intel.
Permet de tester nos offensives et d'anticiper les réactions concurrentielles avant d'engager du budget.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class WarGameMove:
    actor: str  # "US" ou nom du concurrent
    turn_number: int
    action_type: str  # "PRICE_DROP", "NEW_FEATURE", "MARKETING_BLITZ", "REGULATORY_LEVER", "FREE_WEDGE"
    action_description: str
    expected_market_impact: str


@dataclass(frozen=True)
class WarGameSimulationResult:
    scenario_name: str
    turns: list[WarGameMove]
    strategic_blindspots_revealed: list[str]
    conditional_action_plans: list[str]
    equilibrium_verdict: str


class WarGameScenarioSimulator:
    """Simulateur tactique de confrontation concurrentielle multi-tours."""

    @classmethod
    def simulate_price_disruption(
        cls,
        competitor_name: str,
        price_drop_pct: float,
        is_competitor_public_or_pe_backed: bool,
    ) -> WarGameSimulationResult:
        """
        Simule une offensive de baisse de prix ou d'offre d'appel gratuite.
        Évalue si le concurrent peut s'aligner ou s'il est bloqué par ses contraintes d'actionnaires.
        """
        turns: list[WarGameMove] = [
            WarGameMove(
                actor="US",
                turn_number=1,
                action_type="FREE_WEDGE" if price_drop_pct >= 90 else "PRICE_DROP",
                action_description=f"Lancement d'une offre agressive à -{price_drop_pct}% avec modèle local sans abonnement captif.",
                expected_market_impact="Capture immédiate des indépendants et artisans sensibles au budget.",
            )
        ]

        # Réaction du concurrent au Tour 2
        if is_competitor_public_or_pe_backed:
            comp_reaction = (
                f"{competitor_name} ne peut PAS s'aligner sans détruire sa marge d'EBITDA exigée par ses fonds. "
                "Riposte par campagne de réassurance FUD (Fear, Uncertainty, Doubt) axée sur l'ancienneté et la sécurité."
            )
            turns.append(
                WarGameMove(
                    actor=competitor_name,
                    turn_number=2,
                    action_type="MARKETING_BLITZ",
                    action_description=comp_reaction,
                    expected_market_impact="Ralentissement temporaire de l'adoption chez les clients très conservateurs.",
                )
            )
        else:
            comp_reaction = (
                f"{competitor_name} tente un alignement partiel avec une remise spéciale première année sur engagement 24 mois."
            )
            turns.append(
                WarGameMove(
                    actor=competitor_name,
                    turn_number=2,
                    action_type="PRICE_DROP",
                    action_description="Offre de rétention agressive avec engagement de 2 ans caché.",
                    expected_market_impact="Verrouillage partiel de leurs clients existants.",
                )
            )

        # Notre contre-attaque au Tour 3
        turns.append(
            WarGameMove(
                actor="US",
                turn_number=3,
                action_type="REGULATORY_LEVER",
                action_description="Publication de la Battlecard 8-Secondes démontrant les coûts cachés de leur engagement de 2 ans.",
                expected_market_impact="Désamorçage de leur objection et accélération des migrations.",
            )
        )

        blindspots = [
            "Risque que le concurrent verrouille ses clients actuels par des contrats pluriannuels avant notre offensive.",
            "Nécessité absolue d'un convertisseur 1-clic pour empêcher la friction de migration.",
        ]

        plans = [
            "Plan A (Si le rival baisse ses prix) : Démontrer immédiatement le coût total de possession (TCO) sur 36 mois avec les frais d'options cachés.",
            "Plan B (Si le rival dénigre notre jeunesse) : Mettre en avant la souveraineté locale des données (fichiers SQLite locaux sur PC Windows, zéro risque de coupure cloud).",
        ]

        return WarGameSimulationResult(
            scenario_name=f"Offensive Tarifaire vs {competitor_name}",
            turns=turns,
            strategic_blindspots_revealed=blindspots,
            conditional_action_plans=plans,
            equilibrium_verdict="Victoire par contre-positionnement : le leader est incapable de répliquer sans cannibaliser ses marges.",
        )
