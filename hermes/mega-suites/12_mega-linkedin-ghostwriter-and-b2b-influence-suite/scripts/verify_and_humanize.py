#!/usr/bin/env python3
"""Unified LinkedIn Ghostwriting Linter, Watermark Cleaner & Anti-Slop Audit Engine.

Fuses the best heuristics from:
- samber/cc-skills (humaniseur-fr & linkedin-ghostwriting)
- blader/humanizer (Wikipedia 26 anti-AI patterns)
- Jakeschincariol/linkedin-agent-skill (invisible watermark stripping & 5 detection panels)
- coreyhaines31/marketingskills (specificity, falsifiability, active voice)
"""

from __future__ import annotations

import argparse
import math
import re
import sys
from typing import Dict, List, Pattern, Tuple

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# 17 classes of invisible characters & LLM watermarks
INVISIBLE_CHARS: List[str] = [
    "\u200B",  # Zero-width space
    "\u200C",  # Zero-width non-joiner
    "\u200D",  # Zero-width joiner
    "\u2060",  # Word joiner
    "\uFEFF",  # Byte order mark / Zero-width no-break space
    "\u00AD",  # Soft hyphen
    "\u200E",  # Left-to-right mark
    "\u200F",  # Right-to-left mark
    "\u202A",  # Left-to-right embedding
    "\u202B",  # Right-to-left embedding
    "\u202C",  # Pop directional formatting
    "\u202D",  # Left-to-right override
    "\u202E",  # Right-to-left override
    "\u2061",  # Function application
    "\u2062",  # Invisible times
    "\u2063",  # Invisible separator
    "\u2064",  # Invisible plus
]

# French AI-slop vocabulary (top 30 markers)
FRENCH_SLOP_WORDS: List[str] = [
    "crucial",
    "essentiel",
    "décryptage",
    "incontournable",
    "catalyseur",
    "révolutionner",
    "holistique",
    "synergie",
    "pierre angulaire",
    "force motrice",
    "gage de",
    "s'avérer",
    "écosystème",
    "à l'ère de",
    "enjeu crucial",
    "indéniable",
    "il convient de",
    "force est de constater",
    "vecteur",
    "résilience",
    "pépite",
    "maestro",
    "ovni",
    "game-changer",
    "mindset",
    "bienveillant",
    "notamment",
    "disruptif",
    "substantiel",
    "pleinement",
]

# English AI-slop vocabulary (Wikipedia & detectors)
ENGLISH_SLOP_WORDS: List[str] = [
    "delve",
    "tapestry",
    "leverage",
    "foster",
    "harness",
    "crucial",
    "realm",
    "navigate",
    "testament",
    "game-changer",
    "unlock",
    "robust",
    "paradigm shift",
    "holistic",
    "beacon",
    "multifaceted",
    "pivotal",
    "bespoke",
    "meticulous",
    "underscore",
    "showcase",
    "enduring",
]

# Banned structural cliches (French & English)
STRUCTURAL_PATTERNS: List[Tuple[str, str]] = [
    (r"ce\s+n'est\s+pas\s+seulement.+c'est", "Fausse opposition 'ce n'est pas seulement X, c'est Y'"),
    (r"il\s+ne\s+s'agit\s+pas\s+(?:seulement\s+)?de.+mais\s+de", "Fausse opposition 'il ne s'agit pas de X, mais de Y'"),
    (r"^dans\s+un\s+monde\s+où", "Ouverture cosmique 'dans un monde où'"),
    (r"^à\s+l'heure\s+où", "Ouverture convenue 'à l'heure où'"),
    (r"^dans\s+le\s+paysage\s+(?:actuel|numérique|technologique)", "Ouverture clichée 'dans le paysage...'"),
    (r"et\s+si\s+la\s+vraie\s+question", "Question rhétorique scolaire 'et si la vraie question'"),
    (r"la\s+clé\s*\?", "Tic paresseux 'la clé ?'"),
    (r"spoiler\s+alert\s*:", "Méta-annonce 'spoiler alert :'"),
    (r"voici\s+pourquoi\s*:", "Méta-annonce de liste 'voici pourquoi :'"),
    (r"plongeons\s+dans", "Traduction littérale de 'let's dive in'"),
    (r"not\s+just\s+.+,\s+it's\s+", "English false opposition 'not just X, it's Y'"),
    (r"it's\s+not\s+.+,\s+it's\s+", "English false opposition 'it's not X, it's Y'"),
    (r"let's\s+dive\s+in", "English staged run-up 'let's dive in'"),
    (r"read\s+that\s+again", "Arrogant one-line closer 'read that again'"),
    (r"let\s+that\s+sink\s+in", "Arrogant one-line closer 'let that sink in'"),
]

