"""
Traceur vectoriel SVG autonome pour matrices 2x2 et diagrammes radar 6 axes.
Ne nécessite aucune dépendance graphique externe (ni matplotlib, ni cairo).
Produit du code SVG épuré, compatible Obsidian et navigateurs web.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape


@dataclass(frozen=True)
class PositioningEntity:
    label: str
    x_val: float  # Échelle de 0.0 à 10.0
    y_val: float  # Échelle de 0.0 à 10.0
    color: str
    is_hero: bool = False


@dataclass(frozen=True)
class RadarDimensionScore:
    dimension_name: str
    score: float  # Échelle de 0.0 à 10.0


@dataclass(frozen=True)
class RadarEntity:
    label: str
    color: str
    dimensions: list[RadarDimensionScore]
    is_hero: bool = False


class SVGPositioningPlotter:
    """Générateur de graphiques SVG pour la matrice 2x2."""

    @classmethod
    def render_2x2_matrix(
        cls,
        x_axis_label: str,
        y_axis_label: str,
        entities: list[PositioningEntity],
        output_path: Path,
    ) -> Path:
        """Génère un fichier SVG 600x600 représentant la matrice de positionnement."""
        width = 600
        height = 600
        pad = 70
        cx = width / 2
        cy = height / 2

        esc_x = xml_escape(x_axis_label)
        esc_y = xml_escape(y_axis_label)
        svg: list[str] = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">',
            '  <rect width="100%" height="100%" fill="#1a1b26" rx="12"/>',
            '  <!-- Grille et Axes -->',
            f'  <line x1="{pad}" y1="{cy}" x2="{width - pad}" y2="{cy}" stroke="#414868" stroke-width="2"/>',
            f'  <line x1="{cx}" y1="{pad}" x2="{cx}" y2="{height - pad}" stroke="#414868" stroke-width="2"/>',
            f'  <text x="{width - pad}" y="{cy - 12}" fill="#c0caf5" font-family="sans-serif" font-size="12" text-anchor="end">{esc_x} →</text>',
            f'  <text x="{cx + 12}" y="{pad + 12}" fill="#c0caf5" font-family="sans-serif" font-size="12" text-anchor="start">↑ {esc_y}</text>',
        ]

        plot_w = width - (2 * pad)
        plot_h = height - (2 * pad)

        for e in entities:
            px = pad + (e.x_val / 10.0) * plot_w
            py = (height - pad) - (e.y_val / 10.0) * plot_h
            radius = 9 if e.is_hero else 6
            stroke = "#ffffff" if e.is_hero else "#000000"
            stroke_w = "2.5" if e.is_hero else "1"
            esc_label = xml_escape(e.label)

            svg.append(
                f'  <circle cx="{px}" cy="{py}" r="{radius}" fill="{e.color}" stroke="{stroke}" stroke-width="{stroke_w}"/>'
            )
            svg.append(
                f'  <text x="{px + 12}" y="{py + 4}" fill="#ffffff" font-weight="{"bold" if e.is_hero else "normal"}" '
                f'font-family="sans-serif" font-size="11">{esc_label}</text>'
            )

        svg.append("</svg>")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text("\n".join(svg), encoding="utf-8")
        return output_path


class SVGRadarPlotter:
    """Générateur de graphiques Radar (Spider Chart) en SVG pur à 6 axes."""

    @classmethod
    def render_radar_chart(
        cls,
        title: str,
        dimension_names: list[str],
        entities: list[RadarEntity],
        output_path: Path,
    ) -> Path:
        """Génère un diagramme radar polygonal équilibré."""
        width = 650
        height = 650
        cx = width / 2
        cy = height / 2
        radius = 200
        num_vars = len(dimension_names)

        esc_title = xml_escape(title)
        svg: list[str] = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">',
            '  <rect width="100%" height="100%" fill="#1a1b26" rx="12"/>',
            f'  <text x="{cx}" y="45" fill="#c0caf5" font-family="sans-serif" font-size="16" font-weight="bold" text-anchor="middle">{esc_title}</text>',
        ]

        # Cercles concentriques (25%, 50%, 75%, 100%)
        for level in [0.25, 0.50, 0.75, 1.0]:
            r_level = radius * level
            svg.append(
                f'  <circle cx="{cx}" cy="{cy}" r="{r_level}" fill="none" stroke="#414868" stroke-width="1" stroke-dasharray="3,3"/>'
            )

        # Axes radiants et libellés
        angles: list[float] = []
        for i, dim_name in enumerate(dimension_names):
            angle = (2 * math.pi / num_vars) * i - (math.pi / 2)
            angles.append(angle)
            ax = cx + radius * math.cos(angle)
            ay = cy + radius * math.sin(angle)
            svg.append(f'  <line x1="{cx}" y1="{cy}" x2="{ax}" y2="{ay}" stroke="#414868" stroke-width="1.5"/>')

            # Décalage du texte
            tx = cx + (radius + 25) * math.cos(angle)
            ty = cy + (radius + 25) * math.sin(angle) + 4
            anchor = "middle"
            if math.cos(angle) > 0.3:
                anchor = "start"
            elif math.cos(angle) < -0.3:
                anchor = "end"

            esc_dim = xml_escape(dim_name)
            svg.append(
                f'  <text x="{tx}" y="{ty}" fill="#a9b1d6" font-family="sans-serif" font-size="11" text-anchor="{anchor}">{esc_dim}</text>'
            )

        # Tracé des polygones par entité
        for entity in entities:
            score_map = {d.dimension_name: d.score for d in entity.dimensions}
            points: list[str] = []
            for i, dim_name in enumerate(dimension_names):
                score = score_map.get(dim_name, 0.0)
                r_score = radius * (min(10.0, max(0.0, score)) / 10.0)
                px = cx + r_score * math.cos(angles[i])
                py = cy + r_score * math.sin(angles[i])
                points.append(f"{px:.1f},{py:.1f}")

            poly_pts = " ".join(points)
            fill_opacity = "0.35" if entity.is_hero else "0.15"
            stroke_width = "3" if entity.is_hero else "1.5"

            svg.append(
                f'  <polygon points="{poly_pts}" fill="{entity.color}" fill-opacity="{fill_opacity}" stroke="{entity.color}" stroke-width="{stroke_width}"/>'
            )

        svg.append("</svg>")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text("\n".join(svg), encoding="utf-8")
        return output_path
