"""
Point d'Entrée CLI Unifié de Competitive Intelligence OS.
Permet d'exécuter l'ensemble des modules d'analyse stratégique, de simulation
et de génération de livrables en ligne de commande locale (Zero Docker, 100% natif).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from core.altman_distress_calculator import (
    AltmanDistressCalculator,
    FinancialBalanceSheetInput,
)
from core.disruption_radar_index import (
    DisruptionMetricInput,
    DisruptionRadarEngine,
)
from core.kiq_framework_router import KIQRouter
from core.operational_benchmarker import (
    OperationalBenchmarker,
    OperationalMetrics,
)
from core.wargame_scenario_simulator import WarGameScenarioSimulator
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
from deliverables.knowledge_graph_html import (
    GraphLink,
    GraphNode,
    KnowledgeGraphHTMLGenerator,
)
from deliverables.magic_quadrant_svg import (
    MagicQuadrantSVGGenerator,
    QuadrantVendor,
)
from deliverables.win_wire_publisher import (
    WinWireEvent,
    WinWirePublisher,
)
from storage.sqlite_repository import SQLiteRepository


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ci-os",
        description="Competitive Intelligence OS — Suite de renseignement stratégique et d'aide à la décision B2B",
    )
    subparsers = parser.add_subparsers(dest="subcommand", help="Commandes disponibles")

    # 1. Route KIQ
    p_route = subparsers.add_parser("route", help="Aiguille une question stratégique vers le bon framework")
    p_route.add_argument("query", type=str, help="Question stratégique en langage naturel")

    # 2. Battlecard
    p_battlecard = subparsers.add_parser("battlecard", help="Génère une battlecard exécutive en 8 secondes")
    p_battlecard.add_argument("competitor_id", type=str, help="ID du concurrent dans SQLite ou nom")
    p_battlecard.add_argument("--out", type=Path, default=Path("battlecard.md"), help="Chemin du fichier Markdown")

    # 3. Quadrant Gartner
    p_quadrant = subparsers.add_parser("quadrant", help="Génère un Magic Quadrant vectoriel pur en SVG")
    p_quadrant.add_argument("--out", type=Path, default=Path("magic_quadrant.svg"), help="Chemin de sortie SVG")

    # 4. Disruption Radar
    p_disruption = subparsers.add_parser("disruption", help="Calcule l'indice composite DVI (0-100)")
    p_disruption.add_argument("competitor_name", type=str, help="Nom du concurrent")
    p_disruption.add_argument("--tech", type=float, default=65.0, help="Inertie tech (0-100)")
    p_disruption.add_argument("--price", type=float, default=70.0, help="Rigidité tarifaire (0-100)")
    p_disruption.add_argument("--fin", type=float, default=50.0, help="Détresse financière (0-100)")
    p_disruption.add_argument("--fric", type=float, default=60.0, help="Friction client (0-100)")

    # 5. Wargame
    p_wargame = subparsers.add_parser("wargame", help="Simule un scénario wargaming Shell/IBM en 3 tours")
    p_wargame.add_argument("competitor_name", type=str, help="Nom du concurrent")
    p_wargame.add_argument("--price-drop", type=float, default=20.0, help="Baisse de prix en pourcentage (ex: 20.0 pour -20%%)")
    p_wargame.add_argument("--pe-backed", action="store_true", help="Le concurrent est-il soutenu par un fonds PE ou coté en bourse ?")

    # 6. Benchmarker
    p_bench = subparsers.add_parser("bench", help="Calcule les écarts opérationnels (TTV, CAC Payback, NRR)")
    p_bench.add_argument("--us-ttv", type=int, required=True, help="Notre Time-to-Value (jours)")
    p_bench.add_argument("--them-ttv", type=int, required=True, help="Leur Time-to-Value (jours)")
    p_bench.add_argument("--us-cac", type=float, required=True, help="Notre CAC (€)")
    p_bench.add_argument("--them-cac", type=float, required=True, help="Leur CAC (€)")
    p_bench.add_argument("--us-arpu", type=float, required=True, help="Notre ARPU mensuel (€)")
    p_bench.add_argument("--them-arpu", type=float, required=True, help="Leur ARPU mensuel (€)")
    p_bench.add_argument("--margin", type=float, default=0.80, help="Marge brute (défaut: 0.80)")
    p_bench.add_argument("--us-churn", type=float, default=0.08, help="Notre churn annuel (défaut: 0.08)")
    p_bench.add_argument("--them-churn", type=float, default=0.22, help="Leur churn annuel (défaut: 0.22)")
    p_bench.add_argument("--us-nrr", type=float, default=1.15, help="Notre NRR (ex: 1.15)")
    p_bench.add_argument("--them-nrr", type=float, default=0.95, help="Leur NRR (ex: 0.95)")

    # 7. Landing Assaut
    p_landing = subparsers.add_parser("landing", help="Génère une landing page web comparative d'assaut (HTML5/Tailwind)")
    p_landing.add_argument("competitor_name", type=str, help="Nom du concurrent comparé")
    p_landing.add_argument("--out", type=Path, default=Path("landing_assaut.html"), help="Chemin de sortie HTML")

    # 8. Graphe de Connaissances
    p_graph = subparsers.add_parser("graph", help="Génère un graphe de connaissances interactif (HTML5 Canvas)")
    p_graph.add_argument("--out", type=Path, default=Path("market_graph.html"), help="Chemin de sortie HTML")

    # 9. Win-Wire
    p_winwire = subparsers.add_parser("win-wire", help="Publie une alerte Win-Wire de victoire commerciale")
    p_winwire.add_argument("deal_name", type=str, help="Nom du compte / affaire gagnée")
    p_winwire.add_argument("competitor", type=str, help="Concurrent évincé")
    p_winwire.add_argument("--acv", type=float, default=45000.0, help="Valeur annuelle en euros")
    p_winwire.add_argument("--bullet", type=str, default="Interopérabilité instantanée Peppol 2026 sans surcoût", help="Argument décisif")

    # 10. Altman Z-Score
    p_zscore = subparsers.add_parser("zscore", help="Calcule l'Altman Z'-Score pour PME non cotée")
    p_zscore.add_argument("--wc", type=float, required=True, help="Fonds de roulement net (€)")
    p_zscore.add_argument("--ta", type=float, required=True, help="Actif total (€)")
    p_zscore.add_argument("--re", type=float, required=True, help="Bénéfices non distribués / Réserves (€)")
    p_zscore.add_argument("--ebit", type=float, required=True, help="EBIT / Résultat d'exploitation (€)")
    p_zscore.add_argument("--be", type=float, required=True, help="Capitaux propres comptables (€)")
    p_zscore.add_argument("--tl", type=float, required=True, help="Total des dettes / Passif (€)")
    p_zscore.add_argument("--sales", type=float, default=1000000.0, help="Chiffre d'affaires annuel (€)")

    # 11. Wisdom Gate
    p_wisdom = subparsers.add_parser("wisdom", help="Évalue la légalité et l'éthique SCIP d'une source")
    p_wisdom.add_argument("source_url", type=str, help="URL de la source (ex: https://justice.belgium.be/...)")
    p_wisdom.add_argument("--author", type=str, default="Registre Public", help="Auteur de la source")
    p_wisdom.add_argument("--voice", type=str, default="analyst", help="Type de voix (analyst, company, journalist, expert_humint)")
    p_wisdom.add_argument("--age", type=int, default=30, help="Âge de la source en jours")
    p_wisdom.add_argument("--public", action="store_true", help="La source est-elle publique ?")
    p_wisdom.add_argument("--independent", action="store_true", help="La source est-elle indépendante ?")
    p_wisdom.add_argument("--respects-secrets", action="store_true", help="Respecte-t-elle le secret des affaires ?")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if not args.subcommand:
        parser.print_help()
        return 0

    if args.subcommand == "route":
        rec = KIQRouter.route_question(args.query)
        print(f"\n[DECISION STRATEGIQUE] Intention détectée : {rec.intent.value}")
        print(f"Framework principal recommandé : {rec.primary_framework}")
        print(f"Framework secondaire : {rec.secondary_framework}")
        print(f"Résultat attendu : {rec.expected_outcome}")
        print(f"Sources requises : {', '.join(rec.required_data_sources)}")
        print(f"Avertissement frameworks interdits : [!] {rec.banned_frameworks_warning}")
        print(f"Métrique actionnable : {rec.actionable_metric}\n")

    elif args.subcommand == "battlecard":
        db_path = Path(__file__).parent / "storage" / "intelligence.db"
        comp_name = args.competitor_id
        if db_path.exists():
            repo = SQLiteRepository(db_path)
            comp = repo.get_competitor(args.competitor_id)
            if not comp:
                all_comps = repo.list_competitors()
                found = next((c for c in all_comps if c.id == args.competitor_id or c.brand_name.lower() == args.competitor_id.lower()), None)
                if found:
                    comp_name = found.brand_name
            else:
                comp_name = comp.brand_name

        card = LivingBattlecard(
            our_product_name="BTP-Pro Suite",
            competitor_name=comp_name,
            target_persona="Dirigeant PME BTP / Conducteur de travaux",
            one_sentence_counter_pitch=f"BTP-Pro Suite est opérationnel en 24h sans formation lourde, là où {comp_name} impose 3 mois d'implémentation et des frais de support cachés.",
            why_we_win_points=[
                "Time-to-Value 6x plus rapide (prêt à l'emploi le jour même)",
                "Conformité Peppol 2026 et TVA 6% incluse nativement sans surcoût",
                "Application 100% fonctionnelle en mobilité hors-ligne sur les chantiers",
            ],
            objections=[
                ObjectionCounter(
                    objection_title=f"{comp_name} est le leader établi du marché",
                    instant_killer_quote="Leur réputation repose sur leur ancienneté, mais leurs clients dénoncent un support saturé et des hausses annuelles de +15%.",
                    proof_evidence="Étude Win/Loss Q3 2026 : 64% des départs de leur plateforme sont causés par le support.",
                    source_url="https://audit-saas-btp.be/etude-defections-2026",
                ),
                ObjectionCounter(
                    objection_title="Vos tarifs semblent trop abordables pour être complets",
                    instant_killer_quote="Nous n'avons pas d'armée de commerciaux à amortir : toute notre valeur est dans le produit.",
                    proof_evidence="100% des fonctionnalités critiques (devis, factures d'avancement, Peppol) sont incluses.",
                    source_url="https://btp-pro-suite.be/tarifs-transparents",
                ),
            ],
            last_verified_date="2026-11-09",
        )
        md_content = Battlecard8SecBuilder.generate_markdown(card)
        args.out.write_text(md_content, encoding="utf-8")
        print(f"[SUCCESS] Battlecard générée pour '{comp_name}' -> {args.out.resolve()}")

    elif args.subcommand == "quadrant":
        vendors = [
            QuadrantVendor(name="Notre Solution", vision_score=92.0, execution_score=88.0, tier="leader", is_our_solution=True),
            QuadrantVendor(name="BTP-Cloud Inc", vision_score=55.0, execution_score=78.0, tier="challenger"),
            QuadrantVendor(name="ArchiDev Vision", vision_score=85.0, execution_score=40.0, tier="visionary"),
            QuadrantVendor(name="Legacy-BTP Tools", vision_score=30.0, execution_score=35.0, tier="niche"),
        ]
        out_path = MagicQuadrantSVGGenerator.generate_svg(
            title="Marché Logiciels BTP Belgique 2026",
            vendors=vendors,
            output_path=args.out,
        )
        print(f"[SUCCESS] Magic Quadrant SVG généré -> {out_path.resolve()}")

    elif args.subcommand == "disruption":
        disrupt_input = DisruptionMetricInput(
            competitor_name=args.competitor_name,
            tech_inertia_score=args.tech,
            pricing_rigidity_score=args.price,
            financial_distress_score=args.fin,
            customer_friction_score=args.fric,
        )
        disrupt_res = DisruptionRadarEngine.calculate_dvi(disrupt_input)
        print(f"\n[DISRUPTION RADAR] Concurrent : {disrupt_res.competitor_name}")
        print(f"Score Composite DVI : {disrupt_res.composite_dvi}/100")
        print(f"Classification : {disrupt_res.classification.value}")
        print(f"Diagnostic : {disrupt_res.strategic_rationale}")
        print("Vecteurs d'attaque recommandés :")
        for v in disrupt_res.recommended_attack_vectors:
            print(f"  - [*] {v}")
        print()

    elif args.subcommand == "wargame":
        wargame_res = WarGameScenarioSimulator.simulate_price_disruption(
            competitor_name=args.competitor_name,
            price_drop_pct=args.price_drop,
            is_competitor_public_or_pe_backed=args.pe_backed,
        )
        print(f"\n[WARGAME SIMULATION] Scénario : {wargame_res.scenario_name}")
        print(f"Verdict d'équilibre : {wargame_res.equilibrium_verdict}")
        print("Chronologie des tours :")
        for t in wargame_res.turns:
            print(f"  Tour {t.turn_number} [{t.actor} - {t.action_type}] : {t.action_description}")
            print(f"     -> Impact : {t.expected_market_impact}")
        print("\nAngles morts stratégiques révélés :")
        for b in wargame_res.strategic_blindspots_revealed:
            print(f"  - [!] {b}")
        print("\nPlans d'actions conditionnels :")
        for p in wargame_res.conditional_action_plans:
            print(f"  - [ACTION] {p}")
        print()

    elif args.subcommand == "bench":
        us = OperationalMetrics(
            entity_name="Notre Solution",
            time_to_value_days=args.us_ttv,
            cac_eur=args.us_cac,
            monthly_arpu_eur=args.us_arpu,
            gross_margin_pct=args.margin,
            annual_churn_pct=args.us_churn,
            nrr_pct=args.us_nrr,
        )
        them = OperationalMetrics(
            entity_name="Concurrent de référence",
            time_to_value_days=args.them_ttv,
            cac_eur=args.them_cac,
            monthly_arpu_eur=args.them_arpu,
            gross_margin_pct=args.margin,
            annual_churn_pct=args.them_churn,
            nrr_pct=args.them_nrr,
        )
        bench = OperationalBenchmarker.compare(us=us, competitor=them)
        print("\n[BENCHMARK OPERATIONNEL]")
        print(f"Écart TTV : {bench.ttv_gap_days} jours (Avantage rétention x{bench.ttv_retention_multiplier})")
        print(f"Payback CAC (Nous) : {bench.cac_payback_months_us:.1f} mois")
        print(f"Payback CAC (Eux)  : {bench.cac_payback_months_them:.1f} mois")
        print(f"Écart Churn : {bench.churn_gap_pct:+.1f} pts de pourcentage")
        print(f"Priorité critique : {bench.critical_priority_gap}")
        print(f"Plan d'action : {bench.action_plan_summary}\n")

    elif args.subcommand == "landing":
        spec = AssaultLandingSpec(
            our_brand_name="BTP-Pro Suite",
            competitor_brand_name=args.competitor_name,
            target_sector="Entrepreneurs BTP & Artisans en Belgique",
            hero_headline=f"Déçu par les hausses de prix de {args.competitor_name} ?",
            hero_subheadline="Passez à la solution tout-en-un conforme Peppol 2026, sans surcoût caché et avec reprise intégrale de vos devis.",
            call_to_action_text="Démarrer mon essai gratuit (Migration offerte)",
            comparison_rows=[
                ComparisonFeatureRow("Conformité Peppol / TVA 6%", "✅ Native & Gratuite", "❌ Option payante (30 €/m)", "Facturation électronique obligatoire dès 2026"),
                ComparisonFeatureRow("Time-to-Value (Prise en main)", "✅ Moins de 24h", "❌ 3 à 6 semaines", "Import automatisé de vos fichiers Excel et clients"),
                ComparisonFeatureRow("Tarification à l'usage", "✅ Transparente et sans engagement", "❌ Forfait annuel verrouillé", "Résiliable à tout moment en 1 clic"),
            ],
            killer_quote_verbatim="On a divisé par 4 le temps passé sur nos devis de chantier, et on ne paye plus d'options inutiles.",
            quote_author_type="Patron PME Rénovation (Bruxelles)",
        )
        content = AssaultLandingBuilder.generate_html(spec)
        args.out.write_text(content, encoding="utf-8")
        print(f"[SUCCESS] Page d'assaut comparative générée -> {args.out.resolve()}")

    elif args.subcommand == "graph":
        nodes = [
            GraphNode("us", "Notre Plateforme", "competitor", "#3b82f6"),
            GraphNode("comp_a", "BTP-Cloud", "competitor", "#ef4444"),
            GraphNode("comp_b", "ArchiSoft", "competitor", "#f59e0b"),
            GraphNode("fund_x", "Cobepa PE Fund", "investor_fund", "#8b5cf6"),
            GraphNode("bank_y", "Isabel 6 / Peppol", "bank_gateway", "#10b981"),
        ]
        links = [
            GraphLink("fund_x", "comp_a", "Actionnaire majoritaire (80%)"),
            GraphLink("comp_a", "bank_y", "Passerelle exclusive"),
            GraphLink("us", "bank_y", "Interopérabilité directe"),
            GraphLink("us", "comp_a", "Vampire Migration active"),
            GraphLink("comp_b", "comp_a", "Partenariat commercial"),
        ]
        out = KnowledgeGraphHTMLGenerator.generate_html("Écosystème BTP Tech Belgique", nodes, links, args.out)
        print(f"[SUCCESS] Graphe de connaissances interactif généré -> {out.resolve()}")

    elif args.subcommand == "win-wire":
        event = WinWireEvent(
            deal_name=args.deal_name,
            target_industry="BTP / Construction Générale",
            acv_eur=args.acv,
            sales_cycle_days=21,
            displaced_competitor=args.competitor,
            sales_rep_name="Brandon P.",
            decisive_silver_bullet=args.bullet,
            competitor_trap_neutralized="Ils exigeaient 12 mois d'engagement et facturaient le module Peppol en sus.",
            landmines_avoided=[
                "Ne pas dénigrer leur interface, mais insister sur la lenteur du support technique.",
                "Faire une démonstration en direct de l'import de 500 articles du bordereau des prix en 30 secondes.",
            ],
            buyer_verbatim_quote="Votre outil a fait en 5 minutes ce que leur commercial nous promettait depuis 3 mois.",
            key_takeaway_for_team="Face à cet acteur, toujours demander au prospect s'il a chiffré le coût de leur support payant.",
        )
        print(WinWirePublisher.format_markdown(event))

    elif args.subcommand == "zscore":
        sheet_input = FinancialBalanceSheetInput(
            working_capital_eur=args.wc,
            total_assets_eur=args.ta,
            retained_earnings_eur=args.re,
            ebit_eur=args.ebit,
            book_value_equity_eur=args.be,
            total_liabilities_eur=args.tl,
            total_sales_revenue_eur=args.sales,
        )
        zscore_res = AltmanDistressCalculator.calculate_z_prime(sheet_input)
        print(f"\n[ALTMAN Z'-SCORE PME] Score calculé : {zscore_res.z_score:.2f}")
        print(f"Zone de détresse : {zscore_res.distress_zone}")
        print(f"Probabilité de faillite à 12 mois : {zscore_res.bankruptcy_risk_12m_pct:.1f}%")
        print(f"Recommandation stratégique : {zscore_res.predatory_action_recommendation}")
        print(f"Détail des ratios : {zscore_res.detailed_ratios}\n")

    elif args.subcommand == "wisdom":
        audit = WisdomGateChecker.evaluate(
            source_url=args.source_url,
            source_author=args.author,
            source_voice=args.voice,
            age_in_days=args.age,
            is_public_record=args.public,
            is_independent=args.independent,
            respects_trade_secrets=args.respects_secrets,
        )
        status = "ACCEPTEE" if audit.is_passed else "REJETEE"
        print(f"\n[WISDOM GATE SCIP] Verdict : {status} (Statut : {audit.status})")
        print(f"Audit : {audit.audit_notes}")
        if audit.reasons:
            print("Motifs de rejet ou réserves :")
            for r in audit.reasons:
                print(f"  - [!] {r}")
        print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
