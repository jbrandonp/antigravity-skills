"""
Générateur de Magic Quadrant & Forrester Wave en SVG autonome.
Génère une matrice exécutive 2x2 vectorielle pure visualisant le positionnement
stratégique des acteurs du marché selon deux axes standards mondiaux :
- Axe X : Exhaustivité de la Vision (Completeness of Vision, 0-100)
- Axe Y : Capacité d'Exécution (Ability to Execute, 0-100)

Les 4 quadrants officiels sont :
- Leaders (Haut-Droit)
- Challengers (Haut-Gauche)
- Visionnaires (Bas-Droit)
- Acteurs de Niche (Bas-Gauche)
"""

from __future__ import annotations

import xml.sax.saxutils as xml_escape
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class QuadrantVendor:
    name: str
    vision_score: float  # 0.0 à 100.0
    execution_score: float  # 0.0 à 100.0
    tier: str  # 'leader', 'challenger', 'visionary', 'niche'
    is_our_solution: bool = False
    notes: str = ""


class MagicQuadrantSVGGenerator:
    """Générateur SVG autonome du Magic Quadrant de Gartner."""

    WIDTH: int = 900
    HEIGHT: int = 700
    MARGIN: int = 80

    @classmethod
    def generate_svg(
        cls,
        title: str,
        vendors: list[QuadrantVendor],
        output_path: Path,
    ) -> Path:
        """Génère le fichier SVG vectoriel autonome."""
        width = cls.WIDTH
        height = cls.HEIGHT
        margin = cls.MARGIN

        plot_w = width - 2 * margin
        plot_h = height - 2 * margin
        mid_x = margin + plot_w / 2
        mid_y = margin + plot_h / 2

        escaped_title = xml_escape.escape(title)

        elements: list[str] = [
            (
                f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
                f'width="{width}" height="{height}" style="background-color: #0b1120; font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif;">'
            ),
            "  <defs>",
            '    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">',
            '      <stop offset="0%" stop-color="#0f172a" />',
            '      <stop offset="100%" stop-color="#020617" />',
            "    </linearGradient>",
            '    <filter id="glowOurSolution" x="-30%" y="-30%" width="160%" height="160%">',
            '      <feGaussianBlur stdDeviation="6" result="blur" />',
            '      <feComposite in="SourceGraphic" in2="blur" operator="over" />',
            "    </filter>",
            "  </defs>",
            f'  <rect width="{width}" height="{height}" fill="url(#bgGrad)" />',
            # Titre principal
            f'  <text x="{margin}" y="45" font-size="20" font-weight="bold" fill="#f8fafc">{escaped_title}</text>',
            f'  <text x="{margin}" y="65" font-size="12" fill="#94a3b8">Matrice Stratégique Exécutive — Gartner Magic Quadrant Method</text>',
            # Zones des Quadrants
            # Challengers (Top-Left)
            f'  <rect x="{margin}" y="{margin}" width="{plot_w / 2}" height="{plot_h / 2}" fill="#1e293b" fill-opacity="0.25" stroke="#334155" stroke-width="1" />',
            f'  <text x="{margin + 20}" y="{margin + 30}" font-size="14" font-weight="bold" fill="#38bdf8">CHALLENGERS</text>',
            # Leaders (Top-Right)
            f'  <rect x="{mid_x}" y="{margin}" width="{plot_w / 2}" height="{plot_h / 2}" fill="#065f46" fill-opacity="0.15" stroke="#334155" stroke-width="1" />',
            f'  <text x="{width - margin - 110}" y="{margin + 30}" font-size="14" font-weight="bold" fill="#34d399">LEADERS</text>',
            # Niche Players (Bottom-Left)
            f'  <rect x="{margin}" y="{mid_y}" width="{plot_w / 2}" height="{plot_h / 2}" fill="#0f172a" fill-opacity="0.4" stroke="#334155" stroke-width="1" />',
            f'  <text x="{margin + 20}" y="{height - margin - 20}" font-size="14" font-weight="bold" fill="#94a3b8">NICHE PLAYERS</text>',
            # Visionaries (Bottom-Right)
            f'  <rect x="{mid_x}" y="{mid_y}" width="{plot_w / 2}" height="{plot_h / 2}" fill="#854d0e" fill-opacity="0.15" stroke="#334155" stroke-width="1" />',
            f'  <text x="{width - margin - 130}" y="{height - margin - 20}" font-size="14" font-weight="bold" fill="#fbbf24">VISIONARIES</text>',
            # Lignes d'axes médianes
            f'  <line x1="{mid_x}" y1="{margin}" x2="{mid_x}" y2="{height - margin}" stroke="#64748b" stroke-width="1.5" stroke-dasharray="4,4" />',
            f'  <line x1="{margin}" y1="{mid_y}" x2="{width - margin}" y2="{mid_y}" stroke="#64748b" stroke-width="1.5" stroke-dasharray="4,4" />',
            # Libellés des axes
            f'  <text x="{width / 2}" y="{height - 30}" font-size="13" font-weight="600" fill="#cbd5e1" text-anchor="middle">Exhaustivité de la Vision (Completeness of Vision) &rarr;</text>',
            f'  <text x="30" y="{height / 2}" font-size="13" font-weight="600" fill="#cbd5e1" text-anchor="middle" transform="rotate(-90, 30, {height / 2})">Capacité d\'Exécution (Ability to Execute) &rarr;</text>',
        ]

        # Tracé des acteurs
        for vendor in vendors:
            # Conversion scores (0-100) en pixels
            clamped_vis = max(0.0, min(100.0, vendor.vision_score))
            clamped_exec = max(0.0, min(100.0, vendor.execution_score))

            cx = margin + (clamped_vis / 100.0) * plot_w
            # L'axe Y SVG pointe vers le bas, donc 100 en haut et 0 en bas
            cy = (height - margin) - (clamped_exec / 100.0) * plot_h

            escaped_name = xml_escape.escape(vendor.name)

            if vendor.is_our_solution:
                # Surbrillance éclatante pour notre offre
                elements.append(
                    f'  <circle cx="{cx}" cy="{cy}" r="14" fill="#3b82f6" fill-opacity="0.3" filter="url(#glowOurSolution)" />'
                )
                elements.append(
                    f'  <circle cx="{cx}" cy="{cy}" r="8" fill="#2563eb" stroke="#60a5fa" stroke-width="2.5" />'
                )
                elements.append(
                    f'  <text x="{cx}" y="{cy - 14}" font-size="12" font-weight="bold" fill="#60a5fa" text-anchor="middle">{escaped_name} (NOUS)</text>'
                )
            else:
                tier_colors = {
                    "leader": "#10b981",
                    "challenger": "#38bdf8",
                    "visionary": "#f59e0b",
                    "niche": "#94a3b8",
                }
                dot_color = tier_colors.get(vendor.tier.lower(), "#94a3b8")

                elements.append(
                    f'  <circle cx="{cx}" cy="{cy}" r="6" fill="{dot_color}" stroke="#0f172a" stroke-width="1.5" />'
                )
                elements.append(
                    f'  <text x="{cx}" y="{cy - 10}" font-size="11" font-weight="500" fill="#e2e8f0" text-anchor="middle">{escaped_name}</text>'
                )

        elements.append("</svg>")
        svg_content = "\n".join(elements)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(svg_content, encoding="utf-8")
        return output_path
