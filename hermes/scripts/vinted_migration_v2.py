#!/usr/bin/env python3
"""Migration v2: ajout colonnes marges, prix, volumes, Google, matching"""
import mysql.connector

DB = {'host':'127.0.0.1','port':3306,'user':'root','password':'2108','database':'kate_sync'}

def run():
    conn = mysql.connector.connect(**DB)
    cur = conn.cursor()

    # ── 1. vinted_items : nouvelles colonnes ──
    alters = [
        "ALTER TABLE vinted_items ADD COLUMN item_published_at DATETIME NULL",
        "ALTER TABLE vinted_items ADD COLUMN estimated_sell_price DECIMAL(10,2) NULL",
        "ALTER TABLE vinted_items ADD COLUMN price_gap_abs DECIMAL(10,2) NULL",
        "ALTER TABLE vinted_items ADD COLUMN price_gap_pct DECIMAL(6,2) NULL",
        "ALTER TABLE vinted_items ADD COLUMN profit_ratio DECIMAL(6,4) NULL",
        "ALTER TABLE vinted_items ADD COLUMN last_price DECIMAL(10,2) NULL",
        "ALTER TABLE vinted_items ADD COLUMN last_price_change_pct DECIMAL(6,2) NULL",
        "ALTER TABLE vinted_items ADD COLUMN times_sold INT DEFAULT 0",
    ]
    for sql in alters:
        try:
            cur.execute(sql)
            print(f"  ✓ {sql.split('ADD COLUMN')[1].strip().split()[0]}")
        except Exception as e:
            if 'Duplicate column' in str(e):
                print(f"  ⏭ {sql.split('ADD COLUMN')[1].strip().split()[0]} (exists)")
            else:
                print(f"  ✗ {e}")

    # ── 2. ebay_listings : nouvelles colonnes ──
    ebay_alters = [
        "ALTER TABLE ebay_listings ADD COLUMN listing_date DATETIME NULL",
        "ALTER TABLE ebay_listings ADD COLUMN photos JSON NULL",
        "ALTER TABLE ebay_listings ADD COLUMN condition_text VARCHAR(100) NULL",
        "ALTER TABLE ebay_listings ADD COLUMN shipping_cost DECIMAL(10,2) NULL",
        "ALTER TABLE ebay_listings ADD COLUMN bids INT DEFAULT 0",
        "ALTER TABLE ebay_listings ADD COLUMN sold_count INT DEFAULT 0",
    ]
    for sql in ebay_alters:
        try:
            cur.execute(sql)
            print(f"  ✓ {sql.split('ADD COLUMN')[1].strip().split()[0]}")
        except Exception as e:
            if 'Duplicate column' in str(e):
                print(f"  ⏭ {sql.split('ADD COLUMN')[1].strip().split()[0]} (exists)")
            else:
                print(f"  ✗ {e}")

    # ── 3. item_matches (cross-plateforme) ──
    cur.execute("DROP TABLE IF EXISTS item_matches")
    cur.execute("""CREATE TABLE item_matches (
        id INT AUTO_INCREMENT PRIMARY KEY,
        vinted_item_id BIGINT NOT NULL,
        ebay_listing_id INT NULL,
        google_listing_id INT NULL,
        match_confidence DECIMAL(3,2),
        match_method VARCHAR(50) DEFAULT 'title_similarity',
        matched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        INDEX idx_vinted (vinted_item_id),
        INDEX idx_ebay (ebay_listing_id),
        INDEX idx_google (google_listing_id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4""")
    print("  ✓ item_matches created")

    # ── 4. market_stats (agrégation par query/pays/date) ──
    cur.execute("DROP TABLE IF EXISTS market_stats")
    cur.execute("""CREATE TABLE market_stats (
        id INT AUTO_INCREMENT PRIMARY KEY,
        query_id INT NOT NULL,
        country VARCHAR(3),
        source VARCHAR(50) DEFAULT 'vinted',
        active_listings INT DEFAULT 0,
        avg_price DECIMAL(10,2),
        median_price DECIMAL(10,2),
        min_price DECIMAL(10,2),
        max_price DECIMAL(10,2),
        sold_last_7d INT DEFAULT 0,
        new_last_24h INT DEFAULT 0,
        price_drop_count INT DEFAULT 0,
        avg_days_listed DECIMAL(6,1),
        snapshot_date DATE NOT NULL,
        snapshot_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE KEY uq_query_country_date (query_id, country, source, snapshot_date)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4""")
    print("  ✓ market_stats created")

    # ── 5. google_listings ──
    cur.execute("DROP TABLE IF EXISTS google_listings")
    cur.execute("""CREATE TABLE google_listings (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(500),
        price_text VARCHAR(100),
        price_eur DECIMAL(10,2),
        merchant VARCHAR(200),
        source_url VARCHAR(1000),
        query_id INT,
        country VARCHAR(3),
        found_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        INDEX idx_query (query_id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4""")
    print("  ✓ google_listings created")

    conn.commit()

    # ── 6. Vue prix avec variations ──
    cur.execute("DROP VIEW IF EXISTS v_price_history")
    cur.execute("""CREATE VIEW v_price_history AS
    SELECT 
        ps.item_id,
        vi.title,
        vi.brand,
        vi.country,
        vi.price AS current_price,
        ps.price AS snapshot_price,
        LAG(ps.price) OVER (PARTITION BY ps.item_id ORDER BY ps.snapshot_at) AS previous_price,
        ps.price - LAG(ps.price) OVER (PARTITION BY ps.item_id ORDER BY ps.snapshot_at) AS price_delta,
        ROUND((ps.price - LAG(ps.price) OVER (PARTITION BY ps.item_id ORDER BY ps.snapshot_at)) 
            / NULLIF(LAG(ps.price) OVER (PARTITION BY ps.item_id ORDER BY ps.snapshot_at), 0) * 100, 2) AS price_delta_pct,
        DATEDIFF(ps.snapshot_at, LAG(ps.snapshot_at) OVER (PARTITION BY ps.item_id ORDER BY ps.snapshot_at)) AS days_since_change,
        ps.snapshot_at
    FROM price_snapshots ps
    JOIN vinted_items vi ON ps.item_id = vi.id
    ORDER BY ps.item_id, ps.snapshot_at DESC""")
    print("  ✓ v_price_history view created")

    # ── 7. Vue marges calculées ──
    cur.execute("DROP VIEW IF EXISTS v_item_margins")
    cur.execute("""CREATE VIEW v_item_margins AS
    SELECT 
        vi.id,
        vi.title,
        vi.brand,
        vi.price AS buy_price,
        vi.estimated_sell_price AS sell_price,
        vi.price_gap_abs,
        vi.price_gap_pct,
        vi.profit_ratio,
        vi.country,
        vi.url,
        vi.favourites,
        vi.first_seen,
        CASE 
            WHEN vi.profit_ratio >= 2.0 THEN '🔥 Excellent'
            WHEN vi.profit_ratio >= 1.5 THEN '✅ Bon'
            WHEN vi.profit_ratio >= 1.2 THEN '👌 Correct'
            WHEN vi.profit_ratio IS NOT NULL THEN '😐 Faible'
            ELSE '❓ Non estimé'
        END AS opportunity_grade
    FROM vinted_items vi
    WHERE vi.is_sold = 0
    ORDER BY vi.profit_ratio DESC""")
    print("  ✓ v_item_margins view created")

    # ── 8. Vue dashboard arbitrage ──
    cur.execute("DROP VIEW IF EXISTS v_arbitrage_dashboard")
    cur.execute("""CREATE VIEW v_arbitrage_dashboard AS
    SELECT 
        ao.query,
        ao.buy_country,
        ao.buy_platform,
        ao.buy_price,
        ao.sell_country,
        ao.sell_platform,
        ao.sell_price,
        ao.spread_pct,
        ao.potential_profit,
        ao.detected_at,
        CASE 
            WHEN ao.spread_pct >= 100 THEN '🚀 MOON'
            WHEN ao.spread_pct >= 50 THEN '🔥 HOT'
            WHEN ao.spread_pct >= 30 THEN '✅ WARM'
            ELSE '👀 WATCH'
        END AS signal
    FROM arbitrage_opportunities ao
    WHERE ao.notified = 0
    ORDER BY ao.spread_pct DESC""")
    print("  ✓ v_arbitrage_dashboard view created")

    cur.close()
    conn.close()
    print("\n✅ Migration v2 terminée.")

if __name__ == '__main__':
    run()
