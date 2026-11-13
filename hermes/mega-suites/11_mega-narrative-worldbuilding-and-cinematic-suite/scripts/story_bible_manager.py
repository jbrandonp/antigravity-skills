"""Story Bible & Lore Manager for Obsidian & Claude Agent Projects.

Inspired by IPedrax/Storytelling, eeriea/agent-skills, and danjdewhurst/worldbuilding.
Provides deterministic CLI inspection, orphan detection, and Obsidian Dataview export for story bibles:
- Inspect factions, characters, locations, and magic systems
- Detect unregistered lore mentions in manuscripts (orphan references)
- Export automated Obsidian Dataview dashboards (_BIBLE_DASHBOARD.md)
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple


def parse_frontmatter(content: str) -> Tuple[Dict[str, Any], str]:
    """Parse YAML frontmatter without external dependencies."""
    pattern = r"^---\s*\n(.*?)\n---\s*\n(.*)$"
    match = re.match(pattern, content, re.DOTALL)
    if not match:
        return {}, content

    yaml_block = match.group(1)
    body = match.group(2)
    metadata: Dict[str, Any] = {}
    current_key = None

    for line in yaml_block.splitlines():
        trimmed = line.strip()
        if not trimmed or trimmed.startswith("#"):
            continue

        if (trimmed.startswith("- ") or line.startswith("  - ")) and current_key:
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
            else:
                metadata[key] = val.strip("'\"")
        else:
            current_key = None

    return metadata, body


class StoryBibleManager:
    def __init__(self, project_path: str):
        self.project_dir = Path(project_path)
        self.bible_dir = self.project_dir / "bible"
        self.entities: Dict[str, Dict[str, Any]] = {}

    def scan_bible(self) -> None:
        """Scan all markdown files in bible/."""
        if not self.bible_dir.exists():
            return

        for filepath in self.bible_dir.rglob("*.md"):
            content = filepath.read_text(encoding="utf-8", errors="replace")
            meta, body = parse_frontmatter(content)
            entity_id = meta.get("id") or filepath.stem.lower()
            category = filepath.parent.name

            # Extract outgoing wikilinks [[...]]
            wikilinks = re.findall(r"\[\[(.*?)\]\]", body)

            self.entities[entity_id] = {
                "id": entity_id,
                "name": meta.get("name", filepath.stem),
                "category": category,
                "file": str(filepath.relative_to(self.project_dir)),
                "metadata": meta,
                "outgoing_links": wikilinks,
                "body_snippet": body[:200].replace("\n", " ").strip(),
            }

    def find_orphan_mentions(self) -> List[Dict[str, Any]]:
        """Find entity wikilinks mentioned in manuscript that don't exist in bible/."""
        orphans = []
        known_ids = set(self.entities.keys())
        known_names = {e["name"].lower() for e in self.entities.values()}

        manuscript_dirs = [self.project_dir / "acts", self.project_dir / "chapters"]
        for m_dir in manuscript_dirs:
            if not m_dir.exists():
                continue
            for filepath in m_dir.rglob("*.md"):
                content = filepath.read_text(encoding="utf-8", errors="replace")
                wikilinks = re.findall(r"\[\[(.*?)\]\]", content)
                for link in wikilinks:
                    clean_link = link.lower().strip()
                    if clean_link not in known_ids and clean_link not in known_names:
                        orphans.append({
                            "unregistered_entity": link,
                            "file": filepath.name,
                            "path": str(filepath.relative_to(self.project_dir)),
                        })
        return orphans

    def generate_obsidian_dashboard(self) -> str:
        """Generate a complete Markdown Dataview dashboard for Obsidian."""
        lines = [
            "# 📖 Story Bible Master Dashboard (Obsidian Dataview)",
            "",
            "> Tableau de bord généré automatiquement par `story_bible_manager.py`.",
            "",
            "## 👥 Personnages Actifs",
            "```dataview",
            "TABLE role, want, need, flaw, alive",
            'FROM "bible/characters"',
            "SORT file.name ASC",
            "```",
            "",
            "## 🏛️ Factions & Alliances",
            "```dataview",
            "TABLE dominant_resource, threat_level, ideology, allies",
            'FROM "bible/world/factions"',
            "SORT threat_level DESC",
            "```",
            "",
            "## 📜 Registre des Entités Recensées",
            f"- **Nombre total d'entités répertoriées :** {len(self.entities)}",
        ]
        for e in self.entities.values():
            lines.append(f"- **[[{e['id']}]]** ({e['name']}) — *Catégorie : {e['category']}*")

        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Story Bible & Lore Manager for Obsidian")
    parser.add_argument("--project-dir", "-p", default=".", help="Path to story project root")
    parser.add_argument("--list", action="store_true", help="List all registered bible entities")
    parser.add_argument("--orphans", action="store_true", help="Detect unregistered wikilinks in manuscript")
    parser.add_argument("--export-dashboard", help="Export an Obsidian Dataview dashboard to specified path")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    args = parser.parse_args()

    manager = StoryBibleManager(args.project_dir)
    manager.scan_bible()

    if args.export_dashboard:
        content = manager.generate_obsidian_dashboard()
        Path(args.export_dashboard).write_text(content, encoding="utf-8")
        print(f"✅ Obsidian dashboard exported to: {args.export_dashboard}")
        sys.exit(0)

    if args.orphans:
        orphans = manager.find_orphan_mentions()
        if args.json:
            print(json.dumps(orphans, indent=2, ensure_ascii=False))
        else:
            print(f"\n🔍 UNREGISTERED WIKILINK MENTIONS ({len(orphans)} found):")
            for o in orphans:
                print(f"  - [[{o['unregistered_entity']}]] in {o['file']}")
        sys.exit(0)

    if args.json:
        print(json.dumps(manager.entities, indent=2, ensure_ascii=False))
    else:
        print(f"\n🏛️ STORY BIBLE ENTITIES ({len(manager.entities)} total):")
        for e_id, e in manager.entities.items():
            print(f"  [{e['category'].upper()}] {e['name']} (ID: {e_id}) -> {e['file']}")


if __name__ == "__main__":
    main()
