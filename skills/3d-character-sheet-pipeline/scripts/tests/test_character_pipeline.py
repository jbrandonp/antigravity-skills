#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "pillow",
# ]
# ///
"""Automated Test Suite for 3D Character Sheet Pipeline Tools."""

import json
from pathlib import Path
import struct
import tempfile
import unittest

import numpy as np
from PIL import Image

sys_path = Path(__file__).resolve().parent.parent
import sys
if str(sys_path) not in sys.path:
    sys.path.insert(0, str(sys_path))

from scaffold_character_pack import scaffold_pack
from validate_3d_character_mesh import audit_glb_mesh
from verify_orthographic_symmetry import verify_character_sheet


class TestCharacterPipeline(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.work_dir = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_orthographic_symmetry_pass(self):
        """Tests that a perfectly symmetrical A-pose passes verification."""
        # Create a 200x200 pure white canvas
        canvas = np.full((200, 200, 3), 255, dtype=np.uint8)

        # Draw a symmetrical A-pose silhouette in center
        # Head
        canvas[20:50, 85:115] = [50, 50, 50]
        # Torso
        canvas[50:110, 75:125] = [50, 50, 50]
        # Left and Right Arms at 45 degrees
        for i in range(40):
            canvas[55 + i, 75 - i : 85 - i] = [50, 50, 50]  # Left
            canvas[55 + i, 115 + i : 125 + i] = [50, 50, 50]  # Right
        # Legs
        canvas[110:175, 75:92] = [50, 50, 50]
        canvas[110:175, 108:125] = [50, 50, 50]

        img_path = self.work_dir / "symmetric_apose.png"
        Image.fromarray(canvas).save(img_path)

        rep = verify_character_sheet(img_path, bg_mode="white", min_symmetry=0.80)
        self.assertEqual(rep["verdict"], "PASS")
        self.assertGreaterEqual(rep["metrics"]["dice_coefficient"], 0.85)
        self.assertLessEqual(abs(rep["metrics"]["spine_tilt_degrees"]), 3.0)

    def test_orthographic_symmetry_hard_fail_on_3q_rotation(self):
        """Tests that a 3/4 rotated or heavily asymmetric pose is rejected with HARD_FAIL."""
        canvas = np.full((200, 200, 3), 255, dtype=np.uint8)

        # Asymmetric 3/4 pose: character turned heavily to camera right
        canvas[20:50, 95:135] = [50, 50, 50]  # Off-center head
        canvas[50:110, 85:145] = [50, 50, 50]  # Bulging right torso
        # Only right arm visible prominently
        canvas[55:105, 140:170] = [50, 50, 50]
        canvas[110:175, 100:135] = [50, 50, 50]

        img_path = self.work_dir / "asymmetric_3q.png"
        Image.fromarray(canvas).save(img_path)

        rep = verify_character_sheet(img_path, bg_mode="white", min_symmetry=0.80)
        self.assertEqual(rep["verdict"], "HARD_FAIL")
        self.assertIn("escalated_correction_prompt", rep)
        self.assertTrue(len(rep["escalated_correction_prompt"]) > 20)

    def test_scaffold_character_pack(self):
        """Tests standard directory scaffolding and manifest.json creation."""
        pack_path = self.work_dir / "test_hero_pack"
        res = scaffold_pack(
            pack_path,
            character_name="paladin_warrior",
            art_style="stylized_pbr",
            accessories=["greatsword", "kite_shield"]
        )

        self.assertTrue((pack_path / "00_sheet").is_dir())
        self.assertTrue((pack_path / "01_parts").is_dir())
        self.assertTrue((pack_path / "02_multiview").is_dir())
        self.assertTrue((pack_path / "03_360").is_dir())
        self.assertTrue((pack_path / "04_mesh_raw").is_dir())
        self.assertTrue((pack_path / "parts_inventory.md").is_file())
        self.assertTrue((pack_path / "manifest.json").is_file())

        manifest = json.loads((pack_path / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["character_name"], "paladin_warrior")
        self.assertEqual(manifest["art_style"], "stylized_pbr")

    def test_validate_3d_character_mesh(self):
        """Tests GLB mesh validation on a synthetic minimal binary GLB."""
        glb_path = self.work_dir / "minimal_sample.glb"

        # Construct minimal valid binary glTF 2.0 file
        gltf_dict = {
            "asset": {"version": "2.0"},
            "accessors": [
                {
                    "count": 12,
                    "componentType": 5123,  # UNSIGNED_SHORT
                    "type": "SCALAR"
                },
                {
                    "count": 8,
                    "componentType": 5126,  # FLOAT
                    "type": "VEC3",
                    "min": [-0.5, 0.0, -0.5],
                    "max": [0.5, 1.8, 0.5]
                }
            ],
            "meshes": [
                {
                    "primitives": [
                        {
                            "indices": 0,
                            "attributes": {"POSITION": 1},
                            "mode": 4  # TRIANGLES
                        }
                    ]
                }
            ],
            "materials": [
                {
                    "pbrMetallicRoughness": {
                        "baseColorTexture": {"index": 0},
                        "metallicRoughnessTexture": {"index": 1}
                    },
                    "normalTexture": {"index": 2}
                }
            ]
        }
        json_bytes = json.dumps(gltf_dict).encode("utf-8")
        # Pad to 4-byte alignment
        padding = (4 - (len(json_bytes) % 4)) % 4
        json_bytes += b" " * padding

        chunk_len = len(json_bytes)
        total_len = 12 + 8 + chunk_len

        header = struct.pack("<4sII", b"glTF", 2, total_len)
        chunk_header = struct.pack("<I4s", chunk_len, b"JSON")

        with glb_path.open("wb") as f:
            f.write(header)
            f.write(chunk_header)
            f.write(json_bytes)

        rep = audit_glb_mesh(glb_path, max_triangles=10000)
        self.assertEqual(rep["triangles"], 4)  # 12 indices // 3 = 4 triangles
        self.assertEqual(rep["vertices"], 8)
        self.assertTrue(rep["pivot_at_ground"])
        self.assertTrue(rep["pbr_textures"]["base_color"])
        self.assertTrue(rep["pbr_textures"]["normal_map"])
        self.assertEqual(rep["verdict"], "PASS")


if __name__ == "__main__":
    unittest.main()
