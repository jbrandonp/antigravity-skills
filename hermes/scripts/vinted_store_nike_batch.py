"""Store Vinted search results in MySQL kate_sync"""
import mysql.connector
from datetime import datetime

DB = {'host':'127.0.0.1','port':3306,'user':'root','password':'2108','database':'kate_sync'}

items = [
    # FR
    (9176651976,"Nike mercurial",25,"Nike","Tres bon etat","47,5",0,"tg7405","fr"),
    (9176651717,"Nike sportswear react",30,"Nike","Tres bon etat","44",0,"haitamsalkmabli","fr"),
    (9176651181,"Nike Blazer khaki",40,"Nike","Tres bon etat","40",0,"flaviazf93","fr"),
    (9176650219,"Nike Phantom taille 47",15,"Nike","Tres bon etat","47",0,"mezyala","fr"),
    (9176650285,"Basket dunk low enfant",10,"Nike","Satisfaisant","28",0,"yuvinho","fr"),
    (9176648838,"Chaussure Nike",25,"Nike","Tres bon etat","39",0,"jsp3432","fr"),
    (9176652955,"Air force one miste",20,"Nike","Bon etat","38.5",0,"baya6611","fr"),
    (9176648488,"Nike Blazer Low Platform White Black Sail",40,"Nike","Tres bon etat","38",0,"bylvnaa","fr"),
    (9176652609,"Nike air force 1",25,"Nike","Tres bon etat","26",0,"kariina2309","fr"),
    (9176648074,"Vapormax",20,"Nike","Tres bon etat","44",0,"danieleeeros","fr"),
    (9176647548,"Chaussures de foot Nike",35,"Nike","Neuf avec etiquette","33",0,"modem90","fr"),
    (9176647823,"Scarpe Nike",18,"Nike","Tres bon etat","42",0,"giovanni2020140169","fr"),
    (9176647459,"Nike Blazer Mid 77 Vintage",30,"Nike","Neuf sans etiquette","47",0,"bakozeus84","fr"),
    (9176647259,"Air force one noir Nike",20,"Nike","Bon etat","42",0,"alya017","fr"),
    (9176646043,"Dunk noir et blanc",30,"Nike","Tres bon etat","38",0,"m_ena788","fr"),
    (9176646124,"Nike air Huarache",5,"Nike","Bon etat","40",0,"sudeeyk","fr"),
    (9176647521,"Tenis Nike",25,"Nike","Bon etat","39",0,"verissimo.04","fr"),
    (9176646822,"Tenis Jordan",12,"Nike","Bon etat","37",0,"al3824","fr"),
    (9176645813,"Basket Nike",18,"Nike","Tres bon etat","33",0,"artur__97","fr"),
    # DE
    (9176648298,"Nike Cortez sneakers",50,"Nike","Sehr gut","45",0,"mariamario77","de"),
    (9176637647,"Tn 3 full black",49,"Nike","Sehr gut","43",0,"timdu130","de"),
    (9176645958,"AirForce One",19.99,"Nike","Gut","39",0,"alexshopss75","de"),
]

conn = mysql.connector.connect(**DB)
cur = conn.cursor()

# Query mappings
def get_query(title):
    t = title.lower()
    if 'air max' in t or 'tn ' in t: return "Nike Air Max"
    if 'air force' in t: return "Nike Air Force"
    if 'dunk' in t: return "Nike Dunk"
    if 'jordan' in t: return "Air Jordan 1"
    if 'blazer' in t: return "Nike Blazer"
    if 'vapormax' in t: return "Nike Vapormax"
    if 'react' in t: return "Nike React"
    if 'huarache' in t: return "Nike Huarache"
    if 'cortez' in t: return "Nike Cortez"
    return "Nike chaussure"

query_ids = {}
for q in set(get_query(i[1]) for i in items):
    cur.execute("SELECT id FROM search_queries WHERE query=%s", (q,))
    row = cur.fetchone()
    if row:
        query_ids[q] = row[0]
    else:
        cur.execute("INSERT INTO search_queries (query,category,min_price,max_price,brands,countries) VALUES (%s,'sneakers',1,100,'[\"Nike\"]','[\"fr\",\"be\",\"de\",\"nl\",\"it\",\"es\"]')", (q,))
        conn.commit()
        query_ids[q] = cur.lastrowid
        print(f"  + query: {q}")

stored, updated = 0, 0
for (item_id,title,price,brand,condition,size,favs,seller,country) in items:
    q = get_query(title)
    qid = query_ids[q]
    try:
        cur.execute("SELECT id FROM vinted_items WHERE id=%s", (item_id,))
        if cur.fetchone():
            cur.execute("UPDATE vinted_items SET price=%s,favourites=%s,condition_text=%s,last_seen=NOW() WHERE id=%s", (price,favs,condition,item_id))
            updated += 1
        else:
            cur.execute("INSERT INTO vinted_items (id,title,price,brand,condition_text,size,favourites,country,query_id,seller_username,first_seen,last_seen) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW(),NOW())", (item_id,title,price,brand,condition,size,favs,country,qid,seller))
            cur.execute("INSERT INTO price_snapshots (item_id,price,snapshot_at) VALUES (%s,%s,NOW()) ON DUPLICATE KEY UPDATE price=VALUES(price)", (item_id,price))
            stored += 1
    except Exception as e:
        print(f"  x {item_id}: {e}")

conn.commit()

# Rescore all
cur.execute("UPDATE vinted_items SET days_listed = DATEDIFF(NOW(), first_seen) WHERE is_sold=0")
cur.execute("UPDATE vinted_items SET demand_score = ROUND(COALESCE(favourites,0)*0.5 + COALESCE(views,0)*0.05 + 40.0/NULLIF(days_listed+1,0), 2) WHERE is_sold=0")
cur.execute("UPDATE vinted_items vi JOIN (SELECT query_id, country, AVG(price) as avg_p FROM vinted_items WHERE is_sold=0 AND price>0 GROUP BY query_id, country) av ON vi.query_id=av.query_id AND vi.country=av.country SET vi.price_vs_avg_pct = ROUND((av.avg_p-vi.price)/NULLIF(av.avg_p,0)*100, 2) WHERE vi.is_sold=0 AND vi.price>0")
cur.execute("UPDATE vinted_items SET opportunity_score = ROUND((COALESCE(profit_ratio,1.0)-1)*50 + COALESCE(demand_score,0)*0.4 + GREATEST(COALESCE(price_vs_avg_pct,0),0)*0.3, 2) WHERE is_sold=0")
cur.execute("UPDATE vinted_items SET flip_priority = CASE WHEN opportunity_score>=50 THEN 'HOT' WHEN opportunity_score>=30 THEN 'WARM' WHEN opportunity_score>=15 THEN 'COOL' ELSE 'COLD' END WHERE is_sold=0")
conn.commit()

cur.execute("SELECT COUNT(*) FROM vinted_items WHERE brand='Nike' AND is_sold=0")
total = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM vinted_items WHERE flip_priority='HOT'")
hot = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM vinted_items WHERE flip_priority='WARM'")
warm = cur.fetchone()[0]

print(f"\nStored: {stored} new | Updated: {updated} existing")
print(f"Nike in DB: {total} | HOT: {hot} | WARM: {warm}")
print(f"Queries active: {len(query_ids)}")

cur.execute("SELECT COUNT(*) FROM price_snapshots")
print(f"Snapshots: {cur.fetchone()[0]}")

conn.close()
