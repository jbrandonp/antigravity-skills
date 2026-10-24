#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "pillow",
# ]
# ///
"""Pixel Art Quality Gate & Mixel Detection Engine.

Audits 2D pixel art sprites and spritesheets for:
1. Mixels (sub-pixel artifacts, non-integer grid transitions, blurring)
2. Alpha Channel Purity (1-bit binary alpha vs semi-transparent halo pixels)
3. Palette Cohesion (unique color count, near-duplicate color drift)
4. Dimension Contract Conformance (16, 32, 64, 128, 256 contracts)
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
    print("Run with uv: uv run scripts/audit_pixel_art.py ...")
    sys.exit(1)


def audit_sprite(
    image_path: Path,
    expected_grid: int = 0,
    max_colors: int = 32,
    alpha_tolerance: int = 0,
) -> dict:
    """Audits a pixel art image and returns a quality report."""
    img = Image.open(image_path).convert("RGBA")
    arr = np.array(img)
    h, w, _ = arr.shape

    report: dict = {
        "file": str(image_path),
        "dimensions": [w, h],
        "verdict": "PASS",
        "score": 100,
        "penalties": [],
        "metrics": {},
    }

    # 1. Alpha Purity Check (1-bit binary alpha)
    alpha = arr[:, :, 3]
    semi_transparent_mask = (alpha > alpha_tolerance) & (alpha < (255 - alpha_tolerance))
    semi_transparent_count = int(np.sum(semi_transparent_mask))
    total_pixels = w * h
    semi_alpha_ratio = semi_transparent_count / total_pixels

    report["metrics"]["semi_transparent_pixels"] = semi_transparent_count
    report["metrics"]["semi_alpha_ratio"] = round(semi_alpha_ratio, 4)

    if semi_transparent_count > 0:
        penalty = min(35, int(semi_alpha_ratio * 1000) + 10)
        report["penalties"].append(
            f"Alpha halo detected: {semi_transparent_count} semi-transparent pixels ({semi_alpha_ratio*100:.2f}%). Pixel art requires strict 1-bit binary alpha."
        )
        report["score"] -= penalty

    # 2. Palette Cohesion & Color Drift
    opaque_mask = alpha >= (255 - alpha_tolerance)
    if not np.any(opaque_mask):
        report["verdict"] = "FAIL"
        report["score"] = 0
        report["penalties"].append("Image is completely transparent.")
        return report

    opaque_rgb = arr[:, :, :3][opaque_mask]
    unique_colors = np.unique(opaque_rgb, axis=0)
    color_count = len(unique_colors)
    report["metrics"]["unique_colors"] = color_count

    if color_count > max_colors:
        penalty = min(30, int((color_count - max_colors) / 2))
        report["penalties"].append(
            f"Palette bloat: {color_count} unique colors detected (threshold is {max_colors}). Indicates anti-aliasing smear or unquantized gradients."
        )
        report["score"] -= penalty

    # Check for near-duplicate color drift (Euclidean distance < 12 in RGB)
    near_dupe_pairs = 0
    if 2 <= color_count <= 256:
        uc = unique_colors.astype(np.float32)
        diffs = np.sqrt(np.sum((uc[:, np.newaxis, :] - uc[np.newaxis, :, :]) ** 2, axis=2))
        np.fill_diagonal(diffs, 999.0)
        near_dupes = diffs < 12.0
        near_dupe_pairs = int(np.sum(near_dupes) // 2)

    report["metrics"]["near_duplicate_color_pairs"] = near_dupe_pairs
    if near_dupe_pairs > 3:
        penalty = min(20, near_dupe_pairs * 2)
        report["penalties"].append(
            f"Color drift: {near_dupe_pairs} near-duplicate color pairs found. Points to lossy compression or gradient bleeding."
        )
        report["score"] -= penalty

    # 3. Mixel & Sub-Pixel Anti-Aliasing Check
    # Examine horizontal and vertical color changes.
    # In authentic pixel art, color changes happen on integer boundaries.
    # Sub-pixel anti-aliasing creates subtle gradients across 1-2 pixels.
    lum = (
        0.299 * opaque_rgb[:, 0]
        + 0.587 * opaque_rgb[:, 1]
        + 0.114 * opaque_rgb[:, 2]
    )

    # Check gradient smoothness on 2D slice
    lum_2d = 0.299 * arr[:, :, 0] + 0.587 * arr[:, :, 1] + 0.114 * arr[:, :, 2]
    diff_x = np.abs(np.diff(lum_2d, axis=1))
    diff_y = np.abs(np.diff(lum_2d, axis=0))

    # Low-amplitude gradients (between 3 and 18 intensity) often signify anti-aliased mixels
    mixel_edges_x = np.sum((diff_x > 3) & (diff_x < 20))
    mixel_edges_y = np.sum((diff_y > 3) & (diff_y < 20))
    total_edges = np.sum(diff_x > 3) + np.sum(diff_y > 3)

    mixel_ratio = (mixel_edges_x + mixel_edges_y) / max(1, total_edges)
    report["metrics"]["mixel_edge_ratio"] = round(float(mixel_ratio), 4)

    if mixel_ratio > 0.35 and color_count > 16:
        penalty = min(25, int(mixel_ratio * 40))
        report["penalties"].append(
            f"Mixels detected: {mixel_ratio*100:.1f}% of edges exhibit soft anti-aliased gradients rather than crisp pixel clusters."
        )
        report["score"] -= penalty

    # 4. Dimension Contract Conformance
    standard_sizes = (16, 24, 32, 48, 64, 96, 128, 192, 256, 512, 1024, 2048)
    size_conforming = (w in standard_sizes) and (h in standard_sizes)
    report["metrics"]["standard_dimensions"] = size_conforming

    if not size_conforming and (w % 8 != 0 or h % 8 != 0):
        report["penalties"].append(
            f"Non-standard dimensions ({w}×{h} px). Native pixel art should conform to 8px/16px/32px grid multiples."
        )
        report["score"] -= 10

    # Final Verdict
    report["score"] = max(0, min(100, report["score"]))
    if report["score"] < 65:
        report["verdict"] = "FAIL"
    elif report["score"] < 85:
        report["verdict"] = "WARN"
    else:
        report["verdict"] = "PASS"

    return report


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Audit 2D pixel art for mixels, alpha halos, and palette purity."
    )
    parser.add_argument("-i", "--input", required=True, help="Path to pixel art image PNG")
    parser.add_argument(
        "--max-colors", type=int, default=32,
        help="Maximum expected unique colors in palette"
    )
    parser.add_argument(
        "--json", action="store_true",
        help="Output raw JSON report"
    )

    args = parser.parse_args(argv)

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: File not found: {input_path}", file=sys.stderr)
        return 1

    report = audit_sprite(input_path, max_colors=args.max_colors)

    if args.json:
        print(json.dumps(report, indent=2))
        return 0 if report["verdict"] != "FAIL" else 1

    print("==================================================================")
    print(f"             PIXEL ART QUALITY GATE AUDIT REPORT                  ")
    print("==================================================================")
    print(f"File:       {report['file']}")
    print(f"Dimensions: {report['dimensions'][0]}×{report['dimensions'][1]} px")
    print(f"Verdict:    {report['verdict']} (Score: {report['score']}/100)")
    print("------------------------------------------------------------------")
    print("Key Metrics:")
    print(f"  • Unique Colors:             {report['metrics']['unique_colors']}")
    print(f"  • Semi-transparent Pixels:   {report['metrics']['semi_transparent_pixels']}")
    print(f"  • Near-duplicate Pairs:      {report['metrics']['near_duplicate_color_pairs']}")
    print(f"  • Mixel Edge Ratio:          {report['metrics']['mixel_edge_ratio']*100:.1f}%")
    print(f"  • Standard Grid Conformance: {'Yes' if report['metrics']['standard_dimensions'] else 'No'}")

    if report["penalties"]:
        print("\nFindings & Recommendations:")
        for p in report["penalties"]:
            print(f"  ⚠ {p}")
    else:
        print("\n✓ Perfect pixel art integrity! Zero mixels, strict 1-bit alpha.")

    print("==================================================================")
    return 0 if report["verdict"] != "FAIL" else 1


if __name__ == "__main__":
    sys.exit(main())
