"""PlaneGCS Interactive Constraint Solver CLI & Unit Verification Tool.

Usage:
    python solve_sketch.py
"""

from __future__ import annotations
import sys
import numpy as np
import scipy.linalg


def demo_planegcs_sketch_solving() -> int:
    print("[*] Démonstration du solveur d'esquisse 2D PlaneGCS avec décomposition QR")

    # Définition de 3 points d'un triangle rectangle :
    # P0 = (0, 0), P1 = (x1, y1), P2 = (x2, y2)
    # Paramètres : [x0, y0, x1, y1, x2, y2] (6 variables)
    x_init = np.array([0.1, 0.1, 75.0, 2.0, 1.0, 58.0], dtype=np.float64)

    # Contraintes :
    # C0 : x0 = 0 (P0 fixé à l'origine en X)
    # C1 : y0 = 0 (P0 fixé à l'origine en Y)
    # C2 : y1 = y0 (Segment P0-P1 horizontal)
    # C3 : (x1 - x0)^2 + (y1 - y0)^2 - 80^2 = 0 (Longueur P0-P1 = 80 mm)
    # C4 : (x2 - x0)(x1 - x0) + (y2 - y0)(y1 - y0) = 0 (Angle droit en P0)
    # C5 : (x2 - x0)^2 + (y2 - y0)^2 - 60^2 = 0 (Longueur P0-P2 = 60 mm)

    constraints = [
        lambda p: p[0] - 0.0,
        lambda p: p[1] - 0.0,
        lambda p: p[3] - p[1],
        lambda p: (p[2] - p[0]) ** 2 + (p[3] - p[1]) ** 2 - 80.0 ** 2,
        lambda p: (p[4] - p[0]) * (p[2] - p[0]) + (p[5] - p[1]) * (p[3] - p[1]),
        lambda p: (p[4] - p[0]) ** 2 + (p[5] - p[1]) ** 2 - 60.0 ** 2,
    ]

    x = x_init.copy()
    m = len(constraints)
    n = len(x)

    def residuals(v: np.ndarray) -> np.ndarray:
        return np.array([fn(v) for fn in constraints], dtype=np.float64)

    print(f"[*] Système initial : {n} paramètres, {m} contraintes")
    trust_radius = 5.0

    # Résolution DogLeg
    for it in range(80):
        r = residuals(x)
        cost = 0.5 * np.dot(r, r)
        if cost < 1e-10:
            print(f"[+] Convergence atteinte en {it} itérations (Coût résiduel : {cost:.2e})")
            break

        j = np.zeros((m, n), dtype=np.float64)
        for c in range(n):
            xp, xm = x.copy(), x.copy()
            xp[c] += 1e-7
            xm[c] -= 1e-7
            j[:, c] = (residuals(xp) - residuals(xm)) / (2.0 * 1e-7)

        grad = j.T @ r
        j_g = j @ grad
        denom = np.dot(j_g, j_g)
        step_sd = -grad if denom < 1e-12 else -(np.dot(grad, grad) / denom) * grad

        try:
            step_gn = np.linalg.lstsq(j, -r, rcond=1e-8)[0]
        except np.linalg.LinAlgError:
            step_gn = step_sd

        norm_gn = np.linalg.norm(step_gn)
        norm_sd = np.linalg.norm(step_sd)

        if norm_gn <= trust_radius:
            step = step_gn
        elif norm_sd >= trust_radius:
            step = (trust_radius / norm_sd) * step_sd
        else:
            diff = step_gn - step_sd
            a = np.dot(diff, diff)
            b = 2.0 * np.dot(step_sd, diff)
            c_val = np.dot(step_sd, step_sd) - trust_radius ** 2
            beta = (-b + np.sqrt(max(0.0, b * b - 4.0 * a * c_val))) / (2.0 * a)
            step = step_sd + beta * diff

        x_cand = x + step
        cost_cand = 0.5 * np.dot(residuals(x_cand), residuals(x_cand))

        if cost_cand < cost:
            x = x_cand
            if (cost - cost_cand) > 0.5 * cost:
                trust_radius = min(2.0 * trust_radius, 50.0)
        else:
            trust_radius = max(0.5 * trust_radius, 1e-6)

    # Diagnostic QR
    j_fin = np.zeros((m, n), dtype=np.float64)
    for c in range(n):
        xp, xm = x.copy(), x.copy()
        xp[c] += 1e-7
        xm[c] -= 1e-7
        j_fin[:, c] = (residuals(xp) - residuals(xm)) / (2.0 * 1e-7)

    q, r_mat, p_piv = scipy.linalg.qr(j_fin.T, pivoting=True)
    diag = np.abs(np.diag(r_mat))
    rank = int(np.sum(diag > 1e-6))
    dof = n - rank

    print(f"[*] Analyse spectrale QR : Rang Jacobien = {rank}/{n}, Degrés de liberté (DOF) = {dof}")
    print(f"[*] Coordonnées calculées :")
    print(f"    P0 = ({x[0]:.2f}, {x[1]:.2f}) mm (attendu : (0.00, 0.00))")
    print(f"    P1 = ({x[2]:.2f}, {x[3]:.2f}) mm (attendu : (80.00, 0.00))")
    print(f"    P2 = ({x[4]:.2f}, {x[5]:.2f}) mm (attendu : (0.00, 60.00))")

    success = dof == 0 and abs(x[0]) < 1e-3 and abs(x[1]) < 1e-3 and abs(x[2] - 80.0) < 1e-3 and abs(x[5] - 60.0) < 1e-3
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(demo_planegcs_sketch_solving())
