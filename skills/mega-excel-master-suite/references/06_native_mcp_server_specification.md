# 06 — Native Model Context Protocol (MCP) Server Specification

## 🎯 Objective
Expose the complete capabilities of the Excel Master Suite directly to AI agent hosts (Claude Code, Cursor, OpenCode, Hermes, Antigravity) via the standard Model Context Protocol (JSON-RPC 2.0 over stdio).

---

## 🚀 Server Launch Command

```bash
# Direct Python execution
python c:/Users/brand/.agents/skills/mega-excel-master-suite/scripts/excel_master.py mcp

# Via uv / npx / Claude Code configuration
claude mcp add mega-excel -- uv run python c:/Users/brand/.agents/skills/mega-excel-master-suite/scripts/excel_master.py mcp
```

---

## 🛠️ Exposed Tools Catalog

| Tool Name | Parameters | Description |
| :--- | :--- | :--- |
| `excel_recalculate` | `file` (string) | Executes headless recalculation and returns error coordinates and formula statistics. |
| `excel_restructure` | `file`, `sheet`, `action`, `axis`, `index`, `count` | Inserts or deletes rows/columns with full AST formula coordinate shifting. |
| `excel_clean_reconcile` | `input` (string), `output` (string) | Cleans messy ERP spreadsheets with a mandatory $\Delta = 0.00$ reconciliation gate. |
| `excel_generate_model` | `model` (string), `output` (string) | Generates institutional models (`three_statement`, `dcf`, `lbo`, `saas_runway`, `debt_schedule`, `cap_table`, `working_capital`). |
| `excel_read_range` | `file`, `sheet`, `range` | Reads arbitrary A1 ranges and returns compact JSON matrices. |
| `excel_write_range` | `file`, `sheet`, `start`, `data` | Writes a 2D JSON matrix starting at an anchor coordinate. |
| `excel_trace_error` | `file` (string), `cell` (string) | Backtracks along the formula DAG to identify the upstream root cause of an error. |
| `excel_ux_audit` | `file` (string) | Validates freeze panes, auto-filters, column widths (anti-`###`), and formula counts. |
