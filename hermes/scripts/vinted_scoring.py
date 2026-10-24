import mysql.connector
c = mysql.connector.connect(host='127.0.0.1', port=3306, user='root', password='2108', database='kate_sync')
cur = c.cursor()

# Add columns (skip if exist)
alters = [
    'ALTER TABLE vinted_items ADD COLUMN opportunity_score DECIMAL(6,2) DEFAULT 0',
    'ALTER TABLE vinted_items ADD COLUMN demand_score DECIMAL(6,2) DEFAULT 0',
    'ALTER TABLE vinted_items ADD COLUMN flip_priority VARCHAR(10) DEFAULT NULL',
    'ALTER TABLE vinted_items ADD COLUMN days_listed INT DEFAULT 0',
    'ALTER TABLE vinted_items ADD COLUMN seller_rating DECIMAL(3,1) DEFAULT NULL',
    'ALTER TABLE vinted_items ADD COLUMN price_vs_avg_pct DECIMAL(6,2) DEFAULT NULL',
]
for sql in alters:
    try:
        cur.execute(sql)
        print(f'  + {sql.split("ADD COLUMN")[1].strip().split()[0]}')
    except Exception as e:
        if 'Duplicate' in str(e):
            print(f'  ~ {sql.split("ADD COLUMN")[1].strip().split()[0]} (exists)')
        else:
            print(f'  x {e}')

c.commit()

# Step 1: days_listed
cur.execute('UPDATE vinted_items SET days_listed = DATEDIFF(NOW(), first_seen) WHERE is_sold = 0')
print(f'  days_listed: {cur.rowcount} items')

# Step 2: price_vs_avg_pct using a derived table
cur.execute('''
    UPDATE vinted_items vi
    JOIN (
        SELECT query_id, country, AVG(price) as avg_p
        FROM vinted_items WHERE is_sold=0 AND price>0
        GROUP BY query_id, country
    ) av ON vi.query_id = av.query_id AND vi.country = av.country
    SET vi.price_vs_avg_pct = ROUND((av.avg_p - vi.price) / NULLIF(av.avg_p, 0) * 100, 2)
    WHERE vi.is_sold = 0 AND vi.price > 0
''')
print(f'  price_vs_avg_pct: {cur.rowcount} items')

# Step 3: demand_score = favourites * 0.5 + views * 0.05 + recency boost
cur.execute('''
    UPDATE vinted_items SET
        demand_score = ROUND(
            COALESCE(favourites, 0) * 0.5 + 
            COALESCE(views, 0) * 0.05 + 
            (40.0 / NULLIF(days_listed + 1, 0))
        , 2)
    WHERE is_sold = 0
''')
print(f'  demand_score: {cur.rowcount} items')

# Step 4: opportunity_score = flipping potential
# High profit_ratio + high demand + below market price = best flip
cur.execute('''
    UPDATE vinted_items SET
        opportunity_score = ROUND(
            (COALESCE(profit_ratio, 1.0) - 1) * 50 +
            COALESCE(demand_score, 0) * 0.4 +
            GREATEST(COALESCE(price_vs_avg_pct, 0), 0) * 0.3
        , 2)
    WHERE is_sold = 0
''')
print(f'  opportunity_score: {cur.rowcount} items')

# Step 5: flip_priority
cur.execute('''
    UPDATE vinted_items SET flip_priority = 
        CASE 
            WHEN opportunity_score >= 50 THEN 'HOT'
            WHEN opportunity_score >= 30 THEN 'WARM'
            WHEN opportunity_score >= 15 THEN 'COOL'
            ELSE 'COLD'
        END
    WHERE is_sold = 0
''')
print(f'  flip_priority: {cur.rowcount} items')

c.commit()

# Show results
print()
print('=' * 85)
print('TOP 15 FLIPS (opportunity_score composite)')
print('=' * 85)
cur.execute('''
    SELECT id, title, price, favourites, views, days_listed,
           profit_ratio, demand_score, opportunity_score, flip_priority
    FROM vinted_items WHERE is_sold=0 AND price > 0
    ORDER BY opportunity_score DESC LIMIT 15
''')
for r in cur:
    fav = r[3] or 0; views = r[4] or 0; days = r[5] or 0
    print(f'  [{r[9]:5s}] score={r[8]:6.1f} demand={r[7]:6.1f} ratio={r[6] or 1:.2f} | {r[1][:42]:42s} | {r[2]:6.0f}EUR fav={fav:3d} v={views:4d} d={days:2d}j')

print()
print('=' * 85)
print('DISTRIBUTION')
print('=' * 85)
cur.execute('SELECT flip_priority, COUNT(*) FROM vinted_items WHERE is_sold=0 AND flip_priority IS NOT NULL GROUP BY flip_priority ORDER BY FIELD(flip_priority,"HOT","WARM","COOL","COLD")')
for r in cur:
    print(f'  {r[0]:5s}: {r[1]} items')

cur.execute('SELECT AVG(opportunity_score), MAX(opportunity_score) FROM vinted_items WHERE is_sold=0')
r = cur.fetchone()
print(f'\n  Score moyen: {r[0]:.1f} | Score max: {r[1]:.1f}')

c.close()
