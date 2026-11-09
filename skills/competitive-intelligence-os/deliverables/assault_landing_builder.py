"""
Générateur de Landing Pages Comparatives d'Assaut (Guerrilla GTM).
Produit une page web HTML5 complète, responsive, stylisée avec Tailwind CSS.
Permet d'adresser directement les utilisateurs déçus d'un concurrent avec
tableau comparatif impartial, preuves vérifiées et bouton de migration 1-clic.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ComparisonFeatureRow:
    feature_name: str
    our_support: str  # ex: "✅ Inclus nativement (Local)"
    competitor_support: str  # ex: "❌ Option payante (+25 €/mois)"
    explanation: str


@dataclass(frozen=True)
class AssaultLandingSpec:
    our_brand_name: str
    competitor_brand_name: str
    target_sector: str
    hero_headline: str
    hero_subheadline: str
    call_to_action_text: str
    comparison_rows: list[ComparisonFeatureRow]
    killer_quote_verbatim: str
    quote_author_type: str


class AssaultLandingBuilder:
    """Générateur de pages web comparatives d'assaut."""

    @classmethod
    def generate_html(cls, spec: AssaultLandingSpec) -> str:
        """Génère le code HTML5 complet avec Tailwind CSS embarqué."""
        rows_html: list[str] = []
        for row in spec.comparison_rows:
            rows_html.append(
                f"""
                <tr class="border-b border-slate-700 hover:bg-slate-800/50 transition">
                    <td class="p-4 font-semibold text-white">{row.feature_name}</td>
                    <td class="p-4 text-emerald-400 font-bold bg-emerald-950/20">{row.our_support}</td>
                    <td class="p-4 text-rose-400 bg-rose-950/20">{row.competitor_support}</td>
                    <td class="p-4 text-slate-300 text-sm">{row.explanation}</td>
                </tr>
                """
            )

        rows_content = "\n".join(rows_html)

        html = f"""<!DOCTYPE html>
<html lang="fr" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pourquoi quitter {spec.competitor_brand_name} en 2026 ? | {spec.our_brand_name}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            darkMode: 'class',
            theme: {{
                extend: {{
                    colors: {{
                        brand: {{ 500: '#3b82f6', 600: '#2563eb', 700: '#1d4ed8' }}
                    }}
                }}
            }}
        }}
    </script>
</head>
<body class="bg-slate-950 text-slate-100 font-sans antialiased min-h-screen">
    <!-- Navigation -->
    <header class="border-b border-slate-800 py-4 px-6 flex justify-between items-center max-w-6xl mx-auto">
        <div class="text-xl font-bold tracking-tight text-white flex items-center gap-2">
            <span class="w-3 h-3 bg-blue-500 rounded-full inline-block"></span>
            {spec.our_brand_name}
        </div>
        <a href="#migration" class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-semibold transition">
            {spec.call_to_action_text}
        </a>
    </header>

    <!-- Hero Section -->
    <main class="max-w-5xl mx-auto px-6 py-16 text-center">
        <div class="inline-block bg-slate-800/80 border border-slate-700 px-3 py-1 rounded-full text-xs font-semibold text-blue-400 mb-6">
            Comparatif Transparent 2026 • Secteur {spec.target_sector}
        </div>
        <h1 class="text-4xl md:text-5xl font-extrabold tracking-tight text-white mb-6 leading-tight">
            {spec.hero_headline}
        </h1>
        <p class="text-lg md:text-xl text-slate-4xl text-slate-300 max-w-3xl mx-auto mb-10 leading-relaxed">
            {spec.hero_subheadline}
        </p>

        <!-- Témoignage Choc / Verbatim -->
        <div class="bg-slate-900 border border-slate-800 p-6 rounded-2xl max-w-2xl mx-auto mb-16 text-left shadow-xl">
            <p class="italic text-slate-300 mb-3">« {spec.killer_quote_verbatim} »</p>
            <div class="text-xs font-bold text-slate-400">— {spec.quote_author_type}</div>
        </div>

        <!-- Tableau Comparatif -->
        <div class="overflow-x-auto rounded-2xl border border-slate-800 bg-slate-900/60 shadow-2xl mb-16">
            <table class="w-full text-left border-collapse">
                <thead>
                    <tr class="border-b border-slate-700 bg-slate-800/70 text-xs font-bold uppercase tracking-wider text-slate-300">
                        <th class="p-4">Critère Clé</th>
                        <th class="p-4 text-emerald-400 bg-emerald-950/30">{spec.our_brand_name}</th>
                        <th class="p-4 text-rose-400 bg-rose-950/30">{spec.competitor_brand_name}</th>
                        <th class="p-4">Pourquoi c'est décisif</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_content}
                </tbody>
            </table>
        </div>

        <!-- Section Call-To-Action / Migration 1-Clic -->
        <section id="migration" class="bg-gradient-to-b from-blue-950/40 to-slate-900 border border-blue-900/50 p-10 rounded-3xl max-w-3xl mx-auto shadow-2xl">
            <h2 class="text-2xl md:text-3xl font-bold text-white mb-4">Passez chez nous en 60 secondes chrono</h2>
            <p class="text-slate-300 mb-8 max-w-xl mx-auto text-sm md:text-base">
                Importez vos devis, clients et catalogues depuis {spec.competitor_brand_name} sans rien retaper. Zéro engagement, zéro frais de dossier.
            </p>
            <div class="flex flex-col sm:flex-row gap-4 justify-center">
                <button class="bg-blue-600 hover:bg-blue-500 text-white font-bold py-3 px-8 rounded-xl shadow-lg transition">
                    Démarrer la migration gratuite
                </button>
                <button class="bg-slate-800 hover:bg-slate-700 text-slate-200 font-semibold py-3 px-6 rounded-xl border border-slate-700 transition">
                    Voir la démonstration vidéo (2 min)
                </button>
            </div>
        </section>
    </main>

    <!-- Footer -->
    <footer class="border-t border-slate-800 py-8 text-center text-xs text-slate-500">
        Données collectées selon le protocole SCIP Wisdom Gate à partir de sources publiques officielles et d'avis clients vérifiés.
    </footer>
</body>
</html>
"""
        return html

    @classmethod
    def export_to_file(cls, spec: AssaultLandingSpec, output_path: Path) -> Path:
        """Sauvegarde la page d'assaut dans un fichier HTML autonome."""
        html_content = cls.generate_html(spec)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(html_content, encoding="utf-8")
        return output_path
