---
name: verify-brandon
description: "Proof bar BRANDON AI. Le réel, jamais le self-report."
version: 1.0.0
author: Léopold (BRANDON AI)
license: MIT
metadata:
  hermes:
    tags: [verification, quality, brainmaxxing]
    related_skills: [poteto-playbooks]
---

# verify-brandon — Proof bar

## When to Use

Avant de déclarer un livrable « fait » : toute vérification, audit, ou test de système.

Inspiré de poteto/verification-skill-example (patterns, inspiration — pas de licence). Constitution de vérification pour tout livrable BRANDON AI, notamment quality-auditor.

## La proof bar (5 règles)

1. **État frais d'abord** — vérifier l'état ACTUEL du système (doctor/health-check), jamais de preuve sur une instance périmée.
2. **Chemin réel, pas raccourci** — la preuve passe par le chemin utilisateur réel. Interdit : prouver en invoquant des handlers internes au lieu du parcours normal.
3. **Prouver des EFFETS DE BORD** — un mail envoyé = relu depuis la boîte ; un fichier écrit = relu du disque ; un event créé = relu de l'API. Jamais « l'outil a répondu 200 » comme seule preuve.
4. **Paths inatteignables : les nommer** — dire ce qui bloque (auth, quota, entitlement, OS), couvrir le plus proche chemin réel restant. JAMAIS de silence sur un test sauté.
5. **Interdit la preuve « ça marche visiblement »** — pixels ou messages de succès ne prouvent rien.

## Règles complémentaires

- Non-déterministe (streaming, réseaux) → attendre des états observables (wait-settle), jamais de sleeps fixes.
- Mocks : ne comptent que derrière la même frontière de production qu'une dépendance externe indisponible — jamais quand ils court-circuitent la persistance réelle.
- Lire l'état via inspection après le parcours réel ; jamais invoquer des fonctions internes pour fabriquer l'état.

## Feature map (format 4 sections)

Une zone = un fichier dans ce format (index sweepable, l'agent ouvre 1 fichier par changement) :

- **Sub-features** — ce que la zone fait
- **How to get to it** — le chemin d'accès (POV utilisateur/système)
- **Driving it** — comment la piloter/vérifier avec les outils réels
- **Gotchas** — pièges, états non-évidents, historique

Zones BRANDON AI à documenter progressivement : email (Gmail/Outlook), calendar, browser, vault Obsidian, git, LiteLLM, PostgreSQL, n8n, dashboard, crons.

## Sweep de régression

Après toute modification structurelle : parcourir l'index de haut en bas, une vérification par zone, rapport « OK / ÉCHEC / INATTEIGNABLE (raison) ».