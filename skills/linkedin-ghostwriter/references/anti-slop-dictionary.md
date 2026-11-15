# Dictionnaire Anti-Slop LinkedIn (Bilingue FR / EN)

Ce guide répertorie les tics formels, syntaxiques et lexicaux qui trahissent immédiatement un texte rédigé par un grand modèle de langage (Claude, ChatGPT, etc.) et propose les remplacements humains directs.

---

## 🇫🇷 1. La Blacklist Francophone

### A. Mots Interdits & Vocabulaire Creux

| Mot ou expression interdite | Pourquoi c'est du slop | Remplacement direct |
| :--- | :--- | :--- |
| **décryptage** | Tic journalistique pompeux | "analyse", "ce qui s'est passé", ou suppression |
| **incontournable** | Paresseux, dithyrambique | "utile", "requis", ou expliquer pourquoi concrètement |
| **catalyseur** | Métaphore de consultant fatiguée | "accélérateur", "déclencheur", "moteur" |
| **révolutionner** | Hyperbole sans preuve | "changer", "simplifier", "diviser le temps par 2" |
| **holistique** | Jargon creux | "global", "complet", ou suppression |
| **synergie** | Cliché corporate par excellence | "coopération", "gain mutuel", "accord" |
| **pierre angulaire** | Cliché d'écriture automatique | "base", "fondation", "le cœur de" |
| **force motrice** | Formule scolaire | "la raison pour laquelle", "ce qui pousse" |
| **gage de** | Préciosité désuète | "prouve que", "assure", "garantit" |
| **s'avérer** | Tic d'écriture des LLMs | Utiliser simplement le verbe "être" ("c'est") |
| **écosystème** | Utilisé à tort pour désigner 3 outils | "notre stack", "notre marché", "notre équipe" |
| **enjeu crucial** | Emphase artificielle | "gros problème", "risque majeur" |
| **résilience** | Utilisé comme mot-valise moralisateur | "endurance", "capacité à encaisser" |
| **pépite / maestro / ovni** | Éloges creux de réseau social | Décrire le fait mesurable sans adjectif |

---

### B. Structures de Phrases Robotiques

#### 1. La Fausse Opposition ("Il ne s'agit pas de X, mais de Y")
- ❌ *Slop IA* : "Il ne s'agit pas simplement de coder plus vite, mais de concevoir des architectures pérennes."
- ✅ *Humain* : "Coder vite ne sert à rien si l'architecture s'écroule au premier pic de charge."

#### 2. L'Ouverture Cosmique ("Dans un monde où...")
- ❌ *Slop IA* : "Dans un monde en constante évolution où l'IA transforme nos métiers..."
- ✅ *Humain* : "En 6 mois, les équipes qui utilisent Claude ont divisé par 3 leur temps de dev."

#### 3. La Question Rhétorique Prévisible ("La clé ?")
- ❌ *Slop IA* : "La clé ? L'écoute active de ses utilisateurs."
- ✅ *Humain* : "On a passé 20 heures au téléphone avec nos 15 premiers clients."

#### 4. Le Rythme Ternaire Forcé (Règle de Trois)
Les LLMs ont une tendance statistique lourde à grouper les termes par 3 :
- ❌ *Slop IA* : "Une solution rapide, intuitive et puissante." / "Analyser, adapter et réussir."
- ✅ *Humain* : "Une solution rapide qui ne plante pas." / "Regarder les logs et couper le serveur."

---

## 🇬🇧 2. The English Blacklist

| Banned Term | Reason | Human Direct Replacement |
| :--- | :--- | :--- |
| **delve** | The single biggest statistical LLM fingerprint | "explore", "look into", "break down" |
| **tapestry** | Overused poetic metaphor in technical context | "complexity", "mix", "structure" |
| **leverage** | Corporate buzzword verb | "use", "rely on", "take advantage of" |
| **foster** | Vague consultative verb | "build", "encourage", "grow" |
| **harness** | Cliché power verb | "use", "channel", "apply" |
| **crucial / pivotal** | Unearned drama | "important", "vital", or just state the impact |
| **testament to** | Formal filler phrase | "shows that", "proves" |
| **game-changer** | Over-hyped exaggeration | State the concrete metric instead |
| **unlock** | Clickbaity marketing verb | "access", "achieve", "open up" |
| **beacon / nexus** | Flowery literary words | "hub", "center", "example" |

---

## 🧟 3. The Zombie Test (Active Voice)

Le passif rend la lecture molle et anonyme. Les LLMs l'utilisent pour masquer leur manque de conviction.

- **Le Test** : Si tu peux insérer **"[par des zombies]"** après le verbe, ta phrase est passive.
  - *Exemple* : "Des décisions stratégiques ont été prises [par des zombies]."
  - *Correction Active* : "On a pris deux décisions radicales."
  - *Exemple* : "Les erreurs de déploiement doivent être évitées [par des zombies]."
  - *Correction Active* : "Vous devez bloquer les déploiements non testés."

---

## 🛑 4. Les Conclusions Interdites

Tout post se terminant par l'une de ces phrases est immédiatement rejeté :
- ❌ "Et vous, quel est votre avis là-dessus ?"
- ❌ "Et vous, comment gérez-vous cela au quotidien ?"
- ❌ "Le débat est ouvert en commentaires !"
- ❌ "Rappelez-vous : à la fin de la journée, seule l'humain compte."

**Remplacements Recommandés** :
1. **L'Axiome Brutal** : "La complexité inutile est la taxe que paient les équipes sans vision."
2. **Le Déclencheur de Conversation Ciblé** : "Si vous avez déjà testé cette approche sous PostgreSQL, dites-moi comment vous gérez les locks."
3. **Le Direct Resource CTA** : "J'ai documenté les 4 scripts de migration dans ce gist (lien en 1er commentaire)."
