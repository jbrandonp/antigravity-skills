---
name: competitive-intelligence-os
description: Professional competitive intelligence, market warfare, win/loss forensics, and operational benchmarking operating system. Make sure to use this skill whenever the user mentions competitors, competitive analysis, market research, lost deals, battlecards, pricing benchmark, Porter 5 forces, PESTEL, Wardley mapping, or wants to strategically outmaneuver rivals in SaaS, BTP, e-commerce, or local business, even if they simply ask "who are my competitors" or "why am I losing deals".
---

# Competitive Intelligence OS : Le Système d'Exploitation Stratégique

Ce skill applique les standards d'intelligence concurrentielle des leaders mondiaux (Fortune 500, SCIP, Valona World-Class, Crayon, McKinsey & Bain).
Il transforme la veille en décisions opérationnelles et en victoires commerciales en éliminant les rapports inutiles.

---

## 🧭 Principes Directeurs Inviolables

1. **La Question Décisionnelle Avant l'Outil (Pas de Porter par Défaut) :**
   Toujours invoquer `core/kiq_framework_router.py` pour déterminer le bon framework selon la question du décideur :
   - *Rentabilité du secteur ?* $\to$ 5 Forces de Porter (+1 Réglementaire) & PESTEL.
   - *Pertes de contrats ?* $\to$ Win/Loss Forensics débiaisée (Interdiction de Porter !).
   - *Espaces blancs & niches ?* $\to$ Groupes Stratégiques & Cartographie de Wardley.
   - *Écarts d'efficacité ?* $\to$ Benchmarking Opérationnel (Time-to-Value, CAC Payback, Churn).
   - *Armement commercial immédiat ?* $\to$ Battlecard 8-Secondes.

2. **La Règle des 3 Cercles & 4-5 Cibles Maximum :**
   Ne jamais noyer l'utilisateur sous 50 acteurs. Toujours cibler :
   - 2 à 3 concurrents Directs.
   - 1 concurrent Indirect.
   - 1 concurrent Substitut (ex: Excel ou le carnet papier).

3. **Le Filtre Déontologique "Wisdom Gate" (Traçabilité 100%) :**
   Chaque donnée de prix ou affirmation doit être validée par `core/wisdom_gate_checker.py` et adossée à une URL publique vérifiée ou un enregistrement légal (BCE, Moniteur Belge, Infogreffe).

4. **Débiaiser l'Alibi Commercial sur le Win/Loss :**
   Ignorer l'excuse automatique *"On était trop chers"*. Toujours chercher les vraies causes racines (délai de mise en place / Time-to-Value, absence de conformité Peppol 2026/TVA, friction UX).

5. **La Règle des 8 Secondes pour les Battlecards :**
   Toute battlecard commerciale produite via `deliverables/battlecard_8sec_builder.py` doit être scannable en 8 secondes chrono pendant un appel téléphonique en direct.

---

## 🛠️ Boîte à Outils Python Native (`uv run`)

L'agent dispose d'outils Python strictement typés et testés, exécutables directement sous Windows avec `uv run` :

- `cli.py` : Point d'entrée en ligne de commande unifié pour piloter tous les modules en 1 commande locale.
- `core/kiq_framework_router.py` : Aiguillage automatique des KIQs vers le bon framework.
- `core/wisdom_gate_checker.py` : Vérification des 5 serrous éthiques et légaux (standards SCIP).
- `core/win_loss_debiasing_engine.py` : Requalification des motifs de perte d'affaires (démasquage de l'alibi du prix).
- `core/firmographic_job_watcher.py` : Surveillance des inflexions sur offres d'emploi (signaux à 6-12 mois).
- `core/operational_benchmarker.py` : Calcul du Time-to-Value et du CAC Payback ajusté de la marge brute.
- `core/wargame_scenario_simulator.py` : Simulation tactique multi-tours (Shell/IBM style).
- `core/disruption_radar_index.py` : Calculateur de l'indice composite DVI (Disruption Vulnerability Index 0-100).
- `core/positioning_plotter_svg.py` : Générateur vectoriel SVG pour matrices 2x2 et diagrammes radar 6 axes.
- `core/wardley_mapper_svg.py` : Traceur vectoriel SVG de cartes de Wardley (Wardley Mapping).
- `core/altman_distress_calculator.py` : Calculateur d'Altman Z'-Score pour détection de détresse financière BNB/BCE.
- `core/markov_churn_engine.py` : Moteur stochastique de Markov (churn) et équation de diffusion de Frank Bass.
- `codegen/vampire_migrator_builder.py` : Usine de génération automatique de scripts de migration 1-clic ("Attaque Vampire").
- `sentinels/price_watcher_daemon.py` : Vigie cryptographique d'arrière-plan (surveillance SHA-256 des tarifs).
- `deliverables/battlecard_8sec_builder.py` : Générateur de fiches d'assaut 8 secondes.
- `deliverables/magic_quadrant_svg.py` : Générateur vectoriel SVG du Gartner Magic Quadrant (Leaders, Challengers, Visionnaires, Niche).
- `deliverables/cdd_report_generator.py` : Exporteur de classeurs Excel professionnels (`.xlsx` via openpyxl avec formules natives).
- `deliverables/strategic_brief_compiler.py` : Compilateur du One-Pager décisionnel (Noyau de Rumelt + Premortem).
- `deliverables/assault_landing_builder.py` : Générateur de pages d'assaut web comparatives (HTML5/Tailwind responsive).
- `deliverables/knowledge_graph_html.py` : Générateur de graphes relationnels interactifs du marché (Canvas 2D).
- `deliverables/win_wire_publisher.py` : Diffuseur de victoires commerciales "Win-Wire" (Silver Bullet, FUD neutralisé).

