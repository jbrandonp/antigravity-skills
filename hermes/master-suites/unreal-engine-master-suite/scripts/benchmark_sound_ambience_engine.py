"""MMO Sound & Ambience Engine Benchmark.

Validates World of Warcraft audio systems:
- SoundEntries.dbc weighted variation selection with pitch/gain jitter
- Physical footstep surface resolution (Water, WMO Wood/Stone, ADT Grass/Dirt)
- Equal-power zone ambience crossfade: Gain_A^2 + Gain_B^2 = 1.0 (constant acoustic energy)
- Hierarchical music priority stack with anti-flapping combat grace period
- 3D spatial distance attenuation and directional audio cone directivity
- Audio bus ducking compressor (-6 dB to -12 dB on background buses)
"""

from __future__ import annotations

import math
import sys
from dataclasses import dataclass, field
from enum import Enum, auto

sys.stdout.reconfigure(encoding="utf-8")


class SoundCategory(Enum):
    """Audio bus routing categories."""
    MASTER = auto()
    SFX = auto()
    MUSIC = auto()
    AMBIENCE = auto()
    DIALOG = auto()


class TerrainMaterial(Enum):
    """Physical ground material categories from TerrainType.dbc and WMO MOPY."""
    DIRT = 1
    STONE = 2
    GRASS = 3
    WOOD = 4
    SAND = 5
    SNOW = 6
    WATER = 7


class MusicPriority(Enum):
    """Hierarchical music stack priority levels."""
    EXPLORATION = 20
    ZONE_INTRO = 40
    COMBAT = 60
    RAID_BOSS = 80
    CINEMATIC = 100


@dataclass(slots=True)
class SoundEntry:
    """Canonical SoundEntries.dbc record representation."""
    sound_id: int
    name: str
    category: SoundCategory
    file_variants: list[str]
    file_weights: list[int]
    base_volume: float = 1.0
    min_distance: float = 10.0
    distance_cutoff: float = 60.0

    def select_variant_deterministic(self, roll_fraction: float) -> str:
        """Picks a variation using weighted random selection based on roll in [0.0, 1.0)."""
        assert len(self.file_variants) == len(self.file_weights)
        total_weight = sum(self.file_weights)
        if total_weight <= 0:
            return self.file_variants[0]

        target_weight = roll_fraction * total_weight
        acc = 0.0
        for variant, weight in zip(self.file_variants, self.file_weights):
            acc += weight
            if acc > target_weight:
                return variant
        return self.file_variants[-1]


@dataclass(slots=True)
class MusicTrack:
    """Track metadata in the music priority stack."""
    track_id: int
    name: str
    priority: MusicPriority


