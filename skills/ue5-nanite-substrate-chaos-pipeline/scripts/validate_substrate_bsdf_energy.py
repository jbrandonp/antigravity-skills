# -*- coding: utf-8 -*-
"""
validate_substrate_bsdf_energy.py - Unreal Engine 5 Substrate BSDF Validator
Simulateur et verificateur de conservation d'energie pour materiaux multicouches Substrate.
"""

import math
from typing import TypedDict, List, Dict

class SlabLayer(TypedDict):
    name: str
    diffuse_albedo: float
    fresnel_f0: float
    roughness: float
    transmittance_color: float
    thickness_microns: float

class MaterialEnergyAudit(TypedDict):
    layer_count: int
    top_fresnel_specular: float
    transmitted_energy: float
    bottom_diffuse_reflectance: float
    total_reflected_energy: float
    is_energy_conserving: bool

def fresnel_schlick(f0: float, cos_theta: float) -> float:
    """Calcule l'approximation de Fresnel-Schlick."""
    clamped_cos = max(0.0, min(1.0, cos_theta))
    return f0 + (1.0 - f0) * math.pow(1.0 - clamped_cos, 5.0)

def audit_substrate_layers(
    top_coat: SlabLayer,
    base_substrate: SlabLayer,
    incident_angle_degrees: float = 45.0
) -> MaterialEnergyAudit:
    """Audite la composition verticale de deux couches Substrate."""
    rad = math.radians(incident_angle_degrees)
    cos_theta = math.cos(rad)

    # 1. Couche superieure (vernis / clear coat)
    f_top = fresnel_schlick(top_coat["fresnel_f0"], cos_theta)
    
    # 2. Transmission a la couche inferieure (1.0 - F)
    t_to_bottom = (1.0 - f_top) * top_coat["transmittance_color"]

    # 3. Reflexion de la couche de base
    f_bottom = fresnel_schlick(base_substrate["fresnel_f0"], cos_theta)
    diffuse_bottom = base_substrate["diffuse_albedo"] * (1.0 - f_bottom)
    
    reflected_from_bottom = t_to_bottom * (f_bottom + diffuse_bottom)
    total_energy = f_top + reflected_from_bottom

    return {
        "layer_count": 2,
        "top_fresnel_specular": f_top,
        "transmitted_energy": t_to_bottom,
        "bottom_diffuse_reflectance": reflected_from_bottom,
        "total_reflected_energy": total_energy,
        "is_energy_conserving": total_energy <= 1.0001
    }

def run_self_test() -> int:
    """Verifie le respect physique de la conservation d'energie dans Substrate."""
    print("Execution du self-test Substrate BSDF UE5...")

    # Exemple : Peinture automobile multicouche (vernis polyuretane sur couche metallique)
    clear_coat: SlabLayer = {
        "name": "Polyurethane_ClearCoat",
        "diffuse_albedo": 0.0,
        "fresnel_f0": 0.04,  # Verre / resine
        "roughness": 0.05,
        "transmittance_color": 0.98,
        "thickness_microns": 50.0
    }

    base_paint: SlabLayer = {
        "name": "Red_Metallic_Flake",
        "diffuse_albedo": 0.65,
        "fresnel_f0": 0.55,
        "roughness": 0.35,
        "transmittance_color": 0.0,
        "thickness_microns": 100.0
    }

    audit = audit_substrate_layers(clear_coat, base_paint, incident_angle_degrees=30.0)
    assert audit["is_energy_conserving"], f"Energy violated: {audit['total_reflected_energy']}"
    assert audit["total_reflected_energy"] <= 1.0, "Reflectance exceeds physical unity!"

    print(f"[PASS] Substrate Energy audit reussi : Total Reflected = {audit['total_reflected_energy']:.4f} <= 1.0")
    print(f"       Vernis Speculaire = {audit['top_fresnel_specular']:.4f}, Base Transmise = {audit['bottom_diffuse_reflectance']:.4f}")
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(run_self_test())