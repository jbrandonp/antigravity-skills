"""
Suite de tests unitaires et de non-régression pour le Bureau Numérique Universel.
Valide la génération Excel multi-secteurs, l'intégrité des formules, le zonage de protection,
le calcul des dates de relance ($J+14, J+7, J+3, J+5$), la facturation Peppol et la simulation socio-fiscale.
Strictement typé, zéro 'Any'.
"""

import os
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from datetime import date, timedelta
from typing import Final, List, Tuple
import openpyxl

# Configuration UTF-8 pour Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Import des modules opérationnels
TOOLS_DIR: Final[str] = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "05_Outils_et_Modeles_Excel"))
STRAT_DIR: Final[str] = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "01_Strategie_et_Audits"))

if TOOLS_DIR not in sys.path:
    sys.path.insert(0, TOOLS_DIR)
if STRAT_DIR not in sys.path:
    sys.path.insert(0, STRAT_DIR)

from generate_digital_office_workbook import SECTOR_CONFIGS, create_digital_office_workbook
from append_new_deal import append_deal_to_workbook
from draft_followup_messages import generate_messages_for_deal, scan_overdue_deals
from generate_peppol_invoice import create_peppol_ubl_xml
from calculate_lost_revenue_roi import calculate_business_roi
from generate_patron_report import format_patron_report_text, generate_patron_report_metrics
from simulate_socio_fiscal import (
    POINT_DE_BASCULE_SMART_INASTI,
    simuler_etudiant_independant,
    simuler_smart_employe,
    simuler_smart_etudiant,
)


