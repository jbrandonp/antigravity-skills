#!/bin/bash
# Wrapper cron : exécute le drift check en mode silencieux (alerte seulement si dérive)
exec python3 /home/arthur/.hermes/scripts/model-drift-check.py --cron
