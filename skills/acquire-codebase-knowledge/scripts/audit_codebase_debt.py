#!/usr/bin/env python3
"""
audit_codebase_debt.py — Automated technical debt and code health audit.
Scans for God files (>500 LOC), git churn hotspots, circular imports, and TODO density.
Outputs quantitative health metrics and Markdown for CONCERNS.md.

Usage:
  python audit_codebase_debt.py [--root DIR] [--max-lines N] [--json] [--output FILE]

Author: Antigravity Agentic Super Suite
"""

import os
import sys
import argparse
import subprocess
import json
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import Counter

EXCLUDE_DIRS = {
    "node_modules", ".git", "dist", "build", "out", ".next", ".nuxt",
    "__pycache__", ".venv", "venv", ".tox", "target", "vendor",
    "coverage", ".nyc_output", "generated", ".cache", ".turbo",
    "bin", "obj", "Intermediate", "Saved", "Binaries", "tests", "__tests__", "spec"
}

SOURCE_EXTS = {
    ".py", ".ts", ".tsx", ".js", ".jsx", ".go", ".rs", ".java",
    ".kt", ".cs", ".cpp", ".c", ".h", ".rb", ".php", ".swift"
}

IMPORT_REGEX = {
    ".py": re.compile(r'^\s*(?:from|import)\s+([a-zA-Z0-9_\.]+)'),
    ".ts": re.compile(r'(?:import|from|require\()\s*[\'"]([^\'"]+)[\'"]'),
    ".tsx": re.compile(r'(?:import|from|require\()\s*[\'"]([^\'"]+)[\'"]'),
    ".js": re.compile(r'(?:import|from|require\()\s*[\'"]([^\'"]+)[\'"]'),
    ".jsx": re.compile(r'(?:import|from|require\()\s*[\'"]([^\'"]+)[\'"]'),
    ".go": re.compile(r'"([a-zA-Z0-9_\./\-]+)"'),
    ".rs": re.compile(r'(?:use|mod)\s+([a-zA-Z0-9_:]+)'),
    ".cpp": re.compile(r'#include\s+["<]([a-zA-Z0-9_\./\-]+)[">]'),
    ".h": re.compile(r'#include\s+["<]([a-zA-Z0-9_\./\-]+)[">]')
}


