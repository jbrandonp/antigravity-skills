"""MMO SpellMod & Glyph Pipeline Benchmark.

Validates World of Warcraft 3.3.5a dynamic spell alteration mechanics:
- 6-slot glyph system (3 Major, 3 Minor) with level unlock gates
- In-combat glyph swap rejection
- SpellMod interceptor pipeline evaluating FLAT and PCT modifiers (cast time, cost, damage, cooldown, chain jumps)
- Death Knight Runeforging station checks and overwrite semantics
- Temporary weapon enhancements mutual exclusivity rule
"""

from __future__ import annotations

import math
import sys
from dataclasses import dataclass, field
from enum import Enum, auto

sys.stdout.reconfigure(encoding="utf-8")


class GlyphType(Enum):
    """Glyph classification."""
    MAJOR = auto()
    MINOR = auto()


class SpellModOp(Enum):
    """Target spell properties altered by the SpellMod engine."""
    DAMAGE = auto()
    DURATION = auto()
    THREAT = auto()
    EFFECT1 = auto()
    CHARGES = auto()
    RANGE = auto()
    RADIUS = auto()
    CRITICAL_CHANCE = auto()
    CASTING_TIME = auto()
    COOLDOWN = auto()
    COST = auto()
    CRIT_DAMAGE_BONUS = auto()
    JUMP_TARGETS = auto()


class SpellModType(Enum):
    """Modifier arithmetic application method."""
    FLAT = auto()  # Additive value
    PCT = auto()   # Multiplicative percentage


@dataclass(frozen=True, slots=True)
class SpellModifier:
    """Active modifier node applied to spells matching family or spell_id."""
    op: SpellModOp
    mod_type: SpellModType
    value: float
    spell_id: int
    source_description: str


@dataclass(slots=True)
class GlyphSlot:
    """Individual socket in character's inscription grimoire."""
    slot_id: int
    slot_type: GlyphType
    required_level: int
    current_glyph_id: int | None = None
    active_modifiers: list[SpellModifier] = field(default_factory=list)


@dataclass(slots=True)
class BaseSpellTemplate:
    """Canonical spell template definition from Spell.dbc."""
    spell_id: int
    name: str
    cast_time_ms: int
    cooldown_ms: int
    mana_cost: int
    base_damage_min: float
    base_damage_max: float
    chain_jump_targets: int = 1


@dataclass(slots=True)
class TemporaryWeaponEnchantment:
    """Temporary enhancement applied to weapon (poison, sharpening stone, windfury)."""
    enchant_id: int
    name: str
    duration_seconds: float


