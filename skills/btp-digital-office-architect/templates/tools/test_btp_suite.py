"""
Automated test suite for the BTP Digital Office python tooling.
Validates Excel generation, cell protection, report metrics, and CSV export.
Strictly typed, zero 'Any'.
"""

import os
import sys
import unittest
import xml.etree.ElementTree as ET
from datetime import date, timedelta
from typing import Final, List, Tuple
import openpyxl

TEST_DIR: Final[str] = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR: Final[str] = os.path.dirname(TEST_DIR)
DIR_EXCEL: Final[str] = os.path.join(ROOT_DIR, "05_Outils_et_Modeles_Excel")
DIR_PROSPECT: Final[str] = os.path.join(ROOT_DIR, "03_Vente_et_Prospection_Terrain")
DIR_STRATEGIE: Final[str] = os.path.join(ROOT_DIR, "01_Strategie_et_Audits")

if DIR_EXCEL not in sys.path:
    sys.path.insert(0, DIR_EXCEL)
if DIR_PROSPECT not in sys.path:
    sys.path.insert(0, DIR_PROSPECT)
if DIR_STRATEGIE not in sys.path:
    sys.path.insert(0, DIR_STRATEGIE)

from append_new_devis import append_devis_to_workbook
from draft_relance_messages import scan_overdue_quotes, generate_messages_markdown
from export_devis_to_csv import export_devis_to_csv
from generate_devis_sans_oubli import create_devis_sans_oubli_workbook
from generate_peppol_invoice import create_peppol_ubl_xml, PeppolInvoiceData
from generate_prospection_sheet import create_prospection_workbook
from generate_rapport_patron import generate_rapport_patron, RapportMetrics
from simulate_socio_fiscal import simuler_smart_employe, simuler_smart_etudiant, simuler_etudiant_independant

TEST_EXCEL_DEVIS: Final[str] = os.path.join(DIR_EXCEL, "DEVIS_SANS_OUBLI_MODELE_PRO.xlsx")
TEST_EXCEL_PROSPECT: Final[str] = os.path.join(DIR_PROSPECT, "FICHIER_PROSPECTION_LIEGE_BTP.xlsx")
TEST_CSV_EXPORT: Final[str] = os.path.join(DIR_EXCEL, "EXPORTS_DEVIS_ERP_COMPATIBLE.csv")
TEST_TXT_RAPPORT: Final[str] = os.path.join(DIR_EXCEL, "RAPPORT_PATRON_EXEMPLE.txt")


