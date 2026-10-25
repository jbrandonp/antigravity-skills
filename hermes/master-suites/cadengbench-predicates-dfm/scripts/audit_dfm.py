"""Deterministic CADEngBench L0-L1 CLI Audit Tool.

Usage:
    python audit_dfm.py [path_to_step_file]
"""

from __future__ import annotations
import sys
from pathlib import Path
import math
import build123d as bd
from OCP.BRepCheck import BRepCheck_Analyzer


def audit_file(step_path: str) -> int:
    path = Path(step_path)
    if not path.exists():
        print(f"[!] Erreur: Fichier introuvable : {step_path}", file=sys.stderr)
        return 1

    print(f"[*] Chargement du fichier B-Rep : {step_path}")
    part = bd.import_step(str(path))

    # Porte L0
    analyzer = BRepCheck_Analyzer(part.wrapped)
    is_l0 = bool(analyzer.IsValid()) and float(part.volume) > 1e-6 and part.is_valid
    print(f"[*] Porte L0 (Intégrité B-Rep) : {'PASS' if is_l0 else 'FAIL'} (Volume: {float(part.volume):.2f} mm³)")

    if not is_l0:
        return 1

    # Porte L1 (DFM)
    faces = part.faces()
    undercuts = 0
    draft_violations = 0
    min_hole = float("inf")

    for cyl in faces.filter_by(bd.GeomType.CYLINDER):
        min_hole = min(min_hole, float(cyl.radius) * 2.0)
    if min_hole == float("inf"):
        min_hole = 0.0

    for f in faces:
        n = f.normal_at()
        if n.Z < -0.05 and abs(n.Z + 1.0) > 0.05:
            undercuts += 1
        angle_deg = math.degrees(math.asin(max(-1.0, min(1.0, abs(n.Z)))))
        if 0.0 < angle_deg < 1.5:
            draft_violations += 1

    bbox = part.bounding_box()
    min_dim = min(float(bbox.size.X), float(bbox.size.Y), float(bbox.size.Z))

    is_l1 = min_dim >= 1.0 and (min_hole == 0.0 or min_hole >= 2.0) and undercuts == 0
    print(f"[*] Porte L1 (Règles DFM)     : {'PASS' if is_l1 else 'FAIL'}")
    print(f"    - Épaisseur min          : {min_dim:.2f} mm (Seuil: 1.0 mm)")
    print(f"    - Diamètre perçage min   : {min_hole:.2f} mm (Seuil: 2.0 mm)")
    print(f"    - Contre-dépouilles      : {undercuts}")
    print(f"    - Dépouilles < 1.5°      : {draft_violations}")

    return 0 if (is_l0 and is_l1) else 1


if __name__ == "__main__":
    if len(sys.argv) > 1:
        sys.exit(audit_file(sys.argv[1]))
    else:
        print("Usage: python audit_dfm.py [path_to_step_file]")
        sys.exit(0)
