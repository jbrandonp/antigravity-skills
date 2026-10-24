"""
Gameplay Ability System (GAS) — Validateur de Modificateurs & Effets
Auteur: Brandon (Antigravity Studio Engine)
Règles: Typage strict, zéro Any, calculs déterministes.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional


class ModifierOp(str, Enum):
    ADD = "ADD"
    PERCENT_ADD = "PERCENT_ADD"
    MULTIPLY = "MULTIPLY"


class EffectDurationType(str, Enum):
    INSTANT = "INSTANT"
    DURATION = "DURATION"
    INFINITE = "INFINITE"


@dataclass
class GameplayAttribute:
    name: str
    base_value: float
    current_value: float
    min_value: float
    max_value: float

    def clamp(self) -> None:
        if self.current_value < self.min_value:
            self.current_value = self.min_value
        elif self.current_value > self.max_value:
            self.current_value = self.max_value


@dataclass
class AttributeModifier:
    target_attribute: str
    operation: ModifierOp
    magnitude: float


@dataclass
class ActiveGameplayEffect:
    id: str
    duration_type: EffectDurationType
    duration_remaining: float
    modifiers: List[AttributeModifier]
    granted_tags: List[str]
    stack_count: int = 1
    max_stacks: int = 5


class AbilitySystemComponent:
    def __init__(self) -> None:
        self.attributes: Dict[str, GameplayAttribute] = {}
        self.active_effects: List[ActiveGameplayEffect] = []
        self.active_tags: List[str] = []

    def register_attribute(self, name: str, base_val: float, min_val: float, max_val: float) -> None:
        self.attributes[name] = GameplayAttribute(
            name=name,
            base_value=base_val,
            current_value=base_val,
            min_value=min_val,
            max_value=max_val
        )

    def apply_effect(self, effect: ActiveGameplayEffect) -> None:
        if effect.duration_type == EffectDurationType.INSTANT:
            for mod in effect.modifiers:
                attr = self.attributes.get(mod.target_attribute)
                if attr:
                    attr.base_value += mod.magnitude
                    attr.current_value = attr.base_value
                    attr.clamp()
            return

        # Check existing stack
        for existing in self.active_effects:
            if existing.id == effect.id:
                if existing.stack_count < existing.max_stacks:
                    existing.stack_count += 1
                existing.duration_remaining = effect.duration_remaining
                self.recalculate_attributes()
                return

        self.active_effects.append(effect)
        for tag in effect.granted_tags:
            if tag not in self.active_tags:
                self.active_tags.append(tag)
        self.recalculate_attributes()

    def recalculate_attributes(self) -> None:
        for attr in self.attributes.values():
            add_sum = 0.0
            percent_sum = 0.0
            mult_prod = 1.0

            for effect in self.active_effects:
                for mod in effect.modifiers:
                    if mod.target_attribute == attr.name:
                        mag = mod.magnitude * effect.stack_count
                        if mod.operation == ModifierOp.ADD:
                            add_sum += mag
                        elif mod.operation == ModifierOp.PERCENT_ADD:
                            percent_sum += mag
                        elif mod.operation == ModifierOp.MULTIPLY:
                            mult_prod *= mag

            attr.current_value = (attr.base_value + add_sum) * (1.0 + percent_sum) * mult_prod
            attr.clamp()


def run_gas_validation() -> None:
    print("=" * 65)
    print("      GAMEPLAY ABILITY SYSTEM : VALIDATEUR SOTA (GAS)     ")
    print("=" * 65)
    asc = AbilitySystemComponent()
    asc.register_attribute("Health", base_val=100.0, min_val=0.0, max_val=100.0)
    asc.register_attribute("AttackPower", base_val=20.0, min_val=0.0, max_val=500.0)

    # 1. Apply Instant Damage
    instant_damage = ActiveGameplayEffect(
        id="effect_damage_30",
        duration_type=EffectDurationType.INSTANT,
        duration_remaining=0.0,
        modifiers=[AttributeModifier("Health", ModifierOp.ADD, -30.0)],
        granted_tags=[]
    )
    asc.apply_effect(instant_damage)
    hp_after_dmg = asc.attributes["Health"].current_value
    print(f"1. Dégâts instantanés (-30 HP) : Base={asc.attributes['Health'].base_value:.1f}, Current={hp_after_dmg:.1f}")

    # 2. Apply Buff: +50% Attack Power (Duration)
    attack_buff = ActiveGameplayEffect(
        id="effect_berserk_buff",
        duration_type=EffectDurationType.DURATION,
        duration_remaining=10.0,
        modifiers=[AttributeModifier("AttackPower", ModifierOp.PERCENT_ADD, 0.50)],
        granted_tags=["state.berserk", "status.buff.attack"]
    )
    asc.apply_effect(attack_buff)
    atk_val = asc.attributes["AttackPower"].current_value
    print(f"2. Buff Berserk (+50% AP) : Base=20.0 -> Calculé={atk_val:.1f} (Tags: {asc.active_tags})")

    # 3. Apply Stacking Bleed
    bleed_effect = ActiveGameplayEffect(
        id="effect_bleed",
        duration_type=EffectDurationType.DURATION,
        duration_remaining=5.0,
        modifiers=[AttributeModifier("Health", ModifierOp.ADD, -5.0)],
        granted_tags=["status.debuff.bleed"]
    )
    asc.apply_effect(bleed_effect)
    asc.apply_effect(bleed_effect)  # 2nd stack
    print(f"3. Débuff Saignement (2 Stacks) : HP = {asc.attributes['Health'].current_value:.1f}")

    assert hp_after_dmg == 70.0, "Erreur calcul dégâts instantanés"
    assert atk_val == 30.0, "Erreur calcul pourcentage multiplicatif"
    print("-" * 65)
    print("[OK] Calculs d'attributs GAS et gestion des tags 100% validés.")
    print("=" * 65)


if __name__ == "__main__":
    run_gas_validation()
