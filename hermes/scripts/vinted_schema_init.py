#!/usr/bin/env python3
"""Vinted Arbitrage System - MySQL Schema + Seed Data"""
import mysql.connector

DB = {
    'host': '127.0.0.1', 'port': 3306,
    'user': 'root', 'password': '2108',
    'database': 'kate_sync'
}

def main():
    conn = mysql.connector.connect(**DB)
    cur = conn.cursor()

    # Drop existing
    for t in ['arbitrage_opportunities','price_snapshots','ebay_listings',
              'vinted_sellers','vinted_items','scrape_runs','search_queries']:
        cur.execute(f"DROP TABLE IF EXISTS {t}")

    # ── search_queries ──
    cur.execute("""CREATE TABLE search_queries (
        id INT AUTO_INCREMENT PRIMARY KEY,
        query VARCHAR(255) NOT NULL,
        category VARCHAR(100),
        min_price DECIMAL(10,2), max_price DECIMAL(10,2),
        brands JSON, conditions JSON,
        countries JSON,
        ebay_search BOOLEAN DEFAULT TRUE,
        active BOOLEAN DEFAULT TRUE,
        priority INT DEFAULT 5,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4""")

    # ── vinted_items ──
    cur.execute("""CREATE TABLE vinted_items (
        id BIGINT PRIMARY KEY,
        title VARCHAR(500), description TEXT,
        price DECIMAL(10,2), currency VARCHAR(3) DEFAULT 'EUR',
        original_price DECIMAL(10,2),
        brand VARCHAR(200), category VARCHAR(200),
        size VARCHAR(50), condition_text VARCHAR(100),
        color VARCHAR(100), photos JSON,
        favourites INT DEFAULT 0, views INT DEFAULT 0,
        is_sold BOOLEAN DEFAULT FALSE,
        country VARCHAR(3), url VARCHAR(500),
        seller_id BIGINT, seller_username VARCHAR(200),
        query_id INT,
        first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        INDEX idx_country (country), INDEX idx_price (price),
        INDEX idx_brand (brand), INDEX idx_query (query_id),
        FULLTEXT idx_title_desc (title, description)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4""")

    # ── vinted_sellers ──
    cur.execute("""CREATE TABLE vinted_sellers (
        id BIGINT PRIMARY KEY,
        username VARCHAR(200), profile_url VARCHAR(500),
        rating DECIMAL(3,1), rating_count INT DEFAULT 0,
        item_count INT DEFAULT 0, sold_item_count INT DEFAULT 0,
        follower_count INT DEFAULT 0, following_count INT DEFAULT 0,
        country VARCHAR(3), city VARCHAR(200),
        member_since VARCHAR(50), verifications JSON,
        last_scraped TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4""")

    # ── price_snapshots ──
    cur.execute("""CREATE TABLE price_snapshots (
        id INT AUTO_INCREMENT PRIMARY KEY,
        item_id BIGINT NOT NULL, price DECIMAL(10,2),
        favourites INT, views INT, is_sold BOOLEAN,
        country VARCHAR(3),
        snapshot_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        INDEX idx_item_time (item_id, snapshot_at)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4""")

    # ── ebay_listings ──
    cur.execute("""CREATE TABLE ebay_listings (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(500), price_text VARCHAR(100),
        price_eur DECIMAL(10,2),
        source VARCHAR(100) DEFAULT 'ebay',
        url VARCHAR(1000), query_id INT, country VARCHAR(3),
        found_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        INDEX idx_query (query_id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4""")

    # ── arbitrage_opportunities ──
    cur.execute("""CREATE TABLE arbitrage_opportunities (
        id INT AUTO_INCREMENT PRIMARY KEY,
        query VARCHAR(255),
        buy_country VARCHAR(3), buy_platform VARCHAR(50) DEFAULT 'vinted',
        buy_price DECIMAL(10,2),
        sell_country VARCHAR(3), sell_platform VARCHAR(50) DEFAULT 'vinted',
        sell_price DECIMAL(10,2),
        spread_pct DECIMAL(8,2), potential_profit DECIMAL(10,2),
        detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        notified BOOLEAN DEFAULT FALSE,
        INDEX idx_spread (spread_pct)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4""")

    # ── scrape_runs ──
    cur.execute("""CREATE TABLE scrape_runs (
        id INT AUTO_INCREMENT PRIMARY KEY,
        run_type VARCHAR(50) NOT NULL,
        started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        finished_at TIMESTAMP NULL,
        items_found INT DEFAULT 0, items_new INT DEFAULT 0,
        items_updated INT DEFAULT 0,
        errors TEXT, status VARCHAR(20) DEFAULT 'running'
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4""")

    conn.commit()

    # ── Seed queries ──
    queries = [
        ("Nike Air Max 90", "sneakers", 10, 200, '["Nike"]', '["very_good","good"]', '["fr","be","de","nl"]'),
        ("Nike Air Max 95", "sneakers", 10, 200, '["Nike"]', '["very_good","good"]', '["fr","be","de","nl"]'),
        ("Air Jordan 1", "sneakers", 20, 500, '["Nike","Jordan"]', '["very_good","good"]', '["fr","be","de","nl","it","es","pl"]'),
        ("Nike Dunk", "sneakers", 20, 300, '["Nike"]', None, '["fr","be","de","nl"]'),
        ("Adidas Samba", "sneakers", 15, 200, '["Adidas"]', None, '["fr","be","de","nl","it","es"]'),
        ("Adidas Gazelle", "sneakers", 15, 200, '["Adidas"]', None, '["fr","be","de","nl"]'),
        ("Levi's 501", "jeans", 10, 150, '["Levi\'s"]', None, '["fr","be","de","nl"]'),
        ("Carhartt jacket", "streetwear", 20, 250, '["Carhartt"]', None, '["fr","be","de","nl"]'),
        ("Stone Island", "streetwear", 30, 500, '["Stone Island"]', '["very_good","good"]', '["fr","be","de","nl","it"]'),
        ("Ralph Lauren polo", "polos", 10, 100, '["Ralph Lauren"]', None, '["fr","be","de","nl"]'),
        ("The North Face jacket", "outerwear", 20, 300, '["The North Face"]', None, '["fr","be","de","nl"]'),
        ("Patagonia", "outerwear", 20, 300, '["Patagonia"]', None, '["fr","be","de","nl"]'),
        ("Lego Star Wars", "toys", 10, 500, '["Lego"]', None, '["fr","be","de","nl"]'),
        ("Montre automatique", "watches", 20, 500, None, None, '["fr","be","de","nl","it"]'),
        ("iPhone 15", "electronics", 100, 800, '["Apple"]', '["very_good","good"]', '["fr","be","de","nl"]'),
        ("PS5 console", "electronics", 100, 500, '["Sony"]', '["very_good","good"]', '["fr","be","de","nl"]'),
        ("Dyson Airwrap", "beauty", 100, 500, '["Dyson"]', '["very_good","good"]', '["fr","be","de","nl"]'),
        ("New Balance 530", "sneakers", 20, 180, '["New Balance"]', None, '["fr","be","de","nl","it"]'),
        ("Birkenstock Boston", "shoes", 20, 200, '["Birkenstock"]', None, '["fr","be","de","nl"]'),
        ("Arc'teryx", "outerwear", 50, 500, '["Arc\'teryx"]', '["very_good","good"]', '["fr","be","de","nl"]'),
    ]

    for q in queries:
        cur.execute("""INSERT INTO search_queries 
            (query,category,min_price,max_price,brands,conditions,countries)
            VALUES (%s,%s,%s,%s,%s,%s,%s)""", q)

    conn.commit()
    cur.execute("SELECT COUNT(*) FROM search_queries")
    count = cur.fetchone()[0]
    cur.close(); conn.close()
    print(f"✅ Schema créé. {count} requêtes de recherche seedées.")
    return count

if __name__ == '__main__':
    main()
