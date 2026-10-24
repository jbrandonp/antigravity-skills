"""
MMO Spell & Aura Virtual Machine — Simulateur Canonique World of Warcraft
Auteur: Brandon (WoW Clone Architecture Suite)
Règles: Typage strict, zéro Any, calculs probabilistes et gestion de durées déterministes.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple


class SpellSchool(Enum):
    """Écoles de magie fondamentales de World of Warcraft."""
    PHYSICAL = 0
    HOLY = 1
    FIRE = 2
    NATURE = 3
    FROST = 4
    SHADOW = 5
    ARCANE = 6


class DRCategory(Enum):
    """Catégories de rendements dégressifs (Diminishing Returns) en PvP."""
    STUN = "stun"
    INCAPACITATE = "incapacitate"
    FEAR = "fear"
    ROOT = "root"
    SILENCE = "silence"


@dataclass
class SpellHitResult:
    """Résultat de la résolution à deux jets du sort magique."""
    is_hit: bool
    is_crit: bool
    final_damage: float
    message: str


@dataclass
class AuraInstance:
    """Instance active d'une aura (Buff, HoT, Debuff ou DoT)."""
    spell_id: int
    name: str
    base_duration: float
    current_duration: float
    tick_interval: float
    tick_timer: float
    tick_count: int = 0

    def refresh_pandemic(self) -> None:
        """
        Applique la règle canonique Pandemic de WoW.
        Si rafraîchi dans les derniers 30%, la durée résiduelle est ajoutée
        jusqu'à un plafond maximal de 130% de la durée de base.
        """
        pandemic_window: float = self.base_duration * 0.30
        max_duration: float = self.base_duration * 1.30
        if self.current_duration <= pandemic_window:
            self.current_duration = min(max_duration, self.base_duration + self.current_duration)
        else:
            self.current_duration = self.base_duration


class SpellAuraVM:
    """Machine virtuelle de gestion des sorts, procs rPPM et contrôle de foule PvP."""

    def __init__(self) -> None:
        # Table de DR par joueur : player_id -> (categorie -> (palier, timestamp_fin_effet))
        self.dr_table: Dict[str, Dict[DRCategory, Tuple[int, float]]] = {}

    @staticmethod
    def resolve_two_roll_spell(
        base_damage: float,
        hit_chance: float,
        crit_chance: float,
        hit_roll: float,
        crit_roll: float
    ) -> SpellHitResult:
        """
        Résolution à deux jets indépendants :
        Jet 1 : Vérifie si le sort touche la cible.
        Jet 2 : Si touché, vérifie indépendamment si le sort est critique.
        """
        # Jet 1 : Hit Check
        if hit_roll > hit_chance:
            return SpellHitResult(is_hit=False, is_crit=False, final_damage=0.0, message="RÉSISTÉ (Miss)")

        # Jet 2 : Crit Check
        if crit_roll <= crit_chance:
            crit_damage: float = base_damage * 1.5  # Modificateur critique standard des sorts
            return SpellHitResult(is_hit=True, is_crit=True, final_damage=crit_damage, message="COUP CRITIQUE (150%)")

        return SpellHitResult(is_hit=True, is_crit=False, final_damage=base_damage, message="COUP NORMAL (100%)")

    @staticmethod
    def calculate_rppm_chance(
        rppm_value: float,
        time_since_last_hit: float,
        icd: float
    ) -> float:
        """
        Calcule la probabilité de déclenchement selon le modèle Real PPM (rPPM) de WoW.
        Inclut le multiplicateur BadLuckProtection si le temps d'attente dépasse l'ICD.
        """
        base_chance: float = (time_since_last_hit * rppm_value) / 60.0
        bad_luck_factor: float = 1.0
        if icd > 0.0 and time_since_last_hit > icd:
            bad_luck_factor = max(1.0, 1.0 + 3.0 * ((time_since_last_hit - icd) / icd))
        return min(1.0, base_chance * bad_luck_factor)

    def apply_pvp_crowd_control(
        self,
        target_id: str,
        category: DRCategory,
        nominal_duration: float,
        current_server_time: float
    ) -> Tuple[float, str]:
        """
        Applique un contrôle de foule avec Diminishing Returns (100% -> 50% -> 25% -> 0%).
        La fenêtre de 18 secondes démarre APRÈS expiration du contrôle.
        """
        if target_id not in self.dr_table:
            self.dr_table[target_id] = {}

        dr_info = self.dr_table[target_id].get(category)
        stage = 0
        if dr_info is not None:
            prev_stage, end_timestamp = dr_info
            # Si 18 secondes se sont écoulées depuis la fin du dernier CC, réinitialisation
            if current_server_time >= end_timestamp + 18.0:
                stage = 0
            else:
                stage = prev_stage + 1

        multipliers: List[float] = [1.0, 0.5, 0.25, 0.0]
        mult: float = multipliers[min(stage, 3)]
        effective_duration: float = nominal_duration * mult

        # Mise à jour du timestamp d'expiration
        self.dr_table[target_id][category] = (min(stage, 3), current_server_time + effective_duration)

        verdict = f"Palier DR {stage+1} : Multiplicateur {mult*100:.0f}% (Durée {effective_duration:.1f}s)"
        if mult == 0.0:
            verdict = "IMMUNISÉ (DR Maximum Atteint)"
        return effective_duration, verdict


