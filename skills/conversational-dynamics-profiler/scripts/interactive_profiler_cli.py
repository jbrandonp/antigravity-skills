#!/usr/bin/env python3
"""
interactive_profiler_cli.py
---------------------------
Unified Terminal Cockpit & Interactive CLI Suite for Conversational Dynamics Profiler.
Provides a comprehensive menu-driven or one-shot command interface to:
1. Normalize & Anonymize raw chat archives (Meta JSON, WhatsApp, Telegram, Discord, CSV)
2. Compute stochastic metrics (Shannon Entropy, RTT Latency, Burstiness, Gottman)
3. Generate 360° Clinical Relationship Health Reports (/100)
4. Export standalone interactive HTML/SVG Dashboards (100% offline)
5. Run predictive 'What-If' conversational stress tests
6. Execute the automated regression test suite

Zero external dependencies - 100% Python 3.10+ standard library.
Strictly typed: Zero untyped parameters or generic wildcards, in accordance with project standards.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys


SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
TESTS_DIR = os.path.join(os.path.dirname(SCRIPTS_DIR), "tests")


def print_banner():
    banner = """
================================================================================
  🕵️  CONVERSATIONAL DYNAMICS PROFILER & RELATIONSHIP INTELLIGENCE (v8.0)
================================================================================
"""
    print(banner)


def menu():
    print("Sélectionnez une opération :")
    print("  [1] Normaliser & Anonymiser un export brut (WhatsApp, Meta, Telegram, Discord, CSV)")
    print("  [2] Exécuter l'audit métrique quantitatif (Entropie, RTT, Gottman 5:1, Bids)")
    print("  [3] Générer le rapport exécutif clinique 360° (Score de santé /100)")
    print("  [4] Exporter le tableau de bord visuel interactif HTML/SVG (100% offline)")
    print("  [5] Lancer le simulateur de crises prédictif ('What-If' & Machine à États)")
    print("  [6] Traducteur & Reformulateur en Communication Non Violente (CNV - OSBD)")
    print("  [7] Exécuter la suite complète de tests automatisés (Self-Test)")
    print("  [0] Quitter")
    print("-" * 80)


def run_pipeline_all(input_file: str, output_prefix: str, anonymize: bool = False):
    if not os.path.exists(input_file):
        print(f"❌ Erreur : Fichier source introuvable : {input_file}")
        return

    print(f"\n🚀 Lancement du pipeline complet sur : {input_file}")
    norm_file = f"{output_prefix}_normalized.json"
    metrics_file = f"{output_prefix}_metrics.md"
    rep_file = f"{output_prefix}_rapport_sante.md"
    dash_file = f"{output_prefix}_dashboard.html"

    # Step 1: Normalize
    cmd_norm = [sys.executable, "-B", os.path.join(SCRIPTS_DIR, "universal_chat_converter.py"), "-i", input_file, "-o", norm_file]
    if anonymize:
        cmd_norm.append("-a")
    print("➔ Étape 1/4 : Normalisation universelle...")
    subprocess.run(cmd_norm, check=True)

    # Step 2: Quantitative Metrics Markdown
    cmd_metrics = [sys.executable, "-B", os.path.join(SCRIPTS_DIR, "analyze_chat_metrics.py"), "-i", norm_file, "-o", metrics_file, "-f", "markdown"]
    print("➔ Étape 2/4 : Calcul des métriques stochastiques & Gottman...")
    subprocess.run(cmd_metrics, check=True)

    # Step 3: Health Report
    cmd_rep = [sys.executable, "-B", os.path.join(SCRIPTS_DIR, "generate_relationship_report.py"), "-i", norm_file, "-o", rep_file]
    print("➔ Étape 3/4 : Synthèse du rapport clinique 360°...")
    subprocess.run(cmd_rep, check=True)

    # Step 4: HTML Dashboard
    cmd_dash = [sys.executable, "-B", os.path.join(SCRIPTS_DIR, "export_html_dashboard.py"), "-i", norm_file, "-o", dash_file]
    print("➔ Étape 4/4 : Génération du tableau de bord HTML/SVG...")
    subprocess.run(cmd_dash, check=True)

    print("\n✅ Pipeline exécuté avec succès !")
    print(f"  • Corpus normalisé : {norm_file}")
    print(f"  • Audit métrique   : {metrics_file}")
    print(f"  • Rapport clinique : {rep_file}")
    print(f"  • Dashboard visuel : {dash_file}\n")


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Unified Interactive Terminal Cockpit.")
    parser.add_argument("--run-all", action="store_true", help="Execute entire end-to-end pipeline in batch mode")
    parser.add_argument("--input", "-i", type=str, default="", help="Input chat file")
    parser.add_argument("--output-prefix", "-o", type=str, default="audit_output", help="Prefix for output artifacts")
    parser.add_argument("--anonymize", "-a", action="store_true", help="Enable PII anonymization")
    args = parser.parse_args()

    if args.run_all and args.input:
        run_pipeline_all(args.input, args.output_prefix, args.anonymize)
        return

    print_banner()

    # Interactive mode
    while True:
        try:
            menu()
            choice = input("Votre choix [0-6] : ").strip()

            if choice == "0":
                print("\nFermeture du terminal. À bientôt !")
                break
            elif choice == "1":
                inp = input("Chemin du fichier source brut : ").strip()
                out = input("Chemin de destination JSON normalisé [def: normalized.json] : ").strip() or "normalized.json"
                anon = input("Activer l'anonymisation PII (o/n) [def: n] : ").strip().lower() == "o"
                cmd = [sys.executable, "-B", os.path.join(SCRIPTS_DIR, "universal_chat_converter.py"), "-i", inp, "-o", out]
                if anon:
                    cmd.append("-a")
                subprocess.run(cmd)
            elif choice == "2":
                inp = input("Chemin du fichier JSON normalisé : ").strip()
                subprocess.run([sys.executable, "-B", os.path.join(SCRIPTS_DIR, "analyze_chat_metrics.py"), "-i", inp, "-f", "markdown"])
            elif choice == "3":
                inp = input("Chemin du fichier JSON normalisé : ").strip()
                out = input("Chemin du rapport Markdown [def: rapport.md] : ").strip() or "rapport.md"
                subprocess.run([sys.executable, "-B", os.path.join(SCRIPTS_DIR, "generate_relationship_report.py"), "-i", inp, "-o", out])
            elif choice == "4":
                inp = input("Chemin du fichier JSON normalisé : ").strip()
                out = input("Chemin du dashboard HTML [def: dashboard.html] : ").strip() or "dashboard.html"
                subprocess.run([sys.executable, "-B", os.path.join(SCRIPTS_DIR, "export_html_dashboard.py"), "-i", inp, "-o", out])
            elif choice == "5":
                print("Options : 1. Scénarios What-If | 2. Machine à États Markoviens")
                sub = input("Sous-choix (1 ou 2) [def: 1] : ").strip() or "1"
                if sub == "2":
                    subprocess.run([sys.executable, "-B", os.path.join(SCRIPTS_DIR, "simulate_conversational_scenarios.py"), "--state-machine"])
                else:
                    print("Scénarios disponibles : unannounced_silence, laconism_thumbs_up, boundary_leak, construction_stress")
                    scen = input("Scénario [ou Entrée pour tous] : ").strip()
                    cmd = [sys.executable, "-B", os.path.join(SCRIPTS_DIR, "simulate_conversational_scenarios.py")]
                    if scen:
                        cmd.extend(["-s", scen])
                    subprocess.run(cmd)
            elif choice == "6":
                raw_msg = input("Entrez le message brut à reformuler en CNV : ").strip()
                if raw_msg:
                    subprocess.run([sys.executable, "-B", os.path.join(SCRIPTS_DIR, "simulate_conversational_scenarios.py"), "--cnv-reframe", raw_msg])
            elif choice == "7":
                print("\nLancement de la suite de tests...")
                subprocess.run([sys.executable, "-B", os.path.join(TESTS_DIR, "test_conversational_suite.py")])
            else:
                print("Option non reconnue, veuillez réessayer.")
            print("\n" + "=" * 80 + "\n")
        except KeyboardInterrupt:
            print("\n\nInterruption reçue. Retour au menu principal.")


if __name__ == "__main__":
    main()
