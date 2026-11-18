#!/usr/bin/env python3
"""Purge finale 2 : les 7 dernières références BTP2026 (docs stratégiques et manuel)."""
fixes = {
    "/srv/brandon-ai/workspaces/bttp/bttp/05_Outils_et_Modeles_Excel/bttp_password.py": [
        ("— Mot de passe Excel DÉRIVÉ par client (plus jamais BTP2026 partagé).",
         "— (ancien outil de dérivation, remplacé par : AUCUN mot de passe Excel par défaut)."),
    ],
    "/srv/brandon-ai/workspaces/bttp/bttp/03_Vente_et_Prospection_Terrain/MANUEL_PROSPECTION_VENTE_ET_TERRAIN.md": [
        ("La télé-formation finale et la remise du mot de passe de protection de la feuille (`BTP2026`) se font après réception de la preuve de virement du solde.",
         "La télé-formation finale se fait après réception de la preuve de virement du solde. Les feuilles du classeur sont protégées SANS mot de passe (décision 18/11/2026) : déverrouillables à tout moment par le client via Révision > ôter la protection."),
    ],
    "/srv/brandon-ai/workspaces/bttp/bttp/README.md": [
        ("← Classeur maître BTP protégé (5 onglets, mot de passe : BTP2026)",
         "← Classeur maître BTP (5 onglets, protection SANS mot de passe — décision 18/11/2026)"),
    ],
    "/srv/brandon-ai/workspaces/bttp/bttp/01_Strategie_et_Audits/diagnostic_and_audit_rubrics.md": [
        ("verrouiller colonne 9 avec mot de passe `BTP2026`.",
         "verrouiller colonne 9 (protection sans mot de passe, décision 18/11/2026)."),
    ],
    "/srv/brandon-ai/workspaces/bttp/bttp/01_Strategie_et_Audits/AUDIT_CRITIQUE_ET_STRESS_TEST_COMPLET.md": [
        ("sécurisation par cellules protégées (`BTP2026`)",
         "sécurisation par cellules protégées (sans mot de passe — anti-mauvaise-manipulation, décision 18/11/2026)"),
        ("Remise du mot de passe administrateur `BTP2026`. Le client reste propriétaire à 100 % de son historique.",
         "Le classeur est livré protégé SANS mot de passe (aucun risque de perte d'accès). Le client reste propriétaire à 100 % de son historique."),
    ],
    "/srv/brandon-ai/workspaces/bttp/bttp/01_Strategie_et_Audits/gdpr_and_data_security_btp.md": [
        ("Les formules du classeur sont verrouillées sous le mot de passe standard `BTP2026`.",
         "Les formules du classeur sont protégées SANS mot de passe (anti-mauvaise-manipulation ; aucun risque de perte d'accès, décision 18/11/2026)."),
    ],
}
for path, pairs in fixes.items():
    src = open(path, encoding="utf-8").read()
    n = 0
    for old, new in pairs:
        if old in src:
            src = src.replace(old, new); n += 1
    open(path, "w", encoding="utf-8").write(src)
    print(f"{'✅' if n else '⚠️'} {path.split('/')[-1]}: {n}")