LAZY_CLOSINGS: List[Tuple[str, str]] = [
    (r"et\s+vous\s*,?\s*qu'en\s+pensez-vous", "Conclusion paresseuse 'Et vous, qu'en pensez-vous ?'"),
    (r"votre\s+avis\s+en\s+commentaire", "Appel à commentaire forcé"),
    (r"le\s+débat\s+est\s+ouvert", "Fausse ouverture de débat"),
    (r"dites-le[\s\-]moi\s+en\s+commentaire", "Formule d'engagement artificielle"),
    (r"thoughts\s*\?", "English lazy closing 'Thoughts?'"),
    (r"agree\s*\?", "English lazy closing 'Agree?'"),
]

CHATBOT_RESIDUE: List[str] = [
    r"^voici\s+(?:un\s+aperçu|une\s+analyse|le\s+post).*$",
    r"^j'espère\s+que\s+cela\s+vous\s+(?:sera\s+utile|aidera).*$",
    r"^n'hésitez\s+pas\s+si\s+vous\s+avez\s+des\s+questions.*$",
    r"^here\s+is\s+(?:a\s+draft|the\s+post).*$",
    r"^i\s+hope\s+this\s+helps.*$",
]

DECORATIVE_BULLET_EMOJIS: List[str] = ["👉", "💡", "🚀", "🔥", "✨", "🔹", "🎯", "⚡", "✅"]


def clean_text(raw_text: str) -> Tuple[str, List[str]]:
    """Automatically strips invisible watermarks, normalizes dashes and cleans residue."""
    cleaned = raw_text
    actions: List[str] = []

    # 1. Strip invisible characters
    invis_count = 0
    for char in INVISIBLE_CHARS:
        if char in cleaned:
            invis_count += cleaned.count(char)
            cleaned = cleaned.replace(char, "")
    if invis_count > 0:
        actions.append(f"Suppression de {invis_count} caractère(s) invisible(s) / filigrane(s)")

    # 2. Clean chatbot residue lines
    lines = cleaned.split("\n")
    filtered_lines: List[str] = []
    for line in lines:
        is_residue = False
        stripped = line.strip().lower()
        for pat in CHATBOT_RESIDUE:
            if re.match(pat, stripped):
                is_residue = True
                actions.append(f"Suppression de résidu de chat : '{line.strip()}'")
                break
        if not is_residue:
            filtered_lines.append(line)
    cleaned = "\n".join(filtered_lines)

    # 3. Normalize em dashes (limit to max 1, convert excess)
    em_dashes = cleaned.count("—")
    if em_dashes > 1:
        parts = cleaned.split("—")
        # Keep only the first em-dash, convert others to commas/colons
        cleaned = parts[0] + "—" + ", ".join(parts[1:])
        actions.append(f"Normalisation de {em_dashes - 1} tiret(s) cadratin(s) excessif(s)")

    return cleaned.strip(), actions


def extract_hook(text: str) -> str:
    """Extracts the initial paragraph or block constituting the mobile hook."""
    paragraphs = [p.strip() for p in text.strip().split("\n\n") if p.strip()]
    return paragraphs[0] if paragraphs else ""


