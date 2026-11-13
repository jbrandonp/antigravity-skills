#!/usr/bin/env python3
"""Isometric Anatomy SVG Compiler.

Generates standalone, multi-layered isometric technical diagrams with:
- 30-degree isometric projection transformation
- Exploded vertical elevation
- Technical mechanical callouts and wiring
- Dark/editorial color schemes
"""

import argparse
import sys
from pathlib import Path

def generate_isometric_svg(title: str, layers: list, exploded: bool = False) -> str:
    spacing = 90 if exploded else 50
    width = 900
    height = 250 + len(layers) * spacing

    # Isometric colors (top, left, right faces)
    color_schemes = [
        {"top": "#38bdf8", "left": "#0284c7", "right": "#0369a1", "stroke": "#7dd3fc"},
        {"top": "#a855f7", "left": "#7e22ce", "right": "#6b21a8", "stroke": "#d8b4fe"},
        {"top": "#10b981", "left": "#059669", "right": "#047857", "stroke": "#6ee7b7"},
        {"top": "#f59e0b", "left": "#d97706", "right": "#b45309", "stroke": "#fcd34d"},
        {"top": "#ec4899", "left": "#db2777", "right": "#be185d", "stroke": "#f472b6"},
    ]

    svg_parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" style="background:#090d16; font-family: ui-monospace, SFMono-Regular, monospace;">',
        '  <defs>',
        '    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">',
        '      <feGaussianBlur stdDeviation="6" result="blur" />',
        '      <feComposite in="SourceGraphic" in2="blur" operator="over" />',
        '    </filter>',
        '  </defs>',
        f'  <text x="40" y="50" fill="#f8fafc" font-size="22" font-weight="bold">{title}</text>',
        f'  <text x="40" y="75" fill="#64748b" font-size="13">ISOMETRIC MECHANICAL ANATOMY • STANDALONE SVG</text>'
    ]

    cx = width // 2 - 50
    base_y = 130

    for idx, layer_name in enumerate(layers):
        scheme = color_schemes[idx % len(color_schemes)]
        y_offset = base_y + idx * spacing

        # Rhombus points for isometric slab
        # Isometric transformation: x' = (x - y)*cos(30), y' = (x + y)*sin(30)
        # Precomputed isometric polygon points:
        top_pts = f"{cx},{y_offset} {cx+180},{y_offset+90} {cx},{y_offset+180} {cx-180},{y_offset+90}"
        left_pts = f"{cx-180},{y_offset+90} {cx},{y_offset+180} {cx},{y_offset+205} {cx-180},{y_offset+115}"
        right_pts = f"{cx},{y_offset+180} {cx+180},{y_offset+90} {cx+180},{y_offset+115} {cx},{y_offset+205}"

        svg_parts.append(f'  <!-- Layer {idx+1}: {layer_name} -->')
        svg_parts.append(f'  <g id="layer-{idx+1}">')
        svg_parts.append(f'    <polygon points="{left_pts}" fill="{scheme["left"]}" opacity="0.9" />')
        svg_parts.append(f'    <polygon points="{right_pts}" fill="{scheme["right"]}" opacity="0.95" />')
        svg_parts.append(f'    <polygon points="{top_pts}" fill="{scheme["top"]}" stroke="{scheme["stroke"]}" stroke-width="1.5" />')

        # Layer Label with Leader Line
        callout_x = cx + 240
        callout_y = y_offset + 95
        svg_parts.append(f'    <line x1="{cx+130}" y1="{y_offset+90}" x2="{callout_x}" y2="{callout_y}" stroke="{scheme["stroke"]}" stroke-width="1.5" stroke-dasharray="3,3" />')
        svg_parts.append(f'    <circle cx="{cx+130}" cy="{y_offset+90}" r="4" fill="{scheme["stroke"]}" />')
        svg_parts.append(f'    <rect x="{callout_x+5}" y="{callout_y-14}" width="220" height="28" rx="4" fill="#0f172a" stroke="{scheme["stroke"]}" stroke-width="1" />')
        svg_parts.append(f'    <text x="{callout_x+16}" y="{callout_y+5}" fill="#f1f5f9" font-size="12" font-weight="600">{idx+1}. {layer_name}</text>')
        svg_parts.append('  </g>')

    svg_parts.append('</svg>')
    return '\n'.join(svg_parts)

def main():
    parser = argparse.ArgumentParser(description="Isometric Anatomy SVG Compiler")
    parser.add_argument("--title", default="System Architecture Anatomy", help="Diagram title")
    parser.add_argument("--layers", default="Database Layer,Service Mesh,API Gateway,Client Interface", help="Comma-separated layer names")
    parser.add_argument("--exploded", action="store_true", help="Use exploded vertical elevation")
    parser.add_argument("--output", default="anatomy.svg", help="Output SVG path")
    args = parser.parse_args()

    layer_list = [l.strip() for l in args.layers.split(",") if l.strip()]
    svg_content = generate_isometric_svg(args.title, layer_list, args.exploded)

    out_path = Path(args.output)
    out_path.write_text(svg_content, encoding="utf-8")
    print(f"Isometric SVG successfully written to: {out_path.resolve()}")

if __name__ == "__main__":
    main()
