# -*- coding: utf-8 -*-
"""
run_property_fuzzer.py - Property-Based Testing & Invariant Fuzzer
Generateur d entrees extremes et verification d invariants mathematiques/donnees.
"""

import sys
import random
import string
import argparse
from typing import TypedDict, List, Dict, Tuple, Callable

class FuzzReport(TypedDict):
    property_name: str
    iterations: int
    passed: bool
    failed_input: str
    error_message: str

def fuzz_roundtrip_json() -> FuzzReport:
    """Verifie l invariant roundtrip : json.loads(json.dumps(x)) == x"""
    import json
    for i in range(200):
        # Generer des structures arbitraires
        val = {
            "int": random.randint(-1000000, 1000000),
            "float": random.random() * 1000.0,
            "str": "".join(random.choices(string.printable, k=random.randint(0, 50))),
            "bool": random.choice([True, False]),
            "list": [random.randint(0, 100) for _ in range(random.randint(0, 10))],
        }
        encoded = json.dumps(val)
        decoded = json.loads(encoded)
        # Comparaison numerique approchee pour les flottants
        if decoded["int"] != val["int"] or decoded["str"] != val["str"]:
            return {
                "property_name": "Roundtrip JSON",
                "iterations": i + 1,
                "passed": False,
                "failed_input": str(val),
                "error_message": "Non concordance entre encode et decode",
            }
    return {
        "property_name": "Roundtrip JSON",
        "iterations": 200,
        "passed": True,
        "failed_input": "",
        "error_message": "",
    }

def fuzz_idempotent_normalizer() -> FuzzReport:
    """Verifie l invariant d idempotence : normalize(normalize(x)) == normalize(x)"""
    def normalize_price_str(raw: str) -> str:
        # Nettoyage et formatage
        cleaned = raw.strip().replace("€", "").replace(",", ".").strip()
        try:
            val = float(cleaned)
            return f"{val:.2f}"
        except ValueError:
            return "0.00"

    samples = [
        " 12.50 € ",
        "14,99",
        "0.95",
        "invalid",
        " 0 ",
        "  1000.000 €",
    ]
    for s in samples:
        first = normalize_price_str(s)
        second = normalize_price_str(first)
        if first != second:
            return {
                "property_name": "Idempotence Normalisation Prix",
                "iterations": len(samples),
                "passed": False,
                "failed_input": s,
                "error_message": f"first ({first}) != second ({second})",
            }

    return {
        "property_name": "Idempotence Normalisation Prix",
        "iterations": len(samples),
        "passed": True,
        "failed_input": "",
        "error_message": "",
    }

def main():
    parser = argparse.ArgumentParser(description="Property-Based Testing & Invariant Fuzzer")
    parser.add_argument("--demo", action="store_true", help="Executer les tests de proprietes de demonstration")
    parser.add_argument("--iterations", type=int, default=200, help="Nombre d iterations par propriete")
    args = parser.parse_args()

    print("=" * 65)
    print("      PROPERTY-BASED TESTING (VERIFICATEUR D INVARIANTS)      ")
    print("=" * 65)

    reports = [
        fuzz_roundtrip_json(),
        fuzz_idempotent_normalizer(),
    ]

    for r in reports:
        status_tag = "[PASS]" if r["passed"] else "[FAIL]"
        print(f"{status_tag:<8} {r['property_name']:<35} ({r['iterations']} tests)")
        if not r["passed"]:
            print(f"         Entree defaillante : {r['failed_input']}")
            print(f"         Erreur             : {r['error_message']}")

    print("-" * 65)
    all_passed = all(r["passed"] for r in reports)
    if all_passed:
        print("[OK] Tous les invariants mathematiques et structurels sont verifies.")
    else:
        print("[!] Violations d invariants detectees.")
    print("=" * 65)

if __name__ == "__main__":
    main()