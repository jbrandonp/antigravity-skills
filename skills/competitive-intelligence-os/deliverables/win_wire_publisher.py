"""
Générateur de Win-Wires Temps Réel pour l'Accélération Commerciale.
Conçu pour diffuser immédiatement les victoires contre des concurrents majeurs :
- Displaced Competitor (Concurrent évincé)
- ACV (Montant annuel du contrat en €)
- Cycle de vente (jours)
- Silver Bullet (L'argument massue décisif ayant scellé la signature)
- FUD Démantelé (Comment les objections du concurrent ont été neutralisées)
- Citations Verbatim de l'acheteur (Voix du client)
- Recommandation duplicable pour les autres commerciaux
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class WinWireEvent:
    deal_name: str
    target_industry: str
    acv_eur: float
    sales_cycle_days: int
    displaced_competitor: str
    sales_rep_name: str
    decisive_silver_bullet: str
    competitor_trap_neutralized: str
    landmines_avoided: list[str]
    buyer_verbatim_quote: str
    key_takeaway_for_team: str


class WinWirePublisher:
    """Générateur et formateur de Win-Wires exécutifs."""

    @classmethod
    def format_markdown(cls, event: WinWireEvent) -> str:
        """Produit un format Markdown ultra-visuel pour Slack, Teams ou l'intranet."""
        landmines_bullets = "\n".join(f"- ⚠️ {lm}" for lm in event.landmines_avoided)
        formatted_acv = f"{event.acv_eur:,.0f} €".replace(",", " ")

        return f"""# 🏆 WIN-WIRE : Victoire Majeure contre {event.displaced_competitor} !

> **Deal :** {event.deal_name} | **Secteur :** {event.target_industry} | **AE :** {event.sales_rep_name}  
> **Valeur (ACV) :** {formatted_acv} | **Cycle de vente :** {event.sales_cycle_days} jours

---

### 🥊 Concurrent Évincé
**{event.displaced_competitor}** a été remplacé / éliminé au profit de notre solution.

### 🎯 Le "Silver Bullet" Décisif
> *"{event.decisive_silver_bullet}"*

### 🛡️ Démantèlement du Piège Concurrent
{event.competitor_trap_neutralized}

### 💣 Mines du Terrain Évitées (Landmines)
{landmines_bullets}

### 🗣️ Verbatim Acheteur
> *"{event.buyer_verbatim_quote}"*

### 💡 Recommandation Duplicable pour l'Équipe Commerciale
**{event.key_takeaway_for_team}**

---
*Généré par Competitive Intelligence OS — Système d'aide à la décision stratégique.*
"""

    @classmethod
    def export_json(cls, event: WinWireEvent, output_path: Path) -> Path:
        """Exporte l'événement au format JSON pour ingestion webhook / CRM."""
        data = {
            "deal_name": event.deal_name,
            "target_industry": event.target_industry,
            "acv_eur": event.acv_eur,
            "sales_cycle_days": event.sales_cycle_days,
            "displaced_competitor": event.displaced_competitor,
            "sales_rep_name": event.sales_rep_name,
            "decisive_silver_bullet": event.decisive_silver_bullet,
            "competitor_trap_neutralized": event.competitor_trap_neutralized,
            "landmines_avoided": event.landmines_avoided,
            "buyer_verbatim_quote": event.buyer_verbatim_quote,
            "key_takeaway_for_team": event.key_takeaway_for_team,
        }
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        return output_path
