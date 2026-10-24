# -*- coding: utf-8 -*-
"""
calculate_trauma_shake.py - Game Juice and Polish (Screen Shake Decay Calculator)
Calcule la reponse impulsionnelle et la decroissance non-lineaire (Trauma^2).
"""

import math
import argparse
from typing import TypedDict, List, Dict, Tuple

class ShakeFrame(TypedDict):
    time_sec: float
    trauma: float
    shake_intensity: float
    rotational_angle_deg: float

def simulate_trauma_decay(initial_trauma: float, decay_rate: float, max_angle_deg: float = 12.0) -> List[ShakeFrame]:
    frames: List[ShakeFrame] = []
    dt = 0.05 # 20 Hz
    current_trauma = min(1.0, max(0.0, initial_trauma))
    t = 0.0

    while current_trauma > 0.01 and t < 2.5:
        # Intensite non-lineaire T^2
        shake = current_trauma ** 2
        # Oscillation angulaire pseudo-harmonique
        angle = max_angle_deg * shake * math.sin(t * 25.0)

        frames.append({
            "time_sec": round(t, 2),
            "trauma": round(current_trauma, 3),
            "shake_intensity": round(shake, 3),
            "rotational_angle_deg": round(angle, 2),
        })

        current_trauma = max(0.0, current_trauma - decay_rate * dt)
        t += dt

    return frames

def main():
    parser = argparse.ArgumentParser(description="Game Juice - Calculateur de Trauma Screen Shake (Purho Standard)")
    parser.add_argument("--impact", type=float, default=0.9, help="Niveau de choc initial (0.0 a 1.0)")
    parser.add_argument("--decay", type=float, default=1.5, help="Taux d amortissement par seconde")
    parser.add_argument("--demo", action="store_true", help="Lancer la simulation de demonstration")
    args = parser.parse_args()

    print("=" * 65)
    print("      GAME JUICE & POLISH : SIMULATION TRAUMA SCREEN SHAKE      ")
    print("=" * 65)

    frames = simulate_trauma_decay(args.impact, args.decay)

    print(f"Impact Initial (Trauma) : {args.impact:.2f}")
    print(f"Taux d Amortissement     : {args.decay:.2f} / s")
    print("-" * 65)
    print(f"{'Temps (s)':<10} | {'Trauma':<8} | {'Intensite (T²)':<16} | {'Angle Shake'}")
    print("-" * 65)

    for fr in frames[::2]: # Afficher 1 frame sur 2
        bar = "#" * int(fr["shake_intensity"] * 25)
        print(f"{fr['time_sec']:<10.2f} | {fr['trauma']:<8.3f} | {fr['shake_intensity']:<16.3f} | {fr['rotational_angle_deg']:>6.2f}° {bar}")

    print("=" * 65)
    print(f"[OK] Stabilisation complete en {frames[-1]['time_sec']:.2f} secondes (Amortissement doux).")
    print("=" * 65)

if __name__ == "__main__":
    main()