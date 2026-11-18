#!/bin/bash
# Veille BTTP : health check silencieux hebdo (no_agent).
# Sortie vide si tout va bien ; alerte si l'orchestrateur échoue ou la queue disparaît.
cd /srv/brandon-ai/workspaces/bttp/bttp || { echo "🚨 BTTP : dossier introuvable"; exit 0; }
PROBLEMES=""
python3 bttp.py status > /tmp/bttp-status.txt 2>&1 || PROBLEMES="$PROBLEMES\n- orchestrateur status en échec"
grep -q "CONFORME" /tmp/bttp-status.txt || PROBLEMES="$PROBLEMES\n- un pôle non conforme"
[ -f 03_Vente_et_Prospection_Terrain/outreach_queue.json ] || PROBLEMES="$PROBLEMES\n- outreach_queue.json manquant"
python3 run_all_tests.py > /tmp/bttp-tests.txt 2>&1 || PROBLEMES="$PROBLEMES\n- tests en échec"
if [ -n "$PROBLEMES" ]; then
  echo -e "🚨 BTTP — anomalies détectées:$PROBLEMES"
else
  echo ""
fi
