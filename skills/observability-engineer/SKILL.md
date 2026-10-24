---
name: observability-engineer
description: Implement Observability-Driven Development (ODD) based on Charity Majors' Honeycomb standard. Enforces high-cardinality structured JSON logging, distributed tracing contexts (trace_id, span_id), duration metrics, and elimination of silent failures.
---

# Observability Engineer (Charity Majors Standard)

Observability-Driven Development (ODD) methodology formulated by **Charity Majors** (co-founder of *Honeycomb.io* and co-author of *Observability Engineering*).

Core Axiom: **"Software running in production must explain its internal state via wide, structured events. If a scraper fails or slows down, you shouldn't have to guess or reproduce locally: the event trace must tell you why."**

---

## 🔭 The 4 Invariants of Observability

```text
 ┌─────────────────────────────────────────────────────────────┐
 │ 1. Structured JSON Events (Ban unstructured string prints)  │
 ├─────────────────────────────────────────────────────────────┤
 │ 2. High-Cardinality Fields (trace_id, store_id, duration_ms)│
 ├─────────────────────────────────────────────────────────────┤
 │ 3. Unit-of-Work Context Propagation                         │
 ├─────────────────────────────────────────────────────────────┤
 │ 4. Zero Silent Failures (Explicit error stack and causes)   │
 └─────────────────────────────────────────────────────────────┘
```

### Invariant 1: Wide Structured Events
- Never output raw unparsed strings like `print("Done scraping products")`.
- Emit canonical JSON events:
  ```json
  {
    "timestamp": "2026-10-19T19:55:00Z",
    "level": "INFO",
    "event": "scrape_completed",
    "brand": "Delhaize",
    "items_collected": 1420,
    "duration_ms": 2341.2,
    "trace_id": "tr-7f9a8b1c",
    "http_status": 200
  }
  ```

### Invariant 2: High Cardinality & High Dimensionality
- Include specific identifiers: user IDs, product IDs, session IDs, request paths.
- Allows instant slicing and dicing in analytics tools (DuckDB, Honeycomb, Datadog) without code modification.

### Invariant 3: Performance Instrumentation
- Measure elapsed time natively using high-resolution monotonic clocks (`time.perf_counter()`).

---

## 🛠️ Deterministic Tooling

```bash
# Validate log files or stdout streams for ODD compliance
python scripts/validate_structured_logs.py --log-file scraper.log

# Run demonstration validator on sample logs
python scripts/validate_structured_logs.py --demo
```