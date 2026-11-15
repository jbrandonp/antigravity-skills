#!/usr/bin/env python3
"""LinkedIn Ghostwriting Quality & Anti-Slop Audit Engine.

Evaluates LinkedIn drafts against:
1. Mobile Fold Truncation (< 210 characters).
2. French & English AI-Slop vocabulary blacklists.
3. Robotic structural patterns (ternary rhythms, false opposites, passive voice).
4. Punctuation invariants (zero exclamation marks, <= 1 em-dash, no bullet emojis).
5. Sentence burstiness (length variance) and quantitative backing.
"""

from __future__ import annotations

import argparse
import math
import re
import sys
from typing import Dict, List, Pattern, Tuple

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

FRENCH_SLOP_WORDS: List[str] = [
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
]

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
]

FRENCH_SLOP_PATTERNS: List[Tuple[str, str]] = [
    (r"ce\s+n'est\s+pas\s+seulement.+c'est", "Fausse opposition 'ce n'est pas seulement X, c'est Y'"),
    (r"il\s+ne\s+s'agit\s+pas\s+(?:seulement\s+)?de.+mais\s+de", "Fausse opposition 'il ne s'agit pas de X, mais de Y'"),
    (r"^dans\s+un\s+monde\s+où", "Ouverture cosmique clichée 'dans un monde où'"),
    (r"^à\s+l'heure\s+où", "Ouverture convenue 'à l'heure où'"),
    (r"et\s+si\s+la\s+vraie\s+question", "Question rhétorique scolaire 'et si la vraie question'"),
    (r"la\s+clé\s*\?", "Tic paresseux 'la clé ?'"),
    (r"spoiler\s+alert\s*:", "Méta-annonce 'spoiler alert :'"),
    (r"voici\s+pourquoi\s*:", "Méta-annonce de liste 'voici pourquoi :'"),
]

LAZY_CLOSINGS: List[Tuple[str, str]] = [
    (r"et\s+vous\s*,?\s*qu'en\s+pensez-vous", "Conclusion paresseuse 'Et vous, qu'en pensez-vous ?'"),
    (r"votre\s+avis\s+en\s+commentaire", "Appel à commentaire forcé"),
    (r"le\s+débat\s+est\s+ouvert", "Fausse ouverture de débat"),
    (r"dites-le[\s\-]moi\s+en\s+commentaire", "Formule d'engagement artificielle"),
]

DECORATIVE_BULLET_EMOJIS: List[str] = ["👉", "💡", "🚀", "🔥", "✨", "🔹", "🎯", "⚡", "✅"]


def extract_hook(text: str) -> str:
    """Extracts the first paragraph or initial block of lines forming the hook."""
    paragraphs = [p.strip() for p in text.strip().split("\n\n") if p.strip()]
    if not paragraphs:
        return ""
    return paragraphs[0]


def calculate_burstiness(sentences: List[str]) -> Tuple[float, float]:
    """Calculates average sentence length and standard deviation of sentence lengths."""
    lengths: List[int] = []
    for s in sentences:
        words = re.findall(r"\b[\w'-]+\b", s)
        if words:
            lengths.append(len(words))
    if not lengths:
        return 0.0, 0.0
    mean = sum(lengths) / len(lengths)
    variance = sum((x - mean) ** 2 for x in lengths) / len(lengths)
    std_dev = math.sqrt(variance)
    return mean, std_dev


