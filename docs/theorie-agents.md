# Théorie des agents — les 5 concepts, mappés au système BRANDON AI

Note de référence. Chaque concept est défini, puis relié à l'élément concret
qui l'incarne dans ce système. Rien ici n'est théorique : tout existe et
tourne sur le serveur.

## 1. Skill

Une skill est un paquet de savoir-faire réutilisable : une procédure écrite
(`SKILL.md`) que l'agent charge quand la situation s'y prête, au lieu de
réinventer la démarche à chaque fois. C'est de la documentation, pas du
code qui s'exécute tout seul.

**Ici :** 781 fichiers `SKILL.md` installés sous `~/.hermes/skills`
(vérifié le 12 nov. 2026). L'agent les consulte à la demande ; les
exclusions de sécurité (godmode, scraper furtif) sont tenues hors du
système.

## 2. Harness

Le harness est tout ce qui entoure le modèle : la boucle qui reçoit un
message, appelle le modèle, exécute ses outils, gère les erreurs, applique
les approbations et renvoie la réponse. Le modèle raisonne ; le harness
fait tourner le système de façon fiable et répétable.

**Ici :** la gateway Hermes (service systemd, Telegram, sessions), les
routines (`hermes cron`, 14 jobs), le mode bot (délégation entre profils),
les règles d'approbation (`approvals.mode: smart`, exécution sans
surveillance refusée) et les garde-fous des SOUL.

## 3. Résolveur

Le résolveur choisit *comment* répondre à une demande : quel modèle, quel
outil, quelle source. C'est la couche de décision entre l'intention et
l'exécution — routage, repli en cas de panne, sélection d'outil.

**Ici :** le proxy LiteLLM (routeur + chaîne de repli : DeepSeek V4 Flash
en ordre 1, Gemini 2.5 Flash en ordre 2, 2 tentatives), les budgets par
agent, et la sélection d'outils par l'agent lui-même (outils MCP nommés
explicitement dans les consignes, ex. l'outil MCP Gmail plutôt que l'outil
natif non connecté).

## 4. Latent vs Déterministe

- **Latent** : les appels au modèle. Probabilistes : la même demande peut
  donner des réponses différentes. Puissants pour comprendre, rédiger,
  décider dans l'ambiguïté — mais jamais une source de vérité.
- **Déterministe** : les scripts, les requêtes SQL, les serveurs MCP, les
  minuteurs. Même entrée → même sortie, vérifiable, rejouable.

**Ici :** latent = chaque appel modèle via LiteLLM (briefings, analyses,
rédaction). Déterministe = les serveurs MCP (`btp`, `crm`, `hiring`,
`traces`, `bridge`), les vues SQL, le collecteur de la page de statut, les
sauvegardes restic, le watchdog GUARDIAN. La règle du système : le latent
propose, le déterministe consigne et vérifie.

## 5. Journaling

Le journaling est l'enregistrement continu de ce qui a été décidé, fait et
observé — pour se souvenir entre les sessions, auditer après coup et ne
jamais reposer deux fois la même question tranchée.

**Ici :** les traces de décision (`audit.decision_traces`, écriture
append-only via le MCP `traces`), le graphe de contexte et les précédents
(`05-Contexte/`), les journaux du vault (ex. `07-Wiki/log.md`, tenu par
Wiki), les logs de sessions et les snapshots restic quotidiens. Exemple de
précédent consigné : SIM-008, à ne jamais reposer.
