# Recrutement IA — playbook

Système prêt, en attente du premier usage réel. Cadre honnête : Brandon n'a
pas d'entreprise ni de candidats pour l'instant. Ce playbook et les outils
associés servent le jour où un besoin de recrutement apparaît — rien ne
tourne « à vide » en attendant.

## Outils

Serveur MCP `hiring` (profil default uniquement), base `brandon_ai`,
schéma `hiring` :

- `hiring_add_candidate` — ajoute un candidat au stade « reçu ».
- `hiring_list_candidates` — liste, éventuellement filtrée par stade.
- `hiring_screen_candidate` — consigne un tri (critères JSON, score 0-100,
  recommandation). Ne change pas le stade.
- `hiring_move_candidate` — déplace un candidat d'un stade à l'autre.

Stades : reçu → tri → entretien → offre → embauché / refusé.

La table `hiring.messages` stocke les messages en BROUILLON (`sent_at` NULL).
Aucun outil d'envoi n'existe : rien ne part jamais depuis ce système.

## Règle absolue

Rien n'est envoyé à un candidat sans que Brandon ait validé le texte exact.
L'agent prépare le brouillon, Brandon valide, et seulement ensuite le message
peut partir — par le canal que Brandon choisit, jamais automatiquement.

## Étapes

1. **Réception** : chaque candidature reçue est ajoutée avec
   `hiring_add_candidate` (nom, e-mail, source, rôle visé, résumé du CV).
2. **Tri** : `hiring_screen_candidate` avec les critères ci-dessous, un score
   de 0 à 100 et une recommandation en une phrase. Puis
   `hiring_move_candidate` vers « tri » (ou « refusé » si éliminé).
3. **Entretien** : brouillon d'invitation (modèle B) soumis à Brandon.
   Après validation, envoi manuel. Stade → « entretien ».
4. **Offre / refus** : brouillon soumis à Brandon (modèle C pour un refus).
   Stade → « offre », « embauché » ou « refusé ».
5. **Journal** : chaque décision importante est consignée dans une trace
   de décision (`trace_record`) avec la raison.

## Critères de tri (par défaut, à adapter par rôle)

- Adéquation expérience / rôle visé.
- Français écrit (qualité du CV et du message).
- Disponibilité et contraintes (lieu, horaires, télétravail).
- Motivation visible (message personnalisé, recherche sur le poste).
- Signaux d'alerte : CV incohérent, copier-coller générique, exigences
  irréalistes.

Le score n'est qu'une aide : il ne décide jamais seul. Un score bas avec
une vraie motivation mérite un regard humain ; un score haut ne dispense
pas de vérifier les affirmations du CV.

## Modèles d'e-mails — BROUILLONS (placeholders à remplir)

### A. Accusé de réception

> Objet : Candidature reçue — {{rôle}}
>
> Bonjour {{prénom}},
>
> Merci pour votre candidature au poste de {{rôle}}. Nous l'avons bien
> reçue et nous revenons vers vous sous {{délai}}.
>
> Cordialement,
> Brandon Palhano

### B. Invitation à un entretien

> Objet : Entretien — {{rôle}}
>
> Bonjour {{prénom}},
>
> Votre profil a retenu notre attention pour le poste de {{rôle}}.
> Seriez-vous disponible pour un entretien {{format}} le {{date}} à
> {{heure}} ?
>
> N'hésitez pas à me proposer un autre créneau si celui-ci ne convient pas.
>
> Cordialement,
> Brandon Palhano

### C. Refus poli

> Objet : Suite de votre candidature — {{rôle}}
>
> Bonjour {{prénom}},
>
> Merci pour votre candidature et pour le temps consacré. Après étude,
> nous ne donnons pas suite pour le poste de {{rôle}}, car {{raison courte
> et factuelle}}.
>
> Nous vous souhaitons une bonne continuation dans vos recherches.
>
> Cordialement,
> Brandon Palhano
