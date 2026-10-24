#!/usr/bin/env python3
"""
Game Animation Polish: Hitstop & Combat Impact Curve Calculator
Derived from Skullgirls Animation Polish standards and fighting game combat juice engineering.
Generates timing curves for Unity (C# AnimationCurve), Unreal Engine, and Godot.
"""

import sys
import argparse
import json

WEIGHT_PRESETS = {
    "light": {
        "anticipation_ms": 60,
        "snap_ms": 30,
        "hitstop_ms": 50,
        "recovery_ms": 120,
        "camera_shake_amp": 0.05,
        "camera_shake_freq": 25.0
    },
    "medium": {
        "anticipation_ms": 100,
        "snap_ms": 40,
        "hitstop_ms": 100,
        "recovery_ms": 220,
        "camera_shake_amp": 0.15,
        "camera_shake_freq": 18.0
    },
    "heavy": {
        "anticipation_ms": 180,
        "snap_ms": 50,
        "hitstop_ms": 180,
        "recovery_ms": 380,
        "camera_shake_amp": 0.35,
        "camera_shake_freq": 12.0
    },
    "colossal": {
        "anticipation_ms": 280,
        "snap_ms": 60,
        "hitstop_ms": 280,
        "recovery_ms": 550,
        "camera_shake_amp": 0.65,
        "camera_shake_freq": 8.0
    }
}

def calculate_curve(preset: str, target_fps: int = 60):
    cfg = WEIGHT_PRESETS.get(preset.lower(), WEIGHT_PRESETS["medium"])
    
    total_ms = cfg["anticipation_ms"] + cfg["snap_ms"] + cfg["hitstop_ms"] + cfg["recovery_ms"]
    total_frames = int(round((total_ms / 1000.0) * target_fps))
    
    ant_frames = int(round((cfg["anticipation_ms"] / 1000.0) * target_fps))
    snap_frames = int(round((cfg["snap_ms"] / 1000.0) * target_fps))
    hitstop_frames = int(round((cfg["hitstop_ms"] / 1000.0) * target_fps))
    rec_frames = int(round((cfg["recovery_ms"] / 1000.0) * target_fps))
    
    print(f"\n{'='*55}")
    print(f"[Combat Juice] Curve: {preset.upper()} Impact ({target_fps} FPS)")
    print(f"{'='*55}")
    print(f"Total Duration    : {total_ms} ms (~{total_frames} frames)")
    print(f"1. Anticipation   : {cfg['anticipation_ms']:>4} ms ({ant_frames:>2} frames) -> Wind-up ease-in")
    print(f"2. Snap (Apex)    : {cfg['snap_ms']:>4} ms ({snap_frames:>2} frames) -> Maximum velocity strike")
    print(f"3. Hitstop Freeze : {cfg['hitstop_ms']:>4} ms ({hitstop_frames:>2} frames) -> World/Actor time dilation = 0.0")
    print(f"4. Recovery       : {cfg['recovery_ms']:>4} ms ({rec_frames:>2} frames) -> Exponential decay to idle")
    print(f"Camera Trauma     : Amp = {cfg['camera_shake_amp']}, Freq = {cfg['camera_shake_freq']} Hz")
    print(f"{'='*55}\n")
    
    # Unity C# Snippet
    print("// --- Unity C# Implementation ---")
    print(f"""public static IEnumerator TriggerHitstop(float duration = {cfg['hitstop_ms'] / 1000.0:.3f}f)
{{
    Time.timeScale = 0.0f;
    yield return new WaitForSecondsRealtime(duration);
    Time.timeScale = 1.0f;
}}
""")

    # Godot Snippet
    print("# --- Godot 4 GDScript Implementation ---")
    print(f"""func trigger_hitstop(duration: float = {cfg['hitstop_ms'] / 1000.0:.3f}) -> void:
    Engine.time_scale = 0.0
    await get_tree().create_timer(duration, true, false, true).timeout
    Engine.time_scale = 1.0
""")

def main():
    parser = argparse.ArgumentParser(description="Combat Hitstop & Juice Timing Calculator")
    parser.add_argument("--weight", choices=["light", "medium", "heavy", "colossal"], default="heavy", help="Strike weight class")
    parser.add_argument("--fps", type=int, default=60, help="Target game engine framerate")
    args = parser.parse_args()
    
    calculate_curve(args.weight, args.fps)

if __name__ == "__main__":
    main()
