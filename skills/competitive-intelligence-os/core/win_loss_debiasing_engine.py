"""
Moteur d'autopsie Win/Loss débiaisée.
Corrige le biais documenté selon lequel les commerciaux attribuent 40 à 60% des pertes au 'prix'.
Reclasse les causes racines réelles auprès des acheteurs : Time-to-Value, conformité, ergonomie, support.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar


@dataclass(frozen=True)
class DealLossInterview:
    deal_id: str
    deal_name: str
    reported_sales_reason: str  # ex: "trop cher", "remise refusée"
    buyer_verbatim: str  # Ce que l'acheteur a réellement dit en entretien confidentiel
    deal_value_eur: float


@dataclass(frozen=True)
class ReclassifiedRootCause:
    deal_id: str
    stated_sales_reason: str
    true_root_cause: str  # 'time_to_value', 'compliance_security', 'feature_gap', 'support_human', 'pricing_unclear'
    confidence_score: float
    analysis_explanation: str


@dataclass(frozen=True)
class WinLossDebiasingReport:
    total_deals_analyzed: int
    sales_price_blame_pct: float  # Pourcentage où le commercial a accusé le prix
    actual_price_blame_pct: float  # Pourcentage réel où le prix était la vraie cause
    bias_inflation_delta_pct: float  # Écart de surévaluation du prix par l'équipe de vente
    root_cause_distribution: dict[str, float]
    primary_real_bottleneck: str
    recommended_product_action: str


class WinLossDebiasingEngine:
    """Moteur de requalification des motifs de perte d'affaires."""

    ROOT_CAUSE_KEYWORDS: ClassVar[dict[str, list[str]]] = {
        "time_to_value": ["long", "délai", "mise en place", "déploiement", "onboarding", "semaines", "retard", "lent"],
        "compliance_security": ["peppol", "rgpd", "tva 6%", "certification", "soc 2", "juridique", "légal", "norme", "sécurité", "ubl"],
        "feature_gap": ["manque", "impossible de", "fonctionnalité", "pas d'export", "incompatible", "option absente"],
        "support_human": ["injoignable", "téléphone", "robot", "ticket sans réponse", "personne", "support", "aide"],
        "pricing_unclear": ["frais cachés", "surprise", "engagement", "complexe", "astérisque", "devis flou"],
    }

    @classmethod
    def reclassify_deal(cls, interview: DealLossInterview) -> ReclassifiedRootCause:
        """Reclasse un deal en analysant le verbatim de l'acheteur pour isoler la cause racine."""
        text = interview.buyer_verbatim.lower()

        matched_causes: dict[str, int] = {}
        for cause, keywords in cls.ROOT_CAUSE_KEYWORDS.items():
            count = sum(1 for kw in keywords if kw in text)
            if count > 0:
                matched_causes[cause] = count

        if matched_causes:
            # Sélectionne la cause avec le plus d'occurrences
            best_cause = max(matched_causes, key=lambda k: matched_causes[k])
            confidence = min(1.0, 0.6 + (matched_causes[best_cause] * 0.15))
            return ReclassifiedRootCause(
                deal_id=interview.deal_id,
                stated_sales_reason=interview.reported_sales_reason,
                true_root_cause=best_cause,
                confidence_score=round(confidence, 2),
                analysis_explanation=f"Requalifié en '{best_cause}' suite aux mots-clés de l'acheteur ({matched_causes[best_cause]} occurrences).",
            )

        # Si aucune cause opérationnelle n'est trouvée et que le commercial disait prix, on vérifie
        if "cher" in text or "budget" in text or "prix" in text:
            return ReclassifiedRootCause(
                deal_id=interview.deal_id,
                stated_sales_reason=interview.reported_sales_reason,
                true_root_cause="true_price_sensitivity",
                confidence_score=0.85,
                analysis_explanation="Validé comme réelle sensibilité au prix confirmée par l'acheteur.",
            )

        return ReclassifiedRootCause(
            deal_id=interview.deal_id,
            stated_sales_reason=interview.reported_sales_reason,
            true_root_cause="brand_risk",
            confidence_score=0.50,
            analysis_explanation="Manque de réassurance globale ou notoriété perçue.",
        )

    @classmethod
    def analyze_portfolio(cls, interviews: list[DealLossInterview]) -> WinLossDebiasingReport:
        """Analyse un ensemble d'entretiens post-décision et mesure l'inflation du biais prix."""
        if not interviews:
            return WinLossDebiasingReport(
                total_deals_analyzed=0,
                sales_price_blame_pct=0.0,
                actual_price_blame_pct=0.0,
                bias_inflation_delta_pct=0.0,
                root_cause_distribution={},
                primary_real_bottleneck="Aucune donnée",
                recommended_product_action="Collecter des entretiens acheteurs à 30 jours.",
            )

        sales_price_count = sum(
            1 for i in interviews if any(w in i.reported_sales_reason.lower() for w in ["prix", "cher", "tarif", "remise", "budget"])
        )

        reclassified_causes: list[str] = []
        for i in interviews:
            result = cls.reclassify_deal(i)
            reclassified_causes.append(result.true_root_cause)

        total = len(interviews)
        sales_price_pct = round((sales_price_count / total) * 100.0, 1)

        actual_price_count = reclassified_causes.count("true_price_sensitivity")
        actual_price_pct = round((actual_price_count / total) * 100.0, 1)

        distribution: dict[str, float] = {}
        for cause in set(reclassified_causes):
            distribution[cause] = round((reclassified_causes.count(cause) / total) * 100.0, 1)

        # Biais d'inflation
        delta_pct = round(sales_price_pct - actual_price_pct, 1)

        # Bottleneck principal hors prix
        non_price_causes = {k: v for k, v in distribution.items() if k != "true_price_sensitivity"}
        primary_bottleneck = max(non_price_causes, key=lambda k: non_price_causes[k]) if non_price_causes else "Prix réel"

        actions: dict[str, str] = {
            "time_to_value": "Réduire le délai de mise en œuvre : refondre l'onboarding de 12 étapes à 5 pour garantir une première facture en < 48h.",
            "compliance_security": "Combler le vide réglementaire : intégrer nativement Peppol 2026, l'attestation TVA 6% et afficher les garanties de conformité.",
            "feature_gap": "Prioriser dans la roadmap la fonctionnalité bloquante identifiée dans les entretiens.",
            "support_human": "Mettre en avant l'assistance téléphonique en direct pour rassurer face aux concurrents 100% automatisés.",
            "pricing_unclear": "Simplifier la grille tarifaire : éliminer les frais de dossier cachés et passer au sans engagement.",
        }

        return WinLossDebiasingReport(
            total_deals_analyzed=total,
            sales_price_blame_pct=sales_price_pct,
            actual_price_blame_pct=actual_price_pct,
            bias_inflation_delta_pct=delta_pct,
            root_cause_distribution=distribution,
            primary_real_bottleneck=primary_bottleneck,
            recommended_product_action=actions.get(primary_bottleneck, "Auditer le parcours d'achat."),
        )
