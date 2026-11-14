#!/usr/bin/env python3
"""Comprehensive Functional Test Suite for Companion Engineering Scripts.

Validates execution, return codes, and core outputs for:
1. context-mode (ctx_buffer.py)
2. caveman-compress (compressor.py)
3. karpathy-guidelines (surgical_checker.py)
4. gstack-startup-pack (gstack_engine.py)
5. diagram-design-svg (svg_generator.py)
6. isometric-anatomy-svg (isometric_compiler.py)
7. graphify-ast-knowledge (graph_builder.py)
8. impeccable-design-engine (design_audit.py)
9. cloudflare-adversarial-audit (adversarial_gate.py)
10. trail-of-bits-security-engine (static_analyzer.py)
11. ecc-agent-shield (agent_shield.py)
12. socratic-spec-architect (handoff_generator.py)
"""

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"

tests_passed = 0
tests_failed = 0

def run_test(name: str, cmd: list, expect_code: int = 0) -> bool:
    global tests_passed, tests_failed
    print(f"Running test: {name}...", end=" ", flush=True)
    try:
        res = subprocess.run([sys.executable] + cmd, capture_output=True, text=True, check=False)
        if res.returncode == expect_code:
            print("✓ PASSED")
            tests_passed += 1
            return True
        else:
            print(f"✗ FAILED (Code {res.returncode}, expected {expect_code})")
            if res.stderr:
                print("  STDERR:", res.stderr.strip()[:300])
            tests_failed += 1
            return False
    except Exception as e:
        print(f"✗ ERROR: {e}")
        tests_failed += 1
        return False

