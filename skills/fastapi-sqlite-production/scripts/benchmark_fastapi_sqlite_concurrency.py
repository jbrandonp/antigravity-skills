# -*- coding: utf-8 -*-
"""
benchmark_fastapi_sqlite_concurrency.py - FastAPI & SQLite Concurrency Benchmark
Simulateur et testeur de transactions concurrentes sous SQLite en mode WAL et busy_timeout.
"""

import os
import sqlite3
import threading
import time
from typing import List, Tuple, TypedDict

class ConcurrencyResult(TypedDict):
    total_threads: int
    successful_writes: int
    failed_writes: int
    duration_seconds: float
    is_concurrency_safe: bool

def init_database(db_path: str) -> None:
    """Initialise la base de donnees SQLite avec les pragmas de production."""
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
        except Exception:
            pass

    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA synchronous = NORMAL;")
    conn.execute("PRAGMA busy_timeout = 5000;")
    conn.execute("CREATE TABLE gain_logs (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT, val REAL, timestamp REAL);")
    conn.commit()
    conn.close()

def worker_write(db_path: str, user_id: str, count: int, results: List[bool]) -> None:
    """Execute une serie d'ecritures avec timeout de verrouillage."""
    conn = sqlite3.connect(db_path, timeout=5.0)
    conn.execute("PRAGMA busy_timeout = 5000;")
    success = True
    try:
        for i in range(count):
            conn.execute(
                "INSERT INTO gain_logs (user_id, val, timestamp) VALUES (?, ?, ?);",
                (user_id, float(i * 10), time.time())
            )
            conn.commit()
    except Exception:
        success = False
    finally:
        conn.close()
    results.append(success)

def run_benchmark(thread_count: int = 10, writes_per_thread: int = 5) -> ConcurrencyResult:
    """Lance un test de concurrence sur plusieurs threads en simultane."""
    db_path = "test_concurrent_gainlog.sqlite"
    init_database(db_path)

    start_t = time.time()
    threads: List[threading.Thread] = []
    results: List[bool] = []

    for t_idx in range(thread_count):
        t = threading.Thread(
            target=worker_write,
            args=(db_path, f"user_{t_idx}", writes_per_thread, results)
        )
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    duration = time.time() - start_t
    success_count = sum(1 for r in results if r)
    failed_count = thread_count - success_count

    # Nettoyage
    for ext in ["", "-wal", "-shm"]:
        p = db_path + ext
        if os.path.exists(p):
            try:
                os.remove(p)
            except Exception:
                pass

    return {
        "total_threads": thread_count,
        "successful_writes": success_count,
        "failed_writes": failed_count,
        "duration_seconds": duration,
        "is_concurrency_safe": failed_count == 0
    }

def run_self_test() -> int:
    """Verifie que les ecritures concurrentes SQLite s'executent sans blocage."""
    print("Execution du self-test FastAPI & SQLite Concurrency...")
    res = run_benchmark(thread_count=10, writes_per_thread=5)

    assert res["is_concurrency_safe"], f"Lock failure: {res['failed_writes']} threads failed!"
    assert res["successful_writes"] == 10, f"Expected 10 successful threads, got {res['successful_writes']}"

    print(f"[PASS] SQLite WAL Concurrency teste : {res['total_threads']} threads concurrents traites en {res['duration_seconds']:.3f}s.")
    print("       0 verrouillage 'database is locked' detecte.")
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(run_self_test())