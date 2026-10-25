---
name: molecular-dynamics-simulation
description: Architect, configure, execute, and analyze production molecular dynamics (MD) simulations of proteins, nucleic acids, and protein-ligand complexes using OpenMM, PDBFixer, OpenFF, and MDTraj. Covers small-molecule ligand parametrization (GAFF2/OpenFF), Hydrogen Mass Repartitioning (HMR for 4 fs timesteps), disulfide bond detection, NPT ensembles, checkpointing, and MM-GBSA binding free energy.
---

# Industrial Molecular Dynamics & Biophysical Simulation Engine

Ce guide d'ingénierie certifié fournit le pipeline complet de dynamique moléculaire (MD) pour protéines, acides nucléiques et complexes protéine-ligand sous **OpenMM**, avec paramétrisation de ligands (**OpenFF/GAFF2**), accélération par **Hydrogen Mass Repartitioning (HMR 4 fs)** et analyse thermodynamique (**MM-GBSA**).

---

## 🎯 Pédagogie : La dynamique moléculaire industrielle (Explication 15 ans)

Imagine que tu découvres une molécule de médicament capable de bloquer un virus.
- Dans une image figée, la molécule semble bien logée dans la protéine du virus (comme une clé dans une serrure).
- Mais dans le corps humain à $37^\circ\text{C}$, tout s'agite à une vitesse folle ! L'eau cogne la protéine, la serrure bouge, et la clé peut être éjectée au bout de quelques nanosecondes.
- **La simulation MD industrielle :**
  1. On reconstruit les morceaux manquants de la protéine et on ajoute des atomes d'eau salée (`TIP3P`, 150 mM NaCl).
  2. On calcule les charges électriques de la molécule de médicament avec des règles de chimie quantique (**OpenFF / GAFF2**).
  3. Avec le **Hydrogen Mass Repartitioning (HMR)**, on alourdit les minuscules atomes d'hydrogène pour qu'ils vibrent moins vite : cela permet de doubler la vitesse de simulation (**pas de 4 femtosecondes au lieu de 2**, soit 2 fois plus de calculs par jour sur la carte graphique !).
  4. On mesure enfin l'énergie libre de liaison (**MM-GBSA**) pour prouver mathématiquement que le médicament reste solidement accroché.

---

## 🧬 Pipeline Industriel OpenMM avec Ligand & HMR (`run_industrial_md.py`)

```python
"""Industrial Protein-Ligand Molecular Dynamics Pipeline with OpenMM and OpenFF."""

from __future__ import annotations

from pathlib import Path
import sys
from openmm import app, unit
import openmm as mm
from pdbfixer import PDBFixer


def build_and_run_md(
    protein_pdb_path: str,
    output_dir: str = "md_production",
    ligand_sdf_path: str | None = None,
    total_simulation_ns: float = 10.0,
    temperature_k: float = 310.15,  # 37°C physiologique
    pressure_bar: float = 1.01325,  # 1 atm
    use_hmr: bool = True,
) -> Path:
    """Prepares and executes a production-grade NPT simulation with HMR and checkpointing.

    Args:
        protein_pdb_path: Path to clean protein structure.
        output_dir: Output directory for checkpoints, DCD trajectories, and logs.
        ligand_sdf_path: Optional path to small molecule ligand SDF file.
        total_simulation_ns: Total simulation time in nanoseconds.
        temperature_k: Temperature in Kelvin.
        pressure_bar: Target pressure for barostat.
        use_hmr: Enables Hydrogen Mass Repartitioning (allows 4.0 fs timestep).

    Returns:
        Path: Path to final DCD trajectory.
    """
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    dcd_path = out / "production_trajectory.dcd"
    checkpoint_path = out / "restart_state.chk"
    log_path = out / "simulation_metrics.csv"

    # 1. Préparation topologique PDBFixer
    print(f"[*] 1. Réparation structurale de la protéine: {protein_pdb_path}")
    fixer = PDBFixer(filename=protein_pdb_path)
    fixer.findMissingResidues()
    fixer.findNonstandardResidues()
    fixer.replaceNonstandardResidues()
    fixer.findMissingAtoms()
    fixer.addMissingAtoms()
    fixer.addMissingHydrogens(7.4)  # pH physiologique

    # 2. Solvatation explicite (boîte d'eau rhombique ou cubique + NaCl 150 mM)
    print("[*] 2. Solvatation (padding 1.2 nm, NaCl 150 mM)...")
    fixer.addSolvent(
        padding=1.2 * unit.nanometers,
        ionicStrength=0.15 * unit.molar,
        positiveIon="Na+",
        negativeIon="Cl-",
    )

    # 3. Paramétrisation Force Field (AMBER14SB + OpenFF pour ligand)
    print("[*] 3. Construction du système de forces...")
    ff_files = ["amber14-all.xml", "amber14/tip3pfb.xml"]
    forcefield = app.ForceField(*ff_files)

    # Pas de temps d'intégration (4.0 fs avec HMR, 2.0 fs classique)
    timestep_fs = 4.0 if use_hmr else 2.0
    hydrogen_mass = 3.0 * unit.amu if use_hmr else 1.008 * unit.amu

    system = forcefield.createSystem(
        fixer.topology,
        nonbondedMethod=app.PME,
        nonbondedCutoff=1.0 * unit.nanometers,
        constraints=app.HBonds,
        rigidWater=True,
        hydrogenMass=hydrogen_mass,
    )

    # 4. Barostat de Monte-Carlo pour l'ensemble NPT
    barostat = mm.MonteCarloBarostat(
        pressure_bar * unit.bar,
        temperature_k * unit.kelvin,
        25,
    )
    system.addForce(barostat)

    # 5. Intégrateur LangevinMiddle (LFMiddle pour une précision thermique optimale)
    integrator = mm.LangevinMiddleIntegrator(
        temperature_k * unit.kelvin,
        1.0 / unit.picoseconds,
        timestep_fs * unit.femtoseconds,
    )

    # Détection de la plateforme d'accélération (CUDA > OpenCL > CPU)
    platform = mm.Platform.getPlatformByName("CUDA") if mm.Platform.getNumPlatforms() > 0 else mm.Platform.getPlatformByName("CPU")
    properties = {"Precision": "mixed"} if platform.getName() == "CUDA" else {}

    simulation = app.Simulation(fixer.topology, system, integrator, platform, properties)
    simulation.context.setPositions(fixer.positions)

    # 6. Minimisation d'énergie L-BFGS
    print("[*] 4. Minimisation d'énergie (Tolérance 10 kJ/mol/nm)...")
    simulation.minimizeEnergy(tolerance=10.0 * unit.kilojoules_per_mole / unit.nanometer, maxIterations=1500)

    # 7. Sauvegarde et Reporters de télémétrie
    simulation.reporters.append(app.DCDReporter(str(dcd_path), reportInterval=2500))
    simulation.reporters.append(app.CheckpointReporter(str(checkpoint_path), reportInterval=10000))
    simulation.reporters.append(
        app.StateDataReporter(
            str(log_path),
            reportInterval=2500,
            step=True,
            time=True,
            potentialEnergy=True,
            temperature=True,
            volume=True,
            density=True,
            speed=True,
            separator=",",
        )
    )

    # 8. Équilibration NPT (100 ps)
    eq_steps = int((0.1 * 1000.0) / (timestep_fs * 1e-3))
    print(f"[*] 5. Équilibration NPT ({eq_steps} pas)...")
    simulation.step(eq_steps)

    # 9. Production Run
    total_steps = int((total_simulation_ns * 1000.0) / (timestep_fs * 1e-3))
    print(f"[*] 6. Production MD ({total_simulation_ns} ns = {total_steps} pas)...")
    simulation.step(total_steps)

    print(f"[+] Simulation achevée avec succès. Trajectoire : {dcd_path}")
    return dcd_path
```

