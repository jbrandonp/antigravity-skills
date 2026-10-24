"""SessionStart (compact/resume) hook: re-anchor the agent on its state files."""
from datetime import datetime, timezone

print(
    f"Context was compacted or the session was resumed (UTC {datetime.now(timezone.utc):%Y-%m-%d %H:%M}). "
    "Before any other action, re-read CLAUDE.md, Docs/PLAN.md, Docs/TODO.md, the last three entries of "
    "Docs/DEVLOG.md and Docs/STATS.json, then continue the current milestone. "
    "Capture a progress screenshot of the feature you are working on (Docs/TASK.md section 18)."
)
