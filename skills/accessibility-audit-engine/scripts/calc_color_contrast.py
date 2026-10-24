#!/usr/bin/env python3
"""WCAG 2.2 Color Contrast Ratio Calculator & Design System Palette Auditor.

Implements the official W3C relative luminance formula (WCAG 2.1 / 2.2):
- WCAG 1.4.3: Contrast (Minimum) - Level AA: 4.5:1 (normal text), 3.0:1 (large text)
- WCAG 1.4.6: Contrast (Enhanced) - Level AAA: 7.0:1 (normal text), 4.5:1 (large text)
- WCAG 1.4.11: Non-text Contrast - Level AA: 3.0:1 (UI components, borders, icons)
Includes automatic suggestion of the nearest compliant color.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import re
import sys
from typing import Sequence

NAMED_COLORS = {
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "red": (255, 0, 0),
    "green": (0, 128, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "navy": (0, 0, 128),
    "teal": (0, 128, 128),
    "gray": (128, 128, 128),
    "grey": (128, 128, 128),
    "silver": (192, 192, 192),
    "orange": (255, 165, 0),
    "purple": (128, 0, 128),
    "transparent": (0, 0, 0),
}


def parse_color(color_str: str) -> tuple[int, int, int]:
    """Parses Hex, RGB, or Named color into an (R, G, B) tuple [0-255]."""
    s = color_str.strip().lower()

    if s in NAMED_COLORS:
        return NAMED_COLORS[s]

    # Hex: #fff, #ffffff, #ffffff80
    if s.startswith("#"):
        h = s.lstrip("#")
        if len(h) == 3:
            return int(h[0] * 2, 16), int(h[1] * 2, 16), int(h[2] * 2, 16)
        elif len(h) >= 6:
            return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)

    # rgb(...) or rgba(...)
    rgb_m = re.match(r"rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)", s)
    if rgb_m:
        return int(rgb_m.group(1)), int(rgb_m.group(2)), int(rgb_m.group(3))

    raise ValueError(f"Unsupported color format: '{color_str}'")


def srgb_to_linear(c: float) -> float:
    """Converts an sRGB 8-bit channel [0.0 - 1.0] to linear luminance."""
    if c <= 0.04045:
        return c / 12.92
    return ((c + 0.055) / 1.055) ** 2.4


def relative_luminance(rgb: tuple[int, int, int]) -> float:
    """Calculates relative luminance L [0.0 - 1.0] per W3C WCAG 2.1 formula."""
    r = srgb_to_linear(rgb[0] / 255.0)
    g = srgb_to_linear(rgb[1] / 255.0)
    b = srgb_to_linear(rgb[2] / 255.0)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(color_a: tuple[int, int, int], color_b: tuple[int, int, int]) -> float:
    """Calculates the contrast ratio between two colors (range: 1.0 - 21.0)."""
    l1 = relative_luminance(color_a)
    l2 = relative_luminance(color_b)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def rgb_to_hex(rgb: tuple[int, int, int]) -> str:
    return f"#{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}"


def suggest_compliant_color(
    fg_rgb: tuple[int, int, int],
    bg_rgb: tuple[int, int, int],
    target_ratio: float = 4.5
) -> str:
    """Finds the nearest compliant foreground color by adjusting luminance."""
    bg_lum = relative_luminance(bg_rgb)
    fg_lum = relative_luminance(fg_rgb)

    # Determine whether to lighten or darken
    darken = bg_lum > 0.5

    r, g, b = fg_rgb
    for step in range(1, 256):
        if darken:
            new_r = max(0, r - step)
            new_g = max(0, g - step)
            new_b = max(0, b - step)
        else:
            new_r = min(255, r + step)
            new_g = min(255, g + step)
            new_b = min(255, b + step)

        new_rgb = (new_r, new_g, new_b)
        if contrast_ratio(new_rgb, bg_rgb) >= target_ratio:
            return rgb_to_hex(new_rgb)

    return "#000000" if darken else "#FFFFFF"


def evaluate_contrast(fg_str: str, bg_str: str) -> dict:
    """Evaluates contrast ratio and compliance status against all WCAG tiers."""
    fg_rgb = parse_color(fg_str)
    bg_rgb = parse_color(bg_str)
    ratio = round(contrast_ratio(fg_rgb, bg_rgb), 2)

    pass_aa_normal = ratio >= 4.5
    pass_aa_large = ratio >= 3.0
    pass_aa_ui = ratio >= 3.0
    pass_aaa_normal = ratio >= 7.0
    pass_aaa_large = ratio >= 4.5

    suggestion = None
    if not pass_aa_normal:
        suggestion = suggest_compliant_color(fg_rgb, bg_rgb, 4.5)

    return {
        "foreground": rgb_to_hex(fg_rgb),
        "background": rgb_to_hex(bg_rgb),
        "contrast_ratio": f"{ratio}:1",
        "raw_ratio": ratio,
        "wcag_compliance": {
            "AA_normal_text_4_5": pass_aa_normal,
            "AA_large_text_3_0": pass_aa_large,
            "AA_ui_components_3_0": pass_aa_ui,
            "AAA_normal_text_7_0": pass_aaa_normal,
            "AAA_large_text_4_5": pass_aaa_large,
        },
        "verdict": "PASS" if pass_aa_normal else ("WARN" if pass_aa_large else "FAIL"),
        "suggested_fg": suggestion
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="WCAG 2.2 Relative Luminance & Contrast Ratio Calculator."
    )
    parser.add_argument("--fg", help="Foreground color (hex, rgb, or name, e.g. '#333333' or 'blue')")
    parser.add_argument("--bg", help="Background color (hex, rgb, or name, e.g. '#ffffff')")
    parser.add_argument("--palette", help="Path to JSON file containing color pairs to audit")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")

    args = parser.parse_args(argv)

    if args.palette:
        p_path = Path(args.palette)
        if not p_path.exists():
            print(f"Error: Palette file '{p_path}' not found.", file=sys.stderr)
            return 1
        data = json.loads(p_path.read_text(encoding="utf-8"))
        results = []
        for pair in data:
            fg = pair.get("fg") or pair.get("color")
            bg = pair.get("bg") or pair.get("background", "#FFFFFF")
            res = evaluate_contrast(fg, bg)
            res["label"] = pair.get("label", "custom-pair")
            results.append(res)

        if args.json:
            print(json.dumps(results, indent=2))
        else:
            print("==================================================================")
            print("         DESIGN SYSTEM CONTRAST RATIO AUDIT MATRIX                ")
            print("==================================================================")
            for r in results:
                status = f"[{r['verdict']}]"
                print(f"{status:8} {r.get('label', ''):20} FG: {r['foreground']} on BG: {r['background']} -> {r['contrast_ratio']}")
                if r["verdict"] == "FAIL" and r["suggested_fg"]:
                    print(f"         └─ Suggestion for AA: {r['suggested_fg']}")
            print("==================================================================")
        return 0

    if not args.fg or not args.bg:
        print("Error: Specify both --fg and --bg (e.g. --fg '#111' --bg '#fff') or use --palette <file.json>.", file=sys.stderr)
        return 1

    try:
        report = evaluate_contrast(args.fg, args.bg)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(report, indent=2))
        return 0 if report["verdict"] != "FAIL" else 1

    print("==================================================================")
    print("         WCAG 2.2 COLOR CONTRAST RATIO EVALUATION                 ")
    print("==================================================================")
    print(f"Foreground:      {report['foreground']}")
    print(f"Background:      {report['background']}")
    print(f"Contrast Ratio:  {report['contrast_ratio']}")
    print(f"Overall Verdict: {report['verdict']}")
    print("------------------------------------------------------------------")
    comp = report["wcag_compliance"]
    print(f"  • WCAG AA Normal Text (>= 4.5:1): {'✓ PASS' if comp['AA_normal_text_4_5'] else '✗ FAIL'}")
    print(f"  • WCAG AA Large Text  (>= 3.0:1): {'✓ PASS' if comp['AA_large_text_3_0'] else '✗ FAIL'}")
    print(f"  • WCAG AA UI / Icons  (>= 3.0:1): {'✓ PASS' if comp['AA_ui_components_3_0'] else '✗ FAIL'}")
    print(f"  • WCAG AAA Normal     (>= 7.0:1): {'✓ PASS' if comp['AAA_normal_text_7_0'] else '✗ FAIL'}")
    print(f"  • WCAG AAA Large      (>= 4.5:1): {'✓ PASS' if comp['AAA_large_text_4_5'] else '✗ FAIL'}")

    if report["suggested_fg"]:
        print("\nRecommendation for AA (4.5:1) Compliance:")
        print(f"  Shift foreground to: {report['suggested_fg']}")

    print("==================================================================")
    return 0 if report["verdict"] != "FAIL" else 1


if __name__ == "__main__":
    sys.exit(main())
