#!/usr/bin/env python3
"""Applique la reformulation « Copilote » aux documents commerciaux (validation Brandon
18/11 : « fais le brouillon copilote »). Décisions tranchées :
- nom « Copilote » conservé (Pack 3 s'appelait déjà « Copilote Financier & Rituels »)
- chiffre « 3× » ADOUCCI (aucune source dans le dossier stratégique)
- accroche J0 : variante B ajoutée en A/B (test sur les 10 premiers contacts)"""
import datetime

DOCS = {
    "/srv/brandon-ai/workspaces/bttp/bttp/03_Vente_et_Prospection_Terrain/MANUEL_PROSPECTION_VENTE_ET_TERRAIN.md": [
        # 1. Pack 3 reformulé « Copilote » (embauche, pas logiciel)
        ("│  • Pack 3 Copilote Financier & Rituels : 195 € HTVA / trimestre (65 €/m)│",
         "│  • Pack 3 « Votre Copilote » : 195 € HTVA / trimestre (65 €/m)      │"),
        # 2. Accroche J0 : variante B ajoutée après l'existante (A/B)
        ("""> Je ne cherche pas à vous vendre un logiciel supplémentaire : mon travail consiste à vérifier s'il existe des tâches répétitives ou des pertes de temps qui pourraient être simplifiées directement avec vos outils actuels *(Excel, boîte mail, etc.)*.
>
> Seriez-vous disponible pour un court échange de 10 à 15 minutes ?""",
         """> Je ne cherche pas à vous vendre un logiciel supplémentaire : mon travail consiste à vérifier s'il existe des tâches répétitives ou des pertes de temps qui pourraient être simplifiées directement avec vos outils actuels *(Excel, boîte mail, etc.)*.
>
> Seriez-vous disponible pour un court échange de 10 à 15 minutes ?
>
> **— VARIANTE B (angle embauche, A/B test sur les 10 premiers contacts) :**
>
> Monsieur [Nom], la question qui suit va paraître étrange : combien vous coûtent les devis que vous n'avez pas relancés ? Dans le BTP, un devis sur deux n'est jamais relancé — et chaque devis relancé a beaucoup plus de chances d'être signé.
>
> Je ne vends pas de logiciel : je vous installe un copilote qui relance vos devis à votre place, chaque semaine, avec vos mots. Vous ne changez rien à votre façon de travailler. 15 minutes pour voir si ça vous convient — je m'adapte à votre agenda."""),
        # 3. ROI vs salaire ajouté (argumentaire Copilote)
        ("│  GARANTIE : Si le système ne vous fait pas gagner de temps dès la      │",
         """│  ARGUMENT ROI : 65 €/mois vs ~4 000 € chargés d'un secrétaire        │
│  administratif. Relances chaque semaine (pas « quand il y a du      │
│  temps »), rapport patron le 1er du mois, jamais de congé,          │
│  données exportables en un clic (elles restent À VOUS).             │
│                                                                      │
│  GARANTIE : Si le système ne vous fait pas gagner de temps dès la      │"""),
    ],
    "/srv/brandon-ai/workspaces/bttp/bttp/03_Vente_et_Prospection_Terrain/BON_DE_COMMANDE_PROPOSITION_COMMERCIALE.md": [
        # nom Pack 3 harmonisé si l'ancien libellé y figure
        ("Pack 3 Copilote Financier & Rituels", "Pack 3 « Votre Copilote »"),
    ],
}
for path, pairs in DOCS.items():
    src = open(path, encoding="utf-8").read()
    n = 0
    for old, new in pairs:
        if old in src:
            src = src.replace(old, new, 1); n += 1
    open(path, "w", encoding="utf-8").write(src)
    print(f"{'✅' if n else '⚠️'} {path.split('/')[-1]}: {n} modification(s)")

# 4. Brouillon marqué appliqué + décisions tracées
p = "/srv/brandon-ai/workspaces/obsidian-vault/09-Content/brouillons/2026-11-18-copilote-reformulation-offre.md"
src = open(p, encoding="utf-8").read()
src = src.replace("> **Statut : BROUILLON.**",
"> **Statut : APPLIQUÉ le 18/11/2026** (validation Brandon : « fais le brouillon copilote »). Décisions : nom « Copilote » conservé ; chiffre « 3× » adouci (aucune source dans le dossier stratégique) ; variante B en A/B sur les 10 premiers contacts.")
src = src.replace("- [ ] Garder le nom « Copilote » ou un autre ?",
"- [x] Garder le nom « Copilote » — **conservé** (déjà dans le manuel §1.1)")
src = src.replace("- [ ] Le chiffre « devis relancé = 3× plus de chances » vient du dossier stratégique — le garder avec sa source ou l'adoucir ?",
"- [x] Chiffre « 3× » — **adouci** : aucune source trouvée dans le dossier stratégique (vérifié grep 18/11) → « beaucoup plus de chances »")
src = src.replace("- [ ] Tester la nouvelle accroche J0 seulement sur les 10 premiers contacts (A/B) ou basculer direct ?",
"- [x] A/B — **variante B sur les 10 premiers contacts** (prudence : mesurer avant bascule)")
open(p, "w", encoding="utf-8").write(src)
print("✅ brouillon : statut APPLIQUÉ + 3 décisions tracées")
