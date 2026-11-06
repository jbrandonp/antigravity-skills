---
name: conversational-dynamics-profiler
description: Deep psychological profiling, interpersonal relationship intelligence, and behavioral dynamics auditing from raw chat and messaging archives (WhatsApp, Instagram, Messenger, iMessage, Discord, Telegram). Use this skill whenever the user asks to analyze a conversation, decode a relationship or couple dynamics, audit communication patterns, extract behavioral metrics (latency, bursts, emojis, questions), map attachment styles, perform functional conflict-repair analysis, assess third-party triangulation, or build an actionable interpersonal strategy.
---

# 🕵️ Conversational Dynamics Profiler & Relationship Intelligence (v8.0 Enterprise Suite)

Un cadre méthodologique, clinique et logiciel de référence pour **décoder, profiler, simuler, visualiser et auditer les dynamiques interpersonnelles, amoureuses et familiales** à partir d'échanges numériques (messageries instantanées, vocaux, réseaux sociaux).

Ce framework transforme des flux textuels bruts en une **cartographie psychologique prédictive, rigoureuse et immédiatement actionnable**.

---

## 🏛️ Les 4 Piliers Épistémiques Inviolables

Toute analyse produite par ce skill doit impérativement étiqueter ses affirmations selon la grille :
- **`[Vérifié]`** : Donnée matérielle, métrique comptée, horodatage exact, fait objectif extrait du dump.
- **`[Déclaré]`** : Affirmation faite par un interlocuteur sur lui-même, un tiers ou son passé (sans preuve externe).
- **`[Pattern]`** : Régularité comportementale ou statistique récurrente (observée sur ≥ 3 occurrences).
- **`[Hypothèse]`** : Modèle interprétatif déduit (attachement, mentalisation, mécanismes de défense), falsifiable.

> ⚠️ **Interdiction formelle de psychiatrisation sauvage :** Ne jamais poser de diagnostic médical catégoriel (DSM/CIM) sur des logs de chat. Toujours modéliser des **styles relationnels, des modes opératoires et des boucles fonctionnelles**, et tester systématiquement les contre-arguments situationnels (lune de miel, culture, plateforme). Voir `references/epistemic_audit_framework.md`.

---

## 🧰 Boîte à Outils CLI & Scripts Déterministes (scripts/)

Tous les scripts sont 100% natifs en Python 3.10+ (zéro dépendance externe, encodage UTF-8 sous Windows garanti) :

```bash
# 0. Cockpit Terminal Interactif & Pipeline Tout-en-Un (NOUVEAU v8.0)
python scripts/interactive_profiler_cli.py
# Ou en mode batch automatique (génère les 4 artefacts : JSON, métriques, rapport santé, dashboard HTML) :
python scripts/interactive_profiler_cli.py --run-all --input raw_chat.txt --output-prefix mon_audit --anonymize

# 1. Normalisation Universelle & Anonymisation PII (Meta, WhatsApp, Telegram, Discord, CSV)
python scripts/universal_chat_converter.py --input raw_chat.txt --output normalized.json --anonymize

# 2. Audit Métrique Quantitatif Détaillé (Entropie Shannon, RTT, Gottman 5:1, Bids for Connection, 24h & 7j)
python scripts/analyze_chat_metrics.py --input normalized.json --format markdown

# 3. Rapport d'Intelligence Relationnelle 360° avec Score de Santé (/100) & Écologie Affective
python scripts/generate_relationship_report.py --input normalized.json --output rapport_sante.md

# 4. Tableau de Bord Visuel Interactif HTML/SVG (100% autonome, zéro CDN, offline, 24h & 7 jours)
python scripts/export_html_dashboard.py --input normalized.json --output dashboard.html

# 5. Simulateur Prédictif, Machine à États Markoviens & Reformulateur CNV
# 5. Simulateur Prédictif (12 scénarios de crise), Machine à États & CNV
python scripts/simulate_conversational_scenarios.py --scenario demand_withdraw
python scripts/simulate_conversational_scenarios.py unannounced_silence
python scripts/simulate_conversational_scenarios.py --state-machine
python scripts/simulate_conversational_scenarios.py --cnv-reframe "Tu es toujours en retard, tu penses jamais à moi !"

# 6. Exécution de la Suite de Tests Automatisée (17 tests unitaires validés)
python tests/test_conversational_suite.py
```

---

## 🏗️ L'Architecture Intégrale en 7 Couches

Consulter la spécification détaillée dans [`references/full_architecture_specification.md`](references/full_architecture_specification.md).

