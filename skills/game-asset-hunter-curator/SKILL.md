---
name: game-asset-hunter-curator
description: "Discover, curate, and automatically download free, certified game-ready assets across public repositories (Poly Haven, Fab.com, Kenney.nl, Poly Pizza, ambientCG, OpenGameArt, Freesound). Enforces the Hunt-Before-Build triage matrix, automated CREDITS.md license logging, and direct piping to Blender game-ready sanitization."
---

# Game Asset Hunter & Free Repository Curator

Use this skill when looking for game assets of any type (3D models, PBR textures, environment kits, foliage, sound effects, music, or 2D UI icons) across certified free and public domain repositories before wasting time or generative credits creating them from scratch.

---

## 🧒 1. Explication Pédagogique (Style 15 ans)

Pourquoi passer 3 heures à sculpter un tonneau en bois, coder une caisse avec une IA ou dépenser des crédits payants pour générer un caillou ou un bruit de pas... alors que des studios professionnels ont déjà mis en ligne **des dizaines de milliers d'assets parfaits, gratuits et libres de droits (CC0)** ?

C'est la règle d'or des développeurs malins : **"Ne réinvente jamais la roue."**
- Si tu as besoin d'un arbre, d'une chaise, d'un sol en pierre, d'une potion ou d'un son d'épée : **tu cherches d'abord dans les banques gratuites certifiées**.
- Tu ne réserves la modélisation ou l'IA générative 3D (Rodin / Tripo) **que pour les éléments uniques de ton jeu** : ton héros principal, un boss géant spécifique, ou une arme légendaire liée à ton histoire.

Ce skill sait exactement où chercher, télécharge les modèles directement par script, génère le fichier `CREDITS.md` pour être 100% dans la légalité, et passe automatiquement l'asset dans Blender pour coller son pivot au sol ($Z=0$) et créer sa boîte de collision.

---

## 🎯 2. La Matrice de Triage : Quand Chercher vs Quand Fabriquer ?

```
                        [ Besoin d'un Asset ]
                                  |
            +---------------------+---------------------+
            |                                           |
    [ Asset Générique ou Décor ? ]              [ Asset Héro / Signature ? ]
    - Tonneau, caisse, banc, rocher             - Héros jouable custom
    - Arbre, herbe, texture de terre            - Boss final du scénario
    - Bruit de pas, son de vent                 - Arme emblématique du lore
    - Icône d'épée standard, potions            - Bâtiment central unique
            |                                           |
            v                                           v
    ⭐ 1. CHANGER & TÉLÉCHARGER GRATUIT         🤖 2. GÉNÉRATION IA 3D SUR MESURE
    (Poly Haven, Fab.com, Kenney, Freesound)    (Skill: game-ready-3d-assets / Rodin)
```

---

## 🌐 3. Les 12 Banques d'Assets Gratuites Incontournables

