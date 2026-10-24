# -*- coding: utf-8 -*-
"""
sqlite_migration_differ.py - Schema Migration Sentinel
Detecteur de derive de schema SQLite et generateur de scripts de migration securises.
"""

import os
import sys
import sqlite3
import pathlib
import argparse
from typing import TypedDict, List, Dict, Tuple, Set

class ColumnInfo(TypedDict):
    cid: int
    name: str
    col_type: str
    notnull: int
    default_val: str
    pk: int

class DriftReport(TypedDict):
    table_name: str
    missing_columns: List[str]
    extra_columns: List[str]
    is_missing_table: bool

def inspect_columns(conn: sqlite3.Connection, table_name: str) -> Dict[str, ColumnInfo]:
    cur = conn.cursor()
    cur.execute(f"PRAGMA table_info('{table_name}');")
    cols: Dict[str, ColumnInfo] = {}
    for r in cur.fetchall():
        cols[r[1]] = {
            "cid": r[0],
            "name": r[1],
            "col_type": r[2].upper(),
            "notnull": r[3],
            "default_val": str(r[4]),
            "pk": r[5],
        }
    return cols

def audit_schema_drift(live_db_path: str, reference_db_path: str) -> List[DriftReport]:
    reports: List[DriftReport] = []
    conn_live = sqlite3.connect(live_db_path)
    conn_ref = sqlite3.connect(reference_db_path)

    cur_ref = conn_ref.cursor()
    cur_ref.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    ref_tables = [r[0] for r in cur_ref.fetchall()]

    cur_live = conn_live.cursor()
    cur_live.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    live_tables = set(r[0] for r in cur_live.fetchall())

    for tbl in ref_tables:
        if tbl not in live_tables:
            reports.append({
                "table_name": tbl,
                "missing_columns": [],
                "extra_columns": [],
                "is_missing_table": True,
            })
            continue

        ref_cols = inspect_columns(conn_ref, tbl)
        live_cols = inspect_columns(conn_live, tbl)

        missing = [c for c in ref_cols.keys() if c not in live_cols]
        extra = [c for c in live_cols.keys() if c not in ref_cols]

        if missing or extra:
            reports.append({
                "table_name": tbl,
                "missing_columns": missing,
                "extra_columns": extra,
                "is_missing_table": False,
            })

    conn_live.close()
    conn_ref.close()
    return reports

def setup_demo_databases() -> Tuple[str, str]:
    live_p = "demo_live.sqlite"
    ref_p = "demo_ref.sqlite"

    for p in [live_p, ref_p]:
        if os.path.exists(p):
            try:
                os.remove(p)
            except Exception:
                pass

    conn_l = sqlite3.connect(live_p)
    conn_l.execute("CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, price REAL);")
    conn_l.commit()
    conn_l.close()

    conn_r = sqlite3.connect(ref_p)
    conn_r.execute("CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, price REAL, barcode TEXT, store_id INTEGER);")
    conn_r.execute("CREATE TABLE stores (id INTEGER PRIMARY KEY, name TEXT);")
    conn_r.commit()
    conn_r.close()

    return live_p, ref_p

def main():
    parser = argparse.ArgumentParser(description="Schema Migration Sentinel - SQLite Schema Differ")
    parser.add_argument("--live-db", type=str, help="Base SQLite active")
    parser.add_argument("--ref-db", type=str, help="Base SQLite de reference")
    parser.add_argument("--demo", action="store_true", help="Lancer un test de demonstration")
    args = parser.parse_args()

    print("=" * 65)
    print("      SCHEMA MIGRATION SENTINEL (DETECTION DE DERIVE SQLITE)    ")
    print("=" * 65)

    is_demo = args.demo or not (args.live_db and args.ref_db)
    if is_demo:
        live_p, ref_p = setup_demo_databases()
    else:
        live_p, ref_p = args.live_db, args.ref_db

    print(f"Base Active     : {live_p}")
    print(f"Base Reference  : {ref_p}")
    print("-" * 65)

    drifts = audit_schema_drift(live_p, ref_p)

    if not drifts:
        print("[OK] Aucun ecart de schema detecte. Les tables sont 100% synchronisees.")
    else:
        print(f"[!] {len(drifts)} anomalie(s) de schema detectee(s) :")
        for d in drifts:
            if d["is_missing_table"]:
                print(f"  [TABLE MANQUANTE] Table '{d['table_name']}' absente de la base active.")
                print(f"     -> Suggestion : Generer script CREATE TABLE.")
            else:
                print(f"  [DERIVE COLONNES] Table '{d['table_name']}' :")
                if d["missing_columns"]:
                    print(f"     -> Colonnes a ajouter : {', '.join(d['missing_columns'])}")
                    for col in d["missing_columns"]:
                        print(f"        SQL: ALTER TABLE {d['table_name']} ADD COLUMN {col} TEXT;")
                if d["extra_columns"]:
                    print(f"     -> Colonnes orphelines : {', '.join(d['extra_columns'])}")

    print("=" * 65)

    if is_demo:
        for p in [live_p, ref_p]:
            if os.path.exists(p):
                try:
                    os.remove(p)
                except Exception:
                    pass

if __name__ == "__main__":
    main()