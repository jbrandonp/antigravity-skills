#!/usr/bin/env python3
"""LinkedIn Carousel HTML/PDF Generator (1080x1350 ratio 4:5).

Generates standalone pixel-perfect HTML slides ready for headless PDF export via:
  chrome --headless --print-to-pdf=carousel.pdf carousel.html
"""

from __future__ import annotations

import argparse
import html
import json
import sys
from typing import Dict, List, Optional

THEMES: Dict[str, Dict[str, str]] = {
    "developer-dark": {
        "bg_cover": "radial-gradient(circle at top right, #0284c7, #0f172a 70%)",
        "bg_slide": "radial-gradient(circle at top right, #1e293b, #0f172a)",
        "accent": "#38bdf8",
        "text_title": "#ffffff",
        "text_body": "#cbd5e1",
        "footer_color": "#64748b",
        "border_color": "rgba(255, 255, 255, 0.1)",
        "font_family": '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
    },
    "clean-light": {
        "bg_cover": "linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%)",
        "bg_slide": "#ffffff",
        "accent": "#2563eb",
        "text_title": "#0f172a",
        "text_body": "#334155",
        "footer_color": "#94a3b8",
        "border_color": "rgba(0, 0, 0, 0.08)",
        "font_family": '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
    },
    "brutalist": {
        "bg_cover": "#000000",
        "bg_slide": "#09090b",
        "accent": "#ccff00",
        "text_title": "#ffffff",
        "text_body": "#f4f4f5",
        "footer_color": "#71717a",
        "border_color": "#27272a",
        "font_family": 'ui-monospace, "SF Mono", Menlo, Consolas, monospace',
    },
    "executive-slate": {
        "bg_cover": "radial-gradient(circle at top right, #3f3f46, #18181b 75%)",
        "bg_slide": "radial-gradient(circle at top right, #27272a, #18181b)",
        "accent": "#f59e0b",
        "text_title": "#fafafa",
        "text_body": "#d4d4d8",
        "footer_color": "#71717a",
        "border_color": "rgba(255, 255, 255, 0.08)",
        "font_family": 'Georgia, Cambria, "Times New Roman", Times, serif',
    },
}


def build_slide_html(
    slide_num: int,
    total_slides: int,
    title: str,
    body: str,
    category: str = "GUIDE TECHNIQUE",
    author: str = "@jbrandonp",
    is_cover: bool = False,
    is_recap: bool = False,
    theme: str = "developer-dark",
) -> str:
    """Builds a single 1080x1350 slide section."""
    th = THEMES.get(theme, THEMES["developer-dark"])
    bg_gradient = th["bg_cover"] if is_cover else th["bg_slide"]
    title_size = "68px" if is_cover else ("48px" if is_recap else "56px")
    accent_color = th["accent"]

    escaped_title = html.escape(title)
    escaped_body = html.escape(body).replace("\n", "<br>")

    recap_extra = ""
    if is_recap:
        recap_extra = f"<div style='margin-top:20px; font-size:24px; color:{accent_color};'>📸 Capturez cette slide pour plus tard</div>"

    return f"""
  <section class="slide" style="background: {bg_gradient}; font-family: {th['font_family']};">
    <div class="slide-header" style="color: {accent_color};">
      <span>{html.escape(category)}</span>
      <span>{slide_num}/{total_slides}</span>
    </div>
    <div class="slide-content">
      <h1 style="font-size: {title_size}; color: {th['text_title']};">{escaped_title}</h1>
      <p style="color: {th['text_body']};">{escaped_body}</p>
      {recap_extra}
    </div>
    <div class="slide-footer" style="color: {th['footer_color']}; border-color: {th['border_color']};">
      <span>{html.escape(author)}</span>
      <span>{'→' if slide_num < total_slides else 'FIN'}</span>
    </div>
  </section>
"""


