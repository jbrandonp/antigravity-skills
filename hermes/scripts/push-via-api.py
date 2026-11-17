#!/usr/bin/env python3
"""Push incrémental v2 : pousse UNIQUEMENT les fichiers listés vers origin/main via l'API.
Évite de repousser les 347 fichiers déjà poussés dans 99bec074."""
import base64, json, subprocess, os

REPO = "jbrandonp/antigravity-skills"
WORK = "/srv/brandon-ai/workspaces/antigravity-sync"

def gh(endpoint):
    out = subprocess.run(["gh", "api", f"repos/{REPO}/{endpoint}"], capture_output=True, text=True)
    if out.returncode != 0:
        raise RuntimeError(f"{endpoint}: {out.stderr[:300]}")
    return json.loads(out.stdout)

def gh_input(endpoint, payload):
    out = subprocess.run(["gh", "api", f"repos/{REPO}/{endpoint}", "--input", "-"],
                         input=json.dumps(payload), capture_output=True, text=True)
    if out.returncode != 0:
        raise RuntimeError(f"{endpoint}: {out.stderr[:300]}")
    return json.loads(out.stdout)

os.chdir(WORK)
head = gh("git/ref/heads/main")["object"]["sha"]
base_tree = gh(f"git/commits/{head}")["tree"]["sha"]
print(f"HEAD={head[:8]}")

# Fichiers à pousser : (chemin_repo, chemin_source)
FILES = [
    ("skills/ai-redteaming-adversarial-security-suite/SKILL.md",
     "/home/arthur/.hermes/skills/ai-redteaming-adversarial-security-suite/SKILL.md"),
    ("skills/ai-redteaming-adversarial-security-suite/scripts/godmode_load_godmode.py",
     "/home/arthur/.hermes/skills/ai-redteaming-adversarial-security-suite/scripts/godmode_load_godmode.py"),
    ("hermes/master-suites/ai-redteaming-adversarial-security-suite/SKILL.md",
     "/home/arthur/.hermes/skills/ai-redteaming-adversarial-security-suite/SKILL.md"),
    ("skills/watchtower-digest/SKILL.md",
     "/home/arthur/.hermes/skills/watchtower-digest/SKILL.md"),
    ("hermes/master-suites/watchtower-digest/SKILL.md",
     "/home/arthur/.hermes/skills/watchtower-digest/SKILL.md"),
    ("hermes/scripts/jev-decide.py", "/home/arthur/.hermes/scripts/jev-decide.py"),
    ("hermes/scripts/jev-filter.py", "/home/arthur/.hermes/scripts/jev-filter.py"),
    ("hermes/scripts/jev-calibrate.py", "/srv/brandon-ai/workspaces/jev-calibrate.py"),
    ("hermes/scripts/health-check.sh", "/home/arthur/.hermes/scripts/health-check.sh"),
]

tree_entries = []
for repo_path, src in FILES:
    if not os.path.exists(src):
        print(f"SKIP (source absente): {src}")
        continue
    with open(src, "rb") as f:
        content = base64.b64encode(f.read()).decode()
    blob = gh_input("git/blobs", {"content": content, "encoding": "base64"})
    tree_entries.append({"path": repo_path, "mode": "100644", "type": "blob", "sha": blob["sha"]})
    print(f"blob {repo_path} ok ({os.path.getsize(src)} o)")

tree = gh_input("git/trees", {"base_tree": base_tree, "tree": tree_entries})
commit = gh_input("git/commits", {
    "message": "feat(hermes): add Jev decisions system + sync patched skills\n\n"
               "- Add hermes/scripts/jev-decide.py: calibrated email triage (structured state, "
               "atomic phishing signals, confidence routing) — v3.1, validated on 10-case suite\n"
               "- Add hermes/scripts/jev-filter.py: 3-mode relevance pre-filter (articles/findings/tenders), "
               "per-mode thresholds\n"
               "- Add hermes/scripts/jev-calibrate.py: reusable calibration suite\n"
               "- Add hermes/scripts/health-check.sh: service health check\n"
               "- Update watchtower-digest SKILL.md: mandatory Jev pre-filter step before GLM scoring\n"
               "- Update ai-redteaming SKILL.md: Hermes gotcha (homoglyph quarantine) + fixed loader paths",
    "tree": tree["sha"],
    "parents": [head],
})
gh_input("git/refs/heads/main", {"sha": commit["sha"], "force": False})
print(f"PUSHED commit {commit['sha'][:8]} to main ({len(tree_entries)} files)")
