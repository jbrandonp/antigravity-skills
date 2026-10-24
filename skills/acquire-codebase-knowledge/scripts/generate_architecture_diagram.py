#!/usr/bin/env python3
"""
generate_architecture_diagram.py — Generate Mermaid architecture & data flow diagrams from codebase analysis.
Produces valid Mermaid flowchart/graph diagrams for insertion into ARCHITECTURE.md.

Usage:
  python generate_architecture_diagram.py [--root DIR] [--output FILE] [--format {mermaid,markdown,json}]

Author: Antigravity Agentic Super Suite
"""

import os
import sys
import argparse
import re
import json
from pathlib import Path
from typing import Dict, List, Set, Tuple

EXCLUDE_DIRS = {
    "node_modules", ".git", "dist", "build", "out", ".next", ".nuxt",
    "__pycache__", ".venv", "venv", ".tox", "target", "vendor",
    "coverage", ".nyc_output", "generated", ".cache", ".turbo",
    "bin", "obj", "Intermediate", "Saved", "Binaries", "tools", "tests", "__tests__"
}

EXT_PATTERNS = {
    # Python
    ".py": [
        re.compile(r'^\s*(?:from|import)\s+([a-zA-Z0-9_\.]+)'),
    ],
    # JS/TS
    ".ts": [
        re.compile(r'import\s+.*?\s+from\s+[\'"]([^\'"]+)[\'"]'),
        re.compile(r'require\([\'"]([^\'"]+)[\'"]\)'),
    ],
    ".tsx": [
        re.compile(r'import\s+.*?\s+from\s+[\'"]([^\'"]+)[\'"]'),
        re.compile(r'require\([\'"]([^\'"]+)[\'"]\)'),
    ],
    ".js": [
        re.compile(r'import\s+.*?\s+from\s+[\'"]([^\'"]+)[\'"]'),
        re.compile(r'require\([\'"]([^\'"]+)[\'"]\)'),
    ],
    ".jsx": [
        re.compile(r'import\s+.*?\s+from\s+[\'"]([^\'"]+)[\'"]'),
        re.compile(r'require\([\'"]([^\'"]+)[\'"]\)'),
    ],
    # C/C++
    ".cpp": [re.compile(r'#include\s+["<]([a-zA-Z0-9_\./\-]+)[">]')],
    ".h": [re.compile(r'#include\s+["<]([a-zA-Z0-9_\./\-]+)[">]')],
    # Go
    ".go": [re.compile(r'"([a-zA-Z0-9_\./\-]+)"')],
    # Rust
    ".rs": [re.compile(r'(?:use|mod)\s+([a-zA-Z0-9_:]+)')],
}

EXTERNAL_MARKERS = {
    "Database": ["sqlite", "postgres", "mysql", "prisma", "typeorm", "sqlalchemy", "mongo", "redis", "dynamodb"],
    "HTTP / REST": ["axios", "fetch", "requests", "http", "curl", "express", "fastapi", "flask"],
    "Auth / Security": ["jwt", "oauth", "bcrypt", "passport", "firebase", "cognito", "next-auth"],
    "Storage / Cloud": ["s3", "gcs", "azure", "minio", "cloudinary", "blob"],
    "Queue / Events": ["kafka", "rabbitmq", "sqs", "pubsub", "bullmq", "celery", "nats"]
}


def sanitize_id(name: str) -> str:
    """Sanitize string for Mermaid node ID."""
    clean = re.sub(r'[^a-zA-Z0-9_]', '_', name)
    if clean and clean[0].isdigit():
        clean = "node_" + clean
    return clean or "root_node"


def find_top_modules(root_dir: Path) -> List[Path]:
    """Find top-level source modules / packages."""
    candidates = []
    # Check for src/, lib/, packages/, apps/, Source/
    common_roots = ["src", "lib", "packages", "apps", "Source", "app"]
    found_root = None
    for cr in common_roots:
        p = root_dir / cr
        if p.is_dir() and not any(part in EXCLUDE_DIRS for part in p.parts):
            found_root = p
            break

    search_dir = found_root if found_root else root_dir
    try:
        for item in sorted(search_dir.iterdir()):
            if item.is_dir() and item.name not in EXCLUDE_DIRS and not item.name.startswith('.'):
                candidates.append(item)
    except Exception:
        pass

    return candidates


def extract_internal_dependencies(root_dir: Path, modules: List[Path]) -> Dict[str, Set[str]]:
    """Extract inter-module dependencies from source files."""
    module_names = {m.name: m for m in modules}
    deps: Dict[str, Set[str]] = {m.name: set() for m in modules}

    for mod_name, mod_path in module_names.items():
        for root, dirs, files in os.walk(mod_path):
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith('.')]
            for f in files:
                ext = Path(f).suffix
                if ext in EXT_PATTERNS:
                    filepath = Path(root) / f
                    try:
                        with open(filepath, 'r', encoding='utf-8', errors='ignore') as fh:
                            content = fh.read()
                            for pattern in EXT_PATTERNS[ext]:
                                for match in pattern.findall(content):
                                    # Check if match references another module
                                    for other_mod in module_names:
                                        if other_mod != mod_name and (
                                            other_mod in match or
                                            f"/{other_mod}/" in match or
                                            match.startswith(other_mod)
                                        ):
                                            deps[mod_name].add(other_mod)
                    except Exception:
                        pass

    return deps


