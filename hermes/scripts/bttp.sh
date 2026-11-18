#!/bin/bash
# Wrapper Hermes : pilote le Poste de Commandement BTTP depuis n'importe où.
# Usage : bttp.sh [status|btp|sales|jev|test|audit] (sous-commandes de main.py)
exec python3 /srv/brandon-ai/workspaces/bttp/bttp/bttp.py "$@"
