# -*- coding: utf-8 -*-
"""
simulate_wow_combat_attack_table.py - World of Warcraft Attack Table Simulator
Simulateur de resolution de table d'attaque a jet unique et de pipeline d'incantation GCD.
"""

from typing import Dict, List, Tuple, TypedDict

class AttackTableStats(TypedDict):
    miss_chance: float
    dodge_chance: float
    parry_chance: float
    glancing_chance: float
    block_chance: float
    crit_chance: float

class AttackResult(TypedDict):
    roll_value: float
    outcome: str  # MISS, DODGE, PARRY, GLANCING, BLOCK, CRIT, HIT
    damage_multiplier: float

class SpellCastState(TypedDict):
    spell_name: str
    base_cast_time: float
    current_cast_progress: float
    pushback_count: int
    is_interrupted: bool

def resolve_attack_table(stats: AttackTableStats, roll: float) -> AttackResult:
    """Resout le resultat d'un coup blanc de melee selon la table d'attaque WoW."""
    cumulative = 0.0

    # 1. Rate (Miss)
    cumulative += stats["miss_chance"]
    if roll < cumulative:
        return {"roll_value": roll, "outcome": "MISS", "damage_multiplier": 0.0}

    # 2. Esquive (Dodge)
    cumulative += stats["dodge_chance"]
    if roll < cumulative:
        return {"roll_value": roll, "outcome": "DODGE", "damage_multiplier": 0.0}

    # 3. Parade (Parry)
    cumulative += stats["parry_chance"]
    if roll < cumulative:
        return {"roll_value": roll, "outcome": "PARRY", "damage_multiplier": 0.0}

    # 4. Eraflure (Glancing blow contre cible plus haut niveau)
    cumulative += stats["glancing_chance"]
    if roll < cumulative:
        return {"roll_value": roll, "outcome": "GLANCING", "damage_multiplier": 0.7}

    # 5. Blocage (Block)
    cumulative += stats["block_chance"]
    if roll < cumulative:
        return {"roll_value": roll, "outcome": "BLOCK", "damage_multiplier": 0.75}

    # 6. Coup Critique (Crit)
    cumulative += stats["crit_chance"]
    if roll < cumulative:
        return {"roll_value": roll, "outcome": "CRIT", "damage_multiplier": 2.0}

    # 7. Coup Normal (Ordinary Hit)
    return {"roll_value": roll, "outcome": "HIT", "damage_multiplier": 1.0}

def apply_spell_pushback(state: SpellCastState, damage_received: float) -> SpellCastState:
    """Applique la regle WoW de recul d'incantation (pushback) limite a 2 fois."""
    if state["is_interrupted"] or state["pushback_count"] >= 2:
        return state

    # Chaque coup retarde l'incantation de 0.5 seconde
    new_progress = max(0.0, state["current_cast_progress"] - 0.5)
    return {
        "spell_name": state["spell_name"],
        "base_cast_time": state["base_cast_time"],
        "current_cast_progress": new_progress,
        "pushback_count": state["pushback_count"] + 1,
        "is_interrupted": False
    }

def run_self_test() -> int:
    """Verifie le determinisme de la table d'attaque et des pushbacks."""
    print("Execution du self-test WoW Attack Table & Spell Pipeline...")

    # Profil type d'un joueur niveau 60 attaquant un Boss de raid niveau 63
    # Miss: [0, 8.0)
    # Dodge: [8.0, 14.5)
    # Parry: [14.5, 28.5)
    # Glancing: [28.5, 68.5)
    # Block: [68.5, 73.5)
    # Crit: [73.5, 83.5)
    # Hit: [83.5, 100.0]
    raid_boss_stats: AttackTableStats = {
        "miss_chance": 8.0,
        "dodge_chance": 6.5,
        "parry_chance": 14.0,
        "glancing_chance": 40.0,
        "block_chance": 5.0,
        "crit_chance": 10.0
    }

    # Test Miss (Roll = 5.0 < 8.0)
    res_miss = resolve_attack_table(raid_boss_stats, 5.0)
    assert res_miss["outcome"] == "MISS", f"Expected MISS, got {res_miss['outcome']}"

    # Test Glancing (Roll = 35.0, entre 28.5 et 68.5)
    res_glance = resolve_attack_table(raid_boss_stats, 35.0)
    assert res_glance["outcome"] == "GLANCING", f"Expected GLANCING, got {res_glance['outcome']}"
    assert res_glance["damage_multiplier"] == 0.7, "Glancing penalty mismatch!"

    # Test Block (Roll = 70.0, entre 68.5 et 73.5)
    res_block = resolve_attack_table(raid_boss_stats, 70.0)
    assert res_block["outcome"] == "BLOCK", f"Expected BLOCK, got {res_block['outcome']}"

    # Test Crit (Roll = 75.0, entre 73.5 et 83.5)
    res_crit = resolve_attack_table(raid_boss_stats, 75.0)
    assert res_crit["outcome"] == "CRIT", f"Expected CRIT, got {res_crit['outcome']}"
    assert res_crit["damage_multiplier"] == 2.0, "Crit multiplier mismatch!"

    # Test Pushback
    cast: SpellCastState = {
        "spell_name": "Boule de Feu",
        "base_cast_time": 3.0,
        "current_cast_progress": 2.0,
        "pushback_count": 0,
        "is_interrupted": False
    }
    cast = apply_spell_pushback(cast, damage_received=150.0)
    assert cast["current_cast_progress"] == 1.5, "Pushback did not delay cast!"
    cast = apply_spell_pushback(cast, damage_received=150.0)
    cast = apply_spell_pushback(cast, damage_received=150.0)  # 3eme coup ignore
    assert cast["pushback_count"] == 2, "Pushback exceeded 2 maximum penalties!"

    print("[PASS] WoW Combat Pipeline teste : Table d'attaque et regles de pushback certifiees.")
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(run_self_test())