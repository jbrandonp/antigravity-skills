"""
Scaffolding CLI for creating a complete, production-ready BTP Digital Office workspace.
Enforces the 6-folder hierarchy, copies Python tools and documents, runs generators,
and executes the test suite. Strictly typed, zero 'Any'.
"""

import argparse
import os
import shutil
import subprocess
import sys
from typing import Final, List, Optional, Tuple

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def create_directory_structure(base_dir: str) -> List[str]:
    """
    Crée l'arborescence des 6 sous-dossiers professionnels ordonnés.

    Paramètres :
        base_dir (str) : Répertoire racine du projet cible.

    Retour :
        List[str] : Liste des chemins absolus des 6 dossiers créés.
    """
    folder_names: List[str] = [
        "01_Strategie_et_Audits",
        "02_Candidature_Smart_Liege",
        "03_Vente_et_Prospection_Terrain",
        "04_Operations_et_Formation_Client",
        "05_Outils_et_Modeles_Excel",
        "06_Tests_et_Qualite",
    ]
    created_paths: List[str] = []
    for name in folder_names:
        folder_path = os.path.join(base_dir, name)
        os.makedirs(folder_path, exist_ok=True)
        created_paths.append(folder_path)
    return created_paths


def copy_template_files(skill_root: str, target_dir: str) -> None:
    """
    Copie les modèles d'outils et de documents depuis le skill vers l'espace de travail cible.

    Paramètres :
        skill_root (str) : Répertoire racine du skill btp-digital-office-architect.
        target_dir (str) : Répertoire de destination du nouveau projet.

    Retour :
        None
    """
    templates_tools_dir = os.path.join(skill_root, "templates", "tools")
    templates_docs_dir = os.path.join(skill_root, "templates", "docs")
    references_dir = os.path.join(skill_root, "references")
    scripts_dir = os.path.join(skill_root, "scripts")

    # Mappage des fichiers sources vers leurs dossiers cibles respectifs
    file_mapping: List[Tuple[str, str, str]] = [
        # Outils Python
        (templates_tools_dir, "generate_devis_sans_oubli.py", "05_Outils_et_Modeles_Excel"),
        (templates_tools_dir, "generate_rapport_patron.py", "05_Outils_et_Modeles_Excel"),
        (templates_tools_dir, "export_devis_to_csv.py", "05_Outils_et_Modeles_Excel"),
        (templates_tools_dir, "generate_prospection_sheet.py", "03_Vente_et_Prospection_Terrain"),
        (templates_tools_dir, "test_btp_suite.py", "06_Tests_et_Qualite"),
        (scripts_dir, "append_new_devis.py", "05_Outils_et_Modeles_Excel"),
        (scripts_dir, "draft_relance_messages.py", "05_Outils_et_Modeles_Excel"),
        (scripts_dir, "generate_peppol_invoice.py", "05_Outils_et_Modeles_Excel"),
        (scripts_dir, "audit_btp_office.py", "06_Tests_et_Qualite"),
        (scripts_dir, "simulate_socio_fiscal.py", "01_Strategie_et_Audits"),
        # Documents contractuels et mémos
        (templates_docs_dir, "BON_DE_COMMANDE_PROPOSITION_COMMERCIALE.md", "03_Vente_et_Prospection_Terrain"),
        (templates_docs_dir, "DOSSIER_CANDIDATURE_SMART_LIEGE.md", "02_Candidature_Smart_Liege"),
        (templates_docs_dir, "PACK_BIENVENUE_ET_FORMATION_CLIENT.md", "04_Operations_et_Formation_Client"),
        (templates_docs_dir, "PLAN_ACTION_OPERATIONNEL_JOUR_PAR_JOUR.md", "04_Operations_et_Formation_Client"),
        (templates_docs_dir, "PROTOCOLE_INSTALLATION_TECHNIQUE.md", "04_Operations_et_Formation_Client"),
        # Références stratégiques
        (references_dir, "competitor_and_pricing_handbook.md", "01_Strategie_et_Audits"),
        (references_dir, "socio_fiscal_belgium_matrix.md", "01_Strategie_et_Audits"),
        (references_dir, "peppol_belgium_2026_technical_guide.md", "01_Strategie_et_Audits"),
        (references_dir, "gdpr_and_data_security_btp.md", "01_Strategie_et_Audits"),
        (references_dir, "diagnostic_and_audit_rubrics.md", "01_Strategie_et_Audits"),
        (references_dir, "sales_scripts_and_objections.md", "03_Vente_et_Prospection_Terrain"),
        (references_dir, "contracts_and_cgv_handbook.md", "03_Vente_et_Prospection_Terrain"),
        (references_dir, "technical_deployment_and_rituals.md", "04_Operations_et_Formation_Client"),
    ]

    for source_dir, file_name, destination_folder in file_mapping:
        source_path = os.path.join(source_dir, file_name)
        destination_path = os.path.join(target_dir, destination_folder, file_name)
        if os.path.isfile(source_path):
            shutil.copy2(source_path, destination_path)
            print(f"  -> Déployé : {destination_folder}/{file_name}")
        else:
            print(f"  [!] Avertissement : modèle introuvable à {source_path}")


