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
import csv
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
    (r"témoigne\s+de|un\s+rappel\s+cuisant|ouvre\s+la\s+voie\s+à", "Cliché d'emphase dramatique (FR)"),
    (r"serves\s+as\s+a\s+testament|a\s+stark\s+reminder|paves\s+the\s+way\s+for", "Inflated significance cliché (EN)"),
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

    bold_bullet_count = len(re.findall(r"^\s*(?:[-*•]|\d+[\.\)])?\s*\*\*[^*\n]+?[:\s]*\*\*\s*[:—–-]?", clean_draft, re.MULTILINE))
    if bold_bullet_count >= 3:
        violations.append(f"[MAJOR] Found {bold_bullet_count} bold label bullet prefixes. Unnatural AI formatting pattern.")
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

    if re.search(r"https?://\S+", clean_draft):
        violations.append("[WARN] External link detected in post body (-40% to -60% reach penalty). Place URLs in 1st comment.")
        penalties += 10

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


def audit_dm(text: str) -> Dict[str, object]:
    """Audits a LinkedIn connection invite note or direct outreach message."""
    clean_draft, clean_actions = clean_text(text)
    total_chars = len(clean_draft)
    violations: List[str] = []
    penalties: int = 0

    if total_chars > 200:
        violations.append(
            f"[CRITICAL] Connection invite note is {total_chars} chars (limit is 200). Truncated on mobile."
        )
        penalties += 40
    elif total_chars == 0:
        violations.append("[CRITICAL] Empty message.")
        penalties += 50
    elif total_chars < 40:
        violations.append("[WARN] Message is very brief (< 40 chars). Missing contextual hook.")
        penalties += 10

    text_lower = clean_draft.lower()
    pitch_keywords = [
        "jump on a call",
        "quick 15-minute",
        "15 min call",
        "demo",
        "partnership opportunity",
        "discuter 15 minutes",
        "prendre un café virtuel",
        "présenter nos services",
        "votre calendrier",
    ]
    for kw in pitch_keywords:
        if kw in text_lower:
            violations.append(f"[MAJOR] Cold pitch detected in invite note: '{kw}'. Never pitch in connection requests.")
            penalties += 25

    if "!" in clean_draft:
        violations.append("[WARN] Exclamation mark detected. Keep tone understated and peer-to-peer.")
        penalties += 10

    final_score = max(0, 100 - penalties)
    verdict = "PASS" if final_score >= 80 and not any("[CRITICAL]" in v for v in violations) else "FAIL"

    return {
        "score": final_score,
        "verdict": verdict,
        "total_chars": total_chars,
        "clean_actions": clean_actions,
        "violations": violations,
        "clean_text": clean_draft,
    }


def audit_poll(text: str) -> Dict[str, object]:
    """Audits a LinkedIn Poll question and choice options against 2026 limits."""
    clean_draft, clean_actions = clean_text(text)
    violations: List[str] = []
    penalties: int = 0

    lines = [line.strip() for line in clean_draft.split("\n") if line.strip()]
    if not lines:
        return {
            "score": 0,
            "verdict": "FAIL",
            "clean_actions": clean_actions,
            "violations": ["[CRITICAL] Empty poll text."],
            "clean_text": clean_draft,
        }

    question = lines[0]
    options: List[str] = []
    for line in lines[1:]:
        opt_match = re.match(r"^(?:[-*•]|\d+[\.\)])\s*(.+)$", line)
        if opt_match:
            options.append(opt_match.group(1).strip())

    q_len = len(question)
    if q_len > 140:
        violations.append(f"[CRITICAL] Poll question is {q_len} chars (maximum limit is 140 chars).")
        penalties += 35
    elif q_len < 15:
        violations.append("[WARN] Poll question is very short (< 15 chars).")
        penalties += 10

    if len(options) < 2:
        violations.append("[CRITICAL] Less than 2 poll options detected (LinkedIn requires 2 to 4 options).")
        penalties += 30
    elif len(options) > 4:
        violations.append(f"[CRITICAL] Found {len(options)} options (LinkedIn allows maximum 4 options).")
        penalties += 30

    for idx, opt in enumerate(options, start=1):
        if len(opt) > 30:
            violations.append(
                f"[CRITICAL] Option {idx} ('{opt[:20]}...') is {len(opt)} chars (hard limit: 30 chars)."
            )
            penalties += 25

    final_score = max(0, 100 - penalties)
    verdict = "PASS" if final_score >= 80 and not any("[CRITICAL]" in v for v in violations) else "FAIL"

    return {
        "score": final_score,
        "verdict": verdict,
        "question": question,
        "question_chars": q_len,
        "options_count": len(options),
        "options": options,
        "clean_actions": clean_actions,
        "violations": violations,
        "clean_text": clean_draft,
    }


