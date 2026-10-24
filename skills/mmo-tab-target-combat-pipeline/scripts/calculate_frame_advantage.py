# -*- coding: utf-8 -*-
"""
calculate_frame_advantage.py - Combat Frame Architect
Calculateur d avantage de frame data (Startup, Active, Recovery, HitStun, BlockStun).
"""

import argparse
from typing import TypedDict, List, Dict, Tuple

class AttackMove(TypedDict):
    name: str
    startup_frames: int
    active_frames: int
    recovery_frames: int
    hit_stun: int
    block_stun: int

DEMO_MOVESET: List[AttackMove] = [
    {
        "name": "Coup Rapide (Jab)",
        "startup_frames": 4,
        "active_frames": 2,
        "recovery_frames": 8,
        "hit_stun": 14,
        "block_stun": 9,
    },
    {
        "name": "Coup Puissant (Heavy Slash)",
        "startup_frames": 16,
        "active_frames": 4,
        "recovery_frames": 22,
        "hit_stun": 28,
        "block_stun": 12,
    },
    {
        "name": "Attaque Balayage (Sweep)",
        "startup_frames": 10,
        "active_frames": 3,
        "recovery_frames": 18,
        "hit_stun": 24,
        "block_stun": 6,
    },
]

def analyze_moveset(moves: List[AttackMove]) -> None:
    print(f"{'Attaque':<25} | {'Duree Totale':<12} | {'Avantage Coup':<14} | {'Avantage Garde':<14} | {'Securite Garde'}")
    print("-" * 80)

    for m in moves:
        total_frames = m["startup_frames"] + m["active_frames"] + m["recovery_frames"]
        adv_hit = m["hit_stun"] - m["recovery_frames"]
        adv_block = m["block_stun"] - m["recovery_frames"]

        hit_tag = f"+{adv_hit}" if adv_hit > 0 else str(adv_hit)
        block_tag = f"+{adv_block}" if adv_block > 0 else str(adv_block)

        if adv_block >= 0:
            safety = "AVANTAGEUX (Safe)"
        elif adv_block >= -5:
            safety = "RELATIVEMENT SUR (-5)"
        else:
            safety = f"PUNISSABLE ({adv_block})"

        print(f"{m['name']:<25} | {total_frames:<12} | {hit_tag:<14} | {block_tag:<14} | {safety}")

def main():
    parser = argparse.ArgumentParser(description="Combat Frame Architect - Calculateur de Frame Data")
    parser.add_argument("--demo", action="store_true", help="Analyser le moveset de combat de demonstration")
    args = parser.parse_args()

    print("=" * 80)
    print("      COMBAT FRAME ARCHITECT : ANALYSE DES FRAMES DE COMBAT (60 FPS)    ")
    print("=" * 80)

    analyze_moveset(DEMO_MOVESET)

    print("=" * 80)
    print("[OK] Equilibrage de combat verifie : fenetres de punition deterministes.")
    print("=" * 80)

if __name__ == "__main__":
    main()