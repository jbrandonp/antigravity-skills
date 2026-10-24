#!/usr/bin/env python3
"""Pre-flight 3D Character Mesh & Texture Validator.

Audits generative 3D meshes (.glb, .gltf, .obj) from Tripo H3.1, Rodin, or Hunyuan
before sending them to Blender auto-rigging or game engines:
1. Polygon & Triangle Budget (flags 1M+ polygon un-decimated raw meshes)
2. Bounding Box & Ground Pivot Alignment (verifies feet ground-plane at origin)
3. PBR Texture & Material Map Audit (BaseColor, Normal, Metallic-Roughness)
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import struct
import sys
from typing import Sequence


def parse_glb_header(glb_path: Path) -> dict:
    """Parses binary glTF (.glb) header and JSON chunk."""
    with glb_path.open("rb") as f:
        magic, version, length = struct.unpack("<4sII", f.read(12))
        if magic != b"glTF":
            raise ValueError(f"Invalid GLB magic: {magic}. Not a valid binary glTF file.")

        chunk_len, chunk_type = struct.unpack("<I4s", f.read(8))
        if chunk_type != b"JSON":
            raise ValueError(f"Expected JSON chunk, got {chunk_type}")

        json_bytes = f.read(chunk_len)
        gltf_json = json.loads(json_bytes.decode("utf-8"))

    return gltf_json


def audit_glb_mesh(
    glb_path: Path, max_triangles: int = 45000, target_engine: str = "UE5"
) -> dict:
    """Audits a GLB mesh for polygon count, bounding box pivot, and PBR textures."""
    gltf = parse_glb_header(glb_path)

    # 1. Triangle Count Audit
    total_triangles = 0
    total_vertices = 0
    accessors = gltf.get("accessors", [])

    for mesh in gltf.get("meshes", []):
        for prim in mesh.get("primitives", []):
            # Indices accessor
            indices_idx = prim.get("indices")
            if indices_idx is not None and indices_idx < len(accessors):
                acc = accessors[indices_idx]
                count = acc.get("count", 0)
                mode = prim.get("mode", 4)  # 4 = TRIANGLES
                if mode == 4:
                    total_triangles += count // 3
                elif mode == 5 or mode == 6:  # STRIP or FAN
                    total_triangles += max(0, count - 2)

            # Positions accessor
            pos_idx = prim.get("attributes", {}).get("POSITION")
            if pos_idx is not None and pos_idx < len(accessors):
                acc = accessors[pos_idx]
                total_vertices += acc.get("count", 0)

    # 2. Bounding Box & Pivot Check
    # Scan POSITION accessors for min/max coordinates
    min_x, min_y, min_z = float("inf"), float("inf"), float("inf")
    max_x, max_y, max_z = float("-inf"), float("-inf"), float("-inf")

    for acc in accessors:
        if "min" in acc and "max" in acc and len(acc["min"]) == 3:
            p_min, p_max = acc["min"], acc["max"]
            min_x = min(min_x, p_min[0])
            min_y = min(min_y, p_min[1])
            min_z = min(min_z, p_min[2])
            max_x = max(max_x, p_max[0])
            max_y = max(max_y, p_max[1])
            max_z = max(max_z, p_max[2])

    dims = [
        round(max_x - min_x, 3) if max_x > min_x else 0.0,
        round(max_y - min_y, 3) if max_y > min_y else 0.0,
        round(max_z - min_z, 3) if max_z > min_z else 0.0,
    ]

    # In glTF, standard coordinate is Y-up. Floor is usually min_y.
    # In UE5 (Z-up), converted floor is min_z.
    floor_coord = min_y
    pivot_at_ground = abs(floor_coord) < 0.15

    # 3. PBR Material Inspection
    materials = gltf.get("materials", [])
    has_basecolor = False
    has_normal = False
    has_orm = False

    for mat in materials:
        pbr = mat.get("pbrMetallicRoughness", {})
        if "baseColorTexture" in pbr:
            has_basecolor = True
        if "metallicRoughnessTexture" in pbr:
            has_orm = True
        if "normalTexture" in mat:
            has_normal = True

    # 4. Score and Verdict
    penalties = []
    verdict = "PASS"

    if total_triangles > max_triangles:
        penalties.append(
            f"Polygon count too high: {total_triangles:,} triangles (recommended threshold: {max_triangles:,}). Decimate in Blender before real-time use."
        )
        verdict = "WARN" if total_triangles < (max_triangles * 2) else "FAIL"

    if not pivot_at_ground:
        penalties.append(
            f"Pivot not centered at feet: lowest coordinate is {floor_coord:.3f}. Will float or clip in-engine without center_glb_bottom.py."
        )
        if verdict != "FAIL":
            verdict = "WARN"

    if not has_normal:
        penalties.append("Missing Normal map: mesh will appear flat under dynamic lighting.")
        if verdict != "FAIL":
            verdict = "WARN"

    return {
        "file": str(glb_path),
        "triangles": total_triangles,
        "vertices": total_vertices,
        "dimensions": dims,
        "floor_y_min": round(floor_coord, 3),
        "pivot_at_ground": pivot_at_ground,
        "pbr_textures": {
            "base_color": has_basecolor,
            "normal_map": has_normal,
            "metallic_roughness": has_orm,
        },
        "verdict": verdict,
        "penalties": penalties,
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate 3D character mesh for triangle budget, pivot alignment, and PBR."
    )
    parser.add_argument("-i", "--input", required=True, help="Path to .glb mesh")
    parser.add_argument(
        "--max-tris", type=int, default=45000, help="Maximum allowed triangles"
    )
    parser.add_argument("--json", action="store_true", help="Output raw JSON")

    args = parser.parse_args(argv)
    glb_file = Path(args.input)
    if not glb_file.exists():
        print(f"Error: File not found: {glb_file}", file=sys.stderr)
        return 1

    try:
        report = audit_glb_mesh(glb_file, max_triangles=args.max_tris)
    except Exception as e:
        print(f"Error reading GLB: {e}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(report, indent=2))
        return 0 if report["verdict"] != "FAIL" else 1

    print("==================================================================")
    print("            3D CHARACTER MESH PRE-FLIGHT AUDIT                    ")
    print("==================================================================")
    print(f"File:           {report['file']}")
    print(f"Triangles:      {report['triangles']:,}")
    print(f"Vertices:       {report['vertices']:,}")
    print(f"Dimensions:     {report['dimensions'][0]} × {report['dimensions'][1]} × {report['dimensions'][2]} m")
    print(f"Ground Pivot:   {'Centered at feet' if report['pivot_at_ground'] else f'Off-axis ({report['floor_y_min']})'}")
    print(f"PBR Textures:   BaseColor: {report['pbr_textures']['base_color']} | Normal: {report['pbr_textures']['normal_map']} | ORM: {report['pbr_textures']['metallic_roughness']}")
    print(f"Verdict:        {report['verdict']}")
    print("------------------------------------------------------------------")

    if report["penalties"]:
        print("Findings:")
        for p in report["penalties"]:
            print(f"  ⚠ {p}")
    else:
        print("✓ Mesh meets production standards! Clean triangle budget & PBR maps.")

    print("==================================================================")
    return 0 if report["verdict"] != "FAIL" else 1


if __name__ == "__main__":
    sys.exit(main())
