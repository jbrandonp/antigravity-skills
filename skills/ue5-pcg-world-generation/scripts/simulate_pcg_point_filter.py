# -*- coding: utf-8 -*-
"""
simulate_pcg_point_filter.py - Unreal Engine 5 PCG Point Filter Simulator
Simulateur d'echantillonnage spatial et de filtrage par disque de Poisson
pour le placement procedurale de vegetation.
"""

import math
import random
from typing import List, Dict, Tuple, TypedDict

class PCGPoint(TypedDict):
    point_id: int
    pos_x: float
    pos_y: float
    pos_z: float
    slope_angle: float
    scale: float

class PCGExecutionReport(TypedDict):
    initial_points: int
    filtered_slope_points: int
    poisson_final_points: int
    rejection_rate_percent: float

def generate_raw_points(count: int, bounds_size: float = 100.0) -> List[PCGPoint]:
    """Genere une grille de points brute avec pentes simulees."""
    points: List[PCGPoint] = []
    rng = random.Random(42)  # Graine deterministe

    for idx in range(count):
        x = rng.uniform(0.0, bounds_size)
        y = rng.uniform(0.0, bounds_size)
        # Altitude simulee avec colline au centre
        dist_from_center = math.sqrt((x - 50.0)**2 + (y - 50.0)**2)
        z = math.sin(dist_from_center * 0.1) * 20.0
        # Pente proportionnelle au gradient
        slope = min(90.0, abs(math.cos(dist_from_center * 0.1) * 20.0 * 0.1) * 57.29)

        points.append({
            "point_id": idx,
            "pos_x": x,
            "pos_y": y,
            "pos_z": z,
            "slope_angle": slope,
            "scale": rng.uniform(0.8, 1.2)
        })
    return points

def filter_by_slope_and_poisson(
    points: List[PCGPoint],
    max_slope: float = 40.0,
    min_distance: float = 5.0
) -> Tuple[List[PCGPoint], PCGExecutionReport]:
    """Applique le filtre d'inclinaison de pente et le filtrage Poisson Disk."""
    # 1. Filtre de pente
    slope_valid = [p for p in points if p["slope_angle"] <= max_slope]

    # 2. Filtre Poisson Disk glouton
    accepted_points: List[PCGPoint] = []
    min_dist_sq = min_distance * min_distance

    for cand in slope_valid:
        is_too_close = False
        for acc in accepted_points:
            dx = cand["pos_x"] - acc["pos_x"]
            dy = cand["pos_y"] - acc["pos_y"]
            dist_sq = dx * dx + dy * dy
            if dist_sq < min_dist_sq:
                is_too_close = True
                break
        if not is_too_close:
            accepted_points.append(cand)

    report: PCGExecutionReport = {
        "initial_points": len(points),
        "filtered_slope_points": len(slope_valid),
        "poisson_final_points": len(accepted_points),
        "rejection_rate_percent": ((len(points) - len(accepted_points)) / len(points)) * 100.0
    }
    return accepted_points, report

def run_self_test() -> int:
    """Verifie le bon fonctionnement du simulateur PCG."""
    print("Execution du self-test PCG Framework UE5...")
    raw = generate_raw_points(count=300, bounds_size=100.0)
    filtered, report = filter_by_slope_and_poisson(raw, max_slope=35.0, min_distance=6.0)

    assert len(filtered) > 0, "No points remained after PCG filtering!"
    for p in filtered:
        assert p["slope_angle"] <= 35.0, f"Slope violation: {p['slope_angle']}"

    # Verifier distance minimale entre tous les points retenus
    min_dist_sq = 6.0 * 6.0
    for i in range(len(filtered)):
        for j in range(i + 1, len(filtered)):
            dx = filtered[i]["pos_x"] - filtered[j]["pos_x"]
            dy = filtered[i]["pos_y"] - filtered[j]["pos_y"]
            assert (dx * dx + dy * dy) >= (min_dist_sq - 0.001), "Poisson distance violation!"

    print(f"[PASS] PCG Simulation reussie : {report['initial_points']} points bruts -> {report['poisson_final_points']} vegetaux instancies.")
    print(f"       Taux d'elimination naturel = {report['rejection_rate_percent']:.1f}%")
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(run_self_test())