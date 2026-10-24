#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "pillow",
#     "scipy",
# ]
# ///
"""Automated Test Suite for 2D Pixel Sprite Sheet Pipeline Tools."""

import json
from pathlib import Path
import tempfile
import unittest

import numpy as np
from PIL import Image

# Import tools from parent directory
sys_path = Path(__file__).resolve().parent.parent
import sys
if str(sys_path) not in sys.path:
    sys.path.insert(0, str(sys_path))

from audit_pixel_art import audit_sprite
from extract_sprite_frames import extract_frames
from pack_spritesheet import pack_spritesheet
from pixel_snap import snap_image, PRESET_PALETTES, hex_to_rgb


class TestPixelPipeline(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.work_dir = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_pixel_snap_and_palette_quantization(self):
        """Tests that pixel snapping quantizes colors and removes chroma."""
        # Create a synthetic 128x128 image with pitch=16 (8x8 cells)
        arr = np.full((128, 128, 3), [0, 255, 0], dtype=np.uint8)  # Solid green
        # Draw a 4x4 cell character in center (from (32,32) to (96,96))
        # Add random subtle noise to simulate diffusion mixels
        noise = np.random.randint(-10, 10, size=(64, 64, 3), dtype=np.int16)
        base_color = np.array([200, 30, 40], dtype=np.int16)
        noisy_char = np.clip(base_color + noise, 0, 255).astype(np.uint8)
        arr[32:96, 32:96] = noisy_char

        input_img = Image.fromarray(arr, mode="RGB")

        snapped, stats = snap_image(
            input_img,
            target_pitch=16,
            palette_name="pico-8",
            chroma_hex="#00FF00",
            chroma_tolerance=35,
        )

        self.assertEqual(snapped.size, (8, 8))
        self.assertEqual(stats["cell_pitch"], 16)
        self.assertEqual(stats["palette_preset"], "pico-8")

        # Non-transparent pixels must all belong to Pico-8 palette
        snapped_arr = np.array(snapped)
        opaque_mask = snapped_arr[:, :, 3] > 0
        self.assertTrue(np.any(opaque_mask), "Should have opaque character pixels")

        pico_rgbs = {hex_to_rgb(h) for h in PRESET_PALETTES["pico-8"]}
        opaque_pixels = snapped_arr[opaque_mask][:, :3]
        for px in opaque_pixels:
            self.assertIn(tuple(px), pico_rgbs, "All pixels must conform to Pico-8 palette")

    def test_extract_connected_frames(self):
        """Tests connected component frame extraction and reading order."""
        # Create a 300x150 pose board with 2 distinct figures on green background
        board = np.full((150, 300, 3), [0, 255, 0], dtype=np.uint8)
        # Figure 1 at X=30..70, Y=30..90
        board[30:90, 30:70] = [255, 0, 0]
        # Figure 2 at X=150..190, Y=30..90
        board[30:90, 150:190] = [0, 0, 255]

        board_img = Image.fromarray(board, mode="RGB")
        frames, _ = extract_frames(
            board_img,
            chroma_hex="#00FF00",
            min_width=20,
            min_height=20,
            padding=2,
            row_height_cluster=100
        )

        self.assertEqual(len(frames), 2, "Must extract exactly 2 frames")
        # Reading order: left figure first, right figure second
        frame_0_center = frames[0][1][0]
        frame_1_center = frames[1][1][0]
        self.assertLess(frame_0_center, frame_1_center, "Frames must be sorted left to right")

    def test_pack_spritesheet_ground_alignment(self):
        """Tests packing frames into a spritesheet with ground baseline stabilization."""
        # Create 3 frames of different heights (e.g. standing, crouching, jumping)
        fpaths = []
        for i, h in enumerate([40, 25, 35]):
            img = Image.new("RGBA", (32, 50), (0, 0, 0, 0))
            # Draw a block that touches ground at Y=48
            draw_arr = np.array(img)
            draw_arr[48-h:48, 10:22] = [255, 200, 50, 255]
            f_img = Image.fromarray(draw_arr, mode="RGBA")
            fp = self.work_dir / f"frame_{i:02d}.png"
            f_img.save(fp)
            fpaths.append(fp)

        sheet, meta = pack_spritesheet(
            fpaths,
            align_mode="ground",
            bottom_margin=4,
            enforce_power_of_two=True,
            fps=12,
        )

        self.assertEqual(meta["meta"]["frame_count"], 3)
        self.assertEqual(meta["meta"]["fps"], 12)
        # Verify power of two dimensions
        w, h = sheet.size
        self.assertEqual(w & (w - 1), 0, "Width must be power of two")
        self.assertEqual(h & (h - 1), 0, "Height must be power of two")

    def test_audit_pixel_art_quality(self):
        """Tests the quality gate mixel and alpha auditor."""
        # 1. Clean sprite
        clean_img = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
        clean_arr = np.array(clean_img)
        clean_arr[4:28, 4:28] = [255, 0, 0, 255]  # Crisp 1-bit alpha
        clean_path = self.work_dir / "clean.png"
        Image.fromarray(clean_arr).save(clean_path)

        rep_clean = audit_sprite(clean_path, max_colors=16)
        self.assertEqual(rep_clean["verdict"], "PASS")
        self.assertGreaterEqual(rep_clean["score"], 90)

        # 2. Dirty sprite with semi-transparent anti-aliasing halos
        dirty_arr = clean_arr.copy()
        dirty_arr[2:4, 4:28] = [200, 50, 50, 128]  # Semi-transparent halo!
        dirty_path = self.work_dir / "dirty.png"
        Image.fromarray(dirty_arr).save(dirty_path)

        rep_dirty = audit_sprite(dirty_path, max_colors=16)
        self.assertGreater(rep_dirty["metrics"]["semi_transparent_pixels"], 0)
        self.assertLess(rep_dirty["score"], rep_clean["score"])


if __name__ == "__main__":
    unittest.main()
