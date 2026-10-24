# -*- coding: utf-8 -*-
"""
audit_dataset_quality.py - Andrew Ng Data-Centric AI Quality Sentinel
Auditeur de completude, de doublons, de purete de type et de valeurs aberrantes.
"""

import sqlite3
import pathlib
import argparse
from typing import TypedDict, List, Dict, Tuple

class QualityReport(TypedDict):
    total_rows: int
    completeness_score: float
    duplicate_rows: int
    invalid_prices: int
    overall_quality_score: float

def audit_sqlite_table(db_path: str, table_name: str) -> QualityReport:
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute(f"SELECT COUNT(*) FROM {table_name};")
    total_rows = cur.fetchone()[0]

    if total_rows == 0:
        conn.close()
        return {
            "total_rows": 0,
            "completeness_score": 100.0,
            "duplicate_rows": 0,
            "invalid_prices": 0,
            "overall_quality_score": 100.0,
        }

    # 1. Null / Empty checks
    cur.execute(f"PRAGMA table_info('{table_name}');")
    cols = [r[1] for r in cur.fetchall()]
    null_counts = 0
    for c in cols:
        cur.execute(f"SELECT COUNT(*) FROM {table_name} WHERE {c} IS NULL OR {c} = '';")
        null_counts += cur.fetchone()[0]

    completeness = max(0.0, 100.0 - (null_counts / (total_rows * len(cols)) * 100.0))

    # 2. Duplicate check
    cur.execute(f"SELECT COUNT(*) FROM (SELECT {', '.join(cols)}, COUNT(*) FROM {table_name} GROUP BY {', '.join(cols)} HAVING COUNT(*) > 1);")
    dupe_groups = cur.fetchone()[0]

    # 3. Invalid prices if price column exists
    invalid_prices = 0
    if "price" in cols:
        cur.execute(f"SELECT COUNT(*) FROM {table_name} WHERE price <= 0 OR price IS NULL OR typeof(price) NOT IN ('integer', 'real');")
        invalid_prices = cur.fetchone()[0]

    conn.close()

    penalty = (100.0 - completeness) * 0.5 + (dupe_groups * 5) + (invalid_prices * 5)
    overall_score = max(0.0, min(100.0, 100.0 - penalty))

    return {
        "total_rows": total_rows,
        "completeness_score": round(completeness, 1),
        "duplicate_rows": dupe_groups,
        "invalid_prices": invalid_prices,
        "overall_quality_score": round(overall_score, 1),
    }

def create_demo_data(db_path: str) -> None:
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, brand TEXT, price REAL);")
    data = [
        (1, "Lait Demi-Ecreme 1L", "Colruyt", 0.95),
        (2, "Lait Demi-Ecreme 1L", "Colruyt", 0.95), # Duplicat intentionnel
        (3, "Cafe Moulu 500g", "Delhaize", 4.15),
        (4, None, "Delhaize", 2.50),                # Valeur nulle
        (5, "Chocolat Noir 100g", "Colruyt", -1.20),  # Prix negatif aberrant
    ]
    cur.executemany("INSERT INTO products VALUES (?, ?, ?, ?);", data)
    conn.commit()
    conn.close()

def main():
    parser = argparse.ArgumentParser(description="Data Quality Sentinel (Andrew Ng Data-Centric AI Standard)")
    parser.add_argument("--db", type=str, help="Fichier SQLite contenant le jeu de donnees")
    parser.add_argument("--table", type=str, default="products", help="Table a auditer")
    parser.add_argument("--demo", action="store_true", help="Creer et auditer un jeu de donnees d exemple")
    args = parser.parse_args()

    print("=" * 65)
    print("      DATA QUALITY SENTINEL (STANDARD ANDREW NG - DATA-CENTRIC) ")
    print("=" * 65)

    target_db = args.db
    is_demo = False
    if args.demo or not target_db:
        target_db = "demo_quality.sqlite"
        create_demo_data(target_db)
        is_demo = True

    p = pathlib.Path(target_db)
    rep = audit_sqlite_table(str(p), args.table)

    print(f"Jeu de donnees analyse : {p.resolve()} (Table: {args.table})")
    print(f"Total Enregistrements  : {rep['total_rows']}")
    print(f"Completude des champs  : {rep['completeness_score']} %")
    print(f"Lignes dupliquees      : {rep['duplicate_rows']}")
    print(f"Prix invalides / <= 0  : {rep['invalid_prices']}")
    print(f"Note Globale de Qualite: {rep['overall_quality_score']} / 100")
    print("-" * 65)

    if rep["overall_quality_score"] >= 85.0:
        print("[OK] Jeu de donnees sain et pret pour l analyse ou le fine-tuning.")
    else:
        print("[!] Anomalies de donnees detectees. Nettoyage prealable recommande.")
    print("=" * 65)

    if is_demo and p.exists():
        try:
            p.unlink()
        except Exception:
            pass

if __name__ == "__main__":
    main()