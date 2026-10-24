#!/usr/bin/env python3
"""
generate_ui_tokens.py — Deterministic 4-layer design token generator for Anti-UI Slop engineering.
Generates CSS variables, Tailwind configuration, or JSON design tokens adhering to:
  1. The 4-Layer Color System (Canvas, Surface, Border, Accent)
  2. Dark Mode Elevation (z-index luminance climbing, never raw inversion)
  3. Micro-Interaction Timing (cubic-bezier(0.16, 1, 0.3, 1))
  4. Tabular Figures & 4px/8px Spatial Scale

Usage:
  python generate_ui_tokens.py [--theme {slate-enterprise,zinc-craft,warm-stone,obsidian-midnight}] [--format {css,tailwind,json}]

Author: Antigravity Agentic Super Suite
"""

import sys
import json
import argparse
from typing import Dict, Any

THEMES: Dict[str, Dict[str, Any]] = {
    "zinc-craft": {
        "light": {
            "bg_canvas": "#fafafa",
            "bg_surface": "#ffffff",
            "bg_surface_elevated": "#ffffff",
            "border_subtle": "#e4e4e7",
            "border_strong": "#d4d4d8",
            "text_primary": "#09090b",
            "text_secondary": "#52525b",
            "text_muted": "#71717a",
            "accent_primary": "#18181b",
            "accent_hover": "#27272a",
            "accent_contrast": "#ffffff"
        },
        "dark": {
            "bg_canvas": "#09090b",
            "bg_surface": "#121215",
            "bg_surface_elevated": "#18181b",
            "border_subtle": "#27272a",
            "border_strong": "#3f3f46",
            "text_primary": "#fafafa",
            "text_secondary": "#a1a1aa",
            "text_muted": "#71717a",
            "accent_primary": "#fafafa",
            "accent_hover": "#e4e4e7",
            "accent_contrast": "#09090b"
        }
    },
    "slate-enterprise": {
        "light": {
            "bg_canvas": "#f8fafc",
            "bg_surface": "#ffffff",
            "bg_surface_elevated": "#ffffff",
            "border_subtle": "#e2e8f0",
            "border_strong": "#cbd5e1",
            "text_primary": "#0f172a",
            "text_secondary": "#475569",
            "text_muted": "#64748b",
            "accent_primary": "#2563eb",
            "accent_hover": "#1d4ed8",
            "accent_contrast": "#ffffff"
        },
        "dark": {
            "bg_canvas": "#0b1120",
            "bg_surface": "#111827",
            "bg_surface_elevated": "#1e293b",
            "border_subtle": "#1e293b",
            "border_strong": "#334155",
            "text_primary": "#f8fafc",
            "text_secondary": "#94a3b8",
            "text_muted": "#64748b",
            "accent_primary": "#3b82f6",
            "accent_hover": "#60a5fa",
            "accent_contrast": "#ffffff"
        }
    },
    "warm-stone": {
        "light": {
            "bg_canvas": "#fafaf9",
            "bg_surface": "#ffffff",
            "bg_surface_elevated": "#ffffff",
            "border_subtle": "#e7e5e4",
            "border_strong": "#d6d3d1",
            "text_primary": "#1c1917",
            "text_secondary": "#57534e",
            "text_muted": "#78716c",
            "accent_primary": "#ea580c",
            "accent_hover": "#c2410c",
            "accent_contrast": "#ffffff"
        },
        "dark": {
            "bg_canvas": "#0c0a09",
            "bg_surface": "#141210",
            "bg_surface_elevated": "#1c1917",
            "border_subtle": "#292524",
            "border_strong": "#44403c",
            "text_primary": "#fafaf9",
            "text_secondary": "#a8a29e",
            "text_muted": "#78716c",
            "accent_primary": "#f97316",
            "accent_hover": "#fb923c",
            "accent_contrast": "#0c0a09"
        }
    },
    "obsidian-midnight": {
        "light": {
            "bg_canvas": "#f4f4f5",
            "bg_surface": "#ffffff",
            "bg_surface_elevated": "#ffffff",
            "border_subtle": "#e4e4e7",
            "border_strong": "#a1a1aa",
            "text_primary": "#18181b",
            "text_secondary": "#52525b",
            "text_muted": "#71717a",
            "accent_primary": "#059669",
            "accent_hover": "#047857",
            "accent_contrast": "#ffffff"
        },
        "dark": {
            "bg_canvas": "#050507",
            "bg_surface": "#0c0c10",
            "bg_surface_elevated": "#14141a",
            "border_subtle": "#1a1a24",
            "border_strong": "#272738",
            "text_primary": "#f4f4f5",
            "text_secondary": "#9ca3af",
            "text_muted": "#6b7280",
            "accent_primary": "#10b981",
            "accent_hover": "#34d399",
            "accent_contrast": "#050507"
        }
    }
}

