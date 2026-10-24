#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "pillow",
#     "scipy",
# ]
# ///
"""Connected-Component Frame Recovery Engine.

Recovers foreground character frames from generative AI pose boards (e.g. 2048x1536)
without naive uniform grid slicing, preventing decapitation of weapons, capes, or limbs.
Includes chroma despill, morphological bridging, and row-major frame sorting.
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
    from PIL import Image, ImageDraw
    from scipy.ndimage import binary_dilation, find_objects, label
except ImportError:
    print("Error: Missing required packages (numpy, pillow, scipy).")
    print("Run with uv: uv run scripts/extract_sprite_frames.py ...")
    sys.exit(1)


def hex_to_rgb(hex_str: str) -> tuple[int, int, int]:
    h = hex_str.lstrip("#")
    if len(h) == 3:
        h = "".join([c * 2 for c in h])
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def despill_chroma(rgba: np.ndarray, chroma_rgb: tuple[int, int, int], threshold: float = 40.0) -> np.ndarray:
    """Removes chroma green/magenta tint bleeding into edge pixels."""
    out = rgba.copy()
    c_r, c_g, c_b = chroma_rgb
    r = out[:, :, 0].astype(np.float32)
    g = out[:, :, 1].astype(np.float32)
    b = out[:, :, 2].astype(np.float32)
    a = out[:, :, 3]

    # If green chroma (#00FF00), damp excess green on semi-edges
    if c_g > c_r and c_g > c_b:
        excess = g - np.maximum(r, b)
        mask = (excess > 0) & (a > 0)
        out[:, :, 1][mask] = np.maximum(r, b)[mask].astype(np.uint8)
    return out


def extract_frames(
    image: Image.Image,
    chroma_hex: str = "#00FF00",
    chroma_tolerance: int = 35,
    min_width: int = 24,
    min_height: int = 24,
    bridge_dilation: int = 4,
    padding: int = 4,
    row_height_cluster: int = 250,
) -> tuple[list[tuple[Image.Image, tuple[int, int, int, int]]], Image.Image]:
    """Recovers connected character keyframes from a pose board."""
    rgb_img = image.convert("RGB")
    arr = np.array(rgb_img)
    h, w, _ = arr.shape

    # 1. Compute Chroma Mask
    c_rgb = hex_to_rgb(chroma_hex)
    diff = np.sqrt(np.sum((arr.astype(np.float32) - np.array(c_rgb, dtype=np.float32)) ** 2, axis=2))
    foreground_mask = diff > chroma_tolerance

    # 2. Morphological Dilation to bridge floating spell particles / weapons to main character
    if bridge_dilation > 0:
        kernel = np.ones((bridge_dilation * 2 + 1, bridge_dilation * 2 + 1), dtype=bool)
        dilated_mask = binary_dilation(foreground_mask, structure=kernel)
    else:
        dilated_mask = foreground_mask

    # 3. Connected Components Labeling
    labeled_array, num_features = label(dilated_mask)
    slices = find_objects(labeled_array)

    raw_boxes: list[tuple[int, int, int, int]] = []
    for s in slices:
        if s is None:
            continue
        y_slice, x_slice = s
        box_w = x_slice.stop - x_slice.start
        box_h = y_slice.stop - y_slice.start

        if box_w >= min_width and box_h >= min_height:
            # Check actual foreground pixel count to prevent hollow boxes
            cell_fg = foreground_mask[y_slice, x_slice]
            if np.sum(cell_fg) >= (min_width * min_height * 0.2):
                raw_boxes.append((x_slice.start, y_slice.start, x_slice.stop, y_slice.stop))

    # 4. Row-Major Sorting (sort by row band, then X)
    sorted_boxes = sorted(
        raw_boxes,
        key=lambda b: (b[1] // row_height_cluster, b[0])
    )

    # 5. Extract and Crop RGBA Frames with Despill
    # Build base RGBA
    rgba_full = np.dstack((arr, (foreground_mask.astype(np.uint8) * 255)))
    rgba_clean = despill_chroma(rgba_full, c_rgb)

    extracted_frames: list[tuple[Image.Image, tuple[int, int, int, int]]] = []
    debug_img = rgb_img.copy()
    draw = ImageDraw.Draw(debug_img)

    for i, (x0, y0, x1, y1) in enumerate(sorted_boxes):
        # Apply padding
        pad_x0 = max(0, x0 - padding)
        pad_y0 = max(0, y0 - padding)
        pad_x1 = min(w, x1 + padding)
        pad_y1 = min(h, y1 + padding)

        frame_data = rgba_clean[pad_y0:pad_y1, pad_x0:pad_x1]
        frame_pil = Image.fromarray(frame_data, mode="RGBA")
        extracted_frames.append((frame_pil, (pad_x0, pad_y0, pad_x1, pad_y1)))

        # Draw debug annotation
        draw.rectangle([x0, y0, x1, y1], outline=(255, 0, 0), width=3)
        draw.text((x0 + 4, y0 + 4), f"F{i:02d}", fill=(255, 255, 0))

    return extracted_frames, debug_img


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Extract connected sprite frames from AI pose boards."
    )
    parser.add_argument("-i", "--input", required=True, help="Input pose board image PNG/JPG")
    parser.add_argument(
        "-o", "--output-dir", required=True,
        help="Directory to save individual extracted frame PNGs"
    )
    parser.add_argument(
        "--chroma", default="#00FF00",
        help="Background chroma key color hex (#00FF00, #FF00FF, #0000FF)"
    )
    parser.add_argument(
        "--tolerance", type=int, default=35,
        help="Chroma key tolerance (0-100)"
    )
    parser.add_argument(
        "--min-size", type=int, default=24,
        help="Minimum bounding box width/height in px to keep"
    )
    parser.add_argument(
        "--bridge-gap", type=int, default=4,
        help="Dilation radius to bridge floating weapons/particles to character body"
    )
    parser.add_argument(
        "--padding", type=int, default=4,
        help="Padding in pixels around extracted frames"
    )
    parser.add_argument(
        "--row-height", type=int, default=250,
        help="Row cluster height for reading order sorting"
    )
    parser.add_argument(
        "--debug-sheet", default="",
        help="Optional path to save debug overlay PNG with bounding boxes"
    )

    args = parser.parse_args(argv)

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file does not exist: {input_path}", file=sys.stderr)
        return 1

    img = Image.open(input_path)
    frames, debug_img = extract_frames(
        img,
        chroma_hex=args.chroma,
        chroma_tolerance=args.tolerance,
        min_width=args.min_size,
        min_height=args.min_size,
        bridge_dilation=args.bridge_gap,
        padding=args.padding,
        row_height_cluster=args.row_height,
    )

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    manifest = []
    for idx, (frame_img, bbox) in enumerate(frames):
        fname = f"frame_{idx:02d}.png"
        fpath = out_dir / fname
        frame_img.save(fpath, "PNG")
        manifest.append({
            "index": idx,
            "filename": fname,
            "size": list(frame_img.size),
            "source_bbox": list(bbox)
        })

    manifest_path = out_dir / "frames_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    if args.debug_sheet:
        dbg_path = Path(args.debug_sheet)
        dbg_path.parent.mkdir(parents=True, exist_ok=True)
        debug_img.save(dbg_path, "PNG")

    print(f"✓ Recovered {len(frames)} frames to: {out_dir}")
    print(f"  Manifest written to: {manifest_path}")
    if args.debug_sheet:
        print(f"  Debug overlay saved to: {args.debug_sheet}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
