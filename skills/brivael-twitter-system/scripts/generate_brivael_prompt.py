#!/usr/bin/env python3
"""
generate_brivael_prompt.py - Interactive CLI Scaffolder for Brivael Le Pogam (@brivael) prompts.

Guides the user through the 3 mandatory pillars (Empirical Ground, Target, Reframing Axiom)
and formats the prompt for Claude with appropriate sub-skill routing.
Includes optional clipboard copy via Windows clip.exe.
"""

import sys
import argparse
import subprocess
from typing import Dict

MODES: Dict[str, str] = {
    "0": "00_SKILL_master_engine (Méta-Compilateur & Levier Cognitif Anti-Slop)",
    "1": "01_SKILL_systemic_investigation (Enquêtes Macro, Cartels, Step 1 & Reads the Minds - EN/FR)",
    "2": "02_SKILL_french_cultural_offensive (Guerre Culturelle, Manifeste D'où je parle & Riposte Déroulons - FR)",
    "3": "03_SKILL_minimalist_sniper (Quote-Tweets, Assertions Unhedged 1-3 lignes - Bilingue)",
}


def create_prompt(mode: str, skin_in_the_game: str, target: str, reframing_axiom: str, language: str) -> str:
    subskill = MODES.get(mode, "00_SKILL_master_engine")
    
    prompt = f"""[ACTIVATION SKILL: {subskill}]
Langue demandée : {language.upper()}

=== MUNITIONS BRUTES FOURNIES PAR L'HUMAIN (LEVIER COGNITIF) ===
1. ANCRAGE DE TERRAIN / SKIN IN THE GAME :
{skin_in_the_game}

2. LA CIBLE / LE PARASITE ÉTAGE 1 :
{target}

3. L'AXIOME DE REFRAMING RADICAL :
{reframing_axiom}

=== RÈGLES D'EXÉCUTION ABSOLUES ===
- Paragraphes <= 3 lignes sur mobile.
- 40% de phrases staccato (<= 6 mots).
- ZÉRO point d'exclamation (!).
- ZÉRO question ouverte d'engagement mou.
- Utiliser la balise <scratchpad> pour décomposer la causalité avant de rédiger.
"""
    return prompt


def copy_to_clipboard(text: str) -> bool:
    """Copie le texte dans le presse-papiers Windows via clip.exe."""
    try:
        process = subprocess.Popen(["clip.exe"], stdin=subprocess.PIPE, shell=True)
        process.communicate(text.encode("utf-8"))
        return process.returncode == 0
    except Exception:
        return False


def main() -> None:
    parser = argparse.ArgumentParser(description="Générateur de prompt calibré pour la suite Brivael Le Pogam.")
    parser.add_argument("--mode", choices=["0", "1", "2", "3"], help="Numéro du pilier tactique (0-3)")
    parser.add_argument("--skin", help="Ancrage de terrain / Skin in the game")
    parser.add_argument("--target", help="La cible ou l'illusion institutionnelle")
    parser.add_argument("--axiom", help="L'axiome polémique tranché")
    parser.add_argument("--lang", default="FR", choices=["FR", "EN"], help="Langue de sortie (FR ou EN)")
    parser.add_argument("--copy", action="store_true", help="Copier automatiquement le prompt généré dans le presse-papiers Windows")

    args = parser.parse_args()

    if args.mode is None:
        print("\n" + "=" * 65)
        print(" 🎯 GÉNÉRATEUR DE PROMPTS BRIVAEL LE POGAM (@brivael) v5.0")
        print("=" * 65)
        print("Sélectionnez le pilier consolidé :")
        for k, v in MODES.items():
            print(f"  [{k}] {v}")
        mode = input("\nVotre choix (0-3) [défaut 1] : ").strip() or "1"
        skin = input("\n1. Ancrage réel / Chiffre / Vécu (Skin in the game) : ").strip()
        target = input("2. La cible / L'illusion (Le ministre, le média, le cartel) : ").strip()
        axiom = input("3. L'axiome de reframing radical (La vérité sans concession) : ").strip()
        lang = input("4. Langue (FR/EN) [défaut FR] : ").strip().upper() or "FR"
        should_copy = input("5. Copier dans le presse-papiers ? (o/n) [défaut o] : ").strip().lower() != "n"
    else:
        mode = args.mode
        skin = args.skin or "Observateur empirique du terrain."
        target = args.target or "Bureaucratie centrale."
        axiom = args.axiom or "La valeur réelle est créée par les producteurs, pas par les normes."
        lang = args.lang
        should_copy = args.copy

    output_prompt = create_prompt(mode, skin, target, axiom, lang)
    print("\n" + "=" * 65)
    print(" 🚀 PROMPT COMPILÉ POUR CLAUDE :")
    print("=" * 65)
    print(output_prompt)
    print("=" * 65)

    if should_copy:
        success = copy_to_clipboard(output_prompt)
        if success:
            print("📋 [SUCCÈS] Le prompt a été copié dans votre presse-papiers Windows !")
        else:
            print("ℹ️ Copie manuelle requise.")
    print()


if __name__ == "__main__":
    main()
