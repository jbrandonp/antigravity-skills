"""
Indice Composite de Vulnérabilité à la Disruption Concurrentielle (Disruption Vulnerability Index - DVI).
Agrège 4 signaux précurseurs pour quantifier la fragilité structurelle d'un concurrent :
1. Inertie Technologique (Tech Inertia) : % de recrutements en maintenance legacy vs IA/Cloud.
2. Rigidité Tarifaire (Pricing Rigidity) : Opacité, engagement pluriannuel forcé, absence de libre-service.
3. Tension Financière (Financial Distress) : Dérivé de l'Altman Z-Score ou ratio d'endettement.
4. Friction Client (Customer Friction) : Taux de défection dans les deals et sentiment négatif.

Score DVI normalisé entre 0.0 et 100.0 (plus le score est élevé, plus le concurrent est vulnérable).
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ThreatClassification(str, Enum):
    COMMODITY_TRAP_COLLAPSE = "COMMODITY_TRAP_COLLAPSE"  # DVI >= 75
    VULNERABLE_INCUMBENT = "VULNERABLE_INCUMBENT"  # 55 <= DVI < 75
    BALANCED_COMPETITOR = "BALANCED_COMPETITOR"  # 35 <= DVI < 55
    AGGRESSIVE_SCALEUP = "AGGRESSIVE_SCALEUP"  # DVI < 35 et basse inertie
    FORTIFIED_HEGEMON = "FORTIFIED_HEGEMON"  # DVI < 35 et assise établie


@dataclass(frozen=True)
class DisruptionMetricInput:
    competitor_name: str
    tech_inertia_score: float  # 0.0 (très innovant) à 100.0 (legacy pur)
    pricing_rigidity_score: float  # 0.0 (usage transparent) à 100.0 (contrats opaques)
    financial_distress_score: float  # 0.0 (trésorerie pléthorique) à 100.0 (détresse)
    customer_friction_score: float  # 0.0 (clients fans) à 100.0 (colère active)


@dataclass(frozen=True)
class DisruptionAuditResult:
    competitor_name: str
    composite_dvi: float
    classification: ThreatClassification
    recommended_attack_vectors: list[str]
    strategic_rationale: str


class DisruptionRadarEngine:
    """Calculateur d'indice de vulnérabilité à la disruption concurrentielle."""

    WEIGHT_TECH: float = 0.30
    WEIGHT_PRICING: float = 0.25
    WEIGHT_FINANCE: float = 0.25
    WEIGHT_FRICTION: float = 0.20

    @classmethod
    def calculate_dvi(cls, metrics: DisruptionMetricInput) -> DisruptionAuditResult:
        """Calcule l'indice composite DVI et qualifie la vulnérabilité."""
        # Bornage de sécurité des 4 dimensions [0, 100]
        c_tech = max(0.0, min(100.0, metrics.tech_inertia_score))
        c_price = max(0.0, min(100.0, metrics.pricing_rigidity_score))
        c_fin = max(0.0, min(100.0, metrics.financial_distress_score))
        c_fric = max(0.0, min(100.0, metrics.customer_friction_score))

        # Calcul pondéré
        dvi = (
            cls.WEIGHT_TECH * c_tech
            + cls.WEIGHT_PRICING * c_price
            + cls.WEIGHT_FINANCE * c_fin
            + cls.WEIGHT_FRICTION * c_fric
        )
        dvi = round(dvi, 2)

        # Classification stratégique
        attack_vectors: list[str] = []
        if dvi >= 75.0:
            classification = ThreatClassification.COMMODITY_TRAP_COLLAPSE
            rationale = (
                f"{metrics.competitor_name} accumule une dette technologique critique, "
                f"des prix perçus comme abusifs et des bilans fragilisés. Risque de décrochage rapide."
            )
            attack_vectors.append("Lancer une campagne de migration vampire 1-clic avec reprise d'historique.")
            attack_vectors.append("Cibler les contrats à renouvellement sous 90 jours avec tarification à l'usage.")
            attack_vectors.append("Rassurer sur la pérennité financière et l'indépendance de notre plateforme.")
        elif dvi >= 55.0:
            classification = ThreatClassification.VULNERABLE_INCUMBENT
            rationale = (
                f"{metrics.competitor_name} dispose d'une base installée mais subit une érosion "
                f"liée à son manque d'agilité et à la friction client."
            )
            attack_vectors.append("Démontrer un Time-to-Value (TTV) 3x supérieur dès le PoC.")
            attack_vectors.append("Mettre en avant l'absence de frais cachés et le libre-service.")
        elif dvi >= 35.0:
            classification = ThreatClassification.BALANCED_COMPETITOR
            rationale = (
                f"{metrics.competitor_name} maintient un équilibre opérationnel moyen sans faiblesse flagrante."
            )
            attack_vectors.append("Attaquer sur la différenciation fonctionnelle pointue et le support local.")
        else:
            # DVI < 35.0
            if c_tech < 30.0:
                classification = ThreatClassification.AGGRESSIVE_SCALEUP
                rationale = (
                    f"{metrics.competitor_name} est un challenger agile à forte vélocité d'innovation. "
                    f"Surveiller de près son expansion."
                )
                attack_vectors.append("Verrouiller les comptes clés avec des engagements pluriannuels avantageux.")
                attack_vectors.append("Innover plus vite sur les fonctionnalités d'intégration critiques.")
            else:
                classification = ThreatClassification.FORTIFIED_HEGEMON
                rationale = (
                    f"{metrics.competitor_name} est un leader historique assis sur des réserves solides."
                )
                attack_vectors.append("Adopter une stratégie de contournement (marché de niche sous les radars).")
                attack_vectors.append("Éviter la guerre des prix frontale qui favoriserait sa trésorerie.")

        return DisruptionAuditResult(
            competitor_name=metrics.competitor_name,
            composite_dvi=dvi,
            classification=classification,
            recommended_attack_vectors=attack_vectors,
            strategic_rationale=rationale,
        )
