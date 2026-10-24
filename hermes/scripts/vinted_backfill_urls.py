import mysql.connector

c = mysql.connector.connect(host='127.0.0.1', port=3306, user='root', password='2108', database='kate_sync')
cur = c.cursor()

# 1. Backfill missing Vinted URLs
cur.execute("""
    UPDATE vinted_items 
    SET url = CONCAT('https://www.vinted.', country, '/items/', id, '-', REPLACE(REPLACE(LOWER(title),' ','-'), '/','-'))
    WHERE (url IS NULL OR url = '') AND country IS NOT NULL
""")
print(f"URLs backfilled: {cur.rowcount} items")

# 2. Add url column to google_listings if missing
try:
    cur.execute("ALTER TABLE google_listings ADD COLUMN url VARCHAR(1000)")
    print("+ url column on google_listings")
except: 
    print("~ url already on google_listings")

# 3. Add url column to ebay_listings if missing (should already exist)
try:
    cur.execute("SELECT url FROM ebay_listings LIMIT 1")
    print("~ ebay_listings has url")
except:
    cur.execute("ALTER TABLE ebay_listings ADD COLUMN url VARCHAR(1000)")
    print("+ url column on ebay_listings")

# 4. Add url to kolkovo_listings if missing
try:
    cur.execute("SELECT source_url FROM kolkovo_listings LIMIT 1")
    print("~ kolkovo_listings has source_url")
except:
    cur.execute("ALTER TABLE kolkovo_listings ADD COLUMN source_url VARCHAR(1000)")
    print("+ source_url on kolkovo_listings")

# 5. Update v_top_flips to include URL
cur.execute("DROP VIEW IF EXISTS v_top_flips")
cur.execute("""
    CREATE VIEW v_top_flips AS
    SELECT 
        vi.id, vi.title, vi.brand, vi.price, vi.estimated_sell_price,
        vi.price_gap_pct, vi.profit_ratio,
        vi.favourites, vi.views, vi.days_listed,
        vi.condition_text, vi.size, vi.country, vi.url,
        vi.demand_score, vi.opportunity_score, vi.flip_priority,
        ROUND(vi.price_gap_abs, 2) as potential_profit_eur,
        CASE 
            WHEN vi.favourites >= 50 THEN CONCAT('🚀 ', vi.favourites, ' fav')
            WHEN vi.favourites >= 20 THEN CONCAT('🔥 ', vi.favourites, ' fav')
            WHEN vi.favourites >= 10 THEN CONCAT('👀 ', vi.favourites, ' fav')
            ELSE ''
        END as engagement,
        vi.seller_username
    FROM vinted_items vi
    WHERE vi.is_sold = 0 AND vi.price > 0
    ORDER BY vi.opportunity_score DESC
""")
print("+ v_top_flips recreaated with url + seller_username")

c.commit()

# Verify
cur.execute("SELECT COUNT(*) as t, SUM(CASE WHEN url IS NOT NULL AND url!='' THEN 1 ELSE 0 END) as u FROM vinted_items")
r = cur.fetchone()
print(f"\nVerification: {r[1]}/{r[0]} vinted_items avec URL")

cur.execute("SELECT COUNT(*) FROM google_listings")
print(f"google_listings: {cur.fetchone()[0]}")

# Show a few URLs
cur.execute("SELECT id, title, url FROM vinted_items WHERE url IS NOT NULL AND url != '' AND price < 50 LIMIT 3")
for r in cur:
    print(f"  #{r[0]} {r[1][:45]:45s} → {r[2]}" if r[2] else f"  #{r[0]} no URL")

c.close()