def audit_thread(text: str) -> Dict[str, object]:
    """Audits an X thread converted from a LinkedIn publication (280-char limit per post)."""
    clean_draft, clean_actions = clean_text(text)
    violations: List[str] = []
    penalties: int = 0

    raw_tweets = [t.strip() for t in re.split(r"\n\s*---\s*\n|\n\s*\d+[/.)]\s*", clean_draft) if t.strip()]
    if not raw_tweets:
        raw_tweets = [clean_draft.strip()]

    tweet_details: List[Dict[str, object]] = []
    for idx, tweet in enumerate(raw_tweets, start=1):
        t_len = len(tweet)
        t_words = len(re.findall(r"\b[\w'-]+\b", tweet))
        tweet_details.append({"index": idx, "chars": t_len, "words": t_words})
        if t_len > 280:
            violations.append(f"[CRITICAL] Tweet #{idx} is {t_len} chars (maximum limit on X is 280 chars).")
            penalties += 30
        elif t_len == 0:
            violations.append(f"[WARN] Tweet #{idx} is empty.")
            penalties += 10

    if 1 < len(raw_tweets) < 3:
        violations.append("[WARN] Thread has only 2 tweets. Minimum 3 to 5 tweets recommended for traction.")
        penalties += 10

    final_score = max(0, 100 - penalties)
    verdict = "PASS" if final_score >= 80 and not any("[CRITICAL]" in v for v in violations) else "FAIL"

    return {
        "score": final_score,
        "verdict": verdict,
        "tweets_count": len(raw_tweets),
        "tweets": tweet_details,
        "clean_actions": clean_actions,
        "violations": violations,
        "clean_text": clean_draft,
    }


def to_unicode_char(c: str, style: str = "bold") -> str:
    """Converts a single alphanumeric character to styled mathematical Unicode."""
    if style == "bold":
        if "A" <= c <= "Z":
            return chr(0x1D5D4 + ord(c) - ord("A"))
        if "a" <= c <= "z":
            return chr(0x1D5EE + ord(c) - ord("a"))
        if "0" <= c <= "9":
            return chr(0x1D7EC + ord(c) - ord("0"))
    elif style == "italic":
        if "A" <= c <= "Z":
            return chr(0x1D608 + ord(c) - ord("A"))
        if "a" <= c <= "z":
            return chr(0x1D622 + ord(c) - ord("a"))
    elif style == "mono":
        if "A" <= c <= "Z":
            return chr(0x1D670 + ord(c) - ord("A"))
        if "a" <= c <= "z":
            return chr(0x1D68A + ord(c) - ord("a"))
        if "0" <= c <= "9":
            return chr(0x1D7F6 + ord(c) - ord("0"))
    return c


def to_unicode_text(text: str, style: str = "bold") -> str:
    """Converts an entire text string to styled mathematical Unicode."""
    return "".join(to_unicode_char(c, style) for c in text)


def format_to_unicode(text: str, default_style: str = "bold") -> str:
    """Parses markdown syntax (**bold**, *italic*, `code`) into Unicode characters, or converts the whole text."""
    has_markdown = bool(re.search(r"\*\*.+?\*\*|\*[^*]+?\*|`[^`]+?`", text))
    if has_markdown:
        res = re.sub(r"\*\*(.+?)\*\*", lambda m: to_unicode_text(m.group(1), "bold"), text)
        res = re.sub(r"\*([^*]+?)\*", lambda m: to_unicode_text(m.group(1), "italic"), res)
        res = re.sub(r"`([^`]+?)`", lambda m: to_unicode_text(m.group(1), "mono"), res)
        return res
    return to_unicode_text(text, default_style)


PROFILE_RUBRIC_ITEMS: List[Tuple[str, int, str]] = [
    ("headline", 12, "States who you help & outcome; carries proof; under 220c; front-loaded before 65c."),
    ("about_open", 10, "First 2 lines visible before 'see more' name reader's problem. No 'passionate about'."),
    ("about_body", 10, "Addressed to 1 person in 2nd person: problem, mechanism, 1 number proof, clear CTA (<1,400c)."),
    ("featured", 8, "Top 3 assets: highest-performing post, verified case study asset, booking/contact link."),
    ("banner", 6, "1 clear line of positioning + 1 way to reach you. No generic gradient or stock skyline."),
    ("photo", 6, "Face occupies ~60% of frame, eyes visible, recent professional high-contrast headshot."),
    ("current_role", 10, "1 line of scope + 2-3 quantified outcome bullets with numbers. Outcomes over duties."),
    ("experience_depth", 8, "Last 2 roles detailed with hard metrics. Everything > 10 years old compressed to 1 line."),
    ("skills", 6, "Top 3 endorsed skills match the exact core service you sell. The other 47 are noise."),
    ("recommendations", 8, "At least 3 received in the last 2 years, naming specific outcomes rather than character."),
    ("activity", 10, "Posted or commented thoughtfully in the last 7 days. Demonstrates an active presence."),
    ("contact", 6, "Custom URL, verified email or booking link in contact info, consistent handle across platforms."),
]


