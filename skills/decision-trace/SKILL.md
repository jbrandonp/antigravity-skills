---
name: decision-trace
description: "Consigne les décisions critiques dans audit.decision_traces."
version: 1.0.0
author: Léopold (BRANDON AI)
license: MIT
---

# Skill : decision-trace

## Quand utiliser ce skill

- Avant toute décision conséquente (brouillon envoyé, devis créé, exception à une règle, approbation/refus, dépense, changement de config).
- Avant de décider sur un sujet déjà traité : chercher d'abord un précédent.
- Pour tout brouillon important : suivre le cycle contexte → brouillon → trace → validation.

## Le cycle (contexte → brouillon → trace → validation)

1. **Injection de contexte** — Consulter le context graph du vault Obsidian
   (`/srv/brandon-ai/workspaces/obsidian-vault/05-Contexte/` : index, piliers,
   convictions, précédents) et les traces de décision en base. Ne jamais écrire
   depuis le vide. Ne jamais inventer ce qui est marqué « À compléter par Brandon ».
2. **Brouillon** — Produire le brouillon en appliquant le playbook
   (`06-Playbook/` : ton du canal, positions, arguments). Faits confirmés
   uniquement, sources citées si besoin.
3. **Trace de décision** — Au moment du brouillon / de l'action, consigner via
   l'outil `trace_record` (voir ci-dessous) : angle choisi, sources utilisées,
   alternatives écartées, raison.
4. **Curation (validation de Brandon)** — Un brouillon important ne part jamais
   sans sa validation du texte exact (approbations Hermes). Brandon est le pilote
   et le curateur final. Le cycle ne s'auto-approuve jamais.

## Mécanisme : le MCP `traces` (seul canal d'écriture)

Le MCP postgres des agents est verrouillé en lecture seule (son outil `query`
ouvre une transaction READ ONLY) : il ne peut pas écrire. **Ne jamais tenter
d'INSERT par ce canal, et ne jamais contourner par le terminal avec l'URL
d'écriture.** Le MCP `traces` est le seul canal : deux outils, requêtes
paramétrées uniquement, ajout seul (ni UPDATE ni DELETE).

### Chercher un précédent — `trace_search`

Appeler `trace_search` avec un mot-clé (entité, sujet ou mot de la décision),
avant toute décision sur un sujet déjà traité. Exemple : `trace_search("basic-fit")`.

Si un précédent existe : le suivre, ou consigner explicitement pourquoi on s'en
écarte (nouvelle trace via `trace_record`). Si aucun précédent n'existe : le dire
plainement, puis décider selon les règles et tracer.

### Écrire une trace — `trace_record`

Paramètres : `agent` (ton profil), `entity` (ex. `finances/abonnements`),
`topic` (sujet court), `decision` (une phrase), `inputs` (JSON : ce qui a été
consulté), `policies_applied` (JSON : liste des règles appliquées),
`alternatives` (JSON : liste des options écartées et pourquoi), `rationale`
(pourquoi ce choix), `approver` (Brandon, ou l'agent si autonome dans ses
bornes), `outcome` (`decided` / `refused` / `pending` / `executed`),
`precedent_links` (JSON : liste des notes du graph, ex.
`["05-Contexte/Precedents/SIM-008.md"]`).

Règles d'écriture :
- `inputs` : ce qui a été consulté (sources, faits, chiffres) — jamais inventé.
- `policies_applied` : les règles du dossier / du SOUL appliquées.
- `alternatives` : les options écartées ET pourquoi.
- `rationale` : pourquoi ce choix plutôt qu'un autre, en une ou deux phrases.
- `precedent_links` : chemins des notes du graph liées.

## Schéma (référence — table `audit.decision_traces`)

id, ts, agent, entity, topic, decision, inputs (jsonb),
policies_applied (text[]), alternatives (jsonb), rationale, approver, outcome,
precedent_links (text[]). Le rôle lecteur n'y a que SELECT ; l'écriture passe
par le serveur `traces` (rôle applicatif, ajout seul).

## Limites

- Une trace erronée se corrige par une nouvelle trace qui la référence, jamais
  en l'effaçant (l'historique ne se réécrit pas).
- Ne jamais tracer de secret (clé, token, mot de passe) dans une trace.
- Une trace n'est pas une approbation : les actions importantes restent soumises
  à la validation de Brandon (approbations Hermes).