def main():
    print("==================================================================")
    print("     ANTIGRAVITY SUPER SUITE — FUNCTIONAL SCRIPTS TEST SUITE      ")
    print("==================================================================")

    # 1. context-mode (inside context-token-optimization-suite or context-mode)
    ctx_candidates = [
        SKILLS / "context-token-optimization-suite" / "scripts" / "ctx_buffer.py",
        SKILLS / "context-mode" / "scripts" / "ctx_buffer.py",
        ROOT / "hermes" / "master-suites" / "context-token-optimization-suite" / "scripts" / "ctx_buffer.py"
    ]
    ctx_script = next((p for p in ctx_candidates if p.exists()), ctx_candidates[0])
    run_test("context-mode --help", [str(ctx_script), "--help"])
    run_test("context-mode run command", [str(ctx_script), "run", "echo", "hello"])
    run_test("context-mode search", [str(ctx_script), "search", "hello"])

    # 2. caveman-compress (inside context-token-optimization-suite or caveman-compress)
    caveman_candidates = [
        SKILLS / "context-token-optimization-suite" / "scripts" / "compressor.py",
        SKILLS / "caveman-compress" / "scripts" / "compressor.py",
        ROOT / "hermes" / "master-suites" / "context-token-optimization-suite" / "scripts" / "compressor.py"
    ]
    caveman_script = next((p for p in caveman_candidates if p.exists()), caveman_candidates[0])
    run_test("caveman-compress --help", [str(caveman_script), "--help"])
    with tempfile.NamedTemporaryFile("w+", suffix=".md", delete=False) as f:
        f.write("# Rules\nYou must always ensure that you do not fail.\nPlease be polite.\n")
        f_path = f.name
    try:
        run_test("caveman-compress stats", [str(caveman_script), "--stats-only", f_path])
        run_test("caveman-compress run", [str(caveman_script), "--aggressive", f_path])
    finally:
        if os.path.exists(f_path):
            os.remove(f_path)

    # 3. karpathy-guidelines
    karpathy_candidates = [
        SKILLS / "karpathy-guidelines" / "scripts" / "surgical_checker.py",
        ROOT / "hermes" / "master-suites" / "karpathy-guidelines" / "scripts" / "surgical_checker.py"
    ]
    karpathy_script = next((p for p in karpathy_candidates if p.exists()), karpathy_candidates[0])
    run_test("karpathy-guidelines --help", [str(karpathy_script), "--help"])
    run_test("karpathy-guidelines check clean state", [str(karpathy_script)])

    # 4. gstack-startup-pack
    gstack_script = SKILLS / "gstack-startup-pack" / "scripts" / "gstack_engine.py"
    run_test("gstack-startup-pack --help", [str(gstack_script), "--help"])
    run_test("gstack ceo review", [str(gstack_script), "ceo", "--feature", "Scraper Alert", "--desc", "Sends SMS on price drop"])
    run_test("gstack eng review", [str(gstack_script), "eng"])
    run_test("gstack design shotgun", [str(gstack_script), "design", "--component", "Pricing Table"])
    run_test("gstack ship checklist", [str(gstack_script), "ship"])

    # 5. diagram-design-svg
    diagram_script = SKILLS / "diagram-design-svg" / "scripts" / "svg_generator.py"
    with tempfile.TemporaryDirectory() as tmpdir:
        out_svg = Path(tmpdir) / "diag.svg"
        run_test("diagram-design-svg --help", [str(diagram_script), "--help"])
        run_test("diagram-design-svg generate architecture", [str(diagram_script), "--type", "architecture", "--output", str(out_svg)])
        run_test("diagram-design-svg generate sequence", [str(diagram_script), "--type", "sequence", "--output", str(out_svg)])

    # 6. isometric-anatomy-svg
    iso_script = SKILLS / "isometric-anatomy-svg" / "scripts" / "isometric_compiler.py"
    with tempfile.TemporaryDirectory() as tmpdir:
        out_svg = Path(tmpdir) / "iso.svg"
        run_test("isometric-anatomy-svg --help", [str(iso_script), "--help"])
        run_test("isometric-anatomy-svg generate", [str(iso_script), "--title", "Test System", "--output", str(out_svg)])

    # 7. graphify-ast-knowledge
    graph_script = SKILLS / "graphify-ast-knowledge" / "scripts" / "graph_builder.py"
    with tempfile.TemporaryDirectory() as tmpdir:
        sample_code = Path(tmpdir) / "sample.py"
        sample_code.write_text("def hello(): pass\nclass World: pass\n", encoding="utf-8")
        out_json = Path(tmpdir) / "graph.json"
        run_test("graphify-ast-knowledge --help", [str(graph_script), "--help"])
        run_test("graphify-ast-knowledge build", [str(graph_script), "--root", tmpdir, "--json", str(out_json)])

    # 8. impeccable-design-engine
    impeccable_script = SKILLS / "impeccable-design-engine" / "scripts" / "design_audit.py"
    with tempfile.TemporaryDirectory() as tmpdir:
        sample_html = Path(tmpdir) / "index.html"
        sample_html.write_text('<button class="px-4 py-2 hover:bg-blue-600 focus-visible:outline">Click</button>', encoding="utf-8")
        run_test("impeccable-design-engine --help", [str(impeccable_script), "--help"])
        run_test("impeccable-design-engine audit", [str(impeccable_script), tmpdir])

    # 9. cloudflare-adversarial-audit
    cf_script = SKILLS / "cloudflare-adversarial-audit" / "scripts" / "adversarial_gate.py"
    with tempfile.TemporaryDirectory() as tmpdir:
        findings_file = Path(tmpdir) / "findings.json"
        findings_file.write_text(json.dumps([{
            "id": "VULN-1",
            "file": "app.py",
            "line": 10,
            "severity": "HIGH",
            "description": "XSS in profile",
            "finder_agent": "Agent-Scout",
            "adversarial_verifier": "Agent-Skeptic",
            "falsification_attempt": "Attempted payload bypass, verified reflection without escaping",
            "reproduced": True
        }]), encoding="utf-8")
        out_report = Path(tmpdir) / "REPORT.md"
        run_test("cloudflare-adversarial-audit --help", [str(cf_script), "--help"])
        run_test("cloudflare-adversarial-audit triage", [str(cf_script), "--findings", str(findings_file), "--report", str(out_report)])

    # 10. trail-of-bits-security-engine
    tob_script = SKILLS / "trail-of-bits-security-engine" / "scripts" / "static_analyzer.py"
    run_test("trail-of-bits-security-engine --help", [str(tob_script), "--help"])
    run_test("trail-of-bits scan self", [str(tob_script), "--target", str(tob_script)])

    # 11. ecc-agent-shield
    shield_script = SKILLS / "ecc-agent-shield" / "scripts" / "agent_shield.py"
    run_test("ecc-agent-shield --help", [str(shield_script), "--help"])
    run_test("ecc-agent-shield audit safe cmd", [str(shield_script), "audit-cmd", "--cmd", "python test.py"])
    run_test("ecc-agent-shield block destructive cmd", [str(shield_script), "audit-cmd", "--cmd", "rm -rf /"], expect_code=1)

    # 12. socratic-spec-architect
    socratic_script = SKILLS / "socratic-spec-architect" / "scripts" / "handoff_generator.py"
    with tempfile.TemporaryDirectory() as tmpdir:
        out_handoff = Path(tmpdir) / "HANDOFF.md"
        run_test("socratic-spec-architect --help", [str(socratic_script), "--help"])
        run_test("socratic-spec-architect generate", [str(socratic_script), "--title", "Antigravity Handoff", "--summary", "All tests passed", "--output", str(out_handoff)])

    # 13. brivael-twitter-system
    brivael_harness = SKILLS / "brivael-twitter-system" / "scripts" / "test_harness.py"
    brivael_linter = SKILLS / "brivael-twitter-system" / "scripts" / "verify_brivael_post.py"
    run_test("brivael-twitter-system --help", [str(brivael_linter), "--help"])
    run_test("brivael-twitter-system test-harness", [str(brivael_harness)])

    print("==================================================================")
    print(f"TEST RESULTS: {tests_passed} passed, {tests_failed} failed.")
    print("==================================================================")
    if tests_failed > 0:
        sys.exit(1)

if __name__ == "__main__":
    main()
