#!/usr/bin/env python3
"""Docker & Kubernetes Infrastructure as Code (IaC) Linter.

Audits Dockerfiles and Kubernetes manifests for production readiness:
- Docker: Non-root USER, immutable tags (no :latest), cache cleanup
- Kubernetes: Resource limits (CPU/Memory), health probes (liveness/readiness), securityContext non-root
"""

import argparse
from pathlib import Path
import re
import sys


def lint_dockerfile(path: Path) -> list[dict[str, str | int]]:
    issues = []
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()

    has_user = False
    for idx, line in enumerate(lines, 1):
        clean = line.strip()
        if clean.startswith("#") or not clean:
            continue

        # Check for :latest in FROM
        if re.search(r"^FROM\s+[^\s:]+:latest\b", clean, re.IGNORECASE):
            issues.append({
                "severity": "WARN",
                "line": idx,
                "msg": "FROM uses mutable ':latest' tag. Pin an exact version or digest for reproducible builds."
            })

        # Check for USER declaration
        if re.match(r"^USER\s+", clean, re.IGNORECASE):
            has_user = True

        # Check for apt-get without clean
        if "apt-get install" in clean and not ("rm -rf /var/lib/apt/lists" in clean or "apt-get clean" in clean):
            issues.append({
                "severity": "WARN",
                "line": idx,
                "msg": "apt-get install without cleaning '/var/lib/apt/lists/*'. Bloats Docker image size."
            })

    if not has_user:
        issues.append({
            "severity": "FAIL",
            "line": len(lines),
            "msg": "Dockerfile lacks a non-root 'USER' directive. Containers must never run as root in production."
        })

    return issues


def lint_k8s_manifest(path: Path) -> list[dict[str, str | int]]:
    issues = []
    content = path.read_text(encoding="utf-8", errors="replace")
    lines = content.splitlines()

    # Only lint Deployment, StatefulSet, DaemonSet, Pod
    if not any(k in content for k in ["kind: Deployment", "kind: StatefulSet", "kind: DaemonSet", "kind: Pod"]):
        return []

    # 1. Check for resource limits
    if "resources:" not in content or "limits:" not in content:
        issues.append({
            "severity": "FAIL",
            "line": 1,
            "msg": "Kubernetes workload is missing 'resources.limits'. Uncapped pods can crash the entire node."
        })

    # 2. Check for livenessProbe and readinessProbe
    if "livenessProbe:" not in content:
        issues.append({
            "severity": "WARN",
            "line": 1,
            "msg": "Workload is missing 'livenessProbe'. Kubernetes cannot detect deadlocks or frozen processes."
        })

    if "readinessProbe:" not in content:
        issues.append({
            "severity": "WARN",
            "line": 1,
            "msg": "Workload is missing 'readinessProbe'. Traffic may be routed to uninitialized pods."
        })

    # 3. Check for securityContext
    if "runAsNonRoot: true" not in content:
        issues.append({
            "severity": "WARN",
            "line": 1,
            "msg": "Missing 'securityContext.runAsNonRoot: true'. Pod may run with root host privileges."
        })

    return issues


def main() -> None:
    parser = argparse.ArgumentParser(description="Docker & Kubernetes IaC Production Linter")
    parser.add_argument("path", help="Path to Dockerfile, Kubernetes YAML, or directory")
    args = parser.parse_args()

    target = Path(args.path)
    if not target.exists():
        print(f"Error: Path '{target}' not found.", file=sys.stderr)
        sys.exit(1)

    files = [target] if target.is_file() else sorted(target.glob("**/*"))
    total_fails = 0
    total_warns = 0

    print("=" * 65)
    print(" Docker & Kubernetes IaC Production Linter")
    print("=" * 65)

    audited = 0
    for f in files:
        if not f.is_file():
            continue

        issues = []
        if f.name.lower() in ("dockerfile", "containerfile") or f.name.lower().endswith(".dockerfile"):
            issues = lint_dockerfile(f)
            audited += 1
        elif f.suffix.lower() in (".yaml", ".yml"):
            issues = lint_k8s_manifest(f)
            if issues or any(k in f.read_text(encoding="utf-8", errors="replace") for k in ["kind: Deployment", "kind: Pod"]):
                audited += 1

        if not issues:
            continue

        fails = [i for i in issues if i["severity"] == "FAIL"]
        warns = [i for i in issues if i["severity"] == "WARN"]
        total_fails += len(fails)
        total_warns += len(warns)

        status = "[FAIL]" if fails else "[WARN]"
        print(f"{status} {f.name} ({len(fails)} errors, {len(warns)} warnings):")
        for i in issues:
            print(f"  Line {i['line']}: [{i['severity']}] {i['msg']}")

    print("-" * 65)
    print(f"Summary: {audited} files audited | Errors: {total_fails} | Warnings: {total_warns}")
    if total_fails > 0:
        print("Verdict: REJECTED (High-risk security or stability flaws detected)")
        sys.exit(1)
    else:
        print("Verdict: APPROVED (IaC compliant with production standards)")
        sys.exit(0)


if __name__ == "__main__":
    main()