def generate_carousel(
    slides_data: List[Dict[str, str]],
    author: str = "@jbrandonp",
    category: str = "INGÉNIERIE & CODE",
    theme: str = "developer-dark",
) -> str:
    """Generates the complete multi-slide HTML document."""
    total = len(slides_data)
    sections: List[str] = []

    for idx, slide in enumerate(slides_data, start=1):
        is_cov = idx == 1 or slide.get("is_cover", False)
        is_rec = idx == total - 1 or slide.get("is_recap", False)
        sections.append(
            build_slide_html(
                slide_num=idx,
                total_slides=total,
                title=slide.get("title", f"Point {idx}"),
                body=slide.get("body", ""),
                category=slide.get("category", category),
                author=author,
                is_cover=is_cov,
                is_recap=is_rec,
                theme=theme,
            )
        )

    all_sections = "\n".join(sections)
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>LinkedIn Carousel</title>
<style>
  @page {{
    size: 1080px 1350px;
    margin: 0;
  }}
  * {{
    box-sizing: border-box;
  }}
  body {{
    margin: 0;
    padding: 0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    color: #f8fafc;
    background: #000;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }}
  .slide {{
    width: 1080px;
    height: 1350px;
    page-break-after: always;
    break-after: page;
    padding: 100px 90px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    position: relative;
    overflow: hidden;
  }}
  .slide-header {{
    font-size: 26px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 2px;
    display: flex;
    justify-content: space-between;
  }}
  .slide-content h1 {{
    line-height: 1.15;
    margin: 0 0 35px 0;
    font-weight: 800;
    letter-spacing: -1px;
    color: #ffffff;
  }}
  .slide-content p {{
    font-size: 34px;
    line-height: 1.45;
    color: #cbd5e1;
    margin: 0;
    max-width: 900px;
  }}
  .slide-footer {{
    display: flex;
    justify-content: space-between;
    font-size: 24px;
    color: #64748b;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    padding-top: 30px;
    font-weight: 600;
  }}
</style>
</head>
<body>
{all_sections}
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a 1080x1350 LinkedIn carousel HTML.")
    parser.add_argument("--slides", help="JSON file or raw JSON string defining slides")
    parser.add_argument("--output", "-o", default="carousel.html", help="Output HTML file path")
    parser.add_argument("--author", default="@jbrandonp", help="Author handle on footer")
    parser.add_argument("--category", default="ARCHITECTURE LOGICIELLE", help="Category tag on header")
    parser.add_argument(
        "--theme",
        choices=["developer-dark", "clean-light", "brutalist", "executive-slate"],
        default="developer-dark",
        help="Visual theme styling for slides (default: developer-dark)",
    )
    args = parser.parse_args()

    slides: List[Dict[str, str]] = []
    if args.slides:
        try:
            with open(args.slides, "r", encoding="utf-8") as f:
                slides = json.loads(f.read())
        except Exception:
            try:
                slides = json.loads(args.slides)
            except Exception as e:
                print(f"Error parsing slides JSON: {e}", file=sys.stderr)
                return 1
    else:
        # Default sample carousel
        slides = [
            {
                "title": "Pourquoi SQLite bat PostgreSQL en local.",
                "body": "Et comment économiser 400 €/mois d'infrastructure sans perdre 1 transaction.",
            },
            {
                "title": "Le piège de la sur-ingénierie.",
                "body": "90 % des applications internes ont moins de 100 utilisateurs simultanés. Pourquoi déployer un cluster managé ?",
            },
            {
                "title": "Le secret : Le mode WAL.",
                "body": "En activant Write-Ahead Logging (WAL), les lectures ne bloquent plus les écritures. Latence médiane : 0.4 ms.",
            },
            {
                "title": "Ce qu'on a mesuré en production.",
                "body": "140 000 écritures par jour. Zéro corruption. Une facture d'infra réduite à 14 € sur Hetzner.",
            },
            {
                "title": "En résumé (À garder).",
                "body": "1. SQLite WAL encaisse 10k req/s\n2. Zéro latence réseau\n3. Sauvegarde en 1 fichier .db\n4. Simplicité absolue.",
            },
            {
                "title": "Besoin de simplifier votre stack ?",
                "body": "Je documente nos architectures locales en open-source. Le code du benchmark est sur mon GitHub.",
            },
        ]

    html_content = generate_carousel(slides, author=args.author, category=args.category, theme=args.theme)
    try:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"Carousel HTML généré avec succès dans : {args.output} ({len(slides)} slides)")
        return 0
    except Exception as e:
        print(f"Erreur d'écriture : {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
