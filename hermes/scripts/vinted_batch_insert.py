#!/usr/bin/env python3
"""Batch UPSERT Vinted items into MySQL from JSON."""
import mysql.connector, json, sys, re

def slugify(t):
    s = t.lower()
    s = re.sub(r'[^a-z0-9\s-]', '', s)
    s = re.sub(r'\s+', '-', s.strip())
    return s[:80].rstrip('-')

def parse_price(p):
    if isinstance(p, (int, float)):
        return float(p)
    m = re.search(r'[\d,.]+', str(p).replace(',', '.'))
    return float(m.group()) if m else 0.0

def main():
    from pathlib import Path
    json_path = Path.home() / '.hermes' / 'scripts' / 'vinted_batch_run21.json'
    data = json.loads(json_path.read_text(encoding='utf-8'))
    run_id = 21
    
    conn = mysql.connector.connect(
        host='127.0.0.1', port=3306,
        user='root', password='2108',
        database='kate_sync'
    )
    cur = conn.cursor()
    new_items = 0
    exist_items = 0
    
    for entry in data:
        query_id = entry['query_id']
        country = entry['country']
        for item in entry['items']:
            item_id = item['id']
            title = item.get('title', '')
            price = parse_price(item.get('price', '0'))
            brand = item.get('brand', '')
            condition_text = item.get('condition', '')
            size = item.get('size', '')
            favs = int(item.get('favourites', 0))
            seller = item.get('seller', '')
            url = item.get('url', '')
            
            cur.execute("""
                INSERT INTO vinted_items (id, title, price, currency, brand, condition_text, size,
                    favourites, views, country, url, query_id, seller_username, first_seen)
                VALUES (%s, %s, %s, 'EUR', %s, %s, %s, %s, 0, %s, %s, %s, %s, NOW())
                ON DUPLICATE KEY UPDATE 
                    price=VALUES(price), favourites=VALUES(favourites),
                    url=VALUES(url),
                    title=VALUES(title), brand=VALUES(brand),
                    condition_text=VALUES(condition_text), size=VALUES(size),
                    seller_username=VALUES(seller_username)
            """, (item_id, title, price, brand, condition_text, size, favs, country, url, query_id, seller))
            
            if cur.rowcount == 1:
                new_items += 1
            else:
                exist_items += 1
            
            cur.execute("""
                INSERT INTO price_snapshots (item_id, price, favourites, views, country, snapshot_at)
                VALUES (%s, %s, %s, 0, %s, NOW())
                ON DUPLICATE KEY UPDATE price=VALUES(price), favourites=VALUES(favourites)
            """, (item_id, price, favs, country))
            
            if seller:
                cur.execute("""
                    INSERT IGNORE INTO vinted_sellers (username)
                    VALUES (%s)
                """, (seller,))
            
            if (new_items + exist_items) % 10 == 0:
                conn.commit()
    
    conn.commit()
    
    cur.execute("""
        UPDATE scrape_runs SET finished_at=NOW(), items_found=%s, items_new=%s, 
        items_updated=%s, status='completed' WHERE id=%s
    """, (new_items + exist_items, new_items, exist_items, run_id))
    conn.commit()
    
    print(f"OK: {new_items} new, {exist_items} existing, total={new_items+exist_items}")
    cur.close()
    conn.close()

if __name__ == '__main__':
    main()
