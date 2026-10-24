#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "pillow",
#     "scipy",
# ]
# ///
"""Deterministic Pixel Snap Engine.

Eliminates mixels (sub-pixel artifacts, anti-aliased smearing, inconsistent grid pitch)
from AI-generated pixel art using autocorrelation grid detection, modal color voting,
and retro palette quantization.
"""

from __future__ import annotations

import argparse
import json
import math
import os
from pathlib import Path
import sys
from typing import Sequence

try:
    import numpy as np
    from PIL import Image
    from scipy.signal import find_peaks
except ImportError:
    # Allow execution via uv or direct error guidance
    print("Error: Missing required packages (numpy, pillow, scipy).")
    print("Run with uv: uv run scripts/pixel_snap.py ...")
    sys.exit(1)

# Classic Retro Palettes (Hex)
PRESET_PALETTES: dict[str, list[str]] = {
    "pico-8": [
        "#000000", "#1D2B53", "#7E2553", "#008751", "#AB5236", "#5F574F",
        "#C2C3C7", "#FFF1E8", "#FF004D", "#FFA300", "#FFEC27", "#00E436",
        "#29ADFF", "#83769C", "#FF77A8", "#FFCCAA"
    ],
    "gameboy-4": [
        "#0F380F", "#306230", "#8BAC0F", "#9BBC0F"
    ],
    "endesga-32": [
        "#BE4A2F", "#D77643", "#EAD4AA", "#E4A672", "#B86F50", "#733E39",
        "#3E2731", "#A22633", "#E43B44", "#F77622", "#FEE761", "#63C74D",
        "#3E8948", "#265C42", "#193C3E", "#124E89", "#0099DB", "#2CE8F5",
        "#FFFFFF", "#C0CBDC", "#8B9BB4", "#5A6988", "#3A4466", "#262B44",
        "#181425", "#FF0044", "#68386C", "#B55088", "#F6757A", "#E8B796",
        "#C28569", "#000000"
    ],
    "nes-54": [
        "#7C7C7C", "#0000FC", "#0000BC", "#4428BC", "#940084", "#A80020",
        "#A81000", "#881400", "#503000", "#007800", "#006800", "#005800",
        "#004058", "#000000", "#BCBCBC", "#0078F8", "#0058F8", "#6844FC",
        "#D800CC", "#E40058", "#F83800", "#E45C10", "#AC7C00", "#00B800",
        "#00A800", "#00A844", "#008888", "#F8F8F8", "#3CBCFC", "#6888FC",
        "#9878F8", "#F878F8", "#F85898", "#F87858", "#FCA044", "#F8B800",
        "#B8F818", "#58D854", "#58F898", "#00E8D8", "#787878", "#FCFCFC",
        "#A4E4FC", "#B8B8F8", "#D8B8F8", "#F8B8F8", "#F8A4C0", "#F0D0B0",
        "#FCE0A8", "#F8D878", "#D8F878", "#B8F8B8", "#B8F8D8", "#00FCFC"
    ]
}


def hex_to_rgb(hex_str: str) -> tuple[int, int, int]:
    """Converts a hex color string (#RRGGBB) to an RGB tuple."""
    h = hex_str.lstrip("#")
    if len(h) == 3:
        h = "".join([c * 2 for c in h])
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def rgb_to_hex(rgb: tuple[int, int, int]) -> str:
    """Converts an RGB tuple to #RRGGBB."""
    return f"#{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}"


def compute_gradient_1d(image_array: np.ndarray, axis: int) -> np.ndarray:
    """Computes Sobel gradient energy along a 1D projection."""
    # Convert RGB to grayscale luminance
    lum = (
        0.299 * image_array[:, :, 0]
        + 0.587 * image_array[:, :, 1]
        + 0.114 * image_array[:, :, 2]
    )
    if axis == 0:  # Vertical edges (X axis variation)
        diff = np.abs(np.diff(lum, axis=1))
        return np.mean(diff, axis=0)
    else:  # Horizontal edges (Y axis variation)
        diff = np.abs(np.diff(lum, axis=0))
        return np.mean(diff, axis=1)


