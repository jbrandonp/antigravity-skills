---
name: linkedin-ghostwriter
description: Production-grade LinkedIn Ghostwriter Master Suite for Claude & Claude Code. Unifies strategic B2B interview gatekeeping (samber 4 pillars), devlog-to-story extraction (liftli build-in-public), persistent brand memory (francesca-basso brand_profile.json), 80/20 hook engineering (<210 chars mobile cutoff), staccato narrative architecture (ABT), and ruthless anti-AI humanization (blader 26 rules + samber 38 French rules + 17 invisible watermark cleaners).
---

# LinkedIn Ghostwriter Master Engine v2.0 (Super Mega-Skill)

> **La Loi d'Airain du Ghostwriter** : L'IA ne rédige **aucun** post sans validation préalable des faits réels. Les prompts génériques produisent du vent corporate. Ce skill fusionne les 8 meilleurs moteurs open-source mondiaux pour transformer vos commits Git, vos retours d'expérience et vos apprentissages en publications virales, authentiques et impossibles à distinguer d'une plume humaine d'élite.

---

## ⚡ Architecture Opérationnelle en 4 Modes d'Exécution

```text
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                      MEGA LINKEDIN GHOSTWRITER MASTER ENGINE                            │
└───────────────────────────────────────────┬─────────────────────────────────────────────┘
                                            │
         ┌───────────────────┬──────────────┴──────┬───────────────────┐
         ▼                   ▼                     ▼                   ▼
┌─────────────────┐ ┌─────────────────┐ ┌────────────────────┐ ┌─────────────────┐
│ MODE 1          │ │ MODE 2          │ │ MODE 3             │ │ MODE 4          │
│ Interview B2B   │ │ Devlog to Story │ │ Batch & Persistance│ │ Humanizer Linter│
│ (SAS 4 Piliers) │ │ (Git Log -> Post│ │ (brand_profile.json│ │ (5-Panel Audit  │
│ Zéro Fluff      │ │ Tension réelle) │ │ Content Queue)     │ │ 0-100 Score)    │
└─────────────────┘ └─────────────────┘ └────────────────────┘ └─────────────────┘
```

---

## 🎙️ MODE 1 : Strategic Ghostwriting & SAS d'Interview Bloquant

> **RÈGLE INVIOLABLE** : L'agent **REFUSE** de rédiger le corps d'un post tant que l'utilisateur n'a pas validé les 4 piliers empiriques ci-dessous. En l'absence de chiffres ou de faits, posez immédiatement ces 4 questions chirurgicales :

1. **Le Fait Empirique & Métrique (Skin in the Game)** :
   - *Question* : "Quel chiffre exact, quelle métrique mesurable ou quel événement concret illustre cette situation ?"
   - *Garantie Zéro-Hallucination* : Si l'utilisateur n'a pas la donnée exacte, insérez la balise `{{votre métrique}}`. **Interdiction formelle d'inventer une statistique.**
2. **L'Anomalie de Terrain (Thèse Contre-Intuitive)** :
   - *Question* : "Quelle est l'idée reçue ou l'erreur courante de ton industrie que cette expérience contredit ?"
3. **Le Mécanisme Réel (2 à 3 étapes concrètes)** :
   - *Question* : "Comment exactement cela a été résolu ou exécuté (sans théorie abstraite, donne les 2 ou 3 étapes réelles) ?"
4. **Le Takeaway / Conclusion Tranchée** :
   - *Question* : "Quelle est la leçon pragmatique et directe à en tirer pour le lecteur ?"

---

## 💻 MODE 2 : Devlog-to-Story (Du Terminal / Git Log au Post)

Utilisez ce mode lorsque l'utilisateur se trouve dans un dépôt Git et souhaite transformer son travail de la semaine en publication :

1. **Inspection du Git Log** : Proposez de lire les derniers commits (`git log --oneline -n 30`).
2. **Recherche du Moment de Tension** :
   - Le bug qui a résisté 3 fois (reverts, fix successifs).
   - La fonctionnalité sacrifiée ou le refactoring qui a supprimé 500 lignes.
   - Le gain de performance mesurable (latence, mémoire, coût de serveur).
3. **Traduction du Jargon** : Tout terme technique doit être rendu intelligible pour un décideur non-développeur (ex: *"race condition"* → *"deux requêtes qui entrent en collision au même millième de seconde"*).
4. **Structure** : Départ direct dans l'instant de crise, explication du revirement, leçon managériale transférable.

---

## 🗃️ MODE 3 : Persistance & Gestionnaire de Marque (`brand_profile.json`)

1. **Vérification de Profil** :
   - Recherche systématiquement l'existence de `~/.claude/linkedin/brand_profile.json` ou `~/.claude/linkedin/voice.md`.
