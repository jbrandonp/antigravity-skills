#!/usr/bin/env python3
"""
generate_art_palette.py — Mathematically calibrated color palette generator for algorithmic art.
Calculates harmonious palettes using Golden Ratio hue distribution, luminance ramps,
and perceptual color theory (analogous, complementary, triadic, monochrome).

Usage:
  python generate_art_palette.py [--scheme SCHEME] [--count N] [--base-hue H] [--format {js,json,css}]

Author: Antigravity Agentic Super Suite
"""

import sys
import argparse
import math
import json
from typing import List, Dict, Tuple

GOLDEN_RATIO_CONJUGATE = 0.618033988749895

PRESET_THEMES: Dict[str, List[str]] = {
    "nordic-mist": ["#2e3440", "#3b4252", "#434c5e", "#4c566a", "#88c0d0", "#81a1c1", "#5e81ac", "#eceff4"],
    "cyber-neon": ["#0d0221", "#0f084b", "#26408b", "#a6cfd5", "#c2e7da", "#ff007f", "#00f0ff", "#ffe600"],
    "japanese-woodblock": ["#2b2d42", "#8d99ae", "#edf2f4", "#ef233c", "#d90429", "#e9c46a", "#2a9d8f"],
    "solarized-warmth": ["#002b36", "#073642", "#586e75", "#657b83", "#b58900", "#cb4b16", "#dc322f", "#d33682"],
    "earth-mineral": ["#264653", "#2a9d8f", "#e9c46a", "#f4a261", "#e76f51", "#8ab17d", "#babb74"],
    "anthropic-editorial": ["#141413", "#faf9f5", "#b0aea5", "#e8e6dc", "#d97757", "#6a9bcc", "#788c5d"]
}


def hsl_to_rgb(h: float, s: float, l: float) -> Tuple[int, int, int]:
    """Convert HSL color (h in [0, 360], s, l in [0, 1]) to RGB [0, 255]."""
    c = (1.0 - abs(2.0 * l - 1.0)) * s
    x = c * (1.0 - abs((h / 60.0) % 2 - 1.0))
    m = l - c / 2.0

    if 0 <= h < 60:
        r_p, g_p, b_p = c, x, 0
    elif 60 <= h < 120:
        r_p, g_p, b_p = x, c, 0
    elif 120 <= h < 180:
        r_p, g_p, b_p = 0, c, x
    elif 180 <= h < 240:
        r_p, g_p, b_p = 0, x, c
    elif 240 <= h < 300:
        r_p, g_p, b_p = x, 0, c
    else:
        r_p, g_p, b_p = c, 0, x

    r = int(round((r_p + m) * 255))
    g = int(round((g_p + m) * 255))
    b = int(round((b_p + m) * 255))
    return max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b))


def rgb_to_hex(r: int, g: int, b: int) -> str:
    """Format RGB integers as a hexadecimal color string."""
    return f"#{r:02x}{g:02x}{b:02x}"


def generate_golden_ratio_palette(base_hue: float, count: int, saturation: float = 0.65, lightness: float = 0.55) -> List[str]:
    """Generate colors evenly spaced in perception using the golden ratio hue step."""
    colors = []
    current_h = base_hue % 360.0
    for i in range(count):
        # Vary lightness slightly for depth
        lum = lightness + 0.15 * math.sin(i * 1.618)
        lum = max(0.2, min(0.85, lum))
        r, g, b = hsl_to_rgb(current_h, saturation, lum)
        colors.append(rgb_to_hex(r, g, b))
        current_h = (current_h + GOLDEN_RATIO_CONJUGATE * 360.0) % 360.0
    return colors


def generate_analogous_palette(base_hue: float, count: int) -> List[str]:
    """Generate colors with close angular proximity on the color wheel."""
    colors = []
    spread = 60.0  # degrees total
    step = spread / max(1, count - 1)
    start_hue = (base_hue - spread / 2.0) % 360.0
    for i in range(count):
        h = (start_hue + i * step) % 360.0
        l = 0.35 + 0.5 * (i / max(1, count - 1))
        r, g, b = hsl_to_rgb(h, 0.70, l)
        colors.append(rgb_to_hex(r, g, b))
    return colors


def generate_monochrome_ramp(base_hue: float, count: int, saturation: float = 0.40) -> List[str]:
    """Generate high-contrast luminance ramp from dark shadow to bright highlight."""
    colors = []
    for i in range(count):
        l = 0.15 + 0.75 * (i / max(1, count - 1))
        r, g, b = hsl_to_rgb(base_hue, saturation, l)
        colors.append(rgb_to_hex(r, g, b))
    return colors


def generate_triadic_palette(base_hue: float, count: int) -> List[str]:
    """Generate triadic balanced palette (base, +120, +240)."""
    hues = [base_hue % 360.0, (base_hue + 120.0) % 360.0, (base_hue + 240.0) % 360.0]
    colors = []
    for i in range(count):
        h = hues[i % 3]
        l = 0.30 + 0.45 * ((i // 3) / max(1, count // 3))
        l = max(0.25, min(0.80, l))
        r, g, b = hsl_to_rgb(h, 0.65, l)
        colors.append(rgb_to_hex(r, g, b))
    return colors


def build_palette(scheme: str, count: int, base_hue: float) -> List[str]:
    """Build a palette according to scheme name or preset."""
    if scheme in PRESET_THEMES:
        preset = PRESET_THEMES[scheme]
        if len(preset) >= count:
            return preset[:count]
        # Wrap around if count > preset len
        return [preset[i % len(preset)] for i in range(count)]

    scheme_lower = scheme.lower()
    if scheme_lower == "golden-ratio" or scheme_lower == "golden":
        return generate_golden_ratio_palette(base_hue, count)
    elif scheme_lower == "analogous":
        return generate_analogous_palette(base_hue, count)
    elif scheme_lower == "monochrome" or scheme_lower == "mono":
        return generate_monochrome_ramp(base_hue, count)
    elif scheme_lower == "triadic":
        return generate_triadic_palette(base_hue, count)
    else:
        # Default to golden ratio
        return generate_golden_ratio_palette(base_hue, count)


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')

    parser = argparse.ArgumentParser(
        description="Generate mathematical color palettes for p5.js generative art."
    )
    schemes = ["golden-ratio", "analogous", "monochrome", "triadic"] + list(PRESET_THEMES.keys())
    parser.add_argument("--scheme", "-s", default="golden-ratio", choices=schemes, help="Color harmony scheme or preset.")
    parser.add_argument("--count", "-c", type=int, default=6, help="Number of colors to generate.")
    parser.add_argument("--base-hue", "-b", type=float, default=210.0, help="Base hue angle [0, 360].")
    parser.add_argument("--format", "-f", default="js", choices=["js", "json", "css", "hex"], help="Output format.")

    args = parser.parse_args()
    palette = build_palette(args.scheme, args.count, args.base_hue)

    if args.format == "js":
        formatted = json.dumps(palette)
        print(f"const colorPalette = {formatted};")
    elif args.format == "json":
        print(json.dumps({"scheme": args.scheme, "base_hue": args.base_hue, "colors": palette}, indent=2))
    elif args.format == "css":
        print(":root {")
        for idx, col in enumerate(palette):
            print(f"  --art-color-{idx + 1}: {col};")
        print("}")
    else:
        for col in palette:
            print(col)

    return 0


if __name__ == "__main__":
    sys.exit(main())