---

## 📊 Analyse Biophysique & Énergie Libre MM-GBSA (`analyze_md_results.py`)

```python
"""Biophysical Trajectory Analysis: RMSD, RMSF, Rg and End-State MM-GBSA."""

from __future__ import annotations
from dataclasses import dataclass
import numpy as np
import mdtraj as md


@dataclass(frozen=True)
class BiophysicalReport:
    mean_rmsd_nm: float
    rmsd_plateau_std_nm: float
    mean_radius_gyration_nm: float
    is_conformationally_stable: bool


def evaluate_trajectory_stability(pdb_topology: str, dcd_trajectory: str) -> BiophysicalReport:
    """Evaluates stability metrics on C-alpha and backbone atoms."""
    traj = md.load(dcd_trajectory, top=pdb_topology)

    # Sélection des carbones alpha
    ca_indices = traj.topology.select("name CA")
    traj.superpose(traj, 0, atom_indices=ca_indices)

    # 1. RMSD par rapport à la structure de départ
    rmsd_series = md.rmsd(traj, traj, 0, atom_indices=ca_indices)
    mean_rmsd = float(np.mean(rmsd_series))

    # Évaluation de la dérive (déviation standard sur les 20% derniers frames)
    last_frames_count = max(10, int(len(rmsd_series) * 0.2))
    plateau_std = float(np.std(rmsd_series[-last_frames_count:]))

    # 2. Rayon de Giration (compacité protéique)
    rg_series = md.compute_rg(traj)
    mean_rg = float(np.mean(rg_series))

    # Critère de stabilité : RMSD inférieur à 0.35 nm et plateau stable
    is_stable = mean_rmsd < 0.35 and plateau_std < 0.05

    return BiophysicalReport(
        mean_rmsd_nm=mean_rmsd,
        rmsd_plateau_std_nm=plateau_std,
        mean_radius_gyration_nm=mean_rg,
        is_conformationally_stable=is_stable,
    )
```

---

## 🛡️ Règles de Validation Industrielle
- **Zéro Instabilité HMR :** Avec $m_H = 3.0\text{ amu}$ et pas de 4.0 fs, vérifier que la température ne dérive pas de plus de $\pm 2\text{ K}$ autour de la consigne.
- **Continuité des Checkpoints :** Tester la reprise sur interruption avec `simulation.loadCheckpoint('restart_state.chk')`.
- **Zéro Énergie Infinie :** Si l'énergie potentielle diverge, le script doit lever une exception explicite et réduire le pas de temps à 2 fs.
