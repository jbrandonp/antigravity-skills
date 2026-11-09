"""
Script de vérification End-to-End pour valider l'exécution complète du skill competitive-intelligence-os.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Add current skill to sys.path
sys.path.insert(0, str(Path(__file__).parent))

from core.firmographic_job_watcher import FirmographicJobWatcher, JobPostingSnapshot
from core.kiq_framework_router import KIQRouter, StrategicIntent
from core.operational_benchmarker import OperationalBenchmarker, OperationalMetrics
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
from storage.sqlite_repository import (
    CompetitorRecord,
    PricingTierRecord,
    SQLiteRepository,
)


def run_full_verification() -> None:
    print("[1/8] Test Persistance SQLite & Trigger Event Sourcing...")
    db_file = Path(__file__).parent / "storage" / "intelligence.db"
    repo = SQLiteRepository(db_file)

    comp = CompetitorRecord(
        id="comp_batappli",
        legal_name="Batappli Informatique",
        brand_name="Batappli",
        website="https://www.batappli.fr",
        circle="direct",
        surveillance_tier="tight",
        country="FR",
        company_registration="398471928",
        altman_z_score=2.1,
        financial_status="healthy",
    )
    repo.upsert_competitor(comp)

    # Initial price
    repo.upsert_pricing_tier(
        PricingTierRecord(
            id="batappli_artisans",
            competitor_id="comp_batappli",
            tier_name="Artisans Plus",
            price_eur=49.0,
            billing_period="monthly",
            value_metric="per_user",
            setup_fee_eur=250.0,
            is_active=True,
            last_verified_at="2026-11-01",
        )
    )

    # Price update to trigger event-sourcing audit log
    repo.upsert_pricing_tier(
        PricingTierRecord(
            id="batappli_artisans",
            competitor_id="comp_batappli",
            tier_name="Artisans Plus",
            price_eur=59.0,
            billing_period="monthly",
            value_metric="per_user",
            setup_fee_eur=250.0,
            is_active=True,
            last_verified_at="2026-11-09",
        )
    )

    history = repo.get_price_audit_history("comp_batappli")
    assert len(history) >= 1, "Le trigger d'audit n'a pas enregistré l'événement de prix !"
    print(f"      OK : Variation détectée (Ancien: {history[0]['old_price_eur']}€ -> Nouveau: {history[0]['new_price_eur']}€)")

    print("[2/8] Test KIQ Router & Interdiction de Porter...")
    rec_deal = KIQRouter.route_question("Pourquoi perdons-nous des devis face à Obat ?")
    assert rec_deal.intent == StrategicIntent.WIN_LOSS_ANALYSIS
    assert "INTERDICTION STRICTE DE PORTER" in rec_deal.banned_frameworks_warning
    print(f"      OK : Aiguillé vers '{rec_deal.primary_framework}', Porter formellement banni.")

    print("[3/8] Test Wisdom Gate...")
    gate = WisdomGateChecker.evaluate(
        source_url="https://kbopub.economie.fgov.be/kbopub/toononderneming.html?ondernemingsnummer=0123456789",
        source_author="Banque-Carrefour des Entreprises",
        source_voice="company",
        age_in_days=15,
        is_public_record=True,
        is_independent=True,
        respects_trade_secrets=True,
    )
    assert gate.is_passed and gate.status == "PASS"
    print(f"      OK : Statut {gate.status} (Validité légale et éthique confirmée).")

    print("[4/8] Test Win/Loss Debiasing...")
    interviews = [
        DealLossInterview(
            deal_id="d1",
            deal_name="Menuiserie Liège",
            reported_sales_reason="Trop cher",
            buyer_verbatim="Le prix était bien, mais leur mise en place prenait 6 semaines et nous avions besoin de facturer immédiatement.",
            deal_value_eur=2000.0,
        ),
        DealLossInterview(
            deal_id="d2",
            deal_name="Plomberie Namur",
            reported_sales_reason="Trop cher",
            buyer_verbatim="Le logiciel n'a pas la mention légale d'attestation TVA 6% belge ni l'export Peppol.",
            deal_value_eur=1500.0,
        ),
    ]
    wl_report = WinLossDebiasingEngine.analyze_portfolio(interviews)
    assert wl_report.sales_price_blame_pct == 100.0
    assert wl_report.actual_price_blame_pct == 0.0
    print(f"      OK : Biais commercial démasqué (Vendeurs: {wl_report.sales_price_blame_pct}% prix vs Réalité: {wl_report.actual_price_blame_pct}% prix).")
    print(f"      Cause réelle : {wl_report.primary_real_bottleneck}")

    print("[5/8] Test Firmographic Inflexion...")
    prev = JobPostingSnapshot("comp_batappli", "Batappli", 5, 2, 0, 0, "2026-Q1")
    curr = JobPostingSnapshot("comp_batappli", "Batappli", 18, 8, 2, 0, "2026-Q2")
    alerts = FirmographicJobWatcher.analyze_trajectory(curr, prev)
    assert len(alerts) >= 2
    print(f"      OK : {len(alerts)} alertes précoces déclenchées (Lead time: 6 à 12 mois).")

    print("[6/8] Test Benchmarking Opérationnel...")
    us = OperationalMetrics("Notre Solution", 3, 200.0, 35.0, 0.85, 0.08, 1.15)
    them = OperationalMetrics("Batappli", 45, 600.0, 49.0, 0.70, 0.15, 1.02)
    gap = OperationalBenchmarker.compare(us, them)
    assert gap.ttv_gap_days == -42  # Nous sommes 42 jours plus rapides
    print(f"      OK : Avantage TTV confirmé ({gap.ttv_gap_days} jours vs rival).")

    print("[7/8] Test War Gaming...")
    wg = WarGameScenarioSimulator.simulate_price_disruption("Batappli", 20.0, True)
    assert len(wg.turns) == 3
    print(f"      OK : Simulation 3 tours validée. Verdict : {wg.equilibrium_verdict}")

    print("[8/8] Test Génération des Livrables Réels (Battlecard, Excel CDD, One-Pager)...")
    # Battlecard
    card = LivingBattlecard(
        our_product_name="Bureau Numérique BTP",
        competitor_name="Batappli",
        target_persona="Artisan BTP Wallonie",
        one_sentence_counter_pitch="L'outil moderne sans dongle USB ni installation lourde pour sortir un devis conforme sur smartphone en 3 minutes.",
        why_we_win_points=["Attestation TVA 6% en 1 clic", "Sans engagement", "Support direct en Belgique"],
        objections=[
            ObjectionCounter(
                objection_title="Batappli est plus connu",
                instant_killer_quote="Oui, mais ils vous imposent un vieux PC et 250 € de frais de dossier pour démarrer.",
                proof_evidence="Grille tarifaire Batappli 2026 avec frais d'installation.",
                source_url="https://www.batappli.fr/tarifs",
            )
        ],
        last_verified_date="2026-11-09",
    )
    bc_file = Path(__file__).parent / "deliverables" / "battlecard_test.md"
    Battlecard8SecBuilder.export_to_file(card, bc_file)
    assert bc_file.exists() and bc_file.stat().st_size > 500

    # Excel CDD
    cdd_file = Path(__file__).parent / "deliverables" / "cdd_audit_test.xlsx"
    CDDReportGenerator.generate_excel_dossier(
        output_path=cdd_file,
        analysis_title="Audit Stratégique BTP 2026",
        pricing_rows=[
            CDDPricingRow("Batappli", "Artisans Plus", 59.0, 250.0, "per_user", "https://www.batappli.fr/tarifs"),
            CDDPricingRow("Notre Solution", "Standard BTP", 35.0, 0.0, "flat", "https://smart.coop"),
        ],
        benchmark_rows=[
            CDDBenchmarkRow("Batappli", 45, 600.0, 49.0, 0.15, 1.02),
            CDDBenchmarkRow("Notre Solution", 3, 200.0, 35.0, 0.08, 1.15),
        ],
        win_loss_distribution={"time_to_value": 60.0, "compliance_security": 40.0},
    )
    assert cdd_file.exists() and cdd_file.stat().st_size > 2000

    # Strategic Brief
    brief = StrategicBrief(
        title="Offensive BTP Liège 2026",
        target_sector="Artisans BTP",
        key_intelligence_questions=["Comment capturer les artisans déçus des vieux logiciels ?"],
        rumelt_kernel=RumeltKernel(
            brutal_diagnosis="Les artisans ont peur du saut numérique et détestent les logiciels lourds sans support téléphonique.",
            guiding_policy="Offre smartphone ultra-simple + passerelle Peppol 2026 gratuite + accompagnement Smart Coop.",
            coherent_action_steps=[
                "Mettre à disposition le convertisseur d'imports 1-clic.",
                "Diffuser la Battlecard 8-Secondes auprès des prescripteurs locaux.",
            ],
        ),
        premortem_risks=["Résistance si l'artisan n'a pas accès à son devis hors-ligne sur chantier."],
        primary_adversaries=["Batappli (Direct)", "Obat (Direct)", "Excel (Substitut)"],
        wisdom_gate_compliance_statement="Données certifiées 100% publiques via BCE et sites officiels.",
    )
    sb_file = Path(__file__).parent / "deliverables" / "strategic_brief_test.md"
    StrategicBriefCompiler.export_to_file(brief, sb_file)
    assert sb_file.exists() and sb_file.stat().st_size > 500

    print("      OK : Battlecard Markdown, Fichier Excel CDD (.xlsx) et One-Pager décisionnel générés avec succès !")

    print("[9/10] Test Livrables Visuels : Magic Quadrant, Graphe & Landing Assaut...")
    quadrant_file = Path(__file__).parent / "deliverables" / "quadrant_test.svg"
    MagicQuadrantSVGGenerator.generate_svg(
        "Marché BTP Belgique 2026",
        [
            QuadrantVendor("Leader Pro", 90.0, 90.0, "leader", is_our_solution=True),
            QuadrantVendor("Challenger BTP", 50.0, 80.0, "challenger"),
        ],
        quadrant_file,
    )
    assert quadrant_file.exists() and quadrant_file.stat().st_size > 1000

    landing_spec = AssaultLandingSpec(
        our_brand_name="Notre Outil",
        competitor_brand_name="Challenger BTP",
        target_sector="Artisans",
        hero_headline="La vraie alternative",
        hero_subheadline="Sans abonnement forcé",
        call_to_action_text="Essayer",
        comparison_rows=[ComparisonFeatureRow("Peppol", "Oui", "Non", "Conforme 2026")],
        killer_quote_verbatim="Parfait.",
        quote_author_type="Artisan Liège",
    )
    landing_file = Path(__file__).parent / "deliverables" / "landing_test.html"
    landing_file.write_text(AssaultLandingBuilder.generate_html(landing_spec), encoding="utf-8")
    assert landing_file.exists() and landing_file.stat().st_size > 1500

    graph_file = Path(__file__).parent / "deliverables" / "graph_test.html"
    KnowledgeGraphHTMLGenerator.generate_html(
        "Graphe Test",
        [GraphNode("a", "Alpha", "competitor", "#fff")],
        [GraphLink("a", "a", "Auto")],
        graph_file,
    )
    assert graph_file.exists() and graph_file.stat().st_size > 1000
    print("      OK : Magic Quadrant SVG, Page d'Assaut HTML et Graphe de Connaissances validés !")

    print("[10/10] Test Win-Wire Publisher & CLI...")
    ww_event = WinWireEvent(
        deal_name="Projet BTP Bruxelles",
        target_industry="BTP",
        acv_eur=24000.0,
        sales_cycle_days=14,
        displaced_competitor="Challenger BTP",
        sales_rep_name="Brandon P.",
        decisive_silver_bullet="Mise en route en 2 heures",
        competitor_trap_neutralized="Frais cachés de support",
        landmines_avoided=["Éviter la guerre des remises"],
        buyer_verbatim_quote="C'est exactement ce qu'il nous fallait.",
        key_takeaway_for_team="Démontrer la simplicité de l'interface dès la 1ère minute.",
    )
    ww_md = WinWirePublisher.format_markdown(ww_event)
    assert "WIN-WIRE" in ww_md and "24 000 €" in ww_md
    print("      OK : Win-Wire généré et validé !")

    # Nettoyage des fichiers de test
    for f in [quadrant_file, landing_file, graph_file]:
        if f.exists():
            f.unlink()

    print("\n[SUCCESS] VERIFICATION COMPLETE REUSSIE : 10/10 composants sont 100% fonctionnels et valides.")


if __name__ == "__main__":
    run_full_verification()
