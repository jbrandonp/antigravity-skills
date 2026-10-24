# -*- coding: utf-8 -*-
"""
sqlite_detective.py - Simon Willison Datasette SQLite Detective
Diagnostic d integrite, de PRAGMAs (WAL/NORMAL), et detection des index manquants.
"""

import os
import sys
import sqlite3
import pathlib
import argparse
from typing import TypedDict, List, Dict, Tuple

class DiagnosticResult(TypedDict):
    category: str
    status: str
    detail: str

def inspect_sqlite_database(db_path: str) -> Tuple[List[DiagnosticResult], int]:
    results: List[DiagnosticResult] = []
    penalty = 0

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
    except Exception as e:
        results.append({"category": "Connection", "status": "FAIL", "detail": f"Erreur d ouverture : {e}"})
        return results, 100

    # 1. Verification WAL Mode
    cursor.execute("PRAGMA journal_mode;")
    j_mode = cursor.fetchone()[0].upper()
    if j_mode == "WAL":
        results.append({"category": "PRAGMA", "status": "PASS", "detail": "journal_mode = WAL (Optimal pour concurrence)"})
    else:
        results.append({"category": "PRAGMA", "status": "WARN", "detail": f"journal_mode = {j_mode} (Recommande: WAL)"})
        penalty += 15

    # 2. Verification Synchronous
    cursor.execute("PRAGMA synchronous;")
    sync_mode = cursor.fetchone()[0]
    # 1 = NORMAL, 2 = FULL
    if sync_mode in (1, "1", "NORMAL"):
        results.append({"category": "PRAGMA", "status": "PASS", "detail": "synchronous = NORMAL (Optimal en mode WAL)"})
    else:
        results.append({"category": "PRAGMA", "status": "WARN", "detail": f"synchronous = {sync_mode} (Recommande: NORMAL)"})
        penalty += 10

    # 3. Integrity Check
    cursor.execute("PRAGMA integrity_check;")
    integrity = cursor.fetchall()
    if len(integrity) == 1 and integrity[0][0] == "ok":
        results.append({"category": "Integrity", "status": "PASS", "detail": "B-Tree integrity_check = OK"})
    else:
        results.append({"category": "Integrity", "status": "FAIL", "detail": f"Anomalies detectees : {integrity}"})
        penalty += 40

    # 4. Foreign Key Check
    cursor.execute("PRAGMA foreign_key_check;")
    fk_errors = cursor.fetchall()
    if not fk_errors:
        results.append({"category": "Foreign Keys", "status": "PASS", "detail": "Aucune violation de cle etrangere (Orphan rows: 0)"})
    else:
        results.append({"category": "Foreign Keys", "status": "FAIL", "detail": f"{len(fk_errors)} violation(s) de cle etrangere"})
        penalty += 25

    # 5. Detection des index manquants sur les cles etrangeres
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    tables = [r[0] for r in cursor.fetchall()]

    missing_fk_indexes = 0
    for tbl in tables:
        cursor.execute(f"PRAGMA foreign_key_list('{tbl}');")
        fks = cursor.fetchall()
        if not fks:
            continue

        cursor.execute(f"PRAGMA index_list('{tbl}');")
        indexes = cursor.fetchall()
        indexed_cols: List[str] = []
        for idx in indexes:
            idx_name = idx[1]
            cursor.execute(f"PRAGMA index_info('{idx_name}');")
            for col_info in cursor.fetchall():
                indexed_cols.append(col_info[2])

        for fk in fks:
            from_col = fk[3]
            if from_col not in indexed_cols:
                missing_fk_indexes += 1
                results.append({
                    "category": "Indexing",
                    "status": "WARN",
                    "detail": f"Table '{tbl}': cle etrangere '{from_col}' NON indexee -> Risque de Full Table Scan",
                })
                penalty += 10

    if missing_fk_indexes == 0:
        results.append({"category": "Indexing", "status": "PASS", "detail": "Toutes les cles etrangeres possedent un index dedie"})

    conn.close()
    health_score = max(0, 100 - penalty)
    return results, health_score

def setup_demo_db() -> str:
    path = "demo_detective.sqlite"
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.execute("PRAGMA journal_mode = WAL;")
    cur.execute("PRAGMA synchronous = NORMAL;")
    cur.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT);")
    cur.execute("CREATE TABLE orders (id INTEGER PRIMARY KEY, user_id INTEGER, amount REAL, FOREIGN KEY(user_id) REFERENCES users(id));")
    cur.execute("CREATE INDEX idx_orders_user_id ON orders(user_id);")
    cur.execute("INSERT INTO users VALUES (1, 'Brandon');")
    cur.execute("INSERT INTO orders VALUES (101, 1, 49.99);")
    conn.commit()
    conn.close()
    return path

def main():
    parser = argparse.ArgumentParser(description="Datasette SQLite Detective (Simon Willison Standard)")
    parser.add_argument("--db", type=str, help="Chemin vers la base SQLite a diagnostiquer")
    parser.add_argument("--demo", action="store_true", help="Creer et auditer une base de demonstration")
    args = parser.parse_args()

    print("=" * 65)
    print("      DATASETTE SQLITE DETECTIVE (SIMON WILLISON STANDARD)      ")
    print("=" * 65)

    target_db = args.db
    is_demo = False
    if args.demo or not target_db:
        target_db = setup_demo_db()
        is_demo = True

    print(f"Base diagnostiquee : {target_db}")
    results, score = inspect_sqlite_database(target_db)

    for r in results:
        status_tag = f"[{r['status']}]"
        print(f"{status_tag:<8} {r['category']:<15} : {r['detail']}")

    print("-" * 65)
    print(f"Score de Sante Base SQLite : {score} / 100")
    if score >= 90:
        print("[OK] Base de donnees parfaitement conforme aux standards SOTA.")
    else:
        print("[!] Optimisations requises (voir alertes ci-dessus).")
    print("=" * 65)

    if is_demo and os.path.exists(target_db):
        try:
            os.remove(target_db)
            if os.path.exists(target_db + "-wal"):
                os.remove(target_db + "-wal")
            if os.path.exists(target_db + "-shm"):
                os.remove(target_db + "-shm")
        except Exception:
            pass

if __name__ == "__main__":
    main()