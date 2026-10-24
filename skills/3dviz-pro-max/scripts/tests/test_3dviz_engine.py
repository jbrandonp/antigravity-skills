#!/usr/bin/env python3
"""Automated Test Suite for 3Dviz Pro Max Engine & Tooling."""

import importlib.util
import json
from pathlib import Path
import platform
import subprocess
import tempfile
import unittest

sys_path = Path(__file__).resolve().parent.parent
import sys
if str(sys_path) not in sys.path:
    sys.path.insert(0, str(sys_path))

from audit_3d_scene import audit_threejs_scene
import catalog

# Dynamically import host-probe.py (hyphenated filename)
spec = importlib.util.spec_from_file_location("host_probe", sys_path / "host-probe.py")
host_probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(host_probe)


class Test3DVizEngine(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.work_dir = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_host_probe_hardware_detection(self):
        """Tests that host-probe reliably detects hardware specs."""
        system = platform.system()
        cpu = host_probe.cpu_info(system)
        mem = host_probe.memory_gb(system)
        gpu = host_probe.gpu_info(system)

        self.assertIsNotNone(cpu["logical_cores"])
        self.assertGreater(cpu["logical_cores"], 0)

        if system == "Windows":
            # On Windows, our winreg/ctypes upgrade must return valid brand and RAM
            self.assertIsNotNone(cpu["brand"], "CPU brand should be detected via winreg on Windows")
            self.assertIsNotNone(mem, "RAM should be detected via GlobalMemoryStatusEx on Windows")
            self.assertGreater(mem, 1.0)
            self.assertTrue(gpu["found"], "GPU should be detected via winreg on Windows")
            self.assertIn("DriverDesc", gpu["source"])

    def test_catalog_manifest_integrity(self):
        """Tests loading of catalog and uniqueness of knowledge records."""
        skill_root = sys_path.parent
        manifest, records, sources = catalog.load_catalog(root=skill_root, collection="all")

        self.assertGreater(len(records), 10, "Should load catalog records")
        ids = [r["id"] for r in records]
        self.assertEqual(len(ids), len(set(ids)), "All catalog record IDs must be strictly unique")

    def test_search_engine_bm25(self):
        """Tests BM25 search resolution for known blueprint queries."""
        search_script = sys_path / "search.py"
        res = subprocess.run(
            [sys.executable, str(search_script), "watermill"],
            capture_output=True,
            text=True,
            check=True
        )
        data = json.loads(res.stdout)
        self.assertEqual(data["status"], "candidates")
        self.assertGreater(len(data["results"]), 0)
        found_ids = [r["id"] for r in data["results"]]
        self.assertIn("knowledge.blueprint-watermill", found_ids)

    def test_audit_3d_scene_good_and_bad(self):
        """Tests the WebGL / Three.js code auditor on compliant and flawed scenes."""
        # 1. Compliant scene
        good_code = """
        import * as THREE from 'three';
        import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';

        const renderer = new THREE.WebGLRenderer();
        renderer.toneMapping = THREE.ACESFilmicToneMapping;
        renderer.outputColorSpace = THREE.SRGBColorSpace;
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

        const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
        const controls = new OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;

        const clock = new THREE.Clock();
        function animate() {
            requestAnimationFrame(animate);
            const rawDelta = clock.getDelta();
            const dt = Math.min(rawDelta, 0.1);
            renderer.render(scene, camera);
        }

        function cleanup(mesh) {
            mesh.geometry.dispose();
            mesh.material.dispose();
        }
        """
        good_file = self.work_dir / "good_scene.js"
        good_file.write_text(good_code, encoding="utf-8")

        rep_good = audit_threejs_scene(good_file)
        self.assertEqual(rep_good["verdict"], "PASS")
        self.assertGreaterEqual(rep_good["score"], 90)

        # 2. Flawed scene (unclamped pixel ratio, raw delta, near plane 0.0001, missing tone mapping)
        bad_code = """
        import * as THREE from 'three';
        import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';

        const renderer = new THREE.WebGLRenderer();
        renderer.setPixelRatio(window.devicePixelRatio); // Unclamped!

        const camera = new THREE.PerspectiveCamera(60, 1.0, 0.0001, 10000); // Bad near plane!
        const controls = new OrbitControls(camera, renderer.domElement);

        const clock = new THREE.Clock();
        function animate() {
            requestAnimationFrame(animate);
            const delta = clock.getDelta(); // Unbounded delta!
            renderer.render(scene, camera);
        }
        """
        bad_file = self.work_dir / "bad_scene.js"
        bad_file.write_text(bad_code, encoding="utf-8")

        rep_bad = audit_threejs_scene(bad_file)
        self.assertEqual(rep_bad["verdict"], "FAIL")
        self.assertLess(rep_bad["score"], 65)
        self.assertGreater(len(rep_bad["penalties"]), 2)


if __name__ == "__main__":
    unittest.main()
