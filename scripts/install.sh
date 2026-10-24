#!/usr/bin/env bash
# One-click installer for Antigravity, Hermes & Universal AI Agent Skills
set -euo pipefail

TARGET="${1:-All}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# 1. Antigravity Installation (~/.gemini/config and ~/.gemini/antigravity)
if [ "$TARGET" = "All" ] || [ "$TARGET" = "Antigravity" ]; then
    DEST_GEMINI="${HOME}/.gemini/config"
    DEST_SKILLS="${DEST_GEMINI}/skills"
    DEST_PLUGINS="${DEST_GEMINI}/plugins"
    DEST_MCP="${HOME}/.gemini/antigravity/mcp"

    echo "=== Installing Antigravity Customizations (~/.gemini/config) ==="
    mkdir -p "${DEST_SKILLS}" "${DEST_PLUGINS}" "${DEST_MCP}"

    echo "--> Copying skills to ${DEST_SKILLS}..."
    cp -R "${SCRIPT_DIR}/skills/"* "${DEST_SKILLS}/"

    echo "--> Copying plugins (Science, Stitch, Android, Firebase, etc.) to ${DEST_PLUGINS}..."
    cp -R "${SCRIPT_DIR}/plugins/"* "${DEST_PLUGINS}/"

    if [ -d "${SCRIPT_DIR}/mcp" ]; then
        echo "--> Copying MCP tool schemas to ${DEST_MCP}..."
        cp -R "${SCRIPT_DIR}/mcp/"* "${DEST_MCP}/"
    fi

    if [ ! -f "${DEST_GEMINI}/config.json" ]; then
        echo "--> Installing default config.json..."
        cp "${SCRIPT_DIR}/config/config.template.json" "${DEST_GEMINI}/config.json"
    fi

    if [ ! -f "${DEST_GEMINI}/mcp_config.json" ]; then
        echo "--> Installing default mcp_config.json..."
        cp "${SCRIPT_DIR}/config/mcp_config.template.json" "${DEST_GEMINI}/mcp_config.json"
    fi
fi

# 2. Universal Agent Skills Installation (~/.agents/skills)
if [ "$TARGET" = "All" ] || [ "$TARGET" = "Agents" ]; then
    DEST_AGENTS="${HOME}/.agents/skills"
    echo "=== Installing Universal Agent Skills (~/.agents/skills) ==="
    mkdir -p "${DEST_AGENTS}"

    echo "--> Deploying core skills to ${DEST_AGENTS} for Claude Code, Cursor, Copilot & npx skills..."
    cp -R "${SCRIPT_DIR}/skills/"* "${DEST_AGENTS}/"

    SCIENCE_SKILLS="${SCRIPT_DIR}/plugins/science/skills"
    if [ -d "${SCIENCE_SKILLS}" ]; then
        echo "--> Deploying DeepMind Science skills into ${DEST_AGENTS}..."
        for d in "${SCIENCE_SKILLS}"/*/; do
            dirname=$(basename "$d")
            canonical="${dirname//_/-}"
            cp -R "$d" "${DEST_AGENTS}/${canonical}"
        done
    fi

    for p in "${SCRIPT_DIR}/plugins"/stitch-*; do
        if [ -d "$p/skills" ]; then
            echo "--> Deploying $(basename "$p") skills into ${DEST_AGENTS}..."
            for d in "$p/skills"/*/; do
                dirname=$(basename "$d")
                cp -R "$d" "${DEST_AGENTS}/stitch-${dirname}"
            done
        fi
    done

    # Deploy Hermes Mega-Suites & Master-Suites into ~/.agents/skills
    if [ -d "${SCRIPT_DIR}/hermes/mega-suites" ]; then
        echo "--> Deploying Hermes Mega-Suites into ${DEST_AGENTS}..."
        cp -R "${SCRIPT_DIR}/hermes/mega-suites/"* "${DEST_AGENTS}/"
    fi
    if [ -d "${SCRIPT_DIR}/hermes/master-suites" ]; then
        echo "--> Deploying Hermes Master-Suites into ${DEST_AGENTS}..."
        cp -R "${SCRIPT_DIR}/hermes/master-suites/"* "${DEST_AGENTS}/"
    fi
fi

# 3. Hermes Autonomous Agent Ecosystem (~/.hermes/skills and ~/.hermes/mcp)
if [ "$TARGET" = "All" ] || [ "$TARGET" = "Hermes" ]; then
    DEST_HERMES_SKILLS="${HOME}/.hermes/skills"
    DEST_HERMES_MCP="${HOME}/.hermes/mcp"
    echo "=== Installing Hermes Autonomous Suite (~/.hermes) ==="
    mkdir -p "${DEST_HERMES_SKILLS}" "${DEST_HERMES_MCP}"

    echo "--> Copying Hermes Mega-Suites (10) and Master-Suites (50) to ${DEST_HERMES_SKILLS}..."
    cp -R "${SCRIPT_DIR}/hermes/mega-suites/"* "${DEST_HERMES_SKILLS}/"
    cp -R "${SCRIPT_DIR}/hermes/master-suites/"* "${DEST_HERMES_SKILLS}/"

    echo "--> Copying Hermes MCP servers (eBay, Vinted, Web Tools) to ${DEST_HERMES_MCP}..."
    cp -R "${SCRIPT_DIR}/hermes/mcp-servers/"* "${DEST_HERMES_MCP}/"
fi

# 4. Anthropic Claude Code Installation (~/.claude/skills)
if [ "$TARGET" = "All" ] || [ "$TARGET" = "Claude" ]; then
    DEST_CLAUDE_SKILLS="${HOME}/.claude/skills"
    echo "=== Installing Claude Code Skills (~/.claude/skills) ==="
    mkdir -p "${DEST_CLAUDE_SKILLS}"

    echo "--> Deploying Antigravity Elite Skills & Hermes Mega-Suites to ${DEST_CLAUDE_SKILLS}..."
    cp -R "${SCRIPT_DIR}/skills/"* "${DEST_CLAUDE_SKILLS}/"
    cp -R "${SCRIPT_DIR}/hermes/mega-suites/"* "${DEST_CLAUDE_SKILLS}/"
fi

echo "✓ Installation complete! 172 skills & suites (112 elite, 10 mega-suites, 50 master suites, 41 science, 16 stitch) and 8 MCP servers are active and ready."
