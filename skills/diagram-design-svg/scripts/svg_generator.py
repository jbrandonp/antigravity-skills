#!/usr/bin/env python3
"""Standalone Editorial SVG/HTML Technical Diagram Generator.

Generates professional, responsive, zero-dependency SVG technical diagrams
embedded in standalone HTML with adaptive light/dark mode styling.
Inspired by cathrynlavery/diagram-design (66k+ stars).
"""

import argparse
from pathlib import Path
import sys

DIAGRAM_TEMPLATES = {
    "architecture": """<svg viewBox="0 0 800 450" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      .box { rx: 8px; fill: var(--bg-card); stroke: var(--border-color); stroke-width: 1.5; }
      .box-accent { rx: 8px; fill: var(--bg-accent); stroke: var(--primary); stroke-width: 2; }
      .title { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-size: 14px; font-weight: bold; fill: var(--text-primary); }
      .subtitle { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-size: 12px; fill: var(--text-secondary); }
      .arrow { stroke: var(--primary); stroke-width: 2; marker-end: url(#arrowhead); }
    </style>
    <marker id="arrowhead" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
      <polygon points="0 0, 8 3, 0 6" fill="var(--primary)" />
    </marker>
  </defs>

  <!-- Client Layer -->
  <rect x="50" y="80" width="180" height="90" class="box" />
  <text x="70" y="115" class="title">Client Layer</text>
  <text x="70" y="140" class="subtitle">Agent CLI / Web Browser</text>

  <!-- Gateway Layer -->
  <rect x="310" y="80" width="180" height="90" class="box-accent" />
  <text x="330" y="115" class="title">API Gateway</text>
  <text x="330" y="140" class="subtitle">Auth, Rate-Limit & FTS5</text>

  <!-- Service Layer -->
  <rect x="570" y="80" width="180" height="90" class="box" />
  <text x="590" y="115" class="title">Engine Core</text>
  <text x="590" y="140" class="subtitle">Async FastAPI / SQLite WAL</text>

  <!-- Storage Layer -->
  <rect x="310" y="270" width="180" height="90" class="box" />
  <text x="330" y="305" class="title">Persistence</text>
  <text x="330" y="330" class="subtitle">SQLite WAL + Local Parquet</text>

  <!-- Arrows -->
  <line x1="230" y1="125" x2="300" y2="125" class="arrow" />
  <line x1="490" y1="125" x2="560" y2="125" class="arrow" />
  <line x1="400" y1="170" x2="400" y2="260" class="arrow" />
</svg>""",
    "sequence": """<svg viewBox="0 0 800 450" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      .actor { rx: 6px; fill: var(--bg-accent); stroke: var(--primary); stroke-width: 1.5; }
      .actor-text { font-family: sans-serif; font-size: 13px; font-weight: bold; fill: var(--text-primary); text-anchor: middle; }
      .lifeline { stroke: var(--border-color); stroke-width: 1; stroke-dasharray: 4; }
      .msg { stroke: var(--primary); stroke-width: 1.5; marker-end: url(#arrowhead); }
      .msg-text { font-family: sans-serif; font-size: 11px; fill: var(--text-secondary); text-anchor: middle; }
    </style>
    <marker id="arrowhead" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
      <polygon points="0 0, 8 3, 0 6" fill="var(--primary)" />
    </marker>
  </defs>

  <!-- Actors -->
  <rect x="100" y="40" width="120" height="40" class="actor" /><text x="160" y="65" class="actor-text">Agent</text>
  <rect x="340" y="40" width="120" height="40" class="actor" /><text x="400" y="65" class="actor-text">ContextBuffer</text>
  <rect x="580" y="40" width="120" height="40" class="actor" /><text x="640" y="65" class="actor-text">SQLite FTS5</text>

  <!-- Lifelines -->
  <line x1="160" y1="80" x2="160" y2="400" class="lifeline" />
  <line x1="400" y1="80" x2="400" y2="400" class="lifeline" />
  <line x1="640" y1="80" x2="640" y2="400" class="lifeline" />

  <!-- Messages -->
  <line x1="160" y1="130" x2="390" y2="130" class="msg" /><text x="280" y="122" class="msg-text">1. run(command)</text>
  <line x1="400" y1="180" x2="630" y2="180" class="msg" /><text x="520" y="172" class="msg-text">2. insert_log(FTS5)</text>
  <line x1="400" y1="230" x2="170" y2="230" class="msg" /><text x="280" y="222" class="msg-text">3. summary (5 lines)</text>
  <line x1="160" y1="290" x2="630" y2="290" class="msg" /><text x="400" y="282" class="msg-text">4. search(BM25 snippet)</text>
  <line x1="640" y1="340" x2="170" y2="340" class="msg" /><text x="400" y="332" class="msg-text">5. exact failure trace</text>
</svg>"""
}

def render_standalone_html(title: str, svg_content: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
  :root {{
    --bg-page: #f8fafc;
    --bg-card: #ffffff;
    --bg-accent: #f1f5f9;
    --border-color: #cbd5e1;
    --text-primary: #0f172a;
    --text-secondary: #475569;
    --primary: #0284c7;
  }}
  @media (prefers-color-scheme: dark) {{
    :root {{
      --bg-page: #0b0f19;
      --bg-card: #151d2f;
      --bg-accent: #1e293b;
      --border-color: #2e3d5b;
      --text-primary: #f8fafc;
      --text-secondary: #94a3b8;
      --primary: #38bdf8;
    }}
  }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    background: var(--bg-page);
    color: var(--text-primary);
    margin: 0;
    padding: 30px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }}
  h1 {{ font-size: 22px; margin-bottom: 24px; }}
  .diagram-wrapper {{
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 24px;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
    max-width: 900px;
    width: 100%;
  }}
  svg {{ width: 100%; height: auto; display: block; }}
</style>
</head>
<body>
<h1>{title}</h1>
<div class="diagram-wrapper">
{svg_content}
</div>
</body>
</html>
"""

def main() -> None:
    parser = argparse.ArgumentParser(description="Standalone Editorial SVG Diagram Generator")
    parser.add_argument("--type", "-t", choices=["architecture", "sequence"], default="architecture", help="Type of diagram")
    parser.add_argument("--title", default="System Architecture Diagram", help="Diagram title")
    parser.add_argument("--output", "-o", default="diagram.html", help="Output HTML filepath")

    args = parser.parse_args()
    svg = DIAGRAM_TEMPLATES.get(args.type, DIAGRAM_TEMPLATES["architecture"])
    html = render_standalone_html(args.title, svg)

    out_file = Path(args.output)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(html, encoding="utf-8")
    print(f"[diagram-design] Standalone SVG diagram generated at: {out_file}")

if __name__ == "__main__":
    main()
