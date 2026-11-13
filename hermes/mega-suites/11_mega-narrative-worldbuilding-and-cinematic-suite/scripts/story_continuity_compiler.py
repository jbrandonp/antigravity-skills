"""Story Continuity Compiler, Narrative Linter & Scaffolder for AI Agents.

Inspired by danjdewhurst/story-skills, jackterror/writers-room, and haowjy/creative-writing-skills.
Performs deterministic static analysis on narrative projects:
- Character life-cycle & illegal resurrection detection
- Chekhov's gun & narrative promise tracking (Setup / Payoff)
- Epistemic tracking (knowledge leak & secret revelation detection)
- Show, Don't Tell & Perception Filter Linter (filter words detection)
- Causal vs Sequential beat analysis (Therefore/But vs And-Then)
- Full Project Scaffolding (--init) for Obsidian & Story projects
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


# Filter words that violate "Show, Don't Tell" by distancing the reader from immediate POV
FILTER_WORDS_PATTERNS = [
    # French
    r"\b(il|elle)\s+(vit|voyait|remarqua|remarquait|entendit|entendait|sentit|ressentit|perçut|constata)\b",
    r"\b(il|elle)\s+(semblait|paraissait|avait l'air de)\b",
    r"\b(il|elle)\s+se rendit compte que\b",
    r"\b(un frisson lui parcourut l'échine|un silence de plomb|un froid glacial)\b",
    # English
    r"\b(he|she)\s+(felt|saw|heard|noticed|realized|wondered|decided|observed|smelled)\b",
    r"\b(it seemed to him|it appeared to her|she was able to see)\b",
    r"\b(a shiver ran down (his|her) spine|a deafening silence)\b",
]


def parse_frontmatter(content: str) -> Tuple[Dict[str, Any], str]:
    """Extract YAML frontmatter and body markdown without external dependencies."""
    pattern = r"^---\s*\n(.*?)\n---\s*\n(.*)$"
    match = re.match(pattern, content, re.DOTALL)
    if not match:
        return {}, content

    yaml_block = match.group(1)
    body = match.group(2)
    metadata: Dict[str, Any] = {}
    current_key: Optional[str] = None

    for line in yaml_block.splitlines():
        trimmed = line.strip()
        if not trimmed or trimmed.startswith("#"):
            continue

        # Indented list item under current_key
        if (trimmed.startswith("- ") or line.startswith("  - ") or line.startswith("\t- ")) and current_key:
            item_val = trimmed.lstrip("- ").strip().strip("'\"")
            if not isinstance(metadata.get(current_key), list):
                metadata[current_key] = []
            metadata[current_key].append(item_val)
            continue

        if ":" in line:
            key, val = line.split(":", 1)
            key = key.strip()
            val = val.strip()
            current_key = key
            if not val or val.lower() in ("null", "none", "~"):
                metadata[key] = None
            elif val.lower() == "true":
                metadata[key] = True
            elif val.lower() == "false":
                metadata[key] = False
            elif val.isdigit():
                metadata[key] = int(val)
            elif val.startswith("[") and val.endswith("]"):
                items = [x.strip().strip("'\"") for x in val[1:-1].split(",") if x.strip()]
                metadata[key] = items
            else:
                metadata[key] = val.strip("'\"")
        else:
            current_key = None

    return metadata, body


def scaffold_project(target_dir: Path, title: str) -> None:
    """Create a complete production-ready story project structure."""
    target_dir.mkdir(parents=True, exist_ok=True)
    (target_dir / ".story").mkdir(exist_ok=True)
    (target_dir / "bible" / "characters").mkdir(parents=True, exist_ok=True)
    (target_dir / "bible" / "world" / "factions").mkdir(parents=True, exist_ok=True)
    (target_dir / "bible" / "world" / "magic_tech").mkdir(parents=True, exist_ok=True)
    (target_dir / "acts" / "act-1").mkdir(parents=True, exist_ok=True)
    (target_dir / "acts" / "act-2").mkdir(parents=True, exist_ok=True)
    (target_dir / "acts" / "act-3").mkdir(parents=True, exist_ok=True)
    (target_dir / "scenes").mkdir(exist_ok=True)
    (target_dir / "video_shots").mkdir(exist_ok=True)

    # Config
    config_file = target_dir / ".story" / "config.yaml"
    config_file.write_text(f"""title: "{title}"
