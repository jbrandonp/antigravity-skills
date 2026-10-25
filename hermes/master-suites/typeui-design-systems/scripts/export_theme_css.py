#!/usr/bin/env python3
"""Offline CSS Theme Token Exporter for TypeUI Design Systems.

Exports design tokens (colors, radii, shadows, typography) for popular themes:
- bento
- brutalism
- neobrutalism
- glassmorphism
- editorial
- dark-modern
"""
from __future__ import annotations
import argparse
from pathlib import Path
import sys

THEMES = {
    "bento": {
        "--bg-canvas": "#f8fafc",
        "--bg-card": "#ffffff",
        "--text-primary": "#0f172a",
        "--text-muted": "#64748b",
        "--border-color": "#e2e8f0",
        "--radius-card": "16px",
        "--shadow-card": "0 4px 6px -1px rgb(0 0 0 / 0.05), 0 2px 4px -2px rgb(0 0 0 / 0.05)"
    },
    "neobrutalism": {
        "--bg-canvas": "#fef08a",
        "--bg-card": "#ffffff",
        "--text-primary": "#000000",
        "--text-muted": "#333333",
        "--border-color": "#000000",
        "--radius-card": "0px",
        "--shadow-card": "5px 5px 0px #000000"
    },
    "glassmorphism": {
        "--bg-canvas": "#0f172a",
        "--bg-card": "rgba(255, 255, 255, 0.08)",
        "--text-primary": "#ffffff",
        "--text-muted": "#94a3b8",
        "--border-color": "rgba(255, 255, 255, 0.15)",
        "--radius-card": "20px",
        "--shadow-card": "0 8px 32px 0 rgba(0, 0, 0, 0.37)"
    },
    "dark-modern": {
        "--bg-canvas": "#09090b",
        "--bg-card": "#18181b",
        "--text-primary": "#fafafa",
        "--text-muted": "#a1a1aa",
        "--border-color": "#27272a",
        "--radius-card": "12px",
        "--shadow-card": "0 10px 15px -3px rgb(0 0 0 / 0.4)"
    }
}

def export_css(theme_name: str, out_file: Path):
    tokens = THEMES.get(theme_name, THEMES["bento"])
    css = f"/* TypeUI Design System: {theme_name} */\n:root {{\n"
    for k, v in tokens.items():
        css += f"  {k}: {v};\n"
    css += "}\n"
    out_file.write_text(css, encoding="utf-8")
    print(f"✓ Exported CSS variables for '{theme_name}' to {out_file}")

def main() -> int:
    parser = argparse.ArgumentParser(description="TypeUI CSS Exporter")
    parser.add_argument("--theme", choices=list(THEMES.keys()), default="bento")
    parser.add_argument("--out", default="theme.css")
    args = parser.parse_args()

    export_css(args.theme, Path(args.out))
    return 0

if __name__ == "__main__":
    sys.exit(main())