### 📦 3D Models, Décors & PBR
| Répertoire | Type & Licence | URL & Spécificité |
|---|---|---|
| **Poly Haven** | 100% CC0 (Domaine public) | [`polyhaven.com`](https://polyhaven.com) — 500+ modèles ultra-propres (mobilier, props, nature) avec textures PBR 1K à 8K. API directe intégrée. |
| **Fab.com (Epic Games)** | Gratuit / Fab Free Content | [`fab.com`](https://www.fab.com) — Remplace l'Unreal Marketplace et Sketchfab. Contenu gratuit mensuel de très haute volée + Quixel Megascans photogrammétriques gratuits. |
| **Kenney.nl** | 100% CC0 (Le "Sauveur des Indés") | [`kenney.nl/assets`](https://kenney.nl/assets) — 20 000+ assets modulaires low-poly (Nature, Château, Donjon, Ville, Spatial, Meubles). Zéro royalties. |
| **Poly Pizza** | Gratuit / CC-BY / CC0 | [`poly.pizza`](https://poly.pizza) — Milliers de modèles low-poly optimisés avec téléchargement direct GLB. API intégrée. |
| **ambientCG** | 100% CC0 | [`ambientcg.com`](https://ambientcg.com) — 2 000+ matériaux PBR procéduraux (Albedo, Normal, Roughness, Displacement) en haute définition. |
| **Itch.io Game Assets** | Gratuit / CC0 / MIT | [`itch.io/game-assets/free`](https://itch.io/game-assets/free) — Packs complets d'indés (donjons rétro, tuiles 3D, props). |

### 🎨 2D Sprites, Pixel Art & UI
| Répertoire | Type & Licence | URL & Spécificité |
|---|---|---|
| **Game-Icons.net** | CC BY 3.0 (Attribution) | [`game-icons.net`](https://game-icons.net) — 4 000+ icônes vectorielles nettes (sorts, armes, potions, armures). Indispensable pour l'inventaire RPG. |
| **OpenGameArt.org** | CC0 / Open Source | [`opengameart.org`](https://opengameart.org) — Répertoire historique communautaire (tilesets 2D, spritesheets, interfaces). |
| **Kenney UI Packs** | 100% CC0 | [`kenney.nl/assets/category:UI`](https://kenney.nl/assets/category:UI) — Boutons, barres de vie, cadres de dialogue fantasy et sci-fi. |

### 🔊 Audio, Bruitages (SFX) & Musique
| Répertoire | Type & Licence | URL & Spécificité |
|---|---|---|
| **Freesound.org** | CC0 / Creative Commons | [`freesound.org`](https://freesound.org) — 600 000+ sons réels (bruits de pas sur bois/pierre, coups d'épée, sorts, ambiances). |
| **Sonniss GDC Archive** | Commercial Royalty-Free | [`sonniss.com/gameaudiogdc`](https://sonniss.com/gameaudiogdc) — Plus de 150 Go d'enregistrements audio de niveau cinéma offerts chaque année pour la GDC. |
| **Incompetech (Kevin MacLeod)**| CC BY 4.0 / CC0 | [`incompetech.com`](https://incompetech.com) — Musiques d'ambiance orchestrales complètes pour jeux vidéo. |

---

## 🛠️ 4. Outil Déterministe : Chasseur & Téléchargeur CLI

Le script Python intégré [`hunt_free_assets.py`](scripts/hunt_free_assets.py) recherche et télécharge les assets directement par commande :

```bash
# 1. Rechercher un asset (ex: tonneau, rocher, chaise, épée)
python .gemini/config/skills/game-asset-hunter-curator/scripts/hunt_free_assets.py barrel

# 2. Télécharger un modèle PBR Poly Haven en un clic (textures 1K/2K incluses)
python .gemini/config/skills/game-asset-hunter-curator/scripts/hunt_free_assets.py --download Barrel_01 --out-dir ./assets/raw

# 3. Lister les packs 3D complets de Kenney.nl (nature, donjon, château)
python .gemini/config/skills/game-asset-hunter-curator/scripts/hunt_free_assets.py --list-kenney
```

---

## 🔗 5. La Passerelle Automatique Game-Ready

Ne jamais insérer un asset téléchargé brut dans ton moteur de jeu sans vérification.
Dès qu'un modèle est téléchargé via `hunt_free_assets.py`, passe-le directement dans notre pipeline d'assainissement Blender :

```bash
blender --background --python .gemini/config/skills/game-ready-3d-assets/scripts/game_ready_pipeline.py -- \
  --input "./assets/raw/Barrel_01.gltf" \
  --output "./assets/ready/SM_Barrel_01_GameReady.glb" \
  --name "SM_Barrel_01" \
  --target-height 0.9 \
  --qa-image "./assets/qa/qa_Barrel_01.png"
```
**Résultat immédiat :** Le tonneau gratuit est redimensionné à 0.9 m, son pivot est posé à $Z=0$ au sol, 3 LODs sont calculés, et une boîte de collision convexe étanche `UCX_` est créée pour Unreal Engine 5.

---

## ⚖️ 6. Conformité Légale & Traçabilité (`CREDITS.md`)

- **Règle absolue :** Tout asset téléchargé sous licence `CC-BY` ou `CC0` est automatiquement consigné dans [`CREDITS.md`](CREDITS.md) avec son nom, l'auteur original et le lien source.
- **Interdiction formelle :** Ne jamais télécharger d'assets sous licence non-commerciale (`CC-NC`), de rips de jeux propriétaires protégés par copyright, ou de packs sans licence explicite.
