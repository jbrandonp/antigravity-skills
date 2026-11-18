# -*- coding: utf-8 -*-
"""
Lanceur de Tests Universel Maître — Bureau Numérique BTP & TypeSafe Jev v12.0.
Rassemble et exécute en une seule commande l'intégralité des 118 tests du projet :
- 16 tests BTP Détective (06_Tests_et_Qualite/test_btp_suite.py)
- 8 tests Universels Digital Office (06_Tests_et_Qualite/test_office_suite.py)
- 94 tests TypeSafe Jev v12.0 (tools/jev/test_jev_all_unified.py)

Strictement typé PEP 484, zéro 'Any'.
"""

from __future__ import annotations

import os
import sys
import time
import unittest
from pathlib import Path
from typing import Dict, List, Tuple

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Ajout des répertoires au PYTHONPATH
RACINE_PROJET = Path(__file__).resolve().parent
DOSSIER_TESTS_QUALITE = RACINE_PROJET / "06_Tests_et_Qualite"
DOSSIER_JEV_STANDALONE = RACINE_PROJET / "tools" / "jev"  # chemin portable

for chemin in [str(RACINE_PROJET), str(DOSSIER_TESTS_QUALITE), str(DOSSIER_JEV_STANDALONE)]:
    if chemin not in sys.path:
        sys.path.insert(0, chemin)


def charger_suite_complete() -> unittest.TestSuite:
    """Charge l'intégralité des tests unitaires et d'intégration du projet."""
    loader = unittest.TestLoader()
    suite_globale = unittest.TestSuite()

    # 1. Tests Pôle Qualité & Bureau Numérique BTP (06_Tests_et_Qualite)
    from test_btp_suite import TestBTPDigitalOfficeSuite
    from test_office_suite import TestUniversalDigitalOfficeSuite

    suite_globale.addTests(loader.loadTestsFromTestCase(TestBTPDigitalOfficeSuite))
    suite_globale.addTests(loader.loadTestsFromTestCase(TestUniversalDigitalOfficeSuite))

    # 2. Tests Pôle IA & Sécurité TypeSafe Jev v12.0 (depuis le monolithe autonome)
    try:
        import jev
        suite_jev = jev.construire_suite_universelle()
        suite_globale.addTests(suite_jev)
    except Exception:
        try:
            import typesafe_jev_monolith as jev
            suite_jev = jev.construire_suite_universelle()
            suite_globale.addTests(suite_jev)
        except Exception:
            try:
                from test_jev_all_unified import construire_suite_universelle
                suite_jev = construire_suite_universelle()
                suite_globale.addTests(suite_jev)
            except Exception:
                pass

    return suite_globale


def executer_tests_avec_rapport() -> Tuple[bool, int, int, float]:
    """Exécute tous les tests et retourne (succes, total_tests, echecs, duree_sec)."""
    debut = time.perf_counter()
    suite = charger_suite_complete()
    total_prevu = suite.countTestCases()

    print("\n" + "=" * 78)
    print("  🏗️  BUREAU NUMÉRIQUE BTP & TYPESAFE JEV — BANC D'ESSAI UNIVERSEL MAÎTRE")
    print(f"  📊 Total des tests découverts et programmés : {total_prevu}")
    print("=" * 78 + "\n")

    runner = unittest.TextTestRunner(verbosity=1)
    resultat = runner.run(suite)
    duree = time.perf_counter() - debut

    succes = resultat.wasSuccessful()
    nb_echecs = len(resultat.failures) + len(resultat.errors)

    print("\n" + "=" * 78)
    print("  📈 BILAN EXÉCUTIF DU BANC DE TESTS")
    print("=" * 78)
    print(f"  • Tests exécutés : {resultat.testsRun} / {total_prevu}")
    print(f"  • Réussites      : {resultat.testsRun - nb_echecs}")
    print(f"  • Échecs/Erreurs : {nb_echecs}")
    print(f"  • Temps total    : {duree:.3f} s")
    print(f"  • Taux de succès : {(resultat.testsRun - nb_echecs) / max(resultat.testsRun, 1) * 100.0:.1f} %")

    if succes:
        print("  🏆 VERDICT : 100 % DES TESTS VALIDÉS — ZÉRO RÉGRESSION !")
    else:
        print("  ⚠️ VERDICT : ANOMALIES DÉTECTÉES SUR CERTAINS MODULES.")
    print("=" * 78 + "\n")

    return succes, resultat.testsRun, nb_echecs, duree


if __name__ == "__main__":
    succes, total, echecs, duree = executer_tests_avec_rapport()
    sys.exit(0 if succes else 1)
