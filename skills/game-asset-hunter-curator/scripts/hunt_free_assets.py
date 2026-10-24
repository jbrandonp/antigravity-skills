#!/usr/bin/env python3
"""
Game Asset Hunter & Automated Free Repository Downloader
Searches and downloads free, certified CC0 game-ready assets (Poly Haven, Kenney, ambientCG, Fab.com)
and automatically updates CREDITS.md and pipes models to the Game-Ready Blender sanitizer.
"""

import urllib.request
import urllib.parse
import json
import sys
import os
import argparse
import shutil

sys.stdout.reconfigure(encoding='utf-8')

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AntigravityAssetHunter/1.0'}


def search_polyhaven_models(query=None, limit=5):
    """Recherche parmi les 500+ modèles PBR gratuits CC0 de Poly Haven (sans clé API)."""
    url = "https://api.polyhaven.com/assets?t=models"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
        
        results = []
        q_lower = query.lower() if query else ""
        for asset_id, info in data.items():
            name = info.get("name", asset_id)
            tags = [t.lower() for t in info.get("tags", [])]
            categories = [c.lower() for c in info.get("categories", [])]
            
            if not q_lower or q_lower in asset_id.lower() or q_lower in name.lower() or any(q_lower in t for t in tags):
                results.append({
                    "id": asset_id,
                    "name": name,
                    "categories": categories,
                    "tags": tags[:5],
                    "source": "Poly Haven (100% CC0 Public Domain)"
                })
                if len(results) >= limit:
                    break
        return results
    except Exception as e:
        print(f"Erreur recherche Poly Haven: {e}")
        return []


def download_polyhaven_model(asset_id, out_dir, resolution="1k"):
    """Télécharge le modèle glTF avec textures PBR depuis Poly Haven."""
    url = f"https://api.polyhaven.com/files/{asset_id}"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            files_data = json.loads(resp.read().decode('utf-8'))
        
        gltf_info = files_data.get("gltf", {}).get(resolution, {}).get("gltf", {})
        download_url = gltf_info.get("url")
        if not download_url:
            for res in ["1k", "2k", "4k"]:
                if res in files_data.get("gltf", {}):
                    download_url = files_data["gltf"][res]["gltf"]["url"]
                    break
        
        if not download_url:
            print(f"Aucun lien glTF trouvé pour {asset_id}")
            return None
        
        os.makedirs(out_dir, exist_ok=True)
        dest_path = os.path.join(out_dir, f"{asset_id}.gltf")
        
        print(f"Téléchargement de {asset_id} depuis {download_url}...")
        dl_req = urllib.request.Request(download_url, headers=HEADERS)
        with urllib.request.urlopen(dl_req, timeout=30) as dl_resp, open(dest_path, "wb") as out_f:
            shutil.copyfileobj(dl_resp, out_f)
        
        print(f"✅ Modèle téléchargé avec succès : {dest_path}")
        return dest_path
    except Exception as e:
        print(f"Erreur téléchargement Poly Haven {asset_id}: {e}")
        return None


KENNEY_KITS = {
    "nature": ("Kit Nature (arbres, rochers, herbe)", "https://kenney.nl/assets/nature-kit"),
    "castle": ("Kit Château (murs, tours, portes)", "https://kenney.nl/assets/castle-kit"),
    "dungeon": ("Kit Donjon (salles, piliers, dalles)", "https://kenney.nl/assets/dungeon-kit"),
    "furniture": ("Kit Mobilier (chaises, tables, lits)", "https://kenney.nl/assets/furniture-kit"),
    "graveyard": ("Kit Cimetière (tombes, cryptes)", "https://kenney.nl/assets/graveyard-kit"),
    "blaster": ("Kit Blaster / Armes Sci-Fi", "https://kenney.nl/assets/blaster-kit"),
    "impact_sounds": ("Audio : Bruitages d'impacts (CC0 WAV)", "https://kenney.nl/assets/impact-sounds"),
    "rpg_audio": ("Audio : Bruitages RPG / sorts / pas", "https://kenney.nl/assets/rpg-audio")
}


