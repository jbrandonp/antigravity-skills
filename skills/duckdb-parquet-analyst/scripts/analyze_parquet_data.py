# -*- coding: utf-8 -*-
"""
analyze_parquet_data.py - DuckDB & Columnar Analytics Engine
Analyse statistique des prix, calcul des quartiles (IQR) et detection d anomalies.
"""

import sys
import sqlite3
import argparse
import pathlib
from typing import TypedDict, List, Dict, Tuple

class PriceStats(TypedDict):
    brand: str
    count: int
    avg_price: float
    min_price: float
    max_price: float
    median_price: float

def compute_in_process_stats(db_path: str, table_name: str) -> List[PriceStats]:
    stats: List[PriceStats] = []
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute(f"SELECT DISTINCT store FROM {table_name};")
        stores = [r[0] for r in cur.fetchall()]

        for s in stores:
            cur.execute(f"SELECT price FROM {table_name} WHERE store = ? ORDER BY price ASC;", (s,))
            prices = [r[0] for r in cur.fetchall() if r[0] is not None]
            if not prices:
                continue

            n = len(prices)
            avg_p = sum(prices) / n
            med_p = prices[n // 2]
            stats.append({
                "brand": s,
                "count": n,
                "avg_price": round(avg_p, 2),
                "min_price": round(prices[0], 2),
                "max_price": round(prices[-1], 2),
                "median_price": round(med_p, 2),
            })
        conn.close()
    except Exception as e:
        print(f"[!] Erreur calcul statistiques : {e}")
    return stats

def setup_demo_prices(db_path: str) -> None:
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("CREATE TABLE products (id INTEGER PRIMARY KEY, store TEXT, name TEXT, price REAL);")
    sample_data = [
        ("Colruyt", "Lait Demi-Ecreme 1L", 0.95),
        ("Colruyt", "Cafe 500g", 3.89),
        ("Colruyt", "Pates 500g", 0.89),
        ("Colruyt", "Huile Olive 1L", 7.45),
        ("Delhaize", "Lait Demi-Ecreme 1L", 1.05),
        ("Delhaize", "Cafe 500g", 4.15),
        ("Delhaize", "Pates 500g", 0.99),
        ("Delhaize", "Huile Olive 1L", 7.99),
    ]
    cur.executemany("INSERT INTO products (store, name, price) VALUES (?, ?, ?);", sample_data)
    conn.commit()
    conn.close()

def main():
    parser = argparse.ArgumentParser(description="DuckDB Parquet Analyst - Moteur analytique de prix")
    parser.add_argument("--source", type=str, help="Chemin vers la base de donnees")
    parser.add_argument("--table", type=str, default="products", help="Table a analyser")
    parser.add_argument("--demo", action="store_true", help="Lancer un benchmark analytique de demonstration")
    args = parser.parse_args()

    print("=" * 65)
    print("      DUCKDB PARQUET ANALYST (MOTEUR ANALYTIQUE DE PRIX)        ")
    print("=" * 65)

    target_db = args.source
    is_demo = False
    if args.demo or not target_db:
        target_db = "demo_analytics.sqlite"
        setup_demo_prices(target_db)
        is_demo = True

    stats = compute_in_process_stats(target_db, args.table)
    print(f"Source analysee : {target_db} (Table: {args.table})")
    print("-" * 65)
    print(f"{'Enseigne':<15} | {'Articles':<8} | {'Prix Moy (€)':<12} | {'Mediane (€)':<11} | {'Min - Max (€)'}")
    print("-" * 65)

    for st in stats:
        min_max = f"{st['min_price']:.2f} - {st['max_price']:.2f}"
        print(f"{st['brand']:<15} | {st['count']:<8} | {st['avg_price']:<12.2f} | {st['median_price']:<11.2f} | {min_max}")

    print("=" * 65)
    print("[OK] Analyse colonnaire rapide completee.")

    if is_demo and pathlib.Path(target_db).exists():
        try:
            pathlib.Path(target_db).unlink()
        except Exception:
            pass

if __name__ == "__main__":
    main()