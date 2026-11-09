"""
Module d'aiguillage des questions décisionnelles (KIQ - Key Intelligence Questions).
Empêche l'utilisation aveugle de frameworks inadaptés (ex: Porter pour une perte de vente)
et associe chaque besoin décisionnel au bon outil analytique.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import ClassVar


class StrategicIntent(str, Enum):
    SECTOR_ATTRACTIVENESS = "sector_attractiveness"
    COMPETITIVE_POSITIONING = "competitive_positioning"
    STRATEGIC_GROUPS_WHITE_SPACES = "strategic_groups_white_spaces"
    WIN_LOSS_ANALYSIS = "win_loss_analysis"
    OPERATIONAL_BENCHMARKING = "operational_benchmarking"
    CONTINUOUS_SENTINEL = "continuous_sentinel"


@dataclass(frozen=True)
class FrameworkRoutingRecommendation:
    intent: StrategicIntent
    primary_framework: str
    secondary_framework: str
    expected_outcome: str
    required_data_sources: list[str]
    banned_frameworks_warning: str
    actionable_metric: str


class KIQRouter:
    """Aiguilleur de questions stratégiques vers les frameworks adéquats."""

    ROUTING_TABLE: ClassVar[dict[StrategicIntent, FrameworkRoutingRecommendation]] = {
        StrategicIntent.SECTOR_ATTRACTIVENESS: FrameworkRoutingRecommendation(
            intent=StrategicIntent.SECTOR_ATTRACTIVENESS,
            primary_framework="5 Forces de Porter (+1 Réglementaire)",
            secondary_framework="Analyse PESTEL Macro-Environnement",
            expected_outcome="Diagnostic de la profitabilité sectorielle et hauteur des barrières à l'entrée",
            required_data_sources=["Rapports sectoriels", "Directives européennes/locales", "Comptes BNB/BCE"],
            banned_frameworks_warning="Interdiction formelle d'utiliser la Win/Loss Analysis ou une Battlecard pour évaluer l'attractivité d'un secteur.",
            actionable_metric="Indice d'intensité concurrentielle (HHI) et marge brute moyenne de l'industrie",
        ),
        StrategicIntent.COMPETITIVE_POSITIONING: FrameworkRoutingRecommendation(
            intent=StrategicIntent.COMPETITIVE_POSITIONING,
            primary_framework="Carte de Positionnement Perceptuel (2 axes)",
            secondary_framework="Cartographie de Wardley (Chaîne de valeur vs Évolution)",
            expected_outcome="Visualisation du positionnement relatif sur les critères d'achat prioritaires",
            required_data_sources=["Sites web", "Grilles de prix", "Avis clients indépendants"],
            banned_frameworks_warning="Ne pas choisir d'axes flous comme 'Qualité vs Prix' où tout le monde se superpose.",
            actionable_metric="Distance euclidienne de différenciation par rapport aux rivaux",
        ),
        StrategicIntent.STRATEGIC_GROUPS_WHITE_SPACES: FrameworkRoutingRecommendation(
            intent=StrategicIntent.STRATEGIC_GROUPS_WHITE_SPACES,
            primary_framework="Groupes Stratégiques & Barrières à la Mobilité",
            secondary_framework="Matrice Océan Bleu (ERRAC - 4 Actions)",
            expected_outcome="Cartographie des clusters de rivaux et détection des espaces blancs non servis",
            required_data_sources=["Catalogue d'offres", "Bases de données d'entreprises", "Canaux de distribution"],
            banned_frameworks_warning="Éviter de traiter chaque concurrent isolément sans comprendre son cluster stratégique.",
            actionable_metric="Nombre d'espaces blancs viables identifiés avec barrières de mobilité modérées",
        ),
        StrategicIntent.WIN_LOSS_ANALYSIS: FrameworkRoutingRecommendation(
            intent=StrategicIntent.WIN_LOSS_ANALYSIS,
            primary_framework="Win/Loss Analysis Débiaisée (Entretien Acheteur)",
            secondary_framework="Forensics des Objections de Vente",
            expected_outcome="Identification des motifs réels de refus client (Time-to-Value, conformité) au-delà de l'alibi du prix",
            required_data_sources=["Entretiens post-décision à 30 jours", "Retours CRM acheteurs"],
            banned_frameworks_warning="INTERDICTION STRICTE DE PORTER OU DE SWOT : Porter ne dit pas pourquoi un prospect a refusé de signer hier !",
            actionable_metric="Taux de bascule et part des refus attribués aux vraies causes racines",
        ),
        StrategicIntent.OPERATIONAL_BENCHMARKING: FrameworkRoutingRecommendation(
            intent=StrategicIntent.OPERATIONAL_BENCHMARKING,
            primary_framework="Benchmarking Opérationnel d'Élite",
            secondary_framework="Calculateur TCO sur 12/36 mois",
            expected_outcome="Mesure précise des écarts opérationnels (Time-to-Value, CAC Payback, Churn, NRR)",
            required_data_sources=["Grilles tarifaires réelles", "Parcours d'onboarding", "Comptes de résultats"],
            banned_frameworks_warning="Ne pas comparer une simple liste de fonctionnalités coché/non-coché sans mesurer le résultat économique.",
            actionable_metric="Écart de Time-to-Value (en jours) et CAC Payback ajusté de la marge",
        ),
        StrategicIntent.CONTINUOUS_SENTINEL: FrameworkRoutingRecommendation(
            intent=StrategicIntent.CONTINUOUS_SENTINEL,
            primary_framework="Système de Veille Permanente à 3 Niveaux",
            secondary_framework="Battlecards Vivantes 'Règle des 8 Secondes'",
            expected_outcome="Flux continu d'alertes firmographiques et fiches d'objections pour les équipes de vente",
            required_data_sources=["Offres d'emploi", "Brevets/Marques EUIPO", "Pages tarifs horodatées"],
            banned_frameworks_warning="Ne pas produire de rapport statique annuel : la veille doit vivre au quotidien.",
            actionable_metric="Temps de réaction à un mouvement concurrentiel (visé : < 48 heures)",
        ),
    }

    @classmethod
    def route_question(cls, user_query: str) -> FrameworkRoutingRecommendation:
        """Détecte l'intention stratégique sous-jacente et retourne la recommandation de framework."""
        query_lower = user_query.lower()

        if any(w in query_lower for w in ["secteur", "industrie", "rentable", "attractif", "marché global"]):
            return cls.ROUTING_TABLE[StrategicIntent.SECTOR_ATTRACTIVENESS]

        if any(w in query_lower for w in ["perd", "perte", "deal", "win/loss", "refus", "pourquoi ils achètent"]):
            return cls.ROUTING_TABLE[StrategicIntent.WIN_LOSS_ANALYSIS]

        if any(w in query_lower for w in ["espace blanc", "groupe", "cluster", "niche vide", "océan bleu"]):
            return cls.ROUTING_TABLE[StrategicIntent.STRATEGIC_GROUPS_WHITE_SPACES]

        if any(w in query_lower for w in ["benchmarking", "time-to-value", "cac", "churn", "nrr", "vitesse", "onboarding"]):
            return cls.ROUTING_TABLE[StrategicIntent.OPERATIONAL_BENCHMARKING]

        if any(w in query_lower for w in ["veille", "alerte", "battlecard", "suivre", "sentinelle", "quotidien"]):
            return cls.ROUTING_TABLE[StrategicIntent.CONTINUOUS_SENTINEL]

        # Par défaut : positionnement relatif
        return cls.ROUTING_TABLE[StrategicIntent.COMPETITIVE_POSITIONING]
