#!/usr/bin/env python3
"""Socratic Spec & Session Handoff Generator.

Compacts the current session state, active branch details, modified files,
and architectural decisions into a clean, standalone HANDOFF.md document.
Allows seamlessly resuming work in a fresh, unpolluted context window.
"""

import argparse
from pathlib import Path
import subprocess
import sys
import time

def get_git_info() -> dict:
    info = {"branch": "unknown", "status": "clean", "recent_commits": []}
    try:
        branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"], text=True, stderr=subprocess.DEVNULL).strip()
        info["branch"] = branch
    except Exception:
        pass

    try:
        status = subprocess.check_output(["git", "status", "--short"], text=True, stderr=subprocess.DEVNULL).strip()
        info["status"] = status if status else "clean (no unstaged changes)"
    except Exception:
        pass

    try:
        log = subprocess.check_output(["git", "log", "-n", "3", "--oneline"], text=True, stderr=subprocess.DEVNULL).strip()
        info["recent_commits"] = log.splitlines()
    except Exception:
        pass

    return info

def generate_handoff(title: str, summary: str, next_steps: list, out_path: Path) -> Path:
    git = get_git_info()
    now_str = time.strftime("%Y-%m-%d %H:%M:%S")

    commits_md = "\n".join(f"- `{c}`" for c in git["recent_commits"]) if git["recent_commits"] else "- None"
    steps_md = "\n".join(f"- [ ] {s}" for s in next_steps) if next_steps else "- [ ] Resume task implementation"

    content = f"""# 🤝 Session Handoff: {title}

**Generated at:** {now_str}  
**Active Branch:** `{git['branch']}`  

---

## 📌 Context & Executive Summary
{summary}

---

## 📁 Git Working State
```text
{git['status']}
```

### Recent Commits
{commits_md}

---

## 🚀 Priority Next Steps for the Next Agent
{steps_md}

---

## 💡 Key Architectural Invariants
1. Do not overwrite whole files; apply surgical edits only.
2. Verify all modifications with the local test suite before committing.
3. Keep the context clean: execute heavy commands via sandboxed buffers.
"""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(content.strip() + "\n", encoding="utf-8")
    return out_path

def main() -> None:
    parser = argparse.ArgumentParser(description="Generate clean session handoff document for agent context reset")
    parser.add_argument("--title", "-t", required=True, help="Title of the active feature or session")
    parser.add_argument("--summary", "-s", default="Work completed in the current session.", help="Executive summary")
    parser.add_argument("--next", "-n", action="append", default=[], help="Next step item (can be passed multiple times)")
    parser.add_argument("--output", "-o", default="HANDOFF.md", help="Output filepath (defaults to HANDOFF.md)")

    args = parser.parse_args()
    out_file = Path(args.output)
    result = generate_handoff(args.title, args.summary, args.next, out_file)
    print(f"[socratic-spec] Handoff document generated successfully at: {result}")

if __name__ == "__main__":
    main()
