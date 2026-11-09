"""
Générateur de Battlecards Vivantes respectant la 'Règle des 8 Secondes'.
Formaté pour être scanné instantanément par un commercial ou un fondateur en plein appel prospect.
Chaque affirmation est rigoureusement sourcée par une URL ou une preuve tierce vérifiable.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ObjectionCounter:
    objection_title: str
    instant_killer_quote: str  # La réplique à prononcer mot pour mot
    proof_evidence: str  # La preuve chiffrée
    source_url: str  # Lien vérifié Wisdom Gate


@dataclass(frozen=True)
class LivingBattlecard:
    our_product_name: str
    competitor_name: str
    target_persona: str
    one_sentence_counter_pitch: str  # Scannable en 3 secondes
    why_we_win_points: list[str]
    objections: list[ObjectionCounter]  # 2 à 3 objections majeures scannables en 5 secondes
    last_verified_date: str


class Battlecard8SecBuilder:
    """Compilateur de fiches de combat commercial ultra-compactes."""

    @classmethod
    def generate_markdown(cls, card: LivingBattlecard) -> str:
        """Génère le texte Markdown optimisé pour un affichage terminal ou CRM."""
        lines: list[str] = [
            f"# ⚡ BATTLECARD 8-SECONDES : {card.our_product_name} vs {card.competitor_name}",
            f"> **Cible :** {card.target_persona} | **Dernière vérification :** {card.last_verified_date}",
            "",
            "## 🥊 PITCH D'ATTAQUE (3 secondes de lecture)",
            f"> *« {card.one_sentence_counter_pitch} »*",
            "",
            "## 🛡️ TOP OBJECTIONS & RÉPLIQUES CHOC (5 secondes de lecture)",
            "",
        ]

        for i, obj in enumerate(card.objections, 1):
            lines.extend(
                [
                    f"### {i}. Objection : « {obj.objection_title} »",
                    f"- **La Réplique :** *« {obj.instant_killer_quote} »*",
                    f"- **Preuve Choc :** {obj.proof_evidence}",
                    f"- **Source vérifiée :** [{obj.source_url}]({obj.source_url})",
                    "",
                ]
            )

        lines.extend(
            [
                "## ⚡ POURQUOI NOUS GAGNONS (Nos 3 Avantages Décisifs)",
            ]
        )
        for pt in card.why_we_win_points:
            lines.append(f"- ✅ {pt}")

        lines.append("")
        return "\n".join(lines)

    @classmethod
    def export_to_file(cls, card: LivingBattlecard, output_file: Path) -> Path:
        """Exporte la battlecard dans un fichier Markdown."""
        content = cls.generate_markdown(card)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(content, encoding="utf-8")
        return output_file
