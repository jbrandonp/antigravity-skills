"""
Générateur de Graphe de Connaissances Stratégiques Interactif (Knowledge Graph).
Produit un fichier HTML5 autonome visualisant le réseau d'interconnexions du marché :
concurrents, actionnaires communs, fournisseurs de données monopolistiques et passerelles bancaires.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class GraphNode:
    id: str
    label: str
    category: str  # 'competitor', 'investor_fund', 'critical_supplier', 'bank_gateway'
    color: str


@dataclass(frozen=True)
class GraphLink:
    source_id: str
    target_id: str
    relation_label: str


class KnowledgeGraphHTMLGenerator:
    """Générateur de visualisation interactive du graphe relationnel de marché."""

    @classmethod
    def generate_html(
        cls,
        title: str,
        nodes: list[GraphNode],
        links: list[GraphLink],
        output_path: Path,
    ) -> Path:
        """Génère un fichier HTML interactif avec rendu Canvas 2D."""
        nodes_data = [
            {"id": n.id, "label": n.label, "category": n.category, "color": n.color}
            for n in nodes
        ]
        links_data = [
            {"source": l.source_id, "target": l.target_id, "label": l.relation_label}
            for l in links
        ]

        html = f"""<!DOCTYPE html>
<html lang="fr" class="dark">
<head>
    <meta charset="UTF-8">
    <title>{title} | Graphe de Connaissance Marché</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-950 text-white font-sans antialiased flex flex-col h-screen overflow-hidden">
    <header class="p-4 border-b border-slate-800 flex justify-between items-center bg-slate-900/80">
        <h1 class="text-lg font-bold flex items-center gap-2">
            <span class="w-3 h-3 bg-purple-500 rounded-full"></span>
            {title}
        </h1>
        <div class="flex gap-4 text-xs font-semibold">
            <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 bg-blue-500 rounded-full"></span> Concurrents</span>
            <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 bg-rose-500 rounded-full"></span> Fournisseur Monopolistique</span>
            <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 bg-amber-500 rounded-full"></span> Actionnaire Commun</span>
        </div>
    </header>
    <div class="flex-1 relative">
        <canvas id="graphCanvas" class="w-full h-full block bg-slate-950"></canvas>
    </div>
    <script>
        const nodes = {json.dumps(nodes_data)};
        const links = {json.dumps(links_data)};

        const canvas = document.getElementById('graphCanvas');
        const ctx = canvas.getContext('2d');

        function resize() {{
            canvas.width = canvas.parentElement.clientWidth;
            canvas.height = canvas.parentElement.clientHeight;
            draw();
        }}
        window.addEventListener('resize', resize);

        // Positionnement circulaire initial
        const cx = window.innerWidth / 2;
        const cy = window.innerHeight / 2 - 30;
        const radius = Math.min(cx, cy) * 0.65;

        nodes.forEach((n, idx) => {{
            const angle = (2 * Math.PI / nodes.length) * idx;
            n.x = cx + radius * Math.cos(angle);
            n.y = cy + radius * Math.sin(angle);
        }});

        function draw() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Liens
            links.forEach(l => {{
                const s = nodes.find(n => n.id === l.source);
                const t = nodes.find(n => n.id === l.target);
                if (s && t) {{
                    ctx.beginPath();
                    ctx.moveTo(s.x, s.y);
                    ctx.lineTo(t.x, t.y);
                    ctx.strokeStyle = '#334155';
                    ctx.lineWidth = 1.5;
                    ctx.stroke();

                    // Label de relation
                    const mx = (s.x + t.x) / 2;
                    const my = (s.y + t.y) / 2;
                    ctx.fillStyle = '#64748b';
                    ctx.font = '10px sans-serif';
                    ctx.textAlign = 'center';
                    ctx.fillText(l.label, mx, my);
                }}
            }});

            // Nœuds
            nodes.forEach(n => {{
                ctx.beginPath();
                ctx.arc(n.x, n.y, 16, 0, 2 * Math.PI);
                ctx.fillStyle = n.color;
                ctx.fill();
                ctx.strokeStyle = '#ffffff';
                ctx.lineWidth = 2;
                ctx.stroke();

                ctx.fillStyle = '#f8fafc';
                ctx.font = 'bold 12px sans-serif';
                ctx.textAlign = 'center';
                ctx.fillText(n.label, n.x, n.y + 30);
            }});
        }}

        setTimeout(resize, 50);
    </script>
</body>
</html>
"""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(html, encoding="utf-8")
        return output_path
