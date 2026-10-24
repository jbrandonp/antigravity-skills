#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
security_audit.py — Audit de sécurité automatisé combiné (v2, 2026-08-14)
Lance les 4 scanners sur un repo cible et produit un rapport markdown.

v2 : exclusion .venv/node_modules/.git (gitleaks), parsing semgrep robuste
     (verdict basé sur results JSON, pas sur le code retour), résumé osv
     par sévérité, timeouts et erreurs explicites. Jamais de résultats simulés.

Usage:
    python security_audit.py <repo_path> [--output rapport.md] [--skip gitleaks,semgrep,osv]
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone

TOOLS_DIR = os.path.expanduser("~/.hermes/security-tools")
BIN_DIR = os.path.join(TOOLS_DIR, "bin")
SEMGREP = os.path.join(TOOLS_DIR, "venv", "Scripts", "semgrep.exe")
GITLEAKS = os.path.join(BIN_DIR, "gitleaks.exe")
OSV = os.path.join(BIN_DIR, "osv-scanner.exe")
GITLEAKS_CONFIG = os.path.join(TOOLS_DIR, "gitleaks.toml")

# Exclusions globales (deps, builds, VCS) — mêmes patterns que .gitignore classique
IGNORED_DIRS = [".venv", "venv", "node_modules", ".git", "build", "dist", "target",
                "site-packages", "__pycache__", ".next", ".cache", "vendor"]

GITLEAKS_TOML = """# gitleaks.toml — config globale d'audit (créée par security_audit.py)
title = "Hermes security audit global config"

[extend]
useDefault = true

[[allowlist]]
description = "Dépendances, builds et artefacts — hors périmètre du code source"
paths = [
  ".venv/", "venv/", "node_modules/", ".git/", "build/", "dist/", "target/",
  "site-packages/", "__pycache__/", ".next/", ".cache/", "vendor/",
  "*.min.js", "*.map", "package-lock.json", "yarn.lock", "poetry.lock",
]
"""


def ensure_gitleaks_config():
    if not os.path.exists(GITLEAKS_CONFIG):
        with open(GITLEAKS_CONFIG, "w", encoding="utf-8") as f:
            f.write(GITLEAKS_TOML)


def run(cmd, timeout=600):
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout,
                           errors="replace", shell=False)
        return p.returncode, p.stdout or "", p.stderr or ""
    except subprocess.TimeoutExpired:
        return 124, "", "TIMEOUT"
    except FileNotFoundError:
        return 127, "", f"OUTIL INTROUVABLE: {cmd[0]}"


def scan_gitleaks(repo):
    if not os.path.exists(GITLEAKS):
        return "SKIP", "gitleaks non installé"
    ensure_gitleaks_config()
    print("  → gitleaks (secrets, exclusions deps)...", flush=True)
    rc, out, err = run([GITLEAKS, "dir", repo, "--redact", "-v", "--config", GITLEAKS_CONFIG], timeout=600)
    findings = []
    for line in (out + "\n" + err).splitlines():
        if line.startswith("Finding:"):
            findings.append(line.strip())
    leaks = err.count("leaks found")
    status = "FINDINGS" if "leaks found:" in err and "leaks found: 0" not in err else "OK"
    report = f"{len(findings)} findings (secrets)\n" + "\n".join(findings[:50])
    if not findings:
        report = out[-2000:] + err[-2000:]
    return status, report


def scan_semgrep(repo):
    if not os.path.exists(SEMGREP):
        return "SKIP", "semgrep non installé"
    print("  → semgrep (config auto, ~1-3 min)...", flush=True)
    rc, out, err = run([SEMGREP, "scan", "--config", "auto", "--json", repo], timeout=900)
    try:
        data = json.loads(out)
        findings = data.get("results", [])
        if not findings:
            return "OK", f"0 finding sur {len(data.get('paths', {}).get('scanned', []))} fichiers (règles: {len(data.get('rules', []))})"
        lines = [f"{len(findings)} findings:"]
        for f in findings[:100]:
            sev = (f.get("extra", {}).get("severity") or "?").upper()
            path = (f.get("path") or "?").replace(repo, ".").replace("\\", "/")
            line = f.get("start", {}).get("line", "?")
            rule = f.get("check_id", "?").split(".")[-1]
            msg = (f.get("extra", {}).get("message") or "").splitlines()[0][:200]
            lines.append(f"[{sev}] {path}:{line} ({rule}) {msg}")
        return "FINDINGS", "\n".join(lines)
    except Exception:
        return ("OK" if rc == 0 else "FINDINGS"), (out or err)[-8000:]


