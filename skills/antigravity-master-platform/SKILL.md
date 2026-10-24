---
name: antigravity-master-platform
description: "Authoritative Google Antigravity (AGY) Platform & Customization Master Suite: Antigravity IDE, CLI (agy), Antigravity 2.0 app architecture, official Python SDK agent orchestration, and complete customization engine (skills, rules, plugins, lifecycle hooks, and MCP servers)."
category: agentic
risk: safe
tags: ["antigravity", "agy", "antigravity-sdk", "customizations", "plugins", "hooks", "mcp", "rules"]
---

# Google Antigravity (AGY) Master Platform Suite

The complete, authoritative guide and toolchain for developing, orchestrating, and customizing AI agents on **Google Antigravity**.

---

## 🧭 1. Antigravity Surfaces & Sitemap

# Google Antigravity (AGY) Guide & Sitemap

Google Antigravity is an AI-first development platform. Depending on which
surface the user is asking about, you **MUST** read the corresponding
subdocumentation in the `references/` directory of this skill:

## 1. Surfaces Sitemap (Offline Subdocs)

-   **Antigravity CLI (`agy`)**: [references/cli.md](references/cli.md)
    -   Pointers to the authoritative public CLI docs for slash commands,
        features, settings, and best practices.
-   **Antigravity IDE**: [references/ide.md](references/ide.md)
    -   Covers the standalone AI-first IDE, sidebar chat panels, and inline code
        lenses.
-   **Antigravity 2.0**: [references/app.md](references/app.md)
    -   Covers the parallel desktop application, left-hand sidebar, chat canvas,
        and the HTML Auxiliary Pane (Subagents, Background Tasks, Artifacts,
        Files Changed, Terminals).
