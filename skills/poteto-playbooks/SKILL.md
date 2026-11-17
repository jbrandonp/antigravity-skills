---
name: poteto-playbooks
description: "16 playbooks pstack/brainmaxxing adaptés à Hermes."
version: 1.0.0
author: Léopold (BRANDON AI)
license: MIT
metadata:
  hermes:
    tags: [brainmaxxing, principles, pstack]
    related_skills: [bm-reflect, how, verify-brandon]
---

# poteto-playbooks — Les principes en action

## When to Use

Avant toute décision non triviale : identifier le principe applicable et le citer dans la trace de décision.

Les 16 principes brainmaxxing/pstack (Lauren Tan, MIT) traduits en playbooks actionnables Hermes. Référence : `/srv/brandon-ai/workspaces/bm/` et `/srv/brandon-ai/workspaces/plugins/`.

## Core

1. **foundational-thinking** — décisions structurelles avant le code ; data structures first.
2. **redesign-from-first-principles** — intégrer un changement comme si la contrainte avait toujours existé, pas en boulonnant.
3. **subtract-before-you-add** — supprimer la complexité avant d'ajouter. Chaque ajout doit passer le test « qu'est-ce qu'on peut supprimer à la place ? ».
4. **outcome-oriented-execution** — optimiser l'état final vérifiable, jamais les états intermédiaires.
5. **experience-first** — l'expérience (Telegram, dashboard) est le produit.
6. **exhaust-the-design-space** — 2-3 prototypes concurrents avant de choisir sur les décisions importantes.

## Architecture

7. **boundary-discipline** — validation aux frontières, confiance à l'intérieur.
8. **make-operations-idempotent** — crons/scripts re-exécutables sans casse.
9. **migrate-callers-then-delete-legacy** — pas de couche de compat par défaut.
10. **serialize-shared-state-mutations** — sérialiser les écritures d'état partagé (Postgres le fait ; respecter l'ordre dans les scripts).

## Vérification

11. **prove-it-works** — observer le réel, jamais le self-report. Voir skill `verify-brandon`.
12. **fix-root-causes** — jamais masquer un symptôme.

## Délégation

13. **cost-aware-delegation** — budget de tours/tokens par subagent, annoncer le coût d'une récurrence avant de la créer.
14. **guard-the-context-window** — contexte fini : router les gros payloads vers des fichiers, pas dans le contexte.
15. **never-block-on-the-human** — « proceed, then present » pour ce qui est réversible ; demander seulement sur l'irréversible/l'argent.

## Meta

16. **encode-lessons-in-structure** — méta-principe : un fix récurrent devient mécanisme (config, script, lint), pas instruction. C'est le cœur de bm-reflect.

## Usage

Avant toute décision non triviale : identifier le principe applicable et le citer dans la trace de décision.