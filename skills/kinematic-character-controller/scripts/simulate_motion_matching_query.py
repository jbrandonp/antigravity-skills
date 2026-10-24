# -*- coding: utf-8 -*-
"""
simulate_motion_matching_query.py - Unreal Engine 5 Motion Matching Simulator
Simulateur de recherche de pose optimale dans une base de donnees d'animation
par comparaison de trajectoire future et d'orientation.
"""

import math
from typing import List, Dict, Tuple, TypedDict

class TrajectoryPoint(TypedDict):
    time_offset: float
    pos_x: float
    pos_y: float
    velocity_x: float
    velocity_y: float
    facing_angle: float

class DatabasePose(TypedDict):
    pose_id: int
    clip_name: str
    frame_index: int
    left_foot_height: float
    right_foot_height: float
    future_trajectory: List[TrajectoryPoint]

class MatchResult(TypedDict):
    best_pose_id: int
    clip_name: str
    frame_index: int
    total_cost: float
    trajectory_cost: float
    pose_cost: float

def compute_trajectory_distance(
    query_traj: List[TrajectoryPoint],
    candidate_traj: List[TrajectoryPoint],
    pos_weight: float = 1.0,
    vel_weight: float = 0.5,
    facing_weight: float = 0.8
) -> float:
    """Calcule le cout de divergence spatio-temporelle entre deux trajectoires."""
    cost = 0.0
    for q_pt, c_pt in zip(query_traj, candidate_traj):
        dx = q_pt["pos_x"] - c_pt["pos_x"]
        dy = q_pt["pos_y"] - c_pt["pos_y"]
        pos_dist_sq = dx * dx + dy * dy

        dvx = q_pt["velocity_x"] - c_pt["velocity_x"]
        dvy = q_pt["velocity_y"] - c_pt["velocity_y"]
        vel_dist_sq = dvx * dvx + dvy * dvy

        d_angle = abs(q_pt["facing_angle"] - c_pt["facing_angle"])
        if d_angle > math.pi:
            d_angle = 2.0 * math.pi - d_angle
        angle_dist_sq = d_angle * d_angle

        cost += (pos_weight * pos_dist_sq) + (vel_weight * vel_dist_sq) + (facing_weight * angle_dist_sq)

    return cost

def search_best_pose(
    query_trajectory: List[TrajectoryPoint],
    database: List[DatabasePose]
) -> MatchResult:
    """Trouve la meilleure pose dans la base minimisant la fonction de cout globale."""
    best_cost = float("inf")
    best_result: MatchResult = {
        "best_pose_id": -1,
        "clip_name": "unknown",
        "frame_index": 0,
        "total_cost": float("inf"),
        "trajectory_cost": 0.0,
        "pose_cost": 0.0
    }

    for candidate in database:
        traj_cost = compute_trajectory_distance(query_trajectory, candidate["future_trajectory"])
        # Bonus de stabilite pour eviter les changements de pas chaotiques
        pose_cost = abs(candidate["left_foot_height"] - 0.0) * 0.1
        total_cost = traj_cost + pose_cost

        if total_cost < best_cost:
            best_cost = total_cost
            best_result = {
                "best_pose_id": candidate["pose_id"],
                "clip_name": candidate["clip_name"],
                "frame_index": candidate["frame_index"],
                "total_cost": total_cost,
                "trajectory_cost": traj_cost,
                "pose_cost": pose_cost
            }

    return best_result

def generate_mock_database() -> List[DatabasePose]:
    """Genere une bibliotheque de poses de demonstration."""
    db: List[DatabasePose] = []
    actions = [
        ("Walk_Forward", 1.5, 0.0),
        ("Jog_Forward", 4.0, 0.0),
        ("Sprint_Forward", 7.0, 0.0),
        ("Turn_Left_90", 2.0, math.pi / 2.0),
        ("Turn_Right_90", 2.0, -math.pi / 2.0),
        ("Stop_Instant", 0.0, 0.0)
    ]

    p_id = 0
    for clip, speed, angle in actions:
        for f in range(5):
            traj: List[TrajectoryPoint] = []
            for t_step in [0.2, 0.5, 1.0]:
                traj.append({
                    "time_offset": t_step,
                    "pos_x": math.cos(angle) * speed * t_step,
                    "pos_y": math.sin(angle) * speed * t_step,
                    "velocity_x": math.cos(angle) * speed,
                    "velocity_y": math.sin(angle) * speed,
                    "facing_angle": angle
                })
            db.append({
                "pose_id": p_id,
                "clip_name": clip,
                "frame_index": f * 10,
                "left_foot_height": 0.0 if f % 2 == 0 else 0.15,
                "right_foot_height": 0.15 if f % 2 == 0 else 0.0,
                "future_trajectory": traj
            })
            p_id += 1
    return db

def run_self_test() -> int:
    """Verifie la precision et la rapidite de selection du Motion Matching."""
    print("Execution du self-test Motion Matching UE5...")
    db = generate_mock_database()
    assert len(db) == 30, f"Expected 30 poses in mock db, got {len(db)}"

    # Requete simulant un virage brusque a gauche en courant (jog)
    query_turn_left: List[TrajectoryPoint] = [
        {"time_offset": 0.2, "pos_x": 0.0, "pos_y": 0.4, "velocity_x": 0.0, "velocity_y": 2.0, "facing_angle": 1.57},
        {"time_offset": 0.5, "pos_x": 0.0, "pos_y": 1.0, "velocity_x": 0.0, "velocity_y": 2.0, "facing_angle": 1.57},
        {"time_offset": 1.0, "pos_x": 0.0, "pos_y": 2.0, "velocity_x": 0.0, "velocity_y": 2.0, "facing_angle": 1.57}
    ]

    match = search_best_pose(query_turn_left, db)
    assert match["clip_name"] == "Turn_Left_90", f"Expected Turn_Left_90, got {match['clip_name']}"
    assert match["total_cost"] < 0.01, f"Expected near zero cost, got {match['total_cost']}"

    print(f"[PASS] Motion Matching teste : Pose retenue = {match['clip_name']} (Frame {match['frame_index']})")
    print(f"       Cout de divergence = {match['total_cost']:.5f}")
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(run_self_test())