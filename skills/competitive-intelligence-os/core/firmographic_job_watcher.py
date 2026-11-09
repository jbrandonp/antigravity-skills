"""
Module de veille firmographique précoce (Inflexions à 6-12 mois).
Surveille les signaux opérationnels invisibles : offres d'emploi, dépôts légaux et baux.
Permet d'anticiper les virages stratégiques bien avant les communiqués de presse officiels.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class JobPostingSnapshot:
    competitor_id: str
    competitor_name: str
    engineering_postings: int
    sales_postings: int
    legal_compliance_postings: int
    executive_postings: int
    snapshot_quarter: str  # ex: '2026-Q1'


@dataclass(frozen=True)
class FirmographicInflexionAlert:
    competitor_name: str
    lead_time_months: int
    detected_trend: str
    strategic_intent_deduced: str
    threat_severity: str  # 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL'
    recommended_counter_measure: str


class FirmographicJobWatcher:
    """Détecteur d'inflexions stratégiques à partir des signaux d'embauches."""

    @classmethod
    def analyze_trajectory(
        cls,
        current: JobPostingSnapshot,
        previous: JobPostingSnapshot | None = None,
    ) -> list[FirmographicInflexionAlert]:
        """
        Compare les volumes de recrutement pour déduire les mouvements stratégiques à 6-12 mois.
        Inspiré de l'inflexion CoreWeave (75 -> 1336 jobs avant l'IPO).
        """
        alerts: list[FirmographicInflexionAlert] = []

        if previous is None:
            # Analyse statique si pas d'historique
            if current.engineering_postings > 20:
                alerts.append(
                    FirmographicInflexionAlert(
                        competitor_name=current.competitor_name,
                        lead_time_months=9,
                        detected_trend=f"Forte intensité R&D ({current.engineering_postings} postes ouverts)",
                        strategic_intent_deduced="Refonte majeure de l'architecture logicielle ou nouveau produit en préparation.",
                        threat_severity="HIGH",
                        recommended_counter_measure="Surveiller les dépôts de brevets et les changelogs bêta.",
                    )
                )
            return alerts

        # Calcul des deltas
        delta_eng = current.engineering_postings - previous.engineering_postings
        delta_sales = current.sales_postings - previous.sales_postings
        delta_legal = current.legal_compliance_postings - previous.legal_compliance_postings

        # 1. Virage Commercial Agressif (Sales-Led Growth)
        if delta_sales >= 5 and (delta_sales / max(1, previous.sales_postings)) >= 0.5:
            alerts.append(
                FirmographicInflexionAlert(
                    competitor_name=current.competitor_name,
                    lead_time_months=6,
                    detected_trend=f"Explosion des recrutements commerciaux (+{delta_sales} postes)",
                    strategic_intent_deduced="Virage vers le démarchage direct et la vente agressive par téléphone sur le terrain.",
                    threat_severity="HIGH",
                    recommended_counter_measure="Armer immédiatement nos équipes avec les Battlecards 8-Secondes pour contrer leur prospection.",
                )
            )

        # 2. Refonte Technique ou Intégration IA / Réglementaire
        if delta_eng >= 8:
            alerts.append(
                FirmographicInflexionAlert(
                    competitor_name=current.competitor_name,
                    lead_time_months=12,
                    detected_trend=f"Inflexion massive des embauches d'ingénieurs (+{delta_eng} postes)",
                    strategic_intent_deduced="Lancement d'une nouvelle génération de produit (ex: intégration IA ou mise en conformité Peppol 2026).",
                    threat_severity="CRITICAL",
                    recommended_counter_measure="Prendre de vitesse leur mise sur le marché en capitalisant sur notre architecture locale ultra-rapide.",
                )
            )

        # 3. Préparation Réglementaire ou Levée / M&A
        if delta_legal >= 2:
            alerts.append(
                FirmographicInflexionAlert(
                    competitor_name=current.competitor_name,
                    lead_time_months=6,
                    detected_trend=f"Recrutement de juristes et responsables conformité (+{delta_legal} postes)",
                    strategic_intent_deduced="Préparation d'une levée de fonds, d'une acquisition ou réponse à un durcissement réglementaire.",
                    threat_severity="MEDIUM",
                    recommended_counter_measure="Vérifier leurs dépôts d'actes et statuts auprès des registres légaux.",
                )
            )

        return alerts
