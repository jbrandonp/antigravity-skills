#!/usr/bin/env bash
# One-click installer for Antigravity Skills & Plugins on Linux / macOS
set -euo pipefail

DEST_GEMINI="${HOME}/.gemini/config"
DEST_SKILLS="${DEST_GEMINI}/skills"
DEST_PLUGINS="${DEST_GEMINI}/plugins"

echo "=== Installing Antigravity Skills & Plugins ==="
mkdir -p "${DEST_SKILLS}" "${DEST_PLUGINS}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

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

echo "✓ Installation complete! Restart Google Antigravity to load all customizations."