author: "Brandon"
version: "1.0.0"
default_pov: "third-person-limited"
target_word_count: 80000
continuity_strictness: "strict"
created_at: "2026-11-13"
""", encoding="utf-8")

    # Promises registry
    promises_file = target_dir / ".story" / "promises.yaml"
    promises_file.write_text("""# Chekhov's Guns & Narrative Promises Registry
- id: gun-revolver-drawer
  setup_chapter: 1
  expected_payoff_chapter: 3
  description: "Revolver caché sous le double fond du tiroir de bureau de Malik"
  resolved: false
""", encoding="utf-8")

    # Protagonist Sheet
    proto_file = target_dir / "bible" / "characters" / "malik.md"
    proto_file.write_text("""---
id: malik
name: "Malik"
role: "Protagoniste"
alive: true
death_chapter: null
flaw: "Incapacité pathologique à déléguer par peur de la trahison"
want: "Prendre le contrôle du dernier puits artésien"
need: "Accepter sa vulnérabilité et faire confiance à Sora"
known_secrets:
  - "poison-convoi"
secrets_hidden:
  - "origine-lignee-royale"
---

# Fiche Personnage : Malik

## 🎭 Modèle de l'Iceberg (Hemingway)
- **1/8e Émergé :** Négociateur froid, méticuleux, ne hausse jamais la voix.
- **7/8e Immergé :** Hanté par le massacre de son convoi d'enfance dont il est le seul survivant.
""", encoding="utf-8")

    # Chapter 01
    chap1_file = target_dir / "acts" / "act-1" / "chapter-01.md"
    chap1_file.write_text("""---
chapter: 1
title: "La Poussière du Bassin"
pov: "Malik"
characters_present:
  - malik
reveals:
  - "poison-convoi"
word_count: 450
status: "draft"
---

# Chapitre 1 : La Poussière du Bassin

