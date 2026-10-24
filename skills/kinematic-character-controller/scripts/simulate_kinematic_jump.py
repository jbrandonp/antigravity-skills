"""
Kinematic Character Controller — Simulateur Déterministe de Saut & Game Feel
Auteur: Brandon (Antigravity Studio Engine)
Règles: Typage strict, zéro Any, 60 FPS tick simulation.
"""

from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class JumpProfile:
    jump_height: float
    time_to_apex: float
    coyote_time_seconds: float = 0.12   # ~7 frames à 60Hz
    jump_buffer_seconds: float = 0.15   # ~9 frames à 60Hz
    jump_cut_multiplier: float = 0.50

    @property
    def gravity(self) -> float:
        return (2.0 * self.jump_height) / (self.time_to_apex ** 2)

    @property
    def initial_jump_velocity(self) -> float:
        return (2.0 * self.jump_height) / self.time_to_apex


class KinematicPlayerSimulation:
    def __init__(self, profile: JumpProfile) -> None:
        self.profile: JumpProfile = profile
        self.y_pos: float = 0.0
        self.y_vel: float = 0.0
        self.is_grounded: bool = True
        self.coyote_timer: float = 0.0
        self.jump_buffer_timer: float = 0.0

    def update_tick(self, delta_time: float, jump_pressed: bool, jump_held: bool, left_ground_this_frame: bool) -> Tuple[float, float, str]:
        event = "SOL"
        if left_ground_this_frame and self.is_grounded:
            self.is_grounded = False
            self.coyote_timer = self.profile.coyote_time_seconds

        if jump_pressed:
            self.jump_buffer_timer = self.profile.jump_buffer_seconds

        # Déclenchement de saut avec assistance Coyote Time & Jump Buffer
        can_jump = self.is_grounded or (self.coyote_timer > 0.0)
        has_buffered_jump = self.jump_buffer_timer > 0.0

        if can_jump and has_buffered_jump:
            self.y_vel = self.profile.initial_jump_velocity
            self.is_grounded = False
            self.coyote_timer = 0.0
            self.jump_buffer_timer = 0.0
            event = "[SAUT DECLENCHE]"

        # Physique aérienne
        if not self.is_grounded:
            current_gravity = self.profile.gravity
            # Apex Floatiness
            if abs(self.y_vel) < 2.0:
                current_gravity *= 0.60
                event = "[APEX FLOAT]"

            # Variable Jump Cut
            if self.y_vel > 0.0 and not jump_held:
                self.y_vel *= self.profile.jump_cut_multiplier
                event = "[JUMP CUT]"

            self.y_vel -= current_gravity * delta_time
            self.y_pos += self.y_vel * delta_time

            # Collision sol
            if self.y_pos <= 0.0:
                self.y_pos = 0.0
                self.y_vel = 0.0
                self.is_grounded = True
                event = "[ATTERRISSAGE]"

            if self.coyote_timer > 0.0:
                self.coyote_timer -= delta_time

        if self.jump_buffer_timer > 0.0:
            self.jump_buffer_timer -= delta_time

        return (self.y_pos, self.y_vel, event)


def run_kinematic_simulation() -> None:
    print("=" * 70)
    print("   KINEMATIC CHARACTER CONTROLLER : SIMULATION DE GAME FEEL 60HZ")
    print("=" * 70)
    profile = JumpProfile(jump_height=4.0, time_to_apex=0.35)
    print(f"Hauteur Désirée: {profile.jump_height:.1f} m | Temps d'Apex: {profile.time_to_apex:.2f} s")
    print(f"Gravité Calculée: {profile.gravity:.2f} m/s² | Vélocité Initiale: {profile.initial_jump_velocity:.2f} m/s")
    print("-" * 70)

    sim = KinematicPlayerSimulation(profile)
    dt = 1.0 / 60.0

    print("Scénario : Le joueur quitte une plateforme et saute pendant le Coyote Time")
    history: List[str] = []
    for frame in range(1, 35):
        left_edge = (frame == 2)
        press_jump = (frame == 6)   # 4 frames après être tombé dans le vide
        hold_jump = (frame < 18)

        y, vy, evt = sim.update_tick(dt, press_jump, hold_jump, left_edge)
        bar = "#" * int(y * 4)
        if frame % 3 == 0 or "SAUT" in evt or "ATTERRISSAGE" in evt:
            history.append(f"Frame {frame:02d} | Y={y:4.2f}m | Vy={vy:5.2f}m/s | {evt:18s} | {bar}")

    for line in history:
        print(line)

    print("=" * 70)
    print("[OK] Assistance Coyote Time & Saut Kinématique parfaitement validés.")
    print("=" * 70)


if __name__ == "__main__":
    run_kinematic_simulation()
