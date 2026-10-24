#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "pillow",
# ]
# ///
"""Runtime Spritesheet Packer & Ground Aligner.

Stabilizes character animation ground contact (Y-baseline) and centers horizontal anchors,
preventing character foot-sliding, head-bobbing jitter, and floor clip in game engines.
Packs normalized frames into power-of-two spritesheets with engine-ready JSON metadata
(Godot 4, Unity, Phaser, Web Canvas).
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import sys
from typing import Sequence

try:
    import numpy as np
    from PIL import Image
except ImportError:
    print("Error: Missing required packages (numpy, pillow).")
    print("Run with uv: uv run scripts/pack_spritesheet.py ...")
    sys.exit(1)


def next_power_of_two(val: int) -> int:
    """Returns the smallest power of 2 greater than or equal to val."""
    if val <= 0:
        return 1
    return 1 << (val - 1).bit_length()


def analyze_frame_anchors(rgba_img: Image.Image) -> tuple[int, int, tuple[int, int, int, int]]:
    """Finds ground-contact Y (lowest opaque pixel) and horizontal center X."""
    arr = np.array(rgba_img)
    alpha = arr[:, :, 3] > 0
    h, w = alpha.shape

    if not np.any(alpha):
        return w // 2, h - 1, (0, 0, w, h)

    y_indices, x_indices = np.where(alpha)
    y_min, y_max = int(np.min(y_indices)), int(np.max(y_indices))
    x_min, x_max = int(np.min(x_indices)), int(np.max(x_indices))

    # Ground contact is the lowest row with opaque pixels
    ground_y = y_max
    # Center X is the midpoint between min and max X
    center_x = (x_min + x_max) // 2

    return center_x, ground_y, (x_min, y_min, x_max, y_max)


def pack_spritesheet(
    frame_paths: list[Path],
    align_mode: str = "ground",
    bottom_margin: int = 4,
    cell_padding: int = 2,
    columns: int = 0,
    enforce_power_of_two: bool = True,
    fps: int = 10,
) -> tuple[Image.Image, dict]:
    """Packs and aligns frames into a standardized spritesheet."""
    if not frame_paths:
        raise ValueError("No input frame paths provided.")

    loaded_frames = [Image.open(p).convert("RGBA") for p in frame_paths]
    n_frames = len(loaded_frames)

    # 1. Analyze Anchor Metrics across all frames
    anchors = [analyze_frame_anchors(im) for im in loaded_frames]

    # Calculate required cell dimensions
    max_above_ground = max((anc[1] - anc[2][1]) for anc in anchors)  # ground_y - y_min
    max_below_ground = max((anc[2][3] - anc[1]) for anc in anchors)  # y_max - ground_y
    max_half_width = max(
        max(anc[0] - anc[2][0], anc[2][2] - anc[0]) for anc in anchors
    )

    cell_w = max(32, (max_half_width * 2) + (cell_padding * 2))
    cell_h = max(32, max_above_ground + max_below_ground + bottom_margin + cell_padding)

    # Ensure even dimensions
    if cell_w % 2 != 0:
        cell_w += 1
    if cell_h % 2 != 0:
        cell_h += 1

    # 2. Compute Layout (Columns and Rows)
    if columns <= 0:
        # Default to a single strip for walk/attack cycles, or square-ish layout
        cols = n_frames if n_frames <= 16 else int(math.ceil(math.sqrt(n_frames)))
    else:
        cols = columns

    rows = int(math.ceil(n_frames / cols))

    sheet_w = cols * cell_w
    sheet_h = rows * cell_h

    if enforce_power_of_two:
        sheet_w = next_power_of_two(sheet_w)
        sheet_h = next_power_of_two(sheet_h)

    # 3. Create Canvas and Paste Aligned Frames
    sheet_img = Image.new("RGBA", (sheet_w, sheet_h), (0, 0, 0, 0))
    metadata_frames = []

    for idx, (img, (cx, gy, bbox)) in enumerate(zip(loaded_frames, anchors)):
        col_idx = idx % cols
        row_idx = idx // cols

        cell_origin_x = col_idx * cell_w
        cell_origin_y = row_idx * cell_h

        # Alignment offset calculation
        target_center_x = cell_origin_x + (cell_w // 2)
        if align_mode == "ground":
            target_contact_y = cell_origin_y + cell_h - bottom_margin
        elif align_mode == "center":
            target_contact_y = cell_origin_y + (cell_h // 2) + (img.size[1] // 4)
        else:  # top
            target_contact_y = cell_origin_y + img.size[1]

        paste_x = target_center_x - cx
        paste_y = target_contact_y - gy

        sheet_img.paste(img, (paste_x, paste_y), img)

        metadata_frames.append({
            "index": idx,
            "filename": frame_paths[idx].name,
            "frame": {
                "x": cell_origin_x,
                "y": cell_origin_y,
                "w": cell_w,
                "h": cell_h
            },
            "sourceSize": {"w": img.size[0], "h": img.size[1]},
            "anchor": {
                "x": round((target_center_x - cell_origin_x) / cell_w, 3),
                "y": round((target_contact_y - cell_origin_y) / cell_h, 3)
            }
        })

    metadata = {
        "meta": {
            "app": "2d-pixel-sprite-sheet-pipeline",
            "version": "2.0",
            "image": "spritesheet.png",
            "format": "RGBA8888",
            "size": {"w": sheet_w, "h": sheet_h},
            "scale": 1,
            "frame_count": n_frames,
            "fps": fps,
            "cell_size": {"w": cell_w, "h": cell_h},
            "columns": cols,
            "rows": rows,
            "align_mode": align_mode
        },
        "frames": metadata_frames
    }

    return sheet_img, metadata


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Pack normalized sprite frames into an aligned spritesheet."
    )
    parser.add_argument(
        "-i", "--input-dir", required=True,
        help="Directory containing frame PNGs (e.g. frame_00.png, frame_01.png)"
    )
    parser.add_argument(
        "-o", "--output-image", default="spritesheet.png",
        help="Path to output spritesheet PNG"
    )
    parser.add_argument(
        "--output-json", default="",
        help="Optional path to output metadata JSON (defaults to <image_name>.json)"
    )
    parser.add_argument(
        "--align", choices=["ground", "center", "top"], default="ground",
        help="Vertical alignment strategy (ground = feet lock to baseline)"
    )
    parser.add_argument(
        "--margin", type=int, default=4,
        help="Bottom ground margin in pixels"
    )
    parser.add_argument(
        "--columns", type=int, default=0,
        help="Number of columns in spritesheet (0 = single strip or auto)"
    )
    parser.add_argument(
        "--fps", type=int, default=10,
        help="Target animation frame rate in FPS"
    )
    parser.add_argument(
        "--no-pot", action="store_true",
        help="Do not enforce power-of-two texture dimensions"
    )

    args = parser.parse_args(argv)

    in_dir = Path(args.input_dir)
    if not in_dir.exists():
        print(f"Error: Directory not found: {in_dir}", file=sys.stderr)
        return 1

    # Gather frame files
    extensions = ("*.png", "*.PNG")
    frames: list[Path] = []
    for ext in extensions:
        frames.extend(in_dir.glob(ext))

    # Exclude any existing spritesheets
    frames = [f for f in sorted(frames) if "spritesheet" not in f.name.lower()]

    if not frames:
        print(f"Error: No frame PNG files found in {in_dir}", file=sys.stderr)
        return 1

    sheet_img, meta = pack_spritesheet(
        frames,
        align_mode=args.align,
        bottom_margin=args.margin,
        columns=args.columns,
        enforce_power_of_two=not args.no_pot,
        fps=args.fps,
    )

    out_img_path = Path(args.output_image)
    out_img_path.parent.mkdir(parents=True, exist_ok=True)
    sheet_img.save(out_img_path, "PNG")

    json_path = (
        Path(args.output_json)
        if args.output_json
        else out_img_path.with_suffix(".json")
    )
    meta["meta"]["image"] = out_img_path.name
    json_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")

    print(f"✓ Spritesheet packed: {out_img_path} ({sheet_img.size[0]}×{sheet_img.size[1]} px)")
    print(f"  Frames: {len(frames)} (Cell size: {meta['meta']['cell_size']['w']}×{meta['meta']['cell_size']['h']} px)")
    print(f"  Alignment: {args.align} (Locked to baseline)")
    print(f"  Metadata: {json_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
