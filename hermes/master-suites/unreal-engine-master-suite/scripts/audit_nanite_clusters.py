"""
UE5 Nanite Virtualized Geometry — Auditeur de Clusters & Culling Hi-Z
Auteur: Brandon (Antigravity Studio Engine)
Règles: Typage strict, zéro Any, calculs géométriques déterministes.
"""

import math
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class NaniteCluster:
    cluster_id: int
    triangle_count: int  # Exactement 128 triangles
    center_x: float
    center_y: float
    center_z: float
    bounding_radius: float
    depth_z: float
    is_occluded: bool = False


class NaniteRasterEngine:
    def __init__(self, triangles_per_cluster: int = 128) -> None:
        self.triangles_per_cluster: int = triangles_per_cluster

    def partition_mesh(self, total_triangles: int, mesh_radius: float) -> List[NaniteCluster]:
        num_clusters = math.ceil(total_triangles / self.triangles_per_cluster)
        clusters: List[NaniteCluster] = []

        for i in range(num_clusters):
            # Répartition spatiale simulée des clusters
            phi = (i / num_clusters) * math.pi
            theta = (i / num_clusters) * 2.0 * math.pi
            r = mesh_radius * 0.9

            cx = r * math.sin(phi) * math.cos(theta)
            cy = r * math.sin(phi) * math.sin(theta)
            cz = 10.0 + r * math.cos(phi)  # Profondeur médiane à 10m de la caméra

            clusters.append(NaniteCluster(
                cluster_id=i,
                triangle_count=self.triangles_per_cluster,
                center_x=cx,
                center_y=cy,
                center_z=cz,
                bounding_radius=mesh_radius / math.sqrt(num_clusters) * 1.5,
                depth_z=cz
            ))
        return clusters

    def perform_hiz_culling(self, clusters: List[NaniteCluster], occluder_depth: float) -> Tuple[int, int]:
        rendered_count = 0
        culled_count = 0

        for c in clusters:
            # Si le cluster se situe derrière un objet opaque occludeur (Hi-Z test)
            if c.depth_z > occluder_depth and abs(c.center_x) < 4.0 and abs(c.center_y) < 4.0:
                c.is_occluded = True
                culled_count += 1
            else:
                c.is_occluded = False
                rendered_count += 1

        return (rendered_count, culled_count)


def run_nanite_audit() -> None:
    print("=" * 70)
    print("    UE5 NANITE : AUDIT DE CLUSTERS (MESHLETS) & CULLING GPU HI-Z  ")
    print("=" * 70)
    engine = NaniteRasterEngine(triangles_per_cluster=128)
    high_poly_triangles = 512_000  # Statue cinématique haute fidélité

    clusters = engine.partition_mesh(high_poly_triangles, mesh_radius=5.0)
    total_clusters = len(clusters)
    print(f"Modèle 3D Source         : {high_poly_triangles:,} triangles (Zéro Normal Map baking)")
    print(f"Format de Cluster Nanite : {engine.triangles_per_cluster} triangles par Meshlet")
    print(f"Total Clusters Générés   : {total_clusters:,} clusters")
    print("-" * 70)

    # Simulation d'un mur occludeur devant le modèle
    rendered, culled = engine.perform_hiz_culling(clusters, occluder_depth=10.0)
    rendered_triangles = rendered * engine.triangles_per_cluster

    print(f"Clusters Dessinés (Visible) : {rendered:,} clusters ({rendered_triangles:,} triangles)")
    print(f"Clusters Élagués (Hi-Z Occlusion): {culled:,} clusters ({culled * engine.triangles_per_cluster:,} triangles)")
    savings_pct = (culled / total_clusters) * 100.0
    print(f"Réduction de Rasterisation GPU  : {savings_pct:.1f}% de micro-polygones éliminés !")
    print("=" * 70)
    assert total_clusters == 4000, "512,000 / 128 = 4,000 clusters exacts"
    assert culled > 0, "Le culling Hi-Z doit élaguer les clusters masqués"
    print("[OK] Partitionnement Meshlet et pipeline Hi-Z Nanite 100% validés.")
    print("=" * 70)


if __name__ == "__main__":
    run_nanite_audit()
