#!/usr/bin/env python3
"""Purge finale des références BTP2026 dans la doc (décision : plus de mot de passe)."""
import os

fixes = {
    "/srv/brandon-ai/workspaces/bttp/bttp/05_Outils_et_Modeles_Excel/append_new_devis.py": [
        ('    password: str = "",  # vide = dérivé par client via bttp_password (jamais BTP2026 partagé)',
         '    password: str = "",  # SANS mot de passe par défaut (décision Brandon 18/11 — risque de perte d\'accès)'),
    ],
    "/srv/brandon-ai/workspaces/bttp/bttp/05_Outils_et_Modeles_Excel/README.md": [
        ("← Le classeur maître BTP protégé (5 onglets, mot de passe : BTP2026)",
         "← Le classeur maître BTP (5 onglets, protégé SANS mot de passe — décision Brandon 18/11)"),
        ("- **Mot de passe de protection :** `BTP2026`",
         "- **Protection de la feuille :** active SANS mot de passe (anti-mauvaise-manipulation ; le client peut déverrouiller à tout moment)"),
    ],
    "/srv/brandon-ai/workspaces/bttp/bttp/04_Operations_et_Formation_Client/PACK_BIENVENUE_ET_FORMATION_CLIENT.md": [
        ("- Mot de passe de déverrouillage de maintenance : `BTP2026`.",
         "- La protection des feuilles est SANS mot de passe (décision du fournisseur 18/11/2026) : déverrouillable à tout moment via Révision > ôter la protection de la feuille."),
    ],
}
for path, pairs in fixes.items():
    src = open(path, encoding="utf-8").read()
    n = 0
    for old, new in pairs:
        if old in src:
            src = src.replace(old, new); n += 1
    open(path, "w", encoding="utf-8").write(src)
    print(f"{'✅' if n else '⚠️'} {os.path.basename(path)}: {n} remplacement(s)")

# clé maître dérivée : inutile maintenant → désactiver (déplacer vers archive, pas supprimer)
key = os.path.expanduser("~/.hermes/secrets/bttp-clients.key")
if os.path.exists(key):
    import shutil
    os.makedirs("/srv/data/bttp-confidentiel/_archives", exist_ok=True)
    shutil.move(key, "/srv/data/bttp-confidentiel/_archives/bttp-clients.key.retired-2026-11-18")
    print("✅ clé maître dérivée archivée (désactivée, non supprimée)")
