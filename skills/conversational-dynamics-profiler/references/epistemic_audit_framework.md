# Grille d'Audit Épistémique & Rigueur Clinique

Ce document définit les standards méthodologiques stricts pour l'analyse de corpus textuels privés (messageries instantanées, emails, SMS). Il vise à éliminer les biais d'interprétation, la psychiatrisation sauvage et les hallucinations de l'IA.

---

## 1. La Taxonomie des 4 Niveaux de Certitude

Chaque affirmation, citation ou conclusion doit porter un tag explicite :

| Tag | Définition Opérationnelle | Critère de Preuve | Exemple |
|---|---|---|---|
| **`[Vérifié]`** | Fait matériel, mesuré ou directement attesté dans la donnée brute. | Timestamp précis, capture de profil, métrique déterministe, URL vérifiable. | Compte Instagram privé avec 0 post ; 382 réactions mesurées ; 2 001 messages extraits. |
| **`[Déclaré]`** | Affirmation faite par un interlocuteur sur lui-même, un tiers ou son passé. | Parole rapportée fidèlement, sans validation externe de sa véracité objective. | *« J'ai deux PC et une PS5 »* ; *« Mon père vient de Caltanissetta »* ; *« J'ai fait des tests au CVIM »*. |
| **`[Pattern]`** | Comportement récurrent, régularité statistique ou séquence cyclique observable. | Répétition mesurable sur ≥ 3 occurrences distinctes dans le temps. | Relance systématique après les silences de >24h (8/9) ; latence de réponse médiane < 30 s. |
| **`[Hypothèse]`** | Modèle interprétatif, déduction clinique, conjecture psychologique ou projection. | Cadre théorique explicite (attachement, mentalisation), révocable par des contre-preuves. | Attachement insécure-anxieux avec stratégies évitantes secondaires ; besoin de contrôle procédural. |

---

## 2. Garde-Fous Déontologiques & Anti-Psychiatrie Sauvage

1. **Interdiction du diagnostic médical/psychiatrique formel**  
   Aucun trouble de la personnalité (Borderline, Narcissique, Bipolaire, TDAH, TSA) ne peut être diagnostiqué à partir de logs de chat. Un diagnostic exige :
   - Un entretien clinique approfondi en présentiel.
   - L'histoire développementale et médicale complète.
   - L'évaluation du retentissement fonctionnel dans plusieurs sphères de vie (travail, social, famille).
   - L'exclusion des causes organiques et toxiques.  
   *Règle :* Décrire des **modes de fonctionnement, des styles relationnels et des patterns de communication**, jamais des pathologies.

2. **Le Test de Falsifiabilité (Popper)**  
   Toute hypothèse psychologique doit s'accompagner de ses critères de réfutation :
   - *« Que faudrait-il observer dans les données futures pour prouver que ce modèle est faux ? »*
   - Si un modèle interprétatif explique tout et son contraire, il est épistémiquement nul.

3. **L'Intégration Systémique du Contre-Argument**  
   Avant de conclure à un trait de personnalité individuel, tester systématiquement les explications situationnelles :
   - **Biais de lune de miel** (l'euphorie du début amplifie artificiellement la dépendance et l'intensité).
   - **Biais culturel/régional** (l'expressivité méditerranéenne ou populaire utilise des hyperboles qui ne sont pas des crises émotionnelles).
   - **Biais de plateforme** (Instagram et Messenger récompensent la fragmentation et les réactions rapides par rapport au mail ou au téléphone).
   - **Biais du partenaire miroir** (l'intensité de l'un est souvent une réponse mécanique à la réserve de l'autre).

---

## 3. Protocole de Traitement des Données Brutes

- **Dédoublonnage strict** : Toujours vérifier que les requêtes API paginées n'ont pas ré-indexé des messages chevauchants.
- **Résolution temporelle** : Pour les calculs de latence (RTT), utiliser les horodatages à la milliseconde. Ne pas calculer des vitesses de réponse précises sur des données tronquées à la minute.
- **Normalisation des citations** : Nettoyer les espaces insécables, apostrophes typographiques (`’` vs `'`) et ligatures (`œ`, `æ`) avant d'affirmer qu'une citation est absente d'un corpus.
- **Respect du secret et sanctuarisation** : Ne jamais stocker de mots de passe, tokens ou informations d'identification bancaire dans les rapports de profiling.
