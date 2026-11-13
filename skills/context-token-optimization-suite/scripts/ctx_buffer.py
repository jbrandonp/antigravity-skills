#!/usr/bin/env python3
"""Context-Mode SQLite FTS5 Terminal Buffer & Log Reducer.

Captures verbose command execution outputs (test suites, builds, linters, scrapers)
into an indexed local SQLite database using Full-Text Search (FTS5).
Surfaces only high-level summary lines to the AI agent, allowing surgical BM25
lookups to eliminate 90-99% of context window pollution.
"""

import argparse
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import time
import uuid

DB_PATH = Path(os.environ.get("CTX_BUFFER_DB", Path.home() / ".antigravity" / "context_buffer.db"))

def get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA synchronous = NORMAL;")
    conn.execute(
        """
        CREATE VIRTUAL TABLE IF NOT EXISTS command_logs USING fts5(
            session_id,
            command,
            output,
            exit_code UNINDEXED,
            timestamp UNINDEXED
        );
        """
    )
    conn.commit()
    return conn

def cmd_run(args: argparse.Namespace) -> int:
    cmd_str = " ".join(args.command)
    if not cmd_str.strip():
        print("Error: No command provided to run.", file=sys.stderr)
        return 1

    session_id = args.session or str(uuid.uuid4())[:8]
    start_time = time.time()

    proc = subprocess.run(
        cmd_str,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace"
    )

    duration = time.time() - start_time
    output_text = proc.stdout or ""
    lines = output_text.splitlines()
    byte_size = len(output_text.encode("utf-8"))

    conn = get_connection()
    conn.execute(
        """
        INSERT INTO command_logs(session_id, command, output, exit_code, timestamp)
        VALUES (?, ?, ?, ?, ?);
        """,
        (session_id, cmd_str, output_text, proc.returncode, time.strftime("%Y-%m-%d %H:%M:%S"))
    )
    conn.commit()
    conn.close()

    status_tag = "SUCCESS" if proc.returncode == 0 else f"FAILED (code {proc.returncode})"
    print(f"[context-mode] {status_tag} | Command: `{cmd_str}`")
    print(f"Captured: {len(lines)} lines ({byte_size / 1024:.1f} KB) in {duration:.2f}s | Session: {session_id}")
    if proc.returncode != 0:
        # Show last 10 error lines automatically for quick triage
        tail_count = min(10, len(lines))
        print("\n--- [Tail 10 lines of failure output] ---")
        for line in lines[-tail_count:]:
            print(f"  {line}")
        print(f"\n[Tip] Query full trace: python -m ctx_buffer search {session_id} \"error\"")
    return proc.returncode

def cmd_search(args: argparse.Namespace) -> int:
    conn = get_connection()
    query = args.query
    session_id = args.session

    cursor = conn.cursor()
    if session_id:
        cursor.execute(
            """
            SELECT session_id, command, snippet(command_logs, 2, '>>>', '<<<', '...', 25), exit_code
            FROM command_logs
            WHERE command_logs MATCH ? AND session_id = ?
            ORDER BY rank
            LIMIT ?;
            """,
            (query, session_id, args.limit)
        )
    else:
        cursor.execute(
            """
            SELECT session_id, command, snippet(command_logs, 2, '>>>', '<<<', '...', 25), exit_code
            FROM command_logs
            WHERE command_logs MATCH ?
            ORDER BY rank
            LIMIT ?;
            """,
            (query, args.limit)
        )

    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print(f"No matches found for query: '{query}'")
        return 0

    print(f"Found {len(rows)} snippet(s) matching '{query}':\n")
    for row in rows:
        sess, cmd, snip, code = row
        print(f"[{sess}] `{cmd}` (exit {code}):")
        print(f"  {snip}\n")
    return 0

def cmd_tail(args: argparse.Namespace) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT output FROM command_logs
        WHERE session_id = ?
        ORDER BY rowid DESC LIMIT 1;
        """,
        (args.session,)
    )
    row = cursor.fetchone()
    conn.close()

    if not row or not row[0]:
        print(f"No output found for session: {args.session}")
        return 1

    lines = row[0].splitlines()
    count = min(args.lines, len(lines))
    print(f"--- [Last {count} lines of session {args.session}] ---")
    for line in lines[-count:]:
        print(line)
    return 0

def cmd_clear(args: argparse.Namespace) -> int:
    if DB_PATH.exists():
        DB_PATH.unlink()
        print(f"Context buffer database cleared: {DB_PATH}")
    else:
        print("Database already empty.")
    return 0

def main() -> None:
    parser = argparse.ArgumentParser(description="Context-Mode SQLite FTS5 Terminal Output Reducer")
    subparsers = parser.add_subparsers(dest="subcommand", required=True)

    run_p = subparsers.add_parser("run", help="Run command, capture output into SQLite FTS5, return summary")
    run_p.add_argument("--session", "-s", help="Optional session identifier")
    run_p.add_argument("command", nargs=argparse.REMAINDER, help="Command to execute")

    search_p = subparsers.add_parser("search", help="Search captured outputs via FTS5 BM25")
    search_p.add_argument("query", help="Search query string or pattern")
    search_p.add_argument("--session", "-s", help="Filter by specific session ID")
    search_p.add_argument("--limit", "-n", type=int, default=5, help="Maximum snippets to return")

    tail_p = subparsers.add_parser("tail", help="Print the last N lines of a session")
    tail_p.add_argument("session", help="Session ID")
    tail_p.add_argument("--lines", "-n", type=int, default=30, help="Number of lines to tail")

    subparsers.add_parser("clear", help="Clear all stored context buffer logs")

    parsed = parser.parse_args()
    if parsed.subcommand == "run":
        sys.exit(cmd_run(parsed))
    elif parsed.subcommand == "search":
        sys.exit(cmd_search(parsed))
    elif parsed.subcommand == "tail":
        sys.exit(cmd_tail(parsed))
    elif parsed.subcommand == "clear":
        sys.exit(cmd_clear(parsed))

if __name__ == "__main__":
    main()
