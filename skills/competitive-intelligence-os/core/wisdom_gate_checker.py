"""
Module Wisdom Gate : Contrôleur déontologique, éthique et légal de l'information.
Applique les standards SCIP (Strategic and Competitive Intelligence Professionals).
Vérifie qu'aucune donnée non sourcée, illégale ou biaisée ne pollue l'analyse.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GateEvaluationResult:
    is_passed: bool
    status: str  # 'PASS' ou 'REJECTED'
    reasons: list[str]
    audit_notes: str


class WisdomGateChecker:
    """Filtre de validation des données selon les 5 serrous d'admissibilité."""

    MAX_TEMPORAL_VALIDITY_DAYS: int = 180

    @classmethod
    def evaluate(
        cls,
        source_url: str,
        source_author: str,
        source_voice: str,  # 'company', 'analyst', 'expert_humint', 'journalist'
        age_in_days: int,
        is_public_record: bool,
        is_independent: bool,
        respects_trade_secrets: bool,
    ) -> GateEvaluationResult:
        """
        Évalue une donnée collectée selon les 5 serrous éthiques et légaux :
        1. Provenance : URL ou registre légal vérifié.
        2. Indépendance : Absence de conflit d'intérêt évident.
        3. Validité temporelle : < 180 jours (sinon mention obsolescence requise).
        4. Admissibilité légale : Donnée publique, zéro hacking, zéro violation de NDA.
        5. Légitimité éthique : Conforme au code SCIP.
        """
        reasons: list[str] = []

        if not source_url or not source_url.startswith(("http://", "https://", "urn:")):
            reasons.append("Échec Provenance : L'URL ou l'identifiant légal (BCE/Infogreffe) est manquant ou invalide.")

        if not is_public_record:
            reasons.append("Échec Admissibilité Légale : La donnée n'est pas issue du domaine public ou d'une communication autorisée.")

        if not respects_trade_secrets:
            reasons.append("Échec Légitimité Éthique : Risque de violation du secret des affaires ou d'atteinte à la vie privée.")

        if age_in_days > cls.MAX_TEMPORAL_VALIDITY_DAYS:
            reasons.append(f"Alerte Temporalité : Donnée âgée de {age_in_days} jours (> 180 jours). Risque d'obsolescence tarifaire ou technique.")

        if not is_independent and source_voice == "analyst":
            reasons.append("Avertissement Indépendance : Rapport d'analyste susceptible d'être sponsorisé par le concurrent.")

        # Le test échoue formellement si la légalité ou la provenance est compromise
        critical_failure = not source_url or not is_public_record or not respects_trade_secrets

        if critical_failure:
            return GateEvaluationResult(
                is_passed=False,
                status="REJECTED",
                reasons=reasons,
                audit_notes="Donnée rejetée par le protocole Wisdom Gate. Ne doit pas alimenter la décision stratégique.",
            )

        return GateEvaluationResult(
            is_passed=True,
            status="PASS",
            reasons=reasons,
            audit_notes="Donnée validée pour intégration dans la mémoire SQLite et les battlecards.",
        )