def calculate_burstiness(sentences: List[str]) -> Tuple[float, float]:
    """Calculates mean words per sentence and standard deviation (burstiness)."""
    lengths: List[int] = []
    for s in sentences:
        words = re.findall(r"\b[\w'-]+\b", s)
        if words:
            lengths.append(len(words))
    if not lengths:
        return 0.0, 0.0
    mean = sum(lengths) / len(lengths)
    variance = sum((x - mean) ** 2 for x in lengths) / len(lengths)
    return mean, math.sqrt(variance)


def audit_post(text: str) -> Dict[str, object]:
    """Runs a 5-panel forensic audit of the LinkedIn draft."""
    clean_draft, clean_actions = clean_text(text)
    total_chars = len(clean_draft)
    words = re.findall(r"\b[\w'-]+\b", clean_draft)
    total_words = len(words)

    # Sentence parsing
    sentences = [s.strip() for s in re.split(r"[.!?]+(?:\s+|\n+)", clean_draft) if s.strip()]
    avg_words, std_words = calculate_burstiness(sentences)

    hook = extract_hook(clean_draft)
    hook_len = len(hook)

    violations: List[str] = []
    penalties: int = 0

    # PANEL 1 : Mobile Fold Geometry (< 210 chars)
    if hook_len > 210:
        violations.append(
            f"[CRITICAL] Hook length ({hook_len} chars) exceeds mobile fold (< 210 chars). Text cut mid-sentence."
        )
        penalties += 30
    elif hook_len == 0:
        violations.append("[CRITICAL] Empty draft or missing hook.")
        penalties += 50
    elif hook_len < 40:
        violations.append("[WARN] Hook is suspiciously short (< 40 chars). Missing context.")
        penalties += 10

    # PANEL 2 : Punctuation & Formatting Invariants
    exclamations = clean_draft.count("!")
    if exclamations > 0:
        violations.append(f"[MAJOR] Found {exclamations} exclamation mark(s). Unearned hype detected. Use periods.")
        penalties += min(exclamations * 10, 25)

    em_dashes = clean_draft.count("—")
    if em_dashes > 1:
        violations.append(f"[MINOR] Found {em_dashes} em-dashes ('—'). Limit to at most 1 per post.")
        penalties += 10

    lines = clean_draft.split("\n")
    bullet_emoji_count = sum(1 for line in lines if any(line.strip().startswith(em) for em in DECORATIVE_BULLET_EMOJIS))
    if bullet_emoji_count >= 3:
        violations.append(f"[MAJOR] Line-initial bullet emoji spam ({bullet_emoji_count} lines). Use '-' or numbers.")
        penalties += 15

    # PANEL 3 : Slop Lexicon Density (FR & EN)
    text_lower = clean_draft.lower()
    for word in FRENCH_SLOP_WORDS:
        m = len(re.findall(r"\b" + re.escape(word) + r"\b", text_lower))
        if m > 0:
            violations.append(f"[MAJOR] French AI-Slop keyword: '{word}' ({m}x).")
            penalties += m * 15

    for word in ENGLISH_SLOP_WORDS:
        m = len(re.findall(r"\b" + re.escape(word) + r"\b", text_lower))
        if m > 0:
            violations.append(f"[MAJOR] English AI-Slop keyword: '{word}' ({m}x).")
            penalties += m * 15

    # PANEL 4 : Structural Cliches & Lazy Endings
    for regex_pat, desc in STRUCTURAL_PATTERNS:
        if re.search(regex_pat, text_lower, re.MULTILINE):
            violations.append(f"[MAJOR] Structural AI pattern: {desc}.")
            penalties += 20

    for regex_pat, desc in LAZY_CLOSINGS:
        if re.search(regex_pat, text_lower):
            violations.append(f"[MAJOR] Lazy generic ending: {desc}.")
            penalties += 20

    # PANEL 5 : Specificity, Burstiness & Substance
    has_numbers = bool(re.search(r"\b\d+(?:[.,]\d+)?%?\b", clean_draft))
    has_placeholders = bool(re.search(r"\{\{.+?\}\}", clean_draft))
    if not has_numbers and not has_placeholders:
        violations.append("[WARN] No concrete numbers, %, or '{{votre métrique}}' found. Risk of generic fluff.")
        penalties += 15

    if len(sentences) >= 4 and std_words < 2.5:
        violations.append(
            f"[WARN] Low sentence burstiness (std-dev = {std_words:.1f} words). Monotonous robotic rhythm."
        )
        penalties += 10

    # Passive voice check (Zombie Test heuristic: être + participe passé)
    passive_matches = len(re.findall(r"\b(?:été|sont|étaient|fut|furent)\s+[a-zéèêë]+(?:é|és|ée|ées)\b", text_lower))
    if passive_matches >= 3:
        violations.append(f"[WARN] Passive voice density ({passive_matches} occurrences). Apply Zombie Test.")
        penalties += 10

    final_score = max(0, 100 - penalties)
    verdict = "PASS" if final_score >= 80 and not any("[CRITICAL]" in v for v in violations) else "FAIL"

    return {
        "score": final_score,
        "verdict": verdict,
        "total_chars": total_chars,
        "total_words": total_words,
        "hook_chars": hook_len,
        "sentence_count": len(sentences),
        "avg_words_per_sentence": round(avg_words, 1),
        "burstiness_std_dev": round(std_words, 1),
        "clean_actions": clean_actions,
        "violations": violations,
        "clean_text": clean_draft,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Unified LinkedIn Ghostwriting Quality & Anti-Slop Audit Engine.")
    parser.add_argument("file", nargs="?", help="Path to text file containing the draft")
    parser.add_argument("--text", help="Direct text of the draft to audit")
    parser.add_argument("--clean", action="store_true", help="Output automatically cleaned text directly")
    args = parser.parse_args()

    content = ""
    if args.text:
        content = args.text
    elif args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading file '{args.file}': {e}", file=sys.stderr)
            return 1
    elif not sys.stdin.isatty():
        content = sys.stdin.read()
    else:
        parser.print_help()
        return 1

    result = audit_post(content)

    if args.clean:
        print(result["clean_text"])
        return 0

    print("==================================================================")
    print("      MEGA LINKEDIN GHOSTWRITER — 5-PANEL QUALITY & ANTI-SLOP     ")
    print("==================================================================")
    print(f"Verdict:              {result['verdict']}")
    print(f"Score d'Authenticité: {result['score']}/100")
    print(f"Longueur Totale:      {result['total_chars']} caractères ({result['total_words']} mots)")
    print(f"Longueur du Hook:     {result['hook_chars']} caractères (Cible mobile: 140 à 210)")
    print(f"Phrases & Rythme:     {result['sentence_count']} phrases, moyenne {result['avg_words_per_sentence']} mots/phrase")
    print(f"Indice de Burstiness: {result['burstiness_std_dev']} (Variance de cadence, cible: >= 3.5)")
    print("------------------------------------------------------------------")

    actions: List[str] = result["clean_actions"]  # type: ignore[assignment]
    if actions:
        print("Actions Automatiques Réalisées :")
        for a in actions:
            print(f"  ✓ {a}")
        print("------------------------------------------------------------------")

    violations: List[str] = result["violations"]  # type: ignore[assignment]
    if not violations:
        print("  ✓ Zéro tic d'écriture IA détecté. Texte pur, incisif, prêt pour publication.")
    else:
        print(f"Infractions Détectées ({len(violations)}) :")
        for v in violations:
            print(f"  • {v}")

    print("==================================================================")
    return 0 if result["verdict"] == "PASS" else 2


if __name__ == "__main__":
    sys.exit(main())
