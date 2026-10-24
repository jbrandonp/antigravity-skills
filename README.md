# 🚀 Antigravity Super Suite

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Google Antigravity](https://img.shields.io/badge/Antigravity-2.0%20Ready-4285F4.svg)](https://antigravity.google)
[![Skills Count](https://img.shields.io/badge/Elite%20Skills-109%20Active-success.svg)](skills/)
[![DeepMind Science](https://img.shields.io/badge/DeepMind%20Science-41%20Skills-8A2BE2.svg)](plugins/science/)
[![Integrity Score](https://img.shields.io/badge/Audit%20Score-100%2F100-brightgreen.svg)](scripts/verify_skills.py)
[![CI Status](https://img.shields.io/badge/CI-Passing-brightgreen.svg)](.github/workflows/validate-skills.yml)

> **The Ultimate Production-Ready Skill & Customization Suite for [Google Antigravity](https://antigravity.google) and Modern AI Coding Agents.**  
> Includes **109 audited and fused elite skills**, the official **Google DeepMind Science toolkit** (41 skills + 3D Mol* interactive sidecar), custom Model Context Protocol (MCP) servers, and one-click installers.

---

## 📑 Table of Contents

1. [Overview & Philosophy](#-overview--philosophy)
2. [Multi-Agent Portability](#-multi-agent-portability)
3. [One-Click Installation](#-one-click-installation)
4. [Elite Skills Catalog (109 Skills)](#-elite-skills-catalog-109-skills)
5. [Google DeepMind Science Suite (41 Skills)](#-google-deepmind-science-suite-41-skills)
6. [Plugins & MCP Architecture](#-plugins--mcp-architecture)
7. [Zero-Trust Security & Sanitization](#-zero-trust-security--sanitization)
8. [Automated CI & Validation](#-automated-ci--validation)
9. [License & Credits](#-license--credits)

---

## 🌟 Overview & Philosophy

In modern agentic AI development, probabilistic language models frequently suffer from two fatal traps:
1. **Context Bloat & Token Degradation**: Stuffing dozens of redundant, overlapping prompts degrades reasoning and inflates costs.
2. **Hallucinated Execution**: Agents guessing CLI flags, imaginary timestamps, or non-existent APIs.

The **Antigravity Super Suite** solves this through the **WAT (Workflows, Agents, Tools) architecture** and a strict **100% Audit Score**:
- **Consolidated Master Suites**: 12 fragmented sub-skills were unified into 7 master suites (e.g., `gsap-core`, `reel-cut`, `minecraft-plugin-development`, `mmo-tab-target-combat-pipeline`).
- **Zero Duplicates**: Every skill has a single, authoritative responsibility.
- **Hermetic Tool Execution**: Uses Python PEP 723 metadata with `uv` for sub-second, isolated CLI executions without polluting global environments.

---

## 🔄 Multi-Agent Portability

While natively architected for **Google Antigravity**, every skill in this repository strictly adheres to universal agent conventions (standard Markdown with YAML frontmatter). They are immediately compatible with:
- **Google Antigravity IDE & CLI (`agy`)**
- **Claude Code (`~/.claude/skills/` or `~/.agents/skills/`)**
- **Cursor & GitHub Copilot (`.cursor/skills/`)**
- **Open-Source Agent CLI (`npx skills`)**

---

## ⚡ One-Click Installation

### Windows (PowerShell)
Open PowerShell and run:
```powershell
irm https://raw.githubusercontent.com/jbrandonp/antigravity-skills/main/scripts/install.ps1 | iex
```
*Or clone the repo and run locally:*
```powershell
git clone https://github.com/jbrandonp/antigravity-skills.git
cd antigravity-skills
.\scripts\install.ps1
```

### Linux / macOS (Bash)
```bash
curl -fsSL https://raw.githubusercontent.com/jbrandonp/antigravity-skills/main/scripts/install.sh | bash
```
*Or clone the repo and run locally:*
```bash
git clone https://github.com/jbrandonp/antigravity-skills.git
cd antigravity-skills
chmod +x scripts/install.sh && ./scripts/install.sh
```

---

## 📦 Elite Skills Catalog (109 Skills)


### 🎮 Game Development, 3D & Shaders

| Skill | Description |
| :--- | :--- |
| [`game-ready-3d-assets`](skills/game-ready-3d-assets/SKILL.md) | End-to-end 3D game-ready asset pipeline (PBR, metric scale, LODs, UCX collisions) via Blender. |
| [`3d-character-sheet-pipeline`](skills/3d-character-sheet-pipeline/SKILL.md) | Turn 2D concepts into production 3D reference packages (Nano Banana Pro, Rodin, Tripo, Patina PBR). |
| [`blender-game-rigging-animation`](skills/blender-game-rigging-animation/SKILL.md) | Headless Blender rigging, IK solving, walk skating elimination, and FBX export for UE5/Unity. |
| [`mixamo-animation-library-engine`](skills/mixamo-animation-library-engine/SKILL.md) | Programmatic, zero-credential acquisition of 90+ FBX animations from Hugging Face with SHA-256 receipts. |
| [`kinematic-character-controller`](skills/kinematic-character-controller/SKILL.md) | 2D/3D kinematic controllers with Coyote Time, Jump Buffering, and UE5 Motion Matching. |
| [`game-animation-polish-juice`](skills/game-animation-polish-juice/SKILL.md) | Tactile combat juice, Anticipation-Snap-Hitstop curves, gait phase matching, and impact sync. |
| [`gameplay-ability-system`](skills/gameplay-ability-system/SKILL.md) | World of Warcraft style GAS engine (Attributes, Gameplay Tags, 2-roll attack tables, Pandemic rollover). |
| [`mmo-tab-target-combat-pipeline`](skills/mmo-tab-target-combat-pipeline/SKILL.md) | Tab-targeting combat, Threat/Hate list hysteresis, quest DAG engine, reputation matrices, and HUD. |
| [`game-ai-behavior-tree`](skills/game-ai-behavior-tree/SKILL.md) | Hierarchical Behavior Trees, UE5 StateTree, Blackboard memory, and Catmull-Rom patrol engines. |
| [`game-world-warmup-streaming`](skills/game-world-warmup-streaming/SKILL.md) | Zero-stutter world warmup, static orthographic minimap baking, and shader keep-alive guards. |
| [`game-save-state-manager`](skills/game-save-state-manager/SKILL.md) | Atomic disk writes, checksums/HMAC corruption detection, and schema migration for game saves. |
| [`game-asset-hunter-curator`](skills/game-asset-hunter-curator/SKILL.md) | Discover and download free CC0/CC-BY game assets across Poly Haven, Kenney, Fab, and Freesound. |
| [`autonomous-game-slice-director`](skills/autonomous-game-slice-director/SKILL.md) | Orchestrate 24-48h autonomous game development marathons with greybox-first MVP in <2.5h. |
| [`ue5-nanite-substrate-chaos-pipeline`](skills/ue5-nanite-substrate-chaos-pipeline/SKILL.md) | Next-gen UE5 rendering, micro-polygon Nanite geometry, Substrate BSDF, and Chaos physics. |
| [`ue5-pcg-world-generation`](skills/ue5-pcg-world-generation/SKILL.md) | Unreal Engine Procedural Content Generation (PCG) graphs, Poisson disk distributions, and biomes. |
| [`ue5-metasound-procedural-audio`](skills/ue5-metasound-procedural-audio/SKILL.md) | Sample-accurate DSP audio graphs, 3D spatial ambience, dynamic combat ducking, and footstep triggers. |
| [`ue5-mcp-automation`](skills/ue5-mcp-automation/SKILL.md) | Programmatic Unreal Engine 5 automation via Model Context Protocol (MCP) TCP bridge. |
| [`game-engine`](skills/game-engine/SKILL.md) | Web-based game engine in Canvas, WebGL, and JavaScript (physics, collisions, loops, WebRTC multiplayer). |
| [`slang-shader-engineer`](skills/slang-shader-engineer/SKILL.md) | Cross-platform Slang shader architecture targeting DX12, Vulkan, Metal, and WebGPU. |
| [`2d-pixel-sprite-sheet-pipeline`](skills/2d-pixel-sprite-sheet-pipeline/SKILL.md) | End-to-end 2D pixel-art sprite production pipeline without mixels (sub-pixel artifacts). |

### 📱 Mobile Development (Expo, React Native, iOS, Android, EAS)

| Skill | Description |
| :--- | :--- |
| [`expo-native-ui`](skills/expo-native-ui/SKILL.md) | Apple HIG and Material You native-feeling Expo screens with design tokens and responsive layout. |
| [`expo-router`](skills/expo-router/SKILL.md) | File-based navigation, groups, dynamic routes, native Stack, modals, and tabs for Expo Router. |
| [`expo-web-to-native`](skills/expo-web-to-native/SKILL.md) | Comprehensive migration guide from web React to native iOS/Android, including modern DOM components. |
| [`expo-animation`](skills/expo-animation/SKILL.md) | Fluid animations with Reanimated, Gesture Handler, and haptics running at native 60/120 FPS. |
| [`expo-data-fetching`](skills/expo-data-fetching/SKILL.md) | Production network requests, React Query caching, offline synchronization, and error states. |
| [`expo-project-structure`](skills/expo-project-structure/SKILL.md) | Clean architectural directory layouts and file organization for modern Expo apps. |
| [`expo-brownfield`](skills/expo-brownfield/SKILL.md) | Integrate Expo and React Native screens into existing native iOS (Swift/UIKit) and Android (Kotlin) apps. |
| [`expo-module`](skills/expo-module/SKILL.md) | Create native Swift/Kotlin modules using the Expo Modules API 2.0 with type-safe bindings. |
| [`expo-app-clip`](skills/expo-app-clip/SKILL.md) | Lightweight iOS App Clip companion targets invoked directly via URLs and NFC tags. |
| [`expo-dev-client`](skills/expo-dev-client/SKILL.md) | Custom local and cloud Expo Development Clients for internal team testing. |
| [`expo-upgrade`](skills/expo-upgrade/SKILL.md) | Deterministic upgrade procedures across Expo SDK major releases and dependency resolution. |
| [`eas-app-stores`](skills/eas-app-stores/SKILL.md) | Automated app submission to Apple App Store (TestFlight) and Google Play Store via EAS. |
| [`eas-hosting`](skills/eas-hosting/SKILL.md) | Deploy full-stack Expo websites and API routes to EAS Hosting with Cloudflare Workers runtime. |
| [`eas-workflows`](skills/eas-workflows/SKILL.md) | CI/CD workflow automation YAML pipelines for building, testing, and shipping Expo projects. |
| [`eas-update`](skills/eas-update/SKILL.md) | Over-the-air (OTA) updates and rollback strategies for instant bug fixes without App Store review. |
| [`eas-observe`](skills/eas-observe/SKILL.md) | Real-time crash reporting, performance observability, and error tracking in production. |
| [`material-3`](skills/material-3/SKILL.md) | Material Design 3 (Material You) implementation in Jetpack Compose, Flutter, and Web. |
| [`compose-agent`](skills/compose-agent/SKILL.md) | Modern Jetpack Compose architecture: state hoisting, side effects, Navigation 3, and Paging 3. |
| [`jetpack-compose-audit`](skills/jetpack-compose-audit/SKILL.md) | Comprehensive Android Compose code audit scoring recompositions, state traps, and splash screens. |
| [`android-cli`](skills/android-cli/SKILL.md) | Android SDK CLI management, emulator provisioning, UI inspection, and app lifecycle commands. |

### 🎨 Frontend Craft, UI/UX & Design Systems

| Skill | Description |
| :--- | :--- |
| [`ui-ux-pro-max`](skills/ui-ux-pro-max/SKILL.md) | Elite UI/UX intelligence: 79 design styles, 192 product palettes, 74 typography pairings, and 25 chart types. |
| [`frontend-design`](skills/frontend-design/SKILL.md) | Distinctive, human-crafted visual direction eliminating templated generic AI aesthetics. |
| [`anti-ui-slop`](skills/anti-ui-slop/SKILL.md) | Grounded UI development using 800,000+ real web/iOS screens and hard finish gate checks. |
| [`frontend-reference-match`](skills/frontend-reference-match/SKILL.md) | Exact pixel-by-pixel reference matching pipeline with local serving and Puppeteer screenshot diffs. |
| [`typeui-design-systems`](skills/typeui-design-systems/SKILL.md) | Registry of 67 distinct pre-compiled design system themes (Bento, Brutalism, Claymorphism, Editorial). |
| [`shadcn`](skills/shadcn/SKILL.md) | Component registry manager, theming, and layout composition for modern shadcn/ui interfaces. |
| [`design-system`](skills/design-system/SKILL.md) | Three-layer design token architecture (primitive -> semantic -> component) with CSS variables. |
| [`banner-design`](skills/banner-design/SKILL.md) | Production-grade social, display ad, and web hero banner generation with responsive art directions. |
| [`canvas-design`](skills/canvas-design/SKILL.md) | Procedural visual art, posters, and vector canvas documents using generative design philosophy. |
| [`algorithmic-art`](skills/algorithmic-art/SKILL.md) | Generative art with p5.js, seeded randomness, flow fields, and interactive particle systems. |
| [`web-artifacts-builder`](skills/web-artifacts-builder/SKILL.md) | Complex interactive multi-component React/Tailwind/shadcn artifacts with local state. |
| [`generative_ui`](skills/generative_ui/SKILL.md) | Render rich interactive HTML widgets, walkthroughs, and reactive dashboards inline in chat. |
| [`theme-factory`](skills/theme-factory/SKILL.md) | Universal theme styling toolkit for documents, presentation decks, and web landing pages. |
| [`redesign-existing-projects`](skills/redesign-existing-projects/SKILL.md) | Upgrade legacy or mediocre web applications to high-end design without breaking functionality. |
| [`premium-frontend-ui`](skills/premium-frontend-ui/SKILL.md) | High-performance web craftsmanship with advanced motion choreography and typography scales. |
| [`design-taste-frontend`](skills/design-taste-frontend/SKILL.md) | Anti-slop frontend art direction, distillation principles, and custom aesthetic palettes. |

### 🛡️ Cybersecurity, DevSecOps & Quality Assurance

| Skill | Description |
| :--- | :--- |
| [`bridgesecurity-auditor`](skills/bridgesecurity-auditor/SKILL.md) | Senior security audits (OWASP Top 10, CWE Top 25), zero-trust secrets, age/SOPS envelope encryption. |
| [`threat-model`](skills/threat-model/SKILL.md) | Structured threat modeling and attack surface mapping across distributed architectures. |
| [`vuln-scan`](skills/vuln-scan/SKILL.md) | Static source-code vulnerability scanning with parallel analysis and triage scoring. |
| [`test-driven-development`](skills/test-driven-development/SKILL.md) | Strict Red-Green-Refactor TDD cycle combined with property-based invariant fuzzing. |
| [`loopcraft-harness-engineer`](skills/loopcraft-harness-engineer/SKILL.md) | Autonomous self-healing test loops with automatic error classification (SYNTAX, RUNTIME, LINT). |
| [`senior-code-reviewer`](skills/senior-code-reviewer/SKILL.md) | Google/Anthropic standard code review: logic verification, dead code pruning, and zero bloat. |
| [`tech-debt-audit`](skills/tech-debt-audit/SKILL.md) | Multi-dimensional technical debt audit across 9 architectural metrics using AST-grep. |
| [`systematic-debugging`](skills/systematic-debugging/SKILL.md) | SWE-bench systematic debugging standard with deterministic reproduction scripts. |
| [`remove-ai-slops`](skills/remove-ai-slops/SKILL.md) | Purge AI-generated code smells, speculative generality, and hallucinated patterns. |
| [`visual-qa`](skills/visual-qa/SKILL.md) | Rigorous Apple HIG visual QA across web, mobile, and terminal surfaces with paired light/dark captures. |

### 📊 Data Engineering, Stealth Scraping & Columnar Analytics

| Skill | Description |
| :--- | :--- |
| [`stealth-hybrid-scraper-architect`](skills/stealth-hybrid-scraper-architect/SKILL.md) | Resilient anti-detection web scrapers with JA4 TLS fingerprint spoofing via curl_cffi. |
| [`datasette-sqlite-detective`](skills/datasette-sqlite-detective/SKILL.md) | SQLite database auditing, WAL mode verification, query plan analysis, and schema migrations. |
| [`duckdb-parquet-analyst`](skills/duckdb-parquet-analyst/SKILL.md) | High-performance columnar analytics, Parquet pipelines, and dataset quality auditing. |
| [`fastapi-sqlite-production`](skills/fastapi-sqlite-production/SKILL.md) | Asynchronous production FastAPI services with concurrent SQLite persistence and JWT auth. |
| [`api-reverse-engineer`](skills/api-reverse-engineer/SKILL.md) | Reverse-engineer private mobile/web APIs from HAR captures and decompiled Android APKs. |
| [`observability-engineer`](skills/observability-engineer/SKILL.md) | Observability-Driven Development (ODD) with high-cardinality JSON logging and distributed tracing. |
| [`excel-architect`](skills/excel-architect/SKILL.md) | Production-grade Excel spreadsheets (.xlsx) with native formulas, zebra-striping, and freeze panes. |
| [`pdf`](skills/pdf/SKILL.md) | Exhaustive PDF manipulation: extraction, OCR, merging, watermarks, form filling, and encryption. |
| [`ast-grep`](skills/ast-grep/SKILL.md) | Syntactic pattern searching and AST-based code rewrites across 25 programming languages. |

### 🤖 Agent Architecture, Multi-Agent & WAT Paradigm

| Skill | Description |
| :--- | :--- |
| [`wat-framework`](skills/wat-framework/SKILL.md) | WAT (Workflows, Agents, Tools) architecture separating probabilistic reasoning from deterministic code. |
| [`agent-architecture`](skills/agent-architecture/SKILL.md) | AI agent architectural design, requirements discovery, and failure mode diagnosis. |
| [`context-engineering`](skills/context-engineering/SKILL.md) | Agent token budget optimization, LLM prompt caching strategies, and context rot prevention. |
| [`mcp-builder`](skills/mcp-builder/SKILL.md) | Design and implementation of Model Context Protocol (MCP) servers in Python (FastMCP) and TypeScript. |
| [`rust-mcp-server-generator`](skills/rust-mcp-server-generator/SKILL.md) | Generate complete high-performance Rust Model Context Protocol servers using official rmcp SDK. |
| [`unlazy`](skills/unlazy/SKILL.md) | Completion discipline for autonomous coding tasks with acceptance gates and depth tree execution. |
| [`workflow-skill-creator`](skills/workflow-skill-creator/SKILL.md) | Distill completed workflows and human interactions into reusable, deterministic agent skills. |
| [`skill-creator`](skills/skill-creator/SKILL.md) | Create, benchmark, and evaluate AI agent skills with variance analysis and trigger optimization. |
| [`acquire-codebase-knowledge`](skills/acquire-codebase-knowledge/SKILL.md) | Onboard and map unfamiliar codebases, architectures, and data flows into structured documentation. |

### 🔬 Science, Rigorous Mathematics & Humanoid Robotics

| Skill | Description |
| :--- | :--- |
| [`humanoid-robotics-architect`](skills/humanoid-robotics-architect/SKILL.md) | Design, actuator sizing, DoF mapping, URDF kinematics, and Sim-to-Real robotics pipelines. |
| [`math-rigor-tutor`](skills/math-rigor-tutor/SKILL.md) | Mathematical proofs, real analysis, linear algebra, calculus, and verified LaTeX formalization. |
| [`rust-engineer`](skills/rust-engineer/SKILL.md) | Systems programming, Cargo crates, Bevy engine components, and memory-safe algorithms. |
| [`swift-concurrency-expert`](skills/swift-concurrency-expert/SKILL.md) | Swift 6.2+ concurrency review, actor isolation, data race elimination, and Sendable safety. |
| [`swiftui-skills`](skills/swiftui-skills/SKILL.md) | Apple-native SwiftUI and SwiftData architecture based on 20 authoritative Xcode guides. |
| [`swiftui-ui-patterns`](skills/swiftui-ui-patterns/SKILL.md) | Best practices for declarative iOS UI layouts, stacks, grids, and State/Binding navigation. |
| [`minecraft-plugin-development`](skills/minecraft-plugin-development/SKILL.md) | Paper/Spigot plugin suite with Adventure/MiniMessage text and KingdomsX French localization. |

### 🎬 Video Editing, Sound Design & Media

| Skill | Description |
| :--- | :--- |
| [`reel-cut`](skills/reel-cut/SKILL.md) | Autonomous short-form video editing: Whisper transcription, silence midpoint cutting, and HyperFrames DOM. |
| [`app-promo-reel`](skills/app-promo-reel/SKILL.md) | Beat-synced 30s vertical/feed promo reels with ACE-Step audio and kick-locked animations. |
| [`repurpose-youtube-video`](skills/repurpose-youtube-video/SKILL.md) | Repurpose YouTube videos into high-converting LinkedIn, Instagram, and X posts via Blotato API. |
| [`real-sound`](skills/real-sound/SKILL.md) | Zero-royalty sound effects synthesis, audio spatial mastering, and loudness normalization. |

### ⚡ GSAP & Advanced Motion Animation

| Skill | Description |
| :--- | :--- |
| [`gsap-core`](skills/gsap-core/SKILL.md) | Comprehensive GSAP 3 Master Suite: timelines, React useGSAP hook, ScrollTrigger, and premium plugins. |
| [`gsap-framer-scroll-animation`](skills/gsap-framer-scroll-animation/SKILL.md) | Bespoke scroll-driven choreography uniting GSAP ScrollTrigger with Framer Motion. |
| [`cinetic`](skills/cinetic/SKILL.md) | Cinematic motion design, dithered gradients, audio-visual synchrony, and aesthetic video title cards. |

### 📑 Formal Productivity (Office & Documents)

| Skill | Description |
| :--- | :--- |
| [`slides`](skills/slides/SKILL.md) | Strategic HTML/Canvas presentations with Chart.js, design tokens, and copywriting formulas. |
| [`brand`](skills/brand/SKILL.md) | Brand voice architecture, messaging frameworks, design compliance, and style guidelines. |
| [`vibe-aso`](skills/vibe-aso/SKILL.md) | Full-funnel App Store Optimization: keyword research, localized metadata, and screenshot design. |
| [`webapp-testing`](skills/webapp-testing/SKILL.md) | Playwright end-to-end browser automation, screenshots, console logging, and regression tests. |

---

## 🔬 Google DeepMind Science Suite (41 Skills)

Included in [`plugins/science/`](plugins/science/), the official scientific toolkit by Google DeepMind empowers AI agents to conduct rigorous biomedical, chemical, and genomic research:

- **Structural Biology**: AlphaFold structure fetcher, Foldseek 3D structural alignment, PDB coordinates parser.
- **Interactive 3D Sidecar**: Built-in Mol* biomolecular viewer with native MCP server (`biomolecular_structure_viewer_mcp`).
- **Genomics & Clinical Trials**: ClinVar pathogenicity, dbSNP short variants, GTEx gene expression, ENCODE cCREs, gnomAD allele frequencies.
- **Cheminformatics**: PubChem chemical resolution, ChEMBL bioactivity search, OpenTargets drug discovery.
- **Literature Search**: OpenAlex scholarly graphs, PubMed API, bioRxiv/medRxiv preprints, arXiv search.

---

## 🔌 Plugins & MCP Architecture

This repository includes turnkey templates for Antigravity's native plugin and Model Context Protocol engines:

1. **`config/config.template.json`**: Enable official plugins (`science`, `android-cli-plugin`, `firebase`, `chrome-devtools`).
2. **`config/mcp_config.template.json`**:
   - `blender`: Headless Blender 3D rigging, skinning, and asset generation via `uvx`.
   - `cloudrun`: Deploy microservices and APIs directly to Google Cloud Run.
   - `firebase-mcp-server`: Manage Firestore, Auth, and Cloud Functions.
   - `genkit-mcp-server`: Orchestrate generative AI flows with Google Genkit.

---

## 🛡️ Zero-Trust Security & Sanitization

Every file in this repository has been audited against BridgeMind BridgeSecurity standards:
- **Zero Credentials**: Absolutely no API keys, private tokens, or secrets are committed.
- **Zero Personal Paths**: All hardcoded local paths have been sanitized to standard portable environment variables (`$HOME` / `~`).
- **Clean Git State**: No `__pycache__`, compiled bytecode, or extraneous files.

---

## 🧪 Automated CI & Validation

To maintain flawless skill discovery, our GitHub Actions workflow ([`.github/workflows/validate-skills.yml`](.github/workflows/validate-skills.yml)) verifies on every commit:
- 100% of `SKILL.md` files possess valid YAML frontmatters (`name`, `description`).
- All internal Python utility scripts compile without syntax errors.
- Relative links across skills resolve correctly.

Run the test suite locally at any time:
```bash
python scripts/verify_skills.py
```

---

## ⚖️ License & Credits

- **Core Skills & Customizations**: Licensed under [Apache License 2.0](LICENSE).
- **Google DeepMind Science Skills**: Copyright 2026 Google LLC, licensed under Apache License 2.0 and Creative Commons Attribution 4.0.
- **Author & Maintainer**: Brandon ([`@jbrandonp`](https://github.com/jbrandonp)).