-   **Antigravity SDK**: [references/sdk.md](references/sdk.md)
    -   Covers the public Python SDK
        (https://github.com/google-antigravity/antigravity-sdk-python) for
        programmatic agent leasing, orchestration APIs, and custom tool
        exposing.

--------------------------------------------------------------------------------

## 2. Smart Hybrid Retrieval: When to Fetch Live Docs

The offline subdocs provide excellent quick references. However, if the user
asks for the latest updates, advanced Vertex AI integrations, or complex setups
not covered here, you **MUST** dynamically fetch the live page from the official
sitemap:

<!-- LINT.IfChange(sitemap) -->

-   **Main Documentation Home**: `https://antigravity.google/docs`
-   **Skills**: `https://antigravity.google/docs/skills`
-   **Rules**: `https://antigravity.google/docs/rules-workflows`
-   **Hooks**: `https://antigravity.google/docs/hooks`
-   **Plugins**: `https://antigravity.google/docs/plugins`
-   **Sidecars**: `https://antigravity.google/docs/sidecars`
-   **Model Context Protocol (MCP)**: `https://antigravity.google/docs/mcp`
-   **Browser Automation & Testing**:
    `https://antigravity.google/docs/ide/browser`
-   **Agent Permissions & Security**:
    `https://antigravity.google/docs/permissions`
-   **Terminal Sandbox**: `https://antigravity.google/docs/sandbox`
-   **Changelog & Release Notes**: `https://antigravity.google/changelog`
-   **Troubleshooting & Support**: `https://antigravity.google/support`
    <!-- LINT.ThenChange(//depot/google3/third_party/gemini_coder/agent_ui_toolkit/dev/appVariant/externalAppVariant.ts:custom_links) -->

---

## 🤖 2. Official Google Antigravity Python SDK

# Google Antigravity SDK

## Installation & Setup

Before proceeding with any Google Antigravity tasks, ensure the environment is
ready:

-   **Verify Applicability**: If operating in an existing codebase, verify that
    using this Python SDK is possible and appropriate for the project.
-   **Check Dependencies**: Check if `google-antigravity` is listed in the
    project's dependencies (e.g., `requirements.txt`, `pyproject.toml`).
-   **Install Package**: Ensure the `google-antigravity` Python package is
    installed.
-   **Authentication Setup**: Check for a valid `GEMINI_API_KEY` environment
    variable or a `.env` file (required to access Gemini models).
    -   If credentials are missing, you MUST actively help the user get set up
        with an API key by providing the following link:
        -   Default to Google AI Studio:
            `https://aistudio.google.com/app/api-keys`
    -   Explain that the API key can be passed explicitly in code as shorthand
        (e.g., `LocalAgentConfig(api_key="...")`) or automatically read from the
        environment.

## Routing Table

Use the following information to dig deeper into specific topics based on the
user request. Read the referenced files or explore the directories to find
relevant information.

### References

-   If the user needs to understand the high-level overview and core concepts of
    the Google Antigravity SDK (Agent, Conversation, Connection), read
    [`references/sdk.md`](references/sdk.md) (Architecture section).
-   If the user needs to perform advanced agent configuration, select
    appropriate models, or understand the critical rules for model identifiers
    to avoid assumptions, read [`references/sdk.md`](references/sdk.md) (Agent Configuration section).
-   If the user needs to extend an agent's capabilities by integrating Model
    Context Protocol (MCP) servers, or configure tool permissions for the agent,
    read [`references/sdk.md`](references/sdk.md) (MCP Integration section).
-   If the user needs to define safety policies, resolve execution order, or
    restrict agent actions using predicates, read
    [`references/sdk.md`](references/sdk.md) (Safety Policies section).
-   If the user needs to debug failed agents, stream logs, or implement error
    recovery using hooks to make agents robust, read
    [`references/sdk.md`](references/sdk.md) (Error Handling section).
-   If the user needs to monitor costs, track token usage (including thinking
    tokens), or build custom audit logs for advanced monitoring, read
    [`references/sdk.md`](references/sdk.md) (Observability section).
-   If the user needs to see a list of built-in tools and understand their default state, read [`references/sdk.md`](references/sdk.md) (Built-in Tools section).

### Examples

-   If the user needs to implement basic agent behavior, streaming responses, or
    expose internal thoughts, read `examples/getting_started/hello_world.md`.
-   If the user needs to equip an agent with custom capabilities (tools) derived
    from Python functions, or maintain agent state across tool execution, read
    `examples/getting_started/custom_tool.md`.
-   If the user needs to shape an agent's persona, define its system
    instructions, or dynamically adapt its behavior, read
    `examples/getting_started/persona_config.md`.
-   If the user needs to build multimodal agents capable of processing images
    and PDFs, or generating visual content, read
    `examples/getting_started/multimodal.md`.
-   If the user needs to implement multi-agent delegation, allowing a main agent
    to spawn and orchestrate subagents for complex tasks, read
    `examples/getting_started/subagents.md`.
-   If the user needs to connect an agent to external services via MCP (Stdio or
    SSE), read `examples/getting_started/mcp_tools.md`.
-   If the user needs to create proactive agents that respond to time-based
    events or file system triggers in the background, read
    `examples/getting_started/periodic_trigger.md`.
-   If the user needs to intercept agent lifecycle events (e.g., pre/post turn,
    tool execution, errors) to customize execution flow, read
    `examples/getting_started/hooks.md`.
-   If the user needs to implement persistent agents that remember past
    interactions across sessions, read
    `examples/getting_started/persistence.md`.
-   If the user needs to override the default application data directory
    for agent artifacts, scratch files, and media storage, read
    `examples/getting_started/app_data_dir_override.md`.
-   If the user needs an agent to output structured data (e.g., JSON matching a
    Pydantic schema) for reliable integration, read
    `examples/getting_started/structured_output.md`.
-   If the user needs to add, configure, or load agent skills into the Google
    Antigravity SDK agent, read `examples/getting_started/agent_skills.md`.

---

## 🛠️ 3. Antigravity Customization System (Skills, Rules, Plugins, Hooks, MCP)

# Antigravity Customization System Guide

The Antigravity Customization System allows you to tailor the agent's behavior, teach it new workflows, enforce guidelines, and integrate it with external tools. By customizing the agent, you transition it from a general-purpose assistant into an expert pair programmer specialized in your project's codebase and processes.

---

## 💡 Comprendre le Système Antigravity (Explication Simple)

Imagine qu'Antigravity soit un **développeur junior ultra-rapide** qui débarque dans ton équipe :
1. **Les Rules (`AGENTS.md`)** : C'est le **règlement intérieur** du bureau. "Ici, on ne commite jamais de mot de passe, on type toujours le code, et on écrit en français".
2. **Les Skills (`SKILL.md` + scripts)** : Ce sont ses **fiches de compétences**. Au lieu de tout charger dans sa tête (ce qui saturerait sa mémoire immédiate), il regarde l'index de ses fiches. Quand tu lui dis "optimise cette base SQLite", il ouvre le classeur correspondant, lit la méthode et exécute les scripts.
3. **Les Plugins (`plugin.json`)** : C'est une **boîte à outils complète** qui regroupe dans un même paquet des fiches (skills), des règles (rules) et des outils externes (MCP).
4. **Les Lifecycle Hooks (`hooks.json`)** : Ce sont des **gardes du corps automatiques**. Dès que l'IA veut exécuter une commande bash, le hook s'interpose avant (`PreToolUse`) ou après (`PostToolUse`) pour vérifier que tout est sûr ou lancer un linter.
5. **Les MCP Servers (`mcp_config.json`)** : Ce sont ses **bras articulés** pour se connecter à des bases de données réelles, des navigateurs ou des APIs.

---

## 🛠️ Outils Déterministes Inclus (WAT Framework)

Le skill fournit une suite d'outils CLI Python déterministes situés dans `scripts/` :

### 1. Validateur d'Environnement Antigravity (`scripts/validate_agy_environment.py`)
Scanne et valide l'intégrité de tous tes composants (skills, plugins, hooks, MCP) :
```bash
# Audit standard de ton dossier config
python scripts/validate_agy_environment.py --config-dir ~/.gemini/config

# Export des résultats en JSON pour intégration CI/CD
python scripts/validate_agy_environment.py --config-dir ~/.gemini/config --json
```

### 2. Générateur de Customisations (`scripts/scaffold_agy_customization.py`)
Génère instantanément des squelettes conformes aux standards Antigravity :
```bash
# Créer un nouveau Skill
python scripts/scaffold_agy_customization.py --type skill --name mon-skill --desc "Description du skill" --output ./skills

# Créer un Plugin complet
python scripts/scaffold_agy_customization.py --type plugin --name mon-plugin --output ./plugins

# Créer un Hook de sécurité sur run_command
python scripts/scaffold_agy_customization.py --type hook --name audit-cmd --event PreToolUse --matcher run_command --command "python guard.py" --output ./

# Créer une Règle d'architecture
python scripts/scaffold_agy_customization.py --type rule --name clean-code-rules --output ./rules

# Déclarer un serveur MCP
python scripts/scaffold_agy_customization.py --type mcp --name sqlite-db --command "uv run mcp-server-sqlite" --output ./
```

### 3. Suite de Tests Automatisée (`scripts/tests/test_agy_customizations.py`)
Vérifie 100% du comportement du validateur et du générateur :
```bash
python scripts/tests/test_agy_customizations.py
```

---

## 📑 Customization Types: Quick Reference

| Type | Config File/Folder | Scope | Best For | Reference Docs |
| :--- | :--- | :--- | :--- | :--- |
| **Rules** | `AGENTS.md`, `GEMINI.md` | Contextual / Hierarchical | Enforcing coding styles, API restrictions, and local guidelines. | [Rules Guide](./docs/rules.md) |
| **Skills** | `skills/<name>/SKILL.md` | On-Demand (Progressive) | Teaching the agent multi-step procedures, runbooks, and tool workflows. | [Skills Guide](./docs/skills.md) |
| **Plugins** | `plugins/<name>/plugin.json` | Bundle | Packaging related skills, rules, hooks, and MCP configs into a single unit. | [Plugins Guide](./docs/plugins.md) |
| **Hooks** | `hooks.json` | Lifecycle Event | Running scripts/commands at specific agent lifecycle points (e.g., pre-tool execution). | [Hooks Guide](./docs/hooks.md) |
| **MCP Servers** | `mcp_config.json` | Tool Integration | Connecting the agent to external services and custom tool providers. | [MCP Guide](./docs/mcp_servers.md) |
| **UI Plugins** | `plugins/<name>/sidecars/` | Auxiliary Panel UI | Surfacing interactive web sidecars & chat pills via `sidecar://` URI scheme. | [UI Plugins Guide](./docs/ui-plugins-navigation.md) |

---

## ⚡ Loading Priority and Precedence

When multiple customizations are discovered, they are resolved following a strict 4-tier precedence hierarchy:

1. **Workspace Project** (`<workspace>/.agents/`): Highest priority, project-specific overrides.
2. **Declared Configurations**: Customizations explicitly listed in `skills.json` or `plugins.json`.
3. **Global User Root** (`~/.agents/` or `~/.gemini/config/`): User-wide tools and developer defaults.
4. **Built-in Customizations**: Default skills bundled with the Antigravity application runtime.

### Component Collision Policies
- **Skills**: First-hit wins (workspace overrides global).
- **Rules**: Deep merged (global rules apply, followed by workspace rules).
- **Hooks**: Sequential chaining (handlers executed in order of registration).
- **MCP Servers**: Higher-tier configuration replaces matching server keys.

---

## 📖 Architecture Deep Dive
Pour une étude approfondie des protocoles JSON, des cycles de vie des hooks et des configurations avancées, consulte :
- [Playbook Complet d'Architecture](./references/antigravity_customization_playbook.md)
- [Documentation Hooks](./docs/hooks.md)
- [Documentation Plugins](./docs/plugins.md)
- [Documentation Configurations JSON](./docs/json_configs.md)
