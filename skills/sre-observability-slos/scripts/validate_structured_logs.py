# -*- coding: utf-8 -*-
"""
validate_structured_logs.py - Charity Majors Observability Validator
Valide la structure JSON des logs, les champs de haute cardinalite et les metriques de temps.
"""

import json
import pathlib
import argparse
from typing import TypedDict, List, Dict, Tuple

class LogCheckResult(TypedDict):
    line_num: int
    is_json: bool
    missing_fields: List[str]
    has_duration: bool
    has_trace_id: bool

MANDATORY_FIELDS = ["timestamp", "level", "event"]
RECOMMENDED_FIELDS = ["trace_id", "duration_ms"]

def audit_log_line(line_str: str, line_num: int) -> LogCheckResult:
    stripped = line_str.strip()
    if not stripped:
        return {
            "line_num": line_num,
            "is_json": False,
            "missing_fields": [],
            "has_duration": False,
            "has_trace_id": False,
        }

    try:
        data = json.loads(stripped)
        if not isinstance(data, dict):
            return {"line_num": line_num, "is_json": False, "missing_fields": [], "has_duration": False, "has_trace_id": False}
    except Exception:
        return {"line_num": line_num, "is_json": False, "missing_fields": [], "has_duration": False, "has_trace_id": False}

    missing = [f for f in MANDATORY_FIELDS if f not in data]
    return {
        "line_num": line_num,
        "is_json": True,
        "missing_fields": missing,
        "has_duration": "duration_ms" in data,
        "has_trace_id": "trace_id" in data or "request_id" in data,
    }

def create_demo_logs(file_path: str) -> None:
    events = [
        {"timestamp": "2026-10-19T19:55:01Z", "level": "INFO", "event": "scraper_started", "brand": "Colruyt", "trace_id": "tr-101"},
        {"timestamp": "2026-10-19T19:55:03Z", "level": "INFO", "event": "products_extracted", "brand": "Colruyt", "count": 250, "duration_ms": 1420.5, "trace_id": "tr-101"},
        "Texte brut non structure qui ne respecte pas le standard ODD",
        {"timestamp": "2026-10-19T19:55:05Z", "level": "ERROR", "event": "http_timeout", "brand": "Delhaize", "duration_ms": 5000.0, "trace_id": "tr-102", "error": "ConnectTimeout"},
    ]
    with open(file_path, "w", encoding="utf-8") as f:
        for ev in events:
            if isinstance(ev, dict):
                f.write(json.dumps(ev) + "\n")
            else:
                f.write(str(ev) + "\n")

def main():
    parser = argparse.ArgumentParser(description="Observability Engineer - Validateur de logs ODD (Charity Majors)")
    parser.add_argument("--log-file", type=str, help="Fichier de logs a inspecter")
    parser.add_argument("--demo", action="store_true", help="Creer et valider des logs de demonstration")
    args = parser.parse_args()

    print("=" * 65)
    print("      OBSERVABILITY ENGINEER (STANDARD CHARITY MAJORS - ODD)    ")
    print("=" * 65)

    target_file = args.log_file
    is_demo = False
    if args.demo or not target_file:
        target_file = "demo_odd.log"
        create_demo_logs(target_file)
        is_demo = True

    p = pathlib.Path(target_file)
    lines = p.read_text(encoding="utf-8", errors="ignore").splitlines()

    results = [audit_log_line(l, idx) for idx, l in enumerate(lines, start=1) if l.strip()]
    json_count = sum(1 for r in results if r["is_json"])
    unstructured_count = len(results) - json_count
    with_trace = sum(1 for r in results if r["has_trace_id"])

    odd_score = max(0, int((json_count / len(results) * 60) + (with_trace / len(results) * 40))) if results else 0

    print(f"Fichier analyse : {p.resolve()}")
    print(f"Total evenements : {len(results)}")
    print(f"  - Evenements JSON valides    : {json_count}")
    print(f"  - Lignes de texte brut (Non ODD) : {unstructured_count}")
    print(f"  - Traces avec trace_id / duree : {with_trace}")
    print(f"Score de Maturite Observabilite : {odd_score} / 100")
    print("-" * 65)

    for r in results:
        if not r["is_json"]:
            print(f"[NON-CONFORME] Ligne {r['line_num']} : Ligne de texte brut au lieu d un objet JSON structure.")
        elif r["missing_fields"]:
            print(f"[CHAMPS MANQUANTS] Ligne {r['line_num']} : Champs requis manquants {r['missing_fields']}")

    if odd_score >= 85:
        print("[OK] Journalisation hautement observable et conforme aux standards ODD.")
    print("=" * 65)

    if is_demo and p.exists():
        try:
            p.unlink()
        except Exception:
            pass

if __name__ == "__main__":
    main()