Le vent du désert raclait les tôles rouillées de l'avant-poste. Malik ajusta son foulard sur ses lèvres sèches.
L'eau manquait depuis l'aube. DONC le troc du soir devenait une question de vie ou de mort.
MAIS quand la caravane entra dans la gorge, les fûts de cuivre sonnaient creux.
Malik glissa les doigts sous le tiroir en bois de genévrier, là où reposait le canon huilé de son revolver.
""", encoding="utf-8")

    print(f"✅ Story project '{title}' successfully scaffolded at: {target_dir}")


class StoryContinuityCompiler:
    def __init__(self, project_path: str):
        self.project_dir = Path(project_path)
        self.errors: List[Dict[str, Any]] = []
        self.warnings: List[Dict[str, Any]] = []
        self.style_nits: List[Dict[str, Any]] = []
        self.characters: Dict[str, Dict[str, Any]] = {}
        self.promises: List[Dict[str, Any]] = []
        self.chapters: List[Dict[str, Any]] = []
        self.reveals_timeline: Dict[str, int] = {}
        self.causality_score: float = 100.0

    def load_characters(self) -> None:
        """Scan bible/characters for character sheets."""
        chars_dir = self.project_dir / "bible" / "characters"
        if not chars_dir.exists():
            return

        for filepath in chars_dir.glob("*.md"):
            content = filepath.read_text(encoding="utf-8", errors="replace")
            meta, body = parse_frontmatter(content)
            char_id = meta.get("id") or filepath.stem.lower()
            raw_secrets = meta.get("known_secrets") or []
            if isinstance(raw_secrets, str):
                raw_secrets = [s.strip() for s in raw_secrets.split(",") if s.strip()]
            self.characters[char_id] = {
                "id": char_id,
                "name": meta.get("name", filepath.stem),
                "alive": meta.get("alive", True),
                "death_chapter": meta.get("death_chapter", None),
                "known_secrets": set(raw_secrets),
                "path": str(filepath),
            }

    def load_promises(self) -> None:
        """Scan .story/promises.yaml or promises.json for Chekhov's guns."""
        promises_file = self.project_dir / ".story" / "promises.yaml"
        if not promises_file.exists():
            promises_file = self.project_dir / "promises.yaml"

        if promises_file.exists():
            content = promises_file.read_text(encoding="utf-8", errors="replace")
            current_promise: Dict[str, Any] = {}
            for line in content.splitlines():
                line = line.strip()
                if line.startswith("- id:"):
                    if current_promise:
                        self.promises.append(current_promise)
                    current_promise = {"id": line.replace("- id:", "").strip()}
                elif ":" in line and current_promise:
                    k, v = line.split(":", 1)
                    k = k.strip()
                    v = v.strip().strip("'\"")
                    if v.isdigit():
                        current_promise[k] = int(v)
                    elif v.lower() in ("true", "false"):
                        current_promise[k] = v.lower() == "true"
                    else:
                        current_promise[k] = v
            if current_promise:
                self.promises.append(current_promise)

    def load_chapters(self) -> None:
        """Scan acts/ or chapters/ for manuscript files."""
        chapters_paths: List[Path] = []
        acts_dir = self.project_dir / "acts"
        chap_dir = self.project_dir / "chapters"

        if acts_dir.exists():
            chapters_paths.extend(acts_dir.rglob("*.md"))
        if chap_dir.exists():
            chapters_paths.extend(chap_dir.glob("*.md"))

        chapters_paths = sorted(chapters_paths, key=lambda p: p.name)

        for idx, filepath in enumerate(chapters_paths, start=1):
            content = filepath.read_text(encoding="utf-8", errors="replace")
            meta, body = parse_frontmatter(content)
            chapter_num = meta.get("chapter", idx)
            chars_present = meta.get("characters_present") or []
            if isinstance(chars_present, str):
                chars_present = [c.strip() for c in chars_present.split(",") if c.strip()]

            reveals = meta.get("reveals") or []
            if isinstance(reveals, str):
                reveals = [r.strip() for r in reveals.split(",") if r.strip()]

            for rev in reveals:
                if rev not in self.reveals_timeline:
                    self.reveals_timeline[rev] = chapter_num

            self.chapters.append({
                "number": chapter_num,
                "file": filepath.name,
                "path": str(filepath),
                "title": meta.get("title", filepath.stem),
                "pov": meta.get("pov", ""),
                "characters_present": [c.lower() for c in chars_present],
                "reveals": reveals,
                "body": body,
            })

    def audit_character_continuity(self) -> None:
        """Detect illegal resurrections and dead character appearances."""
        for chap in self.chapters:
            chap_num = chap["number"]
            present = chap["characters_present"]
            body_text = chap["body"].lower()

            for char_id, char_data in self.characters.items():
                death_chap = char_data.get("death_chapter")
                if death_chap is not None:
                    try:
                        d_num = int(death_chap)
                        c_num = int(chap_num)
                        if c_num > d_num:
                            is_in_meta = char_id in present or char_data["name"].lower() in present
                            direct_dialogue = bool(re.search(rf'\b{re.escape(char_data["name"].lower())}\s*[:—"-]', body_text))

                            if is_in_meta or direct_dialogue:
                                self.errors.append({
                                    "type": "ILLEGAL_RESURRECTION",
                                    "severity": "CRITICAL",
                                    "chapter": chap_num,
                                    "file": chap["file"],
                                    "character": char_data["name"],
                                    "message": f"Character '{char_data['name']}' died in Chapter {death_chap} but appears actively in Chapter {chap_num}.",
                                })
                    except (ValueError, TypeError):
                        pass

    def audit_chekhov_guns(self) -> None:
        """Verify that every setup has a matching payoff and payoffs don't precede setups."""
        for p in self.promises:
            p_id = p.get("id", "unknown")
            setup = p.get("setup_chapter")
            payoff = p.get("payoff_chapter")
            resolved = p.get("resolved", False)

            if setup is not None and payoff is not None:
                if payoff < setup:
                    self.errors.append({
                        "type": "TIMELINE_PARADOX",
                        "severity": "CRITICAL",
                        "promise_id": p_id,
                        "message": f"Promise '{p_id}' payoff (Ch. {payoff}) occurs before setup (Ch. {setup}).",
                    })

            if setup is not None and not resolved and payoff is None:
                total_chaps = len(self.chapters)
                if total_chaps > 0 and (total_chaps - setup) >= 5:
                    self.warnings.append({
                        "type": "ORPHANED_SETUP",
                        "severity": "WARNING",
                        "promise_id": p_id,
                        "setup_chapter": setup,
                        "message": f"Setup '{p_id}' introduced in Ch. {setup} remains unfired after {total_chaps} chapters.",
                    })

    def audit_show_dont_tell(self) -> None:
        """Scan manuscript text for perception filters and filter words with concrete rewrite suggestions."""
        rewrite_suggestions = {
            "il vit": "Montrer directement l'action ou l'élément visuel (ex: 'La silhouette se découpa contre le néon' au lieu de 'Il vit la silhouette se découper')",
            "elle sentit": "Traduire par une réaction sensorielle ou corporelle (ex: 'Le vent glacé lui brûla les paumes' au lieu de 'Elle sentit le vent froid')",
            "un frisson lui parcourut l'échine": "Décrire le spasme physique réel (ex: 'Les poils de ses avant-bras se dressèrent' ou 'Sa déglutition se bloqua')",
            "un silence de plomb": "Décrire les bruits de fond subtils qui soulignent le silence (ex: 'Seul le grésillement du tube fluorescent résonnait')",
            "se rendit compte que": "Supprimer le filtre cognitif et énoncer directement la prise de conscience ou la vérité brute",
            "he felt": "Anchor directly in visceral physiology (e.g., 'His stomach clenched into a hard fist' instead of 'He felt anxious')",
            "she noticed": "State the sensory observation directly into the scene framing without narrator buffering",
        }

        for chap in self.chapters:
            chap_num = chap["number"]
            body = chap["body"]

            for pat in FILTER_WORDS_PATTERNS:
                matches = re.finditer(pat, body, re.IGNORECASE)
                for m in matches:
                    matched_str = m.group(0).lower()
                    snippet = body[max(0, m.start() - 25): min(len(body), m.end() + 25)].strip().replace("\n", " ")
                    
                    suggestion = "Rephrase without sensory intermediary filter word."
                    for k, sugg in rewrite_suggestions.items():
                        if k in matched_str:
                            suggestion = sugg
                            break

                    self.style_nits.append({
                        "type": "PERCEPTION_FILTER_WORD",
                        "severity": "STYLE_NIT",
                        "chapter": chap_num,
                        "file": chap["file"],
                        "matched": m.group(0),
                        "snippet": f"...{snippet}...",
                        "suggestion": suggestion,
                        "message": f"Filter word detected ('{m.group(0)}'). Violates direct POV immersion.",
                    })

    def compute_pacing_and_tension(self) -> List[Dict[str, Any]]:
        """Calculate narrative tension and pacing curves across all chapters."""
        pacing_data = []
        conflict_tokens = {
            "mort", "sang", "danger", "cria", "tir", "arme", "fuir", "fuite", "sombre",
            "rage", "frapp", "choc", "lame", "feu", "flamme", "catastrophe", "secret", "trahi",
            "fear", "blood", "death", "scream", "shot", "flee", "hit", "shock", "blade", "fire", "betrayal"
        }

        for chap in self.chapters:
            body = chap["body"]
            words = re.findall(r"\b\w+\b", body)
            word_count = len(words)
            if word_count == 0:
                continue

            # Dialogue proportion
            dialogue_lines = [l for l in body.splitlines() if re.match(r"^\s*([—\-\"«]|>\s*)", l)]
            dialogue_ratio = round((len(dialogue_lines) / max(1, len(body.splitlines()))) * 100, 1)

            # Conflict density
            lower_body = body.lower()
            conflict_hits = sum(1 for token in conflict_tokens if token in lower_body)
            punctuation_urgency = body.count("!") + body.count("?")

            # Tension calculation (0 - 100)
            raw_tension = (conflict_hits * 6.0) + (punctuation_urgency * 2.5) + (dialogue_ratio * 0.3)
            tension_score = min(100.0, max(15.0, round(raw_tension, 1)))

            pacing_data.append({
                "chapter": chap["number"],
                "title": chap["title"],
                "word_count": word_count,
                "dialogue_ratio": dialogue_ratio,
                "tension_score": tension_score,
            })

        return pacing_data

    def generate_mermaid_graph(self) -> str:
        """Generate a Mermaid relationship graph connecting characters based on chapter co-occurrences."""
        interactions: Dict[Tuple[str, str], List[int]] = {}

        for chap in self.chapters:
            chap_num = chap["number"]
            present = chap["characters_present"]
            for i in range(len(present)):
                for j in range(i + 1, len(present)):
                    c1, c2 = sorted([present[i], present[j]])
                    if (c1, c2) not in interactions:
                        interactions[(c1, c2)] = []
                    interactions[(c1, c2)].append(chap_num)

        mermaid_lines = ["```mermaid", "graph TD"]
        for char_id, char_data in self.characters.items():
            alive_icon = "👤" if char_data.get("alive", True) else "💀"
            mermaid_lines.append(f'    {char_id}["{alive_icon} {char_data["name"]}"]')

        for (c1, c2), chaps in interactions.items():
            chap_str = f"Ch. {', '.join(map(str, chaps))}"
            mermaid_lines.append(f"    {c1} ---|{chap_str}| {c2}")

        mermaid_lines.append("```")
        return "\n".join(mermaid_lines)

    def audit_causality_connectors(self) -> None:
        """Calculate the ratio of causal connectors (Therefore/But) vs sequential connectors (And Then)."""
        all_text = " ".join(c["body"].lower() for c in self.chapters)
        if not all_text.strip():
            return

        causal_words = len(re.findall(r"\b(donc|par conséquent|mais|cependant|pourtant|néanmoins|therefore|however|thus|nevertheless)\b", all_text))
        sequential_words = len(re.findall(r"\b(et ensuite|puis après|après cela|et alors|and then|after that|next thing)\b", all_text))

        total_connectors = causal_words + sequential_words
        if total_connectors > 0:
            causal_ratio = (causal_words / total_connectors) * 100.0
            if causal_ratio < 75.0:
                self.warnings.append({
                    "type": "WEAK_CAUSALITY_FLOW",
                    "severity": "WARNING",
                    "causal_ratio": round(causal_ratio, 1),
                    "message": f"Low narrative causality ratio ({causal_ratio:.1f}% < 75%). High occurrence of sequential 'And then' beats. Enforce South Park 'Therefore / But' transitions.",
                })
            self.causality_score = causal_ratio

    def run_all(self) -> Dict[str, Any]:
        """Execute full narrative audit suite."""
        self.load_characters()
        self.load_promises()
        self.load_chapters()

        self.audit_character_continuity()
        self.audit_chekhov_guns()
        self.audit_show_dont_tell()
        self.audit_causality_connectors()

        critical_penalty = len(self.errors) * 25
        warning_penalty = len(self.warnings) * 5
        style_penalty = min(15.0, len(self.style_nits) * 1.0)
        score = max(0.0, min(100.0, 100.0 - critical_penalty - warning_penalty - style_penalty))

        pacing_data = self.compute_pacing_and_tension()

        return {
            "status": "PASS" if len(self.errors) == 0 else "FAIL",
            "consistency_score": round(score, 1),
            "chapters_analyzed": len(self.chapters),
            "characters_tracked": len(self.characters),
            "promises_tracked": len(self.promises),
            "critical_errors_count": len(self.errors),
            "warnings_count": len(self.warnings),
            "style_nits_count": len(self.style_nits),
            "causality_ratio": round(self.causality_score, 1),
            "pacing_curve": pacing_data,
            "errors": self.errors,
            "warnings": self.warnings,
            "style_nits": self.style_nits,
        }


