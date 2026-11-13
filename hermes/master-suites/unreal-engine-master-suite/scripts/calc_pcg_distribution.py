#!/usr/bin/env python3
"""
Unreal Engine 5: Procedural Content Generation (PCG) Distribution & Density Calculator
Calculates Poisson disk point counts, VRAM transform memory footprints,
and optimal hierarchical subdivision bounds for massive open-world biomes.
"""

import sys
import math
import argparse

def calc_pcg_bounds(area_km2: float, min_radius_m: float, max_radius_m: float, density_factor: float = 0.7):
    # Convert km^2 to m^2
    area_m2 = area_km2 * 1_000_000.0
    avg_radius_m = (min_radius_m + max_radius_m) / 2.0
    
    # In 2D Poisson disk sampling with Bridson's algorithm, packaging efficiency is ~0.65-0.75
    point_footprint_m2 = math.pi * (avg_radius_m ** 2) / density_factor
    est_points = int(round(area_m2 / point_footprint_m2))
    
    # Each Nanite/Hierarchical Instanced Static Mesh (HISM) instance transform is 64 bytes (Matrix 4x4)
    vram_bytes = est_points * 64
    vram_mb = vram_bytes / (1024 * 1024)
    
    print(f"\n{'='*60}")
    print(f"[UE5 PCG] Biome Distribution Estimation ({area_km2} km^2)")
    print(f"{'='*60}")
    print(f"Biome Area         : {area_km2:.2f} km^2 ({area_m2:,.0f} m^2)")
    print(f"Point Separation   : {min_radius_m:.1f} m to {max_radius_m:.1f} m (Avg: {avg_radius_m:.1f} m)")
    print(f"Estimated Points   : {est_points:,} instances")
    print(f"HISM Transform VRAM: {vram_mb:.2f} MB")
    
    # Partitioning recommendations
    grid_size = 256 if est_points > 100_000 else 128
    print(f"\nPCG Graph Recommendations:")
    print(f"  - Spatial Partition Grid Size : {grid_size} m")
    print(f"  - Poisson Disk Pruning Radius : {min_radius_m:.2f} m")
    print(f"  - Culling Distance (Max LOD)  : {min(1500, int(avg_radius_m * 80))} m")
    print(f"  - Enable 'Use Hierarchical Generation': {'True (Required for >100k instances)' if est_points > 100_000 else 'False'}")
    print(f"{'='*60}\n")

def main():
    parser = argparse.ArgumentParser(description="UE5 PCG Biome Point & VRAM Calculator")
    parser.add_argument("--area", type=float, default=1.0, help="Biome area in square kilometers (km^2)")
    parser.add_argument("--min-radius", type=float, default=4.0, help="Minimum point separation in meters")
    parser.add_argument("--max-radius", type=float, default=8.0, help="Maximum point separation in meters")
    parser.add_argument("--density", type=float, default=0.7, help="Packaging density ratio (0.5 to 0.9)")
    args = parser.parse_args()
    
    calc_pcg_bounds(args.area, args.min_radius, args.max_radius, args.density)

if __name__ == "__main__":
    main()
