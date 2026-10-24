#!/usr/bin/env python3
"""Character Pack Scaffolder & Manifest Generator.

Initializes the standardized SOTA 3D character package directory structure,
generates the modular parts inventory catalog, and scaffolds manifest.json
for tracking generation provenance, verification scores, and 3D engine routing.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
from typing import Sequence


def scaffold_pack(
    pack_dir: Path,
    character_name: str = "hero_character",
    art_style: str = "stylized_fantasy",
    target_engine: str = "Unreal_Engine_5",
    accessories: list[str] | None = None,
) -> dict:
    """Scaffolds character_pack directory and metadata."""
    accessories = accessories or ["weapon_sword", "shield", "pauldrons"]

    # 1. Create directory hierarchy
    subdirs = [
        pack_dir / "00_sheet",
        pack_dir / "01_parts",
        pack_dir / "02_multiview",
        pack_dir / "03_360",
        pack_dir / "04_mesh_raw",
    ]
    for d in subdirs:
        d.mkdir(parents=True, exist_ok=True)

    # 2. Build parts catalog
    parts_list = [
        {"id": "body_torso", "category": "body-essential", "expected_view": "strict_front", "status": "pending"},
        {"id": "body_legs", "category": "body-essential", "expected_view": "strict_front", "status": "pending"},
        {"id": "body_arms", "category": "body-essential", "expected_view": "strict_front", "status": "pending"},
        {"id": "head", "category": "body-essential", "expected_view": "neutral_front", "status": "pending"},
        {"id": "hair", "category": "hair", "expected_view": "isolated_front", "status": "pending"},
        {"id": "hands_pair", "category": "paired", "expected_view": "palms_front", "status": "pending"},
        {"id": "boots_pair", "category": "paired", "expected_view": "feet_front", "status": "pending"},
    ]
    for acc in accessories:
        clean_acc = acc.strip().replace(" ", "_").lower()
        parts_list.append({
            "id": clean_acc,
            "category": "accessory",
            "expected_view": "strict_front",
            "status": "pending"
        })

    # 3. Generate parts_inventory.md
    inventory_md = f"""# 📦 Modular Parts Inventory: {character_name}

- **Art Style**: {art_style}
- **Target Engine**: {target_engine}
- **Created At**: {datetime.now(timezone.utc).isoformat()}

## Parts Breakdown

| Index | Part ID | Category | Expected Orientation | Status | Verified (IoU) |
|---|---|---|---|---|---|
"""
    for i, p in enumerate(parts_list, start=1):
        inventory_md += f"| {i:02d} | `{p['id']}` | `{p['category']}` | {p['expected_view']} | {p['status']} | — |\n"

    inventory_md += """
---
## Modular Assembly Rules
1. **Zero 3/4 hero angles** on any extracted part.
2. Arms at $45^\\circ$ A-pose angle, palms facing forward or neutral down.
3. Legs straight, feet shoulder-width, toes facing dead front.
4. Accessories generated isolated on pure white with zero ambient shadow.
"""
    (pack_dir / "parts_inventory.md").write_text(inventory_md, encoding="utf-8")

    # 4. Generate manifest.json
    manifest = {
        "schema_version": "3.0",
        "character_name": character_name,
        "art_style": art_style,
        "target_engine": target_engine,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "stages": {
            "stage_1_intake": {"completed": False, "source_concept": None},
            "stage_2a_apose_sheet": {"completed": False, "model": "Nano Banana Pro", "file": "00_sheet/01a_apose_front.png", "symmetry_score": None},
            "stage_2b_multiview_sheet": {"completed": False, "model": "GPT-Image-2.5", "file": "00_sheet/01b_character_sheet.png"},
            "stage_4_parts_extraction": {"total_parts": len(parts_list), "approved_parts": 0, "parts": parts_list},
            "stage_4_5_verification_log": [],
            "stage_7_mesh_routing": {
                "3d_engine": "Higgsfield tripo_h3_1_image_to_3d",
                "face_limit": 25000,
                "texture_quality": "detailed",
                "texture_alignment": "original_image"
            }
        }
    }
    manifest_path = pack_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    return {
        "pack_dir": str(pack_dir),
        "character_name": character_name,
        "total_parts": len(parts_list),
        "manifest": str(manifest_path)
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Scaffold standardized 3D character package directory and manifest."
    )
    parser.add_argument("-d", "--dir", required=True, help="Directory to scaffold character_pack")
    parser.add_argument("-n", "--name", default="hero_character", help="Character name")
    parser.add_argument("-s", "--style", default="stylized_fantasy", help="Art style")
    parser.add_argument("-e", "--engine", default="Unreal_Engine_5", help="Target game engine")
    parser.add_argument(
        "--accessories", nargs="*", default=["weapon_sword", "shield", "pauldrons"],
        help="List of optional accessories to catalog"
    )

    args = parser.parse_args(argv)
    res = scaffold_pack(
        Path(args.dir),
        character_name=args.name,
        art_style=args.style,
        target_engine=args.engine,
        accessories=args.accessories
    )

    print("==================================================================")
    print("           3D CHARACTER PACKAGE SCAFFOLD COMPLETE                 ")
    print("==================================================================")
    print(f"Directory:       {res['pack_dir']}")
    print(f"Character:       {res['character_name']}")
    print(f"Cataloged Parts: {res['total_parts']}")
    print(f"Manifest:        {res['manifest']}")
    print("==================================================================")
    return 0


if __name__ == "__main__":
    sys.exit(main())