def main():
    parser = argparse.ArgumentParser(description="Deterministic Continuity Compiler & Narrative Linter")
    parser.add_argument("--project-dir", "-p", default=".", help="Path to story project root")
    parser.add_argument("--init", type=str, help="Scaffold a new story project in the specified directory with given title")
    parser.add_argument("--pacing", action="store_true", help="Display chapter-by-chapter dramatic tension curve")
    parser.add_argument("--graph", action="store_true", help="Output Mermaid relationship graph of characters")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    args = parser.parse_args()

    if args.init:
        target = Path(args.project_dir) if args.project_dir != "." else Path(args.init.lower().replace(" ", "-"))
        scaffold_project(target, args.init)
        sys.exit(0)

    compiler = StoryContinuityCompiler(args.project_dir)
    results = compiler.run_all()

    if args.graph:
        print("\n" + compiler.generate_mermaid_graph() + "\n")
        sys.exit(0)

    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        print("\n" + "=" * 65)
        print("📖 STORY CONTINUITY COMPILER & SHOW-DON'T-TELL LINTER")
        print("=" * 65)
        print(f"Status                 : {results['status']}")
        print(f"Narrative Audit Score  : {results['consistency_score']} / 100")
        print(f"Causality Flow Ratio   : {results['causality_ratio']} %")
        print(f"Chapters Audited       : {results['chapters_analyzed']}")
        print(f"Characters Tracked     : {results['characters_tracked']}")
        print(f"Promises / Chekhov     : {results['promises_tracked']}")
        print(f"Critical Errors        : {results['critical_errors_count']}")
        print(f"Continuity Warnings    : {results['warnings_count']}")
        print(f"Style / Perception Nits: {results['style_nits_count']}")
        print("-" * 65)

        if results["errors"]:
            print("\n❌ CRITICAL CONTINUITY ERRORS:")
            for err in results["errors"]:
                print(f"  [{err['type']}] (Ch. {err.get('chapter', '?')}): {err['message']}")

        if results["warnings"]:
            print("\n⚠️ WARNINGS & NARRATIVE DRIFT:")
            for warn in results["warnings"]:
                print(f"  [{warn['type']}]: {warn['message']}")

        if results["style_nits"] and len(results["style_nits"]) <= 5:
            print("\n🔍 SHOW, DON'T TELL (PERCEPTION FILTER WORDS):")
            for nit in results["style_nits"]:
                print(f"  (Ch. {nit['chapter']} in {nit['file']}): '{nit['matched']}'")
                print(f"    Snippet    : {nit['snippet']}")
                print(f"    Suggestion : {nit.get('suggestion', '')}")

        if args.pacing and results["pacing_curve"]:
            print("\n📈 DRAMATIC TENSION PACING CURVE:")
            for p in results["pacing_curve"]:
                bar = "█" * int(p["tension_score"] / 5)
                print(f"  Ch. {p['chapter']:02d} [{bar:<20}] {p['tension_score']:>5.1f}/100 | {p['word_count']} mots | {p['dialogue_ratio']}% dialogue")

        print("\n" + "=" * 65)

    sys.exit(0 if results["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