def log_attribution(credits_file, asset_name, author, source, license_type):
    """Enregistre automatiquement l'attribution dans CREDITS.md."""
    line = f"- **{asset_name}** | Auteur: {author} | Source: {source} | Licence: {license_type}\n"
    if not os.path.exists(credits_file):
        with open(credits_file, "w", encoding="utf-8") as f:
            f.write("# 📜 Game Asset Credits & Licences\n\nCe projet utilise des assets gratuits certifiés sous licences libres :\n\n")
    
    with open(credits_file, "r+", encoding="utf-8") as f:
        content = f.read()
        if asset_name not in content:
            f.write(line)
            print(f"Attribution enregistrée dans {credits_file}")


def main():
    parser = argparse.ArgumentParser(description="Chasseur d'Assets Gratuits pour Jeux Vidéo")
    parser.add_argument("query", nargs="?", default="", help="Mot-clé de recherche (ex: barrel, rock, sword, chair)")
    parser.add_argument("--download", help="ID de l'asset Poly Haven à télécharger immédiatement")
    parser.add_argument("--out-dir", default="./assets/downloaded", help="Dossier de destination")
    parser.add_argument("--resolution", default="1k", choices=["1k", "2k", "4k"], help="Résolution textures Poly Haven")
    parser.add_argument("--credits", default="./CREDITS.md", help="Fichier d'attribution des crédits")
    parser.add_argument("--list-kenney", action="store_true", help="Afficher les kits incontournables de Kenney.nl")
    args = parser.parse_args()

    if args.list_kenney:
        print("\n=== KITS POPULAIRES GRATUITS DE KENNEY.NL (100% CC0) ===")
        for kit_name, (desc, url) in KENNEY_KITS.items():
            print(f"• [{kit_name.upper()}] {desc} : {url}")
        return

    if args.download:
        path = download_polyhaven_model(args.download, args.out_dir, args.resolution)
        if path:
            log_attribution(args.credits, args.download, "Poly Haven Community", "https://polyhaven.com", "CC0 Public Domain")
            print(f"\n💡 Passe ce modèle dans le sanitizer Blender pour caler le pivot Z=0 et générer la collision :")
            script_path = Path.home() / ".gemini" / "config" / "skills" / "game-ready-3d-assets" / "scripts" / "game_ready_pipeline.py"
            print(f"blender --background --python {script_path.as_posix()} -- --input \"{path}\" --output \"./assets/ready/{args.download}_GameReady.glb\" --name \"{args.download}\"")
        return

    if not args.query:
        print("Veuillez spécifier un mot-clé (ex: python hunt_free_assets.py barrel)")
        return

    print(f"\n🔍 RECHERCHE D'ASSETS GRATUITS POUR : '{args.query}'\n")

    # 1. Poly Haven (API directe 100% CC0)
    print("--- 📦 POLY HAVEN (500+ Modèles PBR CC0 Réalistes - Téléchargeable Immédiatement) ---")
    poly_results = search_polyhaven_models(args.query, limit=5)
    if poly_results:
        for r in poly_results:
            print(f"  • ID: {r['id']} | Nom: {r['name']} | Tags: {', '.join(r['tags'])}")
            print(f"    --> Télécharger : python .gemini/config/skills/game-asset-hunter-curator/scripts/hunt_free_assets.py --download {r['id']}")
    else:
        print("  Aucun résultat direct sur Poly Haven.")

    # 2. Hubs Gratuits Recommandés
    print("\n--- 🌐 HUBS MAJEURS EN LIGNE (Accès Direct) ---")
    q_enc = urllib.parse.quote(args.query)
    print(f"  • Fab.com (Epic Games / Quixel / Unreal) : https://www.fab.com/search?is_free=true&q={q_enc}")
    print(f"  • Kenney.nl Kits (100% CC0)             : https://kenney.nl/assets?q={q_enc}")
    print(f"  • Itch.io Game Assets (Free)             : https://itch.io/game-assets/free/tag-{args.query.lower()}")
    print(f"  • ambientCG (Matériaux PBR CC0)          : https://ambientcg.com/list?q={q_enc}")
    print(f"  • OpenGameArt (Sprites 2D & Audio)       : https://opengameart.org/art-search-advanced?keys={q_enc}")
    print(f"  • Game-Icons.net (4000+ Icônes RPG)      : https://game-icons.net/search.html?q={q_enc}")
    print(f"  • Freesound (SFX CC0)                    : https://freesound.org/search/?q={q_enc}&f=license:%22Creative+Commons+0%22")


if __name__ == "__main__":
    main()
