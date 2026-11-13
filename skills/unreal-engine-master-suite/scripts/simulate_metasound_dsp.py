# -*- coding: utf-8 -*-
"""
simulate_metasound_dsp.py - Unreal Engine 5 MetaSound DSP Simulator
Simulateur de synthese audio procedurale et filtrage passe-bas sample-accurate.
"""

import math
from typing import List, TypedDict

class AudioBlock(TypedDict):
    sample_rate: int
    block_size: int
    samples: List[float]
    peak_amplitude: float
    rms_level: float

def generate_procedural_engine_block(
    rpm: float,
    sample_rate: int = 48000,
    block_size: int = 64,
    phase_acc: float = 0.0
) -> AudioBlock:
    """Genere un bloc audio DSP synthetisant le grondement d'un moteur a explosion."""
    # Frequence fondamentale calibree sur les tours/min (moteur 4 cylindres : 2 combustions par tour)
    fundamental_hz = max(20.0, (rpm / 60.0) * 2.0)
    samples: List[float] = []
    
    current_phase = phase_acc
    phase_inc = (2.0 * math.pi * fundamental_hz) / sample_rate

    peak = 0.0
    sum_squares = 0.0

    for _ in range(block_size):
        # Somme d'harmoniques paires et impaires pour timbre riche
        harmonic1 = math.sin(current_phase)
        harmonic2 = 0.5 * math.sin(current_phase * 2.0)
        harmonic3 = 0.25 * math.sin(current_phase * 3.0)

        sample_val = (harmonic1 + harmonic2 + harmonic3) / 1.75
        samples.append(sample_val)

        abs_val = abs(sample_val)
        if abs_val > peak:
            peak = abs_val
        sum_squares += sample_val * sample_val

        current_phase += phase_inc
        if current_phase > 2.0 * math.pi:
            current_phase -= 2.0 * math.pi

    rms = math.sqrt(sum_squares / block_size)
    return {
        "sample_rate": sample_rate,
        "block_size": block_size,
        "samples": samples,
        "peak_amplitude": peak,
        "rms_level": rms
    }

def apply_biquad_lowpass(
    block: AudioBlock,
    cutoff_hz: float,
    sample_rate: int = 48000
) -> AudioBlock:
    """Applique un filtre passe-bas monopolaire temps reel."""
    rc = 1.0 / (2.0 * math.pi * cutoff_hz)
    dt = 1.0 / sample_rate
    alpha = dt / (rc + dt)

    filtered: List[float] = []
    last_val = 0.0
    peak = 0.0
    sum_squares = 0.0

    for s in block["samples"]:
        out = last_val + alpha * (s - last_val)
        filtered.append(out)
        last_val = out

        abs_val = abs(out)
        if abs_val > peak:
            peak = abs_val
        sum_squares += out * out

    return {
        "sample_rate": sample_rate,
        "block_size": block["block_size"],
        "samples": filtered,
        "peak_amplitude": peak,
        "rms_level": math.sqrt(sum_squares / block["block_size"])
    }

def run_self_test() -> int:
    """Verifie la generation et le filtrage DSP de MetaSound."""
    print("Execution du self-test MetaSound DSP UE5...")
    raw_block = generate_procedural_engine_block(rpm=3000.0, sample_rate=48000, block_size=128)
    assert len(raw_block["samples"]) == 128, "Invalid sample count!"
    assert raw_block["peak_amplitude"] <= 1.0, f"Clipping detected: {raw_block['peak_amplitude']}"

    # Filtrage passe-bas a 200 Hz (simulant occlusion par un mur)
    filtered_block = apply_biquad_lowpass(raw_block, cutoff_hz=200.0, sample_rate=48000)
    assert filtered_block["rms_level"] <= raw_block["rms_level"], "Lowpass filter failed to attenuate high frequencies!"

    print(f"[PASS] MetaSound DSP teste : Bloc de 128 echantillons synthetise avec succes.")
    print(f"       Amortissement Occlusion : RMS brut = {raw_block['rms_level']:.3f} -> Filtre = {filtered_block['rms_level']:.3f}")
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(run_self_test())