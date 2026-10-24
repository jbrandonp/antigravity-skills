# Antigravity Customization Architecture & Playbook

> **Scope**: Master reference for designing, implementing, validating, and debugging customizations in Google Antigravity (AGY) / Gemini Agentic environments.

---

## 1. 🏗️ Precedence & Priority Resolution Hierarchy

When Antigravity discovers customizations across multiple directories, it applies a deterministic 4-tier precedence cascade:

```
┌────────────────────────────────────────────────────────┐
│  Tier 1: Workspace Root                                │
│  <workspace>/.agents/  or  <workspace>/.gemini/        │
│  (Highest priority: project-specific overrides)        │
└──────────────────────────┬─────────────────────────────┘
                           │ overrides
┌──────────────────────────▼─────────────────────────────┐
│  Tier 2: Explicit Declared Root                        │
│  Passed via --config-dir flag or AGY_CONFIG_PATH       │
└──────────────────────────┬─────────────────────────────┘
                           │ overrides
┌──────────────────────────▼─────────────────────────────┐
│  Tier 3: Global User Root                              │
│  ~/.agents/  or  ~/.gemini/config/                     │
│  (User-wide tools, shared developer defaults)          │
└──────────────────────────┬─────────────────────────────┘
                           │ overrides
┌──────────────────────────▼─────────────────────────────┐
│  Tier 4: Builtin System Packages                       │
│  Bundled with Antigravity IDE / CLI runtime            │
│  (Lowest priority fallback)                            │
└────────────────────────────────────────────────────────┘
```

### Component Collision Resolution Matrix

| Asset Type | Collision Resolution Policy | Example / Behavior |
| :--- | :--- | :--- |
| **Skills** | **First-hit wins**: Higher-tier skill completely shadows lower-tier skill with the same folder name. | A workspace `.agents/skills/pdf` shadows `~/.agents/skills/pdf`. |
| **Rules** | **Deep Merge**: All active markdown files in `rules/` and `AGENTS.md` are concatenated in order of tier. | Global rules apply, plus workspace-specific project constraints appended. |
| **Hooks** | **Sequential Chaining**: Handlers defined for identical events are merged into an ordered array. | Global `PreToolUse` security check executes first, followed by workspace linter. |
| **MCP Servers** | **Name Override**: Servers in higher-tier `mcp_config.json` override same-named server entries. | Local `sqlite` server config overrides global user `sqlite` server. |
| **Plugins** | **Explicit Activation**: Discovered plugins are enabled unless explicitly toggled off in `config.json`. | Config setting `plugins.<name>.enabled: false` overrides manifest default. |

---

## 2. ⚡ Lifecycle Hooks Engine (`hooks.json`)

Lifecycle hooks allow executing deterministic external commands at critical milestones in the agent's reasoning loop.

### 2.1 Hook Lifecycle Sequence

```mermaid
sequenceDiagram
    participant User
    participant Loop as Agent Loop
    participant Model as LLM Engine
    participant Tool as Tool Executor
    participant Hook as Lifecycle Hooks

    User->>Loop: Sends Prompt
    Hook->>Loop: SessionStart (once per session)
    Hook->>Loop: PreInvocation (prompt injection guards)
    Loop->>Model: Query LLM
    Model-->>Loop: Tool Call Request
    Hook->>Tool: PreToolUse (matcher check, validate args)
    alt PreToolUse Fails (Exit != 0)
        Tool-->>Loop: Step Aborted (Error returned to Model)
    else PreToolUse Passes
        Loop->>Tool: Execute Native / MCP Tool
        Tool-->>Hook: PostToolUse (linter, auto-format, telemetry)
        Tool-->>Loop: Tool Result
    end
    Loop->>Hook: PostInvocation (turn completed)
    User->>Loop: Session Terminated
    Loop->>Hook: Stop / SessionEnd (resource cleanup)
```

### 2.2 Event Specifications & Matcher Rules

1. **Flat Events** (`SessionStart`, `PreInvocation`, `PostInvocation`, `Stop`):
   - Contain a flat list of handler objects.
   - Matchers are not evaluated for these events.