---

## 🔄 Protocole d'Exécution en 5 Étapes

### Étape 1 : Formuler les KIQs & Sélectionner le Framework
- Identifier la décision concrète à prendre.
- Exécuter l'aiguilleur pour valider le framework adéquat et bannir les outils inadaptés.

### Étape 2 : Cadrer les 4-5 Cibles (Directs, Indirects, Substituts)
- Définir les 2-3 rivaux directs, 1 rival indirect, 1 substitut.
- Affecter les niveaux de surveillance (Rapprochée, Substantielle, Large).

### Étape 3 : Collecte à 4 Voix & Filtre Wisdom Gate
- Croiser les sources : Voix Entreprise (bilans, CGV), Voix Analyste, Voix Expert/HUMINT (acheteurs réels), Voix Médias.
- Vérifier la provenance et l'admissibilité légale de chaque fait avant stockage dans `storage/intelligence.db`.

### Étape 4 : Déconstruction & Débiaisage
- Si perte de vente : passer au crible les verbatims avec `win_loss_debiasing_engine.py`.
- Si comparaison de prix : calculer le TCO réel sur 36 mois avec les frais d'options masqués.
- Si benchmarking : mesurer l'écart de Time-to-Value (TTV) et la vitesse d'onboarding.

### Étape 5 : Restitution & Armement Opérationnel
- Générer la Battlecard 8-Secondes pour le terrain (`uv run python cli.py battlecard <id>`).
- Générer le Magic Quadrant exécutif (`uv run python cli.py quadrant`).
- Compiler la note stratégique selon le **Noyau de Rumelt** (Diagnostic brutal, politique directrice, actions cohérentes).
- Rédiger obligatoirement l'audit de **Premortem** (les raisons pour lesquelles nous pourrions échouer).
- Déployer la landing page d'assaut comparative (`uv run python cli.py landing <concurrent>`).
- Diffuser le Win-Wire dès qu'un contrat est remporté (`uv run python cli.py win-wire <deal> <concurrent>`).

---

## ⚡ Commandes Rapides CLI (`ci-os`)

```bash
# 1. Aiguillage KIQ d'une question stratégique (interdiction de Porter si vente perdue)
uv run python cli.py route "Pourquoi perdons-nous des devis face à Obat ?"

# 2. Génération de Battlecard 8-Secondes
uv run python cli.py battlecard comp_obat --out battlecard_obat.md

# 3. Magic Quadrant de Gartner vectoriel SVG
uv run python cli.py quadrant --out gartner_quadrant.svg

# 4. Indice Composite de Vulnérabilité à la Disruption (DVI 0-100)
uv run python cli.py disruption "Legacy-BTP" --tech 85 --price 90 --fin 70 --fric 80

# 5. Simulation Wargame 3 tours (Shell / IBM)
uv run python cli.py wargame "BTP-Cloud" --price-drop 20 --pe-backed

# 6. Benchmarking Opérationnel (TTV, CAC Payback, NRR)
uv run python cli.py bench --us-ttv 1 --them-ttv 45 --us-cac 450 --them-cac 1200 --us-arpu 99 --them-arpu 89

# 7. Landing Page Comparative d'Assaut (Guerrilla Marketing HTML5/Tailwind)
uv run python cli.py landing "BTP-Cloud" --out landing_btp_cloud.html

# 8. Graphe de Connaissances Relationnel du Marché (Canvas interactif)
uv run python cli.py graph --out market_graph.html

# 9. Publication instantanée de Win-Wire commercial
uv run python cli.py win-wire "Chantier Tour Bruxelles" "BTP-Cloud" --acv 36000 --bullet "Conformité Peppol 2026 native"

# 10. Calcul d'Altman Z'-Score pour PME
uv run python cli.py zscore --wc 45000 --ta 250000 --re 30000 --ebit 18000 --be 80000 --tl 170000 --sales 400000
```