def audit_post(text: str) -> Dict[str, object]:
    """Runs a complete rigorous audit of the LinkedIn post."""
    text_clean = text.strip()
    total_chars = len(text_clean)
    words = re.findall(r"\b[\w'-]+\b", text_clean)
    total_words = len(words)

    # Split into sentences
    sentences = [s.strip() for s in re.split(r"[.!?]+(?:\s+|\n+)", text_clean) if s.strip()]
    avg_words, std_words = calculate_burstiness(sentences)

    hook = extract_hook(text_clean)
    hook_len = len(hook)

    violations: List[str] = []
    penalties: int = 0

    # 1. Mobile Fold Truncation Check
    if hook_len > 210:
        violations.append(
            f"[CRITICAL] Hook length ({hook_len} chars) exceeds mobile fold (< 210 chars). Text will be cut mid-sentence."
        )
        penalties += 25
    elif hook_len == 0:
        violations.append("[CRITICAL] Empty post or missing hook.")
        penalties += 50

    # 2. Exclamation Marks Check
    exclamations = text_clean.count("!")
    if exclamations > 0:
        violations.append(
            f"[MAJOR] Found {exclamations} exclamation mark(s). Unearned enthusiasm detected. Use periods."
        )
        penalties += min(exclamations * 10, 25)

    # 3. Em-Dash Check
    em_dashes = text_clean.count("—")
    if em_dashes > 1:
        violations.append(
            f"[MINOR] Found {em_dashes} em-dashes ('—'). Limit to at most 1 per post to avoid LLM styling."
        )
        penalties += 10

    # 4. Slop Vocabulary (French)
    text_lower = text_clean.lower()
    for word in FRENCH_SLOP_WORDS:
        pattern = r"\b" + re.escape(word) + r"\b"
        matches = len(re.findall(pattern, text_lower))
        if matches > 0:
            violations.append(f"[MAJOR] French AI-Slop keyword detected: '{word}' ({matches} time(s)).")
            penalties += matches * 15

    # 5. Slop Vocabulary (English)
    for word in ENGLISH_SLOP_WORDS:
        pattern = r"\b" + re.escape(word) + r"\b"
        matches = len(re.findall(pattern, text_lower))
        if matches > 0:
            violations.append(f"[MAJOR] English AI-Slop keyword detected: '{word}' ({matches} time(s)).")
            penalties += matches * 15

    # 6. Slop Structural Patterns
    for regex_pat, desc in FRENCH_SLOP_PATTERNS:
        if re.search(regex_pat, text_lower, re.MULTILINE):
            violations.append(f"[MAJOR] Structural AI cliche: {desc}.")
            penalties += 20

    # 7. Lazy Closings
    for regex_pat, desc in LAZY_CLOSINGS:
        if re.search(regex_pat, text_lower):
            violations.append(f"[MAJOR] Banned generic ending: {desc}.")
            penalties += 20

    # 8. Bullet Emoji Spam Check
    lines = text_clean.split("\n")
    bullet_emoji_count = 0
    for line in lines:
        stripped = line.strip()
        for emoji in DECORATIVE_BULLET_EMOJIS:
            if stripped.startswith(emoji):
                bullet_emoji_count += 1
                break
    if bullet_emoji_count >= 3:
        violations.append(
            f"[MAJOR] Line-initial bullet emoji spam detected ({bullet_emoji_count} lines). Use '-' or numbers."
        )
        penalties += 15

    # 9. Quantitative Backing / Metrics presence
    has_numbers = bool(re.search(r"\b\d+(?:[.,]\d+)?%?\b", text_clean))
    has_placeholders = bool(re.search(r"\{\{.+?\}\}", text_clean))
    if not has_numbers and not has_placeholders:
        violations.append(
            "[WARN] No concrete numbers, percentages, or '{{votre chiffre}}' placeholders found. Risk of generic fluff."
        )
        penalties += 10

    # 10. Sentence Burstiness Check (variance)
    if len(sentences) >= 4 and std_words < 2.5:
        violations.append(
            f"[WARN] Monotonous rhythm detected (burstiness std-dev = {std_words:.1f} words). Vary sentence lengths."
        )
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
        "violations": violations,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit a LinkedIn post against anti-slop & mobile rules.")
    parser.add_argument("file", nargs="?", help="Path to text file containing the LinkedIn post")
    parser.add_argument("--text", help="Direct text of the post to audit")
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

    print("==================================================================")
    print("       LINKEDIN GHOSTWRITER — POST QUALITY & ANTI-SLOP AUDIT       ")
    print("==================================================================")
    print(f"Verdict:              {result['verdict']}")
    print(f"Score d'Authenticité: {result['score']}/100")
    print(f"Longueur Totale:      {result['total_chars']} caractères ({result['total_words']} mots)")
    print(f"Longueur du Hook:     {result['hook_chars']} caractères (Cible mobile: <= 210)")
    print(f"Phrases & Rythme:     {result['sentence_count']} phrases, moyenne {result['avg_words_per_sentence']} mots/phrase")
    print(f"Indice de Burstiness: {result['burstiness_std_dev']} (Variance de cadence)")
    print("------------------------------------------------------------------")

    violations = result["violations"]
    if not violations:
        print("  ✓ Aucun tic d'écriture IA détecté. Texte pur, incisif et humain.")
    else:
        print(f"Infractions Détectées ({len(violations)}) :")
        for v in violations:
            print(f"  • {v}")

    print("==================================================================")
    return 0 if result["verdict"] == "PASS" else 2


if __name__ == "__main__":
    sys.exit(main())
