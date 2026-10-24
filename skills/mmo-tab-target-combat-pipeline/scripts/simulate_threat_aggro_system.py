# -*- coding: utf-8 -*-
"""
simulate_threat_aggro_system.py - MMORPG Threat & Aggro Simulator
Simulateur de Hate List, de seuils de reprise 110%/130% et de mecanique de Taunt.
"""

from typing import Dict, Optional, Tuple, TypedDict

class PlayerThreatRecord(TypedDict):
    player_id: str
    threat_value: float
    distance_meters: float

class ThreatManager:
    """Gestionnaire de table de menace d'une creature MMORPG."""
    def __init__(self, spawn_pos: Tuple[float, float] = (0.0, 0.0), leash_radius: float = 40.0):
        self.spawn_pos: Tuple[float, float] = spawn_pos
        self.leash_radius: float = leash_radius
        self.hate_list: Dict[str, float] = {}
        self.current_target_id: Optional[str] = None
        self.is_evading: bool = False

    def add_threat(self, player_id: str, amount: float) -> None:
        """Ajoute de la menace a un joueur dans la Hate List."""
        if self.is_evading:
            return
        self.hate_list[player_id] = self.hate_list.get(player_id, 0.0) + amount
        if self.current_target_id is None:
            self.current_target_id = player_id

    def check_aggro_switch(self, player_distances: Dict[str, float]) -> Optional[str]:
        """Evalue si un joueur a franchi le seuil de reprise d'aggro (110% ou 130%)."""
        if not self.current_target_id or self.current_target_id not in self.hate_list:
            return None

        current_threat = self.hate_list[self.current_target_id]

        for p_id, threat in self.hate_list.items():
            if p_id == self.current_target_id:
                continue

            dist = player_distances.get(p_id, 10.0)
            # 110% en melee (<= 5m), 130% a distance (> 5m)
            threshold = (current_threat * 1.10) if dist <= 5.0 else (current_threat * 1.30)

            if threat > threshold:
                self.current_target_id = p_id
                return p_id

        return self.current_target_id

    def apply_taunt(self, tank_id: str) -> None:
        """Applique la provocation : le tank prend l'aggro et egale la plus haute menace."""
        if not self.hate_list:
            return
        highest_threat = max(self.hate_list.values())
        self.hate_list[tank_id] = highest_threat
        self.current_target_id = tank_id

    def check_leash(self, current_pos: Tuple[float, float]) -> bool:
        """Verifie si la creature doit passer en mode Evade (reinitialisation)."""
        dx = current_pos[0] - self.spawn_pos[0]
        dy = current_pos[1] - self.spawn_pos[1]
        dist_from_spawn = (dx * dx + dy * dy) ** 0.5

        if dist_from_spawn > self.leash_radius:
            self.is_evading = True
            self.hate_list.clear()
            self.current_target_id = None
            return True
        return False

def run_self_test() -> int:
    """Verifie les regles fondamentales de l'aggro WoW."""
    print("Execution du self-test Threat & Aggro System...")
    tm = ThreatManager(spawn_pos=(0.0, 0.0), leash_radius=45.0)

    # 1. Le Tank ouvre le combat
    tm.add_threat("Tank_Guerrier", 1000.0)
    assert tm.current_target_id == "Tank_Guerrier"

    # 2. Le DPS Mage inflige des degats a distance (dist = 30m)
    # A 1200 de menace, le Mage depasse le Tank, mais le seuil a distance est de 130% (1300)
    tm.add_threat("Mage_DPS", 1200.0)
    distances = {"Tank_Guerrier": 2.0, "Mage_DPS": 30.0}
    tm.check_aggro_switch(distances)
    assert tm.current_target_id == "Tank_Guerrier", "Aggro switched prematurely before 130% ranged threshold!"

    # 3. Le Mage passe a 1350 (> 1300) -> Reprise d'aggro !
    tm.add_threat("Mage_DPS", 150.0)
    tm.check_aggro_switch(distances)
    assert tm.current_target_id == "Mage_DPS", "Aggro failed to switch to Mage after crossing 130% threshold!"

    # 4. Le Tank utilise Taunt
    tm.apply_taunt("Tank_Guerrier")
    assert tm.current_target_id == "Tank_Guerrier", "Taunt failed to reclaim aggro!"
    assert tm.hate_list["Tank_Guerrier"] == 1350.0, "Taunt failed to match highest threat value!"

    # 5. Le monstre est attire trop loin du spawn -> Evade
    assert tm.check_leash((50.0, 0.0)), "Leash mechanism failed to trigger beyond radius!"
    assert tm.is_evading and tm.current_target_id is None, "Evade state failed to clear hate list!"

    print("[PASS] Threat & Aggro teste : Seuil 130% distance, Taunt et Laisse valides avec succes.")
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(run_self_test())