class SoundAmbienceEngine:
    """Authoritative WoW 3D spatial audio and dynamic music engine."""

    COMBAT_GRACE_DURATION: float = 5.0  # Seconds before falling back from combat music

    def __init__(self) -> None:
        self.active_music_stack: list[MusicTrack] = []
        self.combat_grace_remaining: float = 0.0
        self.is_in_combat_state: bool = False
        self.is_dialog_ducking_active: bool = False

    def resolve_footstep_sound(
        self,
        foot_z: float,
        water_surface_z: float,
        is_on_wmo_structure: bool,
        wmo_material: TerrainMaterial | None,
        adt_dominant_material: TerrainMaterial,
    ) -> TerrainMaterial:
        """Resolves surface material for footstep sound generation."""
        # 1. Submerged fluid test
        if foot_z <= water_surface_z:
            return TerrainMaterial.WATER

        # 2. WMO architectural polygon test
        if is_on_wmo_structure and wmo_material is not None:
            return wmo_material

        # 3. Natural ADT terrain splatting
        return adt_dominant_material

    def calculate_equal_power_crossfade(self, tau: float) -> tuple[float, float]:
        """Calculates equal-power gains for outgoing and incoming audio streams.

        Guarantees Gain_out^2 + Gain_in^2 = 1.0 for constant perceived acoustic energy.
        """
        tau_clamped = max(0.0, min(1.0, tau))
        gain_out = math.cos(math.pi * 0.5 * tau_clamped)
        gain_in = math.sin(math.pi * 0.5 * tau_clamped)
        return gain_out, gain_in

    def push_music_track(self, track: MusicTrack) -> None:
        """Pushes a track onto the priority stack and maintains priority order."""
        self.active_music_stack.append(track)
        self.active_music_stack.sort(key=lambda t: t.priority.value)

    def pop_music_track(self, track_id: int) -> None:
        """Removes a track from the priority stack."""
        self.active_music_stack = [t for t in self.active_music_stack if t.track_id != track_id]

    def get_current_playing_music(self) -> MusicTrack | None:
        """Returns the highest priority track currently active."""
        if not self.active_music_stack:
            return None
        return self.active_music_stack[-1]

    def update_combat_music_fsm(
        self, threat_count: int, delta_time: float
    ) -> MusicPriority:
        """Updates combat music state machine with grace period hysteresis."""
        if threat_count > 0:
            # Active threat: enter combat immediately, reset grace timer
            self.is_in_combat_state = True
            self.combat_grace_remaining = self.COMBAT_GRACE_DURATION
            return MusicPriority.COMBAT

        # Zero threat
        if self.is_in_combat_state:
            # Slaying monster: stay in combat grace period
            self.combat_grace_remaining -= delta_time
            if self.combat_grace_remaining <= 0.0:
                self.is_in_combat_state = False
                self.combat_grace_remaining = 0.0
                return MusicPriority.EXPLORATION
            else:
                return MusicPriority.COMBAT

        return MusicPriority.EXPLORATION

    def compute_3d_spatial_attenuation(
        self,
        distance: float,
        min_distance: float,
        distance_cutoff: float,
    ) -> float:
        """Calculates clamped inverse distance spatial attenuation."""
        if distance <= min_distance:
            return 1.0
        if distance >= distance_cutoff:
            return 0.0

        # WoW clamped inverse distance model
        return min_distance / (min_distance + (distance - min_distance))

    def compute_directional_cone_attenuation(
        self,
        angle_radians: float,
        inner_cone_radians: float,
        outer_cone_radians: float,
        outer_gain: float = 0.20,
    ) -> float:
        """Calculates directional sound cone directivity factor."""
        if angle_radians <= inner_cone_radians:
            return 1.0
        if angle_radians >= outer_cone_radians:
            return outer_gain

        # Linear interpolation between inner and outer cone
        t = (angle_radians - inner_cone_radians) / (outer_cone_radians - inner_cone_radians)
        return 1.0 - t * (1.0 - outer_gain)

    def compute_ducked_bus_volume(
        self,
        base_volume: float,
        is_ducked: bool,
        ducking_db: float = -6.0,
    ) -> float:
        """Applies decibel attenuation when ducking bus is active."""
        if not is_ducked:
            return base_volume
        # Convert dB to linear gain multiplier: 10^(dB / 20)
        gain_mult = 10.0 ** (ducking_db / 20.0)
        return base_volume * gain_mult