def detect_cell_pitch(gradient_1d: np.ndarray, min_pitch: int = 4, max_pitch: int = 64) -> int:
    """Detects the median pixel cell pitch via gradient peak autocorrelation."""
    if len(gradient_1d) < 32:
        return 16
    # Compute autocorrelation
    norm_grad = gradient_1d - np.mean(gradient_1d)
    autocorr = np.correlate(norm_grad, norm_grad, mode="full")
    autocorr = autocorr[len(autocorr) // 2 :]

    if np.max(autocorr) > 0:
        autocorr = autocorr / np.max(autocorr)

    peaks, _ = find_peaks(autocorr[min_pitch:max_pitch], prominence=0.08)
    if len(peaks) > 0:
        detected = int(peaks[0] + min_pitch)
        # Power-of-two bias for standard pixel art (8, 16, 24, 32, 48, 64)
        for std in (8, 16, 24, 32, 48, 64):
            if abs(detected - std) <= 1:
                return std
        return detected

    return 16


def quantize_to_palette(
    rgb_array: np.ndarray, palette_rgb: list[tuple[int, int, int]]
) -> np.ndarray:
    """Maps each pixel to the closest color in the target palette via Euclidean RGB."""
    pal = np.array(palette_rgb, dtype=np.float32)  # (K, 3)
    orig_shape = rgb_array.shape
    flat_rgb = rgb_array.reshape(-1, 3).astype(np.float32)  # (N, 3)

    # Compute pairwise squared distances: (N, 1, 3) - (1, K, 3) -> (N, K)
    dists = np.sum((flat_rgb[:, np.newaxis, :] - pal[np.newaxis, :, :]) ** 2, axis=2)
    nearest_indices = np.argmin(dists, axis=1)
    quantized = pal[nearest_indices].astype(np.uint8)
    return quantized.reshape(orig_shape)


def snap_image(
    image: Image.Image,
    target_pitch: int | None = None,
    palette_name: str | None = None,
    chroma_hex: str | None = "#00FF00",
    chroma_tolerance: int = 35,
    custom_colors: int | None = None,
) -> tuple[Image.Image, dict]:
    """Applies the 5-step deterministic Pixel Snap algorithm."""
    img_rgb = image.convert("RGB")
    arr = np.array(img_rgb)
    h, w, _ = arr.shape

    # 1. Pitch Detection
    if target_pitch is None or target_pitch <= 0:
        grad_x = compute_gradient_1d(arr, axis=0)
        grad_y = compute_gradient_1d(arr, axis=1)
        pitch_x = detect_cell_pitch(grad_x)
        pitch_y = detect_cell_pitch(grad_y)
        pitch = max(pitch_x, pitch_y)
    else:
        pitch = target_pitch

    cells_x = max(1, w // pitch)
    cells_y = max(1, h // pitch)

    # 2. Chroma Masking
    is_chroma = np.zeros((h, w), dtype=bool)
    if chroma_hex:
        c_rgb = np.array(hex_to_rgb(chroma_hex), dtype=np.float32)
        diff = np.sqrt(np.sum((arr.astype(np.float32) - c_rgb) ** 2, axis=2))
        is_chroma = diff <= chroma_tolerance

    # 3. Cell Cut-Walking & Modal Color Voting
    snapped_native = np.zeros((cells_y, cells_x, 4), dtype=np.uint8)

    for cy in range(cells_y):
        for cx in range(cells_x):
            y0, y1 = cy * pitch, min(h, (cy + 1) * pitch)
            x0, x1 = cx * pitch, min(w, (cx + 1) * pitch)

            cell_pixels = arr[y0:y1, x0:x1]
            cell_chroma = is_chroma[y0:y1, x0:x1]

            # If more than 50% of the cell is chroma background, mark transparent
            if np.mean(cell_chroma) >= 0.5:
                snapped_native[cy, cx] = [0, 0, 0, 0]
                continue

            # Non-chroma pixels vote for modal color
            non_chroma = cell_pixels[~cell_chroma]
            if len(non_chroma) == 0:
                snapped_native[cy, cx] = [0, 0, 0, 0]
                continue

            # Compute median / mode color
            # Use discrete binning or median to prevent anti-aliasing smear
            median_color = np.median(non_chroma, axis=0).astype(np.uint8)
            snapped_native[cy, cx] = [
                median_color[0],
                median_color[1],
                median_color[2],
                255,
            ]

    # 4. Palette Quantization
    rgb_part = snapped_native[:, :, :3]
    alpha_part = snapped_native[:, :, 3]

    if palette_name and palette_name.lower() in PRESET_PALETTES:
        pal_hex = PRESET_PALETTES[palette_name.lower()]
        pal_rgb = [hex_to_rgb(hx) for hx in pal_hex]
        rgb_part = quantize_to_palette(rgb_part, pal_rgb)
    elif custom_colors and custom_colors > 0:
        # Quantize using PIL's adaptive palette
        temp_img = Image.fromarray(rgb_part)
        temp_quant = temp_img.quantize(colors=custom_colors, method=Image.Quantize.FASTOCTREE)
        rgb_part = np.array(temp_quant.convert("RGB"))

    # Recombine RGBA
    final_native = np.dstack((rgb_part, alpha_part))
    out_native_img = Image.fromarray(final_native, mode="RGBA")

    # Metrics
    opaque_mask = alpha_part > 0
    unique_colors = len(np.unique(rgb_part[opaque_mask], axis=0)) if np.any(opaque_mask) else 0

    stats = {
        "original_size": [w, h],
        "native_grid": [cells_x, cells_y],
        "cell_pitch": pitch,
        "unique_palette_colors": unique_colors,
        "palette_preset": palette_name or "none",
        "chroma_stripped": bool(chroma_hex),
    }

    return out_native_img, stats


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Deterministic Pixel Snap Engine for 2D Sprite Art."
    )
    parser.add_argument("-i", "--input", required=True, help="Path to input image PNG/JPG")
    parser.add_argument("-o", "--output", required=True, help="Path to output snapped PNG")
    parser.add_argument(
        "-p", "--pitch", type=int, default=0,
        help="Cell pitch in pixels (e.g. 16, 24, 32). Set 0 to auto-detect."
    )
    parser.add_argument(
        "--palette",
        choices=["pico-8", "gameboy-4", "endesga-32", "nes-54", "none"],
        default="none",
        help="Retro palette preset to enforce"
    )
    parser.add_argument(
        "--colors", type=int, default=0,
        help="Max adaptive palette colors (e.g. 16, 32)"
    )
    parser.add_argument(
        "--chroma", default="#00FF00",
        help="Chroma key hex color to remove (#00FF00 for green, none to disable)"
    )
    parser.add_argument(
        "--chroma-tolerance", type=int, default=35,
        help="Chroma key distance tolerance (0-100)"
    )
    parser.add_argument(
        "--scale", type=int, default=1,
        help="Nearest-neighbor integer scale multiplier for preview (e.g. 4 or 8)"
    )
    parser.add_argument(
        "--json", action="store_true",
        help="Output JSON statistics to stdout"
    )

    args = parser.parse_args(argv)

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file does not exist: {input_path}", file=sys.stderr)
        return 1

    img = Image.open(input_path)
    chroma = None if args.chroma.lower() in ("none", "") else args.chroma

    snapped_img, stats = snap_image(
        img,
        target_pitch=args.pitch if args.pitch > 0 else None,
        palette_name=args.palette if args.palette != "none" else None,
        chroma_hex=chroma,
        chroma_tolerance=args.chroma_tolerance,
        custom_colors=args.colors if args.colors > 0 else None,
    )

    # Scale if requested
    if args.scale > 1:
        w, h = snapped_img.size
        snapped_img = snapped_img.resize(
            (w * args.scale, h * args.scale), resample=Image.Resampling.NEAREST
        )
        stats["exported_scale"] = args.scale
        stats["exported_size"] = [w * args.scale, h * args.scale]
    else:
        stats["exported_scale"] = 1
        stats["exported_size"] = list(snapped_img.size)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    snapped_img.save(output_path, "PNG")

    if args.json:
        print(json.dumps(stats, indent=2))
    else:
        print(f"✓ Snapped sprite saved to: {output_path}")
        print(f"  Native Grid: {stats['native_grid'][0]}×{stats['native_grid'][1]} px (Cell Pitch: {stats['cell_pitch']}px)")
        print(f"  Unique Colors: {stats['unique_palette_colors']} (Palette: {stats['palette_preset']})")
        if args.scale > 1:
            print(f"  Export Preview: {stats['exported_size'][0]}×{stats['exported_size'][1]} px ({args.scale}x nearest)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
