# 🚀 Antigravity Super Suite

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Google Antigravity](https://img.shields.io/badge/Antigravity-2.0%20Ready-4285F4.svg)](https://antigravity.google)
[![Skills Count](https://img.shields.io/badge/Elite%20Skills-117%20Active-success.svg)](skills/)
[![DeepMind Science](https://img.shields.io/badge/DeepMind%20Science-41%20Skills-8A2BE2.svg)](plugins/science/)
[![Google Stitch](https://img.shields.io/badge/Google%20Stitch-16%20Skills-4285F4.svg)](plugins/stitch-design/)
[![Plugins Count](https://img.shields.io/badge/Plugins-9%20Bundled-blue.svg)](plugins/)
[![MCP Servers](https://img.shields.io/badge/MCP%20Servers-5%20Bundled-blue.svg)](mcp/)
[![Total Tools](https://img.shields.io/badge/Total%20Tools-174%20Skills%20%2B%205%20MCP-orange.svg)](#)
[![Integrity Score](https://img.shields.io/badge/Audit%20Score-100%2F100-brightgreen.svg)](scripts/verify_skills.py)
[![CI Status](https://img.shields.io/badge/CI-Passing-brightgreen.svg)](.github/workflows/validate-skills.yml)

> **The Ultimate Production-Grade Skill & Customization Suite for [Google Antigravity](https://antigravity.google) and Modern AI Coding Agents.**  
> Includes **117 audited elite skills**, the official **Google DeepMind Science toolkit** (41 skills + 3D Mol* interactive sidecar), the **Google Labs Stitch design suite** (16 skills across 3 plugins), **5 pre-bundled MCP servers** (Blender, Cloud Run, Firebase, Genkit, Science Mol*), and one-click installers.

---

## 📑 Table of Contents

1. [Overview & Philosophy](#-overview--philosophy)
2. [Universal Agent Compatibility (~/.agents/skills)](#-universal-agent-compatibility-agentsskills)
3. [One-Click Installation](#-one-click-installation)
4. [Elite Skills Catalog (117 Skills)](#-elite-skills-catalog-117-skills)
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
- **Consolidated Master Suites**: Micro-skills are unified into coherent, authoritative suites (e.g., `devops-infrastructure-as-code`, `postgresql-production-dba`, `saas-backend-architecture`, `rag-vector-search-engineer`).
- **Zero Duplicates**: Every skill has a single, unambiguous operational responsibility.
- **Hermetic Tool Execution**: Uses Python PEP 723 metadata with `uv` for sub-second, isolated CLI executions without polluting global environments.

---

## 🔄 Universal Agent Compatibility (`~/.agents/skills`)

This suite natively supports the **open-standard multi-agent specification** (`~/.agents/skills/`), ensuring that all skills work seamlessly across:
- **Google Antigravity IDE & CLI (`agy`)**
- **Claude Code (`~/.claude/skills/` or `~/.agents/skills/`)**
- **Cursor & GitHub Copilot (`.cursor/skills/`)**
- **Open-Source Agent CLI (`npx skills`)**

By default, running our one-click installer deploys all skills to **both** Google Antigravity (`~/.gemini/config/skills`) and the universal agent registry (`~/.agents/skills`), giving you immediate superpower across every AI tool on your machine.

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

## 📦 Elite Skills Catalog (117 Skills)

### 📐 Computer-Aided Design (CAD) & Parametric Engineering (2 Skills)

| Skill | Description |
| :--- | :--- |
| [`fusion-360`](skills/fusion-360/SKILL.md) | Automate Autodesk Fusion parametric models with the Python API, inspect timeline features, and prepare CAM workflows for review. |
| [`solidworks`](skills/solidworks/SKILL.md) | Automate SOLIDWORKS parts and assemblies with COM, Python, and VBA; inspect FeatureManager rebuild errors, configure mates, and batch-export CAD files. |

### 🌌 Google Antigravity & Agentic Customizations (11 Skills)

| Skill | Description |
| :--- | :--- |
| [`agy-customizations`](skills/agy-customizations/SKILL.md) | Comprehensive guide and reference for the Antigravity Customization System: loading priority, discovery mechanisms, skills, rules, plugins, hooks, and MCP servers. |
| [`android-cli`](skills/android-cli/SKILL.md) | Instructions for installing and using the `android` CLI: create projects, run apps, manage virtual devices, take screenshots, UI inspection, and SDK management. |
| [`antigravity-guide`](skills/antigravity-guide/SKILL.md) | Authoritative reference and sitemap for Google Antigravity (AGY CLI, Antigravity 2.0, IDE, Python SDK, slash commands, keybindings, and customizations). |
| [`automation`](skills/automation/SKILL.md) | Interactive guide to design and create scheduled background automations and recurring cron tasks. |
| [`generative_ui`](skills/generative_ui/SKILL.md) | Render rich interactive HTML widgets inline in chat or as standalone artifacts (diagrams, data visualizations, controls, educational walkthroughs). |
| [`google-antigravity-sdk`](skills/google-antigravity-sdk/SKILL.md) | Design, implement, and debug autonomous AI agents and multi-agent systems using the official Google Antigravity (AGY) SDK. |
| [`crewai-orchestration-suite`](skills/crewai-orchestration-suite/SKILL.md) | Master CrewAI Multi-Agent Orchestration Suite: Architecture decisions, mandatory CLI scaffolding (crewai create flow), Agent design (Role-Goal-Backstory), Task design, Structured outputs, Flow state machines (@start/@listen), YAML configs, tool integration, and official documentation lookup via docs.crewai.com/llms.txt. Complete all-in-one suite. |
| [`migrate-workflows`](skills/migrate-workflows/SKILL.md) | Automatically migrate legacy workflows to modern skills across global and workspace configurations. |
| [`permissioned-github`](skills/permissioned-github/SKILL.md) | Guidelines for interacting with GitHub and requesting user permissions safely when commands fail due to sandbox restrictions. |
| [`plugin`](skills/plugin/SKILL.md) | Create and manage Antigravity plugins — namespaced bundles of skills, agents, rules, MCP servers and hooks. |
| [`run-workflow`](skills/run-workflow/SKILL.md) | Author and run dynamic workflow scripts with the `run_workflow` automation engine. |


### 🎮 Game Development, 3D & Shaders

| Skill | Description |
| :--- | :--- |
| [`2d-pixel-sprite-sheet-pipeline`](skills/2d-pixel-sprite-sheet-pipeline/SKILL.md) | Architect and execute an end-to-end 2D pixel-art sprite production pipeline without mixels (sub-pixel artifacts). Covers South anchor discipline, deterministic 5-step Pixel Snap, directional anchors (NSEW), connected-component frame recovery, I2V walk cycles, size contracts (16/32/64/128/256), runtime ground alignment, and the complete WAT deterministic CLI toolkit. |
| [`3d-character-sheet-pipeline`](skills/3d-character-sheet-pipeline/SKILL.md) | Turn a single 2D character concept image (any pose, any style) into a complete production-ready 3D reference package — strict-front A-pose sheet (2K, Nano Banana Pro), orthographic 3-projection visual reference sheet (GPT-Image-2.5), individually extracted parts in matching strict-front orientation (body, limbs, head, hair, accessories), vision-classifier anti-3/4 drift verification loop, and downstream routing to Tripo H3.1/P1, Rodin, and Patina PBR textures for Unreal Engine 5 and Unity. |
| [`3dviz-pro-max`](skills/3dviz-pro-max/SKILL.md) | Design and build expressive 3D scenes, explainers and interactive models with grounded subject knowledge. Use for 3D creation or edits, including scientific visualization and spatial puzzles. |
| [`autonomous-game-slice-director`](skills/autonomous-game-slice-director/SKILL.md) | Architect and orchestrate long-running autonomous game development marathons (24h-48h). Enforces greybox-first MVP in <2.5h, disk-backed compaction survival (PLAN/PROGRESS/REPORT), world-space outcome probes vs naive logs, compile race prevention, ACES camera grading, minimap static baking, shader keep-alive guards, and automated asset storage cleanup based on the World of Oldcraft 36h autonomous MMO post-mortem. |
| [`blender-game-rigging-animation`](skills/blender-game-rigging-animation/SKILL.md) | Automate Blender headless rigging, skinning, bone roll stabilization, animation baking, and FBX export for Unreal Engine 5 and Unity. Solves generative 3D pivot misalignment (center_glb_bottom.py), Mixamo rest-pose lean back (25-30°), walk cycle skating (20-37° drift), foot sliding (reducing 6.9cm slide to 0.02cm), quadruped two-bone IK rigging, and certified engine export standards. |
| [`game-ai-behavior-tree`](skills/game-ai-behavior-tree/SKILL.md) | Design and implement hierarchical Game AI Behavior Trees, Unreal Engine 5 StateTree state machines, Utility AI, and creature spawning/patrol engines. Enforces composite nodes (Selectors, Sequences), Decorators, Blackboard shared state memory, Catmull-Rom spline patrol motion with dwell times, delta-level aggro radiuses (5m to 40m), tactical kiting/retreat state machines for ranged enemies, and UE5 StateTree evaluators, tasks, and state transitions. |
| [`game-animation-polish-juice`](skills/game-animation-polish-juice/SKILL.md) | Architect and implement game feel, tactile combat juice, Skullgirls animation polish, and turn-to-travel locomotion phase matching across 2D/3D game engines (Unreal Engine 5, Unity, Godot). Enforces the Anticipation-Snap-Hitstop-Recovery curve, 64-sample gait phase matching, foot-lock grounding, and multi-genre impact synchronization. |
| [`game-asset-hunter-curator`](skills/game-asset-hunter-curator/SKILL.md) | Discover, curate, and automatically download free, certified game-ready assets across public repositories (Poly Haven, Fab.com, Kenney.nl, Poly Pizza, ambientCG, OpenGameArt, Freesound). Enforces the Hunt-Before-Build triage matrix, automated CREDITS.md license logging, and direct piping to Blender game-ready sanitization. |
| [`game-engine`](skills/game-engine/SKILL.md) | Expert skill for building web-based game engines and games using HTML5, Canvas, WebGL, and JavaScript. Use when asked to create games, build game engines, implement game physics, handle collision detection, set up game loops, manage sprites, add game controls, or work with 2D/3D rendering. Covers techniques for platformers, breakout-style games, maze games, tilemaps, audio, multiplayer via WebRTC, and publishing games. |
| [`game-ready-3d-assets`](skills/game-ready-3d-assets/SKILL.md) | Pipeline complet de génération et d'optimisation d'assets 3D Game-Ready (PBR, Pivot Z=0, échelle métrique, LOD0/1/2, collision UCX et contrôle qualité visuel) via serveurs MCP 3D et Blender headless. Couvre la conversion Image-to-3D, le nettoyage topologique et la génération procédurale modulaire (murs, caisses, tuyaux). |
| [`game-save-state-manager`](skills/game-save-state-manager/SKILL.md) | Implement robust game save systems and state persistence. Enforces atomic disk writes, corruption detection (checksums/HMAC), backward-compatible schema migrations, and slot management. |
| [`gameplay-ability-system`](skills/gameplay-ability-system/SKILL.md) | Architect and implement a robust Gameplay Ability System (GAS) and Spell/Aura Virtual Machine for abilities, attributes, tags, and status effects. Enforces Attribute Sets, Gameplay Tags, instant/duration/infinite Gameplay Effects, Two-roll spell attack tables, PPM/rPPM proc engines, 18s PvP diminishing returns, Pandemic 30% duration rollover, and dynamic SpellMod/glyph alteration pipelines. |
| [`kinematic-character-controller`](skills/kinematic-character-controller/SKILL.md) | Design and implement responsive 2D and 3D kinematic character controllers with premium game feel, tactile juice, and Unreal Engine 5.5 - 5.8 Motion Matching. Enforces Coyote Time (80-130ms), Jump Buffering (100-150ms), variable jump height, apex floatiness, slope projection, Two-Bone Inverse Kinematics (IK) for foot placement, trauma-based screen shake (T²), hitstop freeze-frames, audio pitch randomization, and UE5 Motion Matching (Pose Search Databases, Chooser Tables, Trajectory sampling, and Inertialization blending). |
| [`mixamo-animation-library-engine`](skills/mixamo-animation-library-engine/SKILL.md) | Programmatic, zero-credential animation acquisition of 90+ production-ready humanoid FBX clips directly from Hugging Face (Linzhan/Mixamo-Animations-Characters). Features automated SHA-256 integrity verification, categorized core animation catalog (locomotion, 1H sword & shield, 2H greatsword, archery, magic casting, hit reactions, deaths, social emotes), and seamless integration into Unreal Engine 5 and Unity animation state machines. |
| [`mmo-tab-target-combat-pipeline`](skills/mmo-tab-target-combat-pipeline/SKILL.md) | World of Warcraft style MMORPG Engine. Covers Tab-Targeting combat, single-roll attack tables (Miss/Dodge/Parry/Block/Crit), Threat & Hate List (110% melee / 130% ranged), Quest DAG prerequisite engines, NPC Gossip dialogue trees, 8-tier faction reputation matrices, and MMORPG Head-Up Display (portrait frames, radial cooldown action bars, dynamic threat nameplates, floating combat text). |
| [`slang-shader-engineer`](skills/slang-shader-engineer/SKILL.md) | Use when working with Slang shaders, shader modules, HLSL-compatible GPU code, graphics pipelines, compute shaders, tessellation, ray tracing, parameter blocks, generics, interfaces, capabilities, cross-compilation, shader optimization, shader review, or C++ engine integration for Slang. Trigger on any mention of Slang, .slang files, slangc, SPIR-V from Slang, Slang modules, [shader("compute")], [shader("vertex")], or requests to write/review/refactor shader code with modern language features. Also trigger for Slang-to-HLSL/GLSL/Metal/CUDA cross-compile questions, or when the user says "shader" alongside "generics", "interfaces", "parameter blocks", "autodiff", or "capabilities". |
| [`ue5-mcp-automation`](skills/ue5-mcp-automation/SKILL.md) | Control Unreal Engine 5 programmatically from AI agents using the Model Context Protocol (MCP) and Python remote bridge. Automates actor manipulation, Blueprint generation, Node Graph pin wiring, UMG UI, and viewport camera automation via TCP socket 55557. |
| [`ue5-metasound-procedural-audio`](skills/ue5-metasound-procedural-audio/SKILL.md) | Architect and implement Unreal Engine 5 MetaSound procedural audio graphs and World of Warcraft style 3D audio spatial ambience. Sample-accurate digital signal processing (DSP), dynamic combat audio, SoundEntries relationals with weighted random variation, surface-material footstep triggers, equal-power zone crossfading, music priority stacks with combat grace periods, and ducking compressors. |
| [`ue5-nanite-substrate-chaos-pipeline`](skills/ue5-nanite-substrate-chaos-pipeline/SKILL.md) | Architect and implement next-generation Unreal Engine 5.5 - 5.8 rendering, materials, and physics. Unifies Nanite virtualized micro-polygon geometry (Hi-Z occlusion culling, meshlet cluster trees), Lumen dynamic Global Illumination (Surface Cache, Mesh Distance Fields), Substrate modular BSDF materials (Slab layers, energy conservation), and Chaos Physics (Voronoi Geometry Collections, strain damage thresholds, physics field impulses, and active physical ragdolls). |
| [`ue5-pcg-world-generation`](skills/ue5-pcg-world-generation/SKILL.md) | Architect and implement Unreal Engine 5 Procedural Content Generation (PCG) Framework graphs. Generates massive open-world biomes, point grids, Poisson disk distributions, spline samplers, and integrates with World Partition. |
| [`unity`](skills/unity/SKILL.md) | Automate Unity editor and runtime workflows with C#, Addressables, render pipelines, and batch builds. |

### 📱 Mobile Development (Expo, React Native, iOS, Android, EAS)

| Skill | Description |
| :--- | :--- |
| [`jetpack-compose-suite`](skills/jetpack-compose-suite/SKILL.md) | Comprehensive Android Jetpack Compose Master Suite: Architecture, Modern Authoring, Navigation 3, Lifecycle Coroutines, and Automated Diagnostic Auditing & Scoring (Kotlin 2.0+ / Strong Skipping Mode). |
| [`eas-app-stores`](skills/eas-app-stores/SKILL.md) | Build and submit iOS and Android apps with EAS to TestFlight, the App Store, or Google Play. Supports Expo and other React Native projects, plus existing native apps. Use for eas.json setup, release pipelines, signing, app versions and build numbers, store submissions, and listing metadata. For Expo websites and API routes, use eas-hosting; for adding React Native screens to a native app, use expo-brownfield. |
| [`eas-hosting`](skills/eas-hosting/SKILL.md) | Deploy Expo websites and Expo Router API routes to EAS Hosting - export the web bundle, run eas deploy for production and PR preview URLs, manage environment secrets and custom domains, and work within the Cloudflare Workers runtime. Also covers authoring API routes (+api.ts handlers, HTTP methods, request handling, CORS). Use when deploying an Expo web app or API routes, setting up EAS Hosting, or configuring hosting environments and domains. Not for native builds or store releases - use the eas-app-stores skill for those. |
| [`eas-update`](skills/eas-update/SKILL.md) | Configure and use EAS Update for over-the-air JavaScript and asset updates with expo-updates and EAS CLI. Use when setting up OTA updates, running eas update:configure or eas update, publishing to preview/staging/production channels, explaining branches/channels/runtime versions, testing updates, or debugging why an installed build still shows old code. Load for TestFlight, preview, or production updates that do not appear, including questions about cold launches or reopening the app. Not for update health metrics; use eas-update-insights for adoption, crashes, and rollout monitoring. |
| [`eas-workflows`](skills/eas-workflows/SKILL.md) | Helps understand and write EAS workflow YAML files for Expo projects. Use this skill when the user asks about CI/CD or workflows in an Expo or EAS context, mentions .eas/workflows/, or wants help with EAS build pipelines or deployment automation. |
| [`expo-animation`](skills/expo-animation/SKILL.md) | Build animations in React Native and Expo, making the decisions in the order that determines whether they feel right — should it animate, which thread it runs on, which properties, spring or timing, how the gesture hands off, how it degrades. Writes the implementation with Reanimated, Gesture Handler, Expo Router and expo-haptics. Use when animating anything in an Expo app, adding gestures, sheets, screen transitions, press feedback or haptics, or fixing motion that stutters on device. For web animation use `animate`. |
| [`expo-app-clip`](skills/expo-app-clip/SKILL.md) | Add an iOS App Clip target to an Expo app. Use when the user mentions App Clip, AASA, apple-app-site-association, appclips, smart app banner, or wants to ship a lightweight iOS Clip invoked from a URL alongside their parent app. |
| [`expo-brownfield`](skills/expo-brownfield/SKILL.md) | Integrate Expo and React Native into an existing native iOS or Android app. Use for brownfield, embedding a React Native screen in SwiftUI/UIKit or Kotlin, or AAR/XCFramework packaging. Covers isolated and integrated approaches. For building or distributing a purely native app with EAS, use eas-app-stores. |
| [`expo-data-fetching`](skills/expo-data-fetching/SKILL.md) | Use when implementing or debugging ANY network request, API call, or data fetching. Covers fetch API, React Query, SWR, error handling, caching, offline support, loading/empty/error screen states, and Expo Router data loaders (`useLoaderData`). |
| [`expo-module`](skills/expo-module/SKILL.md) | Guide for creating and writing Expo native modules and views using the Expo Modules API (Swift, Kotlin, TypeScript). Covers module definition DSL, native views, shared objects, config plugins, lifecycle hooks, autolinking, and type system. Use when building or modifying native modules for Expo. Not for migrating an existing Swift module from the definition DSL to the Expo Modules API 2.0 macros; use expo-migrate-module (from the expo-experiments plugin) for that. |
| [`expo-native-ui`](skills/expo-native-ui/SKILL.md) | Build beautiful, native-feeling Expo screens. Covers Apple HIG styling, semantic colors, native controls, SF Symbols, media, visual effects, gradients, storage, and responsive layout. For routing and navigation, use the expo-router skill; for motion and animation, use the expo-animation skill. |
| [`expo-router`](skills/expo-router/SKILL.md) | Navigation and routing for Expo Router. Covers file-based routes, groups and dynamic routes, folder organization, Link with previews and context menus, native Stack, page titles, modals and form sheets, NativeTabs, headers and toolbars, and header search bars. |
| [`expo-upgrade`](skills/expo-upgrade/SKILL.md) | Guidelines for upgrading Expo SDK versions and fixing dependency issues |
| [`expo-web-to-native`](skills/expo-web-to-native/SKILL.md) | Migrate an existing web React app to a native iOS/Android app with Expo. Use when the user wants to turn a website into a mobile app, port a Next.js/Vite/CRA React codebase to React Native, reuse web code on native incrementally, or asks how web idioms (the DOM, CSS, React Router, localStorage, window) map to native. This is the end-to-end migration guide; use the `expo-dom` skill for the DOM-component mechanism itself. |
| [`material-3`](skills/material-3/SKILL.md) | Implement Google's Material Design 3 (Material You) UI system. Primary: Jetpack Compose |
| [`mobile-app-ui-design`](skills/mobile-app-ui-design/SKILL.md) | Design high-quality mobile app UI/UX screens, flows, and components. Use this skill whenever the user asks to design a mobile app screen, create app mockups, build mobile UI components, improve an existing mobile app design, create onboarding flows, design mobile navigation, or requests any mobile-first interface work. Also trigger when the user mentions app design, mobile UI, mobile UX, screen design, app mockups, wireframes, or wants to build React Native / Flutter / SwiftUI style interfaces as visual prototypes. Even if the user just says "design an app" or "make this screen look better", use this skill. |

### 🎨 Frontend Craft, UI/UX, Design Systems & Accessibilité

| Skill | Description |
| :--- | :--- |
| [`accessibility-audit-engine`](skills/accessibility-audit-engine/SKILL.md) | Automated and manual accessibility testing engine enforcing WCAG 2.2 Level AA/AAA and European Accessibility Act (EAA) compliance. Integrates axe-core, Pa11y CLI, ARIA pattern validation, keyboard focus trap detection, and screen reader compatibility audits. |
| [`algorithmic-art`](skills/algorithmic-art/SKILL.md) | Creating algorithmic art using p5.js with seeded randomness and interactive parameter exploration. Use this when users request creating art using code, generative art, algorithmic art, flow fields, or particle systems. Create original algorithmic art rather than copying existing artists' work to avoid copyright violations. |
| [`anti-ui-slop`](skills/anti-ui-slop/SKILL.md) | Master Anti-UI Slop & UI Design Pro System. Eliminates generic AI-generated interfaces and builds production-grade software by combining UIZZE 800,000+ real web and iOS screens with 25+ foundational design laws (color theory, OKLCH, typography, card spacing, micro-interactions). |
| [`banner-design`](skills/banner-design/SKILL.md) | Design banners for social media, ads, website heroes, creative assets, and print. Multiple art direction options with optional generated or supplied visuals. Actions: design, create, generate banner. Platforms: Facebook, Twitter/X, LinkedIn, YouTube, Instagram, Google Display, website hero, print. Styles: minimalist, gradient, bold typography, photo-based, illustrated, geometric, retro, glassmorphism, 3D, neon, duotone, editorial, collage. |
| [`design-system`](skills/design-system/SKILL.md) | Token architecture, component specifications, and slide generation. Three-layer tokens (primitive→semantic→component), CSS variables, spacing/typography scales, component specs, strategic slide creation. Use for design tokens, systematic design, brand-compliant presentations. |
| [`design-taste-frontend`](skills/design-taste-frontend/SKILL.md) | tasteskill v2, the anti-slop frontend skill. Art direction for websites, distilled from a study of |
| [`frontend-reference-match`](skills/frontend-reference-match/SKILL.md) | Exact reference-matching frontend reproduction pipeline. Enforces strict visual matching, local serving (http://localhost:3000), multi-round Puppeteer screenshot diffing, and anti-generic craft guardrails (banning default Tailwind palettes, flat shadows, and transition-all). |
| [`image-to-code`](skills/image-to-code/SKILL.md) | Elite website image-to-code skill for Codex. For visually important web tasks, it must first generate the design image(s) itself, deeply analyze them, then implement the website to match them as closely as possible. In Codex, it must prefer large, readable, section-specific images instead of tiny compressed boards, generate fresh standalone images for sections or detail views instead of cropping old ones, avoid lazy under-generation, avoid cards-inside-cards-inside-cards UI, and keep the hero clean, spacious, readable, and visible on a small laptop. |
| [`shadcn`](skills/shadcn/SKILL.md) | Manages shadcn components and projects — adding, searching, fixing, debugging, styling, and composing UI, including chat interfaces. Provides project context, component docs, and usage examples. Applies when working with shadcn/ui, component registries, presets, --preset codes, or any project with a components.json file. Also triggers for "shadcn init", "create an app with --preset", "switch to --preset", and for building a design system or applying a DESIGN.md or brand spec to shadcn/ui. |
| [`typeui-design-systems`](skills/typeui-design-systems/SKILL.md) | Curated registry of 67 distinct design system themes (bento, brutalism, neobrutalism, claymorphism, glassmorphism, neumorphism, editorial, retro, corporate, matrix, etc.) with pre-defined color palettes, typography scales, spacing tokens, and component guidelines. Use when styling a new web application, choosing a visual identity, or generating themed UI components. |
| [`ui-ux-pro-max`](skills/ui-ux-pro-max/SKILL.md) | UI/UX design intelligence for web, mobile, and desktop. This skill should be used when designing, building, reviewing, or fixing interfaces, including pages, components, design systems, accessibility, interaction, responsive layout, typography, color, charts, and stack-specific UI implementation. Searchable local data: 79 searchable styles (50 active), 192 product palettes and reasoning profiles, 74 font pairings, 119 UX guidelines, 105 icons, 17 GSAP presets, 25 chart types, and 22 stacks. |
| [`web-artifacts-builder`](skills/web-artifacts-builder/SKILL.md) | Suite of tools for creating elaborate, multi-component claude.ai HTML artifacts using modern frontend web technologies (React, Tailwind CSS, shadcn/ui). Use for complex artifacts requiring state management, routing, or shadcn/ui components - not for simple single-file HTML/JSX artifacts. |

### 🛡️ Cybersecurity, DevSecOps, Privacy & Governance

| Skill | Description |
| :--- | :--- |
| [`agent-owasp-compliance`](skills/agent-owasp-compliance/SKILL.md) | | |
| [`bridgesecurity-auditor`](skills/bridgesecurity-auditor/SKILL.md) | Perform senior-level security audits, input defense, and Zero-Trust secrets governance based on BridgeMind BridgeSecurity standards. Scans for OWASP Top 10, CWE Top 25, high-entropy secrets and API keys, actively defends against prompt-injections during web scraping, enforces age/SOPS envelope encryption in Git, ephemeral environment injection, and native in-memory secret masking (Zero-Docker). |
| [`compliance-privacy-gdpr-engineer`](skills/compliance-privacy-gdpr-engineer/SKILL.md) | Audit and implement software privacy compliance, GDPR/RGPD regulations, open-source license compatibility, and European AI Act requirements. Enforces privacy-by-design, cookie consent architectures, right-to-erasure workflows, data processing registers, and license risk triage. |
| [`loopcraft-harness-engineer`](skills/loopcraft-harness-engineer/SKILL.md) | Use this skill when designing, setting up, or executing autonomous agentic loops, self-healing test harnesses, continuous verification pipelines, automated error classification (SYNTAX, RUNTIME, TEST_FAIL, LINT, SECURITY), or SonarQube / ISO 25010 Quality Gates. Enforces systematic plan-code-test-diagnose cycles with up to 8 bounded iterations. |
| [`remove-ai-slops`](skills/remove-ai-slops/SKILL.md) | Removes AI-generated code smells from branch changes or an explicit file list behind regression tests. Use when the user asks to clean up, deslop, or remove AI-slop patterns from recent changes. |
| [`senior-code-reviewer`](skills/senior-code-reviewer/SKILL.md) | Conduct structured senior-level code reviews and anti-bloat architectural audits following Google, Anthropic, and Swyx's Smol Architect standards. Classifies findings by strict severity tiers (Critical, Major, Minor, Nit), audits logic flaws, eliminates speculative generality, prunes dead code, and inlines single-use indirections. |
| [`skill-security-auditor`](skills/skill-security-auditor/SKILL.md) | Audit and verify third-party AI agent skills and plugins before installation. Detects prompt injections in markdown/docstrings, dangerous tool permissions (raw shell execution, network exfiltration, arbitrary file system writes), dependency supply-chain risks, and issues a deterministic PASS / WARN / FAIL security verdict. |
| [`systematic-debugging`](skills/systematic-debugging/SKILL.md) | Investigate and resolve complex bugs using the Anthropic SWE-bench Systematic Debugging standard. Enforces root-cause investigation, deterministic reproduction scripts, difference analysis, and regression guards before applying code fixes. |
| [`tech-debt-audit`](skills/tech-debt-audit/SKILL.md) | Thorough, file-cited technical debt audit across 9 dimensions using AST-grep (tree-sitter), grep, LSP, and language-native tooling. Produces TECH_DEBT_AUDIT.md with severity, effort estimates, and prioritized fixes. Use when asked for codebase health check, tech debt audit, architecture review, code quality assessment, or cleanup planning. Triggers: 'tech debt', 'technical debt', 'debt audit', 'code health', 'technical debt audit', 'codebase health check', 'find tech debt', 'debt analysis', 'audit code quality'. |
| [`test-driven-development`](skills/test-driven-development/SKILL.md) | Enforce strict Test-Driven Development (TDD) using the Red-Green-Refactor cycle combined with generative property-based testing and invariant fuzzing inspired by Hypothesis and QuickCheck. Forbids writing production code without a failing test, validates test failure semantics, and generates randomized edge-case inputs (surrogate Unicode, boundary numbers, empty sequences) to discover hidden boundary bugs. |
| [`visual-qa`](skills/visual-qa/SKILL.md) | Runs rigorous visual QA across web, terminal, and paginated surfaces: an Apple HIG-based checklist, paired light/dark captures at phone and desktop widths, screenshot evidence, and a per-item PASS/FAIL verdict. Use for any UI build or change, or when asked whether a page, component, or TUI looks right or follows the platform's design guidelines. |
| [`vuln-scan`](skills/vuln-scan/SKILL.md) | Static source-code vulnerability scan. Reads a target directory (and |

### 📊 Data Engineering, Databases & Modern Data Stack

| Skill | Description |
| :--- | :--- |
| [`ast-grep`](skills/ast-grep/SKILL.md) | Searches and rewrites code by AST shape across 25 languages. Use when the target is a syntax pattern (every call/class/import shaped like X, a codemod, a YAML rule) rather than literal text; for plain strings, comments, or filenames, use rg. |
| [`datasette-sqlite-detective`](skills/datasette-sqlite-detective/SKILL.md) | Investigate, profile, and audit SQLite databases using Simon Willison Datasette Detective standards, while guarding schema evolution without data loss. Validates WAL mode, foreign key integrity, missing indexes, query plan efficiency (EXPLAIN QUERY PLAN), table fragmentation, detects schema drift between code models and production databases, and generates reversible UP/DOWN migration scripts. |
| [`dbt-data-pipeline-engineer`](skills/dbt-data-pipeline-engineer/SKILL.md) | Design, orchestrate, and test scalable data transformation pipelines using dbt (data build tool), modern orchestrators (Dagster, Prefect, Airflow), and cloud data warehouses (BigQuery, Snowflake). Covers staging/intermediate/marts modeling, lineage graphs, incremental models, and automated data quality tests. |
| [`docx`](skills/docx/SKILL.md) | Use this skill whenever the user wants to create, read, edit, or manipulate Word documents (.docx files) or Word templates (.dotx files). Triggers include: any mention of 'Word doc', 'word document', '.docx', '.dotx', or requests to produce professional documents with formatting like tables of contents, headings, page numbers, or letterheads. Also use when extracting or reorganizing content from .docx or .dotx files, inserting or replacing images in documents, performing find-and-replace in Word files, working with tracked changes or comments, or converting content into a polished Word document. If the user asks for a 'report', 'memo', 'letter', 'template', or similar deliverable as a Word or .docx file, use this skill. Do NOT use for PDFs, spreadsheets, Google Docs, or general coding tasks unrelated to document generation. |
| [`duckdb-parquet-analyst`](skills/duckdb-parquet-analyst/SKILL.md) | Perform high-performance columnar analytics, query Parquet datasets, and benchmark data pipelines using DuckDB, while enforcing dataset quality based on Andrew Ng Data-Centric AI standards (detecting duplicate records, missing fields, distribution skew, corrupted types, and statistical anomalies in scraped supermarket datasets). |
| [`excel-architect`](skills/excel-architect/SKILL.md) | Design and generate production-grade Excel spreadsheets (.xlsx) using openpyxl. Enforces professional styling, native formulas (SUM, AVERAGE, XLOOKUP), auto-fit column widths, freeze panes, data filters, and zebra-striping without file corruption. |
| [`fastapi-sqlite-production`](skills/fastapi-sqlite-production/SKILL.md) | Architect and implement production-grade asynchronous FastAPI services with concurrent SQLite persistence (WAL mode, busy_timeout), Pydantic V2 schemas, JWT auth with refresh tokens, and ultra-lean native execution (uv/venv, zero-Docker). |
| [`pdf`](skills/pdf/SKILL.md) | Use this skill whenever the user wants to do anything with PDF files. This includes reading or extracting text/tables from PDFs, combining or merging multiple PDFs into one, splitting PDFs apart, rotating pages, adding watermarks, creating new PDFs, filling PDF forms, encrypting/decrypting PDFs, extracting images, and OCR on scanned PDFs to make them searchable. If the user mentions a .pdf file or asks to produce one, use this skill. |
| [`postgresql-production-dba`](skills/postgresql-production-dba/SKILL.md) | Design, optimize, and manage production PostgreSQL databases. Covers 3NF relational modeling, B-Tree/GIN/GiST index tuning, EXPLAIN (ANALYZE, BUFFERS) query optimization, zero-downtime schema migrations (CREATE INDEX CONCURRENTLY, lock timeouts), connection pooling (PgBouncer), and modern ORMs/query builders (Drizzle, Prisma, SQLAlchemy). |
| [`pptx`](skills/pptx/SKILL.md) | Use this skill any time a .pptx or .potx file is involved in any way — as input, output, or both. This includes: creating slide decks, pitch decks, or presentations; reading, parsing, or extracting text from any .pptx or .potx file (even if the extracted content will be used elsewhere, like in an email or summary); editing, modifying, or updating existing presentations; combining or splitting slide files; working with templates (.potx), layouts, speaker notes, or comments. Trigger whenever the user mentions \"deck,\" \"slides,\" \"presentation,\" or references a .pptx or .potx filename, regardless of what they plan to do with the content afterward. If a .pptx or .potx file needs to be opened, created, or touched, use this skill. |
| [`python-pypi-package-builder`](skills/python-pypi-package-builder/SKILL.md) | End-to-end skill for building, testing, linting, versioning, and publishing a production-grade Python library to PyPI. Covers all four build backends (setuptools+setuptools_scm, hatchling, flit, poetry), PEP 440 versioning, semantic versioning, dynamic git-tag versioning, OOP/SOLID design, type hints (PEP 484/526/544/561), Trusted Publishing (OIDC), and the full PyPA packaging flow. Use for: creating Python packages, pip-installable SDKs, CLI tools, framework plugins, pyproject.toml setup, py.typed, setuptools_scm, semver, mypy, pre-commit, GitHub Actions CI/CD, or PyPI publishing. |
| [`stealth-hybrid-scraper-architect`](skills/stealth-hybrid-scraper-architect/SKILL.md) | Architect and implement resilient anti-detection web scrapers for supermarket pricing (Colruyt, Delhaize, Carrefour). Enforces JA4 TLS fingerprint spoofing via curl_cffi, hybrid clearance cookie harvesting, and modular ETL pipelines. |

### ☁️ Cloud, DevOps, IaC, SRE & Observabilité

| Skill | Description |
| :--- | :--- |
| [`devops-infrastructure-as-code`](skills/devops-infrastructure-as-code/SKILL.md) | Architect and implement declarative Infrastructure as Code (IaC) and containerization using Terraform/OpenTofu, Docker multi-stage builds, and Kubernetes (K8s/Helm). Enforces immutable infrastructure, remote state locking, least-privilege non-root containers, health probes, resource limits, and production Kubernetes manifests. |
| [`monorepo-release-engineering`](skills/monorepo-release-engineering/SKILL.md) | Manage monorepos, release automation, and software supply chains: Turborepo/Nx, pnpm workspaces, automated Semantic Versioning (SemVer), changelog generation, Software Bill of Materials (SBOM), and CI/CD secret management (Vault/SOPS). |
| [`sre-observability-slos`](skills/sre-observability-slos/SKILL.md) | Design and manage Site Reliability Engineering (SRE) systems: SLI/SLO definition, error budget calculation and burn rates, Prometheus metric collectors & alerting rules, Grafana dashboard architecture, blameless incident post-mortems, and load testing with k6. |

### 💳 Backend Architecture, APIs & SaaS Revenue Systems

| Skill | Description |
| :--- | :--- |
| [`enterprise-i18n-localization`](skills/enterprise-i18n-localization/SKILL.md) | Architect and implement software internationalization (i18n) and localization (l10n). Covers ICU MessageFormat, plural and gender rules, Right-to-Left (RTL) layout mirroring (Arabic, Hebrew), locale-aware date/currency formatters, pseudo-localization testing, and multilingual SEO (hreflang). |
| [`saas-backend-architecture`](skills/saas-backend-architecture/SKILL.md) | Design and implement production SaaS backend services: OAuth2/OIDC, JWT & RBAC/ABAC authorization, Stripe Checkout & Billing subscriptions, webhook HMAC signature verification with idempotency keys, Redis caching & rate limiting, background job queues (BullMQ/Celery), and transactional email delivery (Resend). |

### 🤖 Agent Architecture, LLM Engineering & RAG

| Skill | Description |
| :--- | :--- |
| [`acquire-codebase-knowledge`](skills/acquire-codebase-knowledge/SKILL.md) | Use this skill when the user explicitly asks to map, document, or onboard into an existing codebase. Trigger for prompts like "map this codebase", "document this architecture", "onboard me to this repo", or "create codebase docs". Do not trigger for routine feature implementation, bug fixes, or narrow code edits unless the user asks for repository-level discovery. |
| [`agent-architecture`](skills/agent-architecture/SKILL.md) | Design AI agent architectures through requirements discovery, or audit and diagnose architectural flaws in existing agents. Architecture only; excludes implementation and general code review. |
| [`claude-api`](skills/claude-api/SKILL.md) | | |
| [`context-engineering`](skills/context-engineering/SKILL.md) | Optimize agent token budgets, context quality, prevent context rot, and architect LLM prompt caching strategies for Anthropic Claude, Google Gemini, and OpenAI. Prunes redundant files, generates high-density scratchpad summaries, enforces selective reading, deterministic tool schema ordering, static cache prefix structuring, cache hit telemetry, and 80%+ API cost reductions. |
| [`mcp-builder`](skills/mcp-builder/SKILL.md) | Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. Use when building MCP servers to integrate external APIs or services, whether in Python (FastMCP) or Node/TypeScript (MCP SDK). |
| [`rag-vector-search-engineer`](skills/rag-vector-search-engineer/SKILL.md) | Design and implement production Retrieval-Augmented Generation (RAG) and semantic search architectures. Covers document chunking (semantic, recursive), vector embeddings, vector databases (pgvector, Qdrant), hybrid search (dense + BM25 sparse), Cohere/BGE reranking, and automated RAG evaluation (Ragas triad: faithfulness, answer relevance, context precision). |
| [`rust-mcp-server-generator`](skills/rust-mcp-server-generator/SKILL.md) | Generate a complete Rust Model Context Protocol server project with tools, prompts, resources, and tests using the official rmcp SDK |
| [`skill-creator`](skills/skill-creator/SKILL.md) | Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch, edit, or optimize an existing skill, run evals to test a skill, benchmark skill performance with variance analysis, or optimize a skill's description for better triggering accuracy. |
| [`unlazy`](skills/unlazy/SKILL.md) | Enforces completion discipline for substantial autonomous work by writing acceptance gates before execution, decomposing work with the Depth Tree, running approved checks, and re-verifying evidence before reporting. Use when an agent faces a long or multi-part task, work that has returned half-done, an exhaustive audit or build, parallel leaves or pipelines, or explicit triggers such as /unlazy, $unlazy, "tree N", "gates", and "do not stop until it is done". |
| [`wat-framework`](skills/wat-framework/SKILL.md) | Architect and execute agentic workflows using the WAT (Workflows, Agents, Tools) paradigm. Separates probabilistic AI reasoning from deterministic Python tools to eliminate compounding error rates and achieve 99%+ reliability. |

### 🔬 Science, Rigorous Mathematics & Humanoid Robotics

| Skill | Description |
| :--- | :--- |
| [`humanoid-robotics-architect`](skills/humanoid-robotics-architect/SKILL.md) | Use this skill when the user asks to design, evaluate, or document humanoid robot architectures, actuator sizing, degrees of freedom (DoF), URDF modeling, or Sim-to-Real pipelines. |
| [`math-rigor-tutor`](skills/math-rigor-tutor/SKILL.md) | Use this skill when the user asks to explain, verify, or solve mathematical concepts, analysis, functions, limits, proofs, calculus, linear algebra, or LaTeX mathematical notation. |
| [`minecraft-plugin-development`](skills/minecraft-plugin-development/SKILL.md) | Complete Paper, Spigot, and Bukkit Minecraft plugin suite. Covers plugin.yml, event listeners, schedulers, custom commands, player persistent data, minigame state machines, Adventure/MiniMessage text, plus French localization and i18n translation preserving placeholders (%player%, {0}) and YAML structure for plugins like KingdomsX. |
| [`rust-engineer`](skills/rust-engineer/SKILL.md) | Use this skill when the user asks to develop, debug, or optimize Rust code, Cargo crates, Bevy game components, memory-safe data structures, or systems algorithms. |
| [`swiftui-skills`](skills/swiftui-skills/SKILL.md) | Comprehensive Apple SwiftUI Master Suite. Unifies Apple-authored architectural guidance extracted directly from Xcode (Liquid Glass, on-device LLMs, SwiftData inheritance, 3D Charts, Swift Concurrency) with complete UI component patterns and navigation recipes (TabView, NavigationStack, forms, sheets, lists, async state, focus, theming). |

### 🎬 Video Editing, Sound Design & Motion

| Skill | Description |
| :--- | :--- |
| [`app-promo-reel`](skills/app-promo-reel/SKILL.md) | Generate beat-synced 30 s vertical (9:16) or feed (4:5) promo reels, or a silent seamless 16:9 web-hero loop, for a mobile app — music from ACE-Step 1.5, MusicGen or the user's own track, a kick-locked beat grid, the app's real UI rebuilt as HTML, HyperFrames render, loudness and sync checks. Use when the user asks for promo / social / showreel videos of an app. Generation only; it never posts or uploads anything. |
| [`cinetic`](skills/cinetic/SKILL.md) | Direct, build and render premium cinematic motion design from code — launch films, product and feature videos, looping feature animations for landing pages and social, logo stings and reveals, UI walkthroughs, app demos, kinetic type, teasers, trailers, intros and promo clips. Use this whenever the user wants any video, animation, motion graphic or animated demo made with Remotion, HyperFrames, HTML/GSAP or React, or asks to storyboard, time, score, render, polish or critique one — even if they only say "make a video about X", "animate this feature" or "we need a launch clip". It supplies concept and copy discipline, type and colour taste that defers to a supplied brand, a beat-locked timeline that drives both picture and a code-made soundtrack, choreography and transition craft, real product UI in motion, film-grade finishing (true motion blur, no banding, BT.709, sync-checked mux) and a measured self-critique loop on contact sheets and renders. |
| [`gsap-core`](skills/gsap-core/SKILL.md) | Comprehensive GSAP 3 Master Suite. Covers core engine (to, from, fromTo, easing, staggers), timelines (gsap.timeline, position parameter, nesting), gsap.utils (clamp, mapRange, snap, wrap, toArray), ScrollTrigger (pinning, scrub, snap, horizontal scroll), official React integration (@gsap/react useGSAP hook, cleanup, refs), and premium plugins (Flip, Draggable, SplitText, Inertia, ScrambleText). |
| [`real-sound`](skills/real-sound/SKILL.md) | Build premium, realistic soundtracks for code-made videos and animations from real licensed recordings - launch films, product and feature videos, UI walkthroughs, logo stings, explainers, trailers and animated shorts made with Remotion, HyperFrames, three.js, GSAP or any renderer. Use this whenever a video or animation needs sound design, SFX, foley, ambience, music, a soundtrack, a score, UI click / whoosh / riser / impact / logo-sting sounds, or a music edit to picture; whenever a synthesized or "random" sounding soundtrack must be replaced with real recordings; or when the user asks to source, license, credit, mix, master, critique or mux audio for a film. It covers cue lists from the picture, sourcing from Freesound / Mixkit / composer libraries with licence checks, a music edit at bar lines, a JSON sound design rendered by a deterministic mixer, measured QA (clicks, masking, harshness, sync, loudness) plus earshot listening, a multi-agent critique, mastering, credits and the mux. |
| [`reel-cut`](skills/reel-cut/SKILL.md) | End-to-end automated face-cam video production pipeline (derush, kinetic typography, camera moves, and SFX). Transcribes words via Whisper, detects silences with FFmpeg, curates best takes, cuts precisely at silence midpoints, and generates interactive HyperFrames DOM compositions with 0.12s lead verbatim subtitles, camera drifts/punch-ins, and synchronized zero-royalty audio SFX. Use when asked to "derush", "coupe les blancs", "monte mon reel", "ajoute des sous-titres", or "reel-cut". |
| [`repurpose-youtube-video`](skills/repurpose-youtube-video/SKILL.md) | Repurpose YouTube videos into high-converting LinkedIn, Instagram, and X (Twitter) posts with platform-optimized visuals via the Blotato API, running post log tracking, and zero-leak credential handling. |

### 📑 Product Management, Specifications & Enterprise Productivity

| Skill | Description |
| :--- | :--- |
| [`brand`](skills/brand/SKILL.md) | Brand voice, visual identity, messaging frameworks, asset management, brand consistency. Activate for branded content, tone of voice, marketing assets, brand compliance, style guides. |
| [`product-management-spec-engineer`](skills/product-management-spec-engineer/SKILL.md) | Author professional Product Requirements Documents (PRD), Technical Architecture RFCs, Architecture Decision Records (ADRs), and Agile sprint planning user stories with INVEST criteria and explicit acceptance tests. |
| [`slides`](skills/slides/SKILL.md) | Create strategic HTML presentations with Chart.js, design tokens, responsive layouts, copywriting formulas, and contextual slide strategies. |
| [`vibe-aso`](skills/vibe-aso/SKILL.md) | Full-funnel App Store Optimization for an iOS app — keyword research (popularity/difficulty driven), a keyword-led name/subtitle/keyword field, App Store metadata localized into up to 50 locales, localized screenshot headings burned over your mockups, worldwide territory pricing, and in-app string localization. Use when the user wants to "do the ASO", "find keywords", "localize my app / my App Store page / my screenshots", "pick a name and subtitle", "set worldwide prices", or is preparing an App Store submission. |
| [`webapp-testing`](skills/webapp-testing/SKILL.md) | Toolkit for interacting with and testing local web applications using Playwright. Supports verifying frontend functionality, debugging UI behavior, capturing browser screenshots, and viewing browser logs. |

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