#!/usr/bin/env python3
"""Banner HTML/SVG Scaffold Generator with Safe-Zones.

Formats:
- og_image (1200x630)
- twitter_header (1500x500)
- linkedin_banner (1584x396)
- youtube_banner (2560x1440)
"""
from __future__ import annotations
import argparse
from pathlib import Path
import sys

PRESETS = {
    "og": (1200, 630, "OpenGraph Social Preview"),
    "twitter": (1500, 500, "Twitter/X Header Banner"),
    "linkedin": (1584, 396, "LinkedIn Company Banner"),
    "youtube": (2560, 1440, "YouTube Channel Header")
}

def generate_banner_html(preset_key: str, title: str, subtitle: str, out_file: Path):
    w, h, desc = PRESETS.get(preset_key, (1200, 630, "Custom Banner"))
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    width: {w}px;
    height: {h}px;
    background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    color: #f8fafc;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: flex-start;
    padding: {int(h * 0.15)}px {int(w * 0.1)}px;
    overflow: hidden;
    position: relative;
  }}
  .badge {{
    background: rgba(99, 102, 241, 0.2);
    border: 1px solid rgba(129, 140, 248, 0.4);
    color: #a5b4fc;
    padding: 6px 16px;
    border-radius: 9999px;
    font-size: 14px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 20px;
  }}
  h1 {{
    font-size: {int(h * 0.12)}px;
    font-weight: 800;
    line-height: 1.1;
    margin-bottom: 16px;
    background: linear-gradient(to right, #ffffff, #cbd5e1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    max-width: 85%;
  }}
  p {{
    font-size: {int(h * 0.055)}px;
    color: #94a3b8;
    max-width: 75%;
    line-height: 1.5;
  }}
</style>
</head>
<body>
  <div class="badge">{desc}</div>
  <h1>{title}</h1>
  <p>{subtitle}</p>
</body>
</html>"""
    out_file.write_text(html, encoding="utf-8")
    print(f"✓ Generated banner HTML ({w}x{h}): {out_file}")

def main() -> int:
    parser = argparse.ArgumentParser(description="Banner Scaffold Generator")
    parser.add_argument("--preset", choices=list(PRESETS.keys()), default="og", help="Preset format")
    parser.add_argument("--title", default="Autonomous AI Engineering", help="Banner title")
    parser.add_argument("--subtitle", default="Deterministic tooling, zero Docker, SOTA performance.", help="Banner subtitle")
    parser.add_argument("--out", default="banner.html", help="Output HTML file")
    args = parser.parse_args()

    generate_banner_html(args.preset, args.title, args.subtitle, Path(args.out))
    return 0

if __name__ == "__main__":
    sys.exit(main())
