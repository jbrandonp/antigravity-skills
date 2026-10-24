#!/usr/bin/env bash
# Portable runner for Vinted MCP server
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec node "$SCRIPT_DIR/node_modules/@andrijdavid/vinted-mcp/dist/bundle.js"
