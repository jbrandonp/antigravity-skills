---
name: agy-customizations
description: >-
  Comprehensive guide and deterministic toolchain for the Antigravity Customization System.
  Use to explain how customizations work, their loading priority, discovery mechanisms,
  audit environment integrity, and scaffold skills, rules, plugins, hooks, and MCP servers.
---

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
