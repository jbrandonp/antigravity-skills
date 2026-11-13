"""Automated End-to-End Verification Test Suite for the 11_mega-narrative-worldbuilding-and-cinematic-suite.

Executes comprehensive tests across:
- YAML parsing & edge-case resiliency
- Project scaffolding
- Character lifecycle & resurrection detection
- Chekhov's gun paradox & orphan tracking
- Show, Don't Tell perception filters linter
- Causality score calculation
- Cinematic prompt compiler multi-model outputs
- FFmpeg automated assembly script generation
"""

import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path

from story_continuity_compiler import (
    StoryContinuityCompiler,
    parse_frontmatter,
    scaffold_project,
)
from cinematic_prompt_compiler import (
    CAMERA_MOVEMENTS,
    FILM_STYLES,
    LIGHTING_SETUPS,
    compile_shot,
)
from ffmpeg_story_assembler import generate_assembly_script
from story_bible_manager import StoryBibleManager


class TestNarrativeSuite(unittest.TestCase):
    def setUp(self):
        """Create a temporary directory for isolated file testing."""
        self.test_dir = tempfile.mkdtemp(prefix="narrative_test_")

    def tearDown(self):
        """Clean up temporary test artifacts."""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    # ---------------------------------------------------------
    # 1. Frontmatter Parser & Edge Cases
    # ---------------------------------------------------------
    def test_parse_frontmatter_standard(self):
        content = """---
title: "L'Ombre du Désert"
chapter: 1
alive: true
death_chapter: null
characters_present:
  - malik
  - sora
---
Corps du texte ici.
"""
        meta, body = parse_frontmatter(content)
        self.assertEqual(meta["title"], "L'Ombre du Désert")
        self.assertEqual(meta["chapter"], 1)
        self.assertTrue(meta["alive"])
        self.assertIsNone(meta["death_chapter"])
        self.assertEqual(meta["characters_present"], ["malik", "sora"])
        self.assertIn("Corps du texte ici.", body)

    def test_parse_frontmatter_corrupted_or_empty(self):
        # Empty text
        meta, body = parse_frontmatter("")
        self.assertEqual(meta, {})
        self.assertEqual(body, "")

        # Text without YAML
        meta, body = parse_frontmatter("# Simple Markdown\nSans frontmatter.")
        self.assertEqual(meta, {})
        self.assertIn("Simple Markdown", body)

        # Incomplete YAML delimiters
        meta, body = parse_frontmatter("---\ntitle: test\n corps sans fermeture")
        self.assertEqual(meta, {})

    # ---------------------------------------------------------
    # 2. Project Scaffolding
    # ---------------------------------------------------------
    def test_scaffold_project(self):
        proj_path = Path(self.test_dir) / "scaffold_demo"
        scaffold_project(proj_path, "Test Project")

        self.assertTrue((proj_path / ".story" / "config.yaml").exists())
        self.assertTrue((proj_path / ".story" / "promises.yaml").exists())
        self.assertTrue((proj_path / "bible" / "characters" / "malik.md").exists())
        self.assertTrue((proj_path / "acts" / "act-1" / "chapter-01.md").exists())

    # ---------------------------------------------------------
    # 3. Clean Story Audit (Expected 100/100)
    # ---------------------------------------------------------
    def test_clean_story_audit(self):
        proj_path = Path(self.test_dir) / "clean_demo"
        scaffold_project(proj_path, "Clean Saga")

        compiler = StoryContinuityCompiler(str(proj_path))
        results = compiler.run_all()

        self.assertEqual(results["status"], "PASS")
        self.assertEqual(results["consistency_score"], 100.0)
        self.assertEqual(results["critical_errors_count"], 0)
        self.assertEqual(results["warnings_count"], 0)

    # ---------------------------------------------------------
    # 4. Illegal Resurrection Detection
    # ---------------------------------------------------------
    def test_illegal_resurrection_detected(self):
        proj_path = Path(self.test_dir) / "resurrection_demo"
        scaffold_project(proj_path, "Ghost Saga")

        # Mark character dead in chapter 1
        char_file = proj_path / "bible" / "characters" / "malik.md"
        char_file.write_text("""---
id: malik
name: "Malik"
alive: false
death_chapter: 1
---
Malik est mort héroïquement au chapitre 1.
""", encoding="utf-8")

        # Add Chapter 2 where Malik speaks or is present
        chap2_file = proj_path / "acts" / "act-1" / "chapter-02.md"
        chap2_file.write_text("""---
chapter: 2
title: "Le Lendemain"
characters_present:
  - malik
---
# Chapitre 2
Malik s'assit au coin du feu.
""", encoding="utf-8")

        compiler = StoryContinuityCompiler(str(proj_path))
        results = compiler.run_all()

        self.assertEqual(results["status"], "FAIL")
        self.assertGreaterEqual(results["critical_errors_count"], 1)
        self.assertEqual(results["errors"][0]["type"], "ILLEGAL_RESURRECTION")
        self.assertIn("died in Chapter 1", results["errors"][0]["message"])

    # ---------------------------------------------------------
    # 5. Chekhov's Gun Paradox & Orphan Detection
    # ---------------------------------------------------------
    def test_chekhov_timeline_paradox(self):
        proj_path = Path(self.test_dir) / "chekhov_demo"
        scaffold_project(proj_path, "Paradox Saga")

        # Setup in Ch. 3, Payoff in Ch. 1 -> Impossible
        promises_file = proj_path / ".story" / "promises.yaml"
        promises_file.write_text("""- id: paradox-dagger
  setup_chapter: 3
  payoff_chapter: 1
  resolved: true
""", encoding="utf-8")

        compiler = StoryContinuityCompiler(str(proj_path))
        results = compiler.run_all()

        self.assertEqual(results["status"], "FAIL")
        self.assertTrue(any(e["type"] == "TIMELINE_PARADOX" for e in results["errors"]))

    # ---------------------------------------------------------
    # 6. Show, Don't Tell Perception Filter Linter
    # ---------------------------------------------------------
    def test_show_dont_tell_filter_detection(self):
        proj_path = Path(self.test_dir) / "filter_demo"
        scaffold_project(proj_path, "Filter Saga")

        chap1 = proj_path / "acts" / "act-1" / "chapter-01.md"
        chap1.write_text("""---
chapter: 1
title: "La Nuit"
---
Il vit la lumière vaciller. Elle sentit la fraîcheur de la pierre.
Un frisson lui parcourut l'échine alors qu'un silence de plomb s'installait.
""", encoding="utf-8")

        compiler = StoryContinuityCompiler(str(proj_path))
        results = compiler.run_all()

        # Should catch filter words
        self.assertGreaterEqual(results["style_nits_count"], 3)
        self.assertLess(results["consistency_score"], 100.0)

    # ---------------------------------------------------------
    # 7. Causality Ratio Calculation (Therefore / But vs And Then)
    # ---------------------------------------------------------
    def test_weak_causality_flow(self):
        proj_path = Path(self.test_dir) / "causality_demo"
        scaffold_project(proj_path, "Weak Flow Saga")

        chap1 = proj_path / "acts" / "act-1" / "chapter-01.md"
        chap1.write_text("""---
chapter: 1
title: "La Liste de Courses"
---
Bob entra dans la pièce. Et ensuite il ouvrit le tiroir. Et ensuite il prit la clé.
Et alors il sortit dans la rue. Puis après il monta dans la voiture.
""", encoding="utf-8")

        compiler = StoryContinuityCompiler(str(proj_path))
        results = compiler.run_all()

        self.assertLess(results["causality_ratio"], 50.0)
        self.assertTrue(any(w["type"] == "WEAK_CAUSALITY_FLOW" for w in results["warnings"]))

    # ---------------------------------------------------------
    # 8. Cinematic Prompt Compiler
    # ---------------------------------------------------------
    def test_cinematic_prompt_compiler(self):
        for style_key in FILM_STYLES.keys():
            res = compile_shot(
                shot_id="TEST_01",
                subject="Cyberpunk detective",
                action="examining a holographic skull",
                camera_move="dolly_in",
                lighting="neon_noir",
                style=style_key,
                voice_text="The city is whispering secrets.",
                bgm_mood="ambient synthwave",
            )
            self.assertIn("midjourney_v6", res["prompts"])
            self.assertIn("runway_kling_video", res["prompts"])
            self.assertIn("elevenlabs_voice", res["prompts"])
            self.assertIn("suno_bgm", res["prompts"])
            self.assertIn("--v 6.1", res["prompts"]["midjourney_v6"])
            self.assertIn("The city is whispering secrets.", res["prompts"]["elevenlabs_voice"])

    # ---------------------------------------------------------
    # 9. FFmpeg Story Assembler Script Generation
    # ---------------------------------------------------------
    def test_ffmpeg_assembler_single_and_multi(self):
        # Single video test
        script_single = generate_assembly_script(
            video_files=["clip1.mp4"],
            bgm_file="music.mp3",
            voiceover_file="voice.mp3",
            output_file="out_single.mp4",
        )
        self.assertIn("amix=inputs=2", script_single)
        self.assertIn("loudnorm=I=-14", script_single)
        self.assertIn("out_single.mp4", script_single)

        # Multi-video with crossfade test
        script_multi = generate_assembly_script(
            video_files=["c1.mp4", "c2.mp4", "c3.mp4"],
            bgm_file="bg.mp3",
            voiceover_file="vo.mp3",
            output_file="out_multi.mp4",
            transition_duration=0.6,
        )
        self.assertIn("xfade=transition=fade", script_multi)
        self.assertIn("[a_mixed]loudnorm", script_multi)
        self.assertIn("out_multi.mp4", script_multi)

    # ---------------------------------------------------------
    # 10. Story Bible Manager & Obsidian Dashboard Export
    # ---------------------------------------------------------
    def test_story_bible_manager(self):
        proj_path = Path(self.test_dir) / "bible_demo"
        scaffold_project(proj_path, "Bible Saga")

        manager = StoryBibleManager(str(proj_path))
        manager.scan_bible()

        self.assertIn("malik", manager.entities)
        self.assertEqual(manager.entities["malik"]["category"], "characters")

        dashboard = manager.generate_obsidian_dashboard()
        self.assertIn("Story Bible Master Dashboard", dashboard)
        self.assertIn('FROM "bible/characters"', dashboard)

    # ---------------------------------------------------------
    # 11. Pacing Trajectory & Mermaid Graph Generation
    # ---------------------------------------------------------
    def test_pacing_and_mermaid_graph(self):
        proj_path = Path(self.test_dir) / "pacing_demo"
        scaffold_project(proj_path, "Pacing Saga")

        compiler = StoryContinuityCompiler(str(proj_path))
        compiler.load_characters()
        compiler.load_chapters()

        pacing = compiler.compute_pacing_and_tension()
        self.assertGreaterEqual(len(pacing), 1)
        self.assertIn("tension_score", pacing[0])

        graph = compiler.generate_mermaid_graph()
        self.assertIn("```mermaid", graph)
        self.assertIn("graph TD", graph)
        self.assertIn("malik", graph)


if __name__ == "__main__":
    unittest.main()
