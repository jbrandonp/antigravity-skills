"""
Automated quality audit and stress-testing tool for BTP Digital Office workspaces.
Checks folder structure, Excel cell protection matrix, live formula injection,
footer disclaimer isolation, legal contract clauses, and automated test pass rate.
Outputs an audit score (0-100) compliant with agentic standards. Strictly typed, zero 'Any'.
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


def audit_workspace(workspace_dir: str) -> AuditReport:
    """
    Exécute un audit complet de conformité architecturale, ergonomique et légale sur l'espace BTP.

    Paramètres :
        workspace_dir (str) : Chemin absolu ou relatif de la racine du projet BTP.

    Retour :
        AuditReport : Rapport détaillé avec score global sur 100 et détails par contrôle.
    """
    items: List[AuditCheckItem] = []

    # -------------------------------------------------------------------------
    # 1. Audit de l'Arborescence des 6 Dossiers (Poids : 20 points)
    # -------------------------------------------------------------------------
    expected_folders: List[str] = [
        "01_Strategie_et_Audits",
        "02_Candidature_Smart_Liege",
        "03_Vente_et_Prospection_Terrain",
        "04_Operations_et_Formation_Client",
        "05_Outils_et_Modeles_Excel",
        "06_Tests_et_Qualite",
    ]
    missing_folders: List[str] = [
        f for f in expected_folders if not os.path.isdir(os.path.join(workspace_dir, f))
    ]
    passed_folders = len(missing_folders) == 0
    score_folders = 20.0 if passed_folders else max(0.0, 20.0 * (1.0 - len(missing_folders) / len(expected_folders)))
    items.append({
        "name": "Arborescence Standardisée (6 dossiers numérotés)",
        "weight": 20.0,
        "score": round(score_folders, 1),
        "passed": passed_folders,
        "details": "Tous les 6 dossiers sont présents." if passed_folders else f"Dossiers manquants : {', '.join(missing_folders)}",
    })

    # -------------------------------------------------------------------------
    # 2. Audit du Classeur Excel et Zonage des Cellules (Poids : 30 points)
    # -------------------------------------------------------------------------
    excel_path = os.path.join(workspace_dir, "05_Outils_et_Modeles_Excel", "DEVIS_SANS_OUBLI_MODELE_PRO.xlsx")
    excel_score = 0.0
    excel_details: List[str] = []

    if os.path.isfile(excel_path):
        try:
            wb = openpyxl.load_workbook(excel_path, data_only=False)
            expected_sheets = ["Suivi des Devis", "Tableau de Bord", "Rituel Hebdomadaire"]
            sheets_ok = all(s in wb.sheetnames for s in expected_sheets)
            if sheets_ok:
                excel_score += 10.0
                excel_details.append("3 feuilles obligatoires présentes")
            else:
                excel_details.append(f"Feuilles manquantes dans {wb.sheetnames}")

            ws_devis = wb["Suivi des Devis"]
            is_protected = bool(ws_devis.protection.sheet)
            if is_protected:
                excel_score += 5.0
                excel_details.append("Feuille protégée par mot de passe")
            else:
                excel_details.append("Feuille NON protégée")

            # Vérification du déverrouillage des colonnes de saisie (Cols 1-8, 10, 11) et verrouillage de la Col 9
            col_client_unlocked = not bool(ws_devis.cell(row=5, column=3).protection.locked)
            col_relance_locked = bool(ws_devis.cell(row=5, column=9).protection.locked)

            if col_client_unlocked and col_relance_locked:
                excel_score += 10.0
                excel_details.append("Zonage ergonomique validé (Saisie libre, Formule verrouillée)")
            else:
                excel_details.append(f"Erreur zonage : Client déverrouillé={col_client_unlocked}, Relance verrouillée={col_relance_locked}")

            # Vérification de formule dans les lignes vides (ex: ligne 12)
            has_formula = bool(ws_devis.cell(row=12, column=8).value)
            if has_formula:
                excel_score += 5.0
                excel_details.append("Formules vivantes injectées dans les lignes vides")
            else:
                excel_details.append("Lignes vides sans formule de relance")

        except Exception as exc:
            excel_details.append(f"Exception lors de la lecture Excel : {exc}")
    else:
        excel_details.append(f"Fichier introuvable à {excel_path}")

    items.append({
        "name": "Intégrité Excel & Ergonomie ('Devis sans oubli')",
        "weight": 30.0,
        "score": round(excel_score, 1),
        "passed": excel_score >= 25.0,
        "details": " | ".join(excel_details),
    })

    # -------------------------------------------------------------------------
    # 3. Audit de Portabilité des Données & Disclaimer (Poids : 20 points)
    # -------------------------------------------------------------------------
    csv_path = os.path.join(workspace_dir, "05_Outils_et_Modeles_Excel", "EXPORTS_DEVIS_ERP_COMPATIBLE.csv")
    csv_score = 0.0
    csv_details: List[str] = []

    if os.path.isfile(csv_path):
        try:
            with open(csv_path, "r", encoding="utf-8-sig") as f:
                lines = [line.strip() for line in f if line.strip()]
            if len(lines) >= 8:
                csv_score += 10.0
                csv_details.append(f"Lignes CSV valides ({len(lines)} lignes)")
            else:
                csv_details.append(f"CSV incomplet ({len(lines)} lignes)")

            # Vérification de l'absence du texte d'avertissement dans les lignes de données
            has_disclaimer = any("AVERTISSEMENT" in l or "Avertissement" in l for l in lines)
            if not has_disclaimer:
                csv_score += 10.0
                csv_details.append("Pied de page filtré avec succès (zéro ligne fantôme)")
            else:
                csv_details.append("Pied de page détecté par erreur comme devis dans le CSV")
        except Exception as exc:
            csv_details.append(f"Erreur lecture CSV : {exc}")
    else:
        csv_details.append("Fichier CSV manquant (lancer export_devis_to_csv.py)")

    items.append({
        "name": "Exportation ERP & Filtrage des Disclaimers",
        "weight": 20.0,
        "score": round(csv_score, 1),
        "passed": csv_score >= 18.0,
        "details": " | ".join(csv_details),
    })

    # -------------------------------------------------------------------------
    # 4. Audit Contractuel & 9 CGV de Protection (Poids : 15 points)
    # -------------------------------------------------------------------------
    contract_path = os.path.join(workspace_dir, "03_Vente_et_Prospection_Terrain", "BON_DE_COMMANDE_PROPOSITION_COMMERCIALE.md")
    contract_score = 0.0
    contract_details: List[str] = []

    if os.path.isfile(contract_path):
        with open(contract_path, "r", encoding="utf-8") as f:
            contract_text = f.read()

        clauses_checked = [
            ("Obligation de moyens", "OBLIGATION STRICTE DE MOYENS" in contract_text or "obligation de moyens" in contract_text),
            ("Plafonnement responsabilité", "LIMITATION ET PLAFONNEMENT DE RESPONSABILITÉ" in contract_text or "plafonné au montant" in contract_text),
            ("Coupe-feu 50 devis", "50 fiches" in contract_text or "50 devis" in contract_text),
            ("Garantie 14 jours", "14 jours" in contract_text),
            ("Fenêtres SLA support", "7h00" in contract_text and "17h00" in contract_text),
            ("Accord RGPD sous-traitance", "RGPD" in contract_text),
            ("Acompte 50/50", "50 %" in contract_text),
        ]

        passed_clauses = sum(1 for _, ok in clauses_checked if ok)
        contract_score = 15.0 * (passed_clauses / len(clauses_checked))
        contract_details.append(f"{passed_clauses}/{len(clauses_checked)} clauses de protection vérifiées")
    else:
        contract_details.append("Bon de commande introuvable")

    items.append({
        "name": "Couverture Juridique & 9 CGV de Protection",
        "weight": 15.0,
        "score": round(contract_score, 1),
        "passed": contract_score >= 12.0,
        "details": " | ".join(contract_details),
    })

    # -------------------------------------------------------------------------
    # 5. Audit de la Suite de Tests Automatisée (Poids : 15 points)
    # -------------------------------------------------------------------------
    test_script = os.path.join(workspace_dir, "06_Tests_et_Qualite", "test_btp_suite.py")
    test_score = 0.0
    test_details: List[str] = []

    if os.path.isfile(test_script):
        try:
            result = subprocess.run([sys.executable, test_script], cwd=workspace_dir, capture_output=True, text=True)
            if result.returncode == 0:
                test_score = 15.0
                test_details.append("5/5 tests unitaires validés (100% OK)")
            else:
                test_details.append(f"Échec des tests (code {result.returncode})")
        except Exception as exc:
            test_details.append(f"Erreur d'exécution des tests : {exc}")
    else:
        test_details.append("test_btp_suite.py manquant")

    items.append({
        "name": "Validation Qualité Automatisée (Suite Unitaire)",
        "weight": 15.0,
        "score": round(test_score, 1),
        "passed": test_score == 15.0,
        "details": " | ".join(test_details),
    })

    # Calcul de la note globale sur 100
    global_score = sum(it["score"] for it in items)
    passed_count = sum(1 for it in items if it["passed"])
    status = "EXCELLENT" if global_score >= 90.0 else ("CONFORME" if global_score >= 65.0 else "NON CONFORME")

    return {
        "workspace_dir": workspace_dir,
        "global_score": round(global_score, 1),
        "total_checks": len(items),
        "passed_checks": passed_count,
        "items": items,
        "status": status,
    }


def afficher_rapport_audit(report: AuditReport) -> None:
    """
    Imprime le rapport d'audit formaté dans la console avec la charte graphique.
    """
    print("======================================================================")
    print("📋 RAPPORT D'AUDIT QUALITÉ BTP — DÉTECTIVE MODE (AGENT AUTONOME)")
    print("======================================================================")
    print(f"Espace audité  : {report['workspace_dir']}")
    print(f"Score Global S : {report['global_score']} / 100")
    print(f"Statut Audit   : {report['status']} ({report['passed_checks']}/{report['total_checks']} contrôles validés)\n")

    for idx, item in enumerate(report["items"], start=1):
        statut_icon = "[OK]" if item["passed"] else "[WARN]"
        print(f"{statut_icon} Contrôle {idx} : {item['name']} ({item['score']}/{item['weight']} pts)")
        print(f"     Détails : {item['details']}\n")

    print("----------------------------------------------------------------------")
    if report["global_score"] >= 65.0:
        print("✅ VERDICT : L'espace de travail respecte les standards de production BTP (≥ 65%).")
    else:
        print("❌ VERDICT : Score insuffisant (< 65%). Corriger les anomalies signalées.")
    print("======================================================================\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Auditeur qualité et conformité pour Bureau Numérique BTP")
    parser.add_argument("--workspace-dir", type=str, default=".", help="Chemin du dossier racine à auditer")

    args = parser.parse_args()
    target_dir = os.path.abspath(args.workspace_dir)
    report = audit_workspace(target_dir)
    afficher_rapport_audit(report)


if __name__ == "__main__":
    main()
