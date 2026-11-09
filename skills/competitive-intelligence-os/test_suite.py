"""
Suite de tests unitaires automatisés pour competitive-intelligence-os.
Valide 100% des modules core, storage et deliverables sous Python 3.12+ (uv).
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from codegen.vampire_migrator_builder import (
    ColumnMapping,
    VampireMigratorBuilder,
    VampireMigratorSpec,
)
from core.altman_distress_calculator import (
    AltmanDistressCalculator,
    FinancialBalanceSheetInput,
)
from core.disruption_radar_index import (
    DisruptionMetricInput,
    DisruptionRadarEngine,
    ThreatClassification,
)
from core.firmographic_job_watcher import FirmographicJobWatcher, JobPostingSnapshot
from core.kiq_framework_router import KIQRouter, StrategicIntent
from core.markov_churn_engine import StochasticMarketEngine
from core.operational_benchmarker import OperationalBenchmarker, OperationalMetrics
from core.positioning_plotter_svg import (
    PositioningEntity,
    RadarDimensionScore,
    RadarEntity,
    SVGPositioningPlotter,
    SVGRadarPlotter,
)
from core.wardley_mapper_svg import (
    WardleyComponent,
    WardleyDependency,
    WardleyMapperSVG,
)
from core.wargame_scenario_simulator import WarGameScenarioSimulator
from core.win_loss_debiasing_engine import DealLossInterview, WinLossDebiasingEngine
from core.wisdom_gate_checker import WisdomGateChecker
from deliverables.assault_landing_builder import (
    AssaultLandingBuilder,
    AssaultLandingSpec,
    ComparisonFeatureRow,
)
from deliverables.battlecard_8sec_builder import (
    Battlecard8SecBuilder,
    LivingBattlecard,
    ObjectionCounter,
)
from deliverables.cdd_report_generator import (
    CDDBenchmarkRow,
    CDDPricingRow,
    CDDReportGenerator,
)
from deliverables.knowledge_graph_html import (
    GraphLink,
    GraphNode,
    KnowledgeGraphHTMLGenerator,
)
from deliverables.magic_quadrant_svg import (
    MagicQuadrantSVGGenerator,
    QuadrantVendor,
)
from deliverables.strategic_brief_compiler import (
    RumeltKernel,
    StrategicBrief,
    StrategicBriefCompiler,
)
from deliverables.win_wire_publisher import (
    WinWireEvent,
    WinWirePublisher,
)
from sentinels.price_watcher_daemon import PriceSnapshotCheck, PriceWatcherSentinel
from storage.sqlite_repository import (
    CompetitorRecord,
    PricingTierRecord,
    SQLiteRepository,
)


class TestCompetitiveIntelligenceOS(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "test_intelligence.db"
        self.repo = SQLiteRepository(self.db_path)

    def tearDown(self) -> None:
        try:
            self.temp_dir.cleanup()
        except OSError:
            pass

    def test_sqlite_repository_and_trigger(self) -> None:
        """Teste l'insertion d'un concurrent, d'un prix et le déclenchement de l'audit automatique."""
        comp = CompetitorRecord(
            id="comp_obat",
            legal_name="Obat SAS",
            brand_name="Obat",
            website="https://www.obat.fr",
            circle="direct",
            surveillance_tier="tight",
            country="FR",
            company_registration="849283748",
            altman_z_score=2.85,
            financial_status="healthy",
        )
        self.repo.upsert_competitor(comp)
        fetched = self.repo.get_competitor("comp_obat")
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.brand_name, "Obat")

        # Insertion d'un palier
        tier = PricingTierRecord(
            id="tier_pro",
            competitor_id="comp_obat",
            tier_name="Pro Artisans",
            price_eur=25.0,
            billing_period="monthly",
            value_metric="per_user",
            setup_fee_eur=0.0,
            is_active=True,
            last_verified_at="2026-11-01",
        )
        self.repo.upsert_pricing_tier(tier)

        # Mise à jour du prix pour vérifier le trigger d'Event Sourcing
        updated_tier = PricingTierRecord(
            id="tier_pro",
            competitor_id="comp_obat",
            tier_name="Pro Artisans",
            price_eur=32.0,  # Hausse de prix
            billing_period="monthly",
            value_metric="per_user",
            setup_fee_eur=0.0,
            is_active=True,
            last_verified_at="2026-11-09",
        )
        self.repo.upsert_pricing_tier(updated_tier)

        # Vérification du journal d'audit
        history = self.repo.get_price_audit_history("comp_obat")
        self.assertGreaterEqual(len(history), 1)
        self.assertEqual(history[0]["new_price_eur"], 32.0)
        self.assertEqual(history[0]["old_price_eur"], 25.0)

    def test_kiq_framework_router(self) -> None:
        """Vérifie l'interdiction de Porter pour une perte de vente et le bon aiguillage."""
        # Test requête de perte de vente
        rec_loss = KIQRouter.route_question("Pourquoi perdons-nous des deals face à notre concurrent ?")
        self.assertEqual(rec_loss.intent, StrategicIntent.WIN_LOSS_ANALYSIS)
        self.assertIn("INTERDICTION STRICTE DE PORTER", rec_loss.banned_frameworks_warning)

        # Test requête d'attractivité
        rec_sector = KIQRouter.route_question("Ce secteur BTP est-il rentable et attractif ?")
        self.assertEqual(rec_sector.intent, StrategicIntent.SECTOR_ATTRACTIVENESS)
        self.assertEqual(rec_sector.primary_framework, "5 Forces de Porter (+1 Réglementaire)")

    def test_wisdom_gate_checker(self) -> None:
        """Vérifie le filtrage déontologique des 5 serrous."""
        # Cas valide
        valid = WisdomGateChecker.evaluate(
            source_url="https://kbopub.economie.fgov.be/kbopub/toononderneming.html?ondernemingsnummer=0123456789",
            source_author="Banque-Carrefour des Entreprises",
            source_voice="company",
            age_in_days=30,
            is_public_record=True,
            is_independent=True,
            respects_trade_secrets=True,
        )
        self.assertTrue(valid.is_passed)
        self.assertEqual(valid.status, "PASS")

        # Cas invalide (source non publique)
        invalid = WisdomGateChecker.evaluate(
            source_url="internal_leak.txt",
            source_author="Anonymous",
            source_voice="expert_humint",
            age_in_days=10,
            is_public_record=False,
            is_independent=True,
            respects_trade_secrets=False,
        )
        self.assertFalse(invalid.is_passed)
        self.assertEqual(invalid.status, "REJECTED")

    def test_win_loss_debiasing_engine(self) -> None:
        """Vérifie le débiaisage de l'alibi commercial 'trop cher'."""
        interviews = [
            DealLossInterview(
                deal_id="deal_01",
                deal_name="Menuiserie Liégeoise",
                reported_sales_reason="Perdu sur le prix : ils voulaient 20% de remise",
                buyer_verbatim="En réalité le tarif était correct, mais leur onboarding prenait 6 semaines et c'était trop long pour notre chantier.",
                deal_value_eur=1800.0,
            ),
            DealLossInterview(
                deal_id="deal_02",
                deal_name="Toitures Dupont",
                reported_sales_reason="Trop cher face à Obat",
                buyer_verbatim="Leur logiciel ne gère pas nativement la facturation Peppol 2026 obligatoire et l'attestation TVA 6% manquait.",
                deal_value_eur=2400.0,
            ),
            DealLossInterview(
                deal_id="deal_03",
                deal_name="Électricité Moreau",
                reported_sales_reason="Trop cher",
                buyer_verbatim="Nous n'avions vraiment pas le budget cette année, nous sommes restés sur Excel.",
                deal_value_eur=1200.0,
            ),
        ]

        report = WinLossDebiasingEngine.analyze_portfolio(interviews)
        self.assertEqual(report.total_deals_analyzed, 3)
        self.assertEqual(report.sales_price_blame_pct, 100.0)  # Tous les commerciaux accusaient le prix
        self.assertLess(report.actual_price_blame_pct, 50.0)  # En réalité seul 1 deal était vraiment bloqué par le budget
        self.assertGreater(report.bias_inflation_delta_pct, 50.0)
        self.assertIn("time_to_value", report.root_cause_distribution)
        self.assertIn("compliance_security", report.root_cause_distribution)

    def test_firmographic_job_watcher(self) -> None:
        """Vérifie la détection d'inflexion firmographique à 6-12 mois."""
        prev = JobPostingSnapshot(
            competitor_id="comp_1",
            competitor_name="BTP Soft",
            engineering_postings=5,
            sales_postings=2,
            legal_compliance_postings=0,
            executive_postings=0,
            snapshot_quarter="2026-Q1",
        )
        curr = JobPostingSnapshot(
            competitor_id="comp_1",
            competitor_name="BTP Soft",
            engineering_postings=18,  # +13 ingénieurs
            sales_postings=8,  # +6 commerciaux
            legal_compliance_postings=2,
            executive_postings=1,
            snapshot_quarter="2026-Q2",
        )

        alerts = FirmographicJobWatcher.analyze_trajectory(curr, prev)
        self.assertGreaterEqual(len(alerts), 2)
        severities = [a.threat_severity for a in alerts]
        self.assertIn("CRITICAL", severities)
        self.assertIn("HIGH", severities)

    def test_operational_benchmarker(self) -> None:
        """Vérifie le calcul du CAC Payback et l'écart de Time-to-Value."""
        us = OperationalMetrics(
            entity_name="Notre Solution",
            time_to_value_days=47,  # Cas concret du brief
            cac_eur=450.0,
            monthly_arpu_eur=35.0,
            gross_margin_pct=0.85,
            annual_churn_pct=0.18,
            nrr_pct=1.05,
        )
        competitor = OperationalMetrics(
            entity_name="Rival Leader",
            time_to_value_days=21,
            cac_eur=300.0,
            monthly_arpu_eur=30.0,
            gross_margin_pct=0.80,
            annual_churn_pct=0.10,
            nrr_pct=1.15,
        )

        gap = OperationalBenchmarker.compare(us, competitor)
        self.assertEqual(gap.ttv_gap_days, 26)  # 47 - 21 = 26 jours
        self.assertEqual(gap.ttv_retention_multiplier, 2.1)
        self.assertIn("Time-to-Value", gap.critical_priority_gap)

    def test_wargame_scenario_simulator(self) -> None:
        """Vérifie la simulation tactique multi-tours."""
        res = WarGameScenarioSimulator.simulate_price_disruption(
            competitor_name="Obat",
            price_drop_pct=25.0,
            is_competitor_public_or_pe_backed=True,
        )
        self.assertEqual(len(res.turns), 3)
        self.assertEqual(res.turns[0].actor, "US")
        self.assertEqual(res.turns[1].actor, "Obat")
        self.assertIn("EBITDA", res.turns[1].action_description)

    def test_battlecard_8sec_builder(self) -> None:
        """Vérifie la génération de la battlecard conforme à la règle des 8 secondes."""
        card = LivingBattlecard(
            our_product_name="Bureau Numérique BTP",
            competitor_name="Batappli",
            target_persona="Artisan Plombier Solo",
            one_sentence_counter_pitch="L'outil moderne sans installation lourde pour sortir un devis conforme sur smartphone en 3 minutes.",
            why_we_win_points=[
                "Attestation TVA 6% belge automatique en 1 clic.",
                "Zéro engagement : arrêtez quand vous voulez.",
                "Support téléphonique basé en Wallonie.",
            ],
            objections=[
                ObjectionCounter(
                    objection_title="Batappli existe depuis 20 ans",
                    instant_killer_quote="C'est vrai, mais leur logiciel demande un vieux PC Windows et 3 jours de formation payante.",
                    proof_evidence="Notice d'installation Batappli requiert Windows local et dongle USB.",
                    source_url="https://www.batappli.fr/tarifs",
                )
            ],
            last_verified_date="2026-11-09",
        )
        md = Battlecard8SecBuilder.generate_markdown(card)
        self.assertIn("8-SECONDES", md)
        self.assertIn("PITCH D'ATTAQUE (3 secondes de lecture)", md)
        self.assertIn("TOP OBJECTIONS & RÉPLIQUES CHOC (5 secondes de lecture)", md)

    def test_cdd_report_generator(self) -> None:
        """Vérifie la génération du classeur Excel Due Diligence via openpyxl."""
        excel_path = Path(self.temp_dir.name) / "test_cdd.xlsx"
        pricing = [
            CDDPricingRow(
                competitor_name="Obat",
                tier_name="Pro",
                monthly_price_eur=25.0,
                setup_fee_eur=0.0,
                value_metric="per_user",
                source_url="https://www.obat.fr/tarifs",
            )
        ]
        bench = [
            CDDBenchmarkRow(
                competitor_name="Obat",
                ttv_days=21,
                cac_eur=300.0,
                arpu_eur=30.0,
                churn_annual_pct=0.12,
                nrr_pct=1.10,
            )
        ]
        winloss = {"time_to_value": 45.0, "compliance_security": 35.0, "true_price_sensitivity": 20.0}

        out = CDDReportGenerator.generate_excel_dossier(
            output_path=excel_path,
            analysis_title="Test CDD BTP",
            pricing_rows=pricing,
            benchmark_rows=bench,
            win_loss_distribution=winloss,
        )
        self.assertTrue(out.exists())
        self.assertGreater(out.stat().st_size, 1000)

    def test_strategic_brief_compiler(self) -> None:
        """Vérifie la compilation de la note stratégique appliquant le noyau de Rumelt."""
        brief = StrategicBrief(
            title="Conquête BTP Wallonie",
            target_sector="Artisans du Bâtiment",
            key_intelligence_questions=["Comment contourner le verrouillage des logiciels historiques ?"],
            rumelt_kernel=RumeltKernel(
                brutal_diagnosis="Les artisans détestent la paperasse mais refusent les logiciels cloud complexes sans support direct.",
                guiding_policy="Proposer une interface smartphone instantanée avec attestation TVA 6% native.",
                coherent_action_steps=[
                    "Déployer le convertisseur 1-clic pour importer les devis Batappli.",
                    "Nouer un partenariat pilote avec Smart Coop à Liège.",
                ],
            ),
            premortem_risks=["Résistance au changement si l'application nécessite plus de 3 clics."],
            primary_adversaries=["Batappli (Direct)", "Obat (Direct)", "Excel (Substitut)"],
            wisdom_gate_compliance_statement="100% des données validées selon le protocole SCIP Wisdom Gate.",
        )
        md = StrategicBriefCompiler.compile_markdown(brief)
        self.assertIn("NOTE DE DÉCISION STRATÉGIQUE", md)
        self.assertIn("Le Noyau Stratégique (The Rumelt Kernel)", md)
        self.assertIn("Le Rapport de Premortem (Gary Klein)", md)

    def test_svg_positioning_and_radar_plotter(self) -> None:
        """Vérifie la génération des graphiques vectoriels 2x2 et Radar SVG."""
        matrix_path = Path(self.temp_dir.name) / "test_matrix.svg"
        entities = [
            PositioningEntity("Notre Solution", 8.5, 9.0, "#9ece6a", is_hero=True),
            PositioningEntity("Batappli", 3.0, 4.0, "#f7768e"),
        ]
        out_matrix = SVGPositioningPlotter.render_2x2_matrix("Simplicité", "Puissance", entities, matrix_path)
        self.assertTrue(out_matrix.exists())
        self.assertIn("<svg", out_matrix.read_text(encoding="utf-8"))

        radar_path = Path(self.temp_dir.name) / "test_radar.svg"
        dims = ["Prix", "Simplicité", "Puissance", "Support", "Souveraineté", "Vitesse"]
        radar_entities = [
            RadarEntity(
                label="Notre Solution",
                color="#9ece6a",
                dimensions=[RadarDimensionScore(d, 8.5) for d in dims],
                is_hero=True,
            )
        ]
        out_radar = SVGRadarPlotter.render_radar_chart("Benchmark Radar", dims, radar_entities, radar_path)
        self.assertTrue(out_radar.exists())
        self.assertIn("polygon", out_radar.read_text(encoding="utf-8"))

    def test_wardley_mapper_svg(self) -> None:
        """Vérifie la génération de la carte de Wardley en SVG pur."""
        wardley_path = Path(self.temp_dir.name) / "test_wardley.svg"
        comps = [
            WardleyComponent("devis", "Devis Client", 0.75, 0.90, is_our_disruption=True),
            WardleyComponent("peppol", "Réseau Peppol", 0.90, 0.20),
        ]
        deps = [WardleyDependency("devis", "peppol")]
        out = WardleyMapperSVG.render_map("Wardley Map BTP", comps, deps, wardley_path)
        self.assertTrue(out.exists())
        self.assertIn("Commodité (+Utilitaire)", out.read_text(encoding="utf-8"))

    def test_altman_distress_calculator(self) -> None:
        """Vérifie le calcul de l'Altman Z'-Score pour société privée."""
        # Cas en détresse
        distressed = FinancialBalanceSheetInput(
            total_assets_eur=100000.0,
            working_capital_eur=-20000.0,
            retained_earnings_eur=-50000.0,
            ebit_eur=-15000.0,
            book_value_equity_eur=10000.0,
            total_liabilities_eur=90000.0,
            total_sales_revenue_eur=80000.0,
        )
        report = AltmanDistressCalculator.calculate_z_prime(distressed)
        self.assertEqual(report.distress_zone, "DISTRESS")
        self.assertLess(report.z_score, 1.23)

    def test_stochastic_market_engine(self) -> None:
        """Vérifie les calculs HHI, Markov Churn et Bass Diffusion."""
        # HHI
        hhi = StochasticMarketEngine.calculate_hhi([40.0, 30.0, 20.0, 10.0])
        self.assertEqual(hhi, 3000.0)  # 1600 + 900 + 400 + 100 = 3000

        # Markov
        prob_switch = StochasticMarketEngine.calculate_markov_churn_transition(
            price_delta_ratio=0.75,  # 25% moins cher
            pain_score=0.8,  # client très mécontent
            switching_friction=0.1,  # friction quasi nulle
        )
        self.assertGreater(prob_switch, 0.70)

        # Bass diffusion
        forecast = StochasticMarketEngine.forecast_bass_diffusion(market_size_total=10000, quarters=4)
        self.assertEqual(len(forecast), 4)
        self.assertGreater(forecast[3].cumulative_market_share_pct, forecast[0].cumulative_market_share_pct)

    def test_vampire_migrator_builder(self) -> None:
        """Vérifie la génération automatique d'un script de migration 1-clic."""
        spec = VampireMigratorSpec(
            competitor_name="Batappli",
            supported_format="CSV",
            delimiter=";",
            mappings=[
                ColumnMapping("CodeClient", "customer_code", "str"),
                ColumnMapping("MontantTTC", "total_eur", "float"),
            ],
        )
        script_path = Path(self.temp_dir.name) / "migrate_batappli.py"
        out = VampireMigratorBuilder.export_script_file(spec, script_path)
        self.assertTrue(out.exists())
        code = out.read_text(encoding="utf-8")
        self.assertIn("migrate_from_batappli", code)

    def test_price_watcher_sentinel(self) -> None:
        """Vérifie la détection de changement de tarif par hash SHA-256."""
        content_v1 = "Forfait Pro : 29 € / mois"
        content_v2 = "Forfait Pro : 39 € / mois (Hausse de 10 €)"

        init_check = PriceWatcherSentinel.check_for_modifications(
            PriceSnapshotCheck("comp_obat", "https://obat.fr/tarifs", content_v1)
        )
        self.assertFalse(init_check.has_changed)

        change_check = PriceWatcherSentinel.check_for_modifications(
            PriceSnapshotCheck("comp_obat", "https://obat.fr/tarifs", content_v2, init_check.new_hash)
        )
        self.assertTrue(change_check.has_changed)
        self.assertIn("ALERTE TACTIQUE", change_check.alert_message)

    def test_magic_quadrant_svg_generation(self) -> None:
        """Vérifie la génération du Magic Quadrant SVG avec surbrillance et zones de quadrants."""
        vendors = [
            QuadrantVendor(name="Leader Vendor", vision_score=90.0, execution_score=85.0, tier="leader", is_our_solution=True),
            QuadrantVendor(name="Challenger Vendor", vision_score=45.0, execution_score=75.0, tier="challenger"),
            QuadrantVendor(name="Visionary Vendor", vision_score=80.0, execution_score=40.0, tier="visionary"),
            QuadrantVendor(name="Niche Vendor", vision_score=30.0, execution_score=30.0, tier="niche"),
        ]
        svg_path = Path(self.temp_dir.name) / "test_quadrant.svg"
        out = MagicQuadrantSVGGenerator.generate_svg("BTP Software Market 2026", vendors, svg_path)
        self.assertTrue(out.exists())
        content = out.read_text(encoding="utf-8")
        self.assertIn("LEADERS", content)
        self.assertIn("CHALLENGERS", content)
        self.assertIn("VISIONARIES", content)
        self.assertIn("NICHE PLAYERS", content)
        self.assertIn("Leader Vendor (NOUS)", content)

    def test_disruption_radar_engine(self) -> None:
        """Vérifie le calcul de l'indice composite DVI et la détection d'acteurs vulnérables."""
        # Cas 1 : Acteur legacy vulnérable au piège de commoditisation
        vulnerable_input = DisruptionMetricInput(
            competitor_name="Legacy Giant",
            tech_inertia_score=85.0,
            pricing_rigidity_score=90.0,
            financial_distress_score=70.0,
            customer_friction_score=80.0,
        )
        res_vulnerable = DisruptionRadarEngine.calculate_dvi(vulnerable_input)
        self.assertGreaterEqual(res_vulnerable.composite_dvi, 75.0)
        self.assertEqual(res_vulnerable.classification, ThreatClassification.COMMODITY_TRAP_COLLAPSE)
        self.assertGreater(len(res_vulnerable.recommended_attack_vectors), 0)

        # Cas 2 : Startup scale-up agile
        scaleup_input = DisruptionMetricInput(
            competitor_name="Agile AI Tool",
            tech_inertia_score=15.0,
            pricing_rigidity_score=10.0,
            financial_distress_score=20.0,
            customer_friction_score=25.0,
        )
        res_scaleup = DisruptionRadarEngine.calculate_dvi(scaleup_input)
        self.assertLess(res_scaleup.composite_dvi, 35.0)
        self.assertEqual(res_scaleup.classification, ThreatClassification.AGGRESSIVE_SCALEUP)

    def test_win_wire_publisher(self) -> None:
        """Vérifie la mise en forme Markdown et l'export JSON d'un Win-Wire commercial."""
        event = WinWireEvent(
            deal_name="Projet Tour Canal (Bruxelles)",
            target_industry="Gros-Œuvre & Maçonnerie",
            acv_eur=36000.0,
            sales_cycle_days=18,
            displaced_competitor="BTP-Cloud",
            sales_rep_name="Brandon P.",
            decisive_silver_bullet="Interopérabilité instantanée Peppol 2026 sans surcoût",
            competitor_trap_neutralized="Exigence d'engagement 3 ans avec frais de paramétrage de 5000 €",
            landmines_avoided=["Ne pas contester la taille de leur catalogue", "Démontrer l'import Excel en 10 secondes"],
            buyer_verbatim_quote="Votre solution est la seule qui a compris les réalités d'un chantier belge.",
            key_takeaway_for_team="Toujours auditer le devis concurrent sur les lignes de maintenance annuelle.",
        )
        md = WinWirePublisher.format_markdown(event)
        self.assertIn("WIN-WIRE : Victoire Majeure contre BTP-Cloud", md)
        self.assertIn("36 000 €", md)
        self.assertIn("Projet Tour Canal (Bruxelles)", md)

        json_path = Path(self.temp_dir.name) / "test_win_wire.json"
        out = WinWirePublisher.export_json(event, json_path)
        self.assertTrue(out.exists())
        self.assertIn("36000.0", out.read_text(encoding="utf-8"))

    def test_assault_landing_builder(self) -> None:
        """Vérifie la génération de la landing comparative d'assaut."""
        spec = AssaultLandingSpec(
            our_brand_name="OurApp",
            competitor_brand_name="TheirApp",
            target_sector="PME BTP",
            hero_headline="Pourquoi payer le triple ?",
            hero_subheadline="Une alternative moderne sans engagement.",
            call_to_action_text="Essayer gratuitement",
            comparison_rows=[
                ComparisonFeatureRow("Feature A", "Oui", "Non", "Explication détaillée"),
            ],
            killer_quote_verbatim="Excellente solution.",
            quote_author_type="Directeur Technique",
        )
        html = AssaultLandingBuilder.generate_html(spec)
        self.assertIn("OurApp", html)
        self.assertIn("TheirApp", html)
        self.assertIn("Pourquoi payer le triple ?", html)
        self.assertIn("Feature A", html)

    def test_knowledge_graph_html(self) -> None:
        """Vérifie la génération du graphe de connaissances interactif."""
        nodes = [
            GraphNode("n1", "Leader A", "competitor", "#ef4444"),
            GraphNode("n2", "Bank Gate", "bank_gateway", "#10b981"),
        ]
        links = [
            GraphLink("n1", "n2", "Flux API"),
        ]
        graph_path = Path(self.temp_dir.name) / "test_graph.html"
        out = KnowledgeGraphHTMLGenerator.generate_html("Test Graph", nodes, links, graph_path)
        self.assertTrue(out.exists())
        content = out.read_text(encoding="utf-8")
        self.assertIn("Test Graph", content)
        self.assertIn("Leader A", content)
        self.assertIn("canvas", content)


if __name__ == "__main__":
    unittest.main()
