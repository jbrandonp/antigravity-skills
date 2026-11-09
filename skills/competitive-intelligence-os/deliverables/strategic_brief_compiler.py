"""
Compilateur de la Note Stratégique Décisionnelle (Executive Brief).
Applique le 'Strategic Kernel' de Richard Rumelt (Good Strategy / Bad Strategy)
et le protocole d'avocat du diable / Premortem de Gary Klein.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class RumeltKernel:
    brutal_diagnosis: str  # L'obstacle central unique et inavoué
    guiding_policy: str  # La doctrine générale de contournement
    coherent_action_steps: list[str]  # Les actions coordonnées qui se renforcent mutuellement


@dataclass(frozen=True)
class StrategicBrief:
    title: str
    target_sector: str
    key_intelligence_questions: list[str]
    rumelt_kernel: RumeltKernel
    premortem_risks: list[str]
    primary_adversaries: list[str]
    wisdom_gate_compliance_statement: str


class StrategicBriefCompiler:
    """Compilateur du One-Pager de direction stratégique."""

    @classmethod
    def compile_markdown(cls, brief: StrategicBrief) -> str:
        """Produit le document Markdown décisionnel prêt pour le comité de direction."""
        lines: list[str] = [
            f"# 🧭 NOTE DE DÉCISION STRATÉGIQUE : {brief.title}",
            f"> **Secteur :** {brief.target_sector} | **Gouvernance :** Standard SCIP & Valona World-Class",
            "",
            "## 🎯 1. Key Intelligence Questions (KIQs Directrices)",
        ]
        for kiq in brief.key_intelligence_questions:
            lines.append(f"- **KIQ :** *« {kiq} »*")

        lines.extend([
            "",
            "## 🏛️ 2. Le Noyau Stratégique (The Rumelt Kernel)",
            "### A. Le Diagnostic Brutal (L'Obstacle Central)",
            f"> {brief.rumelt_kernel.brutal_diagnosis}",
            "",
            "### B. La Politique Directrice (L'Angle d'Attaque)",
            f"> {brief.rumelt_kernel.guiding_policy}",
            "",
            "### C. Le Plan d'Actions Cohérentes (Synergie Mutuelle)",
        ])

        for i, step in enumerate(brief.rumelt_kernel.coherent_action_steps, 1):
            lines.append(f"{i}. **{step}**")

        lines.extend([
            "",
            "## ⚠️ 3. L'Avocat du Diable : Le Rapport de Premortem (Gary Klein)",
            "> *« Nous sommes dans 2 ans. Notre projet a fait faillite totale. Voici l'histoire exacte de ce qui s'est passé : »*",
            "",
        ])
        for risk in brief.premortem_risks:
            lines.append(f"- 🔴 **Facteur d'échec anticipé :** {risk}")

        lines.extend([
            "",
            "## ⚔️ 4. Adversaires Sous Surveillance Rapprochée (Règle des 3 Cercles)",
        ])
        for adv in brief.primary_adversaries:
            lines.append(f"- 🎯 {adv}")

        lines.extend([
            "",
            "## 🛡️ 5. Conformité & Traçabilité Wisdom Gate",
            f"> {brief.wisdom_gate_compliance_statement}",
            "",
        ])

        return "\n".join(lines)

    @classmethod
    def export_to_file(cls, brief: StrategicBrief, output_path: Path) -> Path:
        """Sauvegarde la note de décision sur le disque."""
        content = cls.compile_markdown(brief)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content, encoding="utf-8")
        return output_path
