"""
Générateur automatisé (Scaffolder CLI) pour initialiser un espace Bureau Numérique Universel.
Crée l'arborescence des 6 dossiers ordonnés, déploie les outils Python et les documents,
génère le classeur Excel adapté au secteur choisi, et lance l'audit qualité.
Strictement typé, zéro 'Any'.
"""

import argparse
import os
import shutil
import subprocess
import sys
from typing import Dict, Final, List, Optional, Tuple

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def create_directory_structure(base_dir: str, sector: str = "general") -> List[str]:
    """
    Crée l'arborescence des 6 sous-dossiers professionnels ordonnés.
    """
    folder_2 = "02_Candidature_Smart_Liege" if sector == "btp" else "02_Structure_Legale_et_Conformite"
    folder_names: List[str] = [
        "01_Strategie_et_Audits",
        folder_2,
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


def copy_template_files(skill_root: str, target_dir: str, sector: str = "general") -> None:
    """
    Copie les modèles d'outils et de documents vers le dossier cible.
    """
    templates_tools_dir = os.path.join(skill_root, "templates", "tools")
    templates_docs_dir = os.path.join(skill_root, "templates", "docs")
    references_dir = os.path.join(skill_root, "references")
    scripts_dir = os.path.join(skill_root, "scripts")

    folder_2 = "02_Candidature_Smart_Liege" if sector == "btp" else "02_Structure_Legale_et_Conformite"

    file_mapping: List[Tuple[str, str, str]] = [
        # Outils Python
        (scripts_dir, "generate_digital_office_workbook.py", "05_Outils_et_Modeles_Excel"),
        (templates_tools_dir, "generate_devis_sans_oubli.py", "05_Outils_et_Modeles_Excel"),
        (templates_tools_dir, "generate_rapport_patron.py", "05_Outils_et_Modeles_Excel"),
        (templates_tools_dir, "export_devis_to_csv.py", "05_Outils_et_Modeles_Excel"),
        (templates_tools_dir, "generate_prospection_sheet.py", "03_Vente_et_Prospection_Terrain"),
        (templates_tools_dir, "test_btp_suite.py", "06_Tests_et_Qualite"),
        (templates_tools_dir, "test_office_suite.py", "06_Tests_et_Qualite"),
        (scripts_dir, "append_new_deal.py", "05_Outils_et_Modeles_Excel"),
        (scripts_dir, "draft_followup_messages.py", "05_Outils_et_Modeles_Excel"),
        (scripts_dir, "generate_peppol_invoice.py", "05_Outils_et_Modeles_Excel"),
        (scripts_dir, "calculate_lost_revenue_roi.py", "05_Outils_et_Modeles_Excel"),
        (scripts_dir, "generate_patron_report.py", "05_Outils_et_Modeles_Excel"),
        (scripts_dir, "audit_digital_office.py", "06_Tests_et_Qualite"),
        (scripts_dir, "simulate_socio_fiscal.py", "01_Strategie_et_Audits"),
        # Documents contractuels
        (templates_docs_dir, "BON_DE_COMMANDE_PROPOSITION_COMMERCIALE.md", "03_Vente_et_Prospection_Terrain"),
        (templates_docs_dir, "DOSSIER_CANDIDATURE_SMART_LIEGE.md", folder_2),
        (templates_docs_dir, "PACK_BIENVENUE_ET_FORMATION_CLIENT.md", "04_Operations_et_Formation_Client"),
        (templates_docs_dir, "PACK_BIENVENUE_ET_FORMATION_UNIVERSEL.md", "04_Operations_et_Formation_Client"),
        (templates_docs_dir, "PLAN_ACTION_OPERATIONNEL_JOUR_PAR_JOUR.md", "04_Operations_et_Formation_Client"),
        (templates_docs_dir, "PROTOCOLE_INSTALLATION_TECHNIQUE.md", "04_Operations_et_Formation_Client"),
        # Références universelles & sectorielles
        (references_dir, "universal_business_adaptation_matrix.md", "01_Strategie_et_Audits"),
        (references_dir, "risk_management_and_red_team_protocols.md", "01_Strategie_et_Audits"),
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


def generate_readme(target_dir: str, company_name: str, sector: str, region: str) -> None:
    """
    Rédige le README d'orientation universel à la racine du projet.
    """
    readme_path = os.path.join(target_dir, "README.md")
    content = f"""# Bureau Numérique Universel — {company_name} ({sector.upper()})
> **Région :** {region} | **Modèle :** Squelette Administratif & Suivi d'Affaires Tous Secteurs

---

## 🧭 Architecture des 6 Dossiers

1. `01_Strategie_et_Audits/` : Matrice sectorielle, modélisation socio-fiscale 2026 (Smart/Indépendant) et Peppol.
2. `02_Structure_Legale_et_Conformite/` : Candidature Smart / dossier de conformité légale et précompte.
3. `03_Vente_et_Prospection_Terrain/` : Bon de commande 1 page, 9 CGV de protection, scripts et base prospects.
4. `04_Operations_et_Formation_Client/` : Procédure Quick Assist (`Win+Ctrl+Q`), PWA mobile et feuille de route 14 jours.
5. `05_Outils_et_Modeles_Excel/` : Classeur Excel protégé ({sector.upper()}), générateur de relances du vendredi et facturation Peppol.
6. `06_Tests_et_Qualite/` : Suite de tests unitaires et audit qualité automatisé (Score 100/100).

---

## ⚡ Commandes Rapides

```bash
# 1. Générer le classeur Excel avec le profil sectoriel
python 05_Outils_et_Modeles_Excel/generate_digital_office_workbook.py --sector {sector} --output 05_Outils_et_Modeles_Excel/SUIVI_AFFAIRES_MODELE_PRO.xlsx

# 2. Exécuter le rituel du vendredi (génère les vocaux WhatsApp et e-mails de relance)
python 05_Outils_et_Modeles_Excel/draft_followup_messages.py --excel-path 05_Outils_et_Modeles_Excel/SUIVI_AFFAIRES_MODELE_PRO.xlsx --sector {sector}

# 3. Insérer une nouvelle affaire sans ouvrir Excel
python 05_Outils_et_Modeles_Excel/append_new_deal.py --excel-path 05_Outils_et_Modeles_Excel/SUIVI_AFFAIRES_MODELE_PRO.xlsx --client "Martin Sprl" --montant 3200 --objet "Prestation" --sector {sector}

# 4. Générer une facture Peppol UBL 2.1 obligatoire
python 05_Outils_et_Modeles_Excel/generate_peppol_invoice.py --output-xml FACT-2026-001.xml --client-name "Client Sprl" --amount-htva 350.0

# 5. Auditer l'espace de travail
python 06_Tests_et_Qualite/audit_digital_office.py --workspace-dir .
```
"""
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"  -> README.md généré à la racine.")


def scaffold_office(
    output_dir: str,
    company_name: str = "Bureau Numérique",
    sector: str = "general",
    region: str = "Liège",
) -> None:
    """
    Orchestre le déploiement complet et l'audit de conformité.
    """
    skill_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_dir = os.path.abspath(output_dir)

    print("=" * 70)
    print(f"🏗️ DÉPLOIEMENT DU BUREAU NUMÉRIQUE UNIVERSEL ({sector.upper()})")
    print("=" * 70)
    print(f"Dossier cible  : {target_dir}")
    print(f"Entreprise     : {company_name}")
    print(f"Secteur        : {sector.upper()}")
    print(f"Région         : {region}\n")

    print("[1/4] Création de l'arborescence des 6 dossiers...")
    create_directory_structure(target_dir, sector=sector)

    print("\n[2/4] Déploiement des outils Python et des documents contractuels...")
    copy_template_files(skill_root, target_dir, sector=sector)
    generate_readme(target_dir, company_name, sector, region)

    print("\n[3/4] Génération des livrables opérationnels...")
    outils_dir = os.path.join(target_dir, "05_Outils_et_Modeles_Excel")

    excel_file = "SUIVI_AFFAIRES_MODELE_PRO.xlsx"
    gen_script = os.path.join(outils_dir, "generate_digital_office_workbook.py")
    if os.path.isfile(gen_script):
        subprocess.run(
            [sys.executable, gen_script, "--sector", sector, "--output", os.path.join(outils_dir, excel_file), "--company", company_name],
            cwd=target_dir,
            check=True,
        )

    # Si c'est btp, générer aussi DEVIS_SANS_OUBLI_MODELE_PRO.xlsx
    if sector == "btp":
        gen_btp = os.path.join(outils_dir, "generate_devis_sans_oubli.py")
        if os.path.isfile(gen_btp):
            subprocess.run([sys.executable, gen_btp], cwd=target_dir, check=True)

    # Export CSV automatique pour garantir l'absence de lock-in
    export_script = os.path.join(outils_dir, "export_devis_to_csv.py")
    if os.path.isfile(export_script):
        subprocess.run(
            [sys.executable, export_script, "--excel-path", os.path.join(outils_dir, excel_file)],
            cwd=target_dir,
            check=True,
        )

    print("\n[4/4] Audit de conformité de l'espace déployé...")
    audit_script = os.path.join(target_dir, "06_Tests_et_Qualite", "audit_digital_office.py")
    if os.path.isfile(audit_script):
        subprocess.run([sys.executable, audit_script, "--workspace-dir", target_dir], cwd=target_dir)

    print("\n" + "=" * 70)
    print(f"✅ DÉPLOIEMENT DU BUREAU NUMÉRIQUE RÉUSSI : {target_dir}")
    print("=" * 70)


def main() -> None:
    parser = argparse.ArgumentParser(description="Scaffolder CLI pour le Bureau Numérique Universel.")
    parser.add_argument("--output-dir", "-o", required=True, help="Répertoire cible du projet")
    parser.add_argument("--sector", "-s", default="general", choices=["btp", "services", "maintenance", "healthcare", "retail", "general"], help="Secteur d'activité")
    parser.add_argument("--company-name", "-c", default="Bureau Numérique", help="Nom de l'entreprise")
    parser.add_argument("--region", "-r", default="Liège", help="Région d'intervention")

    args = parser.parse_args()
    scaffold_office(
        output_dir=args.output_dir,
        company_name=args.company_name,
        sector=args.sector,
        region=args.region,
    )


if __name__ == "__main__":
    main()
