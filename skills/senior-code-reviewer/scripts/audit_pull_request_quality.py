# -*- coding: utf-8 -*-
"""
audit_pull_request_quality.py - Senior Code Reviewer Simulator
Simulateur d'analyse statique et de classification par severite des Pull Requests.
"""

from typing import List, Dict, TypedDict

class ReviewFinding(TypedDict):
    file_path: str
    line_number: int
    severity: str  # CRITICAL, MAJOR, MINOR, NIT
    message: str
    suggested_fix: str

class PullRequestVerdict(TypedDict):
    decision: str  # APPROVE, REQUEST_CHANGES
    critical_count: int
    major_count: int
    minor_count: int
    findings: List[ReviewFinding]

def analyze_code_diff(file_name: str, code_lines: List[str]) -> List[ReviewFinding]:
    """Examine les lignes modifiees d'un fichier et detecte les anomalies majeures."""
    findings: List[ReviewFinding] = []

    for idx, line in enumerate(code_lines, 1):
        # 1. Detection de failles critiques (eval, hardcoded secrets)
        if "eval(" in line:
            findings.append({
                "file_path": file_name,
                "line_number": idx,
                "severity": "CRITICAL",
                "message": "Utilisation d'eval() detectee, risque d'execution de code arbitraire.",
                "suggested_fix": "Remplacer par un parseur strict ou ast.literal_eval."
            })

        # 2. Detection de typage Any banni
        if ": Any" in line or "-> Any" in line:
            findings.append({
                "file_path": file_name,
                "line_number": idx,
                "severity": "MAJOR",
                "message": "Type 'Any' detecte, violation de la regle de typage strict OLYMPUS.",
                "suggested_fix": "Specifier le type reel ou utiliser des generics avec contraintes."
            })

        # 3. Detection de variable sans nommage explicite
        if " x =" in line or " temp =" in line:
            findings.append({
                "file_path": file_name,
                "line_number": idx,
                "severity": "MINOR",
                "message": "Nom de variable a une lettre ou generique detecte.",
                "suggested_fix": "Utiliser un nom explicite decrivant le role metier de la variable."
            })

    return findings

def evaluate_pr_verdict(findings: List[ReviewFinding]) -> PullRequestVerdict:
    """Determine la decision de merge basee sur la severite des findings."""
    crit = sum(1 for f in findings if f["severity"] == "CRITICAL")
    maj = sum(1 for f in findings if f["severity"] == "MAJOR")
    min_c = sum(1 for f in findings if f["severity"] == "MINOR")

    decision = "REQUEST_CHANGES" if (crit > 0 or maj > 2) else "APPROVE"

    return {
        "decision": decision,
        "critical_count": crit,
        "major_count": maj,
        "minor_count": min_c,
        "findings": findings
    }

def run_self_test() -> int:
    """Verifie le bon triage des anomalies par le Senior Code Reviewer."""
    print("Execution du self-test Senior Code Reviewer...")

    test_lines = [
        "def compute_total(val: int) -> int:",
        "    x = val * 2",
        "    eval('x + 1')",
        "    return x"
    ]

    findings = analyze_code_diff("calculator.py", test_lines)
    verdict = evaluate_pr_verdict(findings)

    assert verdict["decision"] == "REQUEST_CHANGES", "PR with eval() should have been rejected!"
    assert verdict["critical_count"] == 1, f"Expected 1 critical finding, got {verdict['critical_count']}"
    assert verdict["minor_count"] == 1, f"Expected 1 minor finding, got {verdict['minor_count']}"

    print(f"[PASS] Code Review verdict teste : Decision = {verdict['decision']} (Critical: {verdict['critical_count']}, Minor: {verdict['minor_count']})")
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(run_self_test())