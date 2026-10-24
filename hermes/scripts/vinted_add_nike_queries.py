import mysql.connector

c = mysql.connector.connect(host='127.0.0.1', port=3306, user='root', password='2108', database='kate_sync')
cur = c.cursor()

# Add missing Nike shoe queries
new_queries = [
    ("Nike Air Force", "sneakers", 10, 100, '["Nike"]', None, '["fr","be","de","nl","it","es"]'),
    ("Nike Court Vision", "sneakers", 10, 100, '["Nike"]', None, '["fr","be","de","nl","it","es"]'),
    ("Nike Blazer", "sneakers", 10, 80, '["Nike"]', None, '["fr","be","de","nl","it"]'),
    ("Nike React", "sneakers", 15, 80, '["Nike"]', None, '["fr","be","de","nl"]'),
    ("Nike Revolution", "sneakers", 15, 80, '["Nike"]', None, '["fr","be","de","nl"]'),
    ("Nike Pegasus", "sneakers", 15, 80, '["Nike"]', None, '["fr","be","de","nl"]'),
    ("Nike Huarache", "sneakers", 20, 80, '["Nike"]', None, '["fr","be","de","nl"]'),
    ("Nike Vapormax", "sneakers", 20, 100, '["Nike"]', None, '["fr","be","de","nl"]'),
    ("Nike chaussure", "sneakers", 5, 50, '["Nike"]', '["very_good","good"]', '["fr","be","de","nl","it","es","pl"]'),
]

added = 0
for q in new_queries:
    cur.execute("SELECT id FROM search_queries WHERE query=%s", (q[0],))
    if not cur.fetchone():
        cur.execute("INSERT INTO search_queries (query,category,min_price,max_price,brands,conditions,countries) VALUES (%s,%s,%s,%s,%s,%s,%s)", q)
        added += 1
    else:
        print(f"  SKIP (exists): {q[0]}")

c.commit()
print(f"✅ {added} nouvelles queries Nike ajoutees")

# Store compare_prices results
arbitrages = [
    ("Nike Air Max", "de", 31.00, "es", 50.09, 61.61, 19.09),
    ("Nike Air Force", "it", 28.00, "nl", 40.50, 44.64, 12.50),
    ("Nike Dunk", "nl", 25.32, "es", 31.40, 24.01, 6.08),
    ("Nike Court Vision", "de", 34.45, "es", 42.68, 23.89, 8.23),
]

for (query, buy_c, buy_p, sell_c, sell_p, spread, profit) in arbitrages:
    cur.execute("INSERT INTO arbitrage_opportunities (query,buy_country,buy_platform,buy_price,sell_country,sell_platform,sell_price,spread_pct,potential_profit) VALUES (%s,%s,'vinted',%s,%s,'vinted',%s,%s,%s) ON DUPLICATE KEY UPDATE spread_pct=VALUES(spread_pct), potential_profit=VALUES(potential_profit), detected_at=NOW()",
        (query, buy_c, buy_p, sell_c, sell_p, spread, profit))

c.commit()
print(f"✅ {len(arbitrages)} arbitrages stockes")

# Count
cur.execute("SELECT COUNT(*) FROM search_queries WHERE active=1 AND category='sneakers'")
s = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM vinted_items WHERE brand LIKE '%Nike%' AND price < 50 AND is_sold=0")
n = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM arbitrage_opportunities WHERE notified=0")
o = cur.fetchone()[0]

print(f"\n📊 TOTAL: {s} queries sneakers | {n} Nike <50€ en base | {o} opportunites live")

c.close()
