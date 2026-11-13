# 🤖 Antigravity & Hermes Universal Suite — Claude Code Guide

Welcome to the **Antigravity Super Suite & Hermes Autonomous Ecosystem** repository.
This document provides instructions, conventions, and operational patterns for **Claude Code**, Anthropic agents, and Claude-powered pair programmers.

---

## 🏛️ Repository Architecture

This repository is organized into distinct, modular layers designed for multi-agent execution:

```
antigravity-skills/
├── skills/                  ← 187 Audited Antigravity Elite Skills
├── plugins/                 ← 9 Turnkey Plugins (DeepMind Science, Stitch, Android, Firebase)
│   ├── science/             ← 41 DeepMind Science Skills + Mol* 3D Sidecar
│   └── stitch-*/            ← 16 Google Labs Stitch Design Skills
├── hermes/                  ← Hermes Autonomous Agent Ecosystem
│   ├── mega-suites/         ← 11 All-in-One Mega-Suites (~350,000 words total)
│   ├── master-suites/       ← 63 Consolidated Master Suites (330+ micro-skills unified)
│   ├── mcp-servers/         ← eBay, Vinted, Web Tools MCP servers
│   ├── scripts/             ← A2A Bus, Security Audits, DB Sync, Forecast
│   ├── security-tools/      ← Gitleaks secret detection configs
│   └── self-evolution/      ← Autonomous research & evolutionary algorithms
├── mcp/                     ← 5 Pre-bundled Antigravity MCP server schemas
└── scripts/                 ← Verification & one-click multi-agent installers
```

---

## 🧭 How Claude Code Should Navigate Skills

### 1. Broad Autonomous Agency → Hermes Mega-Suites (`hermes/mega-suites/`)
When the user asks for end-to-end autonomous marathon work, use the **11 Hermes Mega-Suites**:
1. [`hermes-mega-fullstack-web-desktop`](hermes/mega-suites/hermes-mega-fullstack-web-desktop/SKILL.md): Complete web & desktop lifecycle.
2. [`hermes-mega-devops-cloud-infrastructure`](hermes/mega-suites/hermes-mega-devops-cloud-infrastructure/SKILL.md): K8s, Terraform, Docker, CI/CD, SRE.
3. [`hermes-mega-cybersecurity-pentesting-defense`](hermes/mega-suites/hermes-mega-cybersecurity-pentesting-defense/SKILL.md): OWASP, CTF, hardening, OSINT, red/blue teaming.
4. [`hermes-mega-ai-llm-data-science`](hermes/mega-suites/hermes-mega-ai-llm-data-science/SKILL.md): ML/DL, RAG, NLP, computer vision, LangChain, fine-tuning.
5. [`hermes-mega-mobile-crossplatform`](hermes/mega-suites/hermes-mega-mobile-crossplatform/SKILL.md): React Native, Flutter, Swift/iOS, Kotlin/Android.
6. [`hermes-mega-data-engineering-databases`](hermes/mega-suites/hermes-mega-data-engineering-databases/SKILL.md): SQL, NoSQL, ETL, pipelines, vector stores.
7. [`hermes-mega-creative-media-game-design`](hermes/mega-suites/hermes-mega-creative-media-game-design/SKILL.md): Audio, video, 3D, procedural generation, game engines.
8. [`hermes-mega-autonomous-agents-tools`](hermes/mega-suites/hermes-mega-autonomous-agents-tools/SKILL.md): Self-evolution, orchestration, multi-agent teams.
9. [`hermes-mega-product-business-enterprise`](hermes/mega-suites/hermes-mega-product-business-enterprise/SKILL.md): Specs, architecture, finance, marketing, legal.
10. [`hermes-mega-specialized-domains-languages`](hermes/mega-suites/hermes-mega-specialized-domains-languages/SKILL.md): Rust, Go, C++, reverse engineering, hardware/IoT.
11. [`11_mega-narrative-worldbuilding-and-cinematic-suite`](hermes/mega-suites/11_mega-narrative-worldbuilding-and-cinematic-suite/SKILL.md): Universal narrative, worldbuilding, fiction & AI cinematic video suite.

### 2. Targeted Execution & Clean Patterns → Antigravity Elite Skills (`skills/`)
For specific engineering patterns, consult the **187 Antigravity Elite Skills** (e.g. `fastapi-sqlite-production`, `bridgesecurity-auditor`, `duckdb-parquet-analyst`, `shadcn`, `expo-router`, `context-mode`, `trail-of-bits-security-engine`).

### 3. Scientific & Biomedical Research → DeepMind Science (`plugins/science/`)
For AlphaFold structures, ClinVar genetics, ChEMBL pharmacology, or arXiv literature queries, leverage the DeepMind Science suite.

---

## 🧪 Quality Gate Verification

Before proposing or committing changes, always execute the repository test suite:

```bash
python scripts/verify_skills.py
```

The script audits:
- YAML frontmatter validity (`name`, `description`).
- Folder name and skill `name` exact match.
- Syntax validation of 518+ companion Python scripts and automated execution via scripts/test_companion_scripts.py.
- MCP JSON tool schema integrity.
- Absence of `__pycache__` and `.pyc` bytecode pollution.

---

## 🛡️ Security & Zero-Trust Rules

- **Zero Credentials**: Never commit API keys, tokens, passwords, or secrets.
- **Zero Hardcoded Personal Paths**: Always use `$HOME`, `~`, or relative paths.
- **English for Code & Commits**: Write all commit messages and code comments in English.
- **Commit Format**: Follow conventional commits: `type(scope): description`.
  - Types: `feat`, `fix`, `refactor`, `docs`, `chore`, `test`.