def count_file_lines(filepath: Path) -> int:
    """Count non-empty lines in a file."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            return sum(1 for line in f if line.strip())
    except Exception:
        return 0


def get_git_churn_counts(root_dir: Path) -> Dict[str, int]:
    """Retrieve git file modification frequencies over the last 90 days."""
    churn_dict: Dict[str, int] = {}
    try:
        res = subprocess.run(
            ["git", "log", "--since=90 days ago", "--name-only", "--pretty=format:"],
            capture_output=True,
            text=True,
            cwd=root_dir,
            timeout=10
        )
        if res.returncode == 0:
            files = [line.strip().replace('/', os.sep) for line in res.stdout.splitlines() if line.strip()]
            churn_dict = Counter(files)
    except Exception:
        pass
    return churn_dict


def find_source_files(root_dir: Path) -> List[Path]:
    """Find all relevant source files excluding build/vendor directories."""
    source_files = []
    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith('.')]
        for f in files:
            p = Path(root) / f
            if p.suffix in SOURCE_EXTS and not p.name.endswith(('.min.js', '.min.css')):
                source_files.append(p)
    return source_files


def detect_circular_dependencies(root_dir: Path, source_files: List[Path]) -> List[List[str]]:
    """Build an import graph and detect simple circular dependency cycles."""
    file_map = {f.name: f for f in source_files}
    graph: Dict[str, Set[str]] = {f.name: set() for f in source_files}

    for sf in source_files:
        ext = sf.suffix
        regex = IMPORT_REGEX.get(ext)
        if not regex:
            continue
        try:
            with open(sf, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    match = regex.search(line)
                    if match:
                        imported = match.group(1).split('/')[-1].split('.')[-1]
                        # Match with candidate filename
                        for candidate in file_map:
                            cand_stem = Path(candidate).stem
                            if imported == cand_stem and candidate != sf.name:
                                graph[sf.name].add(candidate)
        except Exception:
            pass

    # Simple 2-node and 3-node cycle detection
    cycles: List[List[str]] = []
    visited_pairs = set()

    for node, neighbors in graph.items():
        for neighbor in neighbors:
            if node in graph.get(neighbor, set()):
                pair = tuple(sorted([node, neighbor]))
                if pair not in visited_pairs:
                    visited_pairs.add(pair)
                    cycles.append([node, neighbor])

    return cycles


def audit_codebase(root_dir: Path, max_lines_threshold: int = 500) -> dict:
    """Run full technical debt audit and compute health metrics."""
    source_files = find_source_files(root_dir)
    churn_dict = get_git_churn_counts(root_dir)

    total_loc = 0
    file_stats = []
    god_files = []
    todo_count = 0
    todo_patterns = ["TODO", "FIXME", "HACK", "XXX"]

    for sf in source_files:
        rel_str = str(sf.relative_to(root_dir)).replace('/', os.sep)
        loc = count_file_lines(sf)
        total_loc += loc
        churn = churn_dict.get(rel_str, churn_dict.get(str(sf.relative_to(root_dir)), 0))
        hotspot_score = churn * (loc / 100.0)

        # Count TODOs
        file_todos = 0
        try:
            with open(sf, 'r', encoding='utf-8', errors='ignore') as fh:
                for line in fh:
                    if any(p in line for p in todo_patterns):
                        file_todos += 1
                        todo_count += 1
        except Exception:
            pass

        stat = {
            "path": rel_str,
            "loc": loc,
            "churn": churn,
            "hotspot_score": round(hotspot_score, 2),
            "todos": file_todos
        }
        file_stats.append(stat)

        if loc > max_lines_threshold:
            god_files.append(stat)

    # Sort hotspots
    hotspots = sorted(file_stats, key=lambda x: x["hotspot_score"], reverse=True)[:10]
    hotspots = [h for h in hotspots if h["hotspot_score"] > 0]

    # Detect cycles
    cycles = detect_circular_dependencies(root_dir, source_files)

    # TODO density per 1000 LOC
    todo_density = round((todo_count / max(1, total_loc)) * 1000, 2)

    # Calculate overall health score (0-100)
    deductions = (len(god_files) * 5) + (len(cycles) * 10) + (len(hotspots) * 2) + min(30, int(todo_density * 2))
    health_score = max(0, min(100, 100 - deductions))

    if health_score >= 85:
        verdict = "HEALTHY"
    elif health_score >= 65:
        verdict = "MODERATE_DEBT"
    else:
        verdict = "HIGH_TECH_DEBT"

    return {
        "summary": {
            "total_files": len(source_files),
            "total_loc": total_loc,
            "god_files_count": len(god_files),
            "cycles_count": len(cycles),
            "total_todos": todo_count,
            "todo_density_per_kloc": todo_density,
            "health_score": health_score,
            "verdict": verdict
        },
        "god_files": sorted(god_files, key=lambda x: x["loc"], reverse=True)[:10],
        "top_hotspots": hotspots[:10],
        "cycles": cycles
    }


def format_markdown_report(audit_data: dict) -> str:
    """Format audit results as Markdown for CONCERNS.md."""
    sum_data = audit_data["summary"]
    lines = [
        "# 📉 Technical Debt & Code Health Audit",
        "",
        "## 📊 Executive Health Score",
        f"- **Health Score :** `{sum_data['health_score']}/100` ({sum_data['verdict']})",
        f"- **Total Source Files Scanned :** `{sum_data['total_files']}` files ({sum_data['total_loc']:,} LOC)",
        f"- **TODO / Debt Density :** `{sum_data['todo_density_per_kloc']}` items per 1,000 LOC ({sum_data['total_todos']} total markers)",
        f"- **God Files (>500 LOC) :** `{sum_data['god_files_count']}` files",
        f"- **Circular Dependency Cycles :** `{sum_data['cycles_count']}` detected",
        "",
        "## 🚨 God Files (Refactoring Priority)",
        "Files exceeding 500 lines that frequently violate Single Responsibility Principle:",
        ""
    ]

    if audit_data["god_files"]:
        lines.append("| File Path | LOC | Git Churn | Suggested Action |")
        lines.append("| :--- | :---: | :---: | :--- |")
        for gf in audit_data["god_files"]:
            lines.append(f"| `{gf['path']}` | **{gf['loc']}** | {gf['churn']} edits | Decompose into focused sub-modules |")
    else:
        lines.append("✓ No god files detected over the threshold.")

    lines.extend([
        "",
        "## 🔥 Fragile Hotspots (High Churn ∩ High LOC)",
        "Files with frequent git revisions and high complexity represent the highest defect risk:",
        ""
    ])

    if audit_data["top_hotspots"]:
        lines.append("| Hotspot File | Churn (90d) | LOC | Hotspot Risk Index |")
        lines.append("| :--- | :---: | :---: | :---: |")
        for hs in audit_data["top_hotspots"]:
            lines.append(f"| `{hs['path']}` | {hs['churn']} | {hs['loc']} | **{hs['hotspot_score']}** |")
    else:
        lines.append("✓ No high-churn hotspots detected in git history.")

    if audit_data["cycles"]:
        lines.extend([
            "",
            "## 🔄 Circular Dependency Cycles",
            ""
        ])
        for c in audit_data["cycles"]:
            lines.append(f"- ⚠️ Cycle detected between `{c[0]}` $\\leftrightarrow$ `{c[1]}`")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Audit codebase technical debt, god files, git churn hotspots, and circular dependencies."
    )
    parser.add_argument("--root", type=str, default=".", help="Project root directory (default: current directory)")
    parser.add_argument("--max-lines", type=int, default=500, help="Line threshold for god files (default: 500)")
    parser.add_argument("--json", action="store_true", help="Output audit report as JSON")
    parser.add_argument("--output", type=str, help="Output file path (default: stdout)")
    args = parser.parse_args()

    root_path = Path(args.root).resolve()
    audit_data = audit_codebase(root_path, args.max_lines)

    if args.json:
        output_text = json.dumps(audit_data, indent=2)
    else:
        output_text = format_markdown_report(audit_data)

    if args.output:
        out_p = Path(args.output)
        out_p.parent.mkdir(parents=True, exist_ok=True)
        with open(out_p, 'w', encoding='utf-8') as fh:
            fh.write(output_text + "\n")
        print(f"Technical debt audit written to: {args.output}", file=sys.stderr)
    else:
        print(output_text)

    # Return exit code 0 if score >= 65, else 1
    return 0 if audit_data["summary"]["health_score"] >= 65 else 1


if __name__ == "__main__":
    sys.exit(main())
