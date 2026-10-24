#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "pillow",
# ]
# ///
"""Automated Orthographic Symmetry & Anti-3/4 Drift Verifier.

Analyzes 2D character concept sheets and modular parts using computer vision:
1. Bilateral Silhouette Symmetry (Dice Coefficient / IoU vs Horizontally Flipped Mask)
2. Spine Verticality & Contrapposto Body Twist Angle
3. Estimated Lateral Azimuth Rotation (3/4 angle detector)
4. Framing Isolation & Boundary Crop Detection
Outputs PASS, SOFT_FAIL, or HARD_FAIL with remediation guidance.
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
    print("Run with uv: uv run scripts/verify_orthographic_symmetry.py ...")
    sys.exit(1)


def segment_foreground(
    img: Image.Image, bg_mode: str = "white", white_threshold: int = 240
) -> np.ndarray:
    """Segments foreground binary mask (True = foreground, False = background)."""
    rgba = img.convert("RGBA")
    arr = np.array(rgba)
    h, w, _ = arr.shape

    if bg_mode == "alpha":
        return arr[:, :, 3] > 20
    elif bg_mode == "chroma":
        # Green chroma (#00FF00) distance
        diff = np.sqrt(
            (arr[:, :, 0].astype(float) - 0.0) ** 2
            + (arr[:, :, 1].astype(float) - 255.0) ** 2
            + (arr[:, :, 2].astype(float) - 0.0) ** 2
        )
        return diff > 45.0
    else:  # white or neutral studio
        r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
        is_white = (r >= white_threshold) & (g >= white_threshold) & (b >= white_threshold)
        return ~is_white


def compute_symmetry_metrics(mask: np.ndarray) -> dict:
    """Computes bilateral symmetry, spine tilt, and rotation drift."""
    h, w = mask.shape
    if not np.any(mask):
        return {
            "symmetry_score": 0.0,
            "dice_coefficient": 0.0,
            "spine_tilt_degrees": 0.0,
            "estimated_azimuth_drift": 0.0,
            "aspect_ratio": 0.0,
            "is_cropped": True,
            "bbox": [0, 0, 0, 0],
        }

    y_indices, x_indices = np.where(mask)
    y_min, y_max = int(np.min(y_indices)), int(np.max(y_indices))
    x_min, x_max = int(np.min(x_indices)), int(np.max(x_indices))

    # Boundary crop check (touches image edges within 2px)
    is_cropped = (y_min <= 2) or (y_max >= h - 3) or (x_min <= 2) or (x_max >= w - 3)

    crop_h = max(1, y_max - y_min + 1)
    crop_w = max(1, x_max - x_min + 1)
    aspect_ratio = round(crop_w / crop_h, 3)

    # Extract centered crop
    cropped_mask = mask[y_min : y_max + 1, x_min : x_max + 1]

    # Bilateral Reflection along vertical centerline
    flipped_mask = np.fliplr(cropped_mask)

    intersection = np.sum(cropped_mask & flipped_mask)
    union = np.sum(cropped_mask | flipped_mask)
    total_area = np.sum(cropped_mask) + np.sum(flipped_mask)

    iou = float(intersection / union) if union > 0 else 0.0
    dice = float((2.0 * intersection) / total_area) if total_area > 0 else 0.0

    # Spine Verticality: Compute center of mass across vertical bands (from 20% to 80% height)
    sub_h = cropped_mask.shape[0]
    y_start, y_end = int(sub_h * 0.20), int(sub_h * 0.80)
    centers_x = []
    sample_y = []

    for y in range(y_start, y_end, max(1, (y_end - y_start) // 20)):
        row = cropped_mask[y, :]
        if np.any(row):
            cx = np.mean(np.where(row)[0])
            centers_x.append(cx)
            sample_y.append(y)

    spine_tilt = 0.0
    if len(centers_x) >= 5:
        # Fit linear regression: X = m * Y + b
        coeffs = np.polyfit(sample_y, centers_x, 1)
        slope = coeffs[0]  # dx / dy
        spine_tilt = round(math.degrees(math.atan(slope)), 2)

    # Lateral Mass Imbalance -> Estimated Azimuth Drift
    # If character turns in 3/4, one side has significantly more projected pixel volume
    mid_x = crop_w // 2
    left_mass = np.sum(cropped_mask[:, :mid_x])
    right_mass = np.sum(cropped_mask[:, mid_x:])
    total_mass = max(1, left_mass + right_mass)
    mass_diff_ratio = (right_mass - left_mass) / total_mass

    # Heuristic: 10% mass delta roughly corresponds to ~12° 3/4 azimuth drift
    estimated_azimuth = round(float(mass_diff_ratio * 120.0), 1)

    return {
        "symmetry_score": round(iou, 3),
        "dice_coefficient": round(dice, 3),
        "spine_tilt_degrees": spine_tilt,
        "estimated_azimuth_drift": estimated_azimuth,
        "aspect_ratio": aspect_ratio,
        "is_cropped": is_cropped,
        "bbox": [x_min, y_min, crop_w, crop_h],
    }


def verify_character_sheet(
    image_path: Path,
    bg_mode: str = "white",
    category: str = "body-essential",
    min_symmetry: float = 0.80,
    max_tilt: float = 4.0,
) -> dict:
    """Verifies orthographic strict-front compliance."""
    img = Image.open(image_path)
    mask = segment_foreground(img, bg_mode=bg_mode)
    metrics = compute_symmetry_metrics(mask)

    penalties = []
    verdict = "PASS"

    # Category threshold adjustment
    if category in ("hair", "accessory"):
        target_sym = min(min_symmetry, 0.72)
    elif category == "paired":
        target_sym = min_symmetry
    else:  # body-essential or sheet
        target_sym = min_symmetry

    # Checks
    sym = metrics["dice_coefficient"]
    tilt = abs(metrics["spine_tilt_degrees"])
    azimuth = abs(metrics["estimated_azimuth_drift"])

    if metrics["is_cropped"]:
        penalties.append("Subject touches image boundaries (clipped geometry).")
        verdict = "HARD_FAIL"

    if sym < (target_sym - 0.12) or azimuth > 18.0:
        penalties.append(
            f"Severe 3/4 rotation drift detected: Symmetry dice={sym} (target={target_sym}), estimated rotation ~{azimuth}° off-axis."
        )
        verdict = "HARD_FAIL"
    elif sym < target_sym or azimuth > 9.0:
        penalties.append(
            f"Mild asymmetry / hero tilt: Symmetry dice={sym}, estimated rotation ~{azimuth}°."
        )
        if verdict != "HARD_FAIL":
            verdict = "SOFT_FAIL"

    if tilt > (max_tilt * 1.5):
        penalties.append(f"Contrapposto or spinal tilt detected: {tilt}° off vertical.")
        verdict = "HARD_FAIL"
    elif tilt > max_tilt:
        penalties.append(f"Slight posture lean: {tilt}°.")
        if verdict != "HARD_FAIL":
            verdict = "SOFT_FAIL"

    # Remediation prompt suggestion if failed
    correction_prompt = ""
    if verdict in ("SOFT_FAIL", "HARD_FAIL"):
        direction_hint = "camera-left" if metrics["estimated_azimuth_drift"] > 0 else "camera-right"
        correction_prompt = (
            f"[CRITICAL CORRECTION] Previous generation failed orthographic verification: "
            f"Rotated ~{azimuth}° toward {direction_hint} (symmetry score: {sym*100:.1f}%). "
            f"YOU MUST REGENERATE AT STRICT DEAD-FRONT A-POSE. "
            f"Camera exactly at eye level. Zero 3/4 hero angle. Both shoulders and feet at identical depth."
        )

    return {
        "file": str(image_path),
        "category": category,
        "verdict": verdict,
        "metrics": metrics,
        "penalties": penalties,
        "escalated_correction_prompt": correction_prompt,
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Verify 2D character sheets for strict-front orthographic compliance."
    )
    parser.add_argument("-i", "--input", required=True, help="Input character image path")
    parser.add_argument(
        "--category",
        choices=["body-essential", "paired", "accessory", "hair", "sheet"],
        default="body-essential",
        help="Part category",
    )
    parser.add_argument(
        "--bg",
        choices=["white", "chroma", "alpha"],
        default="white",
        help="Background isolation mode",
    )
    parser.add_argument(
        "--min-symmetry",
        type=float,
        default=0.80,
        help="Minimum dice symmetry threshold (0.0 to 1.0)",
    )
    parser.add_argument(
        "--max-tilt",
        type=float,
        default=4.0,
        help="Maximum allowed spine tilt in degrees",
    )
    parser.add_argument("--json", action="store_true", help="Output raw JSON report")

    args = parser.parse_args(argv)

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: File not found: {input_path}", file=sys.stderr)
        return 1

    report = verify_character_sheet(
        input_path,
        bg_mode=args.bg,
        category=args.category,
        min_symmetry=args.min_symmetry,
        max_tilt=args.max_tilt,
    )

    if args.json:
        print(json.dumps(report, indent=2))
        return 0 if report["verdict"] != "HARD_FAIL" else 1

    print("==================================================================")
    print("      ORTHOGRAPHIC STRICT-FRONT VERIFICATION REPORT (V3)         ")
    print("==================================================================")
    print(f"File:       {report['file']}")
    print(f"Category:   {report['category']}")
    print(f"Verdict:    {report['verdict']}")
    print("------------------------------------------------------------------")
    m = report["metrics"]
    print(f"  • Bilateral Symmetry (Dice): {m['dice_coefficient']:.3f} (IoU: {m['symmetry_score']:.3f})")
    print(f"  • Spine Vertical Tilt:      {m['spine_tilt_degrees']}°")
    print(f"  • Est. Azimuth 3/4 Drift:   {m['estimated_azimuth_drift']}°")
    print(f"  • Aspect Ratio (W/H):       {m['aspect_ratio']}")
    print(f"  • Boundary Cropped:         {'YES (Geometry Clipped!)' if m['is_cropped'] else 'Clean'}")

    if report["penalties"]:
        print("\nFindings:")
        for p in report["penalties"]:
            print(f"  ⚠ {p}")

    if report["escalated_correction_prompt"]:
        print("\nEscalated Correction Prompt for Model Retry:")
        print(f"  >>> {report['escalated_correction_prompt']}")
    else:
        print("\n✓ Strict-front A-pose verified! Ready for 3D modular extraction.")

    print("==================================================================")
    return 0 if report["verdict"] != "HARD_FAIL" else 1


if __name__ == "__main__":
    sys.exit(main())