class SpellModGlyphPipelineEngine:
    """Authoritative SpellMod evaluation and glyph inscription manager."""

    def __init__(self) -> None:
        self.active_modifiers: list[SpellModifier] = []
        self.glyph_slots: list[GlyphSlot] = [
            # 3 Major Glyphs
            GlyphSlot(0, GlyphType.MAJOR, 15),
            GlyphSlot(1, GlyphType.MAJOR, 30),
            GlyphSlot(2, GlyphType.MAJOR, 80),
            # 3 Minor Glyphs
            GlyphSlot(3, GlyphType.MINOR, 15),
            GlyphSlot(4, GlyphType.MINOR, 50),
            GlyphSlot(5, GlyphType.MINOR, 70),
        ]
        self.equipped_runeforge: str | None = None
        self.main_hand_temp_enchant: TemporaryWeaponEnchantment | None = None

    def inscribe_glyph(
        self,
        slot_index: int,
        glyph_id: int,
        glyph_type: GlyphType,
        player_level: int,
        is_in_combat: bool,
        granted_modifiers: list[SpellModifier],
    ) -> tuple[bool, str]:
        """Inscribes a glyph into a designated slot, respecting level and combat rules."""
        if is_in_combat:
            return False, "CANNOT_CHANGE_GLYPHS_IN_COMBAT"

        if not (0 <= slot_index < len(self.glyph_slots)):
            return False, "INVALID_SLOT_INDEX"

        slot = self.glyph_slots[slot_index]

        if slot.slot_type != glyph_type:
            return False, "GLYPH_TYPE_MISMATCH"

        if player_level < slot.required_level:
            return False, "LEVEL_REQUIREMENT_NOT_MET"

        # Remove previous modifiers from this slot if replacing
        if slot.current_glyph_id is not None:
            for mod in slot.active_modifiers:
                if mod in self.active_modifiers:
                    self.active_modifiers.remove(mod)
            slot.active_modifiers.clear()

        # Inscribe new glyph
        slot.current_glyph_id = glyph_id
        slot.active_modifiers.extend(granted_modifiers)
        self.active_modifiers.extend(granted_modifiers)

        return True, "GLYPH_INSCRIBED_SUCCESSFULLY"

    def apply_spell_mods(
        self, template: BaseSpellTemplate
    ) -> dict[str, float | int]:
        """Passes a base spell through active SpellModifiers to calculate dynamic properties."""
        # 1. Cast Time (ms)
        flat_cast = sum(
            m.value for m in self.active_modifiers
            if m.spell_id == template.spell_id and m.op == SpellModOp.CASTING_TIME and m.mod_type == SpellModType.FLAT
        )
        pct_cast = sum(
            m.value for m in self.active_modifiers
            if m.spell_id == template.spell_id and m.op == SpellModOp.CASTING_TIME and m.mod_type == SpellModType.PCT
        )
        final_cast_ms = max(0, int((template.cast_time_ms + flat_cast) * (1.0 + pct_cast / 100.0)))

        # 2. Cooldown (ms)
        flat_cd = sum(
            m.value for m in self.active_modifiers
            if m.spell_id == template.spell_id and m.op == SpellModOp.COOLDOWN and m.mod_type == SpellModType.FLAT
        )
        final_cd_ms = max(0, int(template.cooldown_ms + flat_cd))

        # 3. Resource Cost
        flat_cost = sum(
            m.value for m in self.active_modifiers
            if m.spell_id == template.spell_id and m.op == SpellModOp.COST and m.mod_type == SpellModType.FLAT
        )
        pct_cost = sum(
            m.value for m in self.active_modifiers
            if m.spell_id == template.spell_id and m.op == SpellModOp.COST and m.mod_type == SpellModType.PCT
        )
        final_cost = max(0, int((template.mana_cost + flat_cost) * (1.0 + pct_cost / 100.0)))

        # 4. Damage
        flat_dmg = sum(
            m.value for m in self.active_modifiers
            if m.spell_id == template.spell_id and m.op == SpellModOp.DAMAGE and m.mod_type == SpellModType.FLAT
        )
        pct_dmg = sum(
            m.value for m in self.active_modifiers
            if m.spell_id == template.spell_id and m.op == SpellModOp.DAMAGE and m.mod_type == SpellModType.PCT
        )
        final_dmg_min = (template.base_damage_min + flat_dmg) * (1.0 + pct_dmg / 100.0)
        final_dmg_max = (template.base_damage_max + flat_dmg) * (1.0 + pct_dmg / 100.0)

        # 5. Chain Jump Targets
        flat_jumps = sum(
            int(m.value) for m in self.active_modifiers
            if m.spell_id == template.spell_id and m.op == SpellModOp.JUMP_TARGETS and m.mod_type == SpellModType.FLAT
        )
        final_jumps = template.chain_jump_targets + flat_jumps

        return {
            "cast_time_ms": final_cast_ms,
            "cooldown_ms": final_cd_ms,
            "resource_cost": final_cost,
            "damage_min": final_dmg_min,
            "damage_max": final_dmg_max,
            "chain_jump_targets": final_jumps,
        }

    def apply_death_knight_runeforge(
        self, runeforge_name: str, near_runeforge_anvil: bool
    ) -> tuple[bool, str]:
        """Applies a death knight runeforge enchantment to main hand weapon."""
        if not near_runeforge_anvil:
            return False, "REQUIRES_NEAR_RUNEFORGE_ANVIL"

        self.equipped_runeforge = runeforge_name
        return True, "RUNEFORGE_APPLIED"

    def apply_temporary_weapon_enchantment(
        self, enchantment: TemporaryWeaponEnchantment
    ) -> str:
        """Applies temporary enhancement, strictly overwriting any previous temporary enhancement."""
        prev = self.main_hand_temp_enchant.name if self.main_hand_temp_enchant else None
        self.main_hand_temp_enchant = enchantment
        return f"REPLACED_{prev}" if prev else "APPLIED_FRESH"


