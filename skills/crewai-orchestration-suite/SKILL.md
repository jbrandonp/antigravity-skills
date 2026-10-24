---
name: crewai-orchestration-suite
description: "Master CrewAI Multi-Agent Orchestration Suite: Architecture decisions, mandatory CLI scaffolding ('crewai create flow'), Agent design (Role-Goal-Backstory), Task design, Structured outputs, Flow state machines (@start/@listen), YAML configs, tool integration, and official documentation lookup via docs.crewai.com/llms.txt. Complete all-in-one suite."
---

# CrewAI Master Orchestration Suite

The complete engineering guide for architecting, scaffolding, configuring, and scaling multi-agent systems with CrewAI.

---

## ⚡ MANDATORY WORKFLOW — Read This First

**NEVER manually create crewAI project files from scratch.** Always scaffold with the CLI:

```bash
crewai create flow <project_name>
```

This is **not optional**. Even for a single crew, run the CLI first:
1. Run `crewai create flow <name>` (use **underscores**, not hyphens).
2. Edit the scaffolded YAML (`agents.yaml`, `tasks.yaml`) and Python files (`crew.py`, `main.py`).
3. Run `crewai install` then `crewai run`.

---

## 🧭 1. Choosing the Right Abstraction

CrewAI has four levels of abstraction. Pick the simplest one that fits your need:

| Level | When to Use | Overhead |
| :--- | :--- | :--- |
| **`LLM.call()`** | Single-prompt tasks without tools or memory. | Zero |
| **`Agent.kickoff()`** | Single agent with tools, needs reasoning/delegation. | Minimal |
| **`Crew.kickoff()`** | Multiple agents collaborating sequentially or hierarchically. | Standard |
| **`Flow`** | Complex pipelines with branching, loops, human-in-the-loop, and state machines. | Production |

---

## 🤖 2. The Agent Design Doctrine (The 80/20 Rule)

> Detailed playbook: `./references/agent-design-guide.md`

### Anti-Pattern: Micro-Agent Proliferation
Do NOT create 10 micro-agents for sequential mechanical steps (e.g. "Reader", "Summarizer", "Sender"). A single well-prompted agent with clear tools is far more reliable and costs 80% fewer tokens.

### The Role-Goal-Backstory Framework
- **Role**: Defines identity and tone (`Senior Financial Analyst`).
- **Goal**: Clear, quantifiable objective (`Extract revenue and EBITDA margins from SEC 10-K filings`).
- **Backstory**: Explains domain expertise and behavioral boundaries.

---

## 📋 3. The Task Design Doctrine

> Detailed playbook: `./references/task-design-guide.md`

### The Single Purpose Principle
- **Description**: Explicit, unambiguous instructions with `{variables}`.
- **Expected Output**: Concrete criteria (e.g. "A bulleted executive summary with exactly 3 risks and 3 opportunities").
- **Structured Output**: Pass Pydantic models to `output_pydantic` for deterministic schema enforcement (see `./references/structured-output.md`).

---

## 🔍 4. Official Docs & API Verification (`llms.txt`)

When checking cutting-edge features, new method signatures, or specific telemetry flags:
1. Fetch the structured index: `https://docs.crewai.com/llms.txt`
2. Retrieve the specific targeted documentation URL.
3. See `./references/docs-lookup.md` for troubleshooting guides.

---

## 📚 Reference Playbooks Routing Table

| Topic | Reference Playbook |
| :--- | :--- |
| **Agent Design Guide** | `./references/agent-design-guide.md` |
| **Task Design Guide** | `./references/task-design-guide.md` |
| **Flow Routing & State** | `./references/flow-routing.md` |
| **Custom Tools & Validation** | `./references/custom-tools.md` |
| **Memory & Knowledge Sources** | `./references/memory-and-knowledge.md` |
| **Structured Output (Pydantic)** | `./references/structured-output.md` |
| **MCP Server Integration** | `./references/mcp-servers.md` |
| **Built-in Tools Catalog** | `./references/tools-catalog.md` |
| **Live Docs & Troubleshooting** | `./references/docs-lookup.md` |
