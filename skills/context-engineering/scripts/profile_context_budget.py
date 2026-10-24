# -*- coding: utf-8 -*-
"""
profile_context_budget.py - Addy Osmani / Anthropic Context Engineering
Profileur de consommation de tokens et detecteur de pollution de contexte.
"""

import os
import sys
import pathlib
import argparse
from typing import List, Tuple

def estimate_tokens(char_count: int) -> int:
    """Estimation heuristique : environ 4 caracteres par token en code."""
    return char_count // 4

def profile_directory(root_dir: pathlib.Path, top_n: int = 10) -> Tuple[int, int, List[Tuple[pathlib.Path, int, int]]]:
    ignored = {".git", ".svn", "node_modules", "venv", ".venv", "__pycache__", "dist", "build", ".gemini"}
    file_stats: List[Tuple[pathlib.Path, int, int]] = []
    total_bytes = 0
    total_tokens = 0

    for current, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in ignored]
        for f in files:
            p = pathlib.Path(current) / f
            try:
                size = p.stat().st_size
                # Ignorer les binaires ou fichiers > 2 Mo
                if size > 2 * 1024 * 1024:
                    continue
                content = p.read_text(encoding="utf-8", errors="ignore")
                char_count = len(content)
                tok = estimate_tokens(char_count)
                total_bytes += size
                total_tokens += tok
                file_stats.append((p, size, tok))
            except Exception:
                continue

    file_stats.sort(key=lambda x: x[2], reverse=True)
    return total_bytes, total_tokens, file_stats[:top_n]

def main():
    parser = argparse.ArgumentParser(description="Context Engineering - Profileur de tokens")
    parser.add_argument("--dir", type=str, default=".", help="Dossier a analyser")
    parser.add_argument("--top", type=int, default=10, help="Nombre de fichiers les plus lourds a afficher")
    args = parser.parse_args()

    print("=" * 65)
    print("      CONTEXT ENGINEERING : PROFILEUR DE BUDGET DE TOKENS       ")
    print("=" * 65)

    root = pathlib.Path(args.dir)
    total_bytes, total_tokens, top_files = profile_directory(root, top_n=args.top)

    print(f"Espace analyse : {root.resolve()}")
    print(f"Poids total    : {total_bytes / 1024:.1f} KB")
    print(f"Tokens estimes : ~{total_tokens:,} tokens")
    print("-" * 65)
    print(f"Top {len(top_files)} fichiers les plus consommateurs de tokens :")
    print(f"{'Fichier':<45} | {'Taille':<8} | {'Tokens est.'}")
    print("-" * 65)

    for p, size, tok in top_files:
        rel_path = str(p.relative_to(root)) if root in p.parents else p.name
        if len(rel_path) > 43:
            rel_path = "..." + rel_path[-40:]
        print(f"{rel_path:<45} | {size/1024:6.1f} KB | ~{tok:<6,}")

    print("=" * 65)
    if total_tokens > 100_000:
        print("[CONSEIL] Budget eleve (>100k tokens). Utiliser 'Select-String' ou grep au lieu de lire les fichiers entiers.")
    else:
        print("[OK] Budget contexte sain.")
    print("=" * 65)

if __name__ == "__main__":
    main()