#!/usr/bin/env bash
# One-click installer for Antigravity & Universal AI Agent Skills
set -euo pipefail

TARGET="${1:-All}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# 1. Antigravity Installation
if [ "$TARGET" = "All" ] || [ "$TARGET" = "Antigravity" ]; then
    DEST_GEMINI="${HOME}/.gemini/config"
    DEST_SKILLS="${DEST_GEMINI}/skills"
    DEST_PLUGINS="${DEST_GEMINI}/plugins"

    echo "=== Installing Antigravity Customizations (~/.gemini/config) ==="
    mkdir -p "${DEST_SKILLS}" "${DEST_PLUGINS}"

    echo "--> Copying skills to ${DEST_SKILLS}..."
    cp -R "${SCRIPT_DIR}/skills/"* "${DEST_SKILLS}/"

    echo "--> Copying plugins to ${DEST_PLUGINS}..."
    cp -R "${SCRIPT_DIR}/plugins/"* "${DEST_PLUGINS}/"

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

    echo "--> Deploying skills to ${DEST_AGENTS} for Claude Code, Cursor, Copilot & npx skills..."
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
fi

echo "✓ Installation complete! All skills and plugins are active and ready."
