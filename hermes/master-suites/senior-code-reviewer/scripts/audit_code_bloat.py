# -*- coding: utf-8 -*-
"""
audit_code_bloat.py - Swyx Smol Architect Standard
Detecteur d obesite logicielle, de sur-abstraction et de wrappers superflus.
"""

import ast
import os
import sys
import pathlib
import argparse
from typing import TypedDict, List, Dict, Tuple

class BloatFinding(TypedDict):
    file: str
    line: int
    category: str
    symbol: str
    reason: str

def check_file_bloat(file_path: pathlib.Path) -> List[BloatFinding]:
    findings: List[BloatFinding] = []
    try:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
        tree = ast.parse(content, filename=str(file_path))
    except Exception:
        return findings

    for node in ast.walk(tree):
        # 1. Detection des classes avec heritages profonds (>2 classes de base)
        if isinstance(node, ast.ClassDef):
            if len(node.bases) > 2:
                findings.append({
                    "file": str(file_path),
                    "line": node.lineno,
                    "category": "Over-Inheritance",
                    "symbol": node.name,
                    "reason": f"Classe '{node.name}' herite de {len(node.bases)} bases. Privilegier la composition plate.",
                })

        # 2. Fonctions triviales monopasse (wrappers pass-through inutiles)
        elif isinstance(node, ast.FunctionDef):
            # Si le corps ne contient qu'une seule instruction de return d un appel
            if len(node.body) == 1 and isinstance(node.body[0], ast.Return):
                ret_val = node.body[0].value
                if isinstance(ret_val, ast.Call) and not node.name.startswith("__"):
                    findings.append({
                        "file": str(file_path),
                        "line": node.lineno,
                        "category": "Trivial Wrapper",
                        "symbol": node.name,
                        "reason": f"Fonction '{node.name}' est un wrapper trivial d un seul appel. Envisager l inlining direct.",
                    })

    return findings

def main():
    parser = argparse.ArgumentParser(description="Smol Architect Code Bloat Auditor (Swyx Standard)")
    parser.add_argument("--dir", type=str, default=".", help="Dossier a auditer")
    parser.add_argument("--file", type=str, help="Fichier specifique a inspecter")
    parser.add_argument("--verbose", action="store_true", help="Afficher les explications detaillees")
    args = parser.parse_args()

    print("=" * 65)
    print("        SMOL ARCHITECT BLOAT AUDITOR (STANDARD SWYX)        ")
    print("=" * 65)

    all_findings: List[BloatFinding] = []
    ignored = {".git", ".venv", "venv", "node_modules", "__pycache__", "dist", "build"}

    if args.file:
        p = pathlib.Path(args.file)
        if p.exists():
            all_findings.extend(check_file_bloat(p))
    else:
        root = pathlib.Path(args.dir)
        for cur, dirs, files in os.walk(root):
            dirs[:] = [d for d in dirs if d not in ignored]
            for f in files:
                if f.endswith(".py"):
                    all_findings.extend(check_file_bloat(pathlib.Path(cur) / f))

    wrappers = sum(1 for f in all_findings if f["category"] == "Trivial Wrapper")
    inheritance = sum(1 for f in all_findings if f["category"] == "Over-Inheritance")

    smol_score = max(0, 100 - (wrappers * 5 + inheritance * 10))

    print(f"Total anomalies de complexite : {len(all_findings)}")
    print(f"  - Wrappers triviaux (Indirections inutiles) : {wrappers}")
    print(f"  - Heritages complexes (>2 bases)            : {inheritance}")
    print(f"Score d Architecture Minimaliste (Smol Score) : {smol_score} / 100")
    print("-" * 65)

    if all_findings:
        for f in all_findings[:15]:
            cat_tag = f"[{f['category']}]"
            print(f"{cat_tag:<22} {pathlib.Path(f['file']).name}:{f['line']} -> {f['symbol']}")
            if args.verbose:
                print(f"                       Detail: {f['reason']}")
    else:
        print("[OK] Architecture 100% smol et directe. Aucune sur-abstraction.")

    print("=" * 65)

if __name__ == "__main__":
    main()