"""
Game Save State Manager — Persistance Atomique & Pipeline de Migration
Auteur: Brandon (Antigravity Studio Engine)
Règles: Typage strict, zéro Any, écriture atomique et checksums SHA-256.
"""

import hashlib
import json
import os
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Tuple


class SaveCorruptionError(Exception):
    pass


class GameSaveManager:
    def __init__(self, save_dir: str) -> None:
        self.save_dir: str = save_dir
        os.makedirs(save_dir, exist_ok=True)
        self.migrations: Dict[int, Callable[[Dict[str, object]], Dict[str, object]]] = {}

    def register_migration(self, from_version: int, handler: Callable[[Dict[str, object]], Dict[str, object]]) -> None:
        self.migrations[from_version] = handler

    def _compute_hash(self, content: str) -> str:
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    def save_atomic(self, slot_id: str, current_version: int, game_data: Dict[str, object]) -> str:
        target_path = os.path.join(self.save_dir, f"slot_{slot_id}.sav")
        tmp_path = target_path + ".tmp"

        payload_content = json.dumps(game_data, sort_keys=True)
        checksum = self._compute_hash(payload_content)

        full_payload = {
            "schema_version": current_version,
            "checksum": checksum,
            "data": game_data
        }

        # Écriture atomique
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(full_payload, f, indent=2)
            f.flush()
            os.fsync(f.fileno())

        os.replace(tmp_path, target_path)
        return target_path

    def load_and_migrate(self, slot_id: str, target_version: int) -> Dict[str, object]:
        target_path = os.path.join(self.save_dir, f"slot_{slot_id}.sav")
        if not os.path.exists(target_path):
            raise FileNotFoundError(f"Sauvegarde introuvable : {target_path}")

        with open(target_path, "r", encoding="utf-8") as f:
            content = json.load(f)

        stored_checksum = str(content.get("checksum", ""))
        raw_data = content.get("data", {})
        computed_checksum = self._compute_hash(json.dumps(raw_data, sort_keys=True))

        if stored_checksum != computed_checksum:
            raise SaveCorruptionError("Intégrité compromise : le checksum SHA-256 ne correspond pas !")

        current_ver = int(content.get("schema_version", 1))
        migrated_data = dict(raw_data)

        # Pipeline de migration séquentiel
        while current_ver < target_version:
            migration_step = self.migrations.get(current_ver)
            if not migration_step:
                raise ValueError(f"Aucun gestionnaire de migration défini pour passer de v{current_ver} à v{current_ver + 1}")
            migrated_data = migration_step(migrated_data)
            current_ver += 1

        return migrated_data


def run_save_manager_demo() -> None:
    print("=" * 65)
    print("      GAME SAVE STATE MANAGER : PERSISTANCE & MIGRATION SOTA     ")
    print("=" * 65)
    import tempfile
    with tempfile.TemporaryDirectory() as temp_dir:
        manager = GameSaveManager(temp_dir)

        # Enregistrement des migrations
        # v1 -> v2 : Ajout du champ 'stamina' avec valeur par défaut 100.0
        def migrate_v1_to_v2(old_data: Dict[str, object]) -> Dict[str, object]:
            new_data = dict(old_data)
            new_data["stamina"] = 100.0
            return new_data

        # v2 -> v3 : Renommage de 'gold' en 'currency'
        def migrate_v2_to_v3(old_data: Dict[str, object]) -> Dict[str, object]:
            new_data = dict(old_data)
            gold_amount = new_data.pop("gold", 0)
            new_data["currency"] = gold_amount
            return new_data

        manager.register_migration(1, migrate_v1_to_v2)
        manager.register_migration(2, migrate_v2_to_v3)

        # 1. Sauvegarde d'un profil joueur v1
        player_v1 = {
            "player_name": "Brandon",
            "level": 5,
            "gold": 250
        }
        saved_file = manager.save_atomic("01", current_version=1, game_data=player_v1)
        print(f"1. Sauvegarde atomique effectuée : slot_01.sav (v1, {os.path.getsize(saved_file)} octets)")

        # 2. Chargement et migration vers v3
        migrated_v3 = manager.load_and_migrate("01", target_version=3)
        print("2. Chargement & Migration automatique v1 -> v2 -> v3 :")
        print(f"   Données migrées : {migrated_v3}")

        assert "stamina" in migrated_v3 and migrated_v3["stamina"] == 100.0, "Migration v2 échouée"
        assert "currency" in migrated_v3 and migrated_v3["currency"] == 250, "Migration v3 échouée"
        assert "gold" not in migrated_v3, "Nettoyage v3 échoué"

    print("-" * 65)
    print("[OK] Écriture atomique, Checksum SHA-256 et Migrations v1->v3 validés.")
    print("=" * 65)


if __name__ == "__main__":
    run_save_manager_demo()
