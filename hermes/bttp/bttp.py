# -*- coding: utf-8 -*-
"""
Alias exécutable du Poste de Commandement Universel BTTP.
Permet d'exécuter `python bttp.py [status|btp|sales|jev|test|audit]`.
"""

from __future__ import annotations

import sys
from pathlib import Path

RACINE_PROJET = Path(__file__).resolve().parent
if str(RACINE_PROJET) not in sys.path:
    sys.path.insert(0, str(RACINE_PROJET))

from main import main

if __name__ == "__main__":
    main()
