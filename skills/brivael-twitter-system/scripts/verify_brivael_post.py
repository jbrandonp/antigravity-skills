#!/usr/bin/env python3
"""
verify_brivael_post.py - Deterministic Stylistic & Rhetorical Linter for Brivael Le Pogam (@brivael) style posts.

Audits generated posts against strict quantitative and qualitative criteria:
1. Zero Exclamation Marks (!)
2. Maximum Paragraph Height (<= 3 lines)
3. Staccato Sentence Distribution (Ratio of <= 6 words sentences >= 35%, Target >= 40%)
4. Slop & Platitude Blacklist Enforcement
5. Presence of High-Signal Tactical Anchors (per consolidated pillar)
"""

import sys
import os
import re
import argparse
from typing import List, Dict, Tuple, Union, Optional

BANNED_SLOP_PATTERNS: List[str] = [
    r"dans un monde (en constant|qui change|complexe)",
    r"il est (crucial|essentiel|important|primordial) de",
    r"il convient de",
    r"en conclusion",
    r"à l'ère du numérique",
    r"partie[s]? prenante[s]?",
    r"synergie[s]?",
    r"changer de paradigme",
    r"n'hésitez pas à",
    r"qu'en pensez-vous\s*\?",
    r"in a world where",
    r"it is crucial to",
    r"at the end of the day",
    r"foster collaboration",
    r"game changer",
    r"delve into",
    r"tapestry",
    r"beacon of",
    r"testament to",
]

# Signatures supportant l'architecture consolidée en 4 piliers + rétro-compatibilité
MODE_SIGNATURES: Dict[str, List[str]] = {
    # Consolidated Pillars
    "investigation": ["now connect it", "step 1", "step 2", "step 3", "reads the", "minds"],
    "offensive": ["déroulons", "d'où je parle", "étage", "immeuble", "cyniques", "croyants", "le réel", "doutez de tout"],
    "sniper": [],  # Verified via word count <= 30
    "engine": ["béquille", "levier", "moines copistes", "gutenberg", "taste"],
    
    # Aliases
    "causal": ["now connect it", "step 1", "step 2", "step 3"],
    "manifesto": ["d'où je parle", "je ne suis pas en train de dire", "doutez de tout"],
    "counterstrike": ["déroulons", "étage", "immeuble", "cyniques", "croyants", "le réel arrive"],
    "reads_the_minds": ["reads the", "minds", "episode"],
    "cognitive_lever": ["béquille", "levier", "moines copistes", "gutenberg", "taste"],
}


