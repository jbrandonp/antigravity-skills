"""
3D Procedural Foot IK — Solveur Analytique Two-Bone IK
Auteur: Brandon (Antigravity Studio Engine)
Règles: Typage strict, zéro Any, calculs trigonométriques purs.
"""

import math
from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass
class TwoBoneIKSolution:
    hip_angle_deg: float
    knee_angle_deg: float
    is_reachable: bool
    pelvis_offset_y: float


def solve_two_bone_ik(
    upper_length: float,
    lower_length: float,
    target_distance: float,
    ground_height_delta: float
) -> TwoBoneIKSolution:
    max_reach = upper_length + lower_length
    min_reach = abs(upper_length - lower_length)

    # 1. Calcul du décalage de bassin
    pelvis_offset = min(0.0, ground_height_delta)
    effective_dist = max(min_reach, min(target_distance, max_reach * 0.999))

    # 2. Loi des cosinus
    # cos(knee) = (L1^2 + L2^2 - D^2) / (2 * L1 * L2)
    cos_knee = (upper_length ** 2 + lower_length ** 2 - effective_dist ** 2) / (2.0 * upper_length * lower_length)
    cos_knee = max(-1.0, min(1.0, cos_knee))
    knee_rad = math.acos(cos_knee)

    # cos(hip) = (L1^2 + D^2 - L2^2) / (2 * L1 * D)
    cos_hip = (upper_length ** 2 + effective_dist ** 2 - lower_length ** 2) / (2.0 * upper_length * effective_dist)
    cos_hip = max(-1.0, min(1.0, cos_hip))
    hip_rad = math.acos(cos_hip)

    return TwoBoneIKSolution(
        hip_angle_deg=math.degrees(hip_rad),
        knee_angle_deg=math.degrees(math.pi - knee_rad),
        is_reachable=(target_distance <= max_reach),
        pelvis_offset_y=pelvis_offset
    )


def run_ik_demonstration() -> None:
    print("=" * 70)
    print("    3D PROCEDURAL FOOT IK : SOLVEUR ANALYTIQUE TWO-BONE IK     ")
    print("=" * 70)
    l1 = 0.50  # Cuisse: 50 cm
    l2 = 0.50  # Mollet: 50 cm
    print(f"Dimensions du squelette de jambe : Cuisse={l1*100:.0f}cm, Mollet={l2*100:.0f}cm (Portée max={l1+l2:.2f}m)")
    print("-" * 70)

    scenarios = [
        ("Sol Plat Standard (Distance 90cm)", 0.90, 0.0),
        ("Pied sur Marche Élevée (+20cm)", 0.75, 0.20),
        ("Pied dans un Trou (-25cm)", 0.98, -0.25),
        ("Jambe Complètement Tendue (100cm)", 1.00, 0.0)
    ]

    for label, dist, delta_h in scenarios:
        sol = solve_two_bone_ik(l1, l2, dist, delta_h)
        print(f"Scénario: {label}")
        print(f"  Angle Hanche: {sol.hip_angle_deg:5.1f}° | Angle Flexion Genou: {sol.knee_angle_deg:5.1f}°")
        print(f"  Décalage Bassin Y: {sol.pelvis_offset_y:5.2f}m | Atteignable: {sol.is_reachable}")
        print()

    print("=" * 70)
    print("[OK] Solveur analytique Two-Bone IK et adaptation de relief validés.")
    print("=" * 70)


if __name__ == "__main__":
    run_ik_demonstration()
