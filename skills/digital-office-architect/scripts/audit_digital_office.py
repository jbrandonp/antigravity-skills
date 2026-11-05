"""
Outil universel d'audit de qualité et de conformité pour le Bureau Numérique.
Valide l'arborescence, l'intégrité du classeur Excel, le zonage de protection,
les formules vivantes, le contrat légal et l'exécution de la suite unitaire.
Calcul un score de conformité sur 100 points. Strictement typé, zéro 'Any'.
"""

import argparse
import os
import subprocess
import sys
from typing import Dict, Final, List, Optional, Tuple, TypedDict
import openpyxl

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


class AuditCheckItem(TypedDict):
    name: str
    weight: float
    score: float
    passed: bool
    details: str


class AuditReport(TypedDict):
    workspace_dir: str
    global_score: float
    total_checks: int
    passed_checks: int
    items: List[AuditCheckItem]
    status: str


def audit_universal_workspace(workspace_dir: str) -> AuditReport:
    """
    Exécute un audit complet de conformité sur un espace Bureau Numérique (BTP ou Tous Secteurs).
    """
    items: List[AuditCheckItem] = []

    # -------------------------------------------------------------------------
    # 1. Audit de l'Arborescence des 6 Dossiers (Poids : 20 points)
    # -------------------------------------------------------------------------
    expected_prefixes = [
        "01_Strategie",
        "02_",  # Accepte Candidature_Smart_Liege ou Structure_Legale_et_Conformite
        "03_Vente",
        "04_Operations",
        "05_Outils",
        "06_Tests",
    ]

    found_folders = os.listdir(workspace_dir) if os.path.isdir(workspace_dir) else []
    missing_prefixes: List[str] = []

    for prefix in expected_prefixes:
        matched = any(f.startswith(prefix) and os.path.isdir(os.path.join(workspace_dir, f)) for f in found_folders)
        if not matched:
            missing_prefixes.append(prefix)

    passed_folders = len(missing_prefixes) == 0
    score_folders = 20.0 if passed_folders else max(0.0, 20.0 * (1.0 - len(missing_prefixes) / len(expected_prefixes)))
    items.append({
        "name": "Arborescence Standardisée (6 dossiers ordonnés)",
        "weight": 20.0,
        "score": round(score_folders, 1),
        "passed": passed_folders,
        "details": "Tous les 6 dossiers sont présents." if passed_folders else f"Dossiers manquants (préfixes) : {', '.join(missing_prefixes)}",
    })

    # -------------------------------------------------------------------------
    # 2. Audit du Classeur Excel et Zonage des Cellules (Poids : 30 points)
    # -------------------------------------------------------------------------
    outils_dir = os.path.join(workspace_dir, "05_Outils_et_Modeles_Excel")
    excel_candidates = [
        os.path.join(outils_dir, "SUIVI_AFFAIRES_MODELE_PRO.xlsx"),
        os.path.join(outils_dir, "DEVIS_SANS_OUBLI_MODELE_PRO.xlsx"),
    ]
    excel_path = next((p for p in excel_candidates if os.path.isfile(p)), "")

    excel_score = 0.0
    excel_details: List[str] = []

    if excel_path:
        try:
            wb = openpyxl.load_workbook(excel_path, data_only=False)
            has_dash = "Tableau de Bord" in wb.sheetnames
            has_rituel = "Rituel Hebdomadaire" in wb.sheetnames
            has_suivi = len(wb.sheetnames) >= 3

            if has_suivi and has_dash and has_rituel:
                excel_score += 10.0
                excel_details.append("3 feuilles obligatoires présentes")
            else:
                excel_details.append(f"Feuilles détectées : {wb.sheetnames}")

            ws_main = wb[wb.sheetnames[0]]
            is_protected = bool(ws_main.protection.sheet)
            if is_protected:
                excel_score += 5.0
                excel_details.append("Feuille protégée par mot de passe")
            else:
                excel_details.append("Feuille NON protégée")

            # Vérifier déverrouillage colonnes 1-8, 10, 11 et verrouillage colonne 9
            sample_row = 5
            unlocked_inputs = True
            for col in (1, 2, 3, 4, 5, 6, 7, 8, 10, 11):
                cell_prot = ws_main.cell(row=sample_row, column=col).protection
                if cell_prot and cell_prot.locked:
                    unlocked_inputs = False
                    break

            col9_prot = ws_main.cell(row=sample_row, column=9).protection
            col9_locked = col9_prot is None or bool(col9_prot.locked)

            if unlocked_inputs and col9_locked:
                excel_score += 10.0
                excel_details.append("Zonage ergonomique validé (Saisie libre cols 1-8/10/11, Formule verrouillée col 9)")
            else:
                excel_details.append(f"Erreur zonage : Inputs déverrouillés={unlocked_inputs}, Col 9 verrouillée={col9_locked}")

            # Vérifier la présence de formules vivantes sur lignes vides
            empty_row_formula_h = str(ws_main.cell(row=20, column=8).value or "")
            empty_row_formula_i = str(ws_main.cell(row=20, column=9).value or "")
            if empty_row_formula_h.startswith("=") and empty_row_formula_i.startswith("="):
                excel_score += 5.0
                excel_details.append("Formules vivantes injectées dans les lignes vides")
            else:
                excel_details.append("Formules absentes des lignes futures")

        except Exception as exc:
            excel_details.append(f"Erreur d'analyse openpyxl : {exc}")
    else:
        excel_details.append("Classeur Excel professionnel introuvable dans 05_Outils_et_Modeles_Excel")

    items.append({
        "name": "Intégrité Excel & Ergonomie (Zonage & Formules)",
        "weight": 30.0,
        "score": round(excel_score, 1),
        "passed": excel_score >= 25.0,
        "details": " | ".join(excel_details),
    })

    # -------------------------------------------------------------------------
    # 3. Audit Exportation CSV & Filtrage des Disclaimers (Poids : 20 points)
    # -------------------------------------------------------------------------
    csv_candidates = [
        os.path.join(outils_dir, "EXPORTS_AFFAIRES_ERP_COMPATIBLE.csv"),
        os.path.join(outils_dir, "EXPORTS_DEVIS_ERP_COMPATIBLE.csv"),
    ]
    csv_path = next((p for p in csv_candidates if os.path.isfile(p)), "")

    csv_score = 0.0
    csv_details: List[str] = []

    if csv_path:
        try:
            with open(csv_path, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f if line.strip()]

            if len(lines) >= 2:
                csv_score += 10.0
                csv_details.append(f"Lignes CSV valides ({len(lines)} lignes)")
            else:
                csv_details.append("Fichier CSV vide ou incomplet")

            has_disclaimer = any("AVERTISSEMENT" in l.upper() or "PROTECTION" in l.upper() for l in lines)
            if not has_disclaimer:
                csv_score += 10.0
                csv_details.append("Pied de page filtré avec succès (zéro ligne fantôme)")
            else:
                csv_details.append("Ligne de disclaimer non filtrée détectée !")

        except Exception as exc:
            csv_details.append(f"Erreur lecture CSV : {exc}")
    else:
        csv_details.append("Fichier CSV exporté introuvable")

    items.append({
        "name": "Exportation ERP & Filtrage des Disclaimers",
        "weight": 20.0,
        "score": round(csv_score, 1),
        "passed": csv_score >= 18.0,
        "details": " | ".join(csv_details),
    })

    # -------------------------------------------------------------------------
    # 4. Audit Couverture Juridique & CGV de Protection (Poids : 15 points)
    # -------------------------------------------------------------------------
    vente_dir = next((os.path.join(workspace_dir, f) for f in found_folders if f.startswith("03_")), "")
    contract_path = os.path.join(vente_dir, "BON_DE_COMMANDE_PROPOSITION_COMMERCIALE.md") if vente_dir else ""

    legal_score = 0.0
    legal_details: List[str] = []

    if os.path.isfile(contract_path):
        try:
            with open(contract_path, "r", encoding="utf-8") as f:
                content = f.read().lower()

            keywords = [
                ("obligation de moyens", 2.5),
                ("responsabilité", 2.5),
                ("acompte", 2.0),
                ("rgpd", 2.0),
                ("garantie", 2.0),
                ("support", 2.0),
                ("propriété", 2.0),
            ]

            matches = 0
            for kw, pts in keywords:
                if kw in content:
                    legal_score += pts
                    matches += 1

            legal_details.append(f"{matches}/{len(keywords)} clauses de protection vérifiées")
        except Exception as exc:
            legal_details.append(f"Erreur lecture contrat : {exc}")
    else:
        legal_details.append("Contrat type BON_DE_COMMANDE introuvable")

    items.append({
        "name": "Couverture Juridique & 9 CGV de Protection",
        "weight": 15.0,
        "score": round(legal_score, 1),
        "passed": legal_score >= 12.0,
        "details": " | ".join(legal_details),
    })

    # -------------------------------------------------------------------------
    # 5. Validation par Suite Unitaire Automatisée (Poids : 15 points)
    # -------------------------------------------------------------------------
    test_dir = next((os.path.join(workspace_dir, f) for f in found_folders if f.startswith("06_")), "")
    test_candidates = [
        os.path.join(test_dir, "test_office_suite.py"),
        os.path.join(test_dir, "test_btp_suite.py"),
    ]
    test_script = next((p for p in test_candidates if os.path.isfile(p)), "")

    test_score = 0.0
    test_details: List[str] = []

    if test_script:
        try:
            res = subprocess.run(
                [sys.executable, test_script],
                cwd=workspace_dir,
                capture_output=True,
                text=True,
                timeout=20,
            )
            if res.returncode == 0:
                test_score = 15.0
                test_details.append("Suite unitaire validée avec succès (100% OK)")
            else:
                test_details.append(f"Échec des tests (code {res.returncode}) : {res.stderr[:150]}")
        except Exception as exc:
            test_details.append(f"Exception lors des tests : {exc}")
    else:
        test_details.append("Script de tests unitaires introuvable")

    items.append({
        "name": "Validation Qualité Automatisée (Suite Unitaire)",
        "weight": 15.0,
        "score": round(test_score, 1),
        "passed": test_score >= 14.0,
        "details": " | ".join(test_details),
    })

    # -------------------------------------------------------------------------
    # Calcul du Score Global S
    # -------------------------------------------------------------------------
    global_score = sum(item["score"] for item in items)
    passed_count = sum(1 for item in items if item["passed"])
    status = "EXCELLENT" if global_score >= 90.0 else ("CONFORME" if global_score >= 65.0 else "NON CONFORME")

    return {
        "workspace_dir": workspace_dir,
        "global_score": round(global_score, 1),
        "total_checks": len(items),
        "passed_checks": passed_count,
        "items": items,
        "status": status,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit de qualité pour le Bureau Numérique.")
    parser.add_argument("--workspace-dir", "-w", required=True, help="Chemin du dossier projet")
    args = parser.parse_args()

    report = audit_universal_workspace(args.workspace_dir)

    print("=" * 70)
    print("📋 RAPPORT D'AUDIT QUALITÉ BUREAU NUMÉRIQUE — UNIVERSEL")
    print("=" * 70)
    print(f"Espace audité  : {report['workspace_dir']}")
    print(f"Score Global S : {report['global_score']} / 100")
    print(f"Statut Audit   : {report['status']} ({report['passed_checks']}/{report['total_checks']} contrôles validés)\n")

    for item in report["items"]:
        symbol = "[OK]" if item["passed"] else "[WARN]"
        print(f"{symbol} {item['name']} ({item['score']}/{item['weight']} pts)")
        print(f"     Détails : {item['details']}\n")

    print("-" * 70)
    if report["global_score"] >= 65.0:
        print("✅ VERDICT : L'espace de travail respecte les standards de production (≥ 65%).")
    else:
        print("❌ VERDICT : Score insuffisant (< 65%). Corriger les contrôles signalés ci-dessus.")
    print("=" * 70)


if __name__ == "__main__":
    main()
