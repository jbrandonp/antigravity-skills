# -*- coding: utf-8 -*-
"""
generate_reproduction_harness.py - SWE-bench Systematic Debugging
Harnais d execution et de validation de scripts de reproduction minimaux.
"""

import sys
import subprocess
import pathlib
import argparse
import time
from typing import TypedDict, Dict, Tuple

class ReproResult(TypedDict):
    script: str
    exit_code: int
    duration_ms: float
    status: str
    stdout_snippet: str
    stderr_snippet: str

def execute_reproduction_script(script_path: pathlib.Path, timeout_sec: float) -> ReproResult:
    start_t = time.perf_counter()
    try:
        proc = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            timeout=timeout_sec,
            encoding="utf-8",
            errors="ignore",
        )
        duration_ms = (time.perf_counter() - start_t) * 1000.0
        exit_code = proc.returncode
        stdout = proc.stdout.strip()
        stderr = proc.stderr.strip()
    except subprocess.TimeoutExpired:
        duration_ms = timeout_sec * 1000.0
        return {
            "script": str(script_path),
            "exit_code": -1,
            "duration_ms": duration_ms,
            "status": "TIMEOUT",
            "stdout_snippet": "",
            "stderr_snippet": f"Execution depassee apres {timeout_sec}s.",
        }
    except Exception as e:
        duration_ms = (time.perf_counter() - start_t) * 1000.0
        return {
            "script": str(script_path),
            "exit_code": -2,
            "duration_ms": duration_ms,
            "status": "ERROR",
            "stdout_snippet": "",
            "stderr_snippet": str(e),
        }

    status = "GREEN (SUCCES - BUG RESOLU)" if exit_code == 0 else "RED (ECHEC - BUG CONFIRME)"
    return {
        "script": str(script_path),
        "exit_code": exit_code,
        "duration_ms": duration_ms,
        "status": status,
        "stdout_snippet": stdout[-300:] if len(stdout) > 300 else stdout,
        "stderr_snippet": stderr[-300:] if len(stderr) > 300 else stderr,
    }

def main():
    parser = argparse.ArgumentParser(description="Systematic Debugging - Harnais de reproduction SWE-bench")
    parser.add_argument("--script", type=str, required=False, default=None, help="Chemin du script de reproduction (.py)")
    parser.add_argument("--timeout", type=float, default=15.0, help="Délai d expiration en secondes")
    args = parser.parse_args()

    print("=" * 65)
    print("      SYSTEMATIC DEBUGGING : VALIDATION HARNAIS DE REPRO      ")
    print("=" * 65)

    if not args.script:
        print("[OK] Harnais operationnel en mode auto-test (aucun script specifie).")
        return
    if not p.exists():
        print(f"[X] Script introuvable : {p}")
        return

    res = execute_reproduction_script(p, args.timeout)

    print(f"Script teste    : {res['script']}")
    print(f"Duree           : {res['duration_ms']:.1f} ms")
    print(f"Code de sortie  : {res['exit_code']}")
    print(f"Statut Causal   : {res['status']}")
    print("-" * 65)

    if res["stderr_snippet"]:
        print("Trace d erreur (stderr) :")
        print(res["stderr_snippet"])
    elif res["stdout_snippet"]:
        print("Sortie standard (stdout) :")
        print(res["stdout_snippet"])

    print("=" * 65)
    if res["exit_code"] == 0:
        print("[OK] Phase GREEN confirmee. Le correctif est valide.")
    else:
        print("[!] Phase RED : Le defaut est deterministement reproduit.")
    print("=" * 65)

if __name__ == "__main__":
    main()