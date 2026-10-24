---
name: game-save-state-manager
description: Implement robust game save systems and state persistence. Enforces atomic disk writes, corruption detection (checksums/HMAC), backward-compatible schema migrations, and slot management.
---

# Game Save State Manager — Persistance Atomique, Détection de Corruption & Migrations

Ce skill formalise l'architecture de sauvegarde et de persistance d'états de jeu conçue pour éliminer tout risque de corruption de fichiers (panne de courant, crash, mise à jour de version du jeu) et explicite la frontière entre intégrité physique et authentification cryptographique.

---

## 🔒 1. Les 4 Règles d'Or de la Persistance Industrielle

1. **Écriture Atomique (`Atomic Write`)** :
   - Ne JAMAIS écraser directement le fichier `save.dat`.
   - Écrire dans un fichier temporaire `save.dat.tmp`.
   - Forcer le vidage physique sur le disque (`flush()` + `os.fsync()`).
   - Remplacer atomiquement le fichier via `os.replace()` (opération atomique garantie par le système de fichiers de l'OS).
2. **Détection de Corruption vs Authentification Cryptographique** :
   - **Détection de corruption accidentelle (Bit rot / troncature)** : Calcul d'un checksum SHA-256 ou CRC32 stocké dans l'en-tête du fichier. Si une discordance est détectée, le fichier a été tronqué lors d'un crash : basculer immédiatement sur la copie de secours `save.dat.bak`.
   - **Protection contre la falsification (Anti-Tampering)** : Un simple hash SHA-256 ne garantit pas l'inviolabilité, car un attaquant local peut modifier la sauvegarde et recalculer le hash. Pour authentifier la sauvegarde contre la falsification locale, utiliser un **HMAC-SHA256 avec clé protégée** ou une signature asymétrique **Ed25519** (recommandations OWASP Cryptography). Pour un jeu multijoueur, la persistance des inventaires et personnages doit rester strictement autoritaire sur le serveur.
3. **Pipeline de Migration de Schémas (Schema Migration)** :
   - Chaque fichier de sauvegarde possède un numéro de schéma (`schema_version: 1`).
   - Lorsque le jeu est mis à jour (`schema_version: 3`), un pipeline de migration séquentiel ($1 \to 2 \to 3$) transforme les données sans supprimer la progression du joueur.
4. **Gestion Multi-Slots Découplée** :
   - Fichiers d'index séparés stockant les métadonnées légères (nom du joueur, temps de jeu, niveau, date, vignette d'aperçu). Permet d'afficher l'écran de sélection de sauvegarde instantanément sans charger les mondes volumineux.

---

## 🗂️ 2. Structure du Payload de Sauvegarde

```json
{
  "header": {
    "magic": "GAMESAVE",
    "schema_version": 2,
    "timestamp": 1776600000,
    "playtime_seconds": 3600,
    "checksum_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "hmac_signature": "optional_hmac_or_ed25519_for_anti_tampering"
  },
  "player": {
    "id": "hero_01",
    "level": 12,
    "position": [120.5, 45.0, 10.2],
    "health": 100,
    "inventory": [
      {"item_id": "sword_iron", "quantity": 1},
      {"item_id": "potion_health", "quantity": 5}
    ]
  },
  "world_state": {
    "current_quest": "quest_goblin_camp",
    "defeated_bosses": ["boss_troll"],
    "unlocked_waypoints": ["town_square", "forest_entry"]
  }
}
```

---

## ⚙️ 3. Pipeline de Migration Déterministe

```python
from typing import Dict, Any, Callable

MigrationFn = Callable[[Dict[str, Any]], Dict[str, Any]]

class SaveMigrator:
    def __init__(self) -> None:
        self.migrations: Dict[int, MigrationFn] = {
            1: self._migrate_v1_to_v2,
            2: self._migrate_v2_to_v3,
        }
        self.target_version: int = 3

    def migrate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        current_v = data["header"]["schema_version"]
        while current_v < self.target_version:
            if current_v not in self.migrations:
                raise ValueError(f"Migration manquante pour la version {current_v}")
            data = self.migrations[current_v](data)
            current_v += 1
            data["header"]["schema_version"] = current_v
        return data

    def _migrate_v1_to_v2(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Exemple: ajout du champ playtime_seconds inexistant en v1
        data["header"]["playtime_seconds"] = data["header"].get("playtime_seconds", 0)
        return data

    def _migrate_v2_to_v3(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Exemple: restructuration de l'inventaire en dictionnaire indexé
        return data
```