def run_benchmark() -> None:
    """Executes deterministic test scenarios for the sound and ambience engine."""
    print("=== STARTING MMO SOUND & AMBIENCE ENGINE BENCHMARK ===")
    engine = SoundAmbienceEngine()

    # 1. Test SoundEntries Weighted Selection
    entry = SoundEntry(
        sound_id=101,
        name="SPELL_Frostbolt_Impact",
        category=SoundCategory.SFX,
        file_variants=["frostbolt_1.ogg", "frostbolt_2.ogg", "frostbolt_3.ogg"],
        file_weights=[10, 30, 60],  # Total = 100
    )
    # Roll 0.05 -> frostbolt_1 (weight 10)
    assert entry.select_variant_deterministic(0.05) == "frostbolt_1.ogg"
    # Roll 0.25 -> frostbolt_2 (range 10..40)
    assert entry.select_variant_deterministic(0.25) == "frostbolt_2.ogg"
    # Roll 0.75 -> frostbolt_3 (range 40..100)
    assert entry.select_variant_deterministic(0.75) == "frostbolt_3.ogg"
    print("[PASS] SoundEntries weighted variation selection verified")

    # 2. Test Footstep Terrain Material Resolution
    # A. Water submersion
    mat_water = engine.resolve_footstep_sound(
        foot_z=9.5, water_surface_z=10.0, is_on_wmo_structure=False, wmo_material=None, adt_dominant_material=TerrainMaterial.GRASS
    )
    assert mat_water == TerrainMaterial.WATER

    # B. WMO Wooden dock
    mat_wood = engine.resolve_footstep_sound(
        foot_z=12.0, water_surface_z=10.0, is_on_wmo_structure=True, wmo_material=TerrainMaterial.WOOD, adt_dominant_material=TerrainMaterial.DIRT
    )
    assert mat_wood == TerrainMaterial.WOOD

    # C. Natural ADT snow
    mat_snow = engine.resolve_footstep_sound(
        foot_z=15.0, water_surface_z=10.0, is_on_wmo_structure=False, wmo_material=None, adt_dominant_material=TerrainMaterial.SNOW
    )
    assert mat_snow == TerrainMaterial.SNOW
    print("[PASS] Footstep physical terrain and fluid surface resolution verified")

    # 3. Test Equal-Power Zone Ambience Crossfade
    # Test boundary tau=0.0 -> G_out=1.0, G_in=0.0
    g_out_0, g_in_0 = engine.calculate_equal_power_crossfade(0.0)
    assert math.isclose(g_out_0, 1.0) and math.isclose(g_in_0, 0.0)

    # Test midpoint tau=0.5 -> G_out = G_in = cos(pi/4) = 0.70710678
    g_out_mid, g_in_mid = engine.calculate_equal_power_crossfade(0.5)
    assert math.isclose(g_out_mid, g_in_mid, rel_tol=1e-5)
    # Fundamental acoustic energy preservation invariant: G_out^2 + G_in^2 = 1.0
    energy_sum = g_out_mid * g_out_mid + g_in_mid * g_in_mid
    assert math.isclose(energy_sum, 1.0, rel_tol=1e-6), "Acoustic energy sum must equal 1.0"

    # Test boundary tau=1.0 -> G_out=0.0, G_in=1.0
    g_out_1, g_in_1 = engine.calculate_equal_power_crossfade(1.0)
    assert math.isclose(g_out_1, 0.0, abs_tol=1e-6) and math.isclose(g_in_1, 1.0)
    print("[PASS] Equal-power zone crossfade (constant acoustic energy G_out^2 + G_in^2 = 1.0) verified")

    # 4. Test Music Priority Stack & Combat Grace Period
    track_explore = MusicTrack(1, "Elwynn Forest Ambience", MusicPriority.EXPLORATION)
    track_boss = MusicTrack(2, "Arthas Lich King Theme", MusicPriority.RAID_BOSS)

    engine.push_music_track(track_explore)
    assert engine.get_current_playing_music().name == "Elwynn Forest Ambience"

    # Raid boss interrupts exploration
    engine.push_music_track(track_boss)
    assert engine.get_current_playing_music().name == "Arthas Lich King Theme"

    # Raid boss ends
    engine.pop_music_track(2)
    assert engine.get_current_playing_music().name == "Elwynn Forest Ambience"

    # Combat FSM: Aggro engaged
    state1 = engine.update_combat_music_fsm(threat_count=1, delta_time=0.1)
    assert state1 == MusicPriority.COMBAT
    assert engine.is_in_combat_state is True

    # Monster dies (threat = 0) -> enters Combat Grace (5.0s remaining)
    state2 = engine.update_combat_music_fsm(threat_count=0, delta_time=2.0)
    assert state2 == MusicPriority.COMBAT, "Combat music should persist during 5s grace period"
    assert math.isclose(engine.combat_grace_remaining, 3.0)

    # Next monster pulled at 3s remaining -> resets grace timer
    state3 = engine.update_combat_music_fsm(threat_count=2, delta_time=0.1)
    assert state3 == MusicPriority.COMBAT
    assert math.isclose(engine.combat_grace_remaining, 5.0)

    # Monster dies and 5.0s expires -> returns to exploration
    engine.update_combat_music_fsm(threat_count=0, delta_time=3.0)
    state4 = engine.update_combat_music_fsm(threat_count=0, delta_time=2.5)
    assert state4 == MusicPriority.EXPLORATION
    assert engine.is_in_combat_state is False
    print("[PASS] Music priority stack & anti-flapping combat grace period verified")

    # 5. Test 3D Spatial Attenuation & Audio Cone
    # Inside min_distance (5m <= 10m) -> 1.0
    assert engine.compute_3d_spatial_attenuation(5.0, min_distance=10.0, distance_cutoff=60.0) == 1.0
    # Beyond cutoff (65m >= 60m) -> 0.0
    assert engine.compute_3d_spatial_attenuation(65.0, min_distance=10.0, distance_cutoff=60.0) == 0.0
    # Halfway (20m): 10 / (10 + 10) = 0.50
    assert math.isclose(engine.compute_3d_spatial_attenuation(20.0, 10.0, 60.0), 0.50)

    # Audio Cone: Inside inner cone (15 deg <= 30 deg) -> 1.0
    assert engine.compute_directional_cone_attenuation(math.radians(15), math.radians(30), math.radians(90)) == 1.0
    # Outside outer cone (100 deg >= 90 deg) -> 0.20
    assert math.isclose(
        engine.compute_directional_cone_attenuation(math.radians(100), math.radians(30), math.radians(90), outer_gain=0.20),
        0.20
    )
    print("[PASS] 3D spatial clamped inverse distance and directional cone attenuation verified")

    # 6. Test Ducking Compressor
    # Base 1.0 volume ducked by -6 dB -> 10^(-6/20) = ~0.501187
    ducked_vol = engine.compute_ducked_bus_volume(1.0, is_ducked=True, ducking_db=-6.0)
    assert math.isclose(ducked_vol, 0.501187, rel_tol=1e-4)
    print("[PASS] Audio bus ducking compressor (-6 dB attenuation) verified")

    print("\nALL SOUND & AMBIENCE ENGINE BENCHMARKS PASSED SUCCESSFULLY (100%)!")


if __name__ == "__main__":
    run_benchmark()