2. **Tool-Scoped Events** (`PreToolUse`, `PostToolUse`):
   - Grouped structure requiring a `matcher` regex.
   - `matcher: "*"`: Matches all tools.
   - `matcher: "run_command"`: Matches shell commands only.
   - `matcher: "run_command|write_file|edit_file"`: Regex disjunction.
   - `matcher: "mcp_.*"`: Matches all lazy/eager MCP tools.

### 2.3 Handler Execution Contract
- **Input (stdin)**: Context JSON payload containing `event`, `tool_name`, `arguments`, and session metadata.
- **Output (stdout)**: JSON object or standard output. If JSON contains `{"decision": "abort", "reason": "..."}`, the operation is halted.
- **Exit Code**:
  - `0`: Execution allowed, proceeds normally.
  - Non-zero: Hook error; aborts tool call in `PreToolUse` and returns stderr to the model.

---

## 3. 🔌 Plugin Bundle Architecture

Plugins consolidate skills, rules, lifecycle hooks, and MCP servers into single distributable units.

### 3.1 Recommended Plugin Layout

```text
my-awesome-plugin/
├── plugin.json         # Manifest marker (Required)
├── mcp_config.json     # MCP servers exposed by plugin (Optional)
├── hooks.json          # Lifecycle hooks (Optional - MUST be at root)
├── rules/              # Consolidated guidelines
│   └── AGENTS.md       # Primary rules file loaded when active
└── skills/             # Skills packaged inside plugin
    └── domain-skill/
        ├── SKILL.md
        └── scripts/
```

### 3.2 Manifest Schema (`plugin.json`)
```json
{
  "name": "my-awesome-plugin",
  "version": "1.2.0",
  "description": "Enterprise plugin delivering specialized database automation.",
  "disabled": false
}
```

---

## 4. 🌐 MCP (Model Context Protocol) Integration

Antigravity natively loads MCP servers declared in `mcp_config.json` or plugin descriptors.

### 4.1 Server Types
- **Standard I/O (`stdio`)**: Subprocess communicating via standard input/output streams. Ideal for local scripts, Python FastMCP, and Node.js servers.
- **Server-Sent Events (`sse`)**: Remote HTTP endpoints providing persistent bidirectional event streaming. Ideal for shared enterprise tools and cloud services.

### 4.2 Standard `mcp_config.json` Configuration
```json
{
  "mcpServers": {
    "sqlite-analyst": {
      "command": "python",
      "args": ["-m", "mcp_server_sqlite", "--db-path", "./data/prod.db"],
      "env": {
        "SQLITE_TIMEOUT": "5000"
      }
    },
    "enterprise-remote": {
      "url": "http://10.0.0.42:8080/sse",
      "transport": "sse"
    }
  }
}
```

---

## 5. 🎛️ Sidecar UI Panels (`sidecar://`)

Antigravity supports interactive web sidecars linked directly from chat responses.

- **Link Convention**: Always format sidecar links as `[Open Viewer](sidecar://<panel_id>)`.
- **Use Cases**:
  - Biomolecular 3D rendering (Mol* viewer).
  - Spatial 3D asset inspection (Three.js / Blender viewport).
  - Live interactive dashboards and Generative UI widgets.

---

## 6. 🛠️ Deterministic Tooling & Verification

In accordance with the **WAT Framework**, probabilistic agents must never guess configuration syntax. Use the bundled CLI scripts:

### Audit Environment Integrity
```bash
python scripts/validate_agy_environment.py --config-dir ~/.gemini/config
```

### Scaffold New Customizations
```bash
# New Skill
python scripts/scaffold_agy_customization.py --type skill --name my-tool --desc "CLI toolchain"

# New Lifecycle Hook
python scripts/scaffold_agy_customization.py --type hook --name guard --event PreToolUse --matcher run_command --command "./guard.sh"

# New Plugin Bundle
python scripts/scaffold_agy_customization.py --type plugin --name database-suite
```
