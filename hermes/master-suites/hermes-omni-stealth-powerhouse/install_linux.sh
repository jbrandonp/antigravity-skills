#!/usr/bin/env bash
# =====================================================================
# Script d'installation Ultra-Lean v5.5 pour VPS Linux Hetzner (Ubuntu / Debian)
# Immunisé contre PEP 668, optimisé pour 0,00 % de risque d'abus Hetzner.
# =====================================================================

set -e

INSTALL_DIR="$HOME/.hermes/stealth"
VENV_DIR="$INSTALL_DIR/venv"

echo "🚀 [1/4] Installation des dépendances système Linux minimales..."
sudo apt-get update -qq
sudo apt-get install -y -qq python3-pip python3-venv curl \
    libglib2.0-0 libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 libcups2 \
    libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 \
    libgbm1 libpango-1.0-0 libcairo2 libasound2

echo "📦 [2/4] Création de l'environnement virtuel dédié (Protection PEP 668)..."
mkdir -p "$INSTALL_DIR"
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
    echo "   -> Venv créé dans $VENV_DIR"
fi

echo "📦 [3/4] Installation des dépendances Python dans le venv..."
"$VENV_DIR/bin/pip" install --upgrade pip -q
"$VENV_DIR/bin/pip" install -r requirements.txt -q

echo "🌐 [4/4] Installation de Chromium Headless Playwright..."
"$VENV_DIR/bin/playwright" install chromium

echo "⚡ Test de validation et diagnostic immédiat..."
"$VENV_DIR/bin/python" scripts/stealth_master.py health

echo "✅ Hermes Omni-Stealth Powerhouse v5.5 est 100% prêt et blindé sur ce VPS Linux !"