def audit_post(text: str, mode: Optional[str] = None) -> Tuple[int, List[str], Dict[str, Union[int, float, bool]]]:
    """
    Audit un texte selon les règles stylistiques de Brivael Le Pogam.
    Retourne (score 0-100, liste des violations, métriques).
    """
    violations: List[str] = []
    score: int = 100
    metrics: Dict[str, Union[int, float, bool]] = {}

    # Normalisation universelle des fins de ligne (Windows CRLF -> LF)
    normalized_text = text.replace("\r\n", "\n").replace("\r", "\n")

    # 1. Règle absolue : Zéro point d'exclamation
    exclamation_count = normalized_text.count("!")
    metrics["exclamation_count"] = exclamation_count
    if exclamation_count > 0:
        penalty = exclamation_count * 15
        score -= penalty
        violations.append(
            f"VIOLATION: {exclamation_count} point(s) d'exclamation détecté(s) (-{penalty} pts). "
            f"Brivael est froid et catégorique, jamais hystérique."
        )

    # 2. Règle des paragraphes compacts (<= 3 lignes de texte consécutives)
    paragraphs = [p.strip() for p in normalized_text.split("\n\n") if p.strip()]
    metrics["paragraph_count"] = len(paragraphs)
    oversized_paragraphs = 0
    for idx, p in enumerate(paragraphs, 1):
        lines = [line for line in p.split("\n") if line.strip()]
        if len(lines) > 3:
            oversized_paragraphs += 1
            violations.append(f"VIOLATION: Paragraphe {idx} dépasse 3 lignes ({len(lines)} lignes). Risque de bloc sur mobile.")
    
    if oversized_paragraphs > 0:
        penalty = min(25, oversized_paragraphs * 10)
        score -= penalty

    # 3. Métrique Staccato : phrases de <= 6 mots
    raw_sentences = re.split(r'(?:[.?!]\s+|\n+)', normalized_text)
    valid_sentences = [re.sub(r'^[^\w]+|[^\w]+$', '', s).strip() for s in raw_sentences]
    valid_sentences = [s for s in valid_sentences if len(s.split()) >= 1]
    metrics["sentence_count"] = len(valid_sentences)
    
    short_sentences = 0
    total_words = 0
    for s in valid_sentences:
        word_count = len(s.split())
        total_words += word_count
        if 1 <= word_count <= 6:
            short_sentences += 1
            
    metrics["total_words"] = total_words
    staccato_ratio = (short_sentences / len(valid_sentences)) if valid_sentences else 0.0
    metrics["staccato_ratio"] = round(staccato_ratio * 100, 1)
    
    # Pour le mode sniper : vérification spécifique de la brièveté totale (<= 30 mots)
    if mode and mode.lower() == "sniper":
        if total_words > 35:
            penalty = 25
            score -= penalty
            violations.append(f"VIOLATION SNIPER: Post trop long ({total_words} mots, max 30-35 mots). Doit être un one-liner tranchant.")
    else:
        # Seuil d'alerte staccato pour les posts normaux : < 35% (cible idéale : >= 40%)
        if staccato_ratio < 0.35 and len(valid_sentences) > 3:
            penalty = 15
            score -= penalty
            violations.append(
                f"VIOLATION: Ratio de phrases staccato (<= 6 mots) trop faible: {metrics['staccato_ratio']}% "
                f"(Seuil min: >= 35%, Cible idéale: >= 40%). Manque de punch."
            )

    # 4. Détection du Slop / Jargon corporate
    found_slop: List[str] = []
    text_lower = normalized_text.lower()
    for pattern in BANNED_SLOP_PATTERNS:
        matches = re.findall(pattern, text_lower)
        if matches:
            found_slop.extend(matches)
            
    if found_slop:
        penalty = len(found_slop) * 15
        score -= penalty
        violations.append(f"VIOLATION: Formule(s) creuse(s) ou slop IA détecté(s): {found_slop} (-{penalty} pts).")

    # 5. Détection des questions ouvertes molles
    open_questions = re.findall(r"(qu'en pensez-vous|votre avis|d'accord ou pas|let me know in the comments)", text_lower)
    if open_questions:
        score -= 20
        violations.append(f"VIOLATION: Question d'engagement molle détectée: {open_questions}. Utiliser uniquement des Cornering Questions.")

    # 6. Vérification des marqueurs de mode si spécifié
    if mode and mode.lower() in MODE_SIGNATURES:
        signatures = MODE_SIGNATURES[mode.lower()]
        if signatures:
            found_anchors = [sig for sig in signatures if sig in text_lower]
            metrics["mode_anchors_found"] = len(found_anchors)
            if not found_anchors:
                penalty = 10
                score -= penalty
                violations.append(
                    f"AVERTISSEMENT MODE '{mode}': Aucun marqueur signature détecté parmi {signatures} (-{penalty} pts)."
                )

    score = max(0, min(100, score))
    metrics["final_score"] = score
    return score, violations, metrics


def safe_read_file(target: str) -> Optional[str]:
    """Lit un fichier de manière sécurisée en évitant les erreurs de chemin invalide sous Windows."""
    try:
        if os.path.isfile(target):
            with open(target, "r", encoding="utf-8") as f:
                return f.read()
    except (OSError, ValueError):
        pass
    return None


def main() -> None:
    parser = argparse.ArgumentParser(description="Deterministic Stylistic & Rhetorical Linter pour le style @brivael.")
    parser.add_argument("target", help="Chemin vers le fichier texte ou contenu brut du post")
    parser.add_argument(
        "--mode",
        choices=["investigation", "offensive", "sniper", "engine", "causal", "manifesto", "counterstrike", "reads_the_minds", "cognitive_lever"],
        help="Vérifier les signatures d'un pilier spécifique"
    )
    
    args = parser.parse_args()

    content = safe_read_file(args.target)
    if content is None:
        content = args.target

    score, violations, metrics = audit_post(content, mode=args.mode)

    print("\n" + "=" * 60)
    print(" 🎯 AUDIT RÉSULTATS — STYLE BRIVAEL LE POGAM (@brivael)")
    print("=" * 60)
    print(f"Score Global       : {score} / 100")
    print(f"Points d'excl.     : {metrics.get('exclamation_count')}")
    print(f"Paragraphes        : {metrics.get('paragraph_count')}")
    print(f"Phrases totales    : {metrics.get('sentence_count')}")
    print(f"Mots totaux        : {metrics.get('total_words')}")
    print(f"Ratio Staccato     : {metrics.get('staccato_ratio')}% (Seuil: >= 35%, Cible: >= 40%)")
    if args.mode:
        print(f"Ancres Mode '{args.mode}': {metrics.get('mode_anchors_found', 0)}")
    print("-" * 60)

    if violations:
        print("⚠️ ANOMALIES DÉTECTÉES :")
        for v in violations:
            print(f" - {v}")
    else:
        print("✅ AUCUNE ANOMALIE. Post 100% conforme au standard Brivael.")
    print("=" * 60 + "\n")

    sys.exit(0 if score >= 80 else 1)


if __name__ == "__main__":
    main()