def print_profile_rubric() -> None:
    """Displays the structured 100-point LinkedIn Profile Optimization Rubric."""
    print("==================================================================")
    print("      LINKEDIN PROFILE OPTIMIZATION RUBRIC (100 POINTS)          ")
    print("==================================================================")
    total_pts = sum(pts for _, pts, _ in PROFILE_RUBRIC_ITEMS)
    for section, pts, check in PROFILE_RUBRIC_ITEMS:
        print(f"[{pts:2d} pts] {section:<17} : {check}")
    print("------------------------------------------------------------------")
    print(f"Total Target Score: {total_pts}/100 (Passing Threshold: >= 85/100)")
    print("==================================================================")


def audit_csv(csv_path: str) -> int:
    """Audits a LinkedIn Content Analytics CSV export and categorizes posts into 4 diagnostic quadrants."""
    try:
        with open(csv_path, "r", encoding="utf-8-sig", errors="ignore") as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading CSV file '{csv_path}': {e}", file=sys.stderr)
        return 1

    delimiter = ";" if ";" in content.split("\n")[0] else ","
    reader = csv.DictReader(content.splitlines(), delimiter=delimiter)
    raw_rows = list(reader)

    if not raw_rows:
        print("[CRITICAL] Empty CSV file or missing headers.", file=sys.stderr)
        return 1

    posts: List[Dict[str, object]] = []
    for r in raw_rows:
        title = ""
        for k in r:
            if any(w in k.lower() for w in ["title", "text", "description", "content", "post"]):
                title = r[k].strip()
                break

        def parse_num(keys: List[str]) -> float:
            for k in r:
                if any(w in k.lower() for w in keys):
                    val = r[k].replace("%", "").replace(",", ".").replace(" ", "").strip()
                    try:
                        return float(val)
                    except ValueError:
                        continue
            return 0.0

        impr = parse_num(["impression", "view"])
        react = parse_num(["reaction", "like"])
        comm = parse_num(["comment"])
        repost = parse_num(["repost", "share"])
        eng_rate = parse_num(["engagement"])

        if eng_rate == 0.0 and impr > 0:
            eng_rate = ((react + comm + repost) / impr) * 100
        elif 0.0 < eng_rate <= 1.0:
            eng_rate = eng_rate * 100

        if impr > 0 or react > 0 or comm > 0:
            posts.append({
                "title": title or "Post sans titre",
                "impressions": impr,
                "reactions": react,
                "comments": comm,
                "reposts": repost,
                "eng_rate": round(eng_rate, 2),
                "hook_len": len(title.split("\n\n")[0]) if title else 0,
            })

    if not posts:
        print("[CRITICAL] No valid post metric rows found in CSV.", file=sys.stderr)
        return 1

    total_posts = len(posts)
    total_impr = sum(p["impressions"] for p in posts)  # type: ignore[misc]
    avg_eng = sum(p["eng_rate"] for p in posts) / total_posts  # type: ignore[misc]
    impr_values = sorted([p["impressions"] for p in posts])  # type: ignore[misc]
    median_impr = impr_values[total_posts // 2]

    q1_outliers: List[Dict[str, object]] = []
    q2_reach: List[Dict[str, object]] = []
    q3_niche: List[Dict[str, object]] = []
    q4_flops: List[Dict[str, object]] = []

    for p in posts:
        er = p["eng_rate"]  # type: ignore[operator]
        imp = p["impressions"]  # type: ignore[operator]
        if er >= avg_eng and imp >= median_impr:
            q1_outliers.append(p)
        elif er < avg_eng and imp >= median_impr:
            q2_reach.append(p)
        elif er >= avg_eng and imp < median_impr:
            q3_niche.append(p)
        else:
            q4_flops.append(p)

    q1_outliers.sort(key=lambda x: x["eng_rate"], reverse=True)  # type: ignore[arg-type,return-value]
    q4_flops.sort(key=lambda x: x["eng_rate"])  # type: ignore[arg-type,return-value]

    avg_hook_q1 = (
        sum(p["hook_len"] for p in q1_outliers) / len(q1_outliers)  # type: ignore[misc]
        if q1_outliers
        else 0
    )
    avg_hook_q4 = (
        sum(p["hook_len"] for p in q4_flops) / len(q4_flops)  # type: ignore[misc]
        if q4_flops
        else 0
    )

    print("==================================================================")
    print("      LINKEDIN CONTENT ANALYTICS AUDIT — FORENSIC REPORT          ")
    print("==================================================================")
    print(f"Publications Analysées :   {total_posts}")
    print(f"Impressions Cumulées :     {int(total_impr):,}".replace(",", " "))
    print(f"Taux d'Engagement Moyen :  {avg_eng:.2f} %")
    print(f"Médiane d'Impressions :    {int(median_impr):,}".replace(",", " "))
    print("------------------------------------------------------------------")
    print(f"⭐ QUADRANT 1 (Outliers & Vainqueurs) :  {len(q1_outliers)} posts")
    if q1_outliers:
        top_p = q1_outliers[0]
        print(f"   Top Post: \"{top_p['title'][:55]}...\"")
        print(f"   Metrics:  {top_p['impressions']} impr, {top_p['eng_rate']}% engagement, {top_p['comments']} comm")
    print(f"📈 QUADRANT 2 (Portée Algorithmique) :   {len(q2_reach)} posts")
    print(f"💎 QUADRANT 3 (Pépites de Niche B2B) :   {len(q3_niche)} posts")
    print(f"📉 QUADRANT 4 (Flops & Sous-Performances): {len(q4_flops)} posts")
    print("------------------------------------------------------------------")
    print("MÉTRIQUES DE HOOK COMPARATIVES :")
    print(f"• Longueur moyenne d'accroche (Gagnants) : {int(avg_hook_q1)} caractères")
    print(f"• Longueur moyenne d'accroche (Flops)    : {int(avg_hook_q4)} caractères")
    print("------------------------------------------------------------------")
    print("RECOMMANDATIONS TACTIQUES :")
    print("1. Recycler les posts du Quadrant 1 en carrousels PDF 1080x1350 (Mode 4).")
    print("2. Rester attentif aux Quadrant 3 : fort engagement malgré faible portée = acheteurs qualifiés.")
    print("3. Pour le Quadrant 4, couper l'accroche avant 210 caractères et bannir les liens dans le corps.")
    print("==================================================================")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Unified LinkedIn Ghostwriting Quality & Anti-Slop Audit Engine.")
    parser.add_argument("file", nargs="?", help="Path to text file containing the draft")
    parser.add_argument("--text", help="Direct text of the draft to audit")
    parser.add_argument("--clean", action="store_true", help="Output automatically cleaned text directly")
    parser.add_argument(
        "--type",
        choices=["post", "dm", "poll", "thread"],
        default="post",
        help="Type of content to audit (default: post)",
    )
    parser.add_argument(
        "--to-unicode",
        choices=["bold", "italic", "mono"],
        help="Convert markdown formatting or text into styled Unicode characters",
    )
    parser.add_argument(
        "--rubric-profile",
        action="store_true",
        help="Display the 100-point LinkedIn Profile Optimization Rubric",
    )
    parser.add_argument(
        "--csv-audit",
        help="Path to LinkedIn Content Analytics CSV export to generate an executive diagnostic report",
    )
    args = parser.parse_args()

    if args.csv_audit:
        return audit_csv(args.csv_audit)

    if args.rubric_profile:
        print_profile_rubric()
        return 0

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

    if args.to_unicode:
        converted = format_to_unicode(content, args.to_unicode)
        print(converted)
        return 0

    if args.type == "dm":
        result = audit_dm(content)
    elif args.type == "poll":
        result = audit_poll(content)
    elif args.type == "thread":
        result = audit_thread(content)
    else:
        result = audit_post(content)

    if args.clean:
        print(result["clean_text"])
        return 0

    print("==================================================================")
    print(f"      MEGA LINKEDIN GHOSTWRITER — {args.type.upper()} QUALITY & ANTI-SLOP     ")
    print("==================================================================")
    print(f"Verdict:              {result['verdict']}")
    print(f"Score d'Authenticité: {result['score']}/100")
    if "total_chars" in result:
        print(f"Longueur Totale:      {result['total_chars']} caractères")
    if "hook_chars" in result:
        print(f"Longueur du Hook:     {result['hook_chars']} caractères (Cible mobile: 140 à 210)")
    if "sentence_count" in result:
        print(f"Phrases & Rythme:     {result['sentence_count']} phrases, moyenne {result['avg_words_per_sentence']} mots/phrase")
        print(f"Indice de Burstiness: {result['burstiness_std_dev']} (Variance de cadence, cible: >= 3.5)")
    if "question_chars" in result:
        print(f"Question du Sondage:  {result['question_chars']} caractères (Limite: 140)")
        print(f"Nombre d'Options:     {result['options_count']} (Limite: 2 à 4, <= 30 chars)")
    if "tweets_count" in result:
        print(f"Nombre de Tweets:     {result['tweets_count']} (Chaque tweet <= 280 chars)")
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
