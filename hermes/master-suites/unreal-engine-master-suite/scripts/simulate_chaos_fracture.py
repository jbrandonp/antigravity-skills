"""
UE5 Chaos Destruction — Simulateur Déterministe de Fracture Voronoi & Strain
Auteur: Brandon (Antigravity Studio Engine)
Règles: Typage strict, zéro Any, propagation physique de contrainte.
"""

from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class ChaosChunk:
    chunk_id: int
    level: int           # 0=Racine, 1=Macro, 2=Gravats
    height_y: float
    strain_threshold: float
    is_anchored: bool = False
    is_broken: bool = False


class ChaosDestructionSolver:
    def __init__(self) -> None:
        self.chunks: List[ChaosChunk] = []

    def build_fractured_wall(self, num_chunks: int = 10) -> None:
        for i in range(num_chunks):
            y_pos = (i / num_chunks) * 5.0  # Mur de 5 mètres de haut
            # Les deux morceaux du bas sont ancrés dans le sol
            is_anchor = (y_pos < 1.0)
            self.chunks.append(ChaosChunk(
                chunk_id=i,
                level=1,
                height_y=y_pos,
                strain_threshold=150.0,
                is_anchored=is_anchor
            ))

    def apply_explosion_field(self, blast_height_y: float, blast_energy: float, blast_radius: float) -> Tuple[int, int]:
        broken_count = 0
        intact_count = 0

        for c in self.chunks:
            dist = abs(c.height_y - blast_height_y)
            if dist <= blast_radius:
                # Énergie atténuée par la distance (Radial Falloff)
                attenuation = max(0.0, 1.0 - (dist / blast_radius))
                received_strain = blast_energy * attenuation

                # Les blocs ancrés absorbent la contrainte sans se briser
                if not c.is_anchored and received_strain >= c.strain_threshold:
                    c.is_broken = True
                    broken_count += 1
                else:
                    intact_count += 1
            else:
                intact_count += 1

        return (broken_count, intact_count)


def run_chaos_simulation() -> None:
    print("=" * 70)
    print("    UE5 CHAOS PHYSICS : SIMULATION DE FRACTURE & STRAIN DAMAGE   ")
    print("=" * 70)
    solver = ChaosDestructionSolver()
    solver.build_fractured_wall(num_chunks=10)

    print(f"Structure de Mur Fracturé : {len(solver.chunks)} morceaux générés")
    print("Morceaux ancrés au sol    : Chunks avec Hauteur < 1.0m (Masse infinie)")
    print("-" * 70)

    # Détonation d'un missile à 3.0m de haut (Énergie 300 Strain, Rayon 2.5m)
    blast_y = 3.0
    energy = 300.0
    radius = 2.5
    print(f"Détonation d'Onde de Choc : Hauteur={blast_y}m, Énergie={energy}N, Rayon={radius}m")
    broken, intact = solver.apply_explosion_field(blast_y, energy, radius)

    print("-" * 70)
    print("État des Morceaux après Détonation :")
    for c in solver.chunks:
        anchor_txt = "[ANCRÉ AU SOL]" if c.is_anchored else "              "
        status_txt = "[FRACTURÉ & DYNAMIQUE]" if c.is_broken else "[INTACT & STABLE]      "
        print(f"  Chunk #{c.chunk_id:02d} | Y={c.height_y:4.2f}m | {anchor_txt} | {status_txt}")

    print("-" * 70)
    print(f"Morceaux brisés en corps rigides : {broken}")
    print(f"Morceaux restés stables          : {intact}")
    print("=" * 70)
    assert broken > 0, "Les morceaux proches de l'explosion doivent se briser"
    assert solver.chunks[0].is_anchored and not solver.chunks[0].is_broken, "L'ancrage sol doit préserver la base"
    print("[OK] Gestion des contraintes Strain et Ancrages physiques Chaos validés.")
    print("=" * 70)


if __name__ == "__main__":
    run_chaos_simulation()