def run_benchmark() -> None:
    """Executes deterministic test scenarios for the SpellMod and glyph pipeline."""
    print("=== STARTING MMO SPELLMOD & GLYPH PIPELINE BENCHMARK ===")
    engine = SpellModGlyphPipelineEngine()

    # 1. Test In-Combat Inscription Lockdown
    res_combat, err = engine.inscribe_glyph(0, 101, GlyphType.MAJOR, 80, is_in_combat=True, granted_modifiers=[])
    assert res_combat is False
    assert err == "CANNOT_CHANGE_GLYPHS_IN_COMBAT"
    print("[PASS] In-combat glyph swap lockdown verified")

    # 2. Test Level Requirements for Slots
    # Slot 2 (Major) requires Level 80
    res_lvl, err_lvl = engine.inscribe_glyph(2, 102, GlyphType.MAJOR, player_level=75, is_in_combat=False, granted_modifiers=[])
    assert res_lvl is False
    assert err_lvl == "LEVEL_REQUIREMENT_NOT_MET"

    res_ok, err_ok = engine.inscribe_glyph(2, 102, GlyphType.MAJOR, player_level=80, is_in_combat=False, granted_modifiers=[])
    assert res_ok is True
    assert err_ok == "GLYPH_INSCRIBED_SUCCESSFULLY"
    print("[PASS] Level unlock gates on Major/Minor glyph slots verified")

    # 3. Test SpellMod Pipeline: Fireball Modifiers
    # Base Fireball: 3500ms cast, 0ms cd, 300 mana, 700.0 - 900.0 dmg
    fireball_base = BaseSpellTemplate(
        spell_id=133,
        name="Fireball",
        cast_time_ms=3500,
        cooldown_ms=0,
        mana_cost=300,
        base_damage_min=700.0,
        base_damage_max=900.0,
    )

    # Inscribe "Glyph of Fireball": reduces cast time by 150ms flat
    glyph_fireball_mods = [
        SpellModifier(SpellModOp.CASTING_TIME, SpellModType.FLAT, -150.0, 133, "Glyph of Fireball"),
    ]
    engine.inscribe_glyph(0, 201, GlyphType.MAJOR, 80, False, glyph_fireball_mods)

    # Add Talent Modifiers: -10% mana cost, +50 flat damage, +15% damage
    talent_mods = [
        SpellModifier(SpellModOp.COST, SpellModType.PCT, -10.0, 133, "Talent: Pyromaniac"),
        SpellModifier(SpellModOp.DAMAGE, SpellModType.FLAT, 50.0, 133, "Talent: Spell Power Flat"),
        SpellModifier(SpellModOp.DAMAGE, SpellModType.PCT, 15.0, 133, "Talent: Fire Power %"),
    ]
    engine.active_modifiers.extend(talent_mods)

    evaluated = engine.apply_spell_mods(fireball_base)

    # Cast Time: 3500 - 150 = 3350 ms
    assert evaluated["cast_time_ms"] == 3350
    # Mana Cost: 300 * (1 - 0.10) = 270
    assert evaluated["resource_cost"] == 270
    # Damage Min: (700 + 50) * 1.15 = 750 * 1.15 = 862.5
    assert math.isclose(float(evaluated["damage_min"]), 862.5, rel_tol=1e-5)
    # Damage Max: (900 + 50) * 1.15 = 950 * 1.15 = 1092.5
    assert math.isclose(float(evaluated["damage_max"]), 1092.5, rel_tol=1e-5)
    print("[PASS] SpellMod pipeline FLAT and PCT multi-stage evaluation verified")

    # 4. Test Chain Lightning Jump Target Increment
    chain_lightning_base = BaseSpellTemplate(
        spell_id=421,
        name="Chain Lightning",
        cast_time_ms=2000,
        cooldown_ms=6000,
        mana_cost=500,
        base_damage_min=900.0,
        base_damage_max=1100.0,
        chain_jump_targets=3,
    )
    # Glyph of Chain Lightning: +1 jump target
    glyph_chain_mods = [
        SpellModifier(SpellModOp.JUMP_TARGETS, SpellModType.FLAT, 1.0, 421, "Glyph of Chain Lightning"),
    ]
    engine.inscribe_glyph(1, 202, GlyphType.MAJOR, 80, False, glyph_chain_mods)

    cl_eval = engine.apply_spell_mods(chain_lightning_base)
    assert cl_eval["chain_jump_targets"] == 4, "Chain lightning should jump to 4 targets with glyph"
    print("[PASS] Chain Lightning target jump increment mod verified")

    # 5. Test Death Knight Runeforging Anvil Requirement & Overwriting
    res_rf_fail, err_rf = engine.apply_death_knight_runeforge("Rune of the Fallen Crusader", near_runeforge_anvil=False)
    assert res_rf_fail is False
    assert err_rf == "REQUIRES_NEAR_RUNEFORGE_ANVIL"

    res_rf_ok, _ = engine.apply_death_knight_runeforge("Rune of the Fallen Crusader", near_runeforge_anvil=True)
    assert res_rf_ok is True
    assert engine.equipped_runeforge == "Rune of the Fallen Crusader"

    # Overwrite with Razorice
    engine.apply_death_knight_runeforge("Rune of Razorice", near_runeforge_anvil=True)
    assert engine.equipped_runeforge == "Rune of Razorice"
    print("[PASS] Death Knight Runeforging anvil check & atomic overwrite verified")

    # 6. Test Temporary Weapon Enhancement Exclusivity Rule
    poison = TemporaryWeaponEnchantment(1, "Deadly Poison IX", 3600.0)
    res_p = engine.apply_temporary_weapon_enchantment(poison)
    assert res_p == "APPLIED_FRESH"

    stone = TemporaryWeaponEnchantment(2, "Dense Sharpening Stone", 3600.0)
    res_s = engine.apply_temporary_weapon_enchantment(stone)
    assert res_s == "REPLACED_Deadly Poison IX"
    assert engine.main_hand_temp_enchant.name == "Dense Sharpening Stone"
    print("[PASS] Temporary weapon enhancement single-buff exclusivity rule verified")

    print("\nALL SPELLMOD & GLYPH PIPELINE BENCHMARKS PASSED SUCCESSFULLY (100%)!")


if __name__ == "__main__":
    run_benchmark()
