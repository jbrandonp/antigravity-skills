"""Stop hook: keep the agent working until the owner ends the session.

Allows the stop only if `.claude/ALLOW_STOP` exists, or if `.claude/session_window.json`
has an "until" time in the past. Otherwise exit code 2 blocks the stop and stderr goes
back to the agent as the reason.
"""
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    json.load(sys.stdin)
except Exception:
    pass

root = Path(os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd()))
if (root / ".claude" / "ALLOW_STOP").exists():
    sys.exit(0)
window = root / ".claude" / "session_window.json"
if window.exists():
    try:
        until = datetime.fromisoformat(json.loads(window.read_text(encoding="utf-8-sig"))["until"])
        if until.tzinfo is None:
            until = until.astimezone()
        if datetime.now(timezone.utc) >= until:
            sys.exit(0)
    except Exception:
        pass
sys.stderr.write(
    "The owner has not ended this session. Do not stop. If you lost context, follow CLAUDE.md section 1. "
    "Take the next item from Docs/TODO.md. If it is empty, run the acceptance test (Docs/TASK.md section 2), "
    "queue fixes for the weakest areas, and continue. Keep capturing progress screenshots (TASK.md section 18)."
)
sys.exit(2)