```text
 ┌────────────────────────────────────────────────────────────────────────┐
 │ COUCHE 7 : PRÉSENTATION MULTI-SURFACES & COCKPIT INTERACTIF CLI        │
 │ ↳ Rapport Markdown 360°, Dashboard HTML/SVG offline, Scripts de crise  │
 ├────────────────────────────────────────────────────────────────────────┤
 │ COUCHE 6 : SIMULATION NON LINÉAIRE & STRESS-TESTING CHAOTIQUE          │
 │ ↳ Attracteurs étranges, Simulations What-If, Vulnérabilité aux chocs   │
 ├────────────────────────────────────────────────────────────────────────┤
 │ COUCHE 5 : SOCIOGRAMME, TRIANGULATION & ÉCOLOGIE SYSTÉMIQUE            │
 │ ↳ Tiers pivots (Bowen), Triangle de Karpman/TED, Sanctuarisation       │
 ├────────────────────────────────────────────────────────────────────────┤
 │ COUCHE 4 : FORMULATION CLINIQUE 4P & ATTACHEMENT DYNAMIQUE             │
 │ ↳ 4P Model, Échelle Fonagy, Danse Demande-Retrait, Porges Polyvagal    │
 ├────────────────────────────────────────────────────────────────────────┤
 │ COUCHE 3 : THÉORIE DE L'INFORMATION & DYNAMIQUE STOCHASTIQUE           │
 │ ↳ Entropie de Shannon H, IAT Burstiness B, RTT Latency, Cycles 24h     │
 ├────────────────────────────────────────────────────────────────────────┤
 │ COUCHE 2 : PSYCHOLINGUISTIQUE, ACTES DE LANGAGE & SÉMIOTIQUE           │
 │ ↳ 4 Cavaliers Gottman, Actes performatifs (Searle), Morphologie        │
 ├────────────────────────────────────────────────────────────────────────┤
 │ COUCHE 1 : INGESTION UNIVERSELLE, NORMALISATION & HYGIÈNE PII          │
 │ ↳ Meta (Insta/Mess), WhatsApp, Telegram, Discord, iMessage, CSV/JSONL  │
 └────────────────────────────────────────────────────────────────────────┘
```

---

## 📚 Références Théoriques & Manuels Opérationnels

- [`references/nonviolent_communication_and_reframing.md`](references/nonviolent_communication_and_reframing.md) : **NOUVEAU** : Guide pratique de Communication Non Violente (CNV - Marshall Rosenberg), modèle OSBD, désamorçage des 4 cavaliers et reformulations pacifiantes.
- [`references/coregulation_and_attachment_repair.md`](references/coregulation_and_attachment_repair.md) : **NOUVEAU** : Corégulation neurobiologique, thérapie de couple centrée sur les émotions (EFT - Sue Johnson), approche PACT (Stan Tatkin), la "Bulle du Couple" et cycle de réparation en 4 étapes.
- [`references/psychological_and_clinical_profiling_guide.md`](references/psychological_and_clinical_profiling_guide.md) : Profilage psychologique et axes psychiatriques, organisation de Kernberg, catalogue des défenses de Vaillant (primitives, intermédiaires, matures), TDAH/RSD et vulnérabilités émotionnelles.
- [`references/behavioral_analysis_and_conditioning_guide.md`](references/behavioral_analysis_and_conditioning_guide.md) : Analyse comportementale appliquée (TCC/Skinner), modèle ABC, renforcement intermittent variable, sémiotique des micro-comportements textuels et pics d'extinction.
- [`references/long_term_relationship_guide_and_strategy.md`](references/long_term_relationship_guide_and_strategy.md) : Guide stratégique du couple sur le long terme (Maison Gottman, 69% de conflits perpétuels, polarité érotique et mystère selon Esther Perel, pacte patrimonial et les 6 heures magiques par semaine).
- [`references/epistemic_audit_framework.md`](references/epistemic_audit_framework.md) : Standard épistémique ([Vérifié], [Déclaré], [Pattern], [Hypothèse]).
- [`references/gottman_attachment_matrix.md`](references/gottman_attachment_matrix.md) : Modèle de John Gottman (4 Cavaliers), Théorie de la Mentalisation (Fonagy) et boucle Demande-Retrait.
- [`references/sociogram_and_triangulation.md`](references/sociogram_and_triangulation.md) : Théorie des systèmes de Murray Bowen, cartographie des tiers tampons et frontières du couple.
- [`references/dialectical_behavior_and_invariants.md`](references/dialectical_behavior_and_invariants.md) : Dialectique du don et de la dette (Marcel Mauss), actes performatifs (Austin/Searle) et invariants structuraux.
- [`references/somatic_anthropology_and_material_worlds.md`](references/somatic_anthropology_and_material_worlds.md) : Choc ontologique matière/virtuel, dysmorphies corporelles croisées et alliance matrilinéaire.
- [`references/neurobiology_and_polyvagal_dynamics.md`](references/neurobiology_and_polyvagal_dynamics.md) : Théorie polyvagale (Stephen Porges), dopamine vs ocytocine en messagerie, attracteurs étranges de la théorie du chaos.
- [`references/crisis_deescalation_playbook.md`](references/crisis_deescalation_playbook.md) : Protocoles d'intervention immédiate (Alpha, Beta, Gamma, Delta).
- [`references/full_architecture_specification.md`](references/full_architecture_specification.md) : Spécification complète des 7 couches techniques et mathématiques.

---

## 📋 Gabarits & Schémas Canoniques (templates/)

- [`templates/normalized_chat_schema.json`](templates/normalized_chat_schema.json) : Schéma JSON standard pour corpus de chat normalisés.
- [`templates/relational_audit_template.md`](templates/relational_audit_template.md) : Modèle professionnel de rapport d'intelligence relationnelle et d'audit clinique.
