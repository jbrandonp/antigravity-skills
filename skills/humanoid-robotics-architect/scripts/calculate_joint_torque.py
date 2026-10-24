import sys
import math

def calculate_torque(mass_kg=5.0, link_len_m=0.4, max_accel_rad_s2=15.0):
    g = 9.81
    r_com = link_len_m / 2.0
    inertia = (1.0 / 3.0) * mass_kg * (link_len_m ** 2)

    # Torque statique max (bras horizontal theta = 90 deg)
    tau_static = mass_kg * g * r_com

    # Torque dynamique d'acceleration
    tau_dynamic = inertia * max_accel_rad_s2

    tau_total = tau_static + tau_dynamic

    print("\n================ DIMENSIONNEMENT COUPLE ARTICULAIRE ROBOTIQUE ================")
    print(f"Masse du lien : {mass_kg} kg | Longueur : {link_len_m} m | Accélération : {max_accel_rad_s2} rad/s²")
    print(f"Inertie articulaire (I) : {inertia:.4f} kg·m²")
    print(f"Couple statique (Gravité) : {tau_static:.2f} N·m")
    print(f"Couple dynamique (Inertie) : {tau_dynamic:.2f} N·m")
    print(f">>> COUPLE TOTAL REQUIS (Pic) : {tau_total:.2f} N·m <<<")
    print(f"Moteur recommandé (marge x1.5) : Couple de pointe minimum >= {tau_total * 1.5:.2f} N·m\n")
    return 0

if __name__ == "__main__":
    calculate_torque()