class TestBTPDigitalOfficeSuite(unittest.TestCase):
    """
    Test cases to ensure complete reliability of generation tools.
    """

    def test_devis_workbook_generation_and_integrity(self) -> None:
        """
        Vérifie la création du classeur de devis, la présence des feuilles
        et l'intégrité de la protection des cellules.
        """
        create_devis_sans_oubli_workbook(TEST_EXCEL_DEVIS)
        self.assertTrue(os.path.exists(TEST_EXCEL_DEVIS), "Le classeur de devis doit exister sur le disque.")

        wb = openpyxl.load_workbook(TEST_EXCEL_DEVIS, data_only=False)
        expected_sheets: List[str] = [
            "Suivi des Devis",
            "Tableau de Bord",
            "Rituel Hebdomadaire"
        ]
        self.assertEqual(wb.sheetnames, expected_sheets, "Toutes les feuilles requises doivent être présentes.")

        ws_devis = wb["Suivi des Devis"]
        self.assertTrue(ws_devis.protection.sheet, "La feuille de devis doit être protégée par mot de passe.")
        self.assertGreaterEqual(ws_devis.max_row, 11, "Au moins 7 devis exemples doivent être encodés.")

        # Vérification du déverrouillage ciblé de la colonne Client (col 3) et verrouillage de la formule (col 8)
        cell_unlocked = ws_devis.cell(row=5, column=3)
        self.assertFalse(cell_unlocked.protection.locked, "La colonne Client doit être modifiable par l'artisan.")

        cell_locked = ws_devis.cell(row=5, column=9)
        self.assertTrue(cell_locked.protection.locked, "La colonne Statut Relance calculée doit être verrouillée.")

    def test_prospection_workbook_generation(self) -> None:
        """
        Vérifie la création de la base prospects et ses données initiales.
        """
        create_prospection_workbook(TEST_EXCEL_PROSPECT)
        self.assertTrue(os.path.exists(TEST_EXCEL_PROSPECT), "Le classeur prospects doit exister.")

        wb = openpyxl.load_workbook(TEST_EXCEL_PROSPECT, data_only=True)
        self.assertIn("Pipeline Prospection Liège", wb.sheetnames)
        ws = wb["Pipeline Prospection Liège"]
        self.assertEqual(ws.max_row, 9, "Ligne 4 en-têtes + 5 prospects qualifiés = 9 lignes au total.")

    def test_rapport_patron_calculation(self) -> None:
        """
        Vérifie l'exactitude des métriques financières et de relance calculées.
        """
        metrics: RapportMetrics = generate_rapport_patron(TEST_EXCEL_DEVIS, TEST_TXT_RAPPORT)
        
        self.assertTrue(os.path.exists(TEST_TXT_RAPPORT), "Le rapport texte patron doit être généré.")
        self.assertEqual(metrics["total_devis"], 7, "Le total des devis analysés doit être exactement de 7.")
        self.assertGreater(metrics["ca_en_attente"], 0.0, "Le CA en attente doit être supérieur à zéro.")
        self.assertGreaterEqual(metrics["nb_urgences"], 1, "Il doit y avoir au moins un devis urgent à relancer.")

        with open(TEST_TXT_RAPPORT, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("RAPPORT MENSUEL DU DIRIGEANT", content)
            self.assertIn("ALERTES PRIORITAIRES", content)

    def test_export_devis_to_csv_integrity(self) -> None:
        """
        Vérifie l'export CSV UTF-8 avec séparateur point-virgule et intégrité des lignes.
        """
        nb_rows: int = export_devis_to_csv(TEST_EXCEL_DEVIS, TEST_CSV_EXPORT)
        self.assertTrue(os.path.exists(TEST_CSV_EXPORT), "Le fichier CSV doit être généré.")
        self.assertEqual(nb_rows, 7, "Exactement 7 lignes de données réelles doivent être exportées.")

        with open(TEST_CSV_EXPORT, "r", encoding="utf-8-sig") as f:
            lines = f.readlines()
            self.assertEqual(len(lines), 8, "En-tête + 7 devis = exactement 8 lignes dans le CSV.")
            self.assertIn(";", lines[0], "Le séparateur CSV doit être le point-virgule.")

    def test_mathematical_and_financial_integrity(self) -> None:
        """
        Vérifie l'exactitude mathématique absolue des modèles financiers (Scénarios A, B,
        trésorerie M1-M12, seuils de rentabilité, et barèmes sociaux 2026).
        """
        import math

        # 1. Modèle A : Sommes et CA
        inst_counts = [0, 0, 1, 1, 1, 2, 2, 2, 3, 2, 3, 4]
        inst_revenues = [0, 0, 250, 300, 300, 600, 700, 700, 1050, 750, 1125, 1500]
        abo_revenues = [0, 0, 0, 0, 60, 120, 180, 180, 180, 240, 300, 360]
        
        self.assertEqual(sum(inst_counts), 21, "Scénario A : 21 installations au total.")
        self.assertEqual(sum(inst_revenues), 7275, "Scénario A : 7 275 € de CA installations.")
        self.assertEqual(sum(abo_revenues), 1620, "Scénario A : 1 620 € de CA abonnements.")
        self.assertEqual(sum(inst_revenues) + sum(abo_revenues), 8895, "Scénario A : 8 895 € de CA global.")

        # 2. Modèle A : Trésorerie cumulée
        cash = 150.0
        cash_history: List[float] = []
        for m in range(12):
            ca = float(inst_revenues[m] + abo_revenues[m])
            dep = (150.0 if m == 0 else 0.0) + 35.0 + (ca * 0.05)
            cash += (ca - dep)
            cash_history.append(cash)

        self.assertEqual(cash_history[0], -35.0, "M1 : Trésorerie à -35,00 €.")
        self.assertEqual(cash_history[1], -70.0, "M2 : Trésorerie à -70,00 €.")
        self.assertTrue(math.isclose(cash_history[11], 8030.25, abs_tol=0.01), "M12 : Trésorerie finale de +8 030,25 €.")

        # 3. Seuils de rentabilité
        ca_seuil = 35.0 / 0.95
        ca_cible_1000 = 1035.0 / 0.95
        self.assertTrue(math.isclose(ca_seuil, 36.8421, abs_tol=0.01), "Seuil de rentabilité : 36,84 € / mois.")
        self.assertTrue(math.isclose(ca_cible_1000, 1089.4736, abs_tol=0.01), "CA cible 1 000 € net : 1 089,47 €.")

        # 4. Modèle B (Lean 50 €)
        inst_counts_B = [0, 0, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2]
        inst_rev_B = [0, 0, 200, 250, 300, 300, 350, 350, 350, 700, 350, 700]
        abo_rev_B = [0, 0, 0, 0, 60, 120, 180, 240, 240, 240, 300, 360]
        total_B = sum(inst_rev_B) + sum(abo_rev_B)

        self.assertEqual(sum(inst_counts_B), 12, "Scénario B : 12 installations.")
        self.assertEqual(total_B, 5590, "Scénario B : 5 590 € de CA.")
        self.assertTrue(math.isclose(total_B * 0.065, 363.35, abs_tol=0.01), "Smart 6,5% : 363,35 €.")
        self.assertTrue(math.isclose(total_B - 363.35 - 120.0, 5106.65, abs_tol=0.01), "Solde brut B : 5 106,65 €.")

    def test_append_devis_flow(self) -> None:
        """
        Vérifie l'insertion sécurisée d'un devis avec préservation des formules et verrous.
        """
        # Création d'un classeur temporaire pour tester l'insertion
        temp_excel = os.path.join(DIR_EXCEL, "TEMP_TEST_DEVIS.xlsx")
        create_devis_sans_oubli_workbook(temp_excel)

        row_inserted, num_genere = append_devis_to_workbook(
            excel_path=temp_excel,
            nom_client="Rénovation Test Sprl",
            montant_htva=1850.0,
            objet_travaux="Remplacement tableau divisionnaire",
            telephone="0499 88 77 66",
            statut_initial="En attente",
            commentaires="Test unitaire insertion",
        )

        self.assertEqual(row_inserted, 12, "La première ligne vide pour le 8ème devis doit être la ligne 12.")
        self.assertEqual(num_genere, f"DEV-{date.today().year}-088", "Le numéro doit s'incrémenter à DEV-2026-088.")

        # Vérification du fichier modifié
        wb = openpyxl.load_workbook(temp_excel, data_only=False)
        ws = wb["Suivi des Devis"]
        self.assertEqual(ws.cell(row=12, column=3).value, "Rénovation Test Sprl")
        self.assertFalse(ws.cell(row=12, column=3).protection.locked, "La cellule client doit être déverrouillée.")
        self.assertTrue(ws.cell(row=12, column=9).protection.locked, "La cellule statut relance doit être verrouillée.")

        # Nettoyage
        if os.path.exists(temp_excel):
            os.remove(temp_excel)

    def test_draft_relance_messages_flow(self) -> None:
        """
        Vérifie la détection des devis en retard et la génération des messages WhatsApp et Email.
        """
        quotes = scan_overdue_quotes(TEST_EXCEL_DEVIS)
        self.assertGreaterEqual(len(quotes), 1, "Il doit y avoir au moins un devis urgent détecté.")

        md = generate_messages_markdown(quotes, company_name="Bureau Numérique BTP", artisan_name="Brandon")
        self.assertIn("MESSAGES DE RELANCE PERSONNALISÉS", md)
        self.assertIn("Option A : Message Texte WhatsApp", md)
        self.assertIn("Option B : Script Vocal WhatsApp", md)
        self.assertIn("Option C : Email de Relance Doux", md)

    def test_peppol_xml_generation(self) -> None:
        """
        Vérifie la génération d'une facture électronique Peppol BIS 3.0 UBL 2.1 conforme et sans erreur XML.
        """
        sample_peppol: PeppolInvoiceData = {
            "invoice_number": "FACT-2026-TEST",
            "issue_date": date.today(),
            "due_date": date.today() + timedelta(days=30),
            "supplier_name": "Smart Coop (SC ES) / Bureau Numérique BTP",
            "supplier_cbe": "0459180573",
            "supplier_vat": "BE0459180573",
            "supplier_street": "Rue Émile Féron 70",
            "supplier_city": "Bruxelles",
            "supplier_postal_code": "1060",
            "customer_name": "Plomberie Liégeoise Sprl",
            "customer_cbe": "0888999111",
            "customer_vat": "BE0888999111",
            "customer_street": "Quai de Rome 45",
            "customer_city": "Liège",
            "customer_postal_code": "4000",
            "item_description": "Installation Pack Devis sans oubli",
            "amount_htva": 350.0,
            "vat_rate": 0.21,
        }

        xml_string = create_peppol_ubl_xml(sample_peppol)
        root = ET.fromstring(xml_string)
        self.assertIn("Invoice", root.tag, "La racine XML doit être un élément Invoice UBL.")
        self.assertIn("FACT-2026-TEST", xml_string)
        self.assertIn("0459180573", xml_string)

    def test_socio_fiscal_simulation_engine(self) -> None:
        """
        Vérifie l'exactitude des calculs socio-fiscaux belges 2026 (Smart et INASTI).
        """
        res_emp = simuler_smart_employe(1000.0)
        self.assertTrue(45.0 <= res_emp["taux_rendement_net"] <= 51.0, "Smart employé net entre 45% et 51%.")

        res_etu = simuler_smart_etudiant(1000.0)
        self.assertTrue(70.0 <= res_etu["taux_rendement_net"] <= 78.0, "Smart étudiant net entre 70% et 78%.")

        res_ind = simuler_etudiant_independant(5000.0, is_annual=True)
        self.assertEqual(res_ind["cotisations_sociales"], 0.0, "Cotisations INASTI à 0 € sous 8 687,04 €.")


if __name__ == "__main__":
    unittest.main()
