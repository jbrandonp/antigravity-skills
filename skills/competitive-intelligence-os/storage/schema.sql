-- ==============================================================================
-- Schema SQL : competitive-intelligence-os (Event Sourcing & SQLite Strict Mode)
-- ==============================================================================

PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;

-- 1. Table des concurrents cibles (4 à 5 cibles prioritaires selon les 3 cercles)
CREATE TABLE IF NOT EXISTS competitors (
    id TEXT PRIMARY KEY,
    legal_name TEXT NOT NULL,
    brand_name TEXT NOT NULL,
    website TEXT NOT NULL,
    circle TEXT NOT NULL CHECK(circle IN ('direct', 'indirect', 'substitute')),
    surveillance_tier TEXT NOT NULL CHECK(surveillance_tier IN ('tight', 'substantial', 'broad')),
    country TEXT NOT NULL CHECK(length(country) = 2),
    company_registration TEXT, -- BCE en Belgique, SIREN en France
    altman_z_score REAL DEFAULT NULL,
    financial_status TEXT DEFAULT 'healthy' CHECK(financial_status IN ('healthy', 'warning', 'distress', 'liquidation')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Paliers tarifaires actuels
CREATE TABLE IF NOT EXISTS pricing_tiers (
    id TEXT PRIMARY KEY,
    competitor_id TEXT NOT NULL REFERENCES competitors(id) ON DELETE CASCADE,
    tier_name TEXT NOT NULL,
    price_eur REAL NOT NULL CHECK(price_eur >= 0.0),
    billing_period TEXT NOT NULL CHECK(billing_period IN ('monthly', 'annual')),
    value_metric TEXT NOT NULL CHECK(value_metric IN ('per_user', 'flat', 'per_invoice', 'usage_based')),
    setup_fee_eur REAL DEFAULT 0.0 CHECK(setup_fee_eur >= 0.0),
    is_active INTEGER DEFAULT 1 CHECK(is_active IN (0, 1)),
    last_verified_at TIMESTAMP NOT NULL
);

-- 3. Historique d'audit des prix (Event Sourcing immuable via Trigger)
CREATE TABLE IF NOT EXISTS price_audit_events (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    tier_id TEXT NOT NULL,
    competitor_id TEXT NOT NULL,
    old_price_eur REAL,
    new_price_eur REAL NOT NULL,
    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    proof_url TEXT NOT NULL,
    raw_payload_hash TEXT NOT NULL
);

CREATE TRIGGER IF NOT EXISTS trg_audit_price_change
AFTER UPDATE OF price_eur ON pricing_tiers
BEGIN
    INSERT INTO price_audit_events (tier_id, competitor_id, old_price_eur, new_price_eur, proof_url, raw_payload_hash)
    VALUES (OLD.id, OLD.competitor_id, OLD.price_eur, NEW.price_eur, 'auto_sentinel_snapshot', 'verified_hash');
END;

-- 4. Registre de conformité et traçabilité Wisdom Gate
CREATE TABLE IF NOT EXISTS wisdom_gate_records (
    record_id TEXT PRIMARY KEY,
    competitor_id TEXT NOT NULL REFERENCES competitors(id) ON DELETE CASCADE,
    data_type TEXT NOT NULL, -- 'pricing', 'firmographic', 'feature', 'review'
    source_url TEXT NOT NULL,
    source_author TEXT NOT NULL,
    source_voice TEXT NOT NULL CHECK(source_voice IN ('company', 'analyst', 'expert_humint', 'journalist')),
    provenance_verified INTEGER NOT NULL CHECK(provenance_verified IN (0, 1)),
    independence_verified INTEGER NOT NULL CHECK(independence_verified IN (0, 1)),
    temporal_validity_days INTEGER NOT NULL,
    legal_admissibility INTEGER NOT NULL CHECK(legal_admissibility IN (0, 1)),
    ethical_legitimacy INTEGER NOT NULL CHECK(ethical_legitimacy IN (0, 1)),
    gate_status TEXT NOT NULL CHECK(gate_status IN ('PASS', 'REJECTED')),
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. Entretiens et autopsies Win/Loss débiaisées
CREATE TABLE IF NOT EXISTS win_loss_interviews (
    id TEXT PRIMARY KEY,
    deal_name TEXT NOT NULL,
    competitor_id TEXT NOT NULL REFERENCES competitors(id) ON DELETE CASCADE,
    deal_outcome TEXT NOT NULL CHECK(deal_outcome IN ('won', 'lost', 'no_decision')),
    deal_value_eur REAL NOT NULL,
    interview_date DATE NOT NULL,
    interviewer_type TEXT NOT NULL CHECK(interviewer_type IN ('third_party', 'neutral_internal')),
    reported_sales_reason TEXT NOT NULL, -- Souvent le faux motif "prix"
    true_root_cause TEXT NOT NULL CHECK(true_root_cause IN ('time_to_value', 'compliance_security', 'feature_gap', 'support_human', 'pricing_unclear', 'brand_risk')),
    buyer_verbatim TEXT NOT NULL,
    action_item TEXT NOT NULL
);

-- 6. Signaux firmographiques d'inflexion précoce (Offres d'emploi, baux, statuts)
CREATE TABLE IF NOT EXISTS firmographic_signals (
    id TEXT PRIMARY KEY,
    competitor_id TEXT NOT NULL REFERENCES competitors(id) ON DELETE CASCADE,
    signal_type TEXT NOT NULL CHECK(signal_type IN ('job_posting_surge', 'legal_entity_creation', 'lease_signing', 'patent_filing', 'tos_change')),
    title TEXT NOT NULL,
    department TEXT NOT NULL, -- 'engineering', 'sales', 'legal', 'executive'
    detected_count INTEGER DEFAULT 1,
    lead_time_months INTEGER NOT NULL, -- Anticipation estimée (ex: 6 à 12 mois)
    deduced_strategic_intent TEXT NOT NULL,
    source_url TEXT NOT NULL,
    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 7. Métriques opérationnelles de benchmarking
CREATE TABLE IF NOT EXISTS operational_benchmarks (
    id TEXT PRIMARY KEY,
    competitor_id TEXT NOT NULL REFERENCES competitors(id) ON DELETE CASCADE,
    time_to_value_days INTEGER NOT NULL,
    cac_eur REAL DEFAULT NULL,
    churn_annual_pct REAL DEFAULT NULL,
    nrr_pct REAL DEFAULT NULL,
    benchmark_quarter TEXT NOT NULL, -- ex: '2026-Q4'
    notes TEXT
);
