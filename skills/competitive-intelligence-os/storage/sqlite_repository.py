"""
Module de persistance SQLite pour le système Competitive Intelligence OS.
Gère les transactions, les contraintes relationnelles et l'historisation des audits.
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class CompetitorRecord:
    id: str
    legal_name: str
    brand_name: str
    website: str
    circle: str  # 'direct', 'indirect', 'substitute'
    surveillance_tier: str  # 'tight', 'substantial', 'broad'
    country: str
    company_registration: str | None = None
    altman_z_score: float | None = None
    financial_status: str = "healthy"


@dataclass(frozen=True)
class PricingTierRecord:
    id: str
    competitor_id: str
    tier_name: str
    price_eur: float
    billing_period: str  # 'monthly', 'annual'
    value_metric: str  # 'per_user', 'flat', 'per_invoice', 'usage_based'
    setup_fee_eur: float
    is_active: bool
    last_verified_at: str


@dataclass(frozen=True)
class WisdomGateRecord:
    record_id: str
    competitor_id: str
    data_type: str
    source_url: str
    source_author: str
    source_voice: str  # 'company', 'analyst', 'expert_humint', 'journalist'
    provenance_verified: bool
    independence_verified: bool
    temporal_validity_days: int
    legal_admissibility: bool
    ethical_legitimacy: bool
    gate_status: str  # 'PASS', 'REJECTED'


class SQLiteRepository:
    def __init__(self, db_path: Path) -> None:
        """Initialise le gestionnaire SQLite et applique le schéma si nécessaire."""
        self.db_path = db_path
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def _execute(self, query: str, params: tuple[object, ...] = ()) -> None:
        """Exécute une commande d'écriture et ferme la connexion."""
        conn = self._get_connection()
        try:
            with conn:
                conn.execute(query, params)
        finally:
            conn.close()

    def _executescript(self, script: str) -> None:
        """Exécute un script SQL et ferme la connexion."""
        conn = self._get_connection()
        try:
            with conn:
                conn.executescript(script)
        finally:
            conn.close()

    def _init_db(self) -> None:
        """Charge et applique le fichier schema.sql."""
        schema_path = Path(__file__).parent / "schema.sql"
        if schema_path.exists():
            schema_content = schema_path.read_text(encoding="utf-8")
            self._executescript(schema_content)

    def upsert_competitor(self, record: CompetitorRecord) -> None:
        """Insère ou met à jour un concurrent dans la base de données."""
        query = """
            INSERT INTO competitors (
                id, legal_name, brand_name, website, circle,
                surveillance_tier, country, company_registration,
                altman_z_score, financial_status, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(id) DO UPDATE SET
                legal_name = excluded.legal_name,
                brand_name = excluded.brand_name,
                website = excluded.website,
                circle = excluded.circle,
                surveillance_tier = excluded.surveillance_tier,
                country = excluded.country,
                company_registration = excluded.company_registration,
                altman_z_score = excluded.altman_z_score,
                financial_status = excluded.financial_status,
                updated_at = CURRENT_TIMESTAMP;
        """
        self._execute(
            query,
            (
                record.id,
                record.legal_name,
                record.brand_name,
                record.website,
                record.circle,
                record.surveillance_tier,
                record.country,
                record.company_registration,
                record.altman_z_score,
                record.financial_status,
            ),
        )

    def get_competitor(self, competitor_id: str) -> CompetitorRecord | None:
        """Récupère un concurrent par son identifiant."""
        conn = self._get_connection()
        try:
            cursor = conn.execute(
                "SELECT * FROM competitors WHERE id = ?;", (competitor_id,)
            )
            row = cursor.fetchone()
            if row is None:
                return None
            return CompetitorRecord(
                id=str(row["id"]),
                legal_name=str(row["legal_name"]),
                brand_name=str(row["brand_name"]),
                website=str(row["website"]),
                circle=str(row["circle"]),
                surveillance_tier=str(row["surveillance_tier"]),
                country=str(row["country"]),
                company_registration=row["company_registration"],
                altman_z_score=row["altman_z_score"],
                financial_status=str(row["financial_status"]),
            )
        finally:
            conn.close()

    def list_competitors(self) -> list[CompetitorRecord]:
        """Liste l'ensemble des concurrents enregistrés."""
        conn = self._get_connection()
        try:
            cursor = conn.execute(
                "SELECT * FROM competitors ORDER BY created_at ASC;"
            )
            records: list[CompetitorRecord] = []
            for row in cursor.fetchall():
                records.append(
                    CompetitorRecord(
                        id=str(row["id"]),
                        legal_name=str(row["legal_name"]),
                        brand_name=str(row["brand_name"]),
                        website=str(row["website"]),
                        circle=str(row["circle"]),
                        surveillance_tier=str(row["surveillance_tier"]),
                        country=str(row["country"]),
                        company_registration=row["company_registration"],
                        altman_z_score=row["altman_z_score"],
                        financial_status=str(row["financial_status"]),
                    )
                )
            return records
        finally:
            conn.close()

    def upsert_pricing_tier(self, tier: PricingTierRecord) -> None:
        """Insère ou met à jour un palier tarifaire, déclenchant l'audit en cas de changement de prix."""
        query = """
            INSERT INTO pricing_tiers (
                id, competitor_id, tier_name, price_eur,
                billing_period, value_metric, setup_fee_eur,
                is_active, last_verified_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                tier_name = excluded.tier_name,
                price_eur = excluded.price_eur,
                billing_period = excluded.billing_period,
                value_metric = excluded.value_metric,
                setup_fee_eur = excluded.setup_fee_eur,
                is_active = excluded.is_active,
                last_verified_at = excluded.last_verified_at;
        """
        self._execute(
            query,
            (
                tier.id,
                tier.competitor_id,
                tier.tier_name,
                tier.price_eur,
                tier.billing_period,
                tier.value_metric,
                tier.setup_fee_eur,
                1 if tier.is_active else 0,
                tier.last_verified_at,
            ),
        )

    def get_pricing_tiers(self, competitor_id: str) -> list[PricingTierRecord]:
        """Récupère les tarifs actifs d'un concurrent ordonnés par prix."""
        conn = self._get_connection()
        try:
            cursor = conn.execute(
                """
                SELECT * FROM pricing_tiers
                WHERE competitor_id = ? AND is_active = 1
                ORDER BY price_eur ASC;
                """,
                (competitor_id,),
            )
            tiers: list[PricingTierRecord] = []
            for row in cursor.fetchall():
                tiers.append(
                    PricingTierRecord(
                        id=str(row["id"]),
                        competitor_id=str(row["competitor_id"]),
                        tier_name=str(row["tier_name"]),
                        price_eur=float(row["price_eur"]),
                        billing_period=str(row["billing_period"]),
                        value_metric=str(row["value_metric"]),
                        setup_fee_eur=float(row["setup_fee_eur"]),
                        is_active=bool(row["is_active"]),
                        last_verified_at=str(row["last_verified_at"]),
                    )
                )
            return tiers
        finally:
            conn.close()

    def record_wisdom_gate(self, gate: WisdomGateRecord) -> None:
        """Enregistre le passage d'une donnée au filtre éthique et légal Wisdom Gate."""
        query = """
            INSERT INTO wisdom_gate_records (
                record_id, competitor_id, data_type, source_url,
                source_author, source_voice, provenance_verified,
                independence_verified, temporal_validity_days,
                legal_admissibility, ethical_legitimacy, gate_status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        self._execute(
            query,
            (
                gate.record_id,
                gate.competitor_id,
                gate.data_type,
                gate.source_url,
                gate.source_author,
                gate.source_voice,
                1 if gate.provenance_verified else 0,
                1 if gate.independence_verified else 0,
                gate.temporal_validity_days,
                1 if gate.legal_admissibility else 0,
                1 if gate.ethical_legitimacy else 0,
                gate.gate_status,
            ),
        )

    def get_price_audit_history(self, competitor_id: str) -> list[dict[str, object]]:
        """Récupère l'historique complet des variations de prix d'un concurrent."""
        conn = self._get_connection()
        try:
            cursor = conn.execute(
                """
                SELECT * FROM price_audit_events
                WHERE competitor_id = ?
                ORDER BY detected_at DESC;
                """,
                (competitor_id,),
            )
            return [dict(row) for row in cursor.fetchall()]
        finally:
            conn.close()