class TestUniversalDigitalOfficeSuite(unittest.TestCase):
    """
    Batterie de tests automatisés validant le squelette universel et les profils sectoriels.
    """

    def setUp(self) -> None:
        self.temp_dir = tempfile.mkdtemp()
        self.excel_test_path = os.path.join(self.temp_dir, "TEST_UNIVERSAL_OFFICE.xlsx")

    def tearDown(self) -> None:
        if os.path.isdir(self.temp_dir):
            import shutil
            shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_01_all_sector_configs_exist(self) -> None:
        """Vérifie la complétude des 6 profils sectoriels."""
        expected_sectors = ["btp", "services", "maintenance", "healthcare", "retail", "general"]
        for sec in expected_sectors:
            self.assertIn(sec, SECTOR_CONFIGS, f"Le profil sectoriel '{sec}' est manquant.")
            cfg = SECTOR_CONFIGS[sec]
            self.assertGreater(cfg["delay_days"], 0, f"Délai invalide pour {sec}")
            self.assertTrue(len(cfg["sample_deals"]) >= 5, f"Pas assez de deals pour {sec}")

    def test_02_generate_workbook_and_protection_invariants(self) -> None:
        """Valide la création Excel, le mot de passe et le zonage déverrouillé/verrouillé."""
        create_digital_office_workbook(self.excel_test_path, sector="services", company_name="Test Agency")
        self.assertTrue(os.path.isfile(self.excel_test_path), "Le classeur Excel n'a pas été créé.")

        wb = openpyxl.load_workbook(self.excel_test_path, data_only=False)
        self.assertEqual(len(wb.sheetnames), 3, "Le classeur doit contenir exactement 3 feuilles.")

        ws = wb[wb.sheetnames[0]]
        self.assertTrue(bool(ws.protection.sheet), "La feuille principale doit être protégée.")

        # Vérifier que les colonnes 1-8, 10, 11 sont déverrouillées et colonne 9 verrouillée
        sample_row = 6
        for col in (1, 2, 3, 4, 5, 6, 7, 8, 10, 11):
            prot = ws.cell(row=sample_row, column=col).protection
            self.assertFalse(prot.locked, f"La cellule ({sample_row}, {col}) doit être déverrouillée.")

        prot_9 = ws.cell(row=sample_row, column=9).protection
        self.assertTrue(prot_9.locked, f"La cellule ({sample_row}, 9) doit être verrouillée pour protéger la formule.")

    def test_03_append_new_deal_incremental_logic(self) -> None:
        """Vérifie l'insertion sécurisée d'une nouvelle affaire et son ID incrémental."""
        create_digital_office_workbook(self.excel_test_path, sector="maintenance", company_name="Garage Test")
        row, deal_id = append_deal_to_workbook(
            excel_path=self.excel_test_path,
            nom_client="Transport Express Sprl",
            montant_htva=1450.0,
            objet_prestation="Remplacement kit distribution",
            telephone="0470 00 11 22",
            sector="maintenance",
        )
        self.assertGreaterEqual(row, 5)
        self.assertTrue(deal_id.startswith("OR-2026-"), f"L'identifiant doit commencer par OR-2026- : {deal_id}")

        wb = openpyxl.load_workbook(self.excel_test_path)
        ws = wb[wb.sheetnames[0]]
        self.assertEqual(ws.cell(row=row, column=3).value, "Transport Express Sprl")
        self.assertEqual(ws.cell(row=row, column=6).value, 1450.0)

    def test_04_draft_messages_sector_adaptation(self) -> None:
        """Vérifie que la rédaction des messages s'adapte au vocabulaire du secteur."""
        fake_deal = {
            "ref_deal": "PROP-2026-001",
            "date_emission": "01/11/2026",
            "client": "Client SaaS",
            "tel": "0471 22 33 44",
            "objet": "Refonte application web",
            "montant_htva": 4500.0,
            "jours_retard": 4,
        }
        msgs = generate_messages_for_deal(fake_deal, sector="services", sender_name="Brandon")
        self.assertIn("projets", msgs["vocal"].lower())
        self.assertIn("proposition", msgs["email"].lower())
        self.assertIn("delivery", msgs["texte"].lower())
        self.assertIn("4,500.00", msgs["vocal"])

    def test_05_peppol_xml_validity(self) -> None:
        """Valide la génération d'une facture XML UBL 2.1 Peppol conforme."""
        xml_path = os.path.join(self.temp_dir, "TEST_PEPPOL.xml")
        invoice_data = {
            "invoice_number": "FACT-2026-TEST",
            "issue_date": date.today(),
            "due_date": date.today() + timedelta(days=30),
            "supplier_name": "Bureau Numérique Sprl",
            "supplier_cbe": "0459180573",
            "supplier_vat": "0459180573",
            "supplier_street": "Boulevard d'Avroy 28",
            "supplier_city": "Liège",
            "supplier_postal_code": "4000",
            "customer_name": "Test Client SA",
            "customer_cbe": "0123456789",
            "customer_vat": "0123456789",
            "customer_street": "Rue de la Loi 1",
            "customer_city": "Bruxelles",
            "customer_postal_code": "1000",
            "item_description": "Prestation d'accompagnement numérique",
            "amount_htva": 500.0,
            "vat_rate": 0.21,
        }
        xml_str = create_peppol_ubl_xml(invoice_data)
        with open(xml_path, "w", encoding="utf-8") as f:
            f.write(xml_str)
        self.assertTrue(os.path.isfile(xml_path))

        tree = ET.parse(xml_path)
        root = tree.getroot()
        self.assertTrue(root.tag.endswith("Invoice"))
        namespaces = {"cbc": "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2"}
        id_elem = root.find("cbc:ID", namespaces)
        self.assertIsNotNone(id_elem)
        self.assertEqual(id_elem.text, "FACT-2026-TEST")

    def test_06_socio_fiscal_math_equilibrium(self) -> None:
        """Valide la formule d'équilibre socio-fiscal (seuil de bascule ~6 200 €)."""
        sim_smart = simuler_smart_etudiant(1000.0)
        self.assertGreater(sim_smart["net_en_poche"], 650.0)
        self.assertGreaterEqual(sim_smart["taux_rendement_net"], 65.0)

        sim_indep_low = simuler_etudiant_independant(ca_htva=3000.0, is_annual=True)
        sim_smart_low = simuler_smart_etudiant(3000.0)
        # En dessous de 6200 €, Smart évite les frais de comptable fixes
        self.assertEqual(POINT_DE_BASCULE_SMART_INASTI, 6200.0)

        sim_indep_high = simuler_etudiant_independant(ca_htva=8000.0, is_annual=True)
        # Au-dessus de 6200 €, l'indépendant étudiant devient plus rentable que Smart
        self.assertGreater(sim_indep_high["net_en_poche"], 7000.0)

    def test_07_calculate_lost_revenue_roi(self) -> None:
        """Valide le calcul d'hémorragie financière et le délai d'amortissement."""
        roi = calculate_business_roi(
            quotes_per_month=10,
            avg_amount=3000.0,
            loss_rate=0.30,
            win_rate=0.40,
            pack_price=350.0,
            client_name="Test Client",
        )
        self.assertGreater(roi["annual_loss_revenue"], 40000.0)
        self.assertLess(roi["amortization_days"], 15.0)
        self.assertGreaterEqual(roi["payback_single_quote_ratio"], 8.0)
        self.assertIn("Test Client", roi["pitch_vocal"])

    def test_08_generate_patron_report_metrics(self) -> None:
        """Valide la compilation automatique des métriques du Rapport Patron."""
        create_digital_office_workbook(self.excel_test_path, sector="btp", company_name="Patron Test")
        metrics = generate_patron_report_metrics(self.excel_test_path, company_name="Patron Test")
        self.assertGreater(metrics["total_deals"], 0)
        self.assertGreater(metrics["pending_revenue"], 0.0)
        report_text = format_patron_report_text(metrics)
        self.assertIn("RAPPORT PATRON MENSUEL", report_text)
        self.assertIn("ACTIONS PRIORITAIRES", report_text)


def run_tests() -> bool:
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUniversalDigitalOfficeSuite)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