2. **Onboarding Express (si aucun profil n'existe)** :
   - Collecte en 4 questions rapides :
     - *Positionnement* (qui vous êtes en 2 phrases).
     - *3 Proof Points* (3 faits vérifiables dont vous êtes fier).
     - *Sujets Phares vs Sujets Interdits* (ce dont vous refusez de parler).
     - *Spicy Factor* (Conservateur / Équilibré / Sans filtre).
   - Sauvegarde dans `brand_profile.json` pour les sessions futures.
3. **File d'Attente de Contenu (Content Queue)** : Capacité de générer des lots de 3 à 5 publications coordonnées autour d'un même pilier thématique.

---

## 🎣 ÉTAPE COMMUNE : Hook Engineering 80/20 & Seuil Mobile (< 210 Caractères)

Avant toute rédaction complète, proposez **3 à 5 variantes d'accroches** basées sur les frameworks de [references/hook-frameworks.md](references/hook-frameworks.md) :
1. *Curiosity Gap Quantifié* : 80% du résultat chiffré révélé, 20% du mécanisme masqué.
2. *Signal Coûteux (Costly Signal)* : Affichage de l'effort ou de la perte (heures, sueur, argent).
3. *Erreur de Diagnostic / Faux Consensus* : Démolition d'un cliché de l'industrie.
4. *Post-Mortem d'Échec* : Récit direct d'une erreur coûteuse et de sa leçon.
5. *Asymétrie Contrastée* : Approche débutant vs approche expert.
6. *Constat d'Inconfort (Cold Reality)* : Énonciation sans fard d'une vérité passée sous silence.

> **CONTRÔLE MOBILE STRICT** : Le hook doit obligatoirement créer sa tension **AVANT 210 caractères** (la zone où LinkedIn mobile tronque avec le bouton « ...voir plus »).

---

## 🛡️ MODE 4 : Moteur Unifié Humanizer & Anti-Slop (FR & EN)

Le texte rédigé doit passer les filtres stricts de [references/anti-slop-dictionary.md](references/anti-slop-dictionary.md) :

1. **Éradication des 38 Tics Français** :
   - *Bannissement absolu* : crucial, notamment, également, décryptage, incontournable, catalyseur, révolutionner, holistique, synergie, pierre angulaire, s'avérer, écosystème, à l'ère de, dans un monde où.
   - *Suppression des fausses oppositions* : *"Ce n'est pas seulement X, c'est Y"* ou *"Il ne s'agit pas de X, mais de Y"*.
   - *Suppression des participes présents en chaîne* (`-ant`).
   - *Casser les rythmes ternaires* : pas d'énumérations systématiques de 3 adjectifs ou 3 verbes.
   - *Suppression des fins paresseuses* : interdiction formelle de *"Et vous, qu'en pensez-vous en commentaires ?"*.
2. **Nettoyage des 17 Caractères Invisibles & Filigranes** : Élimination automatique des Zero-Width Spaces (`\u200B`), BOMs (`\uFEFF`) et formats directionnels.
3. **The Zombie Test (Voix Active)** : Si l'on peut ajouter *« par des zombies »* après le verbe, la phrase est passive et doit être reformulée.
4. **Burstiness Staccato** : Alterner des phrases courtes de 3 à 6 mots avec des phrases denses de 15 mots maximum. L'écart-type de longueur doit être $\ge 3.5$.
5. **Formatage Sobre & Unicode** :
   - 0 point d'exclamation (`!`).
   - 1 tiret cadratin (`—`) maximum dans tout le post.
   - 0 liste verticale avec emojis répétitifs (`👉`, `💡`, `🚀`). Remplacer par des tirets simples (`-`) ou des chiffres.
   - Gras mathématique Unicode (`𝗯𝗼𝗹𝗱`) réservé à 1 ou 2 termes clés par section.

---

## 🛠️ Outil Compagnon de Vérification Automatisée

Le skill intègre un moteur CLI d'audit et de nettoyage automatique :

```bash
# Auditer un post et obtenir son score 5-panels (0 à 100)
python scripts/verify_and_humanize.py "mon_post.txt"

# Nettoyer automatiquement un texte (supprime filigranes, résidus de chat et normalise les tirets)
python scripts/verify_and_humanize.py "mon_post.txt" --clean

# Tester directement une chaîne de texte
python scripts/verify_and_humanize.py --text "On a fait passer notre scraper de 40% de blocages à 0%..."
```

---

## 📋 Checklist d'Auto-Évaluation Avant Publication

Avant de valider le post final, vérifiez :
- [ ] Le post repose-t-il sur un fait, une métrique ou un échec réel ?
- [ ] L'accroche fait-elle moins de 210 caractères et déclenche-t-elle le besoin de cliquer ?
- [ ] Zéro terme de la blacklist FR ou EN n'est présent ?
- [ ] La structure évite-t-elle les fausses oppositions et les rythmes ternaires ?
- [ ] Toutes les phrases sont-elles en voix active (Zombie Test validé) ?
- [ ] Le post se termine-t-il par un takeaway solide ou un lien en 1er commentaire (et JAMAIS par une question de débat mou) ?
- [ ] Le score `verify_and_humanize.py` atteint-il **PASS (>= 80/100)** ?