def run_spell_aura_benchmark() -> None:
    """Exécute les tests de conformité du moteur de sorts et d'auras WoW."""
    print("=" * 80)
    print("   MMO SPELL & AURA VIRTUAL MACHINE (WOW CANONICAL COMBAT) — VALIDATION")
    print("=" * 80)

    vm = SpellAuraVM()

    # 1. Validation de la Table d'Attaque à Deux Jets (Two-Roll System)
    print("1. Table d'Attaque Magique à Deux Jets :")
    base_dmg = 1000.0
    hit_pct = 0.96   # 96% de chance de toucher
    crit_pct = 0.30  # 30% de chance de critique

    # Cas A : Échec au jet 1 (Miss)
    res_miss = vm.resolve_two_roll_spell(base_dmg, hit_pct, crit_pct, hit_roll=0.98, crit_roll=0.10)
    print(f"  Jet 1 Raté (Hit Roll 0.98 > 0.96)     : {res_miss.message} -> {res_miss.final_damage} dégâts")
    assert not res_miss.is_hit and res_miss.final_damage == 0.0

    # Cas B : Succès jet 1 et succès jet 2 (Critique)
    res_crit = vm.resolve_two_roll_spell(base_dmg, hit_pct, crit_pct, hit_roll=0.50, crit_roll=0.20)
    print(f"  Jet 1 Touché + Jet 2 Crit (0.20 <= 0.30): {res_crit.message} -> {res_crit.final_damage} dégâts")
    assert res_crit.is_hit and res_crit.is_crit and res_crit.final_damage == 1500.0

    # 2. Validation de la Règle Pandemic (30% Rollover)
    print("-" * 80)
    print("2. Règle Canonique Pandemic (DoT Rollover sans Clipping) :")
    dot = AuraInstance(
        spell_id=589,
        name="Mot de l'ombre : Douleur",
        base_duration=18.0,
        current_duration=4.0,  # 4.0s restantes (<= 18 * 0.30 = 5.4s -> dans la fenêtre Pandemic)
        tick_interval=3.0,
        tick_timer=1.0
    )
    print(f"  Avant Rafraîchissement : Durée Résiduelle = {dot.current_duration:.1f}s / {dot.base_duration:.1f}s")
    dot.refresh_pandemic()
    print(f"  Après Rafraîchissement  : Nouvelle Durée    = {dot.current_duration:.1f}s (Plafond 130% = {18.0*1.3:.1f}s)")
    assert dot.current_duration == 22.0, "La durée doit être étendue à 18.0 + 4.0 = 22.0s"

    # 3. Validation rPPM (Real PPM avec Bad Luck Protection)
    print("-" * 80)
    print("3. Probabilités rPPM avec Protection contre la Malchance :")
    chance_normal = vm.calculate_rppm_chance(rppm_value=2.0, time_since_last_hit=2.0, icd=20.0)
    chance_starved = vm.calculate_rppm_chance(rppm_value=2.0, time_since_last_hit=45.0, icd=20.0)
    print(f"  Délai 2s (inférieur à l'ICD de 20s)   : Chance rPPM = {chance_normal*100:.1f}%")
    print(f"  Délai 45s (famine post-ICD)            : Chance rPPM = {chance_starved*100:.1f}% (Boost Malchance)")
    assert chance_starved >= chance_normal * 4.0, "La protection contre la malchance doit fortement booster la probabilité"

    # 4. Validation Diminishing Returns PvP (Fenêtre 18 secondes)
    print("-" * 80)
    print("4. Diminishing Returns PvP (Stun 6.0s Nominal) :")
    player = "Rogue_Player_01"
    now = 100.0

    dur1, v1 = vm.apply_pvp_crowd_control(player, DRCategory.STUN, 6.0, now)
    print(f"  Stun 1 (t={now:.1f}s)                : {v1}")
    assert dur1 == 6.0

    # Stun 2 appliqué 8 secondes plus tard (pendant le combat)
    now += 8.0
    dur2, v2 = vm.apply_pvp_crowd_control(player, DRCategory.STUN, 6.0, now)
    print(f"  Stun 2 (t={now:.1f}s)                : {v2}")
    assert dur2 == 3.0  # 50%

    # Stun 3 appliqué 5 secondes plus tard
    now += 5.0
    dur3, v3 = vm.apply_pvp_crowd_control(player, DRCategory.STUN, 6.0, now)
    print(f"  Stun 3 (t={now:.1f}s)                : {v3}")
    assert dur3 == 1.5  # 25%

    # Stun 4 immédiat -> Immunité
    now += 2.0
    dur4, v4 = vm.apply_pvp_crowd_control(player, DRCategory.STUN, 6.0, now)
    print(f"  Stun 4 (t={now:.1f}s)                : {v4}")
    assert dur4 == 0.0

    # Attente de 19 secondes post-expiration -> Reset complet du DR
    now += 19.0
    dur_reset, v_reset = vm.apply_pvp_crowd_control(player, DRCategory.STUN, 6.0, now)
    print(f"  Stun après 19s (t={now:.1f}s)         : {v_reset}")
    assert dur_reset == 6.0, "Le DR doit être totalement réinitialisé après 18s de répit"

    print("=" * 80)
    print("[SUCCÈS] Moteur Spell & Aura VM (Two-roll, Pandemic 30%, rPPM, DR 18s) certifié.")
    print("=" * 80)


if __name__ == "__main__":
    run_spell_aura_benchmark()
