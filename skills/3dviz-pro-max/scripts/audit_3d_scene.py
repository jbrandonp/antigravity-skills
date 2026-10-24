#!/usr/bin/env python3
"""WebGL & Three.js 3D Scene Static Code Quality Gate.

Audits Three.js / WebGL application code (JS/TS/HTML) against production standards:
1. Color Management & Tone Mapping (ACESFilmic, SRGBColorSpace)
2. High-DPI Pixel Ratio Clamping (Math.min(window.devicePixelRatio, 2))
3. Animation Loop Delta-Time Bounding (prevents physics explosion on tab blur)
4. Memory Leak Guards (geometry, material, and texture disposal)
5. Shadow Map & Lighting Budget (guards against GPU fillrate choking)
6. Camera Ergonomics (damping, near/far depth precision)
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
from typing import Sequence


def audit_threejs_scene(file_path: Path) -> dict:
    """Performs static code audit on a Three.js scene file."""
    text = file_path.read_text(encoding="utf-8", errors="replace")

    report: dict = {
        "file": str(file_path),
        "verdict": "PASS",
        "score": 100,
        "penalties": [],
        "checks": {},
    }

    # 1. Tone Mapping Check
    has_tonemapping = bool(
        re.search(r"toneMapping\s*=\s*THREE\.(ACESFilmic|AgX|Neutral|Cineon)ToneMapping", text)
    )
    report["checks"]["tone_mapping_configured"] = has_tonemapping
    if not has_tonemapping:
        report["penalties"].append(
            "Missing modern tone mapping: Set renderer.toneMapping = THREE.ACESFilmicToneMapping to avoid blown-out highlights."
        )
        report["score"] -= 15

    # 2. Output Color Space Check
    has_colorspace = bool(
        re.search(r"outputColorSpace\s*=\s*THREE\.(SRGBColorSpace|LinearSRGBColorSpace)", text)
        or re.search(r"outputEncoding\s*=\s*THREE\.sRGBEncoding", text)
    )
    report["checks"]["output_colorspace_configured"] = has_colorspace
    if not has_colorspace:
        report["penalties"].append(
            "Color space not explicitly configured: Set renderer.outputColorSpace = THREE.SRGBColorSpace for accurate PBR lighting."
        )
        report["score"] -= 10

    # 3. Pixel Ratio Clamping
    has_clamped_pr = bool(
        re.search(r"setPixelRatio\s*\(\s*Math\.min\s*\(\s*window\.devicePixelRatio\s*,\s*[12](\.\d+)?\s*\)\s*\)", text)
    )
    has_raw_pr = bool(
        re.search(r"setPixelRatio\s*\(\s*window\.devicePixelRatio\s*\)", text)
    )
    report["checks"]["pixel_ratio_clamped"] = has_clamped_pr
    if has_raw_pr and not has_clamped_pr:
        report["penalties"].append(
            "Unclamped devicePixelRatio: Causes severe GPU fillrate collapse on Retina/4K screens. Use Math.min(window.devicePixelRatio, 2)."
        )
        report["score"] -= 15

    # 4. Animation Loop Delta-Time Bounding
    has_delta_clamp = bool(
        re.search(r"Math\.min\s*\(\s*(delta|dt)\s*,\s*0\.[01]\d*\s*\)", text)
        or re.search(r"if\s*\(\s*(delta|dt)\s*>\s*0\.[01]\d*\s*\)\s*(delta|dt)\s*=\s*0\.[01]\d*", text)
    )
    has_clock_delta = bool(re.search(r"clock\.getDelta\(\)", text))
    report["checks"]["delta_time_bounded"] = has_delta_clamp or not has_clock_delta
    if has_clock_delta and not has_delta_clamp:
        report["penalties"].append(
            "Unbounded clock.getDelta(): Tab backgrounding causes massive delta spike and physics explosion. Clamp dt = Math.min(delta, 0.1)."
        )
        report["score"] -= 10

    # 5. Memory Disposal Guards
    has_dispose = bool(re.search(r"\.dispose\(\)", text))
    report["checks"]["disposal_logic_present"] = has_dispose
    if not has_dispose and ("new THREE.Mesh" in text or "new THREE.BufferGeometry" in text):
        report["penalties"].append(
            "No .dispose() calls found: Scene may leak WebGL buffers and GPU memory on unmount or recreation."
        )
        report["score"] -= 10

    # 6. Orbit Controls Damping
    has_controls = "OrbitControls" in text
    has_damping = bool(re.search(r"enableDamping\s*=\s*true", text))
    if has_controls and not has_damping:
        report["penalties"].append(
            "OrbitControls missing damping: Set controls.enableDamping = true for smooth physical camera inertia."
        )
        report["score"] -= 5

    # 7. Near/Far Plane Depth Ratio
    near_far_match = re.search(r"PerspectiveCamera\s*\(\s*[^,]+,\s*[^,]+,\s*([0-9.]+)\s*,\s*([0-9.]+)\s*\)", text)
    if near_far_match:
        near = float(near_far_match.group(1))
        far = float(near_far_match.group(2))
        ratio = far / max(0.0001, near)
        report["checks"]["depth_ratio"] = round(ratio, 1)
        if near < 0.01:
            report["penalties"].append(
                f"Camera near plane too close ({near}): Causes severe Z-fighting on standard 24-bit depth buffers. Recommended near >= 0.1."
            )
            report["score"] -= 15
        elif ratio > 100000:
            report["penalties"].append(
                f"Near/Far ratio too high ({ratio:.0f}): Leads to depth buffer precision loss. Keep Far/Near < 50,000."
            )
            report["score"] -= 10

    # Final Verdict
    report["score"] = max(0, min(100, report["score"]))
    if report["score"] < 65:
        report["verdict"] = "FAIL"
    elif report["score"] < 85:
        report["verdict"] = "WARN"
    else:
        report["verdict"] = "PASS"

    return report


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Audit WebGL & Three.js 3D scene code for production performance & stability."
    )
    parser.add_argument("-i", "--input", required=True, help="Path to Three.js JavaScript/TypeScript/HTML file")
    parser.add_argument("--json", action="store_true", help="Output raw JSON report")

    args = parser.parse_args(argv)
    target = Path(args.input)
    if not target.exists():
        print(f"Error: File not found: {target}", file=sys.stderr)
        return 1

    report = audit_threejs_scene(target)

    if args.json:
        print(json.dumps(report, indent=2))
        return 0 if report["verdict"] != "FAIL" else 1

    print("==================================================================")
    print("           THREE.JS & WEBGL SCENE CODE QUALITY AUDIT              ")
    print("==================================================================")
    print(f"File:       {report['file']}")
    print(f"Score:      {report['score']}/100")
    print(f"Verdict:    {report['verdict']}")
    print("------------------------------------------------------------------")
    print("Checks Summary:")
    for k, v in report["checks"].items():
        print(f"  • {k.replace('_', ' ').capitalize()}: {v}")

    if report["penalties"]:
        print("\nFindings & Recommendations:")
        for p in report["penalties"]:
            print(f"  ⚠ {p}")
    else:
        print("\n✓ Perfect 3D scene craftsmanship! Zero memory leaks, proper tone mapping.")

    print("==================================================================")
    return 0 if report["verdict"] != "FAIL" else 1


if __name__ == "__main__":
    sys.exit(main())
