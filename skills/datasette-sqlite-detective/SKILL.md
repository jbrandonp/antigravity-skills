---
name: datasette-sqlite-detective
description: >-
  Investigate, profile, and audit SQLite databases using Simon Willison Datasette Detective standards, while guarding schema evolution without data loss. Validates WAL mode, foreign key integrity, missing indexes, query plan efficiency (EXPLAIN QUERY PLAN), table fragmentation, detects schema drift between code models and production databases, and generates reversible UP/DOWN migration scripts.
---

# Datasette SQLite Detective (Simon Willison Standard)

Data archaeology and diagnostic framework inspired by **Simon Willison** (creator of *Datasette*, *sqlite-utils*, and pioneer in AI data analysis). Transforms the agent into an elite SQLite detective capable of diagnosing schema flaws, indexing bottlenecks, and structural anomalies.

---

## 🔍 The 4 Diagnostic Inspections

```text
 ┌─────────────────────────────────────────────────────────────┐
 │ 1. WAL Mode & Synchronous PRAGMA Audit                      │
 ├─────────────────────────────────────────────────────────────┤
 │ 2. Structural & Foreign Key Integrity Check                 │
 ├─────────────────────────────────────────────────────────────┤
 │ 3. Unindexed Foreign Key Identification (Join Bottlenecks)  │
 ├─────────────────────────────────────────────────────────────┤
 │ 4. Vacuum & Page Fragmentation Analysis                     │
 └─────────────────────────────────────────────────────────────┘
```

### Inspection 1: Concurrency & Performance PRAGMAs
- **WAL Mode**: `PRAGMA journal_mode = WAL;` (Enables concurrent readers during writes).
- **Synchronous**: `PRAGMA synchronous = NORMAL;` (Reduces disk sync stalls without compromising ACID integrity in WAL mode).
- **Foreign Keys**: `PRAGMA foreign_keys = ON;` (Must be enabled explicitly per connection).

### Inspection 2: Schema Health & Integrity
- Run `PRAGMA integrity_check;` to verify B-Tree storage integrity.
- Run `PRAGMA foreign_key_check;` to catch orphaned rows in relational tables.

### Inspection 3: Foreign Key Index Bottlenecks
- In SQLite, creating a `FOREIGN KEY` does **not** automatically create an index on the child table's column.
- Joining without an index on the foreign key column results in expensive full-table scans.
- The detective script automatically flags all foreign keys lacking matching indexes.

### Inspection 4: High-Density Table Profiling
- Generates row count, column types, and primary key structures for rapid agent reasoning.

---

## 🛠️ Tooling 1 : Audit & Diagnostic Simon Willison

```bash
# Audit an SQLite database
python scripts/sqlite_detective.py --db my_database.sqlite

# Run self-test on simulated in-memory database
python scripts/sqlite_detective.py --demo
```

---

## 📜 Module Complémentaire : Sentinelle des Migrations de Schémas SQLite UP/DOWN Sans Perte

# Schema Migration Sentinel (SQLite & Relational Standard)

A robust database schema migration and drift detection framework tailored for SQLite. Prevents data loss during structural evolution in scrapers, backend microservices, and desktop applications.

---

## 🛡️ The 4 Migration Guardrails

```text
 ┌─────────────────────────────────────────────────────────────┐
 │ 1. Schema Drift Detection (Model vs Database schema)        │
 ├─────────────────────────────────────────────────────────────┤
 │ 2. Non-Destructive DDL Generation (Never drop columns blindly)│
 ├─────────────────────────────────────────────────────────────┤
 │ 3. Atomic Transactional Migrations (BEGIN EXCLUSIVE)        │
 ├─────────────────────────────────────────────────────────────┤
 │ 4. Pre-Migration Snapshot Backup (Instant rollback safety)  │
 └─────────────────────────────────────────────────────────────┘
```

### Guardrail 1: Schema Drift Auditing
- Compares expected schema definitions against live database tables.
- Identifies:
  - Missing tables.
  - Missing columns in existing tables.
  - Type drift (e.g. column declared as `INTEGER` but populated as `TEXT`).

### Guardrail 2: Non-Destructive Migrations
- SQLite has historical limitations on `ALTER TABLE` (prior to 3.35, dropping columns was not supported directly).
- Safe 12-step table recreation pattern:
  1. `PRAGMA foreign_keys = OFF;`
  2. `BEGIN TRANSACTION;`
  3. Create temporary table `new_table`.
  4. Copy existing data: `INSERT INTO new_table SELECT ... FROM old_table;`
  5. Drop `old_table`.
  6. Rename `ALTER TABLE new_table RENAME TO old_table;`
  7. Re-create indexes and triggers.
  8. `PRAGMA foreign_key_check;`
  9. `COMMIT;`
  10. `PRAGMA foreign_keys = ON;`

### Guardrail 3: Pre-Migration Snapshotting
- Always duplicate the `.db` file into a timestamped snapshot before running any DDL migration.

---

## 🛠️ Tooling 2 : Détecteur de Dérive de Schéma & Migrations

```bash
# Compare live SQLite DB with expected schema definition
python scripts/sqlite_migration_differ.py --db production.sqlite --schema expected_schema.sql

# Run migration self-test on simulated database
python scripts/sqlite_migration_differ.py --demo
```