MOTION_TOKENS = {
    "ease_out_expo": "cubic-bezier(0.16, 1, 0.3, 1)",
    "ease_in_out": "cubic-bezier(0.4, 0, 0.2, 1)",
    "duration_fast": "150ms",
    "duration_normal": "200ms",
    "duration_slow": "300ms"
}


def render_css_variables(theme_name: str) -> str:
    """Render CSS custom properties for light and dark modes."""
    t = THEMES[theme_name]
    lines = [
        f"/* Anti-UI Slop Design System: {theme_name} */",
        ":root {",
        "  /* Motion & Easing */",
        f"  --ease-out-expo: {MOTION_TOKENS['ease_out_expo']};",
        f"  --duration-fast: {MOTION_TOKENS['duration_fast']};",
        f"  --duration-normal: {MOTION_TOKENS['duration_normal']};",
        "",
        "  /* 4-Layer Light Color Architecture */"
    ]
    for k, v in t["light"].items():
        lines.append(f"  --{k.replace('_', '-')}: {v};")

    lines.extend([
        "}",
        "",
        ".dark, [data-theme='dark'] {",
        "  /* 4-Layer Dark Mode Elevation */"
    ])
    for k, v in t["dark"].items():
        lines.append(f"  --{k.replace('_', '-')}: {v};")
    lines.append("}")

    return "\n".join(lines)


def render_tailwind_config(theme_name: str) -> str:
    """Render Tailwind theme.extend configuration."""
    t = THEMES[theme_name]
    config = {
        "theme": {
            "extend": {
                "colors": {
                    "canvas": "var(--bg-canvas)",
                    "surface": {
                        "DEFAULT": "var(--bg-surface)",
                        "elevated": "var(--bg-surface-elevated)"
                    },
                    "border": {
                        "subtle": "var(--border-subtle)",
                        "strong": "var(--border-strong)"
                    },
                    "foreground": {
                        "DEFAULT": "var(--text-primary)",
                        "secondary": "var(--text-secondary)",
                        "muted": "var(--text-muted)"
                    },
                    "accent": {
                        "DEFAULT": "var(--accent-primary)",
                        "hover": "var(--accent-hover)",
                        "contrast": "var(--accent-contrast)"
                    }
                },
                "transitionTimingFunction": {
                    "expo": MOTION_TOKENS["ease_out_expo"]
                }
            }
        }
    }
    return f"// tailwind.config.js snippet ({theme_name})\nmodule.exports = " + json.dumps(config, indent=2) + ";"


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')

    parser = argparse.ArgumentParser(
        description="Generate 4-layer Anti-UI Slop design tokens in CSS, Tailwind, or JSON."
    )
    parser.add_argument("--theme", choices=list(THEMES.keys()), default="zinc-craft", help="Design system theme palette.")
    parser.add_argument("--format", choices=["css", "tailwind", "json"], default="css", help="Output token format.")

    args = parser.parse_args()

    if args.format == "css":
        print(render_css_variables(args.theme))
    elif args.format == "tailwind":
        print(render_tailwind_config(args.theme))
    elif args.format == "json":
        data = {
            "theme": args.theme,
            "motion": MOTION_TOKENS,
            "palette": THEMES[args.theme]
        }
        print(json.dumps(data, indent=2))

    return 0


if __name__ == "__main__":
    sys.exit(main())