def scan_osv(repo):
    if not os.path.exists(OSV):
        return "SKIP", "osv-scanner non installé"
    print("  → osv-scanner (CVE dépendances)...", flush=True)
    rc, out, err = run([OSV, "scan", "-r", "--format", "json", repo], timeout=900)
    if "No package sources found" in (out + err):
        return "OK", "Aucun manifest de dépendances trouvé à la racine (rien à scanner)"
    try:
        data = json.loads(out)
        results = data.get("results", [])
        vulns = []
        for r in results:
            for pkg in r.get("packages", []):
                name = pkg.get("package", {}).get("name", "?")
                version = pkg.get("version", "?")
                for v in pkg.get("vulnerabilities", []):
                    sev = "?"
                    for db in [v.get("database_specific", {})]:
                        sev = db.get("severity", "?")
                    vulns.append({
                        "id": v.get("id", "?"),
                        "aliases": (v.get("aliases") or [])[:2],
                        "severity": sev,
                        "pkg": name,
                        "version": version,
                        "summary": (v.get("summary") or "")[:160],
                    })
        if not vulns:
            return "OK", "0 vulnérabilité connue (CVE) dans les dépendances"
        sev_counts = {}
        for v in vulns:
            s = str(v["severity"]).upper()[:8]
            sev_counts[s] = sev_counts.get(s, 0) + 1
        lines = [f"{len(vulns)} vulnérabilités : " + ", ".join(f"{k}={v}" for k, v in sev_counts.items())]
        for v in vulns[:60]:
            lines.append(f"[{v['severity']}] {v['pkg']}@{v['version']} — {v['id']} ({', '.join(v['aliases'])}) — {v['summary']}")
        return "FINDINGS", "\n".join(lines)
    except Exception:
        return ("OK" if rc == 0 else "FINDINGS"), (out or err)[-8000:]


def scan_promptfoo(target):
    pf = shutil.which("promptfoo")
    if not pf:
        return "SKIP", "promptfoo non installé (npm i -g promptfoo)"
    print(f"  → promptfoo redteam sur {target}...", flush=True)
    rc, out, err = run([pf, "redteam", "run", "--target", target, "--output", "redteam-report.json"], timeout=1800)
    return ("OK" if rc == 0 else "FINDINGS"), (out or err)[-4000:]


def main():
    ap = argparse.ArgumentParser(description="Audit sécurité combiné v2")
    ap.add_argument("repo", help="Chemin du repo/projet à auditer")
    ap.add_argument("--output", default="security-audit-report.md")
    ap.add_argument("--skip", default="", help="Scanners à sauter: gitleaks,semgrep,osv,promptfoo")
    ap.add_argument("--llm-target", default="", help="URL d'une API LLM à red-teamer (optionnel)")
    ap.add_argument("--cron", action="store_true", help="Mode cron : ne print que le résumé compact (stdout = message)")
    args = ap.parse_args()

    repo = os.path.abspath(args.repo)
    if not os.path.isdir(repo):
        print(f"ERREUR: {repo} n'existe pas")
        sys.exit(1)

    skip = set(s.strip() for s in args.skip.split(",") if s.strip())
    print(f"=== AUDIT SÉCURITÉ {repo} — {datetime.now(timezone.utc):%Y-%m-%d %H:%M UTC} ===")

    results = {}
    if "gitleaks" not in skip:
        results["gitleaks"] = scan_gitleaks(repo)
    if "semgrep" not in skip:
        results["semgrep"] = scan_semgrep(repo)
    if "osv" not in skip:
        results["osv"] = scan_osv(repo)
    if "promptfoo" not in skip and args.llm_target:
        results["promptfoo"] = scan_promptfoo(args.llm_target)

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        f"# Rapport d'audit sécurité — {os.path.basename(repo)}",
        "",
        f"**Date :** {ts} · **Périmètre :** `{repo}`",
        "",
        "| Scanner | Verdict | Détail |",
        "|---------|---------|--------|",
    ]
    verdict_icon = {"OK": "🟢", "FINDINGS": "🔴", "ERROR": "🟠", "SKIP": "⚪"}
    for name in ["gitleaks", "semgrep", "osv", "promptfoo"]:
        if name not in results:
            continue
        status, out = results[name]
        detail = out.splitlines()[0][:90] if out else status
        lines.append(f"| {name} | {verdict_icon.get(status, '🟠')} {status} | {detail} |")

    lines.append("")
    for name, (status, out) in results.items():
        lines.append(f"## {name} — {status}")
        lines.append("```")
        lines.append(out[:12000])
        lines.append("```")
        lines.append("")

    report = "\n".join(lines)
    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(report)

    n_findings = sum(1 for s, _ in results.values() if s == "FINDINGS")
    if args.cron:
        print(f"🔒 Audit sécurité {os.path.basename(repo)} — {datetime.now(timezone.utc):%d/%m %H:%M UTC}")
        for name in ["gitleaks", "semgrep", "osv", "promptfoo"]:
            if name not in results:
                continue
            status, out = results[name]
            detail = out.splitlines()[0][:100] if out else status
            print(f"- {name}: {verdict_icon.get(status, '🟠')} {status} — {detail}")
        print(f"Rapport: {os.path.abspath(args.output)}")
        sys.exit(1 if n_findings else 0)
    print(f"\n=== TERMINÉ — {len(results)} scanners, {n_findings} avec findings ===")
    print(f"Rapport : {os.path.abspath(args.output)}")


if __name__ == "__main__":
    main()
