# -*- coding: utf-8 -*-
"""
tdd_cycle_checker.py - Test-Driven Development Cycle Checker
Contrôleur de conformite du cycle Red-Green-Refactor.
"""

import sys
import unittest
import pathlib
import argparse
import time
from typing import TypedDict, List, Dict, Tuple

class TDDReport(TypedDict):
    total_tests: int
    failures: int
    errors: int
    passed: int
    duration_ms: float
    current_phase: str

def run_tests_in_path(test_path: pathlib.Path) -> TDDReport:
    start_t = time.perf_counter()
    loader = unittest.TestLoader()
    if test_path.is_file():
        suite = loader.loadTestsFromName(test_path.stem)
    else:
        suite = loader.discover(str(test_path), pattern="test_*.py")

    runner = unittest.TextTestRunner(stream=sys.stdout, verbosity=1)
    result = runner.run(suite)
    duration_ms = (time.perf_counter() - start_t) * 1000.0

    failures = len(result.failures)
    errors = len(result.errors)
    total = result.testsRun
    passed = total - (failures + errors)

    if total == 0:
        phase = "EMPTY (Aucun test trouve)"
    elif failures > 0 or errors > 0:
        phase = "RED (Tests en echec - Prêt pour implementation)"
    else:
        phase = "GREEN (Tous les tests passent - Prêt pour Refactor)"

    return {
        "total_tests": total,
        "failures": failures,
        "errors": errors,
        "passed": passed,
        "duration_ms": duration_ms,
        "current_phase": phase,
    }

def main():
    parser = argparse.ArgumentParser(description="TDD Cycle Checker - Validateur de cycle Rouge-Vert-Refactor")
    parser.add_argument("--test-dir", type=str, help="Dossier de tests unitaires")
    parser.add_argument("--test-file", type=str, help="Fichier de test specifique")
    args = parser.parse_args()

    print("=" * 65)
    print("      TEST-DRIVEN DEVELOPMENT (CONTROLEUR DE CYCLE TDD)       ")
    print("=" * 65)

    target = pathlib.Path(args.test_file if args.test_file else (args.test_dir if args.test_dir else "."))
    print(f"Cible evaluee : {target.resolve()}")

    report = run_tests_in_path(target)

    print("-" * 65)
    print(f"Total Tests Lances : {report['total_tests']}")
    print(f"  - Reussis        : {report['passed']}")
    print(f"  - Echecs         : {report['failures']}")
    print(f"  - Erreurs        : {report['errors']}")
    print(f"Duree Execution    : {report['duration_ms']:.1f} ms")
    print(f"Phase TDD Actuelle : {report['current_phase']}")
    print("=" * 65)

if __name__ == "__main__":
    main()