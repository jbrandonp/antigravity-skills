"""
Générateur vectoriel SVG de Cartes de Wardley (Wardley Mapping).
Permet de visualiser la chaîne de valeur ancrée sur le besoin utilisateur
et d'identifier la doctrine stratégique de 'Commoditisation du complémentaire'.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape


@dataclass(frozen=True)
class WardleyComponent:
    id: str
    name: str
    evolution_stage: float  # Entre 0.0 (Genèse) et 1.0 (Commodité/Standard)
    visibility_level: float  # Entre 0.0 (Invisible/Infra) et 1.0 (Directement visible par l'utilisateur)
    is_our_disruption: bool = False
    is_competitor_revenue_driver: bool = False


@dataclass(frozen=True)
class WardleyDependency:
    source_id: str
    target_id: str


class WardleyMapperSVG:
    """Générateur de cartes de Wardley au format SVG pur."""

    @classmethod
    def render_map(
        cls,
        map_title: str,
        components: list[WardleyComponent],
        dependencies: list[WardleyDependency],
        output_path: Path,
    ) -> Path:
        """Génère une carte de Wardley vectorielle de 800x550 pixels."""
        width = 800
        height = 550
        pad_x = 80
        pad_y = 60
        graph_w = width - (2 * pad_x)
        graph_h = height - (2 * pad_y)

        esc_title = xml_escape(map_title)
        svg: list[str] = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">',
            '  <rect width="100%" height="100%" fill="#1a1b26" rx="12"/>',
            f'  <text x="{width / 2}" y="35" fill="#c0caf5" font-family="sans-serif" font-size="16" font-weight="bold" text-anchor="middle">{esc_title}</text>',
            '  <!-- Lignes des 4 phases d\'évolution -->',
        ]

        # 4 zones d'évolution
        stages = ["Genèse", "Sur-mesure", "Produit (+Locatif)", "Commodité (+Utilitaire)"]
        stage_w = graph_w / 4.0

        for idx, stage_name in enumerate(stages):
            sx = pad_x + (idx * stage_w)
            svg.append(f'  <line x1="{sx}" y1="{pad_y}" x2="{sx}" y2="{height - pad_y}" stroke="#292e42" stroke-width="1.5" stroke-dasharray="4,4"/>')
            svg.append(
                f'  <text x="{sx + (stage_w / 2)}" y="{height - pad_y + 25}" fill="#7aa2f7" font-family="sans-serif" font-size="12" text-anchor="middle">{stage_name}</text>'
            )

        # Axes
        svg.append(f'  <line x1="{pad_x}" y1="{height - pad_y}" x2="{width - pad_x}" y2="{height - pad_y}" stroke="#414868" stroke-width="2"/>')
        svg.append(f'  <line x1="{pad_x}" y1="{pad_y}" x2="{pad_x}" y2="{height - pad_y}" stroke="#414868" stroke-width="2"/>')
        svg.append(f'  <text x="{width - pad_x}" y="{height - pad_y + 45}" fill="#a9b1d6" font-family="sans-serif" font-size="11" text-anchor="end">Évolution (Maturité) →</text>')
        svg.append(f'  <text x="{pad_x - 12}" y="{pad_y - 12}" fill="#a9b1d6" font-family="sans-serif" font-size="11" text-anchor="start">↑ Visibilité Utilisateur (Chaîne de Valeur)</text>')

        # Positionnement des composants
        pos_map: dict[str, tuple[float, float]] = {}
        for c in components:
            cx = pad_x + (c.evolution_stage * graph_w)
            cy = (height - pad_y) - (c.visibility_level * graph_h)
            pos_map[c.id] = (cx, cy)

        # Tracé des dépendances
        for dep in dependencies:
            if dep.source_id in pos_map and dep.target_id in pos_map:
                x1, y1 = pos_map[dep.source_id]
                x2, y2 = pos_map[dep.target_id]
                svg.append(f'  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#565f89" stroke-width="1.5"/>')

        # Tracé des nœuds
        for c in components:
            cx, cy = pos_map[c.id]
            node_color = "#f7768e" if c.is_competitor_revenue_driver else ("#9ece6a" if c.is_our_disruption else "#7aa2f7")
            radius = 7
            esc_name = xml_escape(c.name)

            svg.append(f'  <circle cx="{cx}" cy="{cy}" r="{radius}" fill="{node_color}" stroke="#ffffff" stroke-width="1.5"/>')
            svg.append(
                f'  <text x="{cx + 10}" y="{cy + 4}" fill="#ffffff" font-family="sans-serif" font-size="11" font-weight="bold">{esc_name}</text>'
            )

        svg.append("</svg>")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text("\n".join(svg), encoding="utf-8")
        return output_path
