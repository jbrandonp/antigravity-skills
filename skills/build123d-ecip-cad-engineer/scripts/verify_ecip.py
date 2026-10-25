"""ECIP Model Generator & B-Rep Verification CLI Tool.

Usage:
    python verify_ecip.py [output_step_path]
"""

from __future__ import annotations
import sys
from pathlib import Path
import build123d as bd
from OCP.BRepCheck import BRepCheck_Analyzer


def generate_and_verify_part(output_step: str = "output_verified_part.step") -> int:
    print("[*] Génération d'une pièce industrielle déclarative ECIP avec build123d...")

    params = {
        "length": 110.0,
        "width": 70.0,
        "thickness": 12.0,
        "boss_diameter": 32.0,
        "boss_height": 18.0,
        "bore_diameter": 16.0,
        "fillet_radius": 3.0,
    }

    with bd.BuildPart() as model:
        # 1. Base
        bd.Box(params["length"], params["width"], params["thickness"])

        # 2. Bossage cylindrique
        top_face = model.faces().sort_by(bd.Axis.Z)[-1]
        with bd.BuildSketch(top_face):
            bd.Circle(radius=params["boss_diameter"] / 2.0)
        bd.extrude(amount=params["boss_height"])

        # 3. Alésage central traversant avec micro-dépassement
        highest_face = model.faces().sort_by(bd.Axis.Z)[-1]
        with bd.BuildSketch(highest_face):
            bd.Circle(radius=params["bore_diameter"] / 2.0)
        bd.extrude(amount=-(params["thickness"] + params["boss_height"] + 2.0), mode=bd.Mode.SUBTRACT)

        # 4. Perçages aux 4 coins (GridLocations)
        dx = (params["length"] / 2.0) - 10.0
        dy = (params["width"] / 2.0) - 10.0
        with bd.BuildSketch(model.faces().sort_by(bd.Axis.Z)[0]):
            with bd.GridLocations(dx * 2.0, dy * 2.0, 2, 2):
                bd.Circle(radius=4.0)
        bd.extrude(amount=params["thickness"] * 2.0, mode=bd.Mode.SUBTRACT)

        # 5. Congés sécurisés
        vertical_edges = [e for e in model.edges().filter_by(bd.Axis.Z) if float(e.length) >= 2.2 * params["fillet_radius"]]
        if vertical_edges:
            bd.fillet(vertical_edges, radius=params["fillet_radius"])

    part = model.part

    # Validation Porte L0
    analyzer = BRepCheck_Analyzer(part.wrapped)
    is_valid = bool(analyzer.IsValid()) and part.is_valid
    vol = float(part.volume)

    print(f"[*] Analyse BRepCheck : {'VALIDE' if is_valid else 'INVALIDE'}")
    print(f"[*] Volume B-Rep      : {vol:.2f} mm³")
    print(f"[*] Nombre de faces   : {len(part.faces())}")
    print(f"[*] Nombre d'arêtes   : {len(part.edges())}")

    if is_valid and vol > 1e-6:
        out_file = Path(output_step)
        bd.export_step(part, str(out_file))
        print(f"[+] Exportation STEP AP242 réussie : {out_file.resolve()}")
        if output_step == "output_verified_part.step" and out_file.exists():
            out_file.unlink()
        return 0
    else:
        print("[!] Échec de la Porte L0", file=sys.stderr)
        return 1


if __name__ == "__main__":
    step_out = sys.argv[1] if len(sys.argv) > 1 else "output_verified_part.step"
    sys.exit(generate_and_verify_part(step_out))