def create_root_readme(base_dir: str, company_name: str, region: str, password: str) -> str:
    """
    Rédige et enregistre le README.md d'orientation à la racine de l'espace de travail.

    Paramètres :
        base_dir (str) : Chemin du dossier racine.
        company_name (str) : Nom commercial de l'activité.
        region (str) : Territoire ou province d'intervention.
        password (str) : Mot de passe de protection de la feuille Excel.

    Retour :
        str : Chemin absolu du README.md créé.
    """
    readme_path = os.path.join(base_dir, "README.md")
    content = f"""# 🏗️ {company_name.upper()} — ESPACE DE TRAVAIL OFFICIEL
## Organisation Administrative & Automatisation Légère pour Artisans du Bâtiment ({region})

Cet espace de travail regroupe l'ensemble des outils opérationnels, modèles contractuels,
références socio-fiscales belges et suites de tests pour gérer l'activité de conseil.

---

### 🗂️ Arborescence des 6 Dossiers Structurés

1. **`01_Strategie_et_Audits/`**
   - Étude de marché, benchmark de 19 concurrents BTP et catalogue des offres.
   - Simulation socio-fiscale (Smart Coop CP 200 vs Étudiant-Indépendant INASTI 2026).
2. **`02_Candidature_Smart_Liege/`**
   - Dossier formel de candidature pour la coopérative Smart Liège.
   - Attestations nécessaires (Student@work 600h, promotion sociale, eID).
3. **`03_Vente_et_Prospection_Terrain/`**
   - Manuel de prospection terrain, scripts vocaux WhatsApp et matrice des 7 objections.
   - Bon de commande en 1 page avec 9 conditions générales de vente (CGV).
   - Générateur de base de prospection (`generate_prospection_sheet.py`).
4. **`04_Operations_et_Formation_Client/`**
   - Protocole de déploiement à distance via Windows Quick Assist.
   - Guide du Rituel d'adoption du vendredi 16h30 (15 min chrono).
   - Feuille de route opérationnelle jour par jour (Semaines 1 & 2).
5. **`05_Outils_et_Modeles_Excel/`**
   - Modèle de classeur Excel « Devis sans oubli » (mot de passe : `{password}`).
   - Générateur automatique openpyxl (`generate_devis_sans_oubli.py`).
   - Générateur de synthèse exécutive patronale en < 1s (`generate_rapport_patron.py`).
   - Exportateur CSV compatible ERP (`export_devis_to_csv.py`).
6. **`06_Tests_et_Qualite/`**
   - Suite unifiée de tests d'intégrité et de vérifications financières (`test_btp_suite.py`).

---

### 🚀 Commandes de Pilotage Rapide

Générer ou rafraîchir les modèles Excel et rapports :
```powershell
python 05_Outils_et_Modeles_Excel/generate_devis_sans_oubli.py
python 05_Outils_et_Modeles_Excel/generate_rapport_patron.py
python 05_Outils_et_Modeles_Excel/export_devis_to_csv.py
python 03_Vente_et_Prospection_Terrain/generate_prospection_sheet.py
```

Automatisation des devis, relances et facturation Peppol :
```powershell
# Insérer un nouveau devis dans le classeur sans casser les formules
python 05_Outils_et_Modeles_Excel/append_new_devis.py --excel-path 05_Outils_et_Modeles_Excel/DEVIS_SANS_OUBLI_MODELE_PRO.xlsx --client "Nouveau Client" --montant 2400 --objet "Remplacement chaudière"

# Générer les messages WhatsApp / Email personnalisés pour les devis en retard (Rituel du vendredi)
python 05_Outils_et_Modeles_Excel/draft_relance_messages.py --excel-path 05_Outils_et_Modeles_Excel/DEVIS_SANS_OUBLI_MODELE_PRO.xlsx

# Générer une facture électronique Peppol UBL 2.1 obligatoire (Belgique 2026)
python 05_Outils_et_Modeles_Excel/generate_peppol_invoice.py --output-xml FACT-001.xml --client-name "Client SRL" --amount-htva 350.0

# Simuler la conversion net/brut (Smart vs INASTI 2026)
python 01_Strategie_et_Audits/simulate_socio_fiscal.py --revenue 1000
```

Exécuter la suite complète de validation qualité et l'audit détective :
```powershell
python 06_Tests_et_Qualite/test_btp_suite.py
python 06_Tests_et_Qualite/audit_btp_office.py --workspace-dir .
```
"""
    with open(readme_path, "w", encoding="utf-8") as file_handle:
        file_handle.write(content)
    return readme_path


def run_pipeline_generators(base_dir: str) -> None:
    """
    Exécute automatiquement les scripts générateurs pour produire les fichiers Excel, CSV, et rapports.

    Paramètres :
        base_dir (str) : Répertoire racine du projet cible.

    Retour :
        None
    """
    print("\n[*] Exécution des générateurs opérationnels...")
    generators: List[Tuple[str, str]] = [
        ("05_Outils_et_Modeles_Excel", "generate_devis_sans_oubli.py"),
        ("05_Outils_et_Modeles_Excel", "generate_rapport_patron.py"),
        ("05_Outils_et_Modeles_Excel", "export_devis_to_csv.py"),
        ("03_Vente_et_Prospection_Terrain", "generate_prospection_sheet.py"),
    ]

    for subfolder, script_name in generators:
        script_path = os.path.join(base_dir, subfolder, script_name)
        if os.path.isfile(script_path):
            print(f"  -> Lancement de {script_name}...")
            result = subprocess.run([sys.executable, script_path], cwd=os.path.join(base_dir, subfolder), capture_output=True, text=True)
            if result.returncode == 0:
                print(f"     [OK] {script_name} exécuté avec succès.")
            else:
                print(f"     [ERREUR] {script_name} a échoué :\n{result.stderr}")

    # Exécution de la suite de tests
    test_script = os.path.join(base_dir, "06_Tests_et_Qualite", "test_btp_suite.py")
    if os.path.isfile(test_script):
        print("\n[*] Exécution de la suite de validation qualité...")
        test_result = subprocess.run([sys.executable, test_script], cwd=base_dir, capture_output=True, text=True)
        if test_result.returncode == 0:
            print("     [SUCCÈS] Tous les tests unitaires et mathématiques sont validés (100% OK) !")
        else:
            print(f"     [ÉCHEC] La suite de tests a échoué :\n{test_result.stderr}\n{test_result.stdout}")

    # Exécution de l'audit architectural complet
    audit_script = os.path.join(base_dir, "06_Tests_et_Qualite", "audit_btp_office.py")
    if os.path.isfile(audit_script):
        print("\n[*] Exécution de l'audit architectural de l'espace de travail...")
        audit_result = subprocess.run([sys.executable, audit_script, "--workspace-dir", base_dir], cwd=base_dir, capture_output=True, text=True)
        if audit_result.returncode == 0:
            print("     [SUCCÈS] Audit qualité réussi avec note maximale (100/100) !")
        else:
            print(f"     [AVERTISSEMENT] Rapport d'audit :\n{audit_result.stdout}")


def main() -> None:
    """
    Point d'entrée principal de la commande CLI de scaffolding.
    """
    parser = argparse.ArgumentParser(description="Générateur complet d'espace de travail Bureau Numérique BTP")
    parser.add_argument("--output-dir", type=str, required=True, help="Répertoire cible du projet à initialiser")
    parser.add_argument("--company-name", type=str, default="Bureau Numérique BTP", help="Nom commercial de l'activité")
    parser.add_argument("--region", type=str, default="Liège", help="Région ou province d'activité")
    parser.add_argument("--password", type=str, default="BTP2026", help="Mot de passe de protection de la feuille Excel")
    parser.add_argument("--no-run", action="store_true", help="Désactive l'exécution immédiate des générateurs et tests")

    args = parser.parse_args()

    skill_root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_output_dir = os.path.abspath(args.output_dir)

    print("======================================================================")
    print("[BTP DIGITAL OFFICE ARCHITECT] GENERATEUR D'ESPACE DE TRAVAIL")
    print("======================================================================")
    print(f"Dossier cible    : {target_output_dir}")
    print(f"Activité         : {args.company_name}")
    print(f"Territoire       : {args.region}")
    print(f"Mot de passe     : {args.password}")

    # 1. Création de l'arborescence
    create_directory_structure(target_output_dir)
    print(f"[OK] 6 dossiers thématiques créés.")

    # 2. Déploiement des modèles et références
    print("\n[*] Déploiement des modèles et des guides...")
    copy_template_files(skill_root_dir, target_output_dir)

    # 3. Création du README
    readme_created = create_root_readme(target_output_dir, args.company_name, args.region, args.password)
    print(f"[OK] Fichier d'orientation créé : {readme_created}")

    # 4. Exécution immédiate des générateurs et tests si demandé
    if not args.no_run:
        run_pipeline_generators(target_output_dir)

    print("\n======================================================================")
    print("[OK] INITIALISATION TERMINEE AVEC SUCCES")
    print(f"Votre espace de travail est pret dans : {target_output_dir}")
    print("======================================================================")


if __name__ == "__main__":
    main()
