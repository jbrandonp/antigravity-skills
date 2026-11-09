"""
Sentinelle de veille tarifaire cryptographique (SHA-256).
Surveille les empreintes numériques des pages de prix et des CGV des concurrents.
Déclenche une alerte tactique dès qu'une modification de tarif ou de condition est détectée.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass


@dataclass(frozen=True)
class PriceSnapshotCheck:
    competitor_id: str
    target_url: str
    current_content: str
    last_known_hash: str | None = None


@dataclass(frozen=True)
class PriceWatcherAlert:
    competitor_id: str
    target_url: str
    has_changed: bool
    old_hash: str
    new_hash: str
    alert_message: str


class PriceWatcherSentinel:
    """Vigie cryptographique légère fonctionnant en tâche d'arrière-plan."""

    @staticmethod
    def compute_sha256(content: str) -> str:
        """Calcule le hash cryptographique SHA-256 du contenu de l'offre."""
        return hashlib.sha256(content.strip().encode("utf-8")).hexdigest()

    @classmethod
    def check_for_modifications(cls, snapshot: PriceSnapshotCheck) -> PriceWatcherAlert:
        """Compare l'empreinte actuelle à l'ancienne pour détecter les changements silencieux."""
        new_hash = cls.compute_sha256(snapshot.current_content)
        old_hash = snapshot.last_known_hash or ""

        if not old_hash:
            return PriceWatcherAlert(
                competitor_id=snapshot.competitor_id,
                target_url=snapshot.target_url,
                has_changed=False,
                old_hash=new_hash,
                new_hash=new_hash,
                alert_message="Première initialisation de l'empreinte cryptographique enregistrée.",
            )

        if new_hash != old_hash:
            return PriceWatcherAlert(
                competitor_id=snapshot.competitor_id,
                target_url=snapshot.target_url,
                has_changed=True,
                old_hash=old_hash,
                new_hash=new_hash,
                alert_message=(
                    f"🚨 ALERTE TACTIQUE : Modification détectée sur la page {snapshot.target_url}. "
                    "Un changement de prix, d'option ou de condition générale a été publié."
                ),
            )

        return PriceWatcherAlert(
            competitor_id=snapshot.competitor_id,
            target_url=snapshot.target_url,
            has_changed=False,
            old_hash=old_hash,
            new_hash=new_hash,
            alert_message="Aucun changement détecté : la grille tarifaire est stable.",
        )
