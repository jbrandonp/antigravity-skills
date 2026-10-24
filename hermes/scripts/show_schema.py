import mysql.connector
c = mysql.connector.connect(host='127.0.0.1', port=3306, user='root', password='2108', database='kate_sync')
cur = c.cursor()
for t in ['vinted_items', 'ebay_listings', 'price_snapshots', 'arbitrage_opportunities']:
    cur.execute(f"SHOW CREATE TABLE {t}")
    row = cur.fetchone()
    print(f"\n=== {t} ===")
    print(row[1])
c.close()