def detect_external_integrations(root_dir: Path) -> Dict[str, List[str]]:
    """Scan dependencies / imports for external systems."""
    found: Dict[str, List[str]] = {}
    content_samples = []

    # Read manifest files if available
    manifests = ["package.json", "requirements.txt", "pyproject.toml", "Cargo.toml", "go.mod"]
    for m in manifests:
        p = root_dir / m
        if p.is_file():
            try:
                with open(p, 'r', encoding='utf-8', errors='ignore') as fh:
                    content_samples.append(fh.read().lower())
            except Exception:
                pass

    joined = "\n".join(content_samples)
    for category, markers in EXTERNAL_MARKERS.items():
        matched = []
        for marker in markers:
            if marker in joined:
                matched.append(marker)
        if matched:
            found[category] = matched

    return found


def generate_mermaid_diagram(
    root_dir: Path,
    modules: List[Path],
    deps: Dict[str, Set[str]],
    externals: Dict[str, List[str]]
) -> str:
    """Generate Mermaid flowchart TD code."""
    lines = [
        "```mermaid",
        "flowchart TD",
        "    %% Core Architectural Subsystems and Data Flow",
        "    subgraph CoreApplication [\"Core Application Modules\"]"
    ]

    if not modules:
        lines.append("        AppEntry[\"Application Entrypoint / Core Logic\"]")
    else:
        for m in modules:
            m_id = sanitize_id(m.name)
            lines.append(f'        {m_id}["{m.name}"]')

    lines.append("    end")
    lines.append("")

    # Add inter-module connections
    has_edges = False
    for src, targets in deps.items():
        src_id = sanitize_id(src)
        for tgt in targets:
            tgt_id = sanitize_id(tgt)
            lines.append(f"    {src_id} --> {tgt_id}")
            has_edges = True

    if not has_edges and len(modules) > 1:
        # Fallback sequential flow
        for i in range(len(modules) - 1):
            s1 = sanitize_id(modules[i].name)
            s2 = sanitize_id(modules[i+1].name)
            lines.append(f"    {s1} -.-> {s2}")

    # Add External Integrations Subgraph
    if externals:
        lines.append("")
        lines.append("    subgraph ExternalServices [\"External Systems & Infrastructure\"]")
        for cat, items in externals.items():
            cat_id = sanitize_id(cat)
            label = f"{cat} ({', '.join(items[:3])})"
            lines.append(f'        {cat_id}[("{label}")]')
        lines.append("    end")
        lines.append("")

        # Connect core to externals
        entry_id = sanitize_id(modules[0].name) if modules else "AppEntry"
        for cat in externals:
            cat_id = sanitize_id(cat)
            lines.append(f"    {entry_id} -.-> {cat_id}")

    lines.append("```")
    return "\n".join(lines)


def generate_sequence_diagram(modules: List[Path], externals: Dict[str, List[str]]) -> str:
    """Generate Mermaid sequence diagram for request/command lifecycle."""
    lines = [
        "```mermaid",
        "sequenceDiagram",
        "    autonumber",
        "    actor Client as User / Client",
    ]

    m_names = [m.name for m in modules[:3]] if modules else ["Entrypoint", "Service", "Domain"]
    for m in m_names:
        m_id = sanitize_id(m)
        lines.append(f"    participant {m_id} as {m}")

    if externals:
        lines.append("    participant Ext as External System / DB")

    lines.append("")
    first_id = sanitize_id(m_names[0])
    lines.append(f"    Client->>{first_id}: Issue Command / Request")

    for i in range(len(m_names) - 1):
        c1 = sanitize_id(m_names[i])
        c2 = sanitize_id(m_names[i+1])
        lines.append(f"    {c1}->>{c2}: Process & Dispatch Task")

    if externals:
        last_id = sanitize_id(m_names[-1])
        lines.append(f"    {last_id}->>Ext: Query / Persist State")
        lines.append(f"    Ext-->>{last_id}: Return Result Data")

    for i in range(len(m_names) - 1, 0, -1):
        c1 = sanitize_id(m_names[i])
        c2 = sanitize_id(m_names[i-1])
        lines.append(f"    {c1}-->>{c2}: Return DTO / Domain Response")

    lines.append(f"    {first_id}-->>Client: Final Response / UI Feedback")
    lines.append("```")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Generate Mermaid architecture and data flow diagrams from codebase analysis."
    )
    parser.add_argument("--root", type=str, default=".", help="Project root directory (default: current directory)")
    parser.add_argument("--output", type=str, help="Output file path (default: stdout)")
    parser.add_argument(
        "--format",
        choices=["mermaid", "markdown", "json"],
        default="markdown",
        help="Output format: markdown with codeblocks, raw mermaid, or json"
    )
    args = parser.parse_args()

    root_path = Path(args.root).resolve()
    modules = find_top_modules(root_path)
    deps = extract_internal_dependencies(root_path, modules)
    externals = detect_external_integrations(root_path)

    flowchart = generate_mermaid_diagram(root_path, modules, deps, externals)
    sequence = generate_sequence_diagram(modules, externals)

    if args.format == "json":
        data = {
            "modules": [m.name for m in modules],
            "dependencies": {k: list(v) for k, v in deps.items()},
            "external_integrations": externals,
            "flowchart_mermaid": flowchart,
            "sequence_mermaid": sequence
        }
        output_text = json.dumps(data, indent=2)
    elif args.format == "mermaid":
        output_text = f"{flowchart}\n\n{sequence}"
    else:
        output_text = (
            "## 📐 Architecture Diagrams (Auto-Generated)\n\n"
            "### 1. System Component Flowchart\n\n"
            f"{flowchart}\n\n"
            "### 2. Request & Execution Sequence Flow\n\n"
            f"{sequence}\n"
        )

    if args.output:
        out_p = Path(args.output)
        out_p.parent.mkdir(parents=True, exist_ok=True)
        with open(out_p, 'w', encoding='utf-8') as fh:
            fh.write(output_text + "\n")
        print(f"Architecture diagrams written to: {args.output}", file=sys.stderr)
    else:
        print(output_text)

    return 0


if __name__ == "__main__":
    sys.exit(main())
