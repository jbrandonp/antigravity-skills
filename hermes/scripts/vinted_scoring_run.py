#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Vinted pipeline — scoring run (cron Price Compare + Scoring)."""
import mysql.connector, sys

conn = mysql.connector.connect(host='127.0.0.1', port=3306, user='root', password='2108', database='kate_sync')
cur = conn.cursor()
results = {}

def run(label, sql, params=None):
    cur.execute(sql, params or ())
    conn.commit()
    results[label] = cur.rowcount
    print(f"[{label}] changed: {cur.rowcount}")

# 1. days_listed + demand_score
run("days_listed", "UPDATE vinted_items SET days_listed = DATEDIFF(NOW(), first_seen) WHERE is_sold=0")
run("demand_score", """UPDATE vinted_items SET demand_score = ROUND(
        COALESCE(favourites,0)*0.5 + COALESCE(views,0)*0.05 + (40.0/NULLIF(days_listed+1,0)), 2)
    WHERE is_sold=0""")

# 2. price_vs_avg_pct (JOIN, pas sous-requete — MySQL interdit UPDATE meme table)
run("price_vs_avg_pct", """UPDATE vinted_items vi
    JOIN (SELECT query_id, country, AVG(price) as avg_p FROM vinted_items WHERE is_sold=0 AND price>0 GROUP BY query_id, country) av
    ON vi.query_id = av.query_id AND vi.country = av.country
    SET vi.price_vs_avg_pct = ROUND((av.avg_p - vi.price)/NULLIF(av.avg_p,0)*100, 2)
    WHERE vi.is_sold=0 AND vi.price>0""")

# 3. opportunity_score
run("opportunity_score", """UPDATE vinted_items SET opportunity_score = ROUND(
        (COALESCE(profit_ratio,1.0)-1)*50 + COALESCE(demand_score,0)*0.4 + GREATEST(COALESCE(price_vs_avg_pct,0),0)*0.3, 2)
    WHERE is_sold=0""")

# 4. flip_priority
run("flip_priority", """UPDATE vinted_items SET flip_priority = CASE
        WHEN opportunity_score >= 50 THEN 'HOT'
        WHEN opportunity_score >= 30 THEN 'WARM'
        WHEN opportunity_score >= 15 THEN 'COOL'
        ELSE 'COLD' END
    WHERE is_sold=0""")

# 5. price alerts (anti-doublon 1h)
run("price_alerts", """INSERT INTO price_alerts (item_id, alert_type, old_value, new_value, change_pct)
    SELECT id, 'price_drop', last_price, price, last_price_change_pct
    FROM vinted_items WHERE last_price_change_pct <= -5 AND is_sold=0
    AND (id, 'price_drop', last_price, price, last_price_change_pct) NOT IN (
        SELECT item_id, alert_type, old_value, new_value, change_pct FROM price_alerts
        WHERE triggered_at > NOW() - INTERVAL 1 HOUR)""")

# 5b. catch-up: items arrives pendant le scoring
cur.execute("SELECT COUNT(*) FROM vinted_items WHERE is_sold=0 AND flip_priority IS NULL")
nulls = cur.fetchone()[0]
results["null_flip_after"] = nulls
if nulls > 0:
    run("catchup_demand", "UPDATE vinted_items SET demand_score = ROUND(COALESCE(favourites,0)*0.5 + COALESCE(views,0)*0.05 + (40.0/NULLIF(days_listed+1,0)), 2) WHERE is_sold=0 AND flip_priority IS NULL")
    run("catchup_opportunity", "UPDATE vinted_items SET opportunity_score = ROUND((COALESCE(profit_ratio,1.0)-1)*50 + COALESCE(demand_score,0)*0.4 + GREATEST(COALESCE(price_vs_avg_pct,0),0)*0.3, 2) WHERE is_sold=0 AND flip_priority IS NULL")
    run("catchup_flip", """UPDATE vinted_items SET flip_priority = CASE WHEN opportunity_score >= 50 THEN 'HOT'
        WHEN opportunity_score >= 30 THEN 'WARM' WHEN opportunity_score >= 15 THEN 'COOL' ELSE 'COLD' END
        WHERE is_sold=0 AND flip_priority IS NULL""")

# 7. market_stats engagement
run("market_stats", """INSERT INTO market_stats (query_id, country, source, active_listings, avg_price, min_price, max_price, avg_favourites, avg_views, hot_count, warm_count, new_last_24h, snapshot_date)
    SELECT query_id, country, 'vinted', COUNT(*), ROUND(AVG(price),2), MIN(price), MAX(price),
        ROUND(AVG(COALESCE(favourites,0)),1), ROUND(AVG(COALESCE(views,0)),1),
        SUM(CASE WHEN flip_priority='HOT' THEN 1 ELSE 0 END),
        SUM(CASE WHEN flip_priority='WARM' THEN 1 ELSE 0 END),
        SUM(CASE WHEN first_seen >= NOW() - INTERVAL 24 HOUR THEN 1 ELSE 0 END),
        CURDATE()
    FROM vinted_items WHERE is_sold=0 AND price>0
    GROUP BY query_id, country
    ON DUPLICATE KEY UPDATE
        active_listings=VALUES(active_listings), avg_price=VALUES(avg_price),
        avg_favourites=VALUES(avg_favourites), avg_views=VALUES(avg_views),
        hot_count=VALUES(hot_count), warm_count=VALUES(warm_count)""")

# Distribution finale
cur.execute("SELECT flip_priority, COUNT(*) FROM vinted_items WHERE is_sold=0 GROUP BY flip_priority")
dist = cur.fetchall()
print("FINAL DISTRIBUTION:", dist)
conn.close()
print("DONE")
