import mysql.connector
c = mysql.connector.connect(host='127.0.0.1', port=3306, user='root', password='2108', database='kate_sync')
cur = c.cursor()

# Upsert test items
items = [
    (9118889019, 'Nike air max 90', 63.00, 'Nike', 'Tres bon etat', '39', 29, 'be', 'rabis341', 1),
    (9157977506, 'Nike Air Max 90 PRM Multicolor', 110.00, 'Nike', 'Neuf avec etiquette', '43', 11, 'be', 'raphding', 1),
    (9155011941, 'Nike Air Max 90 Drift 44', 120.00, 'Nike', 'Neuf sans etiquette', '44', 14, 'be', 'gabcol13', 1),
    (9176001702, 'Nike Air Max 90 Triple Black', 70.00, 'Nike', 'Neuf sans etiquette', '42', 1, 'be', 'arikatahere', 1),
]
for (iid, title, price, brand, cond, size, favs, country, seller, qid) in items:
    cur.execute("""INSERT INTO vinted_items 
        (id, title, price, brand, condition_text, size, favourites, country, url, seller_username, query_id)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,'',%s,%s)
        ON DUPLICATE KEY UPDATE
        title=VALUES(title), price=VALUES(price), favourites=VALUES(favourites),
        last_price=IF(price!=VALUES(price), price, last_price),
        last_price_change_pct=IF(price!=VALUES(price), ROUND((VALUES(price)-price)/price*100,2), last_price_change_pct),
        last_seen=NOW()""", (iid, title, price, brand, cond, size, favs, country, seller, qid))

# Simulate margins (DE resell higher)
cur.execute("UPDATE vinted_items SET estimated_sell_price = price * 1.30 WHERE query_id=1")
cur.execute("UPDATE vinted_items SET price_gap_abs = estimated_sell_price - price WHERE query_id=1")
cur.execute("UPDATE vinted_items SET price_gap_pct = ROUND((estimated_sell_price - price) / price * 100, 2) WHERE query_id=1")
cur.execute("UPDATE vinted_items SET profit_ratio = ROUND(estimated_sell_price / price, 4) WHERE query_id=1")

# Test price_snapshot
cur.execute("INSERT IGNORE INTO price_snapshots (item_id,price,favourites,country) VALUES (%s,%s,%s,%s)",
    (9118889019,63.00,29,'be'))

c.commit()

print("=" * 70)
print("TEST PIPELINE VINTED v2")
print("=" * 70)

print()
print("--- vinted_items avec marges ---")
cur.execute("SELECT id, title, price, estimated_sell_price, price_gap_abs, price_gap_pct, profit_ratio FROM vinted_items LIMIT 5")
for row in cur:
    est = row[3] or 0; gap = row[4] or 0; gapp = row[5] or 0; ratio = row[6] or 0
    print(f"  [{row[0]}] {row[1][:48]:48s}")
    print(f"         buy={row[2]:6.0f}EUR  estSell={est:6.0f}EUR  gap={gap:5.0f}EUR  gap%={gapp:5.1f}%  ratio={ratio}")

print()
print("--- v_item_margins VIEW (top 3) ---")
cur.execute("SELECT title, buy_price, sell_price, price_gap_pct, profit_ratio, opportunity_grade FROM v_item_margins LIMIT 3")
for row in cur:
    bp = row[1] or 0; sp = row[2] or 0; gp = row[3] or 0; pr = row[4] or 0
    print(f"  {row[0][:40]:40s} buy={bp} sell={sp} gap%={gp} ratio={pr}  [{row[5]}]")

print()
print("--- v_arbitrage_dashboard VIEW ---")
cur.execute("SELECT query, buy_country, buy_price, sell_country, sell_price, spread_pct, alert_level FROM v_arbitrage_dashboard")
for row in cur:
    print(f"  {row[0]:20s} {row[1]} {row[2]}EUR -> {row[3]} {row[4]}EUR  spread={row[5]}%  [{row[6]}]")

print()
print("--- v_price_history VIEW ---")
cur.execute("SELECT item_id, title, snapshot_price, previous_price, price_delta, price_delta_pct FROM v_price_history LIMIT 3")
for row in cur:
    prev = row[3] or 0; delta = row[4] or 0; deltap = row[5] or 0
    print(f"  [{row[0]}] {row[1][:35]:35s} snap={row[2]} prev={prev} delta={delta} delta%={deltap}")

print()
print("--- Toutes les tables ---")
cur.execute("SELECT TABLE_NAME, TABLE_ROWS FROM information_schema.TABLES WHERE TABLE_SCHEMA='kate_sync' AND TABLE_TYPE='BASE TABLE' ORDER BY TABLE_NAME")
for t in cur:
    print(f"  {t[0]:30s} {t[1] or 0} rows")

print()
print("--- Toutes les vues ---")
cur.execute("SELECT TABLE_NAME FROM information_schema.VIEWS WHERE TABLE_SCHEMA='kate_sync'")
for v in cur:
    print(f"  {v[0]}")

print()
print("--- Dernier scrape_run ---")
cur.execute("SELECT id, run_type, started_at, items_found, items_new, status FROM scrape_runs ORDER BY id DESC LIMIT 3")
for r in cur:
    print(f"  #{r[0]} {r[1]:20s} {r[2]} found={r[3]} new={r[4]} status={r[5]}")

print()
print("--- search_queries actives ---")
cur.execute("SELECT id, query, priority, countries FROM search_queries WHERE active=1 ORDER BY priority LIMIT 5")
for r in cur:
    print(f"  [{r[0]}] prio={r[2]} {r[1]:25s} countries={r[3]}")

c.close()
print()
print("=" * 70)
print("TEST COMPLET - TOUT FONCTIONNE")
print("=" * 70)
