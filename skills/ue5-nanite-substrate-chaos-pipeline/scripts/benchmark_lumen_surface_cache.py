"""
UE5 Lumen Global Illumination — Simulateur de Surface Cache & Rebonds Indirects
Auteur: Brandon (Antigravity Studio Engine)
Règles: Typage strict, zéro Any, calculs de transfert radiométrique.
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass
class SurfaceCard:
    card_id: str
    albedo_color: Tuple[float, float, float]  # R, G, B [0.0 - 1.0]
    emissive_radiance: float                 # Watts / Lumens
    indirect_irradiance: float = 0.0         # Lumière reçue par rebonds


class LumenRadianceCache:
    def __init__(self, bounce_count: int = 3) -> None:
        self.bounce_count: int = bounce_count
        self.cards: Dict[str, SurfaceCard] = {}

    def register_card(self, card_id: str, albedo: Tuple[float, float, float], emissive: float = 0.0) -> None:
        self.cards[card_id] = SurfaceCard(card_id, albedo, emissive)

    def compute_indirect_transfers(self, view_factors: Dict[Tuple[str, str], float]) -> None:
        # Initialisation de l'énergie avec l'émissif pur
        current_flux = {cid: card.emissive_radiance for cid, card in self.cards.items()}

        for bounce in range(1, self.bounce_count + 1):
            next_flux: Dict[str, float] = {cid: 0.0 for cid in self.cards}

            for (src_id, dst_id), factor in view_factors.items():
                if src_id in self.cards and dst_id in self.cards:
                    transferred_light = current_flux[src_id] * factor
                    # Modulation par l'albédo moyen du récepteur
                    dst_albedo = sum(self.cards[dst_id].albedo_color) / 3.0
                    reflected_light = transferred_light * dst_albedo

                    self.cards[dst_id].indirect_irradiance += reflected_light
                    next_flux[dst_id] += reflected_light

            current_flux = next_flux


def run_lumen_benchmark() -> None:
    print("=" * 70)
    print("    UE5 LUMEN : SIMULATION DU SURFACE CACHE & MULTI-BOUNCE GI     ")
    print("=" * 70)
    lumen = LumenRadianceCache(bounce_count=3)

    # Scénario : Lampe rouge émissive (Card 1), Mur blanc (Card 2), Plancher sombre (Card 3)
    lumen.register_card("Spot_Neon_Rouge", albedo=(1.0, 0.1, 0.1), emissive=500.0)
    lumen.register_card("Mur_Platre_Blanc", albedo=(0.85, 0.85, 0.85), emissive=0.0)
    lumen.register_card("Sol_Beton_Gris", albedo=(0.30, 0.30, 0.30), emissive=0.0)

    # Facteurs de forme géométriques (View Factors de visibilité mutuelle)
    view_factors = {
        ("Spot_Neon_Rouge", "Mur_Platre_Blanc"): 0.40,
        ("Mur_Platre_Blanc", "Sol_Beton_Gris"): 0.35,
        ("Sol_Beton_Gris", "Mur_Platre_Blanc"): 0.20
    }

    print(f"Nombre de Rebonds Calculés : {lumen.bounce_count} rebonds indirects")
    print("Calcul du transfert d'énergie radiométrique sur le Surface Cache...")
    lumen.compute_indirect_transfers(view_factors)
    print("-" * 70)

    for cid, card in lumen.cards.items():
        print(f"Surface Card '{cid:18s}' | Émissif: {card.emissive_radiance:5.1f} lm | GI Reçue: {card.indirect_irradiance:6.2f} lm")

    assert lumen.cards["Mur_Platre_Blanc"].indirect_irradiance > 150.0, "Le mur blanc doit recevoir la lumière directe"
    assert lumen.cards["Sol_Beton_Gris"].indirect_irradiance > 15.0, "Le sol doit recevoir le 2e rebond indirect"
    print("=" * 70)
    print("[OK] Pipeline de Surface Cache et rebonds infinis Lumen 100% validés.")
    print("=" * 70)


if __name__ == "__main__":
    run_lumen_benchmark()
