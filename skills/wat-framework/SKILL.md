---
name: wat-framework
description: Architect, scaffold, and execute agentic workflows using the WAT (Workflows, Agents, Tools) paradigm. Separates probabilistic AI reasoning from deterministic Python tools to eliminate compounding error rates and achieve 99%+ reliability. Includes automated CLI scaffolder and architectural validator.
---

# WAT Framework: Workflows, Agents, Tools Architecture

The **WAT framework** establishes an engineering discipline for autonomous AI systems. It decouples probabilistic reasoning from deterministic execution.

## The Mathematical Rationale: Compounding Error Prevention

When an AI model attempts to perform every intermediate step directly (scraping, math, regex, audio processing, formatting):
$$\text{Success Rate} = P(\text{step})^N$$
If each step has an optimistic 90% accuracy:
- 1 step: $90\%$
- 3 steps: $72.9\%$
- 5 steps: $59.0\%$
- 10 steps: $34.8\%$

By contrast, when deterministic Python scripts handle execution with $99.9\%$ fidelity, the agent's role is restricted strictly to high-level coordination and semantic decisions:
$$\text{WAT Reliability} \ge 95\% \text{ across } 10+ \text{ sequential steps}$$

---

## 🏗️ The Three Layers of WAT

### Layer 1: Workflows (The SOPs)
- Stored as Markdown files in `workflows/`.
- Written in clean, unambiguous procedure steps like an operations manual.
- Defines: Objective, Required Inputs, Execution Tools, Expected Outputs, Edge Case Fallbacks, and Acceptance Verification.

### Layer 2: Agents (The Decision-Maker)
- Reads the relevant workflow file first.
- Decides execution order, inspects intermediate JSON artifacts, and handles semantic curation.
- **Rule of Thumb**: The agent never writes raw data or performs numeric slicing directly if a tool can do it deterministically.

### Layer 3: Tools (Deterministic Execution)
- Lightweight, single-purpose Python scripts in `tools/`.
- Handles file I/O, API requests, binary processing, database mutations, regex, audio/video encoding.
- Fast, testable, reproducible, and zero-hallucination.
- Credentials stored strictly in `.env`.

---

## 🛠️ CLI Scaffolder & Architecture Validator

This skill includes an automated CLI utility in `scripts/scaffold_wat_pipeline.py` to instantiate and audit WAT project structures:

```bash
# 1. Scaffold a new WAT project with canonical folders, SOP, and starter tool
python scripts/scaffold_wat_pipeline.py scaffold --dir my_wat_project --pipeline video_ingest

# 2. Audit an existing project for WAT compliance (clean separation, gitignore guards)
python scripts/scaffold_wat_pipeline.py validate --dir my_wat_project
```

---

## Standard Project Directory Layout

```
project/
├── .env                  # API keys and secrets (never committed)
├── .gitignore            # Ignores .env, work/, and __pycache__
├── workflows/            # Markdown SOPs defining each pipeline
│   ├── derush_video.md
│   └── publish_post.md
├── tools/                # Deterministic Python execution scripts
│   ├── transcribe.py
│   └── build_cut.py
├── work/                 # Intermediate JSON state artifacts
│   ├── slug_words.json
│   └── slug_plan.json
└── assets/ or output/    # Final validated deliverables
```

---

## Best Practices
1. **Always Verify Environment First**: Provide a `tools/check_env.py` script.
2. **Intermediate Artifacts in JSON**: Pass data between tools via explicit, inspectable JSON files.
3. **Human-in-the-Loop Decision Gates**: Allow the agent or user to review and curate `work/<slug>_plan.json` before triggering heavy render or mutation tools